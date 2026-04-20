# Traceable Runs

This chapter turns each analyze execution into a run-scoped record with its own identity and artifact space. Instead of writing into shared paths, runs become distinct evidence units that preserve provenance over time.

The practical outcome is safer comparison and auditability: configuration snapshots, logs, and outputs stay linked to one run ID. That linkage reduces overwrite risk and makes retrospective interpretation substantially more reliable.

## 1. What This Chapter Adds

This section defines the traceability contract for analyze executions:

1. unique `run_id` and run directory;
2. run-scoped logs and config snapshot;
3. run manifest linking artifacts and metadata.

## 2. Why This Matters for Researchers

Without run identity, result comparison is vulnerable to overwrite and attribution errors. Run-scoped storage makes each execution independently auditable and review-ready.

## 3. Build Steps

Implement these steps from identity primitives to wrapper integration so traceability is introduced systematically. The ordering ensures manifest and logging outputs attach to the correct run context.

### Step 1: Add run context utilities

This step introduces a run identity object that anchors all later provenance files. It turns each execution into an addressable record rather than a transient process. Ensure run IDs are unique and directories are created atomically to avoid collisions.


Update `src/nextgen2026_coding_bootcamp/runtime.py`:

```python
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import logging
import uuid


def configure_logging(log_path: Path, level: str = "INFO") -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.FileHandler(log_path), logging.StreamHandler()],
        force=True,
    )


def make_run_id(run_name: str | None = None) -> str:
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    suffix = uuid.uuid4().hex[:6]
    if run_name:
        return f"{stamp}_{run_name.replace(' ', '-')}_{suffix}"
    return f"{stamp}_{suffix}"


@dataclass
class RunContext:
    run_id: str
    run_dir: Path
    artifacts: dict = field(default_factory=dict)


def create_run_context(output_root: Path, run_name: str | None = None) -> RunContext:
    run_id = make_run_id(run_name=run_name)
    run_dir = output_root / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    return RunContext(run_id=run_id, run_dir=run_dir)
```

### Step 2: Make analyze output location run-aware

This step routes stage outputs into run-scoped paths so runs no longer overwrite one another. For comparative research, that preserves evidence needed for retrospective review. If output files still land in shared folders during traceable mode, treat that as a contract break.


Chapter snapshot (`src/nextgen2026_coding_bootcamp/steps/analyze.py`):

```python
def run_analyze(cfg, ctx=None) -> dict:
    prepared_csv = Path(cfg.paths.intermediate_dir) / "hourly_bike_data.csv"
    if ctx is None:
        output_dir = Path(cfg.paths.results_dir)
    else:
        output_dir = ctx.run_dir / "analyze"
    output_dir.mkdir(parents=True, exist_ok=True)

    ...
```

### Step 3: Write a compact run manifest

This step creates a lightweight index that links run identity to produced artifacts. It improves navigation and automation without replacing underlying files. Keep manifest fields stable across runs so downstream comparison tooling stays simple.


`src/nextgen2026_coding_bootcamp/manifests.py`

```python
import json
from pathlib import Path


def write_manifest(ctx, git_commit: str | None = None) -> Path:
    manifest_path = ctx.run_dir / "manifest.json"
    payload = {
        "run_id": ctx.run_id,
        "git_commit": git_commit,
        "artifacts": ctx.artifacts,
    }
    manifest_path.write_text(json.dumps(payload, indent=2) + "\n")
    return manifest_path
```

### Step 4: Update analyze wrapper for run-scoped execution

This step combines config snapshotting, logging, stage execution, and manifest writing into one repeatable sequence. The operational goal is a complete run record from a single command. If any one of config, log, stage artifacts, or manifest is missing, consider the run incomplete.


Chapter snapshot (`scripts/02_analyze.py`):

```python
from pathlib import Path

from omegaconf import OmegaConf

from nextgen2026_coding_bootcamp.cli import build_stage_parser
from nextgen2026_coding_bootcamp.config import compose_config
from nextgen2026_coding_bootcamp.manifests import write_manifest
from nextgen2026_coding_bootcamp.runtime import create_run_context, configure_logging
from nextgen2026_coding_bootcamp.steps.analyze import run_analyze


def main() -> int:
    parser = build_stage_parser("Run the analyze stage.")
    parser.add_argument("--run-name", type=str, default=None, help="Optional run label")
    args = parser.parse_args()

    config_root = Path("configs")
    stage_part = str(args.config.relative_to(config_root))
    parts = ["run.yaml", "paths.yaml", stage_part, "profiles/base.yaml"]
    cfg = compose_config(config_root=config_root, parts=parts, overrides=args.set)

    ctx = create_run_context(Path(cfg.run.output_root), run_name=args.run_name)
    configure_logging(ctx.run_dir / "run.log", level=args.log_level)
    OmegaConf.save(config=cfg, f=ctx.run_dir / "config.yaml")

    ctx.artifacts["analyze"] = run_analyze(cfg=cfg, ctx=ctx)
    write_manifest(ctx=ctx)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## 4. Run Checkpoint

Use this checkpoint to verify that repeated analyze runs create distinct run directories with complete provenance payloads. Passing means comparison can proceed without overwrite ambiguity.

```bash
uv run python scripts/02_analyze.py --config configs/stages/analyze.yaml --run-name baseline
uv run python scripts/02_analyze.py --config configs/stages/analyze.yaml --run-name q85 --set analysis.high_demand_quantile=0.85
ls -1 runs | tail -n 5
```

## 5. Transition

Next chapter: [Workflow Orchestration](./06-orchestration.md). With run-scoped analyze proven, you can extend the same contract to full pipeline execution.
