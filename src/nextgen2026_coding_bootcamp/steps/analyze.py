from __future__ import annotations

import json
from pathlib import Path
import logging

import pandas as pd

logger = logging.getLogger(__name__)


def _resolve_prepared_csv(cfg, ctx=None, input_csv: Path | None = None) -> Path:
    if input_csv is not None:
        return input_csv

    if ctx is not None:
        prepare_artifact = ctx.artifacts.get("prepare", {})
        prepare_csv = prepare_artifact.get("prepared_csv")
        if prepare_csv:
            return Path(prepare_csv)

    return Path(cfg.paths.intermediate_dir) / "hourly_bike_data.csv"


def build_hourly_profile(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["hour", "day_type"], as_index=False)["total_rentals"]
        .mean()
        .rename(columns={"total_rentals": "mean_rentals"})
    )


def run_analyze(cfg, ctx=None, input_csv: Path | None = None) -> dict:
    prepared_csv = _resolve_prepared_csv(cfg=cfg, ctx=ctx, input_csv=input_csv)

    if ctx is None:
        output_dir = Path(cfg.paths.results_dir)
    else:
        output_dir = ctx.run_dir / "analyze"
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("analyze:start input=%s", prepared_csv)

    prepared = pd.read_csv(prepared_csv)

    high_demand_quantile = float(cfg.analysis.high_demand_quantile)
    high_demand_threshold = float(prepared["total_rentals"].quantile(high_demand_quantile))
    prepared_with_threshold = prepared.assign(
        is_high_demand=lambda x: x["total_rentals"] >= high_demand_threshold,
    )

    hourly_profile = build_hourly_profile(prepared)

    high_demand_share_by_hour = (
        prepared_with_threshold.groupby("hour", as_index=False)["is_high_demand"]
        .mean()
        .rename(columns={"is_high_demand": "high_demand_share"})
    )

    if "weather" in prepared.columns:
        weather_summary = (
            prepared.groupby("weather", as_index=False)
            .agg(
                mean_rentals=("total_rentals", "mean"),
                observations=("total_rentals", "size"),
            )
            .sort_values("mean_rentals", ascending=False)
        )
    else:
        logger.warning("analyze:weather_column_missing skipping weather summary aggregation")
        weather_summary = pd.DataFrame(
            columns=["weather", "mean_rentals", "observations"],
        )

    summary = {
        "high_demand_quantile": high_demand_quantile,
        "high_demand_threshold": high_demand_threshold,
        "rows_in": int(len(prepared)),
        "rows_high_demand": int(prepared_with_threshold["is_high_demand"].sum()),
    }

    hourly_profile_path = output_dir / "hourly_profile.csv"
    high_demand_share_path = output_dir / "high_demand_share_by_hour.csv"
    weather_summary_path = output_dir / "weather_summary.csv"
    summary_path = output_dir / "high_demand_summary.json"

    hourly_profile.to_csv(hourly_profile_path, index=False)
    high_demand_share_by_hour.to_csv(high_demand_share_path, index=False)
    weather_summary.to_csv(weather_summary_path, index=False)
    summary_path.write_text(json.dumps(summary, indent=2) + "\n")

    logger.info(
        "analyze:finish rows_in=%d rows_out_profile=%d threshold=%s",
        len(prepared),
        len(hourly_profile),
        high_demand_threshold,
    )

    return {
        "prepared_csv": str(prepared_csv),
        "hourly_profile_csv": str(hourly_profile_path),
        "high_demand_share_csv": str(high_demand_share_path),
        "weather_summary_csv": str(weather_summary_path),
        "summary_json": str(summary_path),
        "high_demand_quantile": high_demand_quantile,
        "high_demand_threshold": high_demand_threshold,
    }
