from pathlib import Path

from omegaconf import OmegaConf

from nextgen2026_coding_bootcamp.cli import build_stage_parser
from nextgen2026_coding_bootcamp.config import load_config
from nextgen2026_coding_bootcamp.manifests import write_manifest
from nextgen2026_coding_bootcamp.runtime import create_run_context, configure_logging
from nextgen2026_coding_bootcamp.steps.fetch import run_fetch


def main() -> int:
    parser = build_stage_parser("Run the fetch stage.")
    parser.add_argument("--run-name", type=str, default=None, help="Optional run label")
    parser.add_argument(
        "--force-download",
        action="store_true",
        help="Re-download the raw dataset even if a cached copy already exists.",
    )
    args = parser.parse_args()

    overrides = list(args.set)
    if args.force_download:
        overrides.append("fetch.force_download=true")

    cfg = load_config(args.config, overrides=overrides)
    ctx = create_run_context(Path(cfg.run.output_root), run_name=args.run_name)

    configure_logging(ctx.run_dir / "run.log", level=args.log_level)
    OmegaConf.save(config=cfg, f=ctx.run_dir / "config.yaml")

    ctx.artifacts["fetch"] = run_fetch(cfg=cfg, ctx=ctx)
    write_manifest(ctx=ctx)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
