# Three-second synthetic example

This original clip shows a white square on a black background. It demonstrates frame extraction, review, and report generation; it does not measure analysis quality on real gameplay. The generator and example review are provided under the repository's MIT license and contain no third-party footage or assets.

Follow the [installation guide](../../README.md#quick-start) to install Python, rea-game, FFmpeg, and ffprobe. Run all commands below from the repository root.

macOS / Linux, with the virtual environment activated:

```sh
python examples/synthetic/create_video.py out/synthetic.mp4
rea-game extract out/synthetic.mp4 -o out/synthetic --interval 1
```

Windows PowerShell:

```powershell
$env:PYTHONUTF8 = "1"
.\.venv\Scripts\python.exe examples/synthetic/create_video.py out/synthetic.mp4
.\.venv\Scripts\rea-game.exe extract out/synthetic.mp4 -o out/synthetic --interval 1
```

Inspect the three images in `out/synthetic/frames/` and play `out/synthetic.mp4` around the one-second mark. The square is on the left at 0 seconds and closer to the center at 1 and 2 seconds. The clip has no audio track. Once you have checked the footage, copy the example review and generate the report.

macOS / Linux:

```sh
cp examples/synthetic/review.json out/synthetic/review.json
rea-game report out/synthetic
```

Windows PowerShell:

```powershell
Copy-Item examples/synthetic/review.json out/synthetic/review.json
.\.venv\Scripts\rea-game.exe report out/synthetic
```

The result is `out/synthetic/report.md`. Compare it with the [example report](report.md). The source path will differ between machines; the rest of the report should match. Empty sections say "Not yet reviewed."

Do not reuse this example's observations for other videos. The generator refuses to overwrite an existing video, and extraction requires a new output directory. To repeat the example, choose a new video path and output directory. Failed extraction removes the directory created by that run.
