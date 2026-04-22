from __future__ import annotations

from pathlib import Path

import pandas as pd

from nextgen2026_coding_bootcamp.steps.fetch import run_fetch
from nextgen2026_coding_bootcamp.steps.prepare import run_prepare


def test_fetch_writes_bike_demand_raw_csv_contract(workshop_cfg):
    fetch_artifacts = run_fetch(cfg=workshop_cfg)
    raw_path = Path(fetch_artifacts["raw_csv"])
    raw_table = pd.read_csv(raw_path)

    assert raw_path.exists()
    assert fetch_artifacts["dataset_name"] == "bike_rental_demand"
    assert fetch_artifacts["n_rows"] == 96
    assert fetch_artifacts["columns"] == ["dteday", "hr", "cnt", "season", "weathersit"]
    assert raw_table.shape == (96, 5)
    assert raw_table["dteday"].iloc[0] == "2024-04-04"
    assert raw_table["dteday"].iloc[-1] == "2024-04-07"
    assert sorted(raw_table["hr"].unique().tolist()) == list(range(24))


def test_prepare_writes_prepared_demand_contract(workshop_cfg):
    run_fetch(cfg=workshop_cfg)
    prepare_artifacts = run_prepare(cfg=workshop_cfg)

    prepared_path = Path(prepare_artifacts["prepared_csv"])
    prepared = pd.read_csv(prepared_path)

    assert prepared_path.exists()
    assert prepared.shape == (96, 6)
    assert list(prepared.columns) == [
        "timestamp",
        "demand",
        "hour",
        "day_type",
        "season",
        "weather",
    ]
    assert prepared["timestamp"].iloc[0] == "2024-04-04T00:00:00"
    assert prepared["timestamp"].iloc[-1] == "2024-04-07T23:00:00"
    assert prepared["timestamp"].tolist() == sorted(prepared["timestamp"].tolist())
    assert sorted(prepared["day_type"].unique().tolist()) == ["weekday", "weekend"]
    assert prepared["day_type"].value_counts().sort_index().to_dict() == {
        "weekday": 48,
        "weekend": 48,
    }
    assert sorted(prepared["hour"].unique().tolist()) == list(range(24))
