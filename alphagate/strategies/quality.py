"""配置思路：质量（quality）。"""
from __future__ import annotations

from typing import Dict, List, Optional

from alphagate.core.strategy_idea import StrategyIdea
from alphagate.strategies.base import BaseStrategy, build_idea


class QualityStrategy(BaseStrategy):
    """质量思路：盈利质量稳定、ROE 持续的公司能穿越周期，抗跌且长期复利。"""

    slug = "quality"
    display_name = "质量"

    def idea(self) -> StrategyIdea:
        return build_idea(
            name="质量",
            rationale="盈利质量稳定、ROE 持续的公司能穿越周期，抗跌且长期复利",
            applicable_regimes=['bull', 'sideways'],
            keywords=['quality', 'roe', '盈利质量', '穿越周期'],
            default_weight=0.18,
            risk_level="low",
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
        return "quality"


STRATEGY = QualityStrategy()
