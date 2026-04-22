from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

from omegaconf import OmegaConf
import numpy as np
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
def workshop_cfg(tmp_path: Path):
    return OmegaConf.create(
        {
            "run": {"output_root": str(tmp_path / "runs")},
            "paths": {
                "raw_dir": str(tmp_path / "data" / "raw"),
                "intermediate_dir": str(tmp_path / "data" / "intermediate"),
                "results_dir": str(tmp_path / "results"),
            },
            "fetch": {
                "dataset_name": "sklearn_digits",
                "raw_artifact_name": "digits_raw.npz",
            },
            "prepare": {
                "image_array_name": "images.npy",
                "metadata_name": "metadata.csv",
                "normalize_divisor": 16.0,
            },
            "analysis": {
                "dataset_overview_name": "dataset_overview.json",
                "class_summary_name": "class_image_summary.csv",
                "representative_image_name": "class_representatives.png",
                "generate_representative_image": True,
                "edge_threshold": 0.2,
            },
            "report": {
                "markdown_name": "report.md",
                "include_representative_image": True,
            },
            "profile": {"name": "test"},
        }
    )


@pytest.fixture()
def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


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
def synthetic_summary_inputs():
    images = np.array(
        [
            [[0.0, 0.0], [0.0, 0.0]],
            [[0.0, 1.0], [0.0, 1.0]],
            [[1.0, 1.0], [1.0, 1.0]],
        ],
        dtype=np.float32,
    )
    metadata = pd.DataFrame(
        {
            "image_id": [0, 1, 2],
            "label": [0, 0, 1],
        }
    )
    return {
        "images": images,
        "metadata": metadata,
    }


@pytest.fixture()
def synthetic_digits_dataset():
    return SimpleNamespace(
        images=np.array(
            [
                [[0.0, 1.0], [2.0, 3.0]],
                [[4.0, 5.0], [6.0, 7.0]],
            ],
            dtype=np.float32,
        ),
        target=np.array([3, 7], dtype=np.int64),
        target_names=np.arange(10, dtype=np.int64),
        data=np.array(
            [
                [0.0, 1.0, 2.0, 3.0],
                [4.0, 5.0, 6.0, 7.0],
            ],
            dtype=np.float32,
        ),
    )
