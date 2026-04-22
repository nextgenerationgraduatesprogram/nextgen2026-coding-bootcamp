# Repo Workflow And Missing Piece

This repository keeps the four-stage workflow shape intact: `fetch -> prepare -> analyze -> report`. The first two stages already work and produce inspectable artifacts. The last two stages are intentionally left incomplete so students can implement them from a real scaffold instead of from a blank repo.

## Steps

### Step 1. Run `fetch` and inspect the raw artifact

Start by materializing the bike-demand dataset and looking at the raw payload.

```bash
uv run python scripts/00_fetch.py --config configs/base.yaml --run-name fetch-only
LATEST_FETCH=$(ls -1dt runs/*fetch-only* | head -n1)
find "$LATEST_FETCH" -maxdepth 3 -type f | sort
python - <<'PY'
from pathlib import Path
import pandas as pd
latest = sorted(Path("runs").glob("*fetch-only*"), key=lambda p: p.stat().st_mtime)[-1]
raw = pd.read_csv(latest / "fetch" / "bike_demand_raw.csv")
print("shape =", raw.shape)
print("columns =", raw.columns.tolist())
print(raw.head().to_string(index=False))
PY
```

The working `fetch` stage gives you the raw bike-demand table. You do not need to change it.

### Step 2. Run `prepare` and inspect the prepared artifacts

Then inspect the exact input that `analyze` must consume.

```bash
uv run python scripts/01_prepare.py --config configs/base.yaml --run-name prepare-only
LATEST_PREPARE=$(ls -1dt runs/*prepare-only* | head -n1)
find "$LATEST_PREPARE" -maxdepth 3 -type f | sort
python - <<'PY'
from pathlib import Path
import pandas as pd
latest = sorted(Path("runs").glob("*prepare-only*"), key=lambda p: p.stat().st_mtime)[-1]
prepared = pd.read_csv(latest / "prepare" / "prepared_demand.csv")
print("shape =", prepared.shape)
print("columns =", prepared.columns.tolist())
print(prepared.head().to_string(index=False))
print(prepared["day_type"].value_counts().sort_index().to_string())
PY
```

The current `prepare` contract is:

- `prepared_demand.csv`: columns `timestamp`, `demand`, `hour`, `day_type`, `season`, `weather`
- timestamps are hourly ISO-8601 strings sorted ascending

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

- `analyze.py` resolves prepare input, validates config, and shows the expected helper structure
- `report.py` resolves analyze inputs, validates config, and shows the expected helper structure
- the analyze/report config blocks are placeholders that students must fill in

### Step 4. Fill in the config blocks

Students should put the same final values in `configs/base.yaml` and the matching stage fragments.

Use this structure for `analysis`:

```yaml
analysis:
  dataset_overview_name: dataset_overview.json
  hourly_profile_name: hourly_demand_profile.csv
  daily_cycle_plot_name: weekday_weekend_daily_cycle.png
  generate_daily_cycle_plot: true
```

Use this structure for `report`:

```yaml
report:
  markdown_name: report.md
  include_daily_cycle_plot: true
```

### Step 5. Implement the analyze stage

Use the provided helper names and return contract. The exact internals are up to you, but the stage should follow this structure:

```python
def run_analyze(cfg, ctx=None, prepared_csv=None) -> dict:
    prepared_table_csv = _resolve_prepare_input(...)
    analysis_cfg = _validate_analysis_config(cfg)

    shared_output_dir = Path(cfg.paths.results_dir)
    shared_output_dir.mkdir(parents=True, exist_ok=True)

    prepared = pd.read_csv(prepared_table_csv)

    overview = build_dataset_overview(
        prepared=prepared,
        dataset_name=str(cfg.fetch.dataset_name),
    )
    profile = build_hourly_demand_profile(prepared=prepared)

    # write dataset_overview.json
    # write hourly_demand_profile.csv
    # optionally write weekday_weekend_daily_cycle.png
    # copy outputs into ctx.run_dir / "analyze" when ctx is provided
    # return the artifact dictionary expected by the workflow
```

Reference code for shared-path and run-path behavior lives in `src/nextgen2026_coding_bootcamp/steps/prepare.py`.

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

- dataset overview values from `dataset_overview.json`
- an analyze-artifact inventory
- a daily-cycle plot reference when enabled
- an `Hourly Demand Profiles` Markdown table rendered from `hourly_demand_profile.csv`

### Step 7. Write your own behavioural tests

Create your own analyze/report tests before implementation. A good default is:

- `tests/test_analyze_contract.py`
- `tests/test_report_contract.py`

Those tests should lock the final artifact contract you want to validate later in the session.
