import argparse
from pathlib import Path

from omegaconf import OmegaConf

from nextgen2026_coding_bootcamp.steps.prepare import run_prepare


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the prepare stage.")
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to prepare stage config file.",
    )
    args = parser.parse_args()

    cfg = OmegaConf.load(args.config)
    run_prepare(cfg=cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
