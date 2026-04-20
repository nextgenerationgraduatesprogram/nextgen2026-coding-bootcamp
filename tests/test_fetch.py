from pathlib import Path
import shutil
from zipfile import ZipFile

from omegaconf import OmegaConf
import pytest

from nextgen2026_coding_bootcamp.steps import fetch as fetch_module
from nextgen2026_coding_bootcamp.steps.fetch import run_fetch


def _make_fixture_zip(zip_path: Path, csv_content: str) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(zip_path, "w") as zf:
        zf.writestr("hour.csv", csv_content)


def test_run_fetch_downloads_and_extracts_archive_member(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    fixture_zip = tmp_path / "fixture.zip"
    _make_fixture_zip(fixture_zip, "a,b\n1,2\n")

    def fake_urlretrieve(url: str, destination: Path):
        shutil.copyfile(fixture_zip, destination)
        return str(destination), None

    monkeypatch.setattr(fetch_module, "urlretrieve", fake_urlretrieve)

    cfg = OmegaConf.create(
        {
            "paths": {"raw_dir": str(tmp_path / "raw")},
            "fetch": {
                "source_url": "https://example.test/Bike-Sharing-Dataset.zip",
                "archive_member": "hour.csv",
            },
        }
    )

    artifacts = run_fetch(cfg=cfg)

    archive_path = Path(artifacts["archive_path"])
    extracted_csv = Path(artifacts["raw_csv"])

    assert archive_path.exists()
    assert extracted_csv.exists()
    assert extracted_csv.read_text() == "a,b\n1,2\n"
    assert artifacts["downloaded_archive"] is True
    assert artifacts["extracted_member"] is True


def test_run_fetch_reuses_cached_copy_without_redownloading(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    fixture_zip = tmp_path / "fixture.zip"
    _make_fixture_zip(fixture_zip, "a,b\n1,2\n")

    download_calls = {"count": 0}

    def fake_urlretrieve(url: str, destination: Path):
        download_calls["count"] += 1
        shutil.copyfile(fixture_zip, destination)
        return str(destination), None

    monkeypatch.setattr(fetch_module, "urlretrieve", fake_urlretrieve)

    cfg = OmegaConf.create(
        {
            "paths": {"raw_dir": str(tmp_path / "raw")},
            "fetch": {
                "source_url": "https://example.test/Bike-Sharing-Dataset.zip",
                "archive_member": "hour.csv",
            },
        }
    )

    first = run_fetch(cfg=cfg)
    second = run_fetch(cfg=cfg)

    assert download_calls["count"] == 1
    assert first["downloaded_archive"] is True
    assert second["downloaded_archive"] is False
    assert second["extracted_member"] is False


def test_run_fetch_rejects_non_http_source_url(tmp_path: Path):
    cfg = OmegaConf.create(
        {
            "paths": {"raw_dir": str(tmp_path / "raw")},
            "fetch": {
                "source_url": "file:///tmp/local.zip",
                "archive_member": "hour.csv",
            },
        }
    )

    with pytest.raises(ValueError, match=r"HTTP\(S\) URL"):
        run_fetch(cfg=cfg)
