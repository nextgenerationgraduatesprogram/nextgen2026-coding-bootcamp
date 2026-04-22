from __future__ import annotations

import logging
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
        "predictions_name": str(
            _require_value("analysis", "predictions_name", analysis_cfg.predictions_name)
        ),
        "evaluation_summary_name": str(
            _require_value(
                "analysis",
                "evaluation_summary_name",
                analysis_cfg.evaluation_summary_name,
            )
        ),
        "markdown_name": str(
            _require_value("report", "markdown_name", report_cfg.markdown_name)
        ),
        "max_examples": int(_require_value("report", "max_examples", report_cfg.max_examples)),
    }


def _shared_analyze_paths(cfg, names: dict[str, object]) -> dict[str, Path | None]:
    results_dir = Path(cfg.paths.results_dir)
    return {
        "message_predictions_csv": results_dir / str(names["predictions_name"]),
        "evaluation_summary_json": results_dir / str(names["evaluation_summary_name"]),
    }


def _ctx_analyze_paths(cfg, ctx, names: dict[str, object]) -> dict[str, Path | None]:
    analyze_artifact = ctx.artifacts.get("analyze", {})
    if not analyze_artifact:
        return _shared_analyze_paths(cfg, names)

    predictions_path = analyze_artifact.get("message_predictions_csv")
    evaluation_path = analyze_artifact.get("evaluation_summary_json")
    return {
        "message_predictions_csv": Path(predictions_path) if predictions_path else None,
        "evaluation_summary_json": Path(evaluation_path) if evaluation_path else None,
    }


def _format_examples_for_markdown(examples_df: pd.DataFrame) -> pd.DataFrame:
    # Student task:
    # Format booleans and any other display values before turning example rows into
    # Markdown.
    raise NotImplementedError(
        "Implement `_format_examples_for_markdown()` in "
        "`src/nextgen2026_coding_bootcamp/steps/report.py`."
    )


def _dataframe_to_markdown_table(df: pd.DataFrame) -> str:
    # Student task:
    # Turn the input DataFrame into a GitHub-flavored Markdown table string.
    raise NotImplementedError(
        "Implement `_dataframe_to_markdown_table()` in "
        "`src/nextgen2026_coding_bootcamp/steps/report.py`."
    )


def build_prediction_examples_section(
    message_predictions_csv: Path | None,
    max_examples: int,
) -> list[str]:
    # Student task:
    # Read `message_predictions.csv` from analyze output and build the lines for the
    # `## Prediction Examples` section. Raise `FileNotFoundError` if the predictions
    # file is missing instead of recomputing anything inside report.
    raise NotImplementedError(
        "Implement `build_prediction_examples_section()` in "
        "`src/nextgen2026_coding_bootcamp/steps/report.py`."
    )


def build_report_markdown(
    evaluation_summary_json: Path,
    message_predictions_csv: Path | None,
    max_examples: int,
) -> str:
    # Student task:
    # Build the report as a single Markdown string. The final report should contain:
    # - `# SMS Classification Workflow Report`
    # - `## Dataset Overview`
    # - `## Analyze Artifacts`
    # - `## Evaluation Summary`
    # - `## Prediction Examples`
    raise NotImplementedError(
        "Implement `build_report_markdown()` in "
        "`src/nextgen2026_coding_bootcamp/steps/report.py`."
    )


def _write_report(
    output_dir: Path,
    markdown_name: str,
    evaluation_summary_json: Path,
    message_predictions_csv: Path | None,
    max_examples: int,
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
    max_examples = int(names["max_examples"])

    shared_output_dir = Path(cfg.paths.results_dir)
    shared_output_dir.mkdir(parents=True, exist_ok=True)

    shared_inputs = _shared_analyze_paths(cfg, names)
    if ctx is None:
        report_inputs = shared_inputs
    else:
        report_inputs = _ctx_analyze_paths(cfg, ctx, names)

    logger.info(
        "[report]\nreport:start evaluation_summary=%s predictions=%s",
        report_inputs["evaluation_summary_json"],
        report_inputs["message_predictions_csv"],
    )

    # Student task:
    # Suggested shape for the implementation:
    #
    # shared_report_markdown = _write_report(
    #     output_dir=shared_output_dir,
    #     markdown_name=markdown_name,
    #     evaluation_summary_json=shared_inputs["evaluation_summary_json"],
    #     message_predictions_csv=shared_inputs["message_predictions_csv"],
    #     max_examples=max_examples,
    # )
    #
    # If `ctx` is provided, write a run-scoped copy under `ctx.run_dir / "report"`
    # using `report_inputs`. Otherwise return the shared report path.
    #
    # Expected return keys:
    # - evaluation_summary_json
    # - message_predictions_csv
    # - report_markdown
    # - shared_report_markdown
    # - max_examples
    # - copied_to_run
    raise NotImplementedError(
        "Student task: implement `run_report()` so the report stage reads analyze "
        "artifacts and writes `report.md` without recomputing the evaluation summary. "
        "Reference `docs/01-project-brief.md`, "
        "`docs/02-repo-workflow-and-missing-piece.md`, and "
        "`src/nextgen2026_coding_bootcamp/steps/prepare.py`."
    )
