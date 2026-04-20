from pathlib import Path

from omegaconf import OmegaConf

from nextgen2026_coding_bootcamp.cli import build_stage_parser
from nextgen2026_coding_bootcamp.config import compose_config, load_config
from nextgen2026_coding_bootcamp.manifests import write_manifest
from nextgen2026_coding_bootcamp.runtime import create_run_context, configure_logging
from nextgen2026_coding_bootcamp.steps.analyze import run_analyze


def _load_analyze_config(config_path: Path, overrides: list[str]):
    config_root = Path("configs")
    try:
        relative_config = config_path.relative_to(config_root)
    except ValueError:
        relative_config = None

    # Hierarchical config mode: compose shared defaults with stage config.
    if relative_config is not None and relative_config.parts and relative_config.parts[0] == "stages":
        parts = [
            "run.yaml",
            "paths.yaml",
            str(relative_config),
            "profiles/base.yaml",
        ]
        return compose_config(config_root=config_root, parts=parts, overrides=overrides)

    # Single-file mode fallback for ad hoc/local configs.
    return load_config(config_path, overrides=overrides)


def main() -> int:
    parser = build_stage_parser("Run the analyze stage.")
    parser.add_argument("--run-name", type=str, default=None, help="Optional run label")
    args = parser.parse_args()

    cfg = _load_analyze_config(args.config, overrides=args.set)
    if args.run_name is None:
        # Supports the earlier chapter contract where analyze runs without
        # per-run traceability, writing products under results/.
        configure_logging(Path(cfg.paths.results_dir) / "workflow.log", level=args.log_level)
        run_analyze(cfg=cfg)
    else:
        ctx = create_run_context(Path(cfg.run.output_root), run_name=args.run_name)
        configure_logging(ctx.run_dir / "run.log", level=args.log_level)
        OmegaConf.save(config=cfg, f=ctx.run_dir / "config.yaml")
        ctx.artifacts["analyze"] = run_analyze(cfg=cfg, ctx=ctx)
        write_manifest(ctx=ctx)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
