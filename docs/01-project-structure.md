# Project Structure

This chapter introduces project structure as a reproducibility control, not a cosmetic preference. It separates analytical method code from execution wrappers so transformations, orchestration, and interface wiring can evolve without being conflated.

That separation improves interpretability when runs differ, because it narrows where causes can originate. It also creates clear reuse boundaries for testing and orchestration, which are required for the later chapters to remain methodologically consistent.

## 1. What This Chapter Adds

This section defines the minimal architecture contract that keeps stage logic reusable and wrappers operationally lightweight:

- reusable stage logic lives in `src/nextgen2026_coding_bootcamp/steps/`
- executable wrappers live in `scripts/`

Even if `fetch` and `prepare` already exist, we still teach this boundary explicitly before deepening `analyze`.

## 2. Why This Matters for Researchers

When analysis code is embedded in wrappers or notebooks, methodological changes and operational changes are hard to distinguish. Separating concerns reduces that ambiguity and provides three concrete research benefits:

1. stage logic becomes testable in isolation;
2. wrappers can evolve (CLI, logging, tracking) without changing scientific method code;
3. orchestration can reuse the same stage functions without duplication.

## 3. Build Steps

These steps intentionally move from directory boundaries to function extraction to wrapper minimization. The sequence makes the rationale visible before introducing additional workflow features.

### Step 1: Use a stable repository layout (The "Engine vs. Wrapper" Pattern)

This step defines the physical boundaries that keep method code, execution wrappers, and outputs from mixing. For researchers, clear boundaries reduce accidental coupling that later makes provenance reconstruction difficult. When setting this up, verify each directory has one role and avoid placing analysis logic directly in `scripts/`.

```text
repo/
├── configs/               # YAML configuration for each stage (The "Settings")
│   └── stages/
├── data/                  # Data storage (ignored by git)
│   ├── raw/               # Read-only source files
│   └── intermediate/      # Cleaned/transformed data
├── scripts/               # THIN wrappers for execution (The "Ignition")
│   ├── 00_fetch.py
│   ├── 01_prepare.py
│   └── 02_analyze.py
├── src/nextgen2026_coding_bootcamp/
│   └── steps/             # REUSABLE method logic (The "Engine")
│       ├── fetch.py
│       ├── prepare.py
│       └── analyze.py
├── notebooks/             # Exploratory analysis and visualization
├── results/               # Final reports and plots
└── tests/                 # Quality gates for method logic
```

### Step 2: Keep `analyze` method logic in `src/`

This step isolates analytical transformations so they can be reused by wrappers, tests, and orchestration without copy-paste drift. The reproducibility benefit is that one method implementation is audited in one place. If results differ across runs, this separation makes it easier to rule out wrapper-side causes first.


Chapter snapshot (`src/nextgen2026_coding_bootcamp/steps/analyze.py`):

```python
from pathlib import Path

import pandas as pd


def build_hourly_profile(input_csv: Path, output_csv: Path) -> dict:
    df = pd.read_csv(input_csv)
    profile = (
        df.groupby(["hour", "day_type"], as_index=False)["total_rentals"]
        .mean()
        .rename(columns={"total_rentals": "mean_rentals"})
    )
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    profile.to_csv(output_csv, index=False)
    return {
        "rows_in": int(len(df)),
        "rows_out": int(len(profile)),
        "output_csv": str(output_csv),
    }
```

### Step 3: Keep `scripts/02_analyze.py` as a thin wrapper

This step keeps the execution entry point explicit while preventing method duplication in CLI code. Practically, wrappers should only handle input wiring and process control, not scientific transformations. If the wrapper grows large, treat that as a signal that logic is leaking out of the stage layer.


```python
from pathlib import Path

from nextgen2026_coding_bootcamp.steps.analyze import build_hourly_profile


def main() -> int:
    input_csv = Path("data/intermediate/hourly_bike_data.csv")
    output_csv = Path("results/hourly_profile.csv")
    build_hourly_profile(input_csv=input_csv, output_csv=output_csv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## 4. Run Checkpoint

Use this checkpoint to confirm that structural boundaries still support an end-to-end stage invocation. A passing run indicates the new layout did not break the execution surface.

```bash
uv run python scripts/00_fetch.py --config configs/stages/fetch.yaml
uv run python scripts/01_prepare.py --config configs/stages/prepare.yaml
uv run python scripts/02_analyze.py
```

## 5. Transition

Next chapter: [Configuration](./02-config.md). With structure stabilized, you can now externalize run choices without mixing them back into method code.
