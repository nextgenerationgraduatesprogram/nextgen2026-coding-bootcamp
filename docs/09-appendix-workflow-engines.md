# Appendix: Workflow Engines

This appendix introduces workflow engines as operational control around an already stable workflow contract. It focuses on retries, state visibility, and scheduling without changing stage-level analytical behavior.

That distinction is critical for scientific consistency at scale: operational tooling should improve reliability and throughput, but method logic and provenance semantics must remain unchanged across execution surfaces.

## 1. What This Chapter Adds

This section defines the minimum components required to engine-enable execution safely:

1. one reusable engine entry function (`run_once`);
2. one engine task/flow wrapper that adds retries and execution-state visibility;
3. one execution contract for engine-managed runs that preserves local run artifacts.

## 2. Why This Matters for Researchers

As run volume grows, manual loops become fragile and hard to monitor. Engines provide retries, visibility, and scheduling controls, but must remain operational wrappers around unchanged scientific code paths.

This chapter focuses on orchestration mechanics only. Sweep design and cross-run comparison protocol are handled in Appendix `10`.

## 3. Build Steps

Build from reusable execution adapter to engine task wrapper so boundaries remain explicit. This avoids coupling scheduler details to stage-method implementations.

### Step 1: Add a reusable engine entry point

This step defines one callable execution unit so engines and local scripts share identical run behavior. Keep this function thin and aligned with the canonical run contract.

`src/nextgen2026_coding_bootcamp/engine_runner.py`

```python
from __future__ import annotations

from pathlib import Path
import subprocess

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


def _git_commit() -> str | None:
    result = subprocess.run(["git", "rev-parse", "HEAD"], check=False, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    commit = result.stdout.strip()
    return commit or None


def run_once(
    *,
    profile: str = "base",
    overrides: list[str] | None = None,
    extra_parts: list[str] | None = None,
    run_name: str | None = None,
    log_level: str = "INFO",
    config_root: Path = Path("configs"),
) -> Path:
    parts = [*DEFAULT_PARTS, f"profiles/{profile}.yaml", *(extra_parts or [])]
    cfg = compose_config(config_root=config_root, parts=parts, overrides=overrides)

    ctx = create_run_context(Path(cfg.run.output_root), run_name=run_name)
    configure_logging(ctx.run_dir / "run.log", level=log_level)
    OmegaConf.save(config=cfg, f=ctx.run_dir / "config.yaml")

    run_workflow(cfg=cfg, ctx=ctx)
    write_manifest(ctx=ctx, git_commit=_git_commit())
    return ctx.run_dir
```

### Step 2: Add a minimal engine wrapper for batched execution

This step demonstrates engine control semantics (retry behavior, asynchronous task state) without prescribing any specific sweep design.

Install dependency:

```bash
uv add prefect
```

`scripts/prefect_engine_runs.py`

```python
from prefect import flow, task

from nextgen2026_coding_bootcamp.engine_runner import run_once


@task(retries=2)
def execute_run(variant: dict) -> str:
    run_dir = run_once(
        profile=variant.get("profile", "base"),
        overrides=variant.get("overrides", []),
        run_name=variant["run_name"],
    )
    return str(run_dir)


@flow(log_prints=True)
def run_variants(variants: list[dict]) -> list[str]:
    futures = [execute_run.submit(v) for v in variants]
    return [f.result() for f in futures]


if __name__ == "__main__":
    sample_variants = [
        {"run_name": "engine-demo-a", "overrides": ["analysis.high_demand_quantile=0.85"]},
        {"run_name": "engine-demo-b", "overrides": ["analysis.high_demand_quantile=0.90"]},
    ]
    print(run_variants(sample_variants))
```

## 4. Run Checkpoint

Use this checkpoint to verify that engine-managed runs still emit the same local provenance structure as manual runs. Passing confirms operational scaling without contract drift.

```bash
uv run python scripts/prefect_engine_runs.py
ls -1 runs | tail -n 10
```

You should see one run directory per submitted variant with unchanged local provenance (`config.yaml`, `run.log`, `manifest.json`).

## 5. Engine Controls and Boundaries

Treat these boundaries as non-negotiable controls that prevent operational tooling from altering analytical semantics:

1. Engine layer controls execution state, retries, and concurrency.
2. Workflow functions define scientific behavior.
3. Run evidence remains local and run-scoped, regardless of engine choice.

## 6. Transition

Next appendix: [Multiruns](./10-appendix-multiruns.md). After execution control is stable, the next dependency is rigorous sweep protocol and comparison completeness.
