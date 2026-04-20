from pathlib import Path

from omegaconf import OmegaConf
import pandas as pd

from nextgen2026_coding_bootcamp.steps.analyze import run_analyze
from nextgen2026_coding_bootcamp.steps.report import run_report


def test_analyze_and_report_generate_expected_artifacts(tmp_path: Path):
    prepared_csv = tmp_path / "intermediate" / "hourly_bike_data.csv"
    prepared_csv.parent.mkdir(parents=True, exist_ok=True)
    prepared_csv.write_text(
        "date,hour,season,month,weekday,holiday,workingday,day_type,weather,temp_c,feels_like_c,humidity_pct,windspeed_kph,casual,registered,total_rentals\n"
        "2011-01-01,8,winter,1,6,0,0,non_working_day,clear,3.28,3.01,81.0,0.0,3,13,16\n"
        "2011-01-03,8,spring,1,1,0,1,working_day,mist_cloud,2.34,2.00,80.0,6.7,8,32,40\n"
        "2011-01-03,9,spring,1,1,0,1,working_day,mist_cloud,2.34,2.00,80.0,6.7,12,85,97\n"
    )

    cfg = OmegaConf.create(
        {
            "paths": {
                "intermediate_dir": str(tmp_path / "intermediate"),
                "results_dir": str(tmp_path / "results"),
            },
            "analysis": {"high_demand_quantile": 0.9},
            "report": {
                "write_plots": False,
                "write_summary_markdown": True,
            },
        }
    )

    analyze_artifacts = run_analyze(cfg=cfg)
    assert Path(analyze_artifacts["hourly_profile_csv"]).exists()
    assert Path(analyze_artifacts["high_demand_share_csv"]).exists()
    assert Path(analyze_artifacts["weather_summary_csv"]).exists()
    assert Path(analyze_artifacts["summary_json"]).exists()

    hourly_profile = pd.read_csv(analyze_artifacts["hourly_profile_csv"])
    assert {"hour", "day_type", "mean_rentals"}.issubset(set(hourly_profile.columns))

    report_artifacts = run_report(cfg=cfg)
    assert Path(report_artifacts["summary_markdown"]).exists()
    assert report_artifacts["figure_one_png"] is None
    assert report_artifacts["figure_two_png"] is None
