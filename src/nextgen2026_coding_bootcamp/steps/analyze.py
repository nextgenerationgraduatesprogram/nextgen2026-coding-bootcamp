from __future__ import annotations

import logging
from pathlib import Path
import shutil

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

CLASS_IMAGE_SUMMARY_COLUMNS = [
    "label",
    "n_images",
    "mean_intensity",
    "std_intensity",
    "mean_edge_density",
]

DATASET_OVERVIEW_KEYS = [
    "dataset_name",
    "n_images",
    "n_classes",
    "image_height",
    "image_width",
    "labels",
    "images_per_class",
]


def _resolve_prepare_inputs(
    cfg,
    ctx=None,
    images_npy: Path | None = None,
    metadata_csv: Path | None = None,
) -> tuple[Path, Path]:
    if images_npy is not None and metadata_csv is not None:
        return images_npy, metadata_csv

    if ctx is not None:
        prepare_artifact = ctx.artifacts.get("prepare", {})
        prepare_images = prepare_artifact.get("images_npy")
        prepare_metadata = prepare_artifact.get("metadata_csv")
        if prepare_images and prepare_metadata:
            return Path(prepare_images), Path(prepare_metadata)

    shared_dir = Path(cfg.paths.intermediate_dir)
    return (
        shared_dir / str(cfg.prepare.image_array_name),
        shared_dir / str(cfg.prepare.metadata_name),
    )


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
        "generate_representative_image": bool(
            _require_value(
                "analysis",
                "generate_representative_image",
                analysis_cfg.generate_representative_image,
            )
        ),
        "edge_threshold": float(
            _require_value("analysis", "edge_threshold", analysis_cfg.edge_threshold)
        ),
    }


def calculate_edge_density(image: np.ndarray, threshold: float) -> float:
    # Student task:
    # 1. Compute the absolute pixel-to-pixel difference across rows and columns.
    # 2. Count which differences are strictly greater than `threshold`.
    # 3. Return the fraction of edge locations that exceed the threshold.
    raise NotImplementedError(
        "Implement `calculate_edge_density()` in "
        "`src/nextgen2026_coding_bootcamp/steps/analyze.py`."
    )


def build_dataset_overview(images: np.ndarray, metadata: pd.DataFrame) -> dict:
    # Student task:
    # Build the JSON payload written to `dataset_overview.json`.
    # Required keys are listed in `DATASET_OVERVIEW_KEYS`.
    raise NotImplementedError(
        "Implement `build_dataset_overview()` in "
        "`src/nextgen2026_coding_bootcamp/steps/analyze.py`."
    )


def write_representative_image_montage(
    images: np.ndarray,
    metadata: pd.DataFrame,
    output_path: Path,
) -> None:
    # Student task:
    # Create a montage image with one representative digit per class and write it to
    # `output_path`. `matplotlib` is already available in the project dependencies.
    raise NotImplementedError(
        "Implement `write_representative_image_montage()` in "
        "`src/nextgen2026_coding_bootcamp/steps/analyze.py`."
    )


def build_class_image_summary(
    images: np.ndarray,
    metadata: pd.DataFrame,
    edge_threshold: float,
) -> pd.DataFrame:
    # Student task:
    # Return one row per label with the required columns in
    # `CLASS_IMAGE_SUMMARY_COLUMNS`.
    # Use `metadata['image_id']` to align rows with `images`.
    raise NotImplementedError(
        "Implement `build_class_image_summary()` in "
        "`src/nextgen2026_coding_bootcamp/steps/analyze.py`."
    )


def run_analyze(
    cfg,
    ctx=None,
    images_npy: Path | None = None,
    metadata_csv: Path | None = None,
) -> dict:
    prepared_images_npy, prepared_metadata_csv = _resolve_prepare_inputs(
        cfg=cfg,
        ctx=ctx,
        images_npy=images_npy,
        metadata_csv=metadata_csv,
    )
    analysis_cfg = _validate_analysis_config(cfg)

    shared_output_dir = Path(cfg.paths.results_dir)
    shared_output_dir.mkdir(parents=True, exist_ok=True)

    shared_dataset_overview_json = (
        shared_output_dir / analysis_cfg["dataset_overview_name"]
    )
    shared_class_image_summary_csv = (
        shared_output_dir / analysis_cfg["class_summary_name"]
    )
    shared_class_representatives_png = (
        shared_output_dir / analysis_cfg["representative_image_name"]
    )

    logger.info(
        "[analyze]\nanalyze:start images=%s metadata=%s",
        prepared_images_npy,
        prepared_metadata_csv,
    )

    # Student task:
    # Suggested shape for the implementation:
    #
    # images = np.load(prepared_images_npy)
    # metadata = pd.read_csv(prepared_metadata_csv)
    # overview = build_dataset_overview(images=images, metadata=metadata)
    # summary = build_class_image_summary(
    #     images=images,
    #     metadata=metadata,
    #     edge_threshold=analysis_cfg["edge_threshold"],
    # )
    # if analysis_cfg["generate_representative_image"]:
    #     write_representative_image_montage(...)
    # summary.to_csv(shared_class_image_summary_csv, index=False)
    #
    # If `ctx` is provided, copy shared outputs into `ctx.run_dir / "analyze"` using
    # `_copy_to_run`, then return the run-scoped paths. Otherwise return shared paths.
    #
    # Expected return keys:
    # - images_npy
    # - metadata_csv
    # - dataset_overview_json
    # - class_image_summary_csv
    # - class_representatives_png
    # - shared_dataset_overview_json
    # - shared_class_image_summary_csv
    # - shared_class_representatives_png
    # - expected_class_summary_columns
    # - edge_threshold
    # - copied_to_run
    raise NotImplementedError(
        "Student task: implement `run_analyze()` so the analyze stage reads "
        "`images.npy` and `metadata.csv`, writes `dataset_overview.json`, "
        "`class_image_summary.csv`, and `class_representatives.png`, then "
        "returns the artifact dictionary described in this file. Reference "
        "`src/nextgen2026_coding_bootcamp/steps/prepare.py`, "
        "`docs/01-project-brief.md`, and "
        "`docs/02-repo-workflow-and-missing-piece.md`."
    )
