# Task Idea Proposal form snapshot — 2026-07-21

Source: user-provided screenshots of the Snorkel AI Experts Portal submission form.
Purpose: durable local contract for the proposal-first lifecycle gate.

## Required fields observed

1. **Task Idea Summary** — short description, roughly 2–5 sentences, fully and clearly describing the idea.
2. **Idea Category** — exactly one radio selection.
3. **Associated Skills** — 5–10 skills required to accomplish the task.
4. **Task Tags** — 3–6 descriptive tags, analogous to `task.toml` tags.

The **Check feedback** action remains disabled until all four fields are complete.
The platform check is an early idea-validity signal. It is not uniqueness PASS,
Step 2a GO, empirical difficulty, or final acceptance.

## Category labels observed and local normalization

| Platform label | Local category slug | Current local eligibility |
| --- | --- | --- |
| System / Environment Setup & Configuration | `system-administration` | allowed |
| Build / Compilation / Dependency Management | `build-and-dependency-management` | allowed |
| Data / File Processing / ETL / Scripting | `data-processing` | blocked for net-new work |
| Machine Learning / Model Training / Inference | `machine-learning` | allowed |
| Security / Cryptography / Vulnerability Demonstration | `security` | allowed |
| Scientific Computing | `scientific-computing` | allowed |
| Interactive / Simulation Tasks / Games | `games` | allowed |

The platform form does not display the currently blocked `software-engineering`
or `debugging` categories in this snapshot. Local eligibility remains the source
for whether a proposal may proceed.

## Local operating decision

For every new candidate selected for actual task creation:

1. generate these four paste-ready fields before uniqueness research, Step 2a,
   task registration, or file creation;
2. stop and let the user run **Check feedback**;
3. capture the returned verdict/feedback and evidence;
4. if invalid, revise the four fields and re-check or reject the idea;
5. only a passed proposal may enter uniqueness and Step 2a.

Every failed proposal is still captured afterward as a permanent idea record so
its slug/fingerprint is not accidentally recycled.
