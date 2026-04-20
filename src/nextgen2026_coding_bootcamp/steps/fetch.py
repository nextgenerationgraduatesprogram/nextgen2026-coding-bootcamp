from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlretrieve
from zipfile import ZipFile


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


def run_fetch(cfg) -> dict:
    source_url = str(cfg.fetch.source_url)
    archive_member = str(cfg.fetch.archive_member)

    raw_dir = Path(cfg.paths.raw_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)

    archive_name = _archive_name_from_url(source_url)
    archive_path = raw_dir / archive_name
    raw_csv_path = raw_dir / Path(archive_member).name

    downloaded_archive = False
    extracted_member = False

    if not archive_path.exists():
        urlretrieve(source_url, archive_path)
        downloaded_archive = True

    if not raw_csv_path.exists():
        _extract_archive_member(archive_path, archive_member, raw_csv_path)
        extracted_member = True

    return {
        "source_url": source_url,
        "archive_path": str(archive_path),
        "archive_member": archive_member,
        "raw_csv": str(raw_csv_path),
        "downloaded_archive": downloaded_archive,
        "extracted_member": extracted_member,
    }
