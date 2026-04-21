# 03 — Specification and Approval

## What practical question does this guide answer?

This guide answers the approval question: when is the task spec good enough to become the contract for implementation?

Students should not be rewriting the task spec from scratch themselves. They should review the agent’s draft, decide what is pinned versus flexible, and then ask the agent to revise the draft until it is decision-ready.

## Why this matters

The most expensive mistakes in agent work often come from hidden decisions: wrong stage, widened scope, renamed artifacts, or a vague idea of what “done” means. The approved task spec is where the human locks those decisions down.

This is the point where the workshop most clearly shifts from “agent as generator” to “agent as drafting assistant.” The human is not just checking grammar. The human is deciding what the agent is not allowed to improvise.

## Steps

### Step 1 — Review the task spec like a contract

Look for:

- clear intended repo change
- likely files and surfaces that match the task
- constraints and non-goals that prevent drift
- a verification plan that matches the repository
- explicit `Accept / Revise / Reject` criteria

It can help to think in two buckets:

- pinned decisions the agent must not change casually
- flexible implementation choices the agent can handle locally

### Step 2 — Ask the agent to revise the task spec if needed

```text
Revise `agents/docs/<task-slug>-01-task-spec.md` using the review comments below.
Keep the format specified in `@01-task-spec.md`.
Tighten the pinned decisions, constraints, and decision thresholds.
Keep the task bounded.
Do not implement code.
```

Once the draft is close, use a final cleanup prompt like this:

```text
Prepare `agents/docs/<task-slug>-01-task-spec.md` for approval.
Keep the existing facts and scope.
Improve clarity and remove ambiguity.
Do not implement code.
```

### Step 3 — Approve the spec deliberately

The approval moment should feel explicit, not implied. Students should be able to say:

- this is the task
- this is what must not change
- this is how we will know whether it worked
- this is what would cause us to reject the result later

If they cannot say those things yet, the task spec is not ready.

## Outputs

- `agents/docs/<task-slug>-01-task-spec.md` has been revised into the approved task contract for implementation.
- The approved spec has been reviewed for pinned decisions, non-goals, verification thresholds, and explicit acceptance boundaries.

## Discussion

1. Which decisions in the task spec should remain rigid, and which can be left flexible?
2. How would you tell, from the draft alone, whether the agent might be tempted to solve the task in the wrong stage?
3. What kinds of ambiguity are harmless, and what kinds become dangerous once implementation starts?
4. Which sentence in a task spec is most likely to create downstream confusion if it stays vague?
5. How can acceptance criteria stay specific without dictating the exact implementation?

## Next

Continue to [04 — Context Management](./04-context-management.md).
