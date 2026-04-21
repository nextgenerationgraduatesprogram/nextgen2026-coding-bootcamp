from __future__ import annotations

import pandas as pd
import json
from pathlib import Path


def build_hourly_profile(input_csv: Path, output_csv: Path) -> dict:
    """Build a profile of mean rentals by hour and day type."""
    df = pd.read_csv(input_csv)

    profile = (
        df.groupby(["hour", "day_type"], as_index=False)["total_rentals"]
        .mean()
        .rename(columns={"total_rentals": "mean_rentals"})
    )

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    profile.to_csv(output_csv, index=False)

    return {
        "rows_in": int(len(df)),
        "rows_out": int(len(profile)),
        "output_csv": str(output_csv),
    }


def build_high_demand_share(
    input_csv: Path, output_csv: Path, quantile: float = 0.90
) -> dict:
    """Calculate the share of high-demand observations by hour."""
    df = pd.read_csv(input_csv)

    cutoff = df["total_rentals"].quantile(quantile)
    df["is_high_demand"] = df["total_rentals"] >= cutoff

    share = (
        df.groupby("hour", as_index=False)["is_high_demand"]
        .mean()
        .rename(columns={"is_high_demand": "high_demand_share"})
    )

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    share.to_csv(output_csv, index=False)

    return {
        "cutoff": float(cutoff),
        "output_csv": str(output_csv),
    }


def build_weather_summary(input_csv: Path, output_csv: Path) -> dict:
    """Summarize rentals by weather conditions."""
    df = pd.read_csv(input_csv)

    summary = (
        df.groupby("weather", as_index=False)
        .agg(
            mean_rentals=("total_rentals", "mean"),
            observations=("total_rentals", "size"),
        )
        .sort_values("mean_rentals", ascending=False)
    )

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output_csv, index=False)

    return {
        "output_csv": str(output_csv),
    }


def run_analyze(cfg) -> dict:
    """Run the analyze stage with a composed configuration."""
    prepared_csv = Path(cfg.paths.intermediate_dir) / "hourly_bike_data.csv"
    output_dir = Path(cfg.paths.results_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Use the helper functions but wire them to the config
    profile_path = output_dir / "hourly_profile.csv"
    demand_path = output_dir / "high_demand_share_by_hour.csv"
    weather_path = output_dir / "weather_summary.csv"
    summary_path = output_dir / "high_demand_summary.json"

    profile_metrics = build_hourly_profile(prepared_csv, profile_path)
    demand_metrics = build_high_demand_share(
        prepared_csv, demand_path, quantile=cfg.analysis.high_demand_quantile
    )
    build_weather_summary(prepared_csv, weather_path)

    summary_path.write_text(
        json.dumps(
            {
                "high_demand_quantile": float(cfg.analysis.high_demand_quantile),
                "high_demand_threshold": demand_metrics["cutoff"],
                "rows_in": profile_metrics["rows_in"],
            },
            indent=2,
        )
        + "\n"
    )

    return {
        "prepared_csv": str(prepared_csv),
        "hourly_profile_csv": str(profile_path),
        "summary_json": str(summary_path),
    }
