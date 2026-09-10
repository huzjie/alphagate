"""配置加载与校验：从 YAML/JSON/环境变量读取并合并。"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from alphagate.core.exceptions import ConfigError

try:  # pragma: no cover - 可选依赖
    import yaml  # type: ignore
    _HAS_YAML = True
except ImportError:  # pragma: no cover
    _HAS_YAML = False


DEFAULTS: Dict[str, Any] = {
    "model": {
        "backend": "mock",
        "model_id": "FinStep-AI/Alpha-R1",
        "temperature": 0.1,
        "max_tokens": 2048,
        "device": "auto",
    },
    "gate": {
        "embedder": "hash",
        "similarity_threshold": 0.35,
        "top_k": 5,
        "max_active_strategies": 6,
    },
    "data": {
        "source": "mock",
        "cache_dir": "~/.cache/alphagate",
        "universe": [],
    },
    "backtest": {
        "initial_capital": 1_000_000.0,
        "benchmark": "000300.SH",
        "rebalance_freq": "monthly",
        "cost_rate": 0.0003,
    },
    "serving": {
        "host": "0.0.0.0",
        "port": 8000,
    },
}


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(path: Optional[str] = None, overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """加载配置：默认 -> 文件 -> 环境变量 -> 运行时覆盖。"""
    cfg = _deep_merge(DEFAULTS, {})
    if path:
        p = Path(path).expanduser()
        if not p.exists():
            raise ConfigError(f"config file not found: {p}")
        text = p.read_text(encoding="utf-8")
        if p.suffix in (".yaml", ".yml"):
            if not _HAS_YAML:
                raise ConfigError("PyYAML not installed; pip install pyyaml")
            loaded = yaml.safe_load(text) or {}
        elif p.suffix == ".json":
            loaded = json.loads(text)
        else:
            raise ConfigError(f"unsupported config format: {p.suffix}")
        cfg = _deep_merge(cfg, loaded)
    # 环境变量覆盖：ALPHAGATE_<SECTION>_<KEY>
    for key, val in os.environ.items():
        if not key.startswith("ALPHAGATE_"):
            continue
        parts = key[len("ALPHAGATE_"):].lower().split("_", 1)
        if len(parts) != 2:
            continue
        section, sub = parts
        cfg.setdefault(section, {})[sub.lower()] = val
    if overrides:
        cfg = _deep_merge(cfg, overrides)
    return cfg


def section(cfg: Dict[str, Any], name: str) -> Dict[str, Any]:
    """取配置分区，缺失时返回空 dict。"""
    return cfg.get(name, {}) or {}
