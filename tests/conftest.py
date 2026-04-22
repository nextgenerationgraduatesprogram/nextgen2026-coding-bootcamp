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
                "dataset_name": "sms_spam_collection",
                "uci_dataset_id": 228,
                "raw_artifact_name": "sms_spam_collection.tsv",
                "force_download": False,
            },
            "prepare": {
                "prepared_messages_name": "prepared_messages.csv",
            },
            "analysis": {
                "predictions_name": "message_predictions.csv",
                "evaluation_summary_name": "evaluation_summary.json",
                "sample_size": 25,
                "sample_seed": 2026,
                "model": "test-model",
                "temperature": 0.0,
            },
            "report": {
                "markdown_name": "report.md",
                "max_examples": 10,
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
def synthetic_message_rows():
    return pd.DataFrame(
        {
            "message_id": [0, 1, 2],
            "label": ["ham", "spam", "ham"],
            "text": [
                "See you at noon",
                "WIN cash now",
                "The server restart worked",
            ],
        }
    )


@pytest.fixture()
def synthetic_sms_archive_bytes():
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode="w") as archive:
        archive.writestr(
            "SMSSpamCollection",
            "ham\tSee you at noon\n"
            "spam\tWIN cash now\n"
            "ham\t The server restart worked \n"
            "spam\tClaim your prize today\n",
        )
    return buffer.getvalue()
