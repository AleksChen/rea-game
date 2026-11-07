"""Verify an installed distribution outside the source checkout; never publish."""
import json
import os
import subprocess
import sys
import tempfile
import venv
from pathlib import Path


def main():
    artifact = Path(sys.argv[1]).resolve()
    repo = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        env = os.environ.copy()
        env.pop("PYTHONPATH", None)
        env["PYTHONUTF8"] = "1"
        venv.EnvBuilder(with_pip=True).create(root / "venv")
        bin_dir = root / "venv" / ("Scripts" if os.name == "nt" else "bin")
        python = bin_dir / ("python.exe" if os.name == "nt" else "python")
        cli = bin_dir / ("rea-game.exe" if os.name == "nt" else "rea-game")

        def run(*args):
            return subprocess.run(list(map(str, args)), cwd=root, env=env,
                                  capture_output=True, encoding="utf-8", check=True).stdout

        run(python, "-m", "pip", "install", artifact)
        assert "extract" in run(cli, "--help")
        assert run(cli, "skill") == (repo / "rea_game/SKILL.md").read_text(encoding="utf-8")
        run(python, repo / "examples/synthetic/create_video.py", root / "sample.mp4")
        run(cli, "extract", root / "sample.mp4", "-o", root / "analysis", "--interval", 1)
        review = (repo / "examples/synthetic/review.json").read_text(encoding="utf-8")
        (root / "analysis/review.json").write_text(review, encoding="utf-8")
        run(cli, "report", root / "analysis")
        actual = (root / "analysis/report.md").read_text(encoding="utf-8")
        expected = (repo / "examples/synthetic/report.md").read_text(encoding="utf-8")
        assert actual.splitlines()[3:] == expected.splitlines()[3:]
        evidence = json.loads((root / "analysis/evidence.json").read_text(encoding="utf-8"))
        assert len(evidence["frames"]) == 3
    print(f"Installation and end-to-end workflow verified: {artifact.name}")


if __name__ == "__main__":
    main()
