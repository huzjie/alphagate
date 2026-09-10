"""训练数据：合成「市场状态 -> 应放行思路」偏好对。"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class PreferenceSample:
    """一条偏好样本：市场状态 + 应放行/应拦截思路集合。"""

    regime_text: str
    allowed: List[str]
    blocked: List[str]


def make_rule_based_samples(strategies: List[str], n: int = 50) -> List[PreferenceSample]:
    """基于规则合成样本（演示 Stage1 偏好对齐）。"""
    samples: List[PreferenceSample] = []
    regimes = [
        ("bull", ["momentum", "growth", "quality"]),
        ("bear", ["dividend", "defensive", "value"]),
        ("high_volatility", ["low_volatility", "defensive", "risk_parity"]),
        ("liquidity_driven", ["growth", "size", "liquidity"]),
        ("sideways", ["value", "quality", "dividend"]),
    ]
    for i in range(n):
        reg, allowed = regimes[i % len(regimes)]
        blocked = [s for s in strategies if s not in allowed]
        samples.append(PreferenceSample(
            regime_text=f"市场状态: {reg}；描述: 合成样本 #{i}",
            allowed=allowed,
            blocked=blocked,
        ))
    return samples
