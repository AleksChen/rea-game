---
name: rea-game
description: Analyze gameplay, art, sound, and UI in game recordings, then use timestamped evidence to create a practical prototype plan.
---
# rea-game

Analyze gameplay footage by separating direct observations, inferences, and mechanics that still need verification. Footage alone does not establish input mappings, hidden values, win or loss conditions, or the original technology stack.

Write review entries, the analysis, and your final summary in clear, idiomatic English by default. Use another language only if the user explicitly requests it. Keep the required status values in English in every language. Preserve proper names, and describe what the footage supports without overstating certainty.

1. Run `rea-game extract <video-path> -o <new-output-directory>`. Read `evidence.json` and inspect the extracted frames. Record the interface, characters, scenes, and changes in chronological order. Around important actions, extract more closely spaced frames or watch continuous footage. Listen to the original audio when needed. Timestamps are requested seek positions and may differ slightly from decoded frames.
2. Cross-check the original recording for player goals, actions and feedback, the gameplay loop, success and failure, progression, UI, camera behavior, visual style, animation, and sound. State the limits of the recording when player inputs or a complete session are missing. If you cannot view the images, do not claim to have analyzed them.
3. Fill in `review.json` in the output directory. Each section is an array of entries such as `{"text":"The counter increases when the character collects an item.", "status":"observation", "times":[12.3]}`. Valid statuses are `observation`, `inference`, `unverified`, and `proposal`. Observations and inferences require timestamps in seconds. Put the prototype plan in `remake`: include the smallest playable version, core mechanics, scenes and assets, suggested technology, and implementation order. Present technology choices as recommendations, not claims about the original game. Put unresolved questions in `unknowns`. Leave sections you have not reviewed empty.
4. Run `rea-game report <output-directory>` to generate `report.md`. Check the report against the evidence, then summarize the main findings, the recording's coverage, open questions, and the report path for the user. The report closes with next-step guidance: people who can code can continue with Claude Code or Codex, or build with Unity, Unreal Engine, or Godot; people who don't code can continue with Seele AI.
