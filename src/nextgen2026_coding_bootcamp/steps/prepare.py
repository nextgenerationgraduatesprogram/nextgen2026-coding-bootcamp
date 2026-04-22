from __future__ import annotations

from pathlib import Path
import logging
import shutil

import pandas as pd

logger = logging.getLogger(__name__)

PREPARED_MESSAGE_COLUMNS = ["message_id", "label", "text"]
VALID_MESSAGE_LABELS = ("ham", "spam")


def _normalize_message_text(text: str) -> str:
    return " ".join(str(text).split())


def _resolve_input_tsv(cfg, ctx=None, input_tsv: Path | None = None) -> Path:
    if input_tsv is not None:
        return input_tsv

    if ctx is not None:
        fetch_artifact = ctx.artifacts.get("fetch", {})
        raw_tsv = fetch_artifact.get("raw_tsv")
        if raw_tsv:
            return Path(raw_tsv)

    return Path(cfg.paths.raw_dir) / str(cfg.fetch.raw_artifact_name)


def _copy_to_run(shared_path: Path, run_path: Path) -> None:
    run_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(shared_path, run_path)


def _load_prepared_messages(raw_tsv: Path) -> pd.DataFrame:
    raw_messages = pd.read_csv(
        raw_tsv,
        sep="\t",
        header=None,
        names=["label", "text"],
        dtype=str,
        keep_default_na=False,
    )
    labels = raw_messages["label"].fillna("").astype(str).str.strip().str.lower()
    texts = raw_messages["text"].fillna("").map(_normalize_message_text)
    keep_mask = labels.isin(VALID_MESSAGE_LABELS) & texts.ne("")

    prepared_messages = pd.DataFrame(
        {
            "message_id": range(int(keep_mask.sum())),
            "label": labels[keep_mask].tolist(),
            "text": texts[keep_mask].tolist(),
        }
    )
    return prepared_messages.loc[:, PREPARED_MESSAGE_COLUMNS]


def run_prepare(cfg, ctx=None, input_tsv: Path | None = None) -> dict:
    raw_tsv = _resolve_input_tsv(cfg=cfg, ctx=ctx, input_tsv=input_tsv)

    shared_output_dir = Path(cfg.paths.intermediate_dir)
    shared_output_dir.mkdir(parents=True, exist_ok=True)

    prepared_messages_name = str(cfg.prepare.prepared_messages_name)

    shared_prepared_messages_csv = shared_output_dir / prepared_messages_name

    logger.info("[prepare]")
    logger.info("prepare:start input=%s", raw_tsv)

    prepared_messages = _load_prepared_messages(raw_tsv=raw_tsv)
    prepared_messages.to_csv(shared_prepared_messages_csv, index=False)

    if ctx is None:
        output_prepared_messages_csv = shared_prepared_messages_csv
        copied_to_run = False
    else:
        run_stage_dir = ctx.run_dir / "prepare"
        run_stage_dir.mkdir(parents=True, exist_ok=True)
        output_prepared_messages_csv = run_stage_dir / prepared_messages_name
        _copy_to_run(shared_prepared_messages_csv, output_prepared_messages_csv)
        copied_to_run = True

    logger.info(
        "prepare:finish messages=%d output_messages=%s\n",
        len(prepared_messages),
        output_prepared_messages_csv,
    )

    return {
        "raw_tsv": str(raw_tsv),
        "prepared_messages_csv": str(output_prepared_messages_csv),
        "shared_prepared_messages_csv": str(shared_prepared_messages_csv),
        "n_messages": int(len(prepared_messages)),
        "labels": sorted(prepared_messages["label"].unique().tolist()),
        "copied_to_run": copied_to_run,
    }
