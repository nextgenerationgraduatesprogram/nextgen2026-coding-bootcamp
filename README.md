# Digits Image-Analysis Workshop Branch

This branch is the shared starter for a short workflow workshop. The repository already contains the first half of the pipeline, `fetch -> prepare`, and intentionally leaves `analyze` and `report` incomplete for students to build.

The workshop goal is to finish the missing stages without redesigning the workflow. Students should define their own behavioural tests, implement the analyze/report logic, fill in the analyze/report config blocks, and then validate the full workflow end to end.

## Steps

### Step 1. Start from the working baseline

Run the starter test suite and inspect the first two workflow stages.

```bash
uv run pytest -q
uv run python scripts/00_fetch.py --config configs/base.yaml --run-name fetch-only
uv run python scripts/01_prepare.py --config configs/base.yaml --run-name prepare-only
```

### Step 2. Inspect the current artifacts

Look at the run-scoped outputs so you know what `fetch` and `prepare` already produce before you implement anything else.

```bash
LATEST_RUN=$(ls -1dt runs/* | head -n1)
find "$LATEST_RUN" -maxdepth 3 -type f | sort
```

### Step 3. Work through the session docs

Read the docs in order and keep the project card open while you work.

1. [docs/01-project-brief.md](docs/01-project-brief.md)
2. [docs/02-repo-workflow-and-missing-piece.md](docs/02-repo-workflow-and-missing-piece.md)
3. [docs/03-ai-agent-workflow.md](docs/03-ai-agent-workflow.md)
4. [docs/04-validation-review-and-merge-request.md](docs/04-validation-review-and-merge-request.md)
5. [docs/project-card.md](docs/project-card.md)

### Step 4. Finish the missing stages

Your implementation surface is:

- `src/nextgen2026_coding_bootcamp/steps/analyze.py`
- `src/nextgen2026_coding_bootcamp/steps/report.py`
- `configs/base.yaml`
- `configs/stages/analyze.yaml`
- `configs/stages/report.yaml`
- your own analyze/report tests

### Step 5. Run the completed workflow

Only after you have filled in the stubs and config should you run the full workflow.

```bash
uv run python scripts/run_workflow.py --profile base --run-name completed-workflow
```
