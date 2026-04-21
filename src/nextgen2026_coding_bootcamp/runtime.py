from pathlib import Path
import logging


def configure_logging(log_path: Path, level: str = "INFO") -> None:
    """Standardize logging across all stages and wrappers."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.FileHandler(log_path), logging.StreamHandler()],
        force=True,
    )
