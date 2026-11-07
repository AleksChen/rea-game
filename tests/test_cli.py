import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class WorkflowTest(unittest.TestCase):
    def test_extract_uses_same_video_track_for_metadata_and_frames(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            # Keep a Unicode filename and a space to exercise path handling.
            video, output = root / '\u591a\u8f68 video.mp4', root / 'analysis'
            # Audio precedes both video tracks so absolute and video-only indices differ.
            # The second video is default and larger; automatic selection would pick it.
            subprocess.run([
                'ffmpeg', '-v', 'error',
                '-f', 'lavfi', '-i', 'anullsrc=r=8000:cl=mono:d=4',
                '-f', 'lavfi', '-i', 'color=c=red:s=64x48:r=10:d=2',
                '-f', 'lavfi', '-i', 'color=c=blue:s=320x240:r=10:d=4',
                '-map', '0:a', '-map', '1:v', '-map', '2:v',
                '-c:a', 'aac', '-c:v', 'mpeg4',
                '-disposition:v:0', '0', '-disposition:v:1', 'default', str(video),
            ], check=True)
            result = subprocess.run([
                sys.executable, '-m', 'rea_game.cli', 'extract', str(video),
                '-o', str(output), '--interval', '1',
            ], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            evidence = json.loads((output / 'evidence.json').read_text(encoding='utf-8'))
            self.assertEqual((evidence['width'], evidence['height']), (64, 48))
            self.assertAlmostEqual(evidence['duration_seconds'], 2)
            self.assertEqual([f['time_seconds'] for f in evidence['frames']], [0, 1])
            for frame in evidence['frames']:
                metadata = json.loads(subprocess.check_output([
                    'ffprobe', '-v', 'error', '-show_streams', '-of', 'json',
                    str(output / frame['image']),
                ]))['streams'][0]
                self.assertEqual((metadata['width'], metadata['height']), (64, 48))

    def test_extract_review_report(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            video, output = root / 'sample.mp4', root / 'analysis'
            subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', 'testsrc2=size=64x48:rate=10:duration=2', '-c:v', 'mpeg4', str(video)], check=True)
            def cli(*args):
                return subprocess.run([sys.executable, '-m', 'rea_game.cli', *map(str, args)], capture_output=True, text=True)
            extracted = cli('extract', video, '-o', output, '--interval', 1)
            self.assertEqual(extracted.returncode, 0, extracted.stderr)
            self.assertIn('Extracted 2 frames.', extracted.stdout)
            evidence = json.loads((output / 'evidence.json').read_text(encoding='utf-8'))
            self.assertEqual([f['time_seconds'] for f in evidence['frames']], [0, 1])
            self.assertTrue(all((output / f['image']).is_file() for f in evidence['frames']))
            self.assertNotEqual(cli('report', output).returncode, 0)
            review = json.loads((output / 'review.json').read_text(encoding='utf-8'))
            review['core_loop'] = [{'text': 'The scene changes.', 'status': 'observation', 'times': [1]}]
            review['rules'] = [{'text': 'The scene may change on a timer.', 'status': 'inference', 'times': [1]}]
            review['remake'] = [{'text': 'Build a minimal scene.', 'status': 'proposal', 'times': []}]
            review['unknowns'] = [{'text': 'Does player input affect the scene?', 'status': 'unverified', 'times': []}]
            (output / 'review.json').write_text(json.dumps(review, ensure_ascii=False), encoding='utf-8')
            generated = cli('report', output)
            self.assertEqual(generated.returncode, 0, generated.stderr)
            self.assertIn('Report saved to ', generated.stdout)
            report = (output / 'report.md').read_text(encoding='utf-8')
            self.assertTrue(report.startswith('# Gameplay Analysis\n'))
            self.assertIn('Recording duration: 2.0 seconds', report)
            self.assertIn('## Core Gameplay Loop', report)
            self.assertIn('Not yet reviewed.', report)
            self.assertIn('**Observation**: The scene changes. (Evidence: 1s)', report)
            self.assertIn('**Inference**: The scene may change on a timer. (Evidence: 1s)', report)
            self.assertIn('**Proposal**: Build a minimal scene.', report)
            self.assertIn('**Unverified**: Does player input affect the scene?', report)
            review['core_loop'][0]['times'] = [99]
            (output / 'review.json').write_text(json.dumps(review), encoding='utf-8')
            self.assertNotEqual(cli('report', output).returncode, 0)
            self.assertNotEqual(cli('extract', video, '-o', output).returncode, 0)


if __name__ == '__main__':
    unittest.main()
