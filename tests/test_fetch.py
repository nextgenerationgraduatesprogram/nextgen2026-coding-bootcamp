from __future__ import annotations

from pathlib import Path

import numpy as np

from nextgen2026_coding_bootcamp.runtime import create_run_context
from nextgen2026_coding_bootcamp.steps.fetch import run_fetch


def test_run_fetch_writes_shared_raw_artifact_without_context(workshop_cfg, synthetic_digits_dataset, monkeypatch):
    monkeypatch.setattr(
        "nextgen2026_coding_bootcamp.steps.fetch.load_digits",
        lambda: synthetic_digits_dataset,
    )

    artifacts = run_fetch(cfg=workshop_cfg)
    raw_path = Path(artifacts["raw_npz"])

    assert raw_path == Path(workshop_cfg.paths.raw_dir) / workshop_cfg.fetch.raw_artifact_name
    assert artifacts["copied_to_run"] is False

    with np.load(raw_path) as raw_payload:
        assert raw_payload["images"].shape == (2, 2, 2)
        assert raw_payload["target"].tolist() == [3, 7]
        assert raw_payload["data"].shape == (2, 4)


def test_run_fetch_copies_shared_raw_artifact_into_run_directory(workshop_cfg, synthetic_digits_dataset, monkeypatch, tmp_path: Path):
    workshop_cfg.run.output_root = str(tmp_path / "runs")
    workshop_cfg.paths.raw_dir = str(tmp_path / "raw")
    monkeypatch.setattr(
        "nextgen2026_coding_bootcamp.steps.fetch.load_digits",
        lambda: synthetic_digits_dataset,
    )

    ctx = create_run_context(output_root=Path(workshop_cfg.run.output_root), run_name="fetch")
    artifacts = run_fetch(cfg=workshop_cfg, ctx=ctx)

    assert artifacts["copied_to_run"] is True
    assert Path(artifacts["raw_npz"]).parent == ctx.run_dir / "fetch"
    assert Path(artifacts["shared_raw_npz"]).exists()
    assert Path(artifacts["raw_npz"]).exists()
