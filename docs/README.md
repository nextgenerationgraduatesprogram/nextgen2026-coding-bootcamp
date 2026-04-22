# Session 3 Guide: Specification-First Agent Workflow

This guide is the operator map for Session 3. It assumes one working repository, one bounded workflow change, and one reviewable path from problem definition to durable process improvement. The repository is built around the Bike Sharing workflow, `fetch -> prepare -> analyze -> report`, and the running example across the core path is to add a temperature-band demand summary in `analyze` and surface it in `report`.

The starting repository intentionally does not include that feature. You are meant to define, test, plan, implement, review, and refine the temperature-band change over the course of the session rather than inspect a pre-solved baseline.

The teaching emphasis in this version is specification-first. You still use prompts and templates, but the main contract is not the prompt itself. The main contract is the approved spec, the behavioural tests that make the expected behaviour executable, the approved implementation plan, and the final review record.

That distinction matters. The workshop is not trying to teach “prompt until code appears.” It is trying to teach you how to direct an agent inside a real repository without giving up control of scope, scientific meaning, stage boundaries, or review quality. The structured drafts in `agents/docs/` are there to make that supervision legible.

Git discipline is part of the same loop. You should usually begin by checking git state and creating a task branch, keep work reviewable with small commits during implementation, and only commit or merge after the review record is approved.

Chat discipline is part of the same loop too. When one phase is approved and you move to the next one, prefer starting a fresh agent chat and giving it only the approved artifact, the relevant repo surfaces, and the current stage instructions. That helps prevent context leakage from earlier drafts, abandoned ideas, or half-correct plans.

## Session Pattern

The default loop for the session is:

1. You define a bounded problem and task slug.
2. You ask the agent to draft or revise a structured artifact using a named template.
3. The agent writes the draft into `agents/docs/`, or updates executable behavioural tests in `tests/` once the spec is approved.
4. You review, edit, approve, or request revision.
5. The approved artifact becomes the contract for the next phase.
6. You usually start a new chat for the next phase so the agent sees the approved contract instead of the full history of discarded attempts.

The important point is that templates remain canonical blanks in `agents/templates/`. Working session artifacts live in `agents/docs/`. Repo tests and workflow outputs remain real repo surfaces, not paperwork substitutes.

## Core Flow

1. [00 — Session Overview](./00-session-overview.md)
   Set up git state and the baseline, inspect the current workflow, and learn the draft-review pattern.
2. [01 — Problem Definition and Specification](./01-specification.md)
   Define the problem, iterate on the task spec, and approve the contract for the change.
3. [02 — Behavioural Test Design and Implementation](./02-behavioural-validation.md)
   Turn the approved spec into executable behavioural tests before feature code starts.
4. [03 — Implementation Plan](./03-implementation-plan.md)
   Use the approved spec and behavioural tests to design the implementation plan and context bundle.
5. [04 — Implementation](./04-implementation.md)
   Implement the approved plan and add any needed unit or integration tests.
6. [05 — Review and Commit](./05-review-and-commit.md)
   Review the diff, tests, artifacts, and git state, then decide whether to accept, revise, or reject before commit or merge.
7. [06 — Refinement](./06-refinement.md)
   Turn repeated lessons into stronger instructions, tests, templates, or workflow habits.

Read the guides in order. The early documents are about defining the work and making expected behaviour explicit. The middle documents are about planning and implementing with bounded context. The later documents are about explicit review, commit discipline, and turning one session into better future practice.

## Active Templates

The only active template interfaces for the session are:

- `@01-task-spec.md`
- `@02-implementation-plan.md`
- `@03-review-and-decision.md`
- `@04-hardening-note.md`

Those templates are intentionally few. They are meant to cover the real decision points in the workshop, not to create paperwork for its own sake. If a structured artifact is not helping you supervise the agent, it should not be part of the active path.

Canonical blanks live in [agents/templates/README.md](../agents/templates/README.md). Session-specific drafts live in [agents/docs/README.md](../agents/docs/README.md).

## How To Read These Docs

Each core guide is written to do five jobs:

- explain the practical question for that phase
- explain why that question matters in a real repo
- show the repo surfaces or commands worth inspecting
- give a copy-paste prompt when a structured draft is required
- name the artifact or output that should exist and be reviewed by the end of the step

The core phases also share the same iteration rule:

`draft -> review -> revise -> approve`

That loop applies to the spec, the implementation plan, the review record, and the hardening note. Behavioural tests are the main exception because they become executable repo artifacts rather than docs-only drafts.

The preferred handoff rule is:

`approve stage output -> start a fresh chat -> provide the approved artifact and current-stage repo context`

That keeps each stage grounded in the right contract and reduces context leakage across the session.

## Archive

Historical workshop material lives in [docs/archive/INDEX.md](./archive/INDEX.md). Use the active files in `docs/` for the current session.
