# 06 — Refinement

## What practical question does this guide answer?

This guide answers the final workshop question: what should become part of the repository’s durable workflow after you complete one bounded agent cycle?

You should ask the agent to draft that answer into `@04-hardening-note.md`, then review what really deserves to become repo structure, stronger instructions, or automation.

## Why this matters

If every lesson stays trapped in one session, you pay the same coordination cost again next time. The goal here is to turn repeated friction into better instructions, tests, prompt patterns, or templates.

This closing step is what keeps the workshop from being only a one-off exercise. It asks you to convert experience into durable process: what should become part of `AGENTS.md`, what should become a test, what prompt or template pattern was genuinely reusable, and what was only useful for this one task.

## Steps

### Step 1 — Record the branch outcome

Before turning the session into durable process, you should be able to say what happened to the task branch: committed and merged, held for revision, or discarded after rejection.

That matters because refinement should reflect the real outcome. A merged task and a rejected task teach different lessons.

### Step 2 — Ask the agent to draft the hardening note

```text
Using the approved `agents/docs/<task-slug>-03-review-and-decision.md` and the session notes, fill the format specified in `@04-hardening-note.md`.
Place the result in `agents/docs/<task-slug>-04-hardening-note.md` for review.
Focus on durable instructions, checks to automate, reusable prompt or template patterns, and one concrete improvement action.
Do not change repo files yet.
```

### Step 3 — Distinguish durable lessons from one-off notes

When you review the hardening note, ask:

- is this a repeated problem or just a one-off issue?
- should this become part of `AGENTS.md`?
- should this become a test?
- should this become a stronger template or prompt pattern?
- is this really worth preserving, or is it just session cleanup?

## Outputs

- The task branch outcome is explicit: merged, held for revision, or stopped.
- `agents/docs/<task-slug>-04-hardening-note.md` exists as a draft of durable improvements pulled from the session.
- That draft has been reviewed to separate true reusable changes from one-off notes.

## Discussion

1. Which lesson from the task deserves to become a durable repo rule?
2. What repeated review activity would save the most time if it became a test?
3. Which lesson belongs in `AGENTS.md` versus in a test versus in a reusable template?
4. When does a repeated task shape justify a stronger template versus better context-management habits?
5. When is a reusable skill or agent workflow pattern justified instead of a one-off note in the docs?
6. How do you tell whether a workflow improvement is durable or just a patch for one awkward session?

## Next

Core path complete. Use [Appendices](./appendices/README.md) only after the active workflow is stable.
