import argparse
from pathlib import Path

from omegaconf import OmegaConf

from nextgen2026_coding_bootcamp.steps.fetch import run_fetch


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the fetch stage.")
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to fetch stage config file.",
    )
    args = parser.parse_args()

    cfg = OmegaConf.load(args.config)
    run_fetch(cfg=cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
