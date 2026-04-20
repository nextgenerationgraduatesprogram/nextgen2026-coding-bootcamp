# Appendix: Experiment Tracking

This appendix adds experiment tracking as an index layer over local run records. It captures selected parameters, metrics, and run metadata to make cross-run navigation faster while keeping local artifacts authoritative.

The value appears when run volume grows: comparisons that are slow and error-prone in folders become queryable views with direct links back to concrete provenance files. Tracking extends the core contract; it does not replace it.

## 1. What This Chapter Adds

This section defines the minimal tracking payload that preserves analytical meaning across runs:

1. run identity;
2. selected parameters and metrics;
3. stage artifact metadata;
4. provenance files (`config.yaml`, `run.log`, `manifest.json`).

The local `runs/` directory remains the authoritative evidence store.

## 2. Why This Matters for Researchers

Run folders remain necessary but become cumbersome for large comparisons. Tracking tools provide searchable run metadata while keeping local artifacts as the source of truth.

## 3. Build Steps

Implement tracking in this order: contract first, integration seam second, tracker client wiring third. This keeps metrics naming stable before tooling complexity is introduced.

### Step 1: Define a stable tracking contract

This step decides which parameters, metrics, and tags are consistently logged across runs. Stable naming is what makes cross-run comparison meaningful in tracker UIs. Keep the set small and decision-relevant to avoid noisy, low-value tracking data.


Keep names fixed across runs:

- params: `analysis.high_demand_quantile`, `prepare.keep_holidays`
- metrics: `prepare.rows_out`, `analyze.high_demand_threshold`
- tags: `run_status`, `local_run_dir`

### Step 2: Add stage callback support in workflow

This step adds a clean integration seam so trackers can observe stage completions without changing stage internals. It preserves separation between method execution and telemetry concerns. If tracking logic starts altering stage behavior, move it back behind the callback boundary.


Chapter snapshot (`src/nextgen2026_coding_bootcamp/workflow.py`):

```python
from collections.abc import Callable

from nextgen2026_coding_bootcamp.steps.analyze import run_analyze
from nextgen2026_coding_bootcamp.steps.fetch import run_fetch
from nextgen2026_coding_bootcamp.steps.prepare import run_prepare
from nextgen2026_coding_bootcamp.steps.report import run_report

StageCallback = Callable[[str, dict], None]


def run_workflow(cfg, ctx, on_stage_finish: StageCallback | None = None):
    stage_plan = [
        ("fetch", run_fetch),
        ("prepare", run_prepare),
        ("analyze", run_analyze),
        ("report", run_report),
    ]

    for stage_name, stage_fn in stage_plan:
        artifact = stage_fn(cfg=cfg, ctx=ctx)
        ctx.artifacts[stage_name] = artifact
        if on_stage_finish is not None:
            on_stage_finish(stage_name, artifact)
    return ctx
```

### Step 3: Add inline MLflow integration to workflow wrapper

This step emits run-level metadata and artifacts during the same execution that generates scientific outputs. That timing preserves visibility into partial progress and failures. Ensure tracker records point back to local run directories so provenance remains grounded.


Install dependency:

```bash
uv add mlflow
```

Chapter snapshot (`scripts/run_workflow.py`):

```python
import argparse
from pathlib import Path

import mlflow
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


def _log_selected_params(cfg) -> None:
    mlflow.log_param("analysis.high_demand_quantile", float(cfg.analysis.high_demand_quantile))
    mlflow.log_param("prepare.keep_holidays", bool(cfg.prepare.keep_holidays))


def _log_stage(stage_name: str, artifact: dict) -> None:
    mlflow.log_dict(artifact, f"stage_artifacts/{stage_name}.json")
    if stage_name == "prepare" and artifact.get("rows_out") is not None:
        mlflow.log_metric("prepare.rows_out", float(artifact["rows_out"]))
    if stage_name == "analyze" and artifact.get("high_demand_threshold") is not None:
        mlflow.log_metric("analyze.high_demand_threshold", float(artifact["high_demand_threshold"]))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the full workflow.")
    parser.add_argument("--profile", type=str, default="base")
    parser.add_argument("--part", action="append", default=[])
    parser.add_argument("--set", nargs="*", default=[], metavar="KEY=VALUE")
    parser.add_argument("--log-level", type=str, default="INFO")
    parser.add_argument("--run-name", type=str, default=None)
    parser.add_argument("--tracking-uri", type=str, default="file:./mlruns")
    parser.add_argument("--experiment", type=str, default="nextgen2026-bootcamp")
    args = parser.parse_args()

    parts = [*DEFAULT_PARTS, f"profiles/{args.profile}.yaml", *args.part]
    cfg = compose_config(Path("configs"), parts=parts, overrides=args.set)

    ctx = create_run_context(Path(cfg.run.output_root), run_name=args.run_name)
    configure_logging(ctx.run_dir / "run.log", level=args.log_level)
    OmegaConf.save(config=cfg, f=ctx.run_dir / "config.yaml")

    mlflow.set_tracking_uri(args.tracking_uri)
    mlflow.set_experiment(args.experiment)

    run_status = "success"
    with mlflow.start_run(run_name=ctx.run_id):
        mlflow.set_tag("local_run_dir", str(ctx.run_dir))
        _log_selected_params(cfg)

        try:
            run_workflow(cfg=cfg, ctx=ctx, on_stage_finish=_log_stage)
            write_manifest(ctx=ctx)
        except Exception:
            run_status = "failed"
            raise
        finally:
            manifest_path = ctx.run_dir / "manifest.json"
            mlflow.log_artifact(str(ctx.run_dir / "config.yaml"), artifact_path="run_record")
            if manifest_path.exists():
                mlflow.log_artifact(str(manifest_path), artifact_path="run_record")
            if (ctx.run_dir / "run.log").exists():
                mlflow.log_artifact(str(ctx.run_dir / "run.log"), artifact_path="run_record")
            mlflow.set_tag("run_status", run_status)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## 4. Run Checkpoint

Use this checkpoint to verify that tracker entries, stage artifacts, and local run directories remain cross-referenced. Passing indicates that indexing and provenance are aligned.

```bash
uv run python scripts/run_workflow.py --profile base --run-name tracking-demo
uv run mlflow ui --backend-store-uri mlruns --port 5000
```

## 5. Transition

Next appendix: [Workflow Engines](./09-appendix-workflow-engines.md). With run indexing in place, the next extension is controlled execution scaling without method drift.
