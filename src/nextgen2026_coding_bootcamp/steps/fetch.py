from __future__ import annotations

import io
import logging
from pathlib import Path
import shutil
import urllib.request
import zipfile

import pandas as pd

logger = logging.getLogger(__name__)


def _copy_to_run(shared_path: Path, run_path: Path) -> None:
    run_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(shared_path, run_path)


def _require_value(section: str, key: str, value):
    if value is None:
        raise ValueError(
            f"Missing config value `{section}.{key}`. "
            "Update both `configs/base.yaml` and the matching stage fragment."
        )
    if isinstance(value, str) and not value.strip():
        raise ValueError(
            f"Blank config value `{section}.{key}`. "
            "Update both `configs/base.yaml` and the matching stage fragment."
        )
    return value


def _validate_fetch_config(cfg) -> dict[str, object]:
    fetch_cfg = cfg.fetch
    return {
        "dataset_name": str(_require_value("fetch", "dataset_name", fetch_cfg.dataset_name)),
        "uci_dataset_id": int(_require_value("fetch", "uci_dataset_id", fetch_cfg.uci_dataset_id)),
        "raw_artifact_name": str(
            _require_value("fetch", "raw_artifact_name", fetch_cfg.raw_artifact_name)
        ),
        "force_download": bool(
            _require_value("fetch", "force_download", fetch_cfg.force_download)
        ),
    }


def _build_uci_archive_url(uci_dataset_id: int, dataset_name: str) -> str:
    archive_slug = dataset_name.replace("_", "+")
    return f"https://archive.ics.uci.edu/static/public/{uci_dataset_id}/{archive_slug}.zip"


def _download_archive_bytes(archive_url: str) -> bytes:
    with urllib.request.urlopen(archive_url, timeout=30) as response:
        return response.read()


def _archive_bytes_to_raw_messages(archive_bytes: bytes) -> pd.DataFrame:
    with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
        members = [
            name
            for name in archive.namelist()
            if not name.endswith("/")
        ]
        dataset_member = next(
            (name for name in members if Path(name).name.lower() == "smsspamcollection"),
            None,
        )
        if dataset_member is None:
            raise ValueError("Downloaded archive does not contain `SMSSpamCollection`.")

        raw_text = archive.read(dataset_member).decode("utf-8", errors="replace")

    rows: list[dict[str, str]] = []
    for line in raw_text.splitlines():
        if not line.strip():
            continue
        if "\t" not in line:
            raise ValueError("Downloaded raw dataset has a malformed line without a tab separator.")
        label, text = line.split("\t", 1)
        rows.append(
            {
                "label": label.strip().lower(),
                "text": text,
            }
        )

    return pd.DataFrame(rows, columns=["label", "text"])


def _write_raw_messages(raw_messages: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    raw_messages.to_csv(
        output_path,
        sep="\t",
        header=False,
        index=False,
        lineterminator="\n",
    )


def _read_raw_messages(raw_tsv: Path) -> pd.DataFrame:
    return pd.read_csv(
        raw_tsv,
        sep="\t",
        header=None,
        names=["label", "text"],
        dtype=str,
        keep_default_na=False,
    )


def run_fetch(cfg, ctx=None, archive_downloader=None, force_download: bool | None = None) -> dict:
    fetch_cfg = _validate_fetch_config(cfg)
    dataset_name = str(fetch_cfg["dataset_name"])
    raw_artifact_name = str(fetch_cfg["raw_artifact_name"])
    should_force_download = (
        bool(fetch_cfg["force_download"]) if force_download is None else bool(force_download)
    )
    archive_url = _build_uci_archive_url(
        uci_dataset_id=int(fetch_cfg["uci_dataset_id"]),
        dataset_name=dataset_name,
    )
    archive_downloader = _download_archive_bytes if archive_downloader is None else archive_downloader

    raw_dir = Path(cfg.paths.raw_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    shared_raw_tsv = raw_dir / raw_artifact_name

    logger.info("[fetch]")
    logger.info(
        "fetch:start dataset=%s uci_dataset_id=%s force_download=%s archive_url=%s shared_output=%s",
        dataset_name,
        fetch_cfg["uci_dataset_id"],
        should_force_download,
        archive_url,
        shared_raw_tsv,
    )

    if should_force_download or not shared_raw_tsv.exists():
        archive_bytes = archive_downloader(archive_url)
        raw_messages = _archive_bytes_to_raw_messages(archive_bytes=archive_bytes)
        _write_raw_messages(raw_messages=raw_messages, output_path=shared_raw_tsv)
        downloaded = True
    else:
        downloaded = False

    raw_messages = _read_raw_messages(shared_raw_tsv)
    labels = sorted(raw_messages["label"].astype(str).str.strip().str.lower().unique().tolist())

    if ctx is None:
        output_raw_tsv = shared_raw_tsv
        copied_to_run = False
    else:
        run_stage_dir = ctx.run_dir / "fetch"
        run_stage_dir.mkdir(parents=True, exist_ok=True)
        output_raw_tsv = run_stage_dir / raw_artifact_name
        _copy_to_run(shared_raw_tsv, output_raw_tsv)
        copied_to_run = True

    logger.info(
        "fetch:finish messages=%d labels=%s downloaded=%s output=%s\n",
        len(raw_messages),
        labels,
        downloaded,
        output_raw_tsv,
    )

    return {
        "dataset_name": dataset_name,
        "raw_tsv": str(output_raw_tsv),
        "shared_raw_tsv": str(shared_raw_tsv),
        "n_messages": int(len(raw_messages)),
        "labels": labels,
        "downloaded": downloaded,
        "copied_to_run": copied_to_run,
    }
