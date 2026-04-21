from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlretrieve
from zipfile import ZipFile
import logging
import shutil

logger = logging.getLogger(__name__)


def _archive_name_from_url(source_url: str) -> str:
    parsed = urlparse(source_url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("fetch.source_url must be an HTTP(S) URL")
    name = Path(parsed.path).name
    return name or "dataset.zip"


def _extract_archive_member(archive_path: Path, archive_member: str, output_csv: Path) -> None:
    with ZipFile(archive_path) as zf:
        with zf.open(archive_member) as src, output_csv.open("wb") as dst:
            dst.write(src.read())


def _copy_if_missing(source_path: Path, destination_path: Path) -> bool:
    if destination_path.exists():
        return False
    shutil.copy2(source_path, destination_path)
    return True


def run_fetch(cfg, ctx=None) -> dict:
    source_url = str(cfg.fetch.source_url)
    archive_member = str(cfg.fetch.archive_member)
    archive_name = _archive_name_from_url(source_url)
    csv_name = Path(archive_member).name

    raw_dir = Path(cfg.paths.raw_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    cached_archive_path = raw_dir / archive_name
    cached_csv_path = raw_dir / csv_name

    downloaded_archive = False
    extracted_member = False

    logger.info("[fetch]")
    logger.info("fetch:start source_url=%s cache_dir=%s", source_url, raw_dir)

    if not cached_archive_path.exists():
        logger.info("fetch:download archive=%s", cached_archive_path)
        urlretrieve(source_url, cached_archive_path)
        downloaded_archive = True
    else:
        logger.info("fetch:reuse_cached_archive archive=%s", cached_archive_path)

    if not cached_csv_path.exists():
        logger.info(
            "fetch:extract_member archive=%s member=%s output=%s",
            cached_archive_path,
            archive_member,
            cached_csv_path,
        )
        _extract_archive_member(cached_archive_path, archive_member, cached_csv_path)
        extracted_member = True
    else:
        logger.info("fetch:reuse_cached_csv csv=%s", cached_csv_path)

    if ctx is None:
        archive_path = cached_archive_path
        extracted_csv_path = cached_csv_path
        copied_archive_to_run = False
        copied_csv_to_run = False
    else:
        stage_output_dir = ctx.run_dir / "fetch"
        stage_output_dir.mkdir(parents=True, exist_ok=True)

        archive_path = stage_output_dir / archive_name
        extracted_csv_path = stage_output_dir / csv_name

        copied_archive_to_run = _copy_if_missing(cached_archive_path, archive_path)
        copied_csv_to_run = _copy_if_missing(cached_csv_path, extracted_csv_path)

    logger.info(
        "fetch:finish archive=%s extracted_csv=%s downloaded=%s extracted=%s\n",
        archive_path,
        extracted_csv_path,
        downloaded_archive,
        extracted_member,
    )

    return {
        "source_url": source_url,
        "archive_path": str(archive_path),
        "archive_member": archive_member,
        "raw_csv": str(extracted_csv_path),
        "cache_archive_path": str(cached_archive_path),
        "cache_raw_csv": str(cached_csv_path),
        "downloaded_archive": downloaded_archive,
        "extracted_member": extracted_member,
        "copied_archive_to_run": copied_archive_to_run,
        "copied_csv_to_run": copied_csv_to_run,
    }
