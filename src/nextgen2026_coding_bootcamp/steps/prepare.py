from __future__ import annotations

from pathlib import Path
import logging
import shutil

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def _resolve_input_npz(cfg, ctx=None, input_npz: Path | None = None) -> Path:
    if input_npz is not None:
        return input_npz

    if ctx is not None:
        fetch_artifact = ctx.artifacts.get("fetch", {})
        fetch_npz = fetch_artifact.get("raw_npz")
        if fetch_npz:
            return Path(fetch_npz)

    return Path(cfg.paths.raw_dir) / str(cfg.fetch.raw_artifact_name)


def _copy_to_run(shared_path: Path, run_path: Path) -> None:
    run_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(shared_path, run_path)


def run_prepare(cfg, ctx=None, input_npz: Path | None = None) -> dict:
    raw_npz = _resolve_input_npz(cfg=cfg, ctx=ctx, input_npz=input_npz)

    shared_output_dir = Path(cfg.paths.intermediate_dir)
    shared_output_dir.mkdir(parents=True, exist_ok=True)

    image_array_name = str(cfg.prepare.image_array_name)
    metadata_name = str(cfg.prepare.metadata_name)
    normalize_divisor = float(cfg.prepare.normalize_divisor)

    shared_images_npy = shared_output_dir / image_array_name
    shared_metadata_csv = shared_output_dir / metadata_name

    logger.info("[prepare]")
    logger.info("prepare:start input=%s", raw_npz)

    with np.load(raw_npz) as raw:
        images = raw["images"].astype(np.float32) / normalize_divisor
        labels = raw["target"].astype(np.int64)

    images = np.clip(images, 0.0, 1.0)

    metadata = pd.DataFrame(
        {
            "image_id": np.arange(len(labels), dtype=int),
            "label": labels.astype(int),
        }
    )

    np.save(shared_images_npy, images)
    metadata.to_csv(shared_metadata_csv, index=False)

    if ctx is None:
        output_images_npy = shared_images_npy
        output_metadata_csv = shared_metadata_csv
        copied_to_run = False
    else:
        run_stage_dir = ctx.run_dir / "prepare"
        run_stage_dir.mkdir(parents=True, exist_ok=True)
        output_images_npy = run_stage_dir / image_array_name
        output_metadata_csv = run_stage_dir / metadata_name
        _copy_to_run(shared_images_npy, output_images_npy)
        _copy_to_run(shared_metadata_csv, output_metadata_csv)
        copied_to_run = True

    logger.info(
        "prepare:finish images=%d image_shape=%s output_images=%s output_metadata=%s\n",
        images.shape[0],
        tuple(images.shape[1:]),
        output_images_npy,
        output_metadata_csv,
    )

    return {
        "raw_npz": str(raw_npz),
        "images_npy": str(output_images_npy),
        "metadata_csv": str(output_metadata_csv),
        "shared_images_npy": str(shared_images_npy),
        "shared_metadata_csv": str(shared_metadata_csv),
        "n_images": int(images.shape[0]),
        "image_shape": list(images.shape[1:]),
        "normalize_divisor": normalize_divisor,
        "copied_to_run": copied_to_run,
    }
