from __future__ import annotations

from pathlib import Path
import logging
import shutil

import pandas as pd

logger = logging.getLogger(__name__)


def _copy_to_run(shared_path: Path, run_path: Path) -> None:
    run_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(shared_path, run_path)


def run_fetch(cfg, ctx=None) -> dict:
    dataset_name = str(cfg.fetch.dataset_name)
    raw_artifact_name = str(cfg.fetch.raw_artifact_name)
    source_data_path = Path(cfg.fetch.source_data_path)

    if not source_data_path.exists():
        raise FileNotFoundError(
            f"Configured fetch.source_data_path does not exist: {source_data_path}"
        )

    raw_dir = Path(cfg.paths.raw_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    shared_raw_csv = raw_dir / raw_artifact_name

    logger.info("[fetch]")
    logger.info(
        "fetch:start dataset=%s source=%s shared_output=%s",
        dataset_name,
        source_data_path,
        shared_raw_csv,
    )

    shutil.copy2(source_data_path, shared_raw_csv)
    raw_table = pd.read_csv(shared_raw_csv)

    if ctx is None:
        output_raw_csv = shared_raw_csv
        copied_to_run = False
    else:
        run_stage_dir = ctx.run_dir / "fetch"
        run_stage_dir.mkdir(parents=True, exist_ok=True)
        output_raw_csv = run_stage_dir / raw_artifact_name
        _copy_to_run(shared_raw_csv, output_raw_csv)
        copied_to_run = True

    logger.info(
        "fetch:finish rows=%d columns=%s output=%s\n",
        len(raw_table),
        raw_table.columns.tolist(),
        output_raw_csv,
    )

    return {
        "dataset_name": dataset_name,
        "source_csv": str(source_data_path),
        "raw_csv": str(output_raw_csv),
        "shared_raw_csv": str(shared_raw_csv),
        "n_rows": int(len(raw_table)),
        "columns": raw_table.columns.tolist(),
        "copied_to_run": copied_to_run,
    }
