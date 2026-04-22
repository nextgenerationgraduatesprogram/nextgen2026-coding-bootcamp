from __future__ import annotations

from pathlib import Path

from nextgen2026_coding_bootcamp.runtime import create_run_context
from nextgen2026_coding_bootcamp.steps.fetch import run_fetch


def test_run_fetch_writes_downloaded_shared_raw_artifact_without_context(workshop_cfg, synthetic_sms_archive_bytes):
    requested_urls: list[str] = []

    def fake_archive_downloader(archive_url: str) -> bytes:
        requested_urls.append(archive_url)
        return synthetic_sms_archive_bytes

    artifacts = run_fetch(cfg=workshop_cfg, archive_downloader=fake_archive_downloader)
    raw_path = Path(artifacts["raw_tsv"])

    assert raw_path == Path(workshop_cfg.paths.raw_dir) / workshop_cfg.fetch.raw_artifact_name
    assert artifacts["copied_to_run"] is False
    assert artifacts["downloaded"] is True
    assert artifacts["n_messages"] == 4
    assert artifacts["labels"] == ["ham", "spam"]
    assert raw_path.read_text(encoding="utf-8").splitlines() == [
        "ham\tSee you at noon",
        "spam\tWIN cash now",
        "ham\t The server restart worked ",
        "spam\tClaim your prize today",
    ]
    assert requested_urls == ["https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"]


def test_run_fetch_reuses_cached_raw_artifact_without_downloading(workshop_cfg, tmp_path: Path):
    workshop_cfg.paths.raw_dir = str(tmp_path / "raw")
    raw_dir = Path(workshop_cfg.paths.raw_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    cached_raw_tsv = raw_dir / workshop_cfg.fetch.raw_artifact_name
    cached_raw_tsv.write_text("ham\tCached row\nspam\tCached promo\n", encoding="utf-8")

    artifacts = run_fetch(
        cfg=workshop_cfg,
        archive_downloader=lambda *_: (_ for _ in ()).throw(AssertionError("unexpected download")),
    )

    assert artifacts["downloaded"] is False
    assert artifacts["n_messages"] == 2
    assert Path(artifacts["raw_tsv"]).read_text(encoding="utf-8") == (
        "ham\tCached row\nspam\tCached promo\n"
    )


def test_run_fetch_force_download_refreshes_cached_raw_artifact(workshop_cfg, synthetic_sms_archive_bytes, tmp_path: Path):
    workshop_cfg.paths.raw_dir = str(tmp_path / "raw")
    Path(workshop_cfg.paths.raw_dir).mkdir(parents=True, exist_ok=True)
    cached_raw_tsv = Path(workshop_cfg.paths.raw_dir) / workshop_cfg.fetch.raw_artifact_name
    cached_raw_tsv.write_text("ham\tOld cache\n", encoding="utf-8")

    artifacts = run_fetch(
        cfg=workshop_cfg,
        archive_downloader=lambda archive_url: synthetic_sms_archive_bytes,
        force_download=True,
    )

    assert artifacts["downloaded"] is True
    assert cached_raw_tsv.read_text(encoding="utf-8").splitlines()[0] == "ham\tSee you at noon"


def test_run_fetch_copies_shared_raw_artifact_into_run_directory(workshop_cfg, synthetic_sms_archive_bytes, tmp_path: Path):
    workshop_cfg.run.output_root = str(tmp_path / "runs")
    workshop_cfg.paths.raw_dir = str(tmp_path / "raw")

    ctx = create_run_context(output_root=Path(workshop_cfg.run.output_root), run_name="fetch")
    artifacts = run_fetch(
        cfg=workshop_cfg,
        ctx=ctx,
        archive_downloader=lambda archive_url: synthetic_sms_archive_bytes,
    )

    assert artifacts["copied_to_run"] is True
    assert Path(artifacts["raw_tsv"]).parent == ctx.run_dir / "fetch"
    assert Path(artifacts["shared_raw_tsv"]).exists()
    assert Path(artifacts["raw_tsv"]).exists()
