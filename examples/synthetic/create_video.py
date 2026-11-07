"""Create an original, deterministic test clip; no downloaded media."""
import argparse
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        "ffmpeg", "-v", "error", "-n", "-f", "lavfi", "-i",
        "color=c=black:s=320x180:r=10:d=3",
        "-vf", "drawbox=x=20:y=60:w=40:h=40:color=white:t=fill:enable='lt(t,1)',"
        "drawbox=x=140:y=60:w=40:h=40:color=white:t=fill:enable='gte(t,1)'",
        "-c:v", "mpeg4", str(args.output),
    ], check=True)


if __name__ == "__main__":
    main()
