"""模型/策略卡目录加载。"""
from __future__ import annotations

import glob
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml
    _HAS_YAML = True
except ImportError:  # pragma: no cover
    _HAS_YAML = False


def load_cards(subdir: str) -> List[Dict[str, Any]]:
    """加载 catalog 下某个子目录的全部 YAML 卡。"""
    if not _HAS_YAML:
        return []
    here = Path(__file__).resolve().parent
    pattern = str(here / subdir / "*.yaml")
    cards: List[Dict[str, Any]] = []
    for p in sorted(glob.glob(pattern)):
        with open(p, encoding="utf-8") as f:
            cards.append(yaml.safe_load(f))
    return cards


def list_models() -> List[str]:
    return [c["name"] for c in load_cards("models")]


def list_strategies() -> List[str]:
    return [c["name"] for c in load_cards("strategies")]
