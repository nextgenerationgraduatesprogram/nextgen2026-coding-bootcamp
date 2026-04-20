import json
from pathlib import Path


def write_manifest(ctx, git_commit: str | None = None) -> Path:
    manifest_path = ctx.run_dir / "manifest.json"
    payload = {
        "run_id": ctx.run_id,
        "git_commit": git_commit,
        "artifacts": ctx.artifacts,
    }
    manifest_path.write_text(json.dumps(payload, indent=2) + "\n")
    return manifest_path
