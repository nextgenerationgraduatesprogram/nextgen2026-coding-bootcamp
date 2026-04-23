from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import logging
import uuid


def configure_logging(log_path: Path, level: str = "INFO") -> None:
    """Standardize logging across all stages and wrappers."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.FileHandler(log_path), logging.StreamHandler()],
        force=True,
    )


def make_run_id(run_name: str | None = None) -> str:
    """Generate a unique ID for a run."""
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    suffix = uuid.uuid4().hex[:6]
    if run_name:
        return f"{stamp}_{run_name.replace(' ', '-')}_{suffix}"
    return f"{stamp}_{suffix}"


@dataclass
class RunContext:
    """Context object for a single workflow run."""

    run_id: str
    run_dir: Path
    artifacts: dict = field(default_factory=dict)


def create_run_context(output_root: Path, run_name: str | None = None) -> RunContext:
    """Create a unique directory for a run and return the context."""
    run_id = make_run_id(run_name=run_name)
    run_dir = output_root / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    return RunContext(run_id=run_id, run_dir=run_dir)
