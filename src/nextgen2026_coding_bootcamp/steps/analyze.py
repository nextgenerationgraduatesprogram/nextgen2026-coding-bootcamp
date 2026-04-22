from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

MESSAGE_PREDICTION_COLUMNS = [
    "message_id",
    "text",
    "true_label",
    "predicted_label",
    "is_correct",
    "raw_response",
]

EVALUATION_SUMMARY_KEYS = [
    "dataset_name",
    "n_messages_prepared",
    "sample_size",
    "sample_seed",
    "labels",
    "model",
    "temperature",
    "n_correct",
    "n_incorrect",
    "accuracy",
    "invalid_response_count",
    "confusion_matrix",
]


def _resolve_prepare_input(
    cfg,
    ctx=None,
    prepared_messages_csv: Path | None = None,
) -> Path:
    if prepared_messages_csv is not None:
        return prepared_messages_csv

    if ctx is not None:
        prepare_artifact = ctx.artifacts.get("prepare", {})
        prepared_messages_path = prepare_artifact.get("prepared_messages_csv")
        if prepared_messages_path:
            return Path(prepared_messages_path)

    return Path(cfg.paths.intermediate_dir) / str(cfg.prepare.prepared_messages_name)


def _copy_to_run(shared_path: Path, run_path: Path) -> None:
    run_path.parent.mkdir(parents=True, exist_ok=True)
    run_path.write_bytes(shared_path.read_bytes())


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
        "sample_size": int(_require_value("analysis", "sample_size", analysis_cfg.sample_size)),
        "sample_seed": int(_require_value("analysis", "sample_seed", analysis_cfg.sample_seed)),
        "model": str(_require_value("analysis", "model", analysis_cfg.model)),
        "temperature": float(
            _require_value("analysis", "temperature", analysis_cfg.temperature)
        ),
    }


def select_message_sample(
    prepared_messages: pd.DataFrame,
    sample_size: int,
    sample_seed: int,
) -> pd.DataFrame:
    # Student task:
    # Select a bounded, deterministic sample from `prepared_messages`.
    # The returned rows should preserve the original columns and use
    # `sample_seed` so repeated runs are reproducible.
    raise NotImplementedError(
        "Implement `select_message_sample()` in "
        "`src/nextgen2026_coding_bootcamp/steps/analyze.py`."
    )


def build_classification_prompt(message_text: str) -> str:
    # Student task:
    # Build a short prompt that asks the model to classify one SMS message as either
    # `ham` or `spam`.
    raise NotImplementedError(
        "Implement `build_classification_prompt()` in "
        "`src/nextgen2026_coding_bootcamp/steps/analyze.py`."
    )


def parse_model_label(raw_response: str) -> str:
    # Student task:
    # Normalize the model response into one of:
    # - `ham`
    # - `spam`
    # - `invalid`
    raise NotImplementedError(
        "Implement `parse_model_label()` in "
        "`src/nextgen2026_coding_bootcamp/steps/analyze.py`."
    )


def build_evaluation_summary(
    predictions: pd.DataFrame,
    dataset_name: str,
    n_messages_prepared: int,
    sample_size: int,
    sample_seed: int,
    model: str,
    temperature: float,
) -> dict:
    # Student task:
    # Build the JSON payload written to `evaluation_summary.json`.
    # Required keys are listed in `EVALUATION_SUMMARY_KEYS`.
    raise NotImplementedError(
        "Implement `build_evaluation_summary()` in "
        "`src/nextgen2026_coding_bootcamp/steps/analyze.py`."
    )


def run_analyze(
    cfg,
    ctx=None,
    prepared_messages_csv: Path | None = None,
) -> dict:
    prepared_messages_path = _resolve_prepare_input(
        cfg=cfg,
        ctx=ctx,
        prepared_messages_csv=prepared_messages_csv,
    )
    analysis_cfg = _validate_analysis_config(cfg)

    shared_output_dir = Path(cfg.paths.results_dir)
    shared_output_dir.mkdir(parents=True, exist_ok=True)

    shared_predictions_csv = shared_output_dir / analysis_cfg["predictions_name"]
    shared_evaluation_summary_json = (
        shared_output_dir / analysis_cfg["evaluation_summary_name"]
    )

    logger.info("[analyze]")
    logger.info("analyze:start prepared_messages=%s", prepared_messages_path)

    # Student task:
    # Suggested shape for the implementation:
    #
    # prepared_messages = pd.read_csv(prepared_messages_path)
    # sampled_messages = select_message_sample(
    #     prepared_messages=prepared_messages,
    #     sample_size=analysis_cfg["sample_size"],
    #     sample_seed=analysis_cfg["sample_seed"],
    # )
    #
    # prediction_rows = []
    # for row in sampled_messages.itertuples(index=False):
    #     prompt = build_classification_prompt(row.text)
    #     raw_response = ...  # call your chosen LLM client here
    #     predicted_label = parse_model_label(raw_response)
    #     prediction_rows.append(
    #         {
    #             "message_id": row.message_id,
    #             "text": row.text,
    #             "true_label": row.label,
    #             "predicted_label": predicted_label,
    #             "is_correct": predicted_label == row.label,
    #             "raw_response": raw_response,
    #         }
    #     )
    #
    # predictions = pd.DataFrame(prediction_rows, columns=MESSAGE_PREDICTION_COLUMNS)
    # evaluation_summary = build_evaluation_summary(
    #     predictions=predictions,
    #     dataset_name=str(cfg.fetch.dataset_name),
    #     n_messages_prepared=len(prepared_messages),
    #     sample_size=analysis_cfg["sample_size"],
    #     sample_seed=analysis_cfg["sample_seed"],
    #     model=str(analysis_cfg["model"]),
    #     temperature=float(analysis_cfg["temperature"]),
    # )
    #
    # predictions.to_csv(shared_predictions_csv, index=False)
    # shared_evaluation_summary_json.write_text(..., encoding="utf-8")
    #
    # If `ctx` is provided, copy shared outputs into `ctx.run_dir / "analyze"` using
    # `_copy_to_run`, then return the run-scoped paths. Otherwise return shared paths.
    #
    # Expected return keys:
    # - prepared_messages_csv
    # - message_predictions_csv
    # - evaluation_summary_json
    # - shared_message_predictions_csv
    # - shared_evaluation_summary_json
    # - expected_prediction_columns
    # - sample_size
    # - sample_seed
    # - model
    # - temperature
    # - copied_to_run
    raise NotImplementedError(
        "Student task: implement `run_analyze()` so the analyze stage reads "
        "`prepared_messages.csv`, writes `message_predictions.csv` and "
        "`evaluation_summary.json`, then returns the artifact dictionary "
        "described in this file. Reference "
        "`docs/01-project-brief.md`, `docs/02-repo-workflow-and-missing-piece.md`, "
        "and `src/nextgen2026_coding_bootcamp/steps/prepare.py`."
    )
