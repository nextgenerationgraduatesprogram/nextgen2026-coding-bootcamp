# Project Brief

This workshop uses a small bike-rental-demand dataset derived from a public UCI source. The `fetch`
stage downloads and caches the workshop CSV locally, so the exercise stays bounded without requiring
checked-in dataset files. The learning goal is to build two missing workflow stages from a bounded
scaffold, not to build a forecasting model or redesign the project.

The starter branch already completes `fetch` and `prepare`. Students must implement `analyze`, implement `report`, fill in the analyze/report config blocks, write their own tests, and then prove the full workflow works.

## Steps

### Step 1. Understand the starter state

Before you write code, confirm which parts of the pipeline already work and which parts are still missing.

```bash
uv run pytest -q
uv run python scripts/00_fetch.py --config configs/base.yaml --run-name fetch-only
uv run python scripts/01_prepare.py --config configs/base.yaml --run-name prepare-only
```

The starter expectations are:

- `fetch` downloads or reuses the cached workshop source and writes `bike_demand_raw.csv`
- `prepare` writes `prepared_demand.csv`
- `analyze` is not implemented yet
- `report` is not implemented yet
- the full workflow should not be considered complete until you finish the missing stages

### Step 2. Lock the finished output

When you are done, the workflow should produce these analyze artifacts:

- `dataset_overview.json`
- `hourly_demand_profile.csv`
- `weekday_weekend_daily_cycle.png`

It should also produce this report artifact:

- `report.md`

`dataset_overview.json` must contain these keys:

```json
{
  "dataset_name": "bike_rental_demand",
  "n_rows": 96,
  "timestamp_start": "2024-04-04T00:00:00",
  "timestamp_end": "2024-04-07T23:00:00",
  "target_column": "demand",
  "day_types": ["weekday", "weekend"],
  "rows_per_day_type": {
    "weekday": 48
  }
}
```

`hourly_demand_profile.csv` must have one row per `day_type` and hour bucket and these columns in order:

```text
day_type,hour,n_observations,mean_demand,median_demand,std_demand
```

`report.md` must contain these headings:

```text
# Bike Demand Workflow Report
## Dataset Overview
## Analyze Artifacts
## Daily Demand Cycle
## Hourly Demand Profiles
```

### Step 3. Use the intended metric definitions

Keep the metrics simple and reviewable.

- `n_observations`: the number of prepared rows in the `day_type` and hour bucket
- `mean_demand`: the mean demand for that bucket
- `median_demand`: the median demand for that bucket
- `std_demand`: the population standard deviation of demand for that bucket

`report` must read these values from `hourly_demand_profile.csv`. It must not recalculate them inside the report stage.

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
