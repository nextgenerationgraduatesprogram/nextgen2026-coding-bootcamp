# 02 — Behavioural Test Design and Implementation

## What practical question does this guide answer?

This guide answers the next operator question: how do you turn the approved spec into executable behavioural tests before feature code starts?

The behavioural tests are the executable contract for the change. They should come from the approved spec, use repo-real surfaces where possible, and make the expected behaviour concrete before implementation begins.

## Why this matters

If behaviour is only described abstractly, the agent can improvise what “done” means after the code already exists. That makes review weaker and turns testing into a backfilled justification step.

This repository is a good place to teach the opposite habit. The repo already has stage-scoped checks, handoff checks, workflow smoke tests, and artifact outputs. The behavioural test phase uses those surfaces to pin expected behaviour early.

## Steps

### Step 1 — Inspect the existing test surfaces

```bash
rg --files tests | sort
sed -n '1,220p' tests/test_analyze_report.py
sed -n '1,220p' tests/test_integration_stage_handoff.py
sed -n '1,220p' tests/test_workflow_smoke.py
```

The goal is to understand:

- which existing tests are close to the behaviour you need
- what input/output shapes are already used in the repo
- whether the behavioural contract belongs in a stage-scoped test, a handoff test, a workflow test, or a small combination

### Step 2 — Ask the agent to refine the behavioural cases in the spec if needed

If the approved spec still has weak behavioural cases, revise it before writing tests.

```text
Read `docs/02-behavioural-validation.md` and the relevant test files in `tests/`.
Revise `agents/docs/<task-slug>-01-task-spec.md` in the format specified in `@01-task-spec.md`.
Strengthen the behavioural cases so they can be implemented as executable tests.
Do not implement code or tests.
```

### Step 3 — Implement the behavioural tests

Once the spec is approved and the cases are concrete, implement the behavioural tests in the repo.

```text
Please implement the behavioural cases described in `agents/docs/<task-slug>-01-task-spec.md` as executable tests.
```

The expected pattern is:

- use the approved behavioural cases as the source of truth
- create or extend tests in `tests/`
- make the expected input and output explicit
- keep the tests bounded to the approved behaviour

These tests may fail initially. That is acceptable. A failing behavioural test is often the evidence that the implementation work still needs to be done.

### Step 4 — Review the behavioural tests before feature implementation

Before feature code starts, review whether the tests:

- actually encode the approved behaviour
- use the right stage boundary and repo surface
- avoid quietly expanding scope
- fail for the right reason if the feature is not implemented yet

If the tests reveal a bad spec or a wrong assumption, revise the spec before moving to implementation planning.

Once the behavioural tests are approved, prefer to start a fresh chat for implementation planning. The next chat should begin from the approved spec, the implemented behavioural tests, and the planning guide rather than from the whole test-design conversation.

## Outputs

- The approved spec includes concrete behavioural cases.
- Executable behavioural tests exist in `tests/` before feature code starts.
- Those tests have been reviewed for fidelity to the approved spec, not just for syntax.

## Discussion

1. What makes a behavioural test stronger than a vague “run pytest” instruction?
2. When should a behavioural contract live in a stage-scoped test versus a handoff or smoke test?
3. What would tell you that a behavioural test is encoding a design guess rather than an approved requirement?
4. How much repo context does the agent actually need to design these tests well without drifting into implementation?
5. Why is it useful for the behavioural tests to exist before feature implementation even if they fail?
6. What should happen if the new tests reveal that the approved spec was still underspecified?

## Next

Continue to [03 — Implementation Plan](./03-implementation-plan.md).
