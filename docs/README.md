# Session 3 Guide: Prompt-First Agent Workflow

This guide is the operator map for Session 3. It assumes one working repository, one bounded workflow change, and one reviewable path from idea to decision. The repository is built around the Bike Sharing workflow, `fetch -> prepare -> analyze -> report`, and the running example across the core path is to add a temperature-band demand summary in `analyze` and surface it in `report`.

The starting repository intentionally does not include that feature. Students are meant to define, implement, verify, and review the temperature-band change over the course of the session rather than inspect a pre-solved baseline.

The teaching emphasis in this version is prompt-first rather than template-first. Students should spend less time hand-authoring structured artifacts themselves and more time learning how to ask the coding agent to draft those artifacts in a reviewable way. The human still owns task choice, approval, interpretation, and merge decisions. What changes is where the clerical and formatting work happens.

That distinction matters. The workshop is not trying to teach “prompt until code appears.” It is trying to teach how to direct an agent inside a real repository without giving up control of scope, scientific meaning, or review quality. The structured drafts in `agents/docs/` are there to make that supervision legible.

Git discipline is part of that supervision loop, not a separate stage. Students should usually begin by checking git state and creating a task branch, keep work reviewable with small commits during implementation, clean up mistakes while the work is still isolated on that branch, and only merge after the review record is approved.

## Session Pattern

The default loop for the session is:

1. Human chooses a bounded task and a task slug.
2. Human asks the agent to convert that task into a structured draft using a named template.
3. Agent writes the draft into `agents/docs/`.
4. Human reviews, edits, approves, or requests revision.
5. Agent uses the approved draft as the contract for the next step.

The important point is that templates remain canonical blanks in `agents/templates/`. The working session artifacts live in `agents/docs/`. That keeps the source templates reusable and gives the human a clean place to review what the agent actually produced.

## Core Flow

1. [00 — Session Overview](./00-session-overview.md)
   Set up git state and the baseline, inspect the current workflow, and learn the draft-review pattern.
2. [01 — Risk, Task Types, and Review Burden](./01-agent-tasks.md)
   Ask the agent to draft the first task spec and review whether the task is appropriate for delegation.
3. [02 — Testing and Verification Strategy](./02-testing-as-verification.md)
   Revise the same task spec so the verification plan is explicit before implementation.
4. [03 — Specification and Approval](./03-specification-templates.md)
   Tighten the approved task spec so the pinned decisions are clear.
5. [04 — Context Management](./04-context-management.md)
   Ask the agent to draft the bounded implementation brief.
6. [05 — Delegation](./05-delegation.md)
   Turn the approved brief into the implementation handoff, plan-review loop, and bounded commit rhythm.
7. [06 — Verification and Decision](./06-verification.md)
   Ask the agent to draft the review-and-decision record from real evidence and use it to gate fix / commit / merge choices.
8. [08 — Refinement and Hardening](./08-refinement.md)
   Ask the agent to draft the hardening note for durable repo improvements.

Read the guides in order. The early documents are about choosing and shaping the task; the middle documents are about briefing and supervising the agent; the later documents are about review, integrated git discipline, and turning one session into better future practice.

## Active Templates

The only active template interfaces for the session are:

- `@01-task-spec.md`
- `@02-agent-brief.md`
- `@03-review-and-decision.md`
- `@04-hardening-note.md`

Those templates are intentionally few. They are meant to cover the actual decision points in the workshop, not to create paperwork for its own sake. If a structured artifact is not helping the human supervise the agent, it should not be part of the active path.

Canonical blanks live in [agents/templates/README.md](../agents/templates/README.md). Session-specific drafts live in [agents/docs/README.md](../agents/docs/README.md).

## How To Read These Docs

Each core guide is written to do five jobs:

- explain what question the human is trying to answer at that stage
- explain why that question matters in a real codebase
- give a copy-paste prompt the human can send to the agent
- name the concrete outputs that should exist and be reviewed by the end of the step
- offer discussion prompts that help the instructor turn the exercise into a conversation

That combination is deliberate. A workshop reader should never be left with only abstract advice, but also should not be left with only prompt snippets and no understanding of why those snippets are shaped the way they are.

## Archive

Historical workshop material lives in [docs/archive/INDEX.md](./archive/INDEX.md). Use the active files in `docs/` for the current session.
