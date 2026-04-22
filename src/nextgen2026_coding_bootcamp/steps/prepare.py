from __future__ import annotations

from pathlib import Path
import logging
import shutil

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


RAW_REQUIRED_COLUMNS = ["dteday", "hr", "cnt", "season", "weathersit"]
PREPARED_COLUMNS = ["timestamp", "demand", "hour", "day_type", "season", "weather"]


def _resolve_input_csv(cfg, ctx=None, input_csv: Path | None = None) -> Path:
    if input_csv is not None:
        return input_csv

    if ctx is not None:
        fetch_artifact = ctx.artifacts.get("fetch", {})
        fetch_csv = fetch_artifact.get("raw_csv")
        if fetch_csv:
            return Path(fetch_csv)

    return Path(cfg.paths.raw_dir) / str(cfg.fetch.raw_artifact_name)


def _copy_to_run(shared_path: Path, run_path: Path) -> None:
    run_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(shared_path, run_path)


def _validate_raw_columns(raw_table: pd.DataFrame) -> None:
    missing_columns = [column for column in RAW_REQUIRED_COLUMNS if column not in raw_table.columns]
    if missing_columns:
        raise ValueError(
            "Raw bike-demand table is missing required columns: "
            + ", ".join(missing_columns)
        )


def run_prepare(cfg, ctx=None, input_csv: Path | None = None) -> dict:
    raw_csv = _resolve_input_csv(cfg=cfg, ctx=ctx, input_csv=input_csv)

    shared_output_dir = Path(cfg.paths.intermediate_dir)
    shared_output_dir.mkdir(parents=True, exist_ok=True)

    prepared_table_name = str(cfg.prepare.prepared_table_name)
    shared_prepared_csv = shared_output_dir / prepared_table_name

    logger.info("[prepare]")
    logger.info("prepare:start input=%s", raw_csv)

    raw_table = pd.read_csv(raw_csv)
    _validate_raw_columns(raw_table)

    timestamp = pd.to_datetime(raw_table["dteday"]) + pd.to_timedelta(
        raw_table["hr"].astype(int),
        unit="h",
    )

    prepared = pd.DataFrame(
        {
            "timestamp": timestamp,
            "demand": raw_table["cnt"].astype(int),
            "hour": timestamp.dt.hour.astype(int),
            "day_type": np.where(timestamp.dt.dayofweek < 5, "weekday", "weekend"),
            "season": raw_table["season"].astype(str),
            "weather": raw_table["weathersit"].astype(str),
        }
    )
    prepared = prepared.sort_values("timestamp", ignore_index=True)
    prepared["timestamp"] = prepared["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S")
    prepared.to_csv(shared_prepared_csv, index=False)

    if ctx is None:
        output_prepared_csv = shared_prepared_csv
        copied_to_run = False
    else:
        run_stage_dir = ctx.run_dir / "prepare"
        run_stage_dir.mkdir(parents=True, exist_ok=True)
        output_prepared_csv = run_stage_dir / prepared_table_name
        _copy_to_run(shared_prepared_csv, output_prepared_csv)
        copied_to_run = True

    logger.info(
        "prepare:finish rows=%d columns=%s output_prepared=%s\n",
        len(prepared),
        PREPARED_COLUMNS,
        output_prepared_csv,
    )

    return {
        "raw_csv": str(raw_csv),
        "prepared_csv": str(output_prepared_csv),
        "shared_prepared_csv": str(shared_prepared_csv),
        "n_rows": int(len(prepared)),
        "columns": PREPARED_COLUMNS,
        "day_types": sorted(prepared["day_type"].unique().tolist()),
        "copied_to_run": copied_to_run,
    }
