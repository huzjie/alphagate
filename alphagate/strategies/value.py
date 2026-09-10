"""配置思路：价值（value）。"""
from __future__ import annotations

from typing import Dict, List, Optional

from alphagate.core.strategy_idea import StrategyIdea
from alphagate.strategies.base import BaseStrategy, build_idea


class ValueStrategy(BaseStrategy):
    """价值思路：低估值资产在均值回归与估值修复时提供安全边际，适合震荡与复苏期。"""

    slug = "value"
    display_name = "价值"

    def idea(self) -> StrategyIdea:
        return build_idea(
            name="价值",
            rationale="低估值资产在均值回归与估值修复时提供安全边际，适合震荡与复苏期",
            applicable_regimes=['sideways', 'bear'],
            keywords=['value', 'low_valuation', 'pe', 'pb', '安全边际'],
            default_weight=0.18,
            risk_level="medium",
        )

    def weights(self, universe: Dict[str, Dict[str, float]], **kwargs) -> Dict[str, float]:
        """基于因子暴露给出权重：因子分越高权重越大。"""
        factor = self.factor_key()
        scored = []
        for sym, feats in universe.items():
            score = feats.get(factor, feats.get("score", 0.0))
            scored.append((sym, max(score, 0.0)))
        if not scored:
            return {}
        total = sum(s for _, s in scored) or 1.0
        return {sym: s / total for sym, s in scored if s > 0}

    def factor_key(self) -> str:
        return "value"


STRATEGY = ValueStrategy()
