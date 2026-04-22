from __future__ import annotations

import io
from pathlib import Path
import logging
import shutil
from urllib.parse import urlparse
import urllib.request
import zipfile

import pandas as pd

logger = logging.getLogger(__name__)

RAW_REQUIRED_COLUMNS = ["dteday", "hr", "cnt", "season", "weathersit"]
UCI_HOURLY_MEMBER_NAME = "hour.csv"
WORKSHOP_ROW_COUNT = 96
WORKSHOP_START = "2024-04-04"
SEASON_LABELS = {1: "spring", 2: "summer", 3: "fall", 4: "winter"}
WEATHER_LABELS = {1: "clear", 2: "cloudy", 3: "light_rain", 4: "heavy_rain"}


def _copy_to_run(shared_path: Path, run_path: Path) -> None:
    run_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(shared_path, run_path)


def _require_value(section: str, key: str, value):
    if value is None:
        raise ValueError(
            f"Missing config value `{section}.{key}`. "
            "Update both `configs/base.yaml` and the matching stage fragment."
        )
    if isinstance(value, str) and not value.strip():
        raise ValueError(
            f"Blank config value `{section}.{key}`. "
            "Update both `configs/base.yaml` and the matching stage fragment."
        )
    return value


def _validate_fetch_config(cfg) -> dict[str, str]:
    fetch_cfg = cfg.fetch
    source_url = str(_require_value("fetch", "source_url", fetch_cfg.source_url))
    parsed = urlparse(source_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("fetch.source_url must be an HTTP(S) URL.")

    return {
        "dataset_name": str(_require_value("fetch", "dataset_name", fetch_cfg.dataset_name)),
        "raw_artifact_name": str(
            _require_value("fetch", "raw_artifact_name", fetch_cfg.raw_artifact_name)
        ),
        "source_data_path": str(
            _require_value("fetch", "source_data_path", fetch_cfg.source_data_path)
        ),
        "source_url": source_url,
    }


def _download_source_bytes(source_url: str) -> bytes:
    with urllib.request.urlopen(source_url, timeout=30) as response:
        return response.read()


def _validate_raw_columns(raw_table: pd.DataFrame) -> None:
    missing_columns = [column for column in RAW_REQUIRED_COLUMNS if column not in raw_table.columns]
    if missing_columns:
        raise ValueError(
            "Raw bike-demand table is missing required columns: " + ", ".join(missing_columns)
        )


def _map_labels(series: pd.Series, labels: dict[int, str]) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    mapped = numeric.map(labels)
    fallback = series.astype(str).str.strip()
    return mapped.fillna(fallback)


def _normalize_raw_table(raw_table: pd.DataFrame) -> pd.DataFrame:
    _validate_raw_columns(raw_table)
    normalized = raw_table.loc[:, RAW_REQUIRED_COLUMNS].copy()
    normalized["dteday"] = pd.to_datetime(normalized["dteday"]).dt.strftime("%Y-%m-%d")
    normalized["hr"] = normalized["hr"].astype(int)
    normalized["cnt"] = normalized["cnt"].astype(int)
    normalized["season"] = normalized["season"].astype(str).str.strip()
    normalized["weathersit"] = normalized["weathersit"].astype(str).str.strip()
    return normalized


def _archive_bytes_to_raw_table(archive_bytes: bytes) -> pd.DataFrame:
    with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
        members = [name for name in archive.namelist() if not name.endswith("/")]
        dataset_member = next(
            (name for name in members if Path(name).name.lower() == UCI_HOURLY_MEMBER_NAME),
            None,
        )
        if dataset_member is None:
            raise ValueError("Downloaded archive does not contain `hour.csv`.")

        hourly = pd.read_csv(archive.open(dataset_member))

    _validate_raw_columns(hourly)
    workshop_source = hourly.loc[:, RAW_REQUIRED_COLUMNS].head(WORKSHOP_ROW_COUNT).copy()
    if len(workshop_source) != WORKSHOP_ROW_COUNT:
        raise ValueError(
            f"Downloaded hourly source must contain at least {WORKSHOP_ROW_COUNT} rows."
        )

    timestamps = pd.date_range(WORKSHOP_START, periods=WORKSHOP_ROW_COUNT, freq="h")
    workshop_source["dteday"] = timestamps.strftime("%Y-%m-%d")
    workshop_source["hr"] = timestamps.hour
    workshop_source["cnt"] = workshop_source["cnt"].astype(int)
    workshop_source["season"] = _map_labels(workshop_source["season"], SEASON_LABELS)
    workshop_source["weathersit"] = _map_labels(
        workshop_source["weathersit"],
        WEATHER_LABELS,
    )
    return workshop_source[RAW_REQUIRED_COLUMNS]


def _source_bytes_to_raw_table(source_bytes: bytes) -> pd.DataFrame:
    try:
        return _archive_bytes_to_raw_table(source_bytes)
    except zipfile.BadZipFile:
        try:
            raw_table = pd.read_csv(io.BytesIO(source_bytes))
        except Exception as exc:  # pragma: no cover - defensive parse guard
            raise ValueError(
                "Downloaded source could not be parsed as a CSV or supported zip archive."
            ) from exc
        return _normalize_raw_table(raw_table)


def _write_source_csv(raw_table: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    raw_table.to_csv(output_path, index=False, lineterminator="\n")


def run_fetch(cfg, ctx=None, source_downloader=None) -> dict:
    fetch_cfg = _validate_fetch_config(cfg)
    dataset_name = str(fetch_cfg["dataset_name"])
    raw_artifact_name = str(fetch_cfg["raw_artifact_name"])
    source_data_path = Path(fetch_cfg["source_data_path"])
    source_url = str(fetch_cfg["source_url"])
    source_downloader = _download_source_bytes if source_downloader is None else source_downloader

    if not source_data_path.exists():
        source_bytes = source_downloader(source_url)
        raw_source_table = _source_bytes_to_raw_table(source_bytes)
        _write_source_csv(raw_source_table, source_data_path)
        downloaded = True
    else:
        downloaded = False

    raw_dir = Path(cfg.paths.raw_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    shared_raw_csv = raw_dir / raw_artifact_name

    logger.info("[fetch]")
    logger.info(
        "fetch:start dataset=%s source_url=%s source_csv=%s shared_output=%s",
        dataset_name,
        source_url,
        source_data_path,
        shared_raw_csv,
    )

    shutil.copy2(source_data_path, shared_raw_csv)
    raw_table = pd.read_csv(shared_raw_csv)
    _validate_raw_columns(raw_table)

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
        "fetch:finish rows=%d columns=%s downloaded=%s output=%s\n",
        len(raw_table),
        raw_table.columns.tolist(),
        downloaded,
        output_raw_csv,
    )

    return {
        "dataset_name": dataset_name,
        "source_url": source_url,
        "source_csv": str(source_data_path),
        "raw_csv": str(output_raw_csv),
        "shared_raw_csv": str(shared_raw_csv),
        "n_rows": int(len(raw_table)),
        "columns": raw_table.columns.tolist(),
        "downloaded": downloaded,
        "copied_to_run": copied_to_run,
    }
