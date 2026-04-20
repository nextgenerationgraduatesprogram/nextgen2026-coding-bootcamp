# Command-Line Interface

This chapter defines a stable command-line contract for stage execution. A reproducible config model is only useful if variant intent is expressed through a consistent invocation surface that can be inspected and repeated.

By standardizing wrapper arguments, command history becomes meaningful evidence instead of partial context. The result is lower operator variance across collaborators and a cleaner integration point for logging and traceability controls added later.

## 1. What This Chapter Adds

This section defines the shared CLI contract that should remain stable across stage wrappers:

- `--config` for stage config path
- `--set` for explicit overrides
- `--log-level` reserved for observability wiring

## 2. Why This Matters for Researchers

If variant runs require editing script bodies, command history no longer captures methodological intent. A stable CLI makes each run request explicit and therefore easier to compare and reproduce.

## 3. Build Steps

Apply these steps from parser definition to wrapper adoption so interface consistency is achieved deliberately, not by convention. This prevents argument drift as new stages are added.

### Step 1: Create a shared stage parser

This step defines one stable CLI contract so stage wrappers do not drift over time. For reproducibility, a uniform command surface makes run intent easier to audit across team members. Keep arguments minimal and explicit so each flag has a clear provenance meaning.


`src/nextgen2026_coding_bootcamp/cli.py`

```python
import argparse
from pathlib import Path


def build_stage_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to stage YAML file",
    )
    parser.add_argument(
        "--set",
        nargs="*",
        default=[],
        metavar="KEY=VALUE",
        help="OmegaConf dotlist overrides",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        help="Reserved for logging setup in Chapter 04",
    )
    return parser
```

### Step 2: Update analyze wrapper to use the shared parser

This step applies the shared contract to the highest-focus stage in this sequence. The practical effect is fewer wrapper-specific argument quirks and more predictable invocation patterns. If confusion appears during teaching, point students to one parser source of truth.


Chapter snapshot (`scripts/02_analyze.py`):

```python
from pathlib import Path

from nextgen2026_coding_bootcamp.cli import build_stage_parser
from nextgen2026_coding_bootcamp.config import compose_config
from nextgen2026_coding_bootcamp.steps.analyze import run_analyze


def main() -> int:
    parser = build_stage_parser("Run the analyze stage.")
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

### Step 3: Apply the same contract to other wrappers

This step extends interface consistency across the full stage set. Methodologically, consistency reduces operator error when switching between stages. A good check is that help output feels structurally identical across wrappers except for stage-specific descriptions.


Use the same parser pattern for `00_fetch.py`, `01_prepare.py`, and `03_report.py`.

Wrapper responsibilities stay narrow:

1. parse args;
2. compose/load config;
3. call one stage function;
4. return status.

## 4. Run Checkpoint

Use this checkpoint to verify interface behavior, not just stage success: help output should be clear, defaults should resolve, and overrides should apply deterministically.

```bash
uv run python scripts/02_analyze.py --help
uv run python scripts/02_analyze.py --config configs/stages/analyze.yaml
uv run python scripts/02_analyze.py --config configs/stages/analyze.yaml --set analysis.high_demand_quantile=0.92
```

## 5. Transition

Next chapter: [Logging and Observability](./04-observability.md). With invocation standardized, you can now capture process evidence consistently across runs.
