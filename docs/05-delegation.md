# 05 — Delegation

## What practical question does this guide answer?

This guide answers the handoff question: what prompt should the human actually send to the agent to begin implementation without losing control of the task?

The answer should already be drafted inside `agents/docs/<task-slug>-02-agent-brief.md`. The human reviews that brief, approves it, and then uses the `First Handoff Message` section as the implementation kickoff.

## Why this matters

The cheapest place to catch scope drift is before implementation starts. A good first handoff asks for understanding, file inspection, and a short plan before any code is written. That is especially important in a workshop, where students can mistake quick code generation for successful supervision.

This stage is also where students learn a subtle but important lesson: the first implementation prompt should itself be a reviewed artifact, not an improvised message typed in the moment.

## Steps

### Step 1 — Ask the agent to finalize the first handoff message inside the brief

```text
Using `agents/docs/<task-slug>-01-task-spec.md`, revise `agents/docs/<task-slug>-02-agent-brief.md` in the format specified in `@02-agent-brief.md`.
Make the `First Handoff Message`, `Required Return Format`, and `Stop and Escalate Conditions` sections ready to send verbatim.
Keep the scope bounded.
Do not implement code.
```

If the brief needs another pass after human review, use:

```text
Revise `agents/docs/<task-slug>-02-agent-brief.md` using the review comments below.
Keep the same template structure.
Make the implementation handoff safer and clearer.
Do not implement code.
```

### Step 2 — Use the approved handoff message

After approval, send the `First Handoff Message` section back to the coding agent as the implementation kickoff. Treat the approved brief as the bounded authority for the task.

### Step 3 — Review the return against the brief

When the agent responds, the human should compare that response to the approved brief:

- did the agent restate the task correctly?
- did it identify the right files?
- did it keep the stage boundary intact?
- did it propose a believable verification path?

If the answer is no, students should revise the brief or the plan before any implementation continues.

### Step 4 — Keep the implementation branch reviewable

Do not wait until the very end of the session to look at git state. Once a coherent slice of implementation has been reviewed and looks worth keeping, inspect the branch and decide whether it deserves a bounded commit.

```bash
git status --short
git diff --stat
git diff
git add <files>
git commit -m "<bounded-change>"
```

The teaching point is not “commit after every keystroke.” It is to prefer small, reviewable commits over one large end-of-session dump. If the agent went down the wrong path, correct or discard that work while it is still isolated on the branch instead of letting a bad diff accumulate.

## Outputs

- `agents/docs/<task-slug>-02-agent-brief.md` has been revised into an approved implementation handoff.
- The `First Handoff Message` and `Required Return Format` sections have been reviewed and are ready to send verbatim.
- The task branch stays reviewable through small, intentional commits instead of one late cleanup pass.

## Discussion

1. Why is plan review cheaper and safer than trying to fix drift after the diff already exists?
2. What kind of plan response would make you stop immediately and ask for revision?
3. What does a good implementation handoff reveal about whether the agent actually understood the task?
4. What should the human do if the agent returns a plausible plan that still widens scope?
5. How do stop-and-escalate conditions change the tone and safety of an implementation handoff?

## Next

Continue to [06 — Verification and Decision](./06-verification.md).
