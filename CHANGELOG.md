# Changelog

Notable changes in each release are recorded here.

## 0.1.0 - 2026-11-08

- Use English throughout the CLI, report templates, review workflow, documentation, and examples.
- Standardize review statuses as `observation`, `inference`, `unverified`, and `proposal`.
- Keep metadata and extracted frames on the same video track in files with multiple tracks, using the first track that is not a cover image.
- Reject intervals that cause the frame count to overflow before creating an output directory, with a clear CLI error.
- Add regression tests for multiple video tracks and tiny intervals.
- Document installation, usage, and package verification on macOS and Windows.
- Configure CI for Python 3.10 and 3.14 on Linux, macOS, and Windows, with UTF-8 used consistently in verification files.
- Add a quick start, workflow diagram, usage boundaries, and a reproducible synthetic example.
- Document how to distinguish evidence from inference and turn a review into a prototype plan.
