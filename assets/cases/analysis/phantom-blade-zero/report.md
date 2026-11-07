# Gameplay Analysis

Source: ../../Phantom Blade Zero.mp4
Recording duration: 69.7 seconds

Timestamps refer to positions in the recording. Inferences and unverified claims are not confirmed game rules.

## Overview

- **Observation**: The clip shows a title screen, third-person traversal through a lantern-lit town, melee combat against human enemies, an equipment inventory with weapon detail panels, and a later forest encounter. (Evidence: 0s, 9s, 15s, 21s, 36s, 39s, 51s, 66s)

## Core Gameplay Loop

- **Observation**: The visible play loop combines moving through a location, engaging enemies with close-range attacks, and opening equipment screens to inspect weapons. (Evidence: 9s, 15s, 21s, 30s, 39s, 45s, 51s, 54s, 66s)
- **Inference**: The footage suggests an action RPG loop that alternates exploration, combat, and gear management, but it does not show a full mission or a confirmed reward cycle. (Evidence: 9s, 21s, 45s, 51s, 66s)

## Controls and Interaction

- **Observation**: The character changes facing and performs attack animations while enemies are nearby; no controller or keyboard input is shown. (Evidence: 15s, 21s, 39s, 66s)
- **Observation**: The HUD includes a cluster of action icons at the lower right, but exact bindings and the purpose of each icon are not established. (Evidence: 9s, 36s, 39s)
- **Unverified**: The combat may involve timed defense, dodging, or weapon-specific actions, but the footage does not isolate inputs enough to verify these mechanics. (Evidence: 21s, 66s)

## Rules and Game States

- **Observation**: Enemy health bars and red hit effects are visible during the town and forest fights; the player HUD shows multiple horizontal status bars. (Evidence: 12s, 18s, 27s, 51s, 57s, 63s)
- **Observation**: The forest fight ends on a red-tinted death screen with a large death mark, establishing a player defeat in this recorded encounter. (Evidence: 66s)
- **Observation**: The clip does not show a restart, checkpoint return, or mission-completion reward. (Evidence: 66s)

## Levels and Progression

- **Observation**: The footage begins on the title screen, then moves to a lantern-lit town and later to a forest area introduced by a location title. (Evidence: 0s, 6s, 36s)
- **Observation**: Weapon detail panels are opened for a heavy firearm-like weapon and a spear-like weapon; the footage does not confirm an equip action. (Evidence: 42s, 45s)
- **Observation**: The forest encounter continues through repeated combat exchanges and ends with a death screen. (Evidence: 48s, 54s, 60s, 66s)

## UI and Feedback

- **Observation**: Combat HUD elements remain in the lower corners, with status bars at the lower left and action or item icons at the lower right. Weapon information panels display an item illustration and descriptive text. (Evidence: 9s, 21s, 45s, 51s)
- **Observation**: Several interface labels are too small to read reliably in the extracted frames, so exact stats and item effects are not transcribed. (Evidence: 45s, 51s)

## Art and Camera

- **Observation**: The presentation uses a muted, cinematic palette, close third-person framing, wet-looking stone streets, warm lantern light, and a darker forest environment. (Evidence: 9s, 15s, 36s, 39s)
- **Observation**: Melee impacts use prominent red visual effects and enemy reactions; the camera tracks behind the player and tightens around nearby combat. (Evidence: 15s, 21s, 39s, 66s)

## Music and Sound Effects

- **Unverified**: Audio is present in the source file, but no sound-specific claim is included because the analysis focused on the visible evidence frames.

## Prototype Plan

- **Proposal**: Start with a third-person character controller, a compact street arena, one enemy with a readable health bar, and a basic light/heavy attack loop.
- **Proposal**: Add enemy hit reactions and clear player feedback for damage before implementing multiple weapon types.
- **Proposal**: Represent equipment in a simple inventory panel with a small set of weapon attributes; add weapon switching only after the combat loop is playable.
- **Proposal**: Build one forest encounter as a second scene after the first combat space is stable. A 3D engine such as Godot or Unity is a reasonable implementation choice, not a statement about the original game.

## Open Questions

- **Unverified**: What are the exact attack, dodge, block, and special-action inputs?
- **Unverified**: Do the inventory values change attack behavior, and how are weapons equipped?
- **Unverified**: Are the forest and street parts of one continuous level?
- **Unverified**: What checkpoint or recovery options follow the death screen?
- **Unverified**: What sounds accompany attacks, movement, and the environments?

## Detailed Timeline

| Time | Visible sequence | Evidence-led reading |
| --- | --- | --- |
| 0–3s | Title screen with game name and character portrait. | Opening/menu state. |
| 6–9s | The character enters a lantern-lit stone town; HUD appears. | Third-person exploration begins. |
| 12–18s | Several human enemies approach; the player attacks and red hit effects appear. | Close-range combat and enemy reactions are visible. |
| 21–33s | Combat continues among multiple opponents with status bars and attack feedback. | Sustained encounter; exact combos and defense rules are unclear. |
| 36–39s | Scene changes to a forest and displays a location title. | A new area or edited transition. |
| 42–45s | Equipment screens show a heavy firearm-like weapon and a spear-like weapon with item text. | Inventory/equipment UI is visible; selection taking effect is not confirmed. |
| 48–60s | The player fights again in the forest; health feedback and red impact effects appear. | A second combat encounter with incoming damage. |
| 63–66s | The fight continues, then a red-tinted death screen appears. | The recorded encounter ends in defeat; recovery is not shown. |

## Gameplay Hypotheses

| Hypothesis | Status | Evidence | Open point |
| --- | --- | --- | --- |
| Exploration, melee combat, and equipment inspection form the visible loop. | Inference | Town traversal, two combat sequences, and weapon panels (6–66s). | Whether equipment changes stats or the sequence is a montage. |
| The player can use multiple weapon classes. | Inference | Firearm-like and spear-like items appear in equipment screens (42–45s). | Equip input, switching, and attack differences. |
| Combat failure leads to the displayed death state. | Inference | Low health feedback precedes the death screen (57–66s). | Defeat threshold, checkpoint, and restart options. |

## Continue to a Playable Recreation

Once you have the analysis, continue toward a playable recreation. If you can code, use Claude Code or Codex to build it, or choose a game development workflow with [Unity](https://unity.com/), [Unreal Engine](https://www.unrealengine.com/), or [Godot](https://godotengine.org/). If you don't code, use [Seele AI](https://www.seeles.ai) for the next development step.
