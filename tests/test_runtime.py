from __future__ import annotations

import logging
from pathlib import Path
import re

from nextgen2026_coding_bootcamp.runtime import (
    RunContext,
    configure_logging,
    create_run_context,
    make_run_id,
)


def test_make_run_id_includes_sanitized_run_name():
    run_id = make_run_id(run_name="My Digits Run")

    assert "My-Digits-Run" in run_id
    assert re.match(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_My-Digits-Run_[0-9a-f]{6}$", run_id)


def test_create_run_context_creates_run_directory(tmp_path: Path):
    ctx = create_run_context(output_root=tmp_path, run_name="unit")

    assert isinstance(ctx, RunContext)
    assert ctx.run_dir.exists()
    assert ctx.run_dir.parent == tmp_path
    assert ctx.artifacts == {}


def test_configure_logging_creates_log_file_and_writes_messages(tmp_path: Path):
    log_path = tmp_path / "logs" / "workflow.log"
    configure_logging(log_path=log_path, level="INFO")

    logger = logging.getLogger("nextgen2026_coding_bootcamp.tests.runtime")
    logger.info("runtime-log-check")
    logging.shutdown()

    assert log_path.exists()
    assert "runtime-log-check" in log_path.read_text()
