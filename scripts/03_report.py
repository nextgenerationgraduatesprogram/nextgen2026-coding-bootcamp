from pathlib import Path

from nextgen2026_coding_bootcamp.cli import build_stage_parser
from nextgen2026_coding_bootcamp.config import compose_config
from nextgen2026_coding_bootcamp.runtime import configure_logging
from nextgen2026_coding_bootcamp.steps.report import run_report


def main() -> int:
    """Thin wrapper to run the report stage using shared CLI contract."""
    parser = build_stage_parser("Run the report stage.")
    args = parser.parse_args()

    config_root = Path("configs")
    try:
        stage_part = str(args.config.relative_to(config_root))
    except ValueError:
        stage_part = str(args.config)

    parts = ["run.yaml", "paths.yaml", stage_part, "profiles/base.yaml"]

    cfg = compose_config(config_root=config_root, parts=parts, overrides=args.set)

    # Configure durable logging
    log_path = Path(cfg.paths.results_dir) / "workflow.log"
    configure_logging(log_path, level=args.log_level)

    run_report(cfg=cfg)
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
