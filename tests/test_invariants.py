from pathlib import Path

from omegaconf import OmegaConf
import pandas as pd

from nextgen2026_coding_bootcamp.steps.prepare import PREPARED_COLUMNS, run_prepare


RAW_CSV_FOR_INVARIANTS = (
    "instant,dteday,season,yr,mnth,hr,holiday,weekday,workingday,weathersit,temp,atemp,hum,windspeed,casual,registered,cnt\n"
    "1,2011-01-01,1,0,1,0,0,6,0,1,0.24,0.2879,0.81,0.0,3,13,16\n"
    "2,2011-01-02,2,0,1,23,0,0,1,2,0.22,0.2727,0.80,0.10,8,32,40\n"
)


def test_prepare_output_invariants_hold_on_valid_input(tmp_path: Path):
    raw_csv_path = tmp_path / "raw" / "hour.csv"
    raw_csv_path.parent.mkdir(parents=True, exist_ok=True)
    raw_csv_path.write_text(RAW_CSV_FOR_INVARIANTS)

    cfg = OmegaConf.create(
        {
            "paths": {
                "raw_dir": str(raw_csv_path.parent),
                "intermediate_dir": str(tmp_path / "intermediate"),
            },
            "fetch": {"archive_member": "hour.csv"},
            "prepare": {
                "keep_holidays": True,
                "write_prepared_csv": True,
            },
        }
    )

    artifacts = run_prepare(cfg=cfg)
    prepared = pd.read_csv(artifacts["prepared_csv"])

    assert list(prepared.columns) == PREPARED_COLUMNS
    assert prepared["total_rentals"].ge(0).all()
    assert prepared["hour"].between(0, 23).all()
    assert prepared["day_type"].isin(["working_day", "non_working_day"]).all()
    assert len(prepared) == artifacts["rows_out"]
