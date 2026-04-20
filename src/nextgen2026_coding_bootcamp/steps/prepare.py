from __future__ import annotations

from pathlib import Path
import logging

import pandas as pd

logger = logging.getLogger(__name__)

SEASON_MAP = {1: "winter", 2: "spring", 3: "summer", 4: "fall"}
WEATHER_MAP = {
    1: "clear",
    2: "mist_cloud",
    3: "light_rain_or_snow",
    4: "heavy_rain_or_snow",
}
DAY_TYPE_MAP = {0: "non_working_day", 1: "working_day"}

PREPARED_COLUMNS = [
    "date",
    "hour",
    "season",
    "month",
    "weekday",
    "holiday",
    "workingday",
    "day_type",
    "weather",
    "temp_c",
    "feels_like_c",
    "humidity_pct",
    "windspeed_kph",
    "casual",
    "registered",
    "total_rentals",
]


def _resolve_input_csv(cfg, ctx=None, input_csv: Path | None = None) -> Path:
    if input_csv is not None:
        return input_csv

    if ctx is not None:
        fetch_artifact = ctx.artifacts.get("fetch", {})
        fetch_csv = fetch_artifact.get("raw_csv")
        if fetch_csv:
            return Path(fetch_csv)

    return Path(cfg.paths.raw_dir) / str(cfg.fetch.archive_member)


def run_prepare(cfg, ctx=None, input_csv: Path | None = None) -> dict:
    source_csv = _resolve_input_csv(cfg=cfg, ctx=ctx, input_csv=input_csv)

    if ctx is None:
        stage_output_dir = Path(cfg.paths.intermediate_dir)
    else:
        stage_output_dir = ctx.run_dir / "prepare"
    stage_output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("prepare:start input=%s", source_csv)

    raw = pd.read_csv(source_csv, parse_dates=["dteday"])
    keep_holidays = bool(cfg.prepare.keep_holidays)
    if not keep_holidays:
        raw = raw.loc[raw["holiday"] == 0].copy()

    prepared = (
        raw.rename(columns={"dteday": "date", "cnt": "total_rentals"})
        .assign(
            season=lambda x: x["season"].map(SEASON_MAP),
            weather=lambda x: x["weathersit"].map(WEATHER_MAP),
            day_type=lambda x: x["workingday"].map(DAY_TYPE_MAP),
            temp_c=lambda x: x["temp"] * 47 - 8,
            feels_like_c=lambda x: x["atemp"] * 66 - 16,
            humidity_pct=lambda x: x["hum"] * 100,
            windspeed_kph=lambda x: x["windspeed"] * 67,
        )
        .loc[
            :,
            [
                "date",
                "hr",
                "season",
                "mnth",
                "weekday",
                "holiday",
                "workingday",
                "day_type",
                "weather",
                "temp_c",
                "feels_like_c",
                "humidity_pct",
                "windspeed_kph",
                "casual",
                "registered",
                "total_rentals",
            ],
        ]
        .rename(columns={"hr": "hour", "mnth": "month"})
    )

    output_csv = stage_output_dir / "hourly_bike_data.csv"
    wrote_prepared_csv = bool(cfg.prepare.write_prepared_csv)
    if wrote_prepared_csv:
        prepared.to_csv(output_csv, index=False)
        output_path = str(output_csv)
    else:
        output_path = None

    logger.info(
        "prepare:finish rows_in=%d rows_out=%d keep_holidays=%s wrote_csv=%s",
        len(raw),
        len(prepared),
        keep_holidays,
        wrote_prepared_csv,
    )

    return {
        "raw_csv": str(source_csv),
        "prepared_csv": output_path,
        "rows_out": int(len(prepared)),
        "columns": PREPARED_COLUMNS,
        "keep_holidays": keep_holidays,
    }
