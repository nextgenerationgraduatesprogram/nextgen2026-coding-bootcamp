from pathlib import Path

from nextgen2026_coding_bootcamp.config import compose_config
from nextgen2026_coding_bootcamp.steps.analyze import run_analyze


def main() -> int:
    """Run the analyze stage using composed configuration."""
    config_root = Path("configs")

    # Chapter 02 focuses on this composition list
    parts = ["run.yaml", "paths.yaml", "stages/analyze.yaml", "profiles/base.yaml"]

    cfg = compose_config(config_root=config_root, parts=parts)

    print(f"Running analyze stage with quantile: {cfg.analysis.high_demand_quantile}")
    run_analyze(cfg=cfg)
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
