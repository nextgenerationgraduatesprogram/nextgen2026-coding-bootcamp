from __future__ import annotations

from pathlib import Path

import pandas as pd

from nextgen2026_coding_bootcamp.runtime import create_run_context
from nextgen2026_coding_bootcamp.steps.fetch import run_fetch


def test_run_fetch_writes_shared_raw_artifact_without_context(workshop_cfg, make_raw_source_csv):
    source_csv = make_raw_source_csv(
        [
            {
                "dteday": "2024-04-05",
                "hr": 8,
                "cnt": 118,
                "season": "spring",
                "weathersit": "cloudy",
            },
            {
                "dteday": "2024-04-06",
                "hr": 12,
                "cnt": 110,
                "season": "spring",
                "weathersit": "cloudy",
            },
        ]
    )
    workshop_cfg.fetch.source_data_path = str(source_csv)

    artifacts = run_fetch(cfg=workshop_cfg)
    raw_path = Path(artifacts["raw_csv"])
    raw_table = pd.read_csv(raw_path)

    assert raw_path == Path(workshop_cfg.paths.raw_dir) / workshop_cfg.fetch.raw_artifact_name
    assert artifacts["copied_to_run"] is False
    assert artifacts["n_rows"] == 2
    assert artifacts["columns"] == ["dteday", "hr", "cnt", "season", "weathersit"]
    assert raw_table["cnt"].tolist() == [118, 110]

def test_run_fetch_copies_shared_raw_artifact_into_run_directory(workshop_cfg, make_raw_source_csv, tmp_path: Path):
    workshop_cfg.run.output_root = str(tmp_path / "runs")
    workshop_cfg.paths.raw_dir = str(tmp_path / "raw")
    source_csv = make_raw_source_csv(
        [
            {
                "dteday": "2024-04-04",
                "hr": 7,
                "cnt": 70,
                "season": "spring",
                "weathersit": "clear",
            }
        ]
    )
    workshop_cfg.fetch.source_data_path = str(source_csv)

    ctx = create_run_context(output_root=Path(workshop_cfg.run.output_root), run_name="fetch")
    artifacts = run_fetch(cfg=workshop_cfg, ctx=ctx)

    assert artifacts["copied_to_run"] is True
    assert Path(artifacts["raw_csv"]).parent == ctx.run_dir / "fetch"
    assert Path(artifacts["shared_raw_csv"]).exists()
    assert Path(artifacts["raw_csv"]).exists()
