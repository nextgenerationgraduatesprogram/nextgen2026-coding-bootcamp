import argparse
from pathlib import Path


def build_stage_parser(description: str) -> argparse.ArgumentParser:
    """Build a standard parser for workflow stages."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to stage YAML file",
    )
    parser.add_argument(
        "--set",
        nargs="*",
        default=[],
        metavar="KEY=VALUE",
        help="OmegaConf dotlist overrides",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        help="Reserved for logging setup in Chapter 04",
    )
    return parser
