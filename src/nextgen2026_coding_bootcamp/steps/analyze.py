from __future__ import annotations

import logging
from pathlib import Path
import shutil

import pandas as pd

logger = logging.getLogger(__name__)

HOURLY_DEMAND_PROFILE_COLUMNS = [
    "day_type",
    "hour",
    "n_observations",
    "mean_demand",
    "median_demand",
    "std_demand",
]

DATASET_OVERVIEW_KEYS = [
    "dataset_name",
    "n_rows",
    "timestamp_start",
    "timestamp_end",
    "target_column",
    "day_types",
    "rows_per_day_type",
]


def _resolve_prepare_input(
    cfg,
    ctx=None,
    prepared_csv: Path | None = None,
) -> Path:
    if prepared_csv is not None:
        return prepared_csv

    if ctx is not None:
        prepare_artifact = ctx.artifacts.get("prepare", {})
        prepared_table = prepare_artifact.get("prepared_csv")
        if prepared_table:
            return Path(prepared_table)

    return Path(cfg.paths.intermediate_dir) / str(cfg.prepare.prepared_table_name)


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


def _validate_analysis_config(cfg) -> dict[str, object]:
    analysis_cfg = cfg.analysis
    return {
        "dataset_overview_name": str(
            _require_value("analysis", "dataset_overview_name", analysis_cfg.dataset_overview_name)
        ),
        "hourly_profile_name": str(
            _require_value("analysis", "hourly_profile_name", analysis_cfg.hourly_profile_name)
        ),
        "daily_cycle_plot_name": str(
            _require_value(
                "analysis",
                "daily_cycle_plot_name",
                analysis_cfg.daily_cycle_plot_name,
            )
        ),
        "generate_daily_cycle_plot": bool(
            _require_value(
                "analysis",
                "generate_daily_cycle_plot",
                analysis_cfg.generate_daily_cycle_plot,
            )
        ),
    }


def build_dataset_overview(prepared: pd.DataFrame, dataset_name: str) -> dict:
    # Student task:
    # Build the JSON payload written to `dataset_overview.json`.
    # Required keys are listed in `DATASET_OVERVIEW_KEYS`.
    raise NotImplementedError(
        "Implement `build_dataset_overview()` in "
        "`src/nextgen2026_coding_bootcamp/steps/analyze.py`."
    )


def build_hourly_demand_profile(prepared: pd.DataFrame) -> pd.DataFrame:
    # Student task:
    # Return one row per `day_type` and hour bucket with the required columns in
    # `HOURLY_DEMAND_PROFILE_COLUMNS`.
    raise NotImplementedError(
        "Implement `build_hourly_demand_profile()` in "
        "`src/nextgen2026_coding_bootcamp/steps/analyze.py`."
    )


def write_daily_cycle_plot(hourly_profile: pd.DataFrame, output_path: Path) -> None:
    # Student task:
    # Plot the weekday and weekend mean-demand curves and write the chart to
    # `output_path`. `matplotlib` is already available in the project dependencies.
    raise NotImplementedError(
        "Implement `write_daily_cycle_plot()` in "
        "`src/nextgen2026_coding_bootcamp/steps/analyze.py`."
    )


def run_analyze(
    cfg,
    ctx=None,
    prepared_csv: Path | None = None,
) -> dict:
    prepared_table_csv = _resolve_prepare_input(
        cfg=cfg,
        ctx=ctx,
        prepared_csv=prepared_csv,
    )
    analysis_cfg = _validate_analysis_config(cfg)

    shared_output_dir = Path(cfg.paths.results_dir)
    shared_output_dir.mkdir(parents=True, exist_ok=True)

    shared_dataset_overview_json = (
        shared_output_dir / analysis_cfg["dataset_overview_name"]
    )
    shared_hourly_demand_profile_csv = (
        shared_output_dir / analysis_cfg["hourly_profile_name"]
    )
    shared_weekday_weekend_daily_cycle_png = (
        shared_output_dir / analysis_cfg["daily_cycle_plot_name"]
    )

    logger.info(
        "[analyze]\nanalyze:start prepared_csv=%s",
        prepared_table_csv,
    )

    # Student task:
    # Suggested shape for the implementation:
    #
    # prepared = pd.read_csv(prepared_table_csv)
    # overview = build_dataset_overview(
    #     prepared=prepared,
    #     dataset_name=str(cfg.fetch.dataset_name),
    # )
    # hourly_profile = build_hourly_demand_profile(prepared=prepared)
    # if analysis_cfg["generate_daily_cycle_plot"]:
    #     write_daily_cycle_plot(hourly_profile=hourly_profile, output_path=...)
    # hourly_profile.to_csv(shared_hourly_demand_profile_csv, index=False)
    #
    # If `ctx` is provided, copy shared outputs into `ctx.run_dir / "analyze"` using
    # `_copy_to_run`, then return the run-scoped paths. Otherwise return shared paths.
    #
    # Expected return keys:
    # - prepared_csv
    # - dataset_overview_json
    # - hourly_demand_profile_csv
    # - weekday_weekend_daily_cycle_png
    # - shared_dataset_overview_json
    # - shared_hourly_demand_profile_csv
    # - shared_weekday_weekend_daily_cycle_png
    # - expected_hourly_profile_columns
    # - copied_to_run
    raise NotImplementedError(
        "Student task: implement `run_analyze()` so the analyze stage reads "
        "`prepared_demand.csv`, writes `dataset_overview.json`, "
        "`hourly_demand_profile.csv`, and `weekday_weekend_daily_cycle.png`, "
        "then returns the artifact dictionary described in this file. Reference "
        "`src/nextgen2026_coding_bootcamp/steps/prepare.py`, "
        "`docs/01-project-brief.md`, and "
        "`docs/02-repo-workflow-and-missing-piece.md`."
    )
