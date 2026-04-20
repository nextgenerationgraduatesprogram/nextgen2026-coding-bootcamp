# Appendix: Hydra

This appendix introduces Hydra as a composition and multirun interface layered over the existing workflow contract. Its role is to standardize override ergonomics and reduce manual configuration drift.

Adoption is useful when experiment matrices expand and custom composition code becomes hard to maintain. The key requirement is equivalence: Hydra-driven runs should preserve the same execution and provenance guarantees as manual runs.

## 1. What This Chapter Adds

This section defines the Hydra integration outcomes required for contract-preserving adoption:

1. Hydra-based config composition;
2. Hydra override and multirun commands;
3. preservation of existing run context and manifest behavior.

## 2. Why This Matters for Researchers

As configuration trees grow, custom composition code can drift between entrypoints. Hydra standardizes override and multirun semantics while keeping stage-level analytical behavior unchanged.

## 3. Build Steps

Implement Hydra adoption from dependency and config declaration to entry script wiring. This preserves equivalence checks at each stage of the migration.

### Step 1: Install dependency

This step introduces Hydra as configuration tooling, not as a replacement for stage method code. From a workflow perspective, dependency addition should serve consistency and multirun ergonomics. Confirm environment resolution is stable before changing execution entrypoints.


```bash
uv add hydra-core
```

### Step 2: Add Hydra composition file

This step encodes default config composition in one declarative location. It makes override behavior more explicit and reduces custom composition plumbing. Keep `chdir` behavior intentional so run artifact paths remain predictable.


`configs/hydra_workflow.yaml`

```yaml
defaults:
  - run
  - paths
  - stages/fetch
  - stages/prepare
  - stages/analyze
  - stages/report
  - profiles/base
  - _self_

run_name: hydra
log_level: INFO

hydra:
  job:
    chdir: false
```

### Step 3: Add Hydra workflow entry script

This step maps Hydra-composed config into the same run-context and manifest lifecycle used elsewhere. The methodological requirement is equivalence: Hydra runs should satisfy the same provenance contract as manual runs. Validate that output structure and metadata remain consistent.


`scripts/hydra_workflow.py`

```python
from __future__ import annotations

from pathlib import Path

import hydra
from omegaconf import DictConfig, OmegaConf

from nextgen2026_coding_bootcamp.manifests import write_manifest
from nextgen2026_coding_bootcamp.runtime import create_run_context, configure_logging
from nextgen2026_coding_bootcamp.workflow import run_workflow


@hydra.main(version_base=None, config_path="../configs", config_name="hydra_workflow")
def main(cfg: DictConfig) -> None:
    ctx = create_run_context(Path(cfg.run.output_root), run_name=str(cfg.run_name))
    configure_logging(ctx.run_dir / "run.log", level=str(cfg.log_level))
    OmegaConf.save(config=cfg, f=ctx.run_dir / "config.yaml")

    run_workflow(cfg=cfg, ctx=ctx)
    write_manifest(ctx=ctx)


if __name__ == "__main__":
    main()
```

## 4. Run Checkpoint

Use this checkpoint to verify semantic equivalence: Hydra-driven runs should produce the same run record structure and interpretive outcomes as manual composition runs.

```bash
uv run python scripts/hydra_workflow.py
uv run python scripts/hydra_workflow.py analysis.high_demand_quantile=0.85 run_name=hydra-q85
uv run python scripts/hydra_workflow.py --multirun analysis.high_demand_quantile=0.85,0.90,0.95 run_name=hydra-sweep
```

## 5. Transition

Next appendix: [Automated Testing on Git Push](./12-appendix-git-push-testing.md). After execution ergonomics are expanded, enforce branch-level quality gates to protect shared baselines.
