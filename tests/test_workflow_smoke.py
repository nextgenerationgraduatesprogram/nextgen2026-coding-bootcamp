from pathlib import Path
import shutil
from zipfile import ZipFile

from omegaconf import OmegaConf
import pytest

from nextgen2026_coding_bootcamp.manifests import write_manifest
from nextgen2026_coding_bootcamp.runtime import create_run_context, configure_logging
from nextgen2026_coding_bootcamp.steps import fetch as fetch_module
from nextgen2026_coding_bootcamp.workflow import run_workflow


def _make_fixture_zip(zip_path: Path) -> None:
    csv_content = (
        "instant,dteday,season,yr,mnth,hr,holiday,weekday,workingday,weathersit,temp,atemp,hum,windspeed,casual,registered,cnt\n"
        "1,2011-01-01,1,0,1,8,0,6,0,1,0.24,0.2879,0.81,0.0,3,13,16\n"
        "2,2011-01-03,2,0,1,9,0,1,1,2,0.22,0.2727,0.80,0.10,8,32,40\n"
    )
    with ZipFile(zip_path, "w") as zf:
        zf.writestr("hour.csv", csv_content)


def test_workflow_smoke_runs_with_fetch_prepare_and_stub_stages(
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
            "analysis": {"high_demand_quantile": 0.9},
            "report": {
                "write_plots": False,
                "write_summary_markdown": True,
            },
        }
    )

    ctx = create_run_context(Path(cfg.run.output_root), run_name="smoke")
    configure_logging(ctx.run_dir / "run.log")
    OmegaConf.save(config=cfg, f=ctx.run_dir / "config.yaml")

    run_workflow(cfg=cfg, ctx=ctx)
    write_manifest(ctx=ctx)

    assert (ctx.run_dir / "config.yaml").exists()
    assert (ctx.run_dir / "run.log").exists()
    assert (ctx.run_dir / "manifest.json").exists()

    assert Path(ctx.artifacts["fetch"]["raw_csv"]).exists()
    assert Path(ctx.artifacts["fetch"]["cache_archive_path"]).exists()
    assert Path(ctx.artifacts["fetch"]["cache_raw_csv"]).exists()
    assert Path(ctx.artifacts["prepare"]["prepared_csv"]).exists()
    assert Path(ctx.artifacts["analyze"]["hourly_profile_csv"]).exists()
    assert Path(ctx.artifacts["analyze"]["high_demand_share_csv"]).exists()
    assert Path(ctx.artifacts["analyze"]["weather_summary_csv"]).exists()
    assert Path(ctx.artifacts["analyze"]["summary_json"]).exists()
    assert Path(ctx.artifacts["report"]["summary_markdown"]).exists()
    assert ctx.artifacts["report"]["figure_one_png"] is None
    assert ctx.artifacts["report"]["figure_two_png"] is None
