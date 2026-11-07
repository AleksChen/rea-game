import argparse
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from rea_game.cli import SECTIONS, extract, report


class ValidationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.evidence = {"source": "sample.mp4", "duration_seconds": 2,
                         "frames": [{"time_seconds": 0, "image": "frames/1.jpg"}]}
        self.review = {key: [] for key in SECTIONS}
        self.review["art"] = [{"text": "A square", "status": "observation", "times": [0]}]

    def write_inputs(self, evidence, review):
        for name, value in (("evidence", evidence), ("review", review)):
            (self.root / f"{name}.json").write_text(json.dumps(value), encoding="utf-8")

    def test_bad_evidence_is_rejected_without_overwriting_report(self):
        bad = [None, [], {}, {**self.evidence, "source": 1},
               {**self.evidence, "frames": []},
               {**self.evidence, "frames": [None]},
               {**self.evidence, "frames": [{"time_seconds": True, "image": "a"}]}]
        for duration in (None, True, "2", 0, -1, float("nan"), float("inf"), 10**400):
            bad.append({**self.evidence, "duration_seconds": duration})
        target = self.root / "report.md"
        target.write_text("keep", encoding="utf-8")
        for evidence in bad:
            with self.subTest(evidence=evidence):
                self.write_inputs(evidence, self.review)
                with self.assertRaises(ValueError):
                    report(argparse.Namespace(output=self.root))
                self.assertEqual(target.read_text(encoding='utf-8'), "keep")

    def test_review_typos_and_invalid_entries(self):
        bad = [{**self.review, "core_lop": []}, {"art": {}}, []]
        for item in (
            {"text": "x", "status": "observation", "time": [1]},
            {"text": "x", "status": "observation", "times": []},
            {"text": " ", "status": "proposal"},
            {"text": "x", "status": "invalid"},
            {"text": "x", "status": "inference", "times": []},
            {"text": "x", "status": "\u89c2\u5bdf", "times": [0]},
            {"text": "x", "status": []},
        ):
            bad.append({"art": [item]})
        for time in (True, -1, 3, "1", None, float("nan"), float("inf"), 10**400):
            bad.append({"art": [{"text": "x", "status": "observation", "times": [time]}]})
        for review in bad:
            with self.subTest(review=review):
                self.write_inputs(self.evidence, review)
                with self.assertRaises(ValueError):
                    report(argparse.Namespace(output=self.root))

    def test_malformed_files_show_cli_error_without_traceback(self):
        self.write_inputs(self.evidence, self.review)
        for contents in ("{", "[]", '{"duration_seconds": "bad"}'):
            (self.root / "evidence.json").write_text(contents, encoding='utf-8')
            result = subprocess.run([sys.executable, "-m", "rea_game.cli", "report", str(self.root)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn("rea-game:", result.stderr)
            self.assertNotIn("Traceback", result.stderr)

    def test_extraction_failure_cleanup_retry_and_existing_directory(self):
        video = self.root / "sample.mp4"
        video.touch()
        output = self.root / "output"
        args = argparse.Namespace(video=video, output=output, interval=1)
        metadata = json.dumps({"streams": [{"index": 0, "codec_type": "video", "duration": "2"}]})
        def fail(cmd):
            if cmd[0] == "ffprobe":
                return metadata
            Path(cmd[-1]).write_text("partial")
            raise ValueError("simulated failure")
        with patch("rea_game.cli.run", side_effect=fail):
            with self.assertRaisesRegex(ValueError, "simulated failure"):
                extract(args)
        self.assertFalse(output.exists())
        def succeed(cmd):
            if cmd[0] == "ffprobe":
                return metadata
            Path(cmd[-1]).touch()
            return ""
        with patch("rea_game.cli.run", side_effect=succeed):
            extract(args)
        saved = (output / "evidence.json").read_bytes()
        with patch("rea_game.cli.run") as runner:
            with self.assertRaisesRegex(ValueError, "output directory already exists"):
                extract(args)
            runner.assert_not_called()
        self.assertEqual((output / "evidence.json").read_bytes(), saved)

    def test_missing_tool_and_failed_tool_are_friendly(self):
        from rea_game.cli import run
        for error in (FileNotFoundError(2, "missing", "ffprobe"),
                      subprocess.CalledProcessError(1, ["ffmpeg"], stderr="bad video")):
            with self.subTest(error=error), patch("rea_game.cli.subprocess.run", side_effect=error):
                with self.assertRaises(ValueError):
                    run(["ffprobe"])

    def test_interval_validation(self):
        video = self.root / "sample.mp4"
        video.touch()
        for interval in (0, -1, float("nan"), float("inf")):
            with self.subTest(interval=interval), self.assertRaises(ValueError):
                extract(argparse.Namespace(video=video, output=self.root / "new", interval=interval))
        self.assertFalse((self.root / "new").exists())

    def test_tiny_interval_is_rejected_before_creating_output(self):
        video = self.root / "sample.mp4"
        video.touch()
        output = self.root / "output"
        metadata = json.dumps({"streams": [{"index": 0, "codec_type": "video", "duration": "2"}]})
        for interval in (1e-309, 5e-324):
            with self.subTest(interval=interval), patch("rea_game.cli.run", return_value=metadata) as runner:
                with self.assertRaisesRegex(ValueError, "interval is too small"):
                    extract(argparse.Namespace(video=video, output=output, interval=interval))
                self.assertFalse(output.exists())
                self.assertEqual(runner.call_count, 1)

    def test_tiny_interval_shows_cli_error_without_traceback(self):
        video = self.root / "sample.mp4"
        subprocess.run([
            "ffmpeg", "-v", "error", "-f", "lavfi", "-i",
            "color=c=black:s=64x48:r=10:d=2", "-c:v", "mpeg4", str(video),
        ], check=True)
        output = self.root / "output"
        result = subprocess.run([
            sys.executable, "-m", "rea_game.cli", "extract", str(video),
            "-o", str(output), "--interval", "1e-309",
        ], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 1)
        self.assertIn("rea-game: The interval is too small", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
