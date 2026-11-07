# Contributing

rea-game focuses on extracting evidence from local gameplay recordings, recording a structured review, and generating a Markdown report. It does not automatically recover a game's complete rules or generate a playable game.

## Local development

You need Python 3.10 or later, FFmpeg, and ffprobe. Follow the [README](README.md#quick-start) to install dependencies and create a virtual environment. Run the following commands from the repository root.

macOS / Linux:

```sh
source .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests
```

Windows PowerShell (using the virtual environment's executables directly):

```powershell
$env:PYTHONUTF8 = "1"
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

Add regression tests when changing behavior. Use English for public documentation, CLI messages, examples, and report templates. Write clear, idiomatic prose, and use the status values documented in the README consistently. The review process is defined in `rea_game/SKILL.md`.

Keep credentials, private local paths, personal recordings, and unlicensed assets out of examples. Prefer reproducible, synthetic footage.

## Issues and pull requests

When reporting an issue, include your operating system, Python and FFmpeg versions, the full command, error output, and expected behavior. Remove private paths before sharing. If you cannot share the original footage, provide a minimal synthetic reproduction.

Pull requests should explain the problem, the resulting behavior, and how the change was verified. Credit third-party code and follow its license terms when reusing or adapting it.

## Pre-release checks

macOS / Linux, with the virtual environment activated:

```sh
python -m pip install build twine
python -m build
python -m twine check dist/rea_game-0.1.0-py3-none-any.whl dist/rea_game-0.1.0.tar.gz
python scripts/check_distribution.py dist/rea_game-0.1.0-py3-none-any.whl
python scripts/check_distribution.py dist/rea_game-0.1.0.tar.gz
```

Windows PowerShell:

```powershell
$env:PYTHONUTF8 = "1"
.\.venv\Scripts\python.exe -m pip install build twine
.\.venv\Scripts\python.exe -m build
.\.venv\Scripts\python.exe -m twine check dist/rea_game-0.1.0-py3-none-any.whl dist/rea_game-0.1.0.tar.gz
.\.venv\Scripts\python.exe scripts/check_distribution.py dist/rea_game-0.1.0-py3-none-any.whl
.\.venv\Scripts\python.exe scripts/check_distribution.py dist/rea_game-0.1.0.tar.gz
```

The verification script creates a temporary virtual environment, installs the built package, and runs the CLI outside the source checkout. It checks the bundled workflow and completes the synthetic example. Installing the source distribution requires a network connection to fetch build dependencies.

CI is configured to run the same checks on Linux, macOS, and Windows with Python 3.10 and 3.14. It does not upload or publish packages. Check Actions runs for actual results.

The version is 0.1.0, and the initial release is still in preparation. Project URLs are omitted until a repository address is chosen. Add the real repository and issue tracker URLs before publishing. Automatic publishing is not configured.
