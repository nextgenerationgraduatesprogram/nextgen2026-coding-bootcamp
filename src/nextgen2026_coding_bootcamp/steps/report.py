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
        "class_summary_name": str(
            _require_value("analysis", "class_summary_name", analysis_cfg.class_summary_name)
        ),
        "representative_image_name": str(
            _require_value(
                "analysis",
                "representative_image_name",
                analysis_cfg.representative_image_name,
            )
        ),
        "markdown_name": str(
            _require_value("report", "markdown_name", report_cfg.markdown_name)
        ),
        "include_representative_image": bool(
            _require_value(
                "report",
                "include_representative_image",
                report_cfg.include_representative_image,
            )
        ),
    }


def _shared_analyze_paths(cfg, names: dict[str, object]) -> dict[str, Path | None]:
    results_dir = Path(cfg.paths.results_dir)
    class_summary_path = results_dir / str(names["class_summary_name"])
    representative_path = results_dir / str(names["representative_image_name"])
    return {
        "dataset_overview_json": results_dir / str(names["dataset_overview_name"]),
        "class_image_summary_csv": class_summary_path,
        "class_representatives_png": representative_path if representative_path.exists() else None,
    }


def _ctx_analyze_paths(cfg, ctx, names: dict[str, object]) -> dict[str, Path | None]:
    analyze_artifact = ctx.artifacts.get("analyze", {})
    if not analyze_artifact:
        return _shared_analyze_paths(cfg, names)

    overview_path = analyze_artifact.get("dataset_overview_json")
    summary_path = analyze_artifact.get("class_image_summary_csv")
    representative_path = analyze_artifact.get("class_representatives_png")
    return {
        "dataset_overview_json": Path(overview_path),
        "class_image_summary_csv": Path(summary_path) if summary_path else None,
        "class_representatives_png": Path(representative_path) if representative_path else None,
    }


def _relative_path(target_path: Path, start_path: Path) -> str:
    return Path(os.path.relpath(target_path, start=start_path)).as_posix()


def _format_summary_for_markdown(summary_df: pd.DataFrame) -> pd.DataFrame:
    # Student task:
    # Format integer columns as integers/strings and numeric metrics to 4 decimal places
    # before rendering the table into Markdown.
    raise NotImplementedError(
        "Implement `_format_summary_for_markdown()` in "
        "`src/nextgen2026_coding_bootcamp/steps/report.py`."
    )


def _dataframe_to_markdown_table(df: pd.DataFrame) -> str:
    # Student task:
    # Turn the input DataFrame into a GitHub-flavored Markdown table string.
    raise NotImplementedError(
        "Implement `_dataframe_to_markdown_table()` in "
        "`src/nextgen2026_coding_bootcamp/steps/report.py`."
    )


def build_digit_class_profiles_section(class_summary_csv: Path | None) -> list[str]:
    # Student task:
    # Read `class_image_summary.csv` from analyze output and build the lines for the
    # `## Digit Class Profiles` section. Raise `FileNotFoundError` if the summary is
    # missing instead of recomputing anything inside report.
    raise NotImplementedError(
        "Implement `build_digit_class_profiles_section()` in "
        "`src/nextgen2026_coding_bootcamp/steps/report.py`."
    )


def build_report_markdown(
    output_dir: Path,
    dataset_overview_json: Path,
    class_image_summary_csv: Path | None,
    class_representatives_png: Path | None,
    include_representative_image: bool,
) -> str:
    # Student task:
    # Build the report as a single Markdown string. The final report should contain:
    # - `# Digits Workflow Report`
    # - `## Dataset Overview`
    # - `## Analyze Artifacts`
    # - `## Representative Digits` (when enabled and present)
    # - `## Digit Class Profiles`
    raise NotImplementedError(
        "Implement `build_report_markdown()` in "
        "`src/nextgen2026_coding_bootcamp/steps/report.py`."
    )


def _write_report(
    output_dir: Path,
    markdown_name: str,
    dataset_overview_json: Path,
    class_image_summary_csv: Path | None,
    class_representatives_png: Path | None,
    include_representative_image: bool,
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
    include_representative_image = bool(names["include_representative_image"])

    shared_output_dir = Path(cfg.paths.results_dir)
    shared_output_dir.mkdir(parents=True, exist_ok=True)

    shared_inputs = _shared_analyze_paths(cfg, names)
    if ctx is None:
        report_inputs = shared_inputs
    else:
        report_inputs = _ctx_analyze_paths(cfg, ctx, names)

    logger.info(
        "[report]\nreport:start dataset_overview=%s class_summary=%s",
        report_inputs["dataset_overview_json"],
        report_inputs["class_image_summary_csv"],
    )

    # Student task:
    # Suggested shape for the implementation:
    #
    # shared_report_markdown = _write_report(
    #     output_dir=shared_output_dir,
    #     markdown_name=markdown_name,
    #     dataset_overview_json=shared_inputs["dataset_overview_json"],
    #     class_image_summary_csv=shared_inputs["class_image_summary_csv"],
    #     class_representatives_png=shared_inputs["class_representatives_png"],
    #     include_representative_image=include_representative_image,
    # )
    #
    # If `ctx` is provided, write a run-scoped copy under `ctx.run_dir / "report"`
    # using `report_inputs`. Otherwise return the shared report path.
    #
    # Expected return keys:
    # - dataset_overview_json
    # - class_image_summary_csv
    # - class_representatives_png
    # - report_markdown
    # - shared_report_markdown
    # - copied_to_run
    raise NotImplementedError(
        "Student task: implement `run_report()` so the report stage reads analyze "
        "artifacts and writes `report.md` without recomputing summary metrics. "
        "Reference `docs/01-project-brief.md`, "
        "`docs/02-repo-workflow-and-missing-piece.md`, and "
        "`src/nextgen2026_coding_bootcamp/steps/prepare.py` for the stage structure."
    )
