# 02 — Testing and Verification Strategy

## What practical question does this guide answer?

This guide answers the next operator question: how will the human know whether the delegated change is good enough to keep?

The answer should live inside the same task spec draft. Students should ask the agent to strengthen the verification plan inside `agents/docs/<task-slug>-01-task-spec.md` instead of filling a separate testing matrix by hand.

## Why this matters

If verification is vague before implementation starts, the agent can end up inventing the success criteria after the code already exists. That is the opposite of a controlled workflow. A reviewable workshop task should have a plausible evidence story before any code is approved.

This repository is especially good for teaching that point because it already has multiple kinds of evidence available:

- unit-ish or stage-scoped checks
- handoff and integration checks
- end-to-end workflow execution
- direct inspection of generated artifacts
- human reading of report output

No single one of those is enough on its own.

## Steps

### Step 1 — Inspect the testing surfaces

```bash
rg --files tests | sort
sed -n '1,220p' tests/test_analyze_report.py
sed -n '1,220p' tests/test_integration_stage_handoff.py
sed -n '1,220p' tests/test_workflow_smoke.py
```

The goal here is not just to collect filenames. It is to notice what the repo can already tell you mechanically, and what still has to stay human-reviewed.

In the baseline repository, `tests/test_analyze_report.py` is intentionally only a neutral analyze/report check. Students are expected to extend that coverage during the session rather than inherit a solved specification from the starting test file.

### Step 2 — Ask the agent to revise the verification plan inside the task spec

```text
Read `docs/02-testing-as-verification.md`, `tests/test_analyze_report.py`, `tests/test_integration_stage_handoff.py`, and `tests/test_workflow_smoke.py`.
Revise `agents/docs/<task-slug>-01-task-spec.md` in the format specified in `@01-task-spec.md`.
Strengthen the `Verification Plan` and `Decision Threshold` sections using the current repo test surfaces.
Place the updated result in the same file for review.
Do not implement code.
```

If the first draft is too weak, use a follow-up prompt like this:

```text
Revise `agents/docs/<task-slug>-01-task-spec.md` using the review comments below.
Make the verification plan more concrete.
Separate what tests can prove from what still needs human review.
Do not implement code.
```

### Step 3 — Review the verification plan like an evidence ladder

When you read the revised draft, you want to see more than “run pytest.” A good plan should tell you:

- what to test in isolation
- what handoff to check between stages
- whether the whole workflow still runs
- what artifact to inspect directly
- what wording or interpretation still requires a human reader

For the temperature-band example, that means the plan should eventually cover a new `temperature_band_summary.csv` artifact and the report markdown, not just the baseline tests.

## Outputs

- `agents/docs/<task-slug>-01-task-spec.md` has been revised to include a concrete verification plan and clearer decision thresholds.
- That draft has been reviewed to confirm it covers tests, workflow evidence, artifact inspection, and human judgment where needed.

## Discussion

1. Which test layer would catch a broken analyze-to-report handoff fastest in this repository?
2. What could still be wrong with the change even if the full test suite passed?
3. Which task types in this repo create the biggest gap between automated evidence and human judgment?
4. What evidence should come from generated artifacts rather than from `pytest` output?
5. How would your verification plan change if the task touched `prepare` instead of only `analyze` and `report`?

## Next

Continue to [03 — Specification and Approval](./03-specification-templates.md).
