# Workflow Orchestration

This chapter introduces one canonical full-workflow execution path that reuses stage functions directly. It replaces manual stage choreography with a single orchestrated command that applies the same run contract end to end.

A canonical path improves reproducibility because stage order, config composition, and provenance capture are applied consistently across operators. It also provides a stable target for test coverage in the next chapter.

## 1. What This Chapter Adds

This section specifies the orchestration components required for a defensible full-run contract:

1. a function-level orchestrator that calls stage functions directly;
2. one official full-run wrapper command;
3. explicit config precedence for full workflow runs.

## 2. Why This Matters for Researchers

Manual stage sequencing introduces omission and ordering risk that can invalidate run comparisons. A canonical orchestration path makes complete-run execution consistent, auditable, and easier to review.

## 3. Build Steps

Proceed from function-level orchestration to CLI wrapper integration to precedence clarification. This order preserves clear ownership between execution logic and invocation surface.

### Step 1: Add the workflow function

This step defines the canonical stage order in reusable function form. For methodological clarity, orchestration should call stage functions directly rather than shelling out to scripts. Keep this order explicit so changes are intentional and reviewable.


`src/nextgen2026_coding_bootcamp/workflow.py`

```python
from nextgen2026_coding_bootcamp.steps.fetch import run_fetch
from nextgen2026_coding_bootcamp.steps.prepare import run_prepare
from nextgen2026_coding_bootcamp.steps.analyze import run_analyze
from nextgen2026_coding_bootcamp.steps.report import run_report


def run_workflow(cfg, ctx):
    ctx.artifacts["fetch"] = run_fetch(cfg=cfg, ctx=ctx)
    ctx.artifacts["prepare"] = run_prepare(cfg=cfg, ctx=ctx)
    ctx.artifacts["analyze"] = run_analyze(cfg=cfg, ctx=ctx)
    ctx.artifacts["report"] = run_report(cfg=cfg, ctx=ctx)
    return ctx
```

### Step 2: Add canonical full-run wrapper

This step creates one official command for full-pipeline execution and provenance capture. It reduces manual stage choreography errors and gives teams a shared execution baseline. Avoid embedding stage-specific logic here; keep this wrapper focused on wiring and run setup.


`scripts/run_workflow.py`

```python
import argparse
from pathlib import Path

from omegaconf import OmegaConf

from nextgen2026_coding_bootcamp.config import compose_config
from nextgen2026_coding_bootcamp.manifests import write_manifest
from nextgen2026_coding_bootcamp.runtime import create_run_context, configure_logging
from nextgen2026_coding_bootcamp.workflow import run_workflow

DEFAULT_PARTS = [
    "run.yaml",
    "paths.yaml",
    "stages/fetch.yaml",
    "stages/prepare.yaml",
    "stages/analyze.yaml",
    "stages/report.yaml",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the full workflow.")
    parser.add_argument("--profile", type=str, default="base")
    parser.add_argument("--part", action="append", default=[])
    parser.add_argument("--set", nargs="*", default=[], metavar="KEY=VALUE")
    parser.add_argument("--log-level", type=str, default="INFO")
    parser.add_argument("--run-name", type=str, default=None)
    args = parser.parse_args()

    parts = [*DEFAULT_PARTS, f"profiles/{args.profile}.yaml", *args.part]
    cfg = compose_config(Path("configs"), parts=parts, overrides=args.set)

    ctx = create_run_context(Path(cfg.run.output_root), run_name=args.run_name)
    configure_logging(ctx.run_dir / "run.log", level=args.log_level)
    OmegaConf.save(config=cfg, f=ctx.run_dir / "config.yaml")

    run_workflow(cfg=cfg, ctx=ctx)
    write_manifest(ctx=ctx)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### Step 3: Keep precedence explicit

This step documents exactly how layered config inputs resolve when multiple sources are present. Explicit precedence is essential for interpreting differences between experimental runs. If run outcomes look surprising, verify resolved precedence before adjusting analytical code.


Later layer wins:

1. `DEFAULT_PARTS`
2. `profiles/<name>.yaml`
3. each `--part`
4. `--set`

## 4. Run Checkpoint

Use this checkpoint to verify that full workflow runs honor configuration precedence and produce run-scoped evidence end to end. Passing confirms that orchestration, not manual sequencing, is now the authoritative path.

```bash
uv run python scripts/run_workflow.py --profile base --run-name baseline
uv run python scripts/run_workflow.py --profile base --run-name q95 --set analysis.high_demand_quantile=0.95
```

## 5. Transition

Next chapter: [Testing the Workflow](./07-testing.md). After defining the canonical execution path, the next dependency is automated verification that protects it from drift.
