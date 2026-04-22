from pathlib import Path

from dotenv import load_dotenv
from omegaconf import DictConfig, OmegaConf

REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_repo_dotenv() -> Path | None:
    dotenv_path = REPO_ROOT / ".env"
    if not dotenv_path.exists():
        return None

    load_dotenv(dotenv_path=dotenv_path, override=False)
    return dotenv_path


def load_config(config_path: Path, overrides: list[str] | None = None) -> DictConfig:
    _load_repo_dotenv()
    cfg = OmegaConf.load(config_path)
    if overrides:
        cfg = OmegaConf.merge(cfg, OmegaConf.from_dotlist(overrides))
    return cfg


def compose_config(
    config_root: Path,
    parts: list[str],
    overrides: list[str] | None = None,
) -> DictConfig:
    _load_repo_dotenv()
    cfg = OmegaConf.create()
    for part in parts:
        cfg = OmegaConf.merge(cfg, OmegaConf.load(config_root / part))
    if overrides:
        cfg = OmegaConf.merge(cfg, OmegaConf.from_dotlist(overrides))
    return cfg
