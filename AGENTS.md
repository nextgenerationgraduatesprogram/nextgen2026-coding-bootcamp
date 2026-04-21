# Repository Instructions for Coding Agents

## Purpose

This repository teaches reproducible, reviewable workflow development on the Bike Sharing dataset.

## Canonical Commands

- Full test suite: `uv run pytest -q`
- Full workflow: `uv run python scripts/run_workflow.py --profile base --run-name local-run`
- Stage scripts:
  - `uv run python scripts/00_fetch.py --config configs/stages/fetch.yaml --run-name fetch-only`
  - `uv run python scripts/01_prepare.py --config configs/stages/prepare.yaml --run-name prepare-only`
  - `uv run python scripts/02_analyze.py --config configs/stages/analyze.yaml --run-name analyze-only`
  - `uv run python scripts/03_report.py --config configs/stages/report.yaml --run-name report-only`

## Repository Map

- `src/nextgen2026_coding_bootcamp/steps/`: stage logic
- `scripts/`: CLI wrappers and workflow runner
- `configs/`: run/path/stage/profile configuration
- `tests/`: regression and workflow checks
- `runs/`: run-scoped artifacts and manifests
- `docs/`: workshop guides, templates, and archive

## Delegation Defaults

- Use one agent per bounded contract.
- Request a plan before implementation.
- Keep diffs small and scoped.
- Run verification commands listed in the task contract.

## Review Requirements

Every delegated change must include:

- contract alignment check
- diff review
- test evidence
- artifact/output inspection
- explicit Accept/Revise/Reject decision

## Do Not Change Unless Explicitly Requested

- stage script CLI semantics
- stage ordering in full workflow (`fetch -> prepare -> analyze -> report`)
- artifact contracts consumed by downstream stages
- scientific meaning of transformations without a documented review decision

## Escalate to For Human Feedback Immediately

- destructive git operations
- broad refactors outside contract
- semantic or interpretation changes that exceed acceptance criteria
