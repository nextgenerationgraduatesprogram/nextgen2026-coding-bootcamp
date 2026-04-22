# Repo Workflow And Missing Piece

This repository keeps the four-stage workflow shape intact: `fetch -> prepare -> analyze -> report`. The first two stages already work and produce inspectable artifacts. The last two stages are intentionally left incomplete so students can implement them from a real scaffold instead of from a blank repo.

## Steps

### Step 0. Create `.env` for later stages

Create a `.env` file at the repository root from the checked-in example:

```bash
cp example.env .env
```

Set `OPENAI_API_KEY` in `.env`. The scripts load it automatically. You do not need the key for `fetch` or `prepare`, but you will need it once you implement `analyze`.

### Step 1. Run `fetch` and inspect the raw artifact

Start by downloading the public SMS dataset and looking at the cached raw payload. Use `--force-download` when you want to refresh the cache explicitly.

```bash
uv run python scripts/00_fetch.py --config configs/base.yaml --run-name fetch-only
LATEST_FETCH=$(ls -1dt runs/*fetch-only* | head -n1)
find "$LATEST_FETCH" -maxdepth 3 -type f | sort
python - <<'PY'
from pathlib import Path
latest = sorted(Path("runs").glob("*fetch-only*"), key=lambda p: p.stat().st_mtime)[-1]
raw_path = latest / "fetch" / "sms_spam_collection.tsv"
lines = raw_path.read_text(encoding="utf-8").splitlines()
print("line_count =", len(lines))
print("first_rows =")
for row in lines[:5]:
    print(row)
PY
```

The working `fetch` stage gives you the raw SMS messages. You do not need to change it.

### Step 2. Run `prepare` and inspect the prepared artifact

Then inspect the exact input that `analyze` must consume.

```bash
uv run python scripts/01_prepare.py --config configs/base.yaml --run-name prepare-only
LATEST_PREPARE=$(ls -1dt runs/*prepare-only* | head -n1)
find "$LATEST_PREPARE" -maxdepth 3 -type f | sort
python - <<'PY'
from pathlib import Path
import pandas as pd
latest = sorted(Path("runs").glob("*prepare-only*"), key=lambda p: p.stat().st_mtime)[-1]
prepared = pd.read_csv(latest / "prepare" / "prepared_messages.csv")
print("prepared.shape =", prepared.shape)
print("prepared.columns =", prepared.columns.tolist())
print(prepared.head().to_string(index=False))
print(prepared["label"].value_counts().sort_index().to_string())
PY
```

The current `prepare` contract is:

- `prepared_messages.csv`: columns `message_id`, `label`, and `text`
- `label`: normalized to `ham` or `spam`
- `text`: stripped and whitespace-normalized

This is the only input the analyze stage needs.

### Step 3. Inspect the missing code

Open the student-facing stubs before you implement anything.

```bash
sed -n '1,260p' src/nextgen2026_coding_bootcamp/steps/analyze.py
sed -n '1,260p' src/nextgen2026_coding_bootcamp/steps/report.py
sed -n '1,220p' configs/base.yaml
sed -n '1,220p' configs/stages/analyze.yaml
sed -n '1,220p' configs/stages/report.yaml
```

The current scaffold state is intentional:

- `analyze.py` resolves prepare inputs, validates config, and shows the expected helper structure
- `report.py` resolves analyze inputs, validates config, and shows the expected helper structure
- the analyze/report config blocks are placeholders that students must fill in

### Step 4. Fill in the config blocks

Students should put the same final values in `configs/base.yaml` and the matching stage fragments.

Use this structure for `analysis`:

```yaml
analysis:
  predictions_name: message_predictions.csv
  evaluation_summary_name: evaluation_summary.json
  sample_size: 25
  sample_seed: 2026
  model: YOUR_MODEL_NAME
  temperature: 0.0
```

Use this structure for `report`:

```yaml
report:
  markdown_name: report.md
  max_examples: 10
```

### Step 5. Implement the analyze stage

Use the provided helper names and return contract. The exact internals are up to you, but the stage should follow this structure:

```python
def run_analyze(cfg, ctx=None, prepared_messages_csv=None) -> dict:
    prepared_messages_path = _resolve_prepare_input(...)
    analysis_cfg = _validate_analysis_config(cfg)

    shared_output_dir = Path(cfg.paths.results_dir)
    shared_output_dir.mkdir(parents=True, exist_ok=True)

    prepared_messages = pd.read_csv(prepared_messages_path)
    sampled_messages = select_message_sample(
        prepared_messages=prepared_messages,
        sample_size=analysis_cfg["sample_size"],
        sample_seed=analysis_cfg["sample_seed"],
    )

    # call the model on each sampled message
    # write message_predictions.csv
    # write evaluation_summary.json
    # copy outputs into ctx.run_dir / "analyze" when ctx is provided
    # return the artifact dictionary expected by the workflow
```

Reference code for shared-path and run-path behaviour lives in `src/nextgen2026_coding_bootcamp/steps/prepare.py`.

### Step 6. Implement the report stage

The report stage must consume analyze artifacts, not recompute them.

```python
def run_report(cfg, ctx=None) -> dict:
    names = _validate_report_config(cfg)
    shared_output_dir = Path(cfg.paths.results_dir)
    shared_output_dir.mkdir(parents=True, exist_ok=True)

    shared_inputs = _shared_analyze_paths(cfg, names)
    report_inputs = shared_inputs if ctx is None else _ctx_analyze_paths(cfg, ctx, names)

    # render report markdown from analyze artifacts
    # write the shared report
    # write a run-scoped report when ctx is provided
    # return the artifact dictionary expected by the workflow
```

Your report should include:

- dataset values from `evaluation_summary.json`
- an analyze-artifact inventory
- summary metrics from `evaluation_summary.json`
- a `Prediction Examples` Markdown table rendered from `message_predictions.csv`

### Step 7. Write your own behavioural tests

Create your own analyze/report tests before implementation. A good default is:

- `tests/test_analyze_contract.py`
- `tests/test_report_contract.py`

Those tests should lock the final artifact contract you want to validate later in the session.
