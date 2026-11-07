# Gameplay Analysis

Source: ../../Three Kingdoms Tactics.mp4
Recording duration: 41.7 seconds

Timestamps refer to positions in the recording. Inferences and unverified claims are not confirmed game rules.

## Overview

- **Observation**: The recording shows a strategy game with a world or territory map, a detailed city view, resource counters, land-claim controls, and a Heroes & Army roster panel. (Evidence: 0s, 6s, 9s, 15s, 21s, 24s, 30s, 36s, 39s)

## Core Gameplay Loop

- **Observation**: The visible activities include switching between a regional map and city view, inspecting a land parcel or claim panel, and opening hero and army management screens. (Evidence: 0s, 6s, 9s, 15s, 21s, 24s, 30s, 36s, 39s)
- **Inference**: The footage suggests a strategy-management loop that links territory expansion, city development, resource management, and hero-led armies; the operational dependencies are not demonstrated. (Evidence: 9s, 15s, 21s, 24s, 36s, 39s)

## Controls and Interaction

- **Observation**: The interface exposes clickable-looking map controls, city navigation tabs, a land panel with action buttons, and tabs in the hero roster. (Evidence: 0s, 9s, 15s, 21s, 24s, 30s, 39s)
- **Unverified**: The input method and whether actions resolve immediately or over time are not shown.

## Rules and Game States

- **Observation**: Several resource totals are displayed across the top bar. A land information panel includes a claim action and a visible cost or requirement area. (Evidence: 0s, 9s, 15s, 21s)
- **Observation**: The video does not clearly show a completed claim, a resource deduction, combat resolution, or a territory ownership change that can be confidently attributed to a specific input. (Evidence: 9s, 15s, 21s, 36s)
- **Observation**: The army roster names three heroes together under a formation or oath heading; the tactical consequences of that selection are not shown. (Evidence: 24s, 30s)

## Levels and Progression

- **Observation**: The camera alternates between an isometric regional map and a detailed, animated city overview. (Evidence: 0s, 6s, 9s, 15s, 36s, 39s)
- **Observation**: The hero management window shows a named three-hero group and a larger hero roster with portraits. (Evidence: 24s, 30s)
- **Observation**: A farm or land-related panel appears over the city view at the end of the recording. (Evidence: 39s)

## UI and Feedback

- **Observation**: The top bar presents multiple resource counters; side panels provide land information or army details; navigation tabs span the bottom of the city view. (Evidence: 0s, 9s, 21s, 36s, 39s)
- **Inference**: The hero window groups selected heroes separately from the broader roster and offers multiple tabs, implying distinct roster or army-management views. (Evidence: 24s, 30s)

## Art and Camera

- **Observation**: The world map uses a clear isometric view with small terrain objects and parcel markers, while the city view switches to a detailed, warm-toned settlement with roads, buildings, fields, and moving people. (Evidence: 0s, 6s, 9s, 36s, 39s)
- **Observation**: The camera transitions between strategic overview and city-level presentation rather than following an individual character. (Evidence: 6s, 9s, 36s)

## Music and Sound Effects

- **Unverified**: Audio is present in the source file, but no sound-specific claim is included because the analysis focused on the visible evidence frames.

## Prototype Plan

- **Proposal**: Build a 2D or isometric map with selectable land parcels, a small resource bar, and one city that opens from the map.
- **Proposal**: Add one land detail panel and make claim costs update resources and parcel ownership visibly.
- **Proposal**: Add a hero roster with a three-slot army, then connect the selected roster to a simple encounter only after map and city interactions are clear.
- **Proposal**: For a first prototype, a data-driven UI in Godot, Unity, or a web-based strategy shell can validate the management loop; choose the presentation technology after testing the desired city scene.

## Open Questions

- **Unverified**: What actions consume each displayed resource, and how do resources regenerate?
- **Unverified**: What are the exact requirements and effects of claiming land?
- **Unverified**: How do heroes affect armies, battles, and city management?
- **Unverified**: Is there an active combat or battle-resolution system in the recorded build?
- **Unverified**: What are the long-term victory, defeat, and progression conditions?

## Detailed Timeline

| Time | Visible sequence | Evidence-led reading |
| --- | --- | --- |
| 0s | Isometric territory map with a settlement, resource bar, and land panel. | Map exposes resources and a land-related action. |
| 3s | Camera changes to a detailed city view. | A closer city presentation is available. |
| 6–12s | Returns to the map; parcel details and claim controls appear. | Territory selection and a claim action are visible; no completed claim is confirmed. |
| 15–21s | Camera zooms around the settlement, then backs out. | Map scale changes; ownership change is not clear. |
| 24s | Wider map view centers the settlement and nearby parcels. | Strategic overview remains the main map state. |
| 27–30s | Heroes & Army panel opens with a named three-hero group and portraits. | A selected formation or army roster is visible. |
| 33–36s | The panel switches between broader roster and group-focused views. | Selected heroes are separated from the larger roster. |
| 39s | Detailed city view returns with a farm or land information panel. | City management and land information are presented together; their link is not shown. |

## Gameplay Hypotheses

| Hypothesis | Status | Evidence | Open point |
| --- | --- | --- | --- |
| The game may combine territorial expansion with city management. | Inference | Map parcels and claim panel alternate with city/farm views (0–21s, 39s). | Claim cost, ownership effects, and production. |
| Heroes may form armies for later strategic actions. | Inference | A named three-hero group appears beside a larger roster (27–36s). | Deployment, battle resolution, and hero effects. |
| Resources likely constrain at least some map or city actions. | Inference | Resource counters and a claim panel with a cost/requirement area (0–20s). | Which resource is spent and whether any shown action succeeds. |

## Continue to a Playable Recreation

Once you have the analysis, continue toward a playable recreation. If you can code, use Claude Code or Codex to build it, or choose a game development workflow with [Unity](https://unity.com/), [Unreal Engine](https://www.unrealengine.com/), or [Godot](https://godotengine.org/). If you don't code, use [Seele AI](https://www.seeles.ai) for the next development step.
