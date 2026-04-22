# 01 — Problem Definition and Specification

## What practical question does this guide answer?

This guide answers the first operator question: what problem are you actually solving, and when is the task specification clear enough to approve?

The spec is the main pre-implementation contract. It should capture the bounded problem, the intended repo change, the key constraints, the likely surfaces, and the design feedback that turns a vague idea into an approved specification.

## Why this matters

A task can sound reasonable and still be a bad implementation target. A one-line change in `prepare` can alter every downstream artifact. A feature that looks small can hide a refactor, a stage-boundary mistake, or an interpretive change that exceeds the workshop contract.

That is why the session starts with problem definition rather than with coding. The agent can help draft the spec, but you still have to decide what the task is, what it must not change, and what feedback is necessary before the task becomes an approved contract.

## Steps

### Step 1 — Ground the problem in the repo

Start with the real repo, not an imagined task.

```bash
sed -n '1,260p' AGENTS.md
rg -n "def run_(fetch|prepare|analyze|report)" src/nextgen2026_coding_bootcamp/steps
rg --files tests | sort
```

The goal is to identify:

- which stage should own the change
- what repo surfaces are likely involved
- what existing tests and outputs already constrain the work
- what `AGENTS.md` rules already limit the task

### Step 2 — Ask the agent to draft the task spec

```text
Read `AGENTS.md`, `docs/01-specification.md`, and the repo structure first.
Convert the task idea below into the format specified in `@01-task-spec.md`.
Place the result in `agents/docs/<task-slug>-01-task-spec.md` for review.
Use the current repo structure and tests to fill:
- the problem definition
- the intended repo change
- risk and review burden
- likely files and surfaces
- constraints and non-goals
- initial behavioural cases
Do not implement code or tests.

Task idea:
<describe the task here>
```

### Step 3 — Review the draft like a contract

Read the draft as an argument the agent is making:

- is the problem statement actually the problem you want to solve?
- is the task bounded enough for one branch?
- does it identify the right stage and file surfaces?
- does it state what must not change?
- do the behavioural cases sound concrete enough to test later?

If the answer is no, revise the spec before anything else moves forward.

### Step 4 — Iterate on design feedback inside the spec

Design feedback is part of the specification loop, not a separate stage. Keep the feedback and the resolved revisions visible inside the spec artifact itself.

Use a revision prompt like this:

```text
Revise `agents/docs/<task-slug>-01-task-spec.md` using the review comments below.
Strengthen the problem statement, constraints, behavioural cases, and approval boundaries.
Keep the format specified in `@01-task-spec.md`.
Do not implement code or tests.
```

### Step 5 — Approve the spec deliberately

The approval moment should feel explicit. You should be able to say:

- this is the problem
- this is the intended repo change
- these are the behavioural expectations
- this is what must not change
- this is what would later cause `Revise` or `Reject`

If you cannot say those things yet, the spec is not ready.

Once the spec is approved, prefer to start a fresh chat for the behavioural test phase. Hand the new chat the approved spec, the relevant test files, and the current guide instead of the full draft history.

## Outputs

- `agents/docs/<task-slug>-01-task-spec.md` exists as the reviewed task spec.
- The spec contains bounded scope, repo grounding, design feedback, and concrete behavioural cases.
- The spec has an explicit approval status before behavioural test implementation begins.

## Discussion

1. What makes a task bounded enough for one branch in this repository?
2. Which kinds of design feedback belong inside the spec instead of being left as side comments?
3. How would you notice that the agent has chosen the wrong stage for the change?
4. Which `AGENTS.md` rules are most important to restate inside the spec, and which are already safe to leave implicit?
5. What is the difference between a helpful ambiguity and a dangerous ambiguity at the spec stage?
6. Which sentence in the spec is most likely to cause downstream scope drift if it stays vague?

## Next

Continue to [02 — Behavioural Test Design and Implementation](./02-behavioural-validation.md).
