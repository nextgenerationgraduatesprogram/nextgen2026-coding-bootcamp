# Project Card: Build Analyze And Report

This workshop starts from a partial workflow. `fetch` and `prepare` already work. `analyze` and `report` are stubs that students must complete.

## Steps

### Step 1. Lock the final output contract

Your completed workflow must produce these outputs:

- `dataset_overview.json`
- `hourly_demand_profile.csv`
- `weekday_weekend_daily_cycle.png`
- `report.md`

`hourly_demand_profile.csv` must contain these columns in order:

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

### Step 2. Implement the missing files

The main student-owned code is:

- `src/nextgen2026_coding_bootcamp/steps/analyze.py`
- `src/nextgen2026_coding_bootcamp/steps/report.py`
- `configs/base.yaml`
- `configs/stages/analyze.yaml`
- `configs/stages/report.yaml`

Recommended student-authored test files are:

- `tests/test_analyze_contract.py`
- `tests/test_report_contract.py`

### Step 3. Use the existing code as reference

Use these files for workflow shape, artifact handoff, and thin stage-script structure:

- `src/nextgen2026_coding_bootcamp/steps/fetch.py`
- `src/nextgen2026_coding_bootcamp/steps/prepare.py`
- `src/nextgen2026_coding_bootcamp/workflow.py`
- `scripts/00_fetch.py`
- `scripts/01_prepare.py`

### Step 4. Stay inside scope

Do not add forecasting models, workflow redesign, notebook-first solutions, or broad refactors. `report` must read analyze artifacts instead of recomputing metrics.
