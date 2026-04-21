from pathlib import Path

from omegaconf import OmegaConf

from nextgen2026_coding_bootcamp.cli import build_stage_parser
from nextgen2026_coding_bootcamp.config import compose_config
from nextgen2026_coding_bootcamp.manifests import write_manifest
from nextgen2026_coding_bootcamp.runtime import create_run_context, configure_logging
from nextgen2026_coding_bootcamp.steps.analyze import run_analyze


def main() -> int:
    """Thin wrapper to run the analyze stage using shared CLI contract."""
    parser = build_stage_parser("Run the analyze stage.")
    parser.add_argument("--run-name", type=str, default=None, help="Optional run label")
    args = parser.parse_args()

    config_root = Path("configs")
    try:
        stage_part = str(args.config.relative_to(config_root))
    except ValueError:
        stage_part = str(args.config)

    parts = ["run.yaml", "paths.yaml", stage_part, "profiles/base.yaml"]

    cfg = compose_config(config_root=config_root, parts=parts, overrides=args.set)

    # Initialize run context and logging
    ctx = create_run_context(Path(cfg.run.output_root), run_name=args.run_name)
    configure_logging(ctx.run_dir / "run.log", level=args.log_level)

    # Save a snapshot of the composed config
    OmegaConf.save(config=cfg, f=ctx.run_dir / "config.yaml")

    print(f"Starting traceable run: {ctx.run_id}")
    ctx.artifacts["analyze"] = run_analyze(cfg=cfg, ctx=ctx)

    # Write manifest
    write_manifest(ctx=ctx)

    print(f"Run complete. Results in: {ctx.run_dir}")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
