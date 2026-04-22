# 03 — Implementation Plan

## What practical question does this guide answer?

This guide answers the planning question: with an approved spec and executable behavioural tests in place, what is the bounded plan for implementation?

The implementation plan is the reviewed handoff artifact for the build phase. It should turn the approved spec into an ordered implementation sequence, a minimal context bundle, explicit escalation conditions, and a clean checkpoint before feature code begins.

## Why this matters

The cheapest place to catch drift after the spec phase is still before feature code starts. A good implementation plan identifies the right files, the right test surfaces, and the right order of operations without flooding the agent with irrelevant context.

This is also where context management belongs. The goal is not to attach the whole repo. The goal is to justify the smallest bundle of files and commands that lets the agent implement the approved task safely.

This is also the right place to define the restore path. If the implementation goes bad, you want a known good branch state containing the approved spec, behavioural tests, and implementation plan so you can discard the code work without losing the planning artifacts.

## Steps

### Step 1 — Inspect likely implementation surfaces

```bash
sed -n '1,260p' AGENTS.md
rg --files src/nextgen2026_coding_bootcamp/steps scripts tests configs | sort
```

The goal is to confirm:

- likely code surfaces
- likely test surfaces
- any config or script entrypoints that might be relevant
- any `AGENTS.md` constraints that should be repeated in the plan

### Step 2 — Ask the agent to draft the implementation plan

```text
Using `agents/docs/<task-slug>-01-task-spec.md` and the behavioural tests already added in `tests/`, prepare the implementation plan in the format specified in `@02-implementation-plan.md`.
Place the result in `agents/docs/<task-slug>-02-implementation-plan.md` for review.
Use the current repo structure to fill:
- approved objective
- bounded scope
- behavioural contract to satisfy
- minimal context bundle
- likely files to inspect or change
- ordered implementation sequence
- pre-implementation checkpoint
- planned unit or integration test additions
- verification commands
- rollback or cleanup approach
- stop and escalate conditions
Do not implement feature code.
```

### Step 3 — Review the plan for sufficiency and restraint

A good plan is not just plausible. It is bounded. You should be able to say:

- why each context item is included
- why the file touch set is realistic
- what work is covered by the behavioural tests already in place
- what additional unit or integration tests are still planned
- what condition would require stopping and revising the plan

### Step 4 — Revise the plan if needed

```text
Revise `agents/docs/<task-slug>-02-implementation-plan.md` using the review comments below.
Trim the context bundle to the minimum needed.
Keep the scope bounded and aligned to the approved spec and behavioural tests.
Do not implement feature code.
```

### Step 5 — Commit the approved plan before feature implementation

Before feature code starts, create a bounded checkpoint commit that captures the approved planning state.

That commit should normally include:

- the approved spec in `agents/docs/`
- the executable behavioural tests in `tests/`
- the approved implementation plan in `agents/docs/`

Example:

```bash
git status --short
git add agents/docs/<task-slug>-01-task-spec.md
git add agents/docs/<task-slug>-02-implementation-plan.md
git add tests/<relevant-test-files>
git commit -m "Checkpoint approved spec and implementation plan"
git rev-parse --short HEAD
```

Record that checkpoint commit ID in the plan or session notes. The purpose of this commit is not ceremony. It gives you a clean restore point if the implementation slice needs to be discarded.

After the plan is approved and checkpointed, prefer to start a fresh chat for feature implementation. Give that chat the approved spec, the behavioural tests, the approved implementation plan, and the specific repo files it needs. Do not rely on the model remembering earlier rejected plans.

## Outputs

- `agents/docs/<task-slug>-02-implementation-plan.md` exists as the reviewed implementation plan.
- The plan references the approved spec and the executable behavioural tests.
- The plan makes context management, file references, verification commands, escalation conditions, and rollback mechanics explicit.
- The branch has a clean checkpoint commit before feature implementation begins.

## Discussion

1. What makes a context bundle minimal rather than merely short?
2. Which repo files belong in the first implementation turn for the temperature-band example?
3. What work should already be covered by the behavioural tests before feature implementation begins?
4. Which parts of the implementation plan should live in the template versus in `AGENTS.md`?
5. What kind of plan response would make you stop immediately and ask for revision?
6. How do escalation conditions protect the implementation phase from silent scope growth?

## Next

Continue to [04 — Implementation](./04-implementation.md).
