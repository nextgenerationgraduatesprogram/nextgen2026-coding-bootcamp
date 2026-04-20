from pathlib import Path

from omegaconf import DictConfig, OmegaConf


def load_config(config_path: Path, overrides: list[str] | None = None) -> DictConfig:
    cfg = OmegaConf.load(config_path)
    if overrides:
        cfg = OmegaConf.merge(cfg, OmegaConf.from_dotlist(overrides))
    return cfg


def compose_config(
    config_root: Path,
    parts: list[str],
    overrides: list[str] | None = None,
) -> DictConfig:
    cfg = OmegaConf.create()
    for part in parts:
        cfg = OmegaConf.merge(cfg, OmegaConf.load(config_root / part))
    if overrides:
        cfg = OmegaConf.merge(cfg, OmegaConf.from_dotlist(overrides))
    return cfg
