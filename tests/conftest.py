from __future__ import annotations

from dataclasses import dataclass
import io
from pathlib import Path
import subprocess
import sys
import zipfile

from omegaconf import OmegaConf
import pandas as pd
import pytest


@dataclass(frozen=True)
class ScratchPaths:
    root: Path
    raw_dir: Path
    intermediate_dir: Path
    results_dir: Path
    runs_dir: Path

    def dotlist_overrides(self) -> list[str]:
        return [
            f"run.output_root={self.runs_dir}",
            f"paths.raw_dir={self.raw_dir}",
            f"paths.intermediate_dir={self.intermediate_dir}",
            f"paths.results_dir={self.results_dir}",
        ]

    def latest_run(self) -> Path:
        run_dirs = sorted(self.runs_dir.glob("*"), key=lambda path: path.stat().st_mtime)
        if not run_dirs:
            raise AssertionError("No run directories were created")
        return run_dirs[-1]


@pytest.fixture()
def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


@pytest.fixture()
def source_dataset_path(repo_root: Path) -> Path:
    return repo_root / "tests" / "fixtures" / "bike_demand_source.csv"


@pytest.fixture()
def workshop_cfg(tmp_path: Path, source_dataset_path: Path):
    return OmegaConf.create(
        {
            "run": {"output_root": str(tmp_path / "runs")},
            "paths": {
                "raw_dir": str(tmp_path / "data" / "raw"),
                "intermediate_dir": str(tmp_path / "data" / "intermediate"),
                "results_dir": str(tmp_path / "results"),
            },
            "fetch": {
                "dataset_name": "bike_rental_demand",
                "raw_artifact_name": "bike_demand_raw.csv",
                "source_data_path": str(source_dataset_path),
                "source_url": "https://archive.ics.uci.edu/ml/machine-learning-databases/00275/Bike-Sharing-Dataset.zip",
            },
            "prepare": {
                "prepared_table_name": "prepared_demand.csv",
            },
            "analysis": {
                "dataset_overview_name": "dataset_overview.json",
                "hourly_profile_name": "hourly_demand_profile.csv",
                "daily_cycle_plot_name": "weekday_weekend_daily_cycle.png",
                "generate_daily_cycle_plot": True,
            },
            "report": {
                "markdown_name": "report.md",
                "include_daily_cycle_plot": True,
            },
            "profile": {"name": "test"},
        }
    )


@pytest.fixture()
def scratch_paths(tmp_path: Path) -> ScratchPaths:
    return ScratchPaths(
        root=tmp_path,
        raw_dir=tmp_path / "raw",
        intermediate_dir=tmp_path / "intermediate",
        results_dir=tmp_path / "results",
        runs_dir=tmp_path / "runs",
    )


@pytest.fixture()
def run_cli(repo_root: Path):
    def _run_cli(script_path: str, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, script_path, *args],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )

    return _run_cli


@pytest.fixture()
def make_raw_source_csv(tmp_path: Path):
    def _make(rows: list[dict], name: str = "bike_source.csv") -> Path:
        csv_path = tmp_path / name
        pd.DataFrame(rows).to_csv(csv_path, index=False)
        return csv_path

    return _make


@pytest.fixture()
def synthetic_bike_archive_bytes() -> bytes:
    rows: list[dict[str, int]] = []
    for day in range(5):
        for hour in range(24):
            rows.append(
                {
                    "dteday": f"2011-01-{day + 1:02d}",
                    "hr": hour,
                    "cnt": 25 + day * 10 + hour,
                    "season": 1,
                    "weathersit": 1 + int(8 <= hour < 18),
                }
            )

    hour_csv = io.StringIO()
    pd.DataFrame(rows).to_csv(hour_csv, index=False)

    archive_buffer = io.BytesIO()
    with zipfile.ZipFile(archive_buffer, mode="w") as archive:
        archive.writestr("Bike-Sharing-Dataset/hour.csv", hour_csv.getvalue())

    return archive_buffer.getvalue()
