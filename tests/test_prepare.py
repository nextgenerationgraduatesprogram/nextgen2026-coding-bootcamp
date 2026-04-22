from __future__ import annotations

from pathlib import Path

import pandas as pd

from nextgen2026_coding_bootcamp.runtime import create_run_context
from nextgen2026_coding_bootcamp.steps.prepare import _resolve_input_csv, run_prepare


def test_resolve_input_csv_prefers_explicit_input(workshop_cfg, tmp_path: Path):
    explicit_csv = tmp_path / "explicit.csv"
    explicit_csv.write_text("dteday,hr,cnt,season,weathersit\n2024-04-05,8,118,spring,cloudy\n")

    resolved = _resolve_input_csv(
        cfg=workshop_cfg,
        ctx=None,
        input_csv=explicit_csv,
    )

    assert resolved == explicit_csv


def test_run_prepare_writes_prepared_shared_artifact(workshop_cfg, make_raw_source_csv):
    raw_csv = make_raw_source_csv(
        [
            {
                "dteday": "2024-04-06",
                "hr": 9,
                "cnt": 50,
                "season": "spring",
                "weathersit": "cloudy",
            },
            {
                "dteday": "2024-04-05",
                "hr": 8,
                "cnt": 118,
                "season": "spring",
                "weathersit": "clear",
            },
        ]
    )

    artifacts = run_prepare(cfg=workshop_cfg, input_csv=raw_csv)
    prepared = pd.read_csv(artifacts["prepared_csv"])

    assert artifacts["copied_to_run"] is False
    assert prepared.to_dict(orient="records") == [
        {
            "timestamp": "2024-04-05T08:00:00",
            "demand": 118,
            "hour": 8,
            "day_type": "weekday",
            "season": "spring",
            "weather": "clear",
        },
        {
            "timestamp": "2024-04-06T09:00:00",
            "demand": 50,
            "hour": 9,
            "day_type": "weekend",
            "season": "spring",
            "weather": "cloudy",
        },
    ]


def test_run_prepare_copies_outputs_into_run_directory(workshop_cfg, make_raw_source_csv, tmp_path: Path):
    workshop_cfg.run.output_root = str(tmp_path / "runs")
    workshop_cfg.paths.intermediate_dir = str(tmp_path / "intermediate")
    raw_csv = make_raw_source_csv(
        [
            {
                "dteday": "2024-04-07",
                "hr": 14,
                "cnt": 112,
                "season": "spring",
                "weathersit": "light_rain",
            }
        ]
    )

    ctx = create_run_context(output_root=Path(workshop_cfg.run.output_root), run_name="prepare")
    artifacts = run_prepare(cfg=workshop_cfg, ctx=ctx, input_csv=raw_csv)

    assert artifacts["copied_to_run"] is True
    assert Path(artifacts["prepared_csv"]).parent == ctx.run_dir / "prepare"
