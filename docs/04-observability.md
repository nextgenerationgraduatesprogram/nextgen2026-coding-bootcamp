# Logging and Observability

This chapter adds observability so runtime behavior is captured as durable process evidence, not only inferred from output files. It instruments analyze execution with structured events and routes logs into persistent sinks.

That evidence is essential when interpreting unexpected results, diagnosing failures, or defending execution decisions during review. With consistent logging in place, reruns can be analyzed from recorded process traces instead of terminal memory.

## 1. What This Chapter Adds

This section defines the minimum observability contract for the analyze stage and wrapper layer. The goal is consistent, durable logging rather than ad hoc terminal output.

You will add:

1. stage-level log events in `run_analyze`;
2. one reusable logging setup helper;
3. wrapper wiring for `--log-level`.

## 2. Why This Matters for Researchers

Artifacts capture outcomes; logs capture execution narrative. In research settings, both are needed to explain discrepancies, support troubleshooting, and justify methodological decisions under review.

## 3. Build Steps

Follow these steps from stage instrumentation to centralized logger setup to wrapper wiring. This sequence keeps logging semantics consistent across modules and commands.

### Step 1: Add structured events inside `analyze`

This step instruments analyze with milestone log events so execution flow can be reconstructed after the fact. For research evidence, logs complement artifacts by showing when and where transformations occurred. Prefer structured, low-ambiguity messages that include key paths and counts.


Chapter snapshot (`src/nextgen2026_coding_bootcamp/steps/analyze.py`):

```python
from __future__ import annotations

import json
import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def run_analyze(cfg) -> dict:
    prepared_csv = Path(cfg.paths.intermediate_dir) / "hourly_bike_data.csv"
    output_dir = Path(cfg.paths.results_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("analyze:start input=%s", prepared_csv)
    prepared = pd.read_csv(prepared_csv)

    high_demand_quantile = float(cfg.analysis.high_demand_quantile)
    threshold = float(prepared["total_rentals"].quantile(high_demand_quantile))

    hourly_profile = (
        prepared.groupby(["hour", "day_type"], as_index=False)["total_rentals"]
        .mean()
        .rename(columns={"total_rentals": "mean_rentals"})
    )

    profile_path = output_dir / "hourly_profile.csv"
    summary_path = output_dir / "high_demand_summary.json"

    logger.info("analyze:write profile=%s", profile_path)
    hourly_profile.to_csv(profile_path, index=False)

    logger.info("analyze:write summary=%s", summary_path)
    summary_path.write_text(
        json.dumps(
            {
                "high_demand_quantile": high_demand_quantile,
                "high_demand_threshold": threshold,
                "rows_in": int(len(prepared)),
            },
            indent=2,
        )
        + "\n"
    )

    logger.info("analyze:finish rows_in=%d threshold=%s", len(prepared), threshold)
    return {
        "prepared_csv": str(prepared_csv),
        "hourly_profile_csv": str(profile_path),
        "summary_json": str(summary_path),
    }
```

### Step 2: Centralize logging setup

This step ensures all modules emit logs with the same format and level behavior. Centralization avoids fragmented observability where different wrappers log differently. If logs are missing or duplicated, debug handler setup once in this helper rather than per script.


`src/nextgen2026_coding_bootcamp/runtime.py`

```python
from pathlib import Path
import logging


def configure_logging(log_path: Path, level: str = "INFO") -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.FileHandler(log_path), logging.StreamHandler()],
        force=True,
    )
```

### Step 3: Wire logging from analyze wrapper

This step activates durable logging at execution time using the CLI-selected level. The research benefit is that process evidence is persisted alongside outputs instead of disappearing in terminal history. Treat absence of the log file as a run-quality failure, not a cosmetic issue.


Chapter snapshot (`scripts/02_analyze.py`):

```python
from pathlib import Path

from nextgen2026_coding_bootcamp.cli import build_stage_parser
from nextgen2026_coding_bootcamp.config import compose_config
from nextgen2026_coding_bootcamp.runtime import configure_logging
from nextgen2026_coding_bootcamp.steps.analyze import run_analyze


def main() -> int:
    parser = build_stage_parser("Run the analyze stage.")
    args = parser.parse_args()

    config_root = Path("configs")
    stage_part = str(args.config.relative_to(config_root))
    parts = ["run.yaml", "paths.yaml", stage_part, "profiles/base.yaml"]

    cfg = compose_config(config_root=config_root, parts=parts, overrides=args.set)
    configure_logging(Path(cfg.paths.results_dir) / "workflow.log", level=args.log_level)

    run_analyze(cfg=cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## 4. Run Checkpoint

Use this checkpoint to confirm that process evidence is persisted and interpretable. A successful run should produce both expected artifacts and readable log milestones tied to paths and counts.

```bash
uv run python scripts/02_analyze.py --config configs/stages/analyze.yaml --log-level INFO
tail -n 20 results/workflow.log
```

## 5. Transition

Next chapter: [Traceable Runs](./05-traceability.md). Once logs are durable, the next dependency is isolating each execution into a unique run record.
