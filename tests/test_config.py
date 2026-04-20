from pathlib import Path

from nextgen2026_coding_bootcamp.config import compose_config, load_config


def test_load_config_applies_dotlist_overrides(tmp_path: Path):
    cfg_path = tmp_path / "analyze.yaml"
    cfg_path.write_text("analysis:\n  high_demand_quantile: 0.9\n")

    cfg = load_config(cfg_path, overrides=["analysis.high_demand_quantile=0.85"])

    assert float(cfg.analysis.high_demand_quantile) == 0.85


def test_compose_config_honors_merge_order_and_overrides(tmp_path: Path):
    (tmp_path / "paths.yaml").write_text("paths:\n  raw_dir: data/raw\n")
    (tmp_path / "stages").mkdir(parents=True, exist_ok=True)
    (tmp_path / "stages" / "prepare.yaml").write_text(
        "prepare:\n  keep_holidays: true\n  write_prepared_csv: true\n"
    )
    (tmp_path / "profiles").mkdir(parents=True, exist_ok=True)
    (tmp_path / "profiles" / "fast.yaml").write_text("prepare:\n  keep_holidays: false\n")

    cfg = compose_config(
        config_root=tmp_path,
        parts=["paths.yaml", "stages/prepare.yaml", "profiles/fast.yaml"],
        overrides=["prepare.write_prepared_csv=false"],
    )

    assert str(cfg.paths.raw_dir) == "data/raw"
    assert bool(cfg.prepare.keep_holidays) is False
    assert bool(cfg.prepare.write_prepared_csv) is False
