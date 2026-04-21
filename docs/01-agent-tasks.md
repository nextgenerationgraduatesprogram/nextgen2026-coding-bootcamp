# 01 — Risk, Task Types, and Review Burden

## What practical question does this guide answer?

This guide answers the first operator decision: is this a good task to hand to the agent, and how much review should the human expect to do?

In the new workflow, the human does not fill out a separate risk card by hand. The agent drafts that reasoning inside `@01-task-spec.md`, and the human reviews whether it is sensible, grounded in the repo, and appropriate for the session.

## Why this matters

A task can look small and still be a bad delegation target. A one-line change in `prepare` might quietly alter every downstream artifact. A slightly larger change in `report` may be much safer because it stays downstream, touches fewer assumptions, and is easier to inspect directly.

That is why the workshop starts with task type and review burden instead of with clever prompts. Prompt quality matters, but task choice matters first. If the task itself is poorly chosen, even a very careful prompt cannot fully rescue the review burden.

## Steps

### Step 1 — Compare realistic task types

Start with the real repo, not imagined examples.

```bash
rg -n "def run_(fetch|prepare|analyze|report)" src/nextgen2026_coding_bootcamp/steps
rg --files tests | sort
```

As you look through the repo, it helps to think in categories such as:

- scaffolding
- refactoring
- validation or testing
- workflow plumbing
- analysis logic
- reporting
- interpretation

The point is not to memorize a taxonomy. The point is to notice that not all “small” tasks are equally safe.

### Step 2 — Ask the agent to draft the task spec

```text
Read `AGENTS.md`, `docs/01-agent-tasks.md`, and the repo structure first.
Convert the task idea below into the format specified in `@01-task-spec.md`.
Place the result in `agents/docs/<task-slug>-01-task-spec.md` for review.
Use the current repo structure and tests to fill:
- why this task is appropriate for delegation
- risk and review burden
- likely files and surfaces
- constraints and non-goals
Do not implement code.

Task idea:
<describe the task here>
```

If you want the agent to revise the task-choice reasoning after review, use:

```text
Revise `agents/docs/<task-slug>-01-task-spec.md` using the review comments below.
Strengthen the sections on task fit, risk, and review burden.
Keep the template structure.
Do not implement code.
```

### Step 3 — Read the draft as a task-choice argument

Do not treat the first draft as automatically correct. Read it as an argument the agent is making:

- is this task bounded?
- is it in the right part of the repo?
- is the review burden realistic?
- is the task appropriate for a workshop session rather than for a long exploratory cycle?

For the running example, the temperature-band summary is a good workshop task because it crosses a real stage boundary, produces a visible artifact, remains reviewable with tests plus output inspection, and is still small enough to isolate on a single task branch.

## Outputs

- `agents/docs/<task-slug>-01-task-spec.md` exists and includes the task summary, delegation rationale, risk/review burden, and likely file surfaces.
- That draft has been reviewed for whether the task is truly workshop-sized and safe enough to delegate.

## Discussion

1. Why is a change in `prepare` often harder to delegate safely than an equally sized change in `report`?
2. Which risk axis is hardest to automate away in research-oriented workflow code, and why?
3. What makes the temperature-band extension a stronger workshop task than a workflow-order or CLI change?
4. What signals tell you a task is really a hidden refactor rather than a bounded feature?
5. How would you rewrite an unsafe task idea so it becomes suitable for one delegation loop?

## Next

Continue to [02 — Testing and Verification Strategy](./02-testing-as-verification.md).
