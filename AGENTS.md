# Repository Instructions for Coding Agents

## Purpose

This repository is a workshop scaffold for building the `analyze` and `report` stages of a small image-analysis workflow built on `sklearn.datasets.load_digits`.

The starter state is intentional:

- `fetch` already works
- `prepare` already works
- `analyze` is a student-facing stub
- `report` is a student-facing stub

Students are expected to implement the missing analyze/report logic, write their own behavioural tests, and then prove the full workflow works end to end.

## Workflow Shape

The workflow stages are fixed and must remain in this order:

1. `fetch`
2. `prepare`
3. `analyze`
4. `report`

`fetch` materializes the raw digits dataset. `prepare` writes normalized images plus metadata. `analyze` must write the derived analysis artifacts. `report` must consume analyze outputs and turn them into a Markdown report.

## Canonical Commands

Run the starter test suite:

```bash
uv run pytest -q
```

Run the working stages that students should inspect before implementing anything:

```bash
uv run python scripts/00_fetch.py --config configs/base.yaml --run-name fetch-only
uv run python scripts/01_prepare.py --config configs/base.yaml --run-name prepare-only
```

Inspect the latest fetch or prepare run:

```bash
LATEST_RUN=$(ls -1dt runs/* | head -n1)
find "$LATEST_RUN" -maxdepth 3 -type f | sort
```

Run the full workflow only after the student has completed the missing analyze/report work:

```bash
uv run python scripts/run_workflow.py --profile base --run-name completed-workflow
```

## Authoritative Code Locations

The authoritative stage logic lives in `src/nextgen2026_coding_bootcamp/steps/`. The CLI wrappers in `scripts/` should stay thin.

The student-owned implementation surface is:

- `src/nextgen2026_coding_bootcamp/steps/analyze.py`
- `src/nextgen2026_coding_bootcamp/steps/report.py`
- `configs/base.yaml`
- `configs/stages/analyze.yaml`
- `configs/stages/report.yaml`
- student-authored analyze/report tests

Reference code for stage structure and artifact handoff lives in:

- `src/nextgen2026_coding_bootcamp/steps/fetch.py`
- `src/nextgen2026_coding_bootcamp/steps/prepare.py`
- `src/nextgen2026_coding_bootcamp/workflow.py`

## Repo Boundaries

This branch is an image-analysis exercise, not a model-training project. Do not add classifier training, CNN code, augmentation pipelines, notebooks as the main interface, async infrastructure, or a new workflow architecture. Keep the existing stage boundaries and artifact flow.

`report` must consume outputs written by `analyze`. Do not duplicate class-summary calculations inside `report`, and do not bypass the analyze artifact contract just to make the report pass.

## Delegation Defaults

Ask for a plan before implementation. Keep diffs small, bounded, and easy to review. Prefer changing only the files that directly support the student task.

When delegating, give the agent:

1. the task contract
2. the relevant files
3. the exact verification commands

Require the result to report contract alignment, tests run, artifact inspection, and an explicit accept or revise recommendation.

## Review Requirements

Every completed student change should be checked against:

1. the behavioural tests the student wrote
2. the full test suite
3. the full workflow run
4. generated artifacts in the latest run directory
5. the git diff
6. the rule that `report` only reads analyze artifacts

## Escalate to a Human Immediately

Escalate if the requested change would redesign the workflow, alter the scientific framing beyond the workshop task, introduce model training, or require a broad refactor outside the bounded analyze/report/config extension.
