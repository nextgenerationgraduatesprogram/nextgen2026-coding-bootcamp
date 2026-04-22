from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from nextgen2026_coding_bootcamp.runtime import create_run_context
from nextgen2026_coding_bootcamp.steps.fetch import run_fetch


def test_run_fetch_downloads_source_csv_when_cache_is_missing(
    workshop_cfg,
    synthetic_bike_archive_bytes,
    tmp_path: Path,
):
    workshop_cfg.paths.raw_dir = str(tmp_path / "raw")
    workshop_cfg.fetch.source_data_path = str(tmp_path / "data" / "source" / "bike_demand_source.csv")
    requested_urls: list[str] = []

    def fake_source_downloader(source_url: str) -> bytes:
        requested_urls.append(source_url)
        return synthetic_bike_archive_bytes

    artifacts = run_fetch(cfg=workshop_cfg, source_downloader=fake_source_downloader)
    raw_path = Path(artifacts["raw_csv"])
    raw_table = pd.read_csv(raw_path)

    assert raw_path == Path(workshop_cfg.paths.raw_dir) / workshop_cfg.fetch.raw_artifact_name
    assert Path(workshop_cfg.fetch.source_data_path).exists()
    assert artifacts["downloaded"] is True
    assert artifacts["copied_to_run"] is False
    assert artifacts["n_rows"] == 96
    assert artifacts["columns"] == ["dteday", "hr", "cnt", "season", "weathersit"]
    assert raw_table.shape == (96, 5)
    assert raw_table["dteday"].iloc[0] == "2024-04-04"
    assert raw_table["dteday"].iloc[-1] == "2024-04-07"
    assert raw_table["season"].iloc[0] == "spring"
    assert sorted(raw_table["hr"].unique().tolist()) == list(range(24))
    assert requested_urls == [workshop_cfg.fetch.source_url]


def test_run_fetch_reuses_cached_source_csv_without_downloading(workshop_cfg, make_raw_source_csv):
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

    artifacts = run_fetch(
        cfg=workshop_cfg,
        source_downloader=lambda *_: (_ for _ in ()).throw(AssertionError("unexpected download")),
    )

    raw_path = Path(artifacts["raw_csv"])
    raw_table = pd.read_csv(raw_path)

    assert artifacts["downloaded"] is False
    assert artifacts["copied_to_run"] is False
    assert artifacts["n_rows"] == 2
    assert raw_table["cnt"].tolist() == [118, 110]


def test_run_fetch_copies_shared_raw_artifact_into_run_directory(
    workshop_cfg,
    make_raw_source_csv,
    tmp_path: Path,
):
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


def test_run_fetch_rejects_non_http_source_url(workshop_cfg):
    workshop_cfg.fetch.source_url = "file:///tmp/bike.csv"

    with pytest.raises(ValueError, match="HTTP\\(S\\) URL"):
        run_fetch(cfg=workshop_cfg)


def test_run_fetch_rejects_malformed_downloaded_csv(workshop_cfg, tmp_path: Path):
    workshop_cfg.fetch.source_data_path = str(tmp_path / "data" / "source" / "bike_demand_source.csv")

    with pytest.raises(ValueError, match="missing required columns"):
        run_fetch(
            cfg=workshop_cfg,
            source_downloader=lambda *_: b"dteday,hr,cnt\n2024-04-04,0,12\n",
        )
