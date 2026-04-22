# Validation, Review, And Merge Request

Use this checklist after you have finished the student implementation. Run the commands in order and do not skip the artifact inspection step.

## Steps

### Step 1. Run your analyze/report contract tests

Run the tests you wrote for the missing stages.

```bash
uv run pytest -q tests/test_analyze_contract.py
uv run pytest -q tests/test_report_contract.py
```

### Step 2. Run the full test suite

Confirm the branch is still green after your student-written tests are in place.

```bash
uv run pytest -q
```

### Step 3. Run the full workflow

Prove that the completed branch now runs `fetch -> prepare -> analyze -> report`.

```bash
uv run python scripts/run_workflow.py --profile base --run-name review-check
```

### Step 4. Inspect the generated artifacts

Check the run-scoped outputs and the rendered report instead of trusting the exit code alone.

```bash
LATEST_RUN=$(ls -1dt runs/* | head -n1)
find "$LATEST_RUN" -maxdepth 3 -type f | sort
sed -n '1,220p' "$LATEST_RUN/report/report.md"
python - <<'PY'
from pathlib import Path
import pandas as pd
latest = sorted(Path("runs").glob("*"), key=lambda p: p.stat().st_mtime, reverse=True)[0]
summary = latest / "analyze" / "class_image_summary.csv"
print(pd.read_csv(summary).head(10).to_string(index=False))
PY
```

### Step 5. Review the diff

Check that the change stayed inside the intended analyze/report/config/test surface.

```bash
git status --short
git diff --stat
git diff -- src/nextgen2026_coding_bootcamp/steps/analyze.py src/nextgen2026_coding_bootcamp/steps/report.py configs tests
```

### Step 6. Commit and push your branch

Create a reviewable commit and push it to your remote branch.

```bash
git add AGENTS.md README.md docs configs src tests
git commit -m "Implement analyze and report workflow stages"
git push -u origin <your-branch>
```

### Step 7. Open the pull request

Open the pull request in your Git host and include:

- a short summary of the change
- the tests you ran
- the workflow command you ran
- the artifacts you inspected
- any remaining review concern
