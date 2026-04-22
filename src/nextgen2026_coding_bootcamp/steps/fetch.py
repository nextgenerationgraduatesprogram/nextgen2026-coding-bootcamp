from __future__ import annotations

from pathlib import Path
import logging
import shutil

import numpy as np
from sklearn.datasets import load_digits

logger = logging.getLogger(__name__)


def _copy_to_run(shared_path: Path, run_path: Path) -> None:
    run_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(shared_path, run_path)


def run_fetch(cfg, ctx=None) -> dict:
    dataset_name = str(cfg.fetch.dataset_name)
    raw_artifact_name = str(cfg.fetch.raw_artifact_name)

    raw_dir = Path(cfg.paths.raw_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    shared_raw_npz = raw_dir / raw_artifact_name

    logger.info("[fetch]")
    logger.info("fetch:start dataset=%s shared_output=%s", dataset_name, shared_raw_npz)

    digits = load_digits()
    images = digits.images.astype(np.float32)
    targets = digits.target.astype(np.int64)
    target_names = np.asarray(digits.target_names, dtype=np.int64)
    flat_data = digits.data.astype(np.float32)

    np.savez_compressed(
        shared_raw_npz,
        images=images,
        target=targets,
        target_names=target_names,
        data=flat_data,
    )

    if ctx is None:
        output_raw_npz = shared_raw_npz
        copied_to_run = False
    else:
        run_stage_dir = ctx.run_dir / "fetch"
        run_stage_dir.mkdir(parents=True, exist_ok=True)
        output_raw_npz = run_stage_dir / raw_artifact_name
        _copy_to_run(shared_raw_npz, output_raw_npz)
        copied_to_run = True

    logger.info(
        "fetch:finish images=%d classes=%d image_shape=%s output=%s\n",
        images.shape[0],
        len(target_names),
        tuple(images.shape[1:]),
        output_raw_npz,
    )

    return {
        "dataset_name": dataset_name,
        "raw_npz": str(output_raw_npz),
        "shared_raw_npz": str(shared_raw_npz),
        "n_images": int(images.shape[0]),
        "n_classes": int(len(target_names)),
        "image_shape": list(images.shape[1:]),
        "copied_to_run": copied_to_run,
    }
