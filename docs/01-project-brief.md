# Project Brief

This workshop uses the public UCI SMS Spam Collection dataset. The `fetch` stage downloads the raw data at runtime and caches it under `data/raw/`, so the repository stays free of checked-in dataset files. The learning goal is to build two missing workflow stages from a bounded scaffold, not to build a full spam detector or redesign the project.

The starter branch already completes `fetch` and `prepare`. Students must implement `analyze`, implement `report`, fill in the analyze/report config blocks, write their own tests, and then prove the full workflow works.

## Steps

### Step 0. Create a local `.env`

Before you work on the LLM-backed `analyze` stage, create a `.env` file at the repository root from the checked-in example:

```bash
cp example.env .env
```

Then edit `.env` and set `OPENAI_API_KEY`. The scripts in this repo load `.env` automatically before config resolution. Keep the model name in YAML config.

### Step 1. Understand the starter state

Before you write code, confirm which parts of the pipeline already work and which parts are still missing.

```bash
uv run pytest -q
uv run python scripts/00_fetch.py --config configs/base.yaml --run-name fetch-only
uv run python scripts/01_prepare.py --config configs/base.yaml --run-name prepare-only
```

The starter expectations are:

- `fetch` downloads the UCI dataset and writes `sms_spam_collection.tsv`
- `prepare` writes `prepared_messages.csv`
- `analyze` is not implemented yet
- `report` is not implemented yet
- the full workflow should not be considered complete until you finish the missing stages

### Step 2. Lock the finished output

When you are done, the workflow should produce these analyze artifacts:

- `message_predictions.csv`
- `evaluation_summary.json`

It should also produce this report artifact:

- `report.md`

`message_predictions.csv` must have these columns in order:

```text
message_id,text,true_label,predicted_label,is_correct,raw_response
```

`evaluation_summary.json` must contain these keys:

```json
{
  "dataset_name": "sms_spam_collection",
  "n_messages_prepared": 5574,
  "sample_size": 25,
  "sample_seed": 2026,
  "labels": ["ham", "spam"],
  "model": "your-model-name",
  "temperature": 0.0,
  "n_correct": 0,
  "n_incorrect": 0,
  "accuracy": 0.0,
  "invalid_response_count": 0,
  "confusion_matrix": {
    "ham": {
      "ham": 0,
      "spam": 0,
      "invalid": 0
    }
  }
}
```

`report.md` must contain these headings:

```text
# SMS Classification Workflow Report
## Dataset Overview
## Analyze Artifacts
## Evaluation Summary
## Prediction Examples
```

### Step 3. Use the intended behaviour

Keep the scope small and reviewable.

- `analyze` should draw a deterministic sample from `prepared_messages.csv`
- `analyze` should call the model once per sampled message
- `analyze` should normalize the model output into `ham`, `spam`, or `invalid`
- `analyze` should preserve the raw model response for inspection
- `report` must read the summary metrics from `evaluation_summary.json`
- `report` must read the example rows from `message_predictions.csv`

`report` must not recompute the evaluation summary inside the report stage.

### Step 4. Implement the missing surfaces

Students are expected to finish these files:

- `src/nextgen2026_coding_bootcamp/steps/analyze.py`
- `src/nextgen2026_coding_bootcamp/steps/report.py`
- `configs/base.yaml`
- `configs/stages/analyze.yaml`
- `configs/stages/report.yaml`

Recommended student-authored test files are:

- `tests/test_analyze_contract.py`
- `tests/test_report_contract.py`

Use these files as reference code:

- `src/nextgen2026_coding_bootcamp/steps/fetch.py`
- `src/nextgen2026_coding_bootcamp/steps/prepare.py`
- `src/nextgen2026_coding_bootcamp/workflow.py`
