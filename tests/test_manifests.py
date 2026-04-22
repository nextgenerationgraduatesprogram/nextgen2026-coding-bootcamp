from __future__ import annotations

import json
from pathlib import Path

from nextgen2026_coding_bootcamp.manifests import write_manifest
from nextgen2026_coding_bootcamp.runtime import RunContext


def test_write_manifest_serializes_run_context(tmp_path: Path):
    ctx = RunContext(
        run_id="run-123",
        run_dir=tmp_path,
        artifacts={"fetch": {"raw_csv": "bike_demand_raw.csv"}},
    )

    manifest_path = write_manifest(ctx=ctx, git_commit="abc123")
    payload = json.loads(manifest_path.read_text())

    assert manifest_path == tmp_path / "manifest.json"
    assert payload == {
        "run_id": "run-123",
        "git_commit": "abc123",
        "artifacts": {"fetch": {"raw_csv": "bike_demand_raw.csv"}},
    }
