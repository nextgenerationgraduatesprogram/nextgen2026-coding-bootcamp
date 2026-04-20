from pathlib import Path
import json

from omegaconf import OmegaConf
import pandas as pd

from nextgen2026_coding_bootcamp.steps.analyze import run_analyze


KNOWN_PREPARED_CSV = (
    "date,hour,season,month,weekday,holiday,workingday,day_type,weather,temp_c,feels_like_c,humidity_pct,windspeed_kph,casual,registered,total_rentals\n"
    "2011-01-01,8,winter,1,6,0,1,working_day,clear,0.0,0.0,80.0,0.0,1,9,10\n"
    "2011-01-01,8,winter,1,6,0,0,non_working_day,clear,0.0,0.0,80.0,0.0,2,18,20\n"
    "2011-01-02,9,winter,1,0,0,1,working_day,mist_cloud,0.0,0.0,80.0,0.0,3,27,30\n"
    "2011-01-02,9,winter,1,0,0,0,non_working_day,mist_cloud,0.0,0.0,80.0,0.0,5,45,50\n"
)


def test_analyze_known_answer_outputs_match_expected_values(tmp_path: Path):
    input_csv = tmp_path / "intermediate" / "hourly_bike_data.csv"
    input_csv.parent.mkdir(parents=True, exist_ok=True)
    input_csv.write_text(KNOWN_PREPARED_CSV)

    cfg = OmegaConf.create(
        {
            "paths": {
                "intermediate_dir": str(input_csv.parent),
                "results_dir": str(tmp_path / "results"),
            },
            "analysis": {"high_demand_quantile": 0.5},
        }
    )

    artifacts = run_analyze(cfg=cfg)

    summary = json.loads(Path(artifacts["summary_json"]).read_text())
    assert summary["high_demand_quantile"] == 0.5
    assert summary["high_demand_threshold"] == 25.0
    assert summary["rows_in"] == 4
    assert summary["rows_high_demand"] == 2

    high_demand_share = pd.read_csv(artifacts["high_demand_share_csv"]).sort_values("hour")
    assert high_demand_share["hour"].tolist() == [8, 9]
    assert high_demand_share["high_demand_share"].tolist() == [0.0, 1.0]

    weather_summary = pd.read_csv(artifacts["weather_summary_csv"])
    assert weather_summary.loc[0, "weather"] == "mist_cloud"
    assert weather_summary.loc[0, "mean_rentals"] == 40.0
    assert weather_summary.loc[0, "observations"] == 2
