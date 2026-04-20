from pathlib import Path

from omegaconf import OmegaConf
import pandas as pd

from nextgen2026_coding_bootcamp.steps.prepare import PREPARED_COLUMNS, run_prepare

RAW_CSV = """instant,dteday,season,yr,mnth,hr,holiday,weekday,workingday,weathersit,temp,atemp,hum,windspeed,casual,registered,cnt
1,2011-01-01,1,0,1,8,1,6,0,1,0.24,0.2879,0.81,0.0,3,13,16
2,2011-01-03,2,0,1,9,0,1,1,2,0.22,0.2727,0.80,0.10,8,32,40
"""


def _write_raw_hour_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(RAW_CSV)


def _base_cfg(tmp_path: Path, keep_holidays: bool) -> object:
    return OmegaConf.create(
        {
            "paths": {
                "raw_dir": str(tmp_path / "raw"),
                "intermediate_dir": str(tmp_path / "intermediate"),
            },
            "fetch": {"archive_member": "hour.csv"},
            "prepare": {
                "keep_holidays": keep_holidays,
                "write_prepared_csv": True,
            },
        }
    )


def test_run_prepare_produces_notebook_equivalent_columns_and_transforms(tmp_path: Path):
    cfg = _base_cfg(tmp_path=tmp_path, keep_holidays=True)
    _write_raw_hour_csv(Path(cfg.paths.raw_dir) / "hour.csv")

    artifacts = run_prepare(cfg=cfg)
    prepared_path = Path(artifacts["prepared_csv"])
    prepared = pd.read_csv(prepared_path)

    assert list(prepared.columns) == PREPARED_COLUMNS
    assert len(prepared) == 2
    assert prepared.loc[0, "season"] == "winter"
    assert prepared.loc[1, "season"] == "spring"
    assert prepared.loc[0, "day_type"] == "non_working_day"
    assert prepared.loc[1, "day_type"] == "working_day"
    assert abs(prepared.loc[0, "temp_c"] - 3.28) < 1e-6
    assert abs(prepared.loc[1, "windspeed_kph"] - 6.7) < 1e-6


def test_run_prepare_can_drop_holiday_rows(tmp_path: Path):
    cfg = _base_cfg(tmp_path=tmp_path, keep_holidays=False)
    _write_raw_hour_csv(Path(cfg.paths.raw_dir) / "hour.csv")

    artifacts = run_prepare(cfg=cfg)
    prepared = pd.read_csv(Path(artifacts["prepared_csv"]))

    assert len(prepared) == 1
    assert int(prepared.iloc[0]["holiday"]) == 0
