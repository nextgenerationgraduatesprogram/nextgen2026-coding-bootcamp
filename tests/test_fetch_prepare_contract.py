from __future__ import annotations

from pathlib import Path

import pandas as pd

from nextgen2026_coding_bootcamp.steps.fetch import run_fetch
from nextgen2026_coding_bootcamp.steps.prepare import run_prepare


def test_fetch_writes_sms_raw_tsv_contract(workshop_cfg, synthetic_sms_archive_bytes):
    fetch_artifacts = run_fetch(
        cfg=workshop_cfg,
        archive_downloader=lambda archive_url: synthetic_sms_archive_bytes,
    )
    raw_path = Path(fetch_artifacts["raw_tsv"])

    assert raw_path.exists()
    assert fetch_artifacts["dataset_name"] == "sms_spam_collection"
    assert fetch_artifacts["n_messages"] == 4
    assert fetch_artifacts["labels"] == ["ham", "spam"]
    first_line = raw_path.read_text(encoding="utf-8").splitlines()[0]
    assert first_line.startswith(("ham\t", "spam\t"))


def test_prepare_writes_prepared_messages_contract(workshop_cfg, synthetic_sms_archive_bytes):
    run_fetch(cfg=workshop_cfg, archive_downloader=lambda archive_url: synthetic_sms_archive_bytes)
    prepare_artifacts = run_prepare(cfg=workshop_cfg)

    messages_path = Path(prepare_artifacts["prepared_messages_csv"])
    prepared_messages = pd.read_csv(messages_path)

    assert messages_path.exists()
    assert list(prepared_messages.columns) == ["message_id", "label", "text"]
    assert prepared_messages["message_id"].tolist() == list(range(len(prepared_messages)))
    assert sorted(prepared_messages["label"].unique().tolist()) == ["ham", "spam"]
    assert prepared_messages["text"].str.len().gt(0).all()
