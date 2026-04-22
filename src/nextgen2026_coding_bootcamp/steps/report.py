from __future__ import annotations

import logging
import os
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


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


def _validate_report_config(cfg) -> dict[str, object]:
    analysis_cfg = cfg.analysis
    report_cfg = cfg.report
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
        "markdown_name": str(
            _require_value("report", "markdown_name", report_cfg.markdown_name)
        ),
        "include_daily_cycle_plot": bool(
            _require_value(
                "report",
                "include_daily_cycle_plot",
                report_cfg.include_daily_cycle_plot,
            )
        ),
    }


def _shared_analyze_paths(cfg, names: dict[str, object]) -> dict[str, Path | None]:
    results_dir = Path(cfg.paths.results_dir)
    hourly_profile_path = results_dir / str(names["hourly_profile_name"])
    daily_cycle_plot_path = results_dir / str(names["daily_cycle_plot_name"])
    return {
        "dataset_overview_json": results_dir / str(names["dataset_overview_name"]),
        "hourly_demand_profile_csv": hourly_profile_path,
        "weekday_weekend_daily_cycle_png": (
            daily_cycle_plot_path if daily_cycle_plot_path.exists() else None
        ),
    }


def _ctx_analyze_paths(cfg, ctx, names: dict[str, object]) -> dict[str, Path | None]:
    analyze_artifact = ctx.artifacts.get("analyze", {})
    if not analyze_artifact:
        return _shared_analyze_paths(cfg, names)

    overview_path = analyze_artifact.get("dataset_overview_json")
    profile_path = analyze_artifact.get("hourly_demand_profile_csv")
    daily_cycle_plot_path = analyze_artifact.get("weekday_weekend_daily_cycle_png")
    return {
        "dataset_overview_json": Path(overview_path),
        "hourly_demand_profile_csv": Path(profile_path) if profile_path else None,
        "weekday_weekend_daily_cycle_png": (
            Path(daily_cycle_plot_path) if daily_cycle_plot_path else None
        ),
    }


def _relative_path(target_path: Path, start_path: Path) -> str:
    return Path(os.path.relpath(target_path, start=start_path)).as_posix()


def _format_profile_for_markdown(profile_df: pd.DataFrame) -> pd.DataFrame:
    # Student task:
    # Format integer columns as integers/strings and numeric metrics to 4 decimal places
    # before rendering the table into Markdown.
    raise NotImplementedError(
        "Implement `_format_profile_for_markdown()` in "
        "`src/nextgen2026_coding_bootcamp/steps/report.py`."
    )


def _dataframe_to_markdown_table(df: pd.DataFrame) -> str:
    # Student task:
    # Turn the input DataFrame into a GitHub-flavored Markdown table string.
    raise NotImplementedError(
        "Implement `_dataframe_to_markdown_table()` in "
        "`src/nextgen2026_coding_bootcamp/steps/report.py`."
    )


def build_hourly_demand_profiles_section(hourly_profile_csv: Path | None) -> list[str]:
    # Student task:
    # Read `hourly_demand_profile.csv` from analyze output and build the lines for the
    # `## Hourly Demand Profiles` section. Raise `FileNotFoundError` if the profile is
    # missing instead of recomputing anything inside report.
    raise NotImplementedError(
        "Implement `build_hourly_demand_profiles_section()` in "
        "`src/nextgen2026_coding_bootcamp/steps/report.py`."
    )


def build_report_markdown(
    output_dir: Path,
    dataset_overview_json: Path,
    hourly_demand_profile_csv: Path | None,
    weekday_weekend_daily_cycle_png: Path | None,
    include_daily_cycle_plot: bool,
) -> str:
    # Student task:
    # Build the report as a single Markdown string. The final report should contain:
    # - `# Bike Demand Workflow Report`
    # - `## Dataset Overview`
    # - `## Analyze Artifacts`
    # - `## Daily Demand Cycle` (when enabled and present)
    # - `## Hourly Demand Profiles`
    raise NotImplementedError(
        "Implement `build_report_markdown()` in "
        "`src/nextgen2026_coding_bootcamp/steps/report.py`."
    )


def _write_report(
    output_dir: Path,
    markdown_name: str,
    dataset_overview_json: Path,
    hourly_demand_profile_csv: Path | None,
    weekday_weekend_daily_cycle_png: Path | None,
    include_daily_cycle_plot: bool,
) -> Path:
    # Student task:
    # Create `output_dir`, render the report with `build_report_markdown()`, write it
    # to disk, and return the path to the Markdown file.
    raise NotImplementedError(
        "Implement `_write_report()` in "
        "`src/nextgen2026_coding_bootcamp/steps/report.py`."
    )


def run_report(cfg, ctx=None) -> dict:
    names = _validate_report_config(cfg)
    markdown_name = str(names["markdown_name"])
    include_daily_cycle_plot = bool(names["include_daily_cycle_plot"])

    shared_output_dir = Path(cfg.paths.results_dir)
    shared_output_dir.mkdir(parents=True, exist_ok=True)

    shared_inputs = _shared_analyze_paths(cfg, names)
    if ctx is None:
        report_inputs = shared_inputs
    else:
        report_inputs = _ctx_analyze_paths(cfg, ctx, names)

    logger.info(
        "[report]\nreport:start dataset_overview=%s hourly_profile=%s",
        report_inputs["dataset_overview_json"],
        report_inputs["hourly_demand_profile_csv"],
    )

    # Student task:
    # Suggested shape for the implementation:
    #
    # shared_report_markdown = _write_report(
    #     output_dir=shared_output_dir,
    #     markdown_name=markdown_name,
    #     dataset_overview_json=shared_inputs["dataset_overview_json"],
    #     hourly_demand_profile_csv=shared_inputs["hourly_demand_profile_csv"],
    #     weekday_weekend_daily_cycle_png=shared_inputs["weekday_weekend_daily_cycle_png"],
    #     include_daily_cycle_plot=include_daily_cycle_plot,
    # )
    #
    # If `ctx` is provided, write a run-scoped copy under `ctx.run_dir / "report"`
    # using `report_inputs`. Otherwise return the shared report path.
    #
    # Expected return keys:
    # - dataset_overview_json
    # - hourly_demand_profile_csv
    # - weekday_weekend_daily_cycle_png
    # - report_markdown
    # - shared_report_markdown
    # - copied_to_run
    raise NotImplementedError(
        "Student task: implement `run_report()` so the report stage reads analyze "
        "artifacts and writes `report.md` without recomputing hourly metrics. "
        "Reference `docs/01-project-brief.md`, "
        "`docs/02-repo-workflow-and-missing-piece.md`, and "
        "`src/nextgen2026_coding_bootcamp/steps/prepare.py` for the stage structure."
    )
