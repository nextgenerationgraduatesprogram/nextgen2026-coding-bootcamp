from __future__ import annotations

import os
from pathlib import Path

from nextgen2026_coding_bootcamp import config as config_module
from nextgen2026_coding_bootcamp.config import compose_config, load_config


def test_load_config_reads_yaml_and_applies_overrides(tmp_path: Path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "run:\n"
        "  output_root: runs\n"
        "fetch:\n"
        "  dataset_name: sms_spam_collection\n"
    )

    cfg = load_config(
        config_path=config_path,
        overrides=["run.output_root=custom-runs", "fetch.dataset_name=patched_sms"],
    )

    assert cfg.run.output_root == "custom-runs"
    assert cfg.fetch.dataset_name == "patched_sms"


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
        "  max_examples: 5\n"
    )

    cfg = compose_config(
        config_root=config_root,
        parts=["base.yaml", "profile.yaml"],
        overrides=["report.markdown_name=custom-report.md"],
    )

    assert cfg.run.output_root == "profiled-runs"
    assert cfg.report.markdown_name == "custom-report.md"
    assert cfg.report.max_examples == 5


def test_load_config_loads_repo_dotenv_before_resolving_values(tmp_path: Path, monkeypatch):
    config_path = tmp_path / "config.yaml"
    dotenv_path = tmp_path / ".env"
    config_path.write_text(
        "analysis:\n"
        "  api_key_copy: ${oc.env:OPENAI_API_KEY}\n"
    )
    dotenv_path.write_text("OPENAI_API_KEY=test-key-from-dotenv\n", encoding="utf-8")

    monkeypatch.setattr(config_module, "REPO_ROOT", tmp_path)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    cfg = load_config(config_path=config_path)

    assert cfg.analysis.api_key_copy == "test-key-from-dotenv"


def test_repo_dotenv_does_not_override_existing_environment(tmp_path: Path, monkeypatch):
    dotenv_path = tmp_path / ".env"
    dotenv_path.write_text("OPENAI_API_KEY=dotenv-value\n", encoding="utf-8")

    monkeypatch.setattr(config_module, "REPO_ROOT", tmp_path)
    monkeypatch.setenv("OPENAI_API_KEY", "existing-shell-value")

    config_module._load_repo_dotenv()

    assert os.environ["OPENAI_API_KEY"] == "existing-shell-value"
