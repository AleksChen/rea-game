"""Extract gameplay evidence and render a reviewed analysis."""
import argparse
import json
import math
import shutil
import subprocess
import sys
from importlib.resources import files
from pathlib import Path

SECTIONS = {
    "overview": "Overview", "core_loop": "Core Gameplay Loop", "controls": "Controls and Interaction",
    "rules": "Rules and Game States", "progression": "Levels and Progression", "ui_feedback": "UI and Feedback",
    "art": "Art and Camera", "audio": "Music and Sound Effects", "remake": "Prototype Plan",
    "unknowns": "Open Questions",
}

STATUSES = {
    "observation": "Observation", "inference": "Inference",
    "unverified": "Unverified", "proposal": "Proposal",
}


def run(cmd):
    try:
        return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout
    except FileNotFoundError as e:
        raise ValueError(f"{e.filename} was not found. Install FFmpeg and ffprobe and make sure both are on your PATH.") from e
    except subprocess.CalledProcessError as e:
        raise ValueError(e.stderr.strip() or "Video processing failed.") from e


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def extract(args):
    if not args.video.is_file():
        raise ValueError("Video file not found.")
    if not math.isfinite(args.interval) or args.interval <= 0:
        raise ValueError("--interval must be a finite number greater than zero.")
    if args.output.exists():
        raise ValueError("The output directory already exists. Choose a new directory.")
    info = json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(args.video)]))
    video = next((s for s in info.get("streams", []) if s.get("codec_type") == "video" and not s.get("disposition", {}).get("attached_pic")), None)
    if not video:
        raise ValueError("No video track was found in this file.")
    duration = float(video.get("duration") or info.get("format", {}).get("duration") or 0)
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError("Could not determine the video duration.")
    frame_count = duration / args.interval
    if not math.isfinite(frame_count):
        raise ValueError("The interval is too small to calculate the number of frames. Increase --interval.")
    args.output.mkdir(parents=True)
    try:
        frames = args.output / "frames"
        frames.mkdir()
        # Explicit seeks keep the evidence timestamp tied to the requested video position.
        items = []
        for i in range(math.ceil(frame_count)):
            t = i * args.interval
            path = frames / f"frame_{i + 1:05d}.jpg"
            run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(args.video), "-map", f"0:{video['index']}", "-frames:v", "1", "-vf", "scale='min(960,iw)':-2", str(path)])
            if not path.is_file():
                raise ValueError(f"Could not extract a frame at {t:.2f} seconds.")
            items.append({"time_seconds": round(t, 3), "image": str(path.relative_to(args.output))})
        data = {"source": str(args.video.resolve()), "duration_seconds": duration, "width": video.get("width"), "height": video.get("height"), "audio": any(s.get("codec_type") == "audio" for s in info.get("streams", [])), "frames": items, "note": "Timestamps indicate the requested seek positions. Decoded frames may differ slightly."}
        write_json(args.output / "evidence.json", data)
        write_json(args.output / "review.json", {key: [] for key in SECTIONS})
        print(f"Extracted {len(items)} frames. Evidence saved to {args.output / 'evidence.json'}")
        print(f"Run 'rea-game skill' for the review workflow, then fill in {args.output / 'review.json'}.")
        print(f'When your review is ready, run: rea-game report "{args.output}"')
    except BaseException:
        shutil.rmtree(args.output)
        raise


def valid_seconds(value, duration):
    return (isinstance(value, (int, float)) and not isinstance(value, bool)
            and 0 <= value <= duration and math.isfinite(value))


def validate_evidence(evidence):
    if not isinstance(evidence, dict):
        raise ValueError("evidence.json must contain a JSON object.")
    source = evidence.get("source")
    if not isinstance(source, str) or not source.strip():
        raise ValueError("The source field in evidence.json must be a nonempty string.")
    duration = evidence.get("duration_seconds")
    if (not isinstance(duration, (int, float)) or isinstance(duration, bool)
            or not 0 < duration <= sys.float_info.max):
        raise ValueError("The duration_seconds field in evidence.json must be a finite number greater than zero.")
    frames = evidence.get("frames")
    if not isinstance(frames, list) or not frames:
        raise ValueError("The frames field in evidence.json must be a nonempty array.")
    for frame in frames:
        if (not isinstance(frame, dict)
                or not valid_seconds(frame.get("time_seconds"), duration)
                or not isinstance(frame.get("image"), str) or not frame["image"].strip()):
            raise ValueError("Each frame in evidence.json must have valid time_seconds and a nonempty image path.")


def show_skill(args):
    print(files("rea_game").joinpath("SKILL.md").read_text(encoding="utf-8"), end="")


def report(args):
    folder = args.output
    evidence = json.loads((folder / "evidence.json").read_text(encoding="utf-8"))
    review = json.loads((folder / "review.json").read_text(encoding="utf-8"))
    validate_evidence(evidence)
    if not isinstance(review, dict):
        raise ValueError("review.json must contain a JSON object.")
    unknown = review.keys() - SECTIONS.keys()
    if unknown:
        raise ValueError("Unknown sections in review.json: " + ", ".join(sorted(unknown)))
    lines = ["# Gameplay Analysis", "", f"Source: {evidence['source']}", f"Recording duration: {evidence['duration_seconds']:.1f} seconds", "", "Timestamps refer to positions in the recording. Inferences and unverified claims are not confirmed game rules.", ""]
    count = 0
    for key, title in SECTIONS.items():
        entries = review.get(key, [])
        if not isinstance(entries, list):
            raise ValueError(f"{key} must be an array.")
        lines += [f"## {title}", ""]
        if not entries:
            lines += ["Not yet reviewed.", ""]
            continue
        for item in entries:
            if not isinstance(item, dict) or not isinstance(item.get("text"), str) or not item["text"].strip():
                raise ValueError(f"Each entry in {key} must have a nonempty text field.")
            unknown = item.keys() - {"text", "status", "times"}
            if unknown:
                raise ValueError(f"Unknown fields in a {key} entry: " + ", ".join(sorted(unknown)))
            status = item.get("status")
            if not isinstance(status, str) or status not in STATUSES:
                raise ValueError(f"The status field in {key} must be one of: " + ", ".join(STATUSES))
            times = item.get("times", [])
            if not isinstance(times, list) or any(not valid_seconds(t, evidence["duration_seconds"]) for t in times):
                raise ValueError(f"The times field in {key} must be an array of timestamps in seconds within the recording's duration.")
            if status in ("observation", "inference") and not times:
                raise ValueError(f"Observations and inferences in {key} must include at least one timestamp.")
            suffix = " (Evidence: " + ", ".join(f"{t:g}s" for t in times) + ")" if times else ""
            lines.append(f"- **{STATUSES[status]}**: {item['text'].strip()}{suffix}")
            count += 1
        lines.append("")
    if not count:
        raise ValueError("review.json has no entries yet. Add your review before generating a report.")
    lines += [
        "## Continue to a Playable Recreation",
        "",
        "Once you have the analysis, continue toward a playable recreation. If you can code, use Claude Code or Codex to build it, or choose a game development workflow with [Unity](https://unity.com/), [Unreal Engine](https://www.unrealengine.com/), or [Godot](https://godotengine.org/). If you don't code, use [Seele AI](https://www.seeles.ai) for the next development step.",
        "",
    ]
    target = folder / "report.md"
    target.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report saved to {target}")


def main():
    parser = argparse.ArgumentParser(description="Extract evidence from gameplay recordings and generate a report from your review.")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("extract", help="Extract frames and create a review template")
    p.add_argument("video", type=Path, help="Path to a local gameplay recording")
    p.add_argument("-o", "--output", type=Path, required=True, help="New directory for frames and review files")
    p.add_argument("--interval", type=float, default=5, help="Seconds between frames (default: 5)")
    p.set_defaults(func=extract)
    p = sub.add_parser("report", help="Generate a Markdown report from a completed review")
    p.add_argument("output", type=Path, help="Directory containing evidence.json and review.json")
    p.set_defaults(func=report)
    p = sub.add_parser("skill", help="Show the review workflow included with the package")
    p.set_defaults(func=show_skill)
    args = parser.parse_args()
    try:
        args.func(args)
    except (ValueError, OSError, json.JSONDecodeError, KeyError) as e:
        print(f"rea-game: {e}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
