from __future__ import annotations

from pathlib import Path

import pandas as pd

from nextgen2026_coding_bootcamp.runtime import create_run_context
from nextgen2026_coding_bootcamp.steps.prepare import _resolve_input_tsv, run_prepare


def test_resolve_input_tsv_prefers_explicit_input(workshop_cfg, tmp_path: Path):
    explicit_tsv = tmp_path / "explicit.tsv"
    explicit_tsv.write_text("ham\tHello there\n", encoding="utf-8")

    resolved = _resolve_input_tsv(
        cfg=workshop_cfg,
        ctx=None,
        input_tsv=explicit_tsv,
    )

    assert resolved == explicit_tsv


def test_run_prepare_writes_clean_shared_artifacts(workshop_cfg, tmp_path: Path):
    raw_tsv = tmp_path / "messages.tsv"
    raw_tsv.write_text(
        "ham\t See you soon \n"
        "spam\tWIN cash now\n"
        "maybe\tignore me\n"
        "ham\t   \n",
        encoding="utf-8",
    )

    artifacts = run_prepare(cfg=workshop_cfg, input_tsv=raw_tsv)
    prepared_messages = pd.read_csv(artifacts["prepared_messages_csv"])

    assert artifacts["copied_to_run"] is False
    assert prepared_messages.to_dict(orient="records") == [
        {"message_id": 0, "label": "ham", "text": "See you soon"},
        {"message_id": 1, "label": "spam", "text": "WIN cash now"},
    ]


def test_run_prepare_copies_outputs_into_run_directory(workshop_cfg, tmp_path: Path):
    workshop_cfg.run.output_root = str(tmp_path / "runs")
    workshop_cfg.paths.intermediate_dir = str(tmp_path / "intermediate")
    raw_tsv = tmp_path / "messages.tsv"
    raw_tsv.write_text("ham\tReady to test\nspam\tClaim now\n", encoding="utf-8")

    ctx = create_run_context(output_root=Path(workshop_cfg.run.output_root), run_name="prepare")
    artifacts = run_prepare(cfg=workshop_cfg, ctx=ctx, input_tsv=raw_tsv)

    assert artifacts["copied_to_run"] is True
    assert Path(artifacts["prepared_messages_csv"]).parent == ctx.run_dir / "prepare"
