# Task Idea Proposal — input-ring-physics-desync

Generated: 2026-07-22T21:16:44Z
Platform check: PASSED
Evidence: chat-2026-07-23 Snorkel Task Idea Proposal Check feedback pasted by Sudhir

## Paste-ready fields

### Task Idea Summary

A headless game simulation records inputs and claims deterministic replay. Fresh live sessions look fine, but replays of the same seed diverge in entity state digests after a few hundred ticks, while a short healthy-control replay stays bit-stable. Tick-count overlays remain green. Restore determinism so failing replays match the recorded outcome digests without breaking the short healthy controls or accepting approximate physics.

### Idea Category

Interactive / Simulation Tasks / Games

Normalized local category: `games`

### Associated Skills

fixed-timestep simulation, input buffering, deterministic replay, state hashing, engine systems programming in C++ or Rust, floating-point determinism hygiene, headless test harnesses

### Task Tags

deterministic-replay, game-simulation, input-buffer, fixed-timestep, state-digest

## Check feedback

Similarity PASS. Idea quality PASS (Decision: Accept; Verifiable: Accept; Well-specified: Uncertain; Solvable: Accept; Difficult: Accept; Interesting: Accept; Outcome-verified: Accept). Category alignment FAIL (selected sim_games; suggested debugging) — non-blocking. Metadata similarity PASS.

## Inspiration provenance

- Source type: game engine determinism incident pattern
- Source reference: fixed-timestep input-ring replay desync (inspiration only; distinct from lockstep-replay-fray; 2026-07-23)
- Reuse boundary: Inspired by tick-count-green / digest-wrong replay; no engine source or tests copied; structurally distinct from IDEA-0020 lockstep replay.
