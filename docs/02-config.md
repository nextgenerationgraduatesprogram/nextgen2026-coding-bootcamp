# Configuration

This chapter treats configuration as part of method specification. It externalizes analyze-stage choices so run behavior is described through composed config inputs rather than hidden source edits.

The benefit is transparent comparison: defaults, profiles, and overrides become inspectable run metadata that can be replayed. This reduces ambiguity in variant analysis and supports clearer justification of why two runs produced different outcomes.

## 1. What This Chapter Adds

This section defines the composition contract that every analyze invocation should follow:

1. shared run/path config parts;
2. stage-specific analyze config;
3. profile overlays;
4. CLI dotlist overrides as final precedence layer.

## 2. Why This Matters for Researchers

Without explicit config, two numerically different runs can be impossible to explain confidently. Configuration turns method choices into inspectable run inputs that can be reviewed, cited, and replayed.

For `analyze`, this is critical because threshold choices (for example, quantiles) directly affect interpretation.

## 3. Build Steps

Follow these steps from static config definition to executable composition in `scripts/02_analyze.py`. This order keeps precedence semantics clear before command-level overrides are introduced.

### Step 1: Create hierarchical config files

This step introduces a composable config hierarchy so shared defaults and stage-specific choices are separated. For research workflows, this structure makes parameter provenance explicit and easier to compare across variants. Keep file responsibilities narrow so precedence remains predictable.


`configs/run.yaml`

```yaml
run:
  output_root: runs
```

`configs/paths.yaml`

```yaml
paths:
  raw_dir: data/raw
  intermediate_dir: data/intermediate
  results_dir: results
```

`configs/stages/analyze.yaml`

```yaml
analysis:
  high_demand_quantile: 0.90
```

`configs/profiles/base.yaml`

```yaml
profile:
  name: base
```

### Step 2: Add a reusable config loader/composer

This step centralizes config behavior into one implementation used by scripts and orchestration. The methodological gain is that all runs interpret overrides the same way, reducing hidden execution differences. If behavior seems inconsistent, inspect composition order first before changing stage logic.


`src/nextgen2026_coding_bootcamp/config.py`

```python
from pathlib import Path

from omegaconf import DictConfig, OmegaConf


def load_config(config_path: Path, overrides: list[str] | None = None) -> DictConfig:
    cfg = OmegaConf.load(config_path)
    if overrides:
        cfg = OmegaConf.merge(cfg, OmegaConf.from_dotlist(overrides))
    return cfg


def compose_config(
    config_root: Path,
    parts: list[str],
    overrides: list[str] | None = None,
) -> DictConfig:
    cfg = OmegaConf.create()
    for part in parts:
        cfg = OmegaConf.merge(cfg, OmegaConf.load(config_root / part))
    if overrides:
        cfg = OmegaConf.merge(cfg, OmegaConf.from_dotlist(overrides))
    return cfg
```

### Step 3: Make `analyze` use config values, not literals

This step moves analytical choices from source literals to run inputs, which makes method changes auditable. Researchers can then compare runs by configuration rather than by reading code diffs. Validate that every threshold or path affecting interpretation is sourced from `cfg`.


Chapter snapshot (`src/nextgen2026_coding_bootcamp/steps/analyze.py`):

```python
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def run_analyze(cfg) -> dict:
    prepared_csv = Path(cfg.paths.intermediate_dir) / "hourly_bike_data.csv"
    output_dir = Path(cfg.paths.results_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    prepared = pd.read_csv(prepared_csv)
    threshold = float(prepared["total_rentals"].quantile(cfg.analysis.high_demand_quantile))

    hourly_profile = (
        prepared.groupby(["hour", "day_type"], as_index=False)["total_rentals"]
        .mean()
        .rename(columns={"total_rentals": "mean_rentals"})
    )

    profile_path = output_dir / "hourly_profile.csv"
    summary_path = output_dir / "high_demand_summary.json"

    hourly_profile.to_csv(profile_path, index=False)
    summary_path.write_text(
        json.dumps(
            {
                "high_demand_quantile": float(cfg.analysis.high_demand_quantile),
                "high_demand_threshold": threshold,
                "rows_in": int(len(prepared)),
            },
            indent=2,
        )
        + "\n"
    )

    return {
        "prepared_csv": str(prepared_csv),
        "hourly_profile_csv": str(profile_path),
        "summary_json": str(summary_path),
    }
```

### Step 4: Compose config in `scripts/02_analyze.py`

This step connects the hierarchy to the executable command surface for analyze. It ensures that profile overlays and `--set` overrides are part of the run record, not ad hoc edits. If a run behaves unexpectedly, reproduce it by re-running the exact command with the same override list.


```python
import argparse
from pathlib import Path

from nextgen2026_coding_bootcamp.config import compose_config
from nextgen2026_coding_bootcamp.steps.analyze import run_analyze


def main() -> int:
    parser = argparse.ArgumentParser(description="Run analyze stage")
    parser.add_argument("--config", type=Path, default=Path("configs/stages/analyze.yaml"))
    parser.add_argument("--set", nargs="*", default=[], metavar="KEY=VALUE")
    args = parser.parse_args()

    config_root = Path("configs")
    stage_part = str(args.config.relative_to(config_root))
    parts = ["run.yaml", "paths.yaml", stage_part, "profiles/base.yaml"]

    cfg = compose_config(config_root=config_root, parts=parts, overrides=args.set)
    run_analyze(cfg=cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Precedence in this chapter: `run/paths/stage` < `profile` < `--set`.

## 4. Run Checkpoint

Use this checkpoint to verify that composed config drives analyze behavior on real data and that override intent is reflected in outputs. A passing checkpoint confirms both execution and provenance transparency.

```bash
uv run python scripts/00_fetch.py --config configs/stages/fetch.yaml
uv run python scripts/01_prepare.py --config configs/stages/prepare.yaml
uv run python scripts/02_analyze.py --config configs/stages/analyze.yaml
uv run python scripts/02_analyze.py --config configs/stages/analyze.yaml --set analysis.high_demand_quantile=0.85
```

## 5. Transition

Next chapter: [Command-Line Interface](./03-cli.md). Once configuration is explicit, the next dependency is a stable command surface that exposes those choices consistently.
