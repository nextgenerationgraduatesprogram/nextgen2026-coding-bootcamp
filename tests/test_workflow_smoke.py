import pytest
from pathlib import Path
import shutil
from omegaconf import OmegaConf
from nextgen2026_coding_bootcamp.config import compose_config
from nextgen2026_coding_bootcamp.manifests import write_manifest
from nextgen2026_coding_bootcamp.runtime import create_run_context
from nextgen2026_coding_bootcamp.workflow import run_workflow

def test_full_workflow_smoke(tmp_path):
    """Run a full workflow on a temporary directory and verify output exists."""
    config_root = Path("configs")
    parts = [
        "run.yaml",
        "paths.yaml",
        "stages/fetch.yaml",
        "stages/prepare.yaml",
        "stages/analyze.yaml",
        "stages/report.yaml",
        "profiles/base.yaml"
    ]
    
    cfg = compose_config(config_root=config_root, parts=parts)
    
    # Override output root to tmp_path
    cfg.run.output_root = str(tmp_path)
    
    ctx = create_run_context(tmp_path, run_name="smoke-test")
    
    # Mocking or running actual stages? 
    # For a smoke test in this bootcamp, we usually run the actual logic 
    # but maybe with limited data if possible. Here we run it as is.
    run_workflow(cfg, ctx)
    write_manifest(ctx)
    
    assert (ctx.run_dir / "manifest.json").exists()
    assert (ctx.run_dir / "analyze" / "hourly_profile.csv").exists()
    assert (ctx.run_dir / "report" / "hourly_demand_by_day_type.png").exists()
