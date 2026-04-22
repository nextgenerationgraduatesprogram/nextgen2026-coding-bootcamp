import argparse
from pathlib import Path

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


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the full workflow.")
    parser.add_argument("--profile", type=str, default="base")
    parser.add_argument("--part", action="append", default=[])
    parser.add_argument("--set", nargs="*", default=[], metavar="KEY=VALUE")
    parser.add_argument("--log-level", type=str, default="INFO")
    parser.add_argument("--run-name", type=str, default=None)
    args = parser.parse_args()

    parts = [*DEFAULT_PARTS, f"profiles/{args.profile}.yaml", *args.part]
    cfg = compose_config(Path("configs"), parts=parts, overrides=args.set)

    ctx = create_run_context(Path(cfg.run.output_root), run_name=args.run_name)
    configure_logging(ctx.run_dir / "run.log", level=args.log_level)
    OmegaConf.save(config=cfg, f=ctx.run_dir / "config.yaml")

    run_workflow(cfg=cfg, ctx=ctx)
    write_manifest(ctx=ctx)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
