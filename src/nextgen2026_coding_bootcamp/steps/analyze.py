from __future__ import annotations

import json
import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def build_hourly_profile(df: pd.DataFrame) -> pd.DataFrame:
    """Build a profile of mean rentals by hour and day type."""
    return (
        df.groupby(["hour", "day_type"], as_index=False)["total_rentals"]
        .mean()
        .rename(columns={"total_rentals": "mean_rentals"})
    )


def run_analyze(cfg, ctx=None) -> dict:
    """Run the full analyze stage with a composed configuration."""
    prepared_csv = Path(cfg.paths.intermediate_dir) / "hourly_bike_data.csv"

    if ctx is None:
        output_dir = Path(cfg.paths.results_dir)
    else:
        output_dir = ctx.run_dir / "analyze"
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"analyze:start input={prepared_csv}")

    prepared = pd.read_csv(prepared_csv)

    # Calculate high demand threshold and share
    high_demand_quantile = float(cfg.analysis.high_demand_quantile)
    high_demand_threshold = float(
        prepared["total_rentals"].quantile(high_demand_quantile)
    )

    prepared_with_threshold = prepared.assign(
        is_high_demand=lambda x: x["total_rentals"] >= high_demand_threshold,
    )

    # 1. Hourly Profile
    hourly_profile = build_hourly_profile(prepared)

    # 2. High Demand Share
    high_demand_share_by_hour = (
        prepared_with_threshold.groupby("hour", as_index=False)["is_high_demand"]
        .mean()
        .rename(columns={"is_high_demand": "high_demand_share"})
    )

    # 3. Weather Summary
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
        logger.warning("analyze:weather_column_missing skipping aggregation")
        weather_summary = pd.DataFrame(
            columns=["weather", "mean_rentals", "observations"]
        )

    # Define output paths
    profile_path = output_dir / "hourly_profile.csv"
    demand_share_path = output_dir / "high_demand_share_by_hour.csv"
    weather_summary_path = output_dir / "weather_summary.csv"
    summary_json_path = output_dir / "high_demand_summary.json"

    # Save results
    logger.info(f"analyze:write profile={profile_path}")
    hourly_profile.to_csv(profile_path, index=False)

    logger.info(f"analyze:write demand_share={demand_share_path}")
    high_demand_share_by_hour.to_csv(demand_share_path, index=False)

    logger.info(f"analyze:write weather_summary={weather_summary_path}")
    weather_summary.to_csv(weather_summary_path, index=False)

    summary_data = {
        "high_demand_quantile": high_demand_quantile,
        "high_demand_threshold": high_demand_threshold,
        "rows_in": int(len(prepared)),
        "rows_high_demand": int(prepared_with_threshold["is_high_demand"].sum()),
    }

    logger.info(f"analyze:write summary={summary_json_path}")
    summary_json_path.write_text(json.dumps(summary_data, indent=2) + "\n")

    logger.info(
        f"analyze:finish rows_in={len(prepared)} threshold={high_demand_threshold:.2f}"
    )

    return {
        "prepared_csv": str(prepared_csv),
        "hourly_profile_csv": str(profile_path),
        "high_demand_share_csv": str(demand_share_path),
        "weather_summary_csv": str(weather_summary_path),
        "summary_json": str(summary_json_path),
    }
