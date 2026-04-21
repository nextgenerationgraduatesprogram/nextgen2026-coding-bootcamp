from pathlib import Path

from nextgen2026_coding_bootcamp.cli import build_stage_parser
from nextgen2026_coding_bootcamp.config import compose_config
from nextgen2026_coding_bootcamp.steps.analyze import run_analyze


def main() -> int:
    """Thin wrapper to run the analyze stage using shared CLI contract."""
    parser = build_stage_parser("Run the analyze stage.")
    args = parser.parse_args()

    config_root = Path("configs")
    # Determine the relative path of the stage config for the composer
    try:
        stage_part = str(args.config.relative_to(config_root))
    except ValueError:
        # Fallback if config is absolute or outside root
        stage_part = str(args.config)

    parts = ["run.yaml", "paths.yaml", stage_part, "profiles/base.yaml"]

    cfg = compose_config(config_root=config_root, parts=parts, overrides=args.set)

    print(f"Running analyze stage with overrides: {args.set}")
    run_analyze(cfg=cfg)
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
