from pathlib import Path
import shutil
from zipfile import ZipFile

from omegaconf import OmegaConf
import pytest

from nextgen2026_coding_bootcamp.runtime import create_run_context
from nextgen2026_coding_bootcamp.steps import fetch as fetch_module
from nextgen2026_coding_bootcamp.steps.fetch import run_fetch
from nextgen2026_coding_bootcamp.steps.prepare import run_prepare


def _make_fixture_zip(zip_path: Path) -> None:
    csv_content = (
        "instant,dteday,season,yr,mnth,hr,holiday,weekday,workingday,weathersit,temp,atemp,hum,windspeed,casual,registered,cnt\n"
        "1,2011-01-01,1,0,1,8,0,6,0,1,0.24,0.2879,0.81,0.0,3,13,16\n"
        "2,2011-01-03,2,0,1,9,0,1,1,2,0.22,0.2727,0.80,0.10,8,32,40\n"
    )
    with ZipFile(zip_path, "w") as zf:
        zf.writestr("hour.csv", csv_content)


def test_fetch_to_prepare_stage_handoff_uses_context_artifacts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    fixture_zip = tmp_path / "fixture.zip"
    _make_fixture_zip(fixture_zip)

    def fake_urlretrieve(url: str, destination: Path):
        shutil.copyfile(fixture_zip, destination)
        return str(destination), None

    monkeypatch.setattr(fetch_module, "urlretrieve", fake_urlretrieve)

    cfg = OmegaConf.create(
        {
            "run": {"output_root": str(tmp_path / "runs")},
            "paths": {
                "raw_dir": str(tmp_path / "raw"),
                "intermediate_dir": str(tmp_path / "intermediate"),
                "results_dir": str(tmp_path / "results"),
            },
            "fetch": {
                "source_url": "https://example.test/Bike-Sharing-Dataset.zip",
                "archive_member": "hour.csv",
            },
            "prepare": {
                "keep_holidays": True,
                "write_prepared_csv": True,
            },
        }
    )

    ctx = create_run_context(Path(cfg.run.output_root), run_name="handoff")

    ctx.artifacts["fetch"] = run_fetch(cfg=cfg, ctx=ctx)
    prepare_artifacts = run_prepare(cfg=cfg, ctx=ctx)

    fetch_csv_path = Path(ctx.artifacts["fetch"]["raw_csv"]).resolve()
    prepare_input_path = Path(prepare_artifacts["raw_csv"]).resolve()
    prepare_output_path = Path(prepare_artifacts["prepared_csv"]).resolve()

    assert fetch_csv_path == prepare_input_path
    assert prepare_output_path.exists()
    assert prepare_output_path.parent == (ctx.run_dir / "prepare").resolve()
