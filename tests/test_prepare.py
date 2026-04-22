from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from nextgen2026_coding_bootcamp.runtime import create_run_context
from nextgen2026_coding_bootcamp.steps.prepare import _resolve_input_npz, run_prepare


def test_resolve_input_npz_prefers_explicit_input(workshop_cfg, tmp_path: Path):
    explicit_npz = tmp_path / "explicit.npz"
    explicit_npz.write_bytes(b"npz")

    resolved = _resolve_input_npz(
        cfg=workshop_cfg,
        ctx=None,
        input_npz=explicit_npz,
    )

    assert resolved == explicit_npz


def test_run_prepare_writes_normalized_shared_artifacts(workshop_cfg, tmp_path: Path):
    raw_npz = tmp_path / "digits_raw.npz"
    np.savez_compressed(
        raw_npz,
        images=np.array([[[0.0, 16.0], [32.0, 8.0]]], dtype=np.float32),
        target=np.array([5], dtype=np.int64),
    )

    artifacts = run_prepare(cfg=workshop_cfg, input_npz=raw_npz)
    images = np.load(artifacts["images_npy"])
    metadata = pd.read_csv(artifacts["metadata_csv"])

    assert artifacts["copied_to_run"] is False
    assert images.tolist() == [[[0.0, 1.0], [1.0, 0.5]]]
    assert metadata.to_dict(orient="records") == [{"image_id": 0, "label": 5}]


def test_run_prepare_copies_outputs_into_run_directory(workshop_cfg, tmp_path: Path):
    workshop_cfg.run.output_root = str(tmp_path / "runs")
    workshop_cfg.paths.intermediate_dir = str(tmp_path / "intermediate")
    raw_npz = tmp_path / "digits_raw.npz"
    np.savez_compressed(
        raw_npz,
        images=np.array([[[0.0, 16.0], [8.0, 4.0]]], dtype=np.float32),
        target=np.array([2], dtype=np.int64),
    )

    ctx = create_run_context(output_root=Path(workshop_cfg.run.output_root), run_name="prepare")
    artifacts = run_prepare(cfg=workshop_cfg, ctx=ctx, input_npz=raw_npz)

    assert artifacts["copied_to_run"] is True
    assert Path(artifacts["images_npy"]).parent == ctx.run_dir / "prepare"
    assert Path(artifacts["metadata_csv"]).parent == ctx.run_dir / "prepare"
