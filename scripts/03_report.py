from pathlib import Path

from nextgen2026_coding_bootcamp.config import compose_config
from nextgen2026_coding_bootcamp.steps.report import run_report


def main() -> int:
    """Run the report stage using composed configuration."""
    config_root = Path("configs")

    parts = [
        "run.yaml",
        "paths.yaml",
        "stages/report.yaml",
        "profiles/base.yaml",
    ]

    cfg = compose_config(config_root=config_root, parts=parts)

    print(f"Running report stage using composed config")
    run_report(cfg=cfg)
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
