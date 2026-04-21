# 07 — Refinement and Hardening

## What practical question does this guide answer?

This guide answers the final workshop question: what should become part of the repository’s durable workflow after one bounded agent cycle is complete?

Students should ask the agent to draft that answer into `@04-hardening-note.md`, then review what really deserves to become repo structure.

## Why this matters

If every lesson stays trapped in one session, the team pays the same coordination cost again next time. The goal here is to turn repeated friction into better instructions, tests, prompts, or templates.

This closing step is what keeps the workshop from being only a one-off exercise. It asks students to convert experience into durable process: what should become part of `AGENTS.md`, what should become a test, what prompt pattern was genuinely reusable, and what was only useful for this one task.

## Steps

### Step 1 — Close the task branch deliberately

Before turning the session into durable process, students should be able to say what happened to the task branch: merged, parked for more revision, or discarded after rejection.

That matters because hardening should reflect the real outcome. A merged task and a rejected task teach different lessons.

### Step 2 — Ask the agent to draft the hardening note

```text
Using the approved `agents/docs/<task-slug>-03-review-and-decision.md` and the session notes, fill the format specified in `@04-hardening-note.md`.
Place the result in `agents/docs/<task-slug>-04-hardening-note.md` for review.
Focus on durable instructions, checks to automate, reusable prompt patterns, and one concrete improvement action.
Do not change repo files yet.
```

If the first draft is too broad, use:

```text
Revise `agents/docs/<task-slug>-04-hardening-note.md` using the review comments below.
Prefer one concrete improvement over a long wish list.
Keep the same template structure.
Do not change repo files yet.
```

### Step 3 — Distinguish durable lessons from one-off notes

Not every annoyance deserves to become repo process. When students review the hardening note, they should ask:

- is this a repeated problem or just a one-off issue?
- would a stronger instruction help next time?
- should this become a test?
- is this really a prompt pattern worth preserving?
- should branch setup, commit checkpoints, or merge gating be made more explicit in the docs or `AGENTS.md`?

That filtering step is important. The workshop should not encourage process bloat.

## Outputs

- The task branch outcome is explicit: merged, held for revision, or stopped.
- `agents/docs/<task-slug>-04-hardening-note.md` exists as a draft of durable improvements pulled from the session.
- That draft has been reviewed to separate true reusable changes from one-off session cleanup.

## Discussion

1. Which reminder from the temperature-band task deserves to become a durable repo rule?
2. What repeated review activity would save the most time if it became a test?
3. When does a repeated task shape justify a skill instead of only a better template?
4. Which lesson from this session belongs in `AGENTS.md` versus in a test versus in a reusable prompt?
5. How do you tell whether a workflow improvement is durable or just a patch for one awkward run?

## Next

Core path complete. Use [Appendices](./appendices/README.md) only after the prompt-first bounded workflow is stable.
