from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from nextgen2026_coding_bootcamp.steps.fetch import run_fetch
from nextgen2026_coding_bootcamp.steps.prepare import run_prepare


def test_fetch_writes_digits_raw_npz_contract(workshop_cfg):
    fetch_artifacts = run_fetch(cfg=workshop_cfg)
    raw_path = Path(fetch_artifacts["raw_npz"])

    assert raw_path.exists()
    assert fetch_artifacts["dataset_name"] == "sklearn_digits"
    assert fetch_artifacts["n_images"] == 1797
    assert fetch_artifacts["n_classes"] == 10
    assert fetch_artifacts["image_shape"] == [8, 8]

    with np.load(raw_path) as raw_payload:
        assert set(raw_payload.files) == {"images", "target", "target_names", "data"}
        assert raw_payload["images"].shape == (1797, 8, 8)
        assert raw_payload["target"].shape == (1797,)
        assert raw_payload["target_names"].tolist() == list(range(10))
        assert raw_payload["data"].shape == (1797, 64)


def test_prepare_writes_normalized_images_and_metadata_contract(workshop_cfg):
    run_fetch(cfg=workshop_cfg)
    prepare_artifacts = run_prepare(cfg=workshop_cfg)

    images_path = Path(prepare_artifacts["images_npy"])
    metadata_path = Path(prepare_artifacts["metadata_csv"])
    images = np.load(images_path)
    metadata = pd.read_csv(metadata_path)

    assert images_path.exists()
    assert metadata_path.exists()
    assert images.shape == (1797, 8, 8)
    assert metadata.shape == (1797, 2)
    assert list(metadata.columns) == ["image_id", "label"]
    assert metadata["image_id"].tolist() == list(range(1797))
    assert sorted(metadata["label"].unique().tolist()) == list(range(10))
    assert float(images.min()) >= 0.0
    assert float(images.max()) <= 1.0
