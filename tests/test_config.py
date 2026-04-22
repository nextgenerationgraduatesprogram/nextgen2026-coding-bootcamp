from __future__ import annotations

from pathlib import Path

from nextgen2026_coding_bootcamp.config import compose_config, load_config


def test_load_config_reads_yaml_and_applies_overrides(tmp_path: Path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "run:\n"
        "  output_root: runs\n"
        "fetch:\n"
        "  dataset_name: sklearn_digits\n"
    )

    cfg = load_config(
        config_path=config_path,
        overrides=["run.output_root=custom-runs", "fetch.dataset_name=patched_digits"],
    )

    assert cfg.run.output_root == "custom-runs"
    assert cfg.fetch.dataset_name == "patched_digits"


def test_compose_config_merges_parts_in_order_and_applies_overrides(tmp_path: Path):
    config_root = tmp_path / "configs"
    config_root.mkdir()
    (config_root / "base.yaml").write_text(
        "run:\n"
        "  output_root: runs\n"
        "report:\n"
        "  markdown_name: report.md\n"
    )
    (config_root / "profile.yaml").write_text(
        "run:\n"
        "  output_root: profiled-runs\n"
        "report:\n"
        "  include_representative_image: true\n"
    )

    cfg = compose_config(
        config_root=config_root,
        parts=["base.yaml", "profile.yaml"],
        overrides=["report.markdown_name=custom-report.md"],
    )

    assert cfg.run.output_root == "profiled-runs"
    assert cfg.report.markdown_name == "custom-report.md"
    assert cfg.report.include_representative_image is True
