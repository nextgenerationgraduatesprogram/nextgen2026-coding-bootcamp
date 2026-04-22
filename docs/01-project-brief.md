# Project Brief

This workshop uses the handwritten digits dataset that ships with `scikit-learn`, so the exercise stays fast and offline-friendly. The learning goal is to build two missing workflow stages from a bounded scaffold, not to train a classifier or redesign the project.

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

- `fetch` writes `digits_raw.npz`
- `prepare` writes `images.npy` and `metadata.csv`
- `analyze` is not implemented yet
- `report` is not implemented yet
- the full workflow should not be considered complete until you finish the missing stages

### Step 2. Lock the finished output

When you are done, the workflow should produce these analyze artifacts:

- `dataset_overview.json`
- `class_image_summary.csv`
- `class_representatives.png`

It should also produce this report artifact:

- `report.md`

`dataset_overview.json` must contain these keys:

```json
{
  "dataset_name": "sklearn_digits",
  "n_images": 1797,
  "n_classes": 10,
  "image_height": 8,
  "image_width": 8,
  "labels": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
  "images_per_class": {
    "0": 178
  }
}
```

`class_image_summary.csv` must have one row per digit class and these columns in order:

```text
label,n_images,mean_intensity,std_intensity,mean_edge_density
```

`report.md` must contain these headings:

```text
# Digits Workflow Report
## Dataset Overview
## Analyze Artifacts
## Representative Digits
## Digit Class Profiles
```

### Step 3. Use the intended metric definitions

Keep the metrics simple and reviewable.

- `n_images`: the number of prepared images for the class
- `mean_intensity`: the mean of the per-image mean intensities for that class
- `std_intensity`: the population standard deviation of the per-image mean intensities for that class
- `mean_edge_density`: the mean of the per-image edge densities for that class
- `edge_density`: the fraction of horizontal and vertical neighboring pixel differences that are strictly greater than `edge_threshold`

`report` must read these values from `class_image_summary.csv`. It must not recalculate them inside the report stage.

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
