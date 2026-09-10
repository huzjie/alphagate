"""配置思路：防御（defensive）。"""
from __future__ import annotations

from typing import Dict, List, Optional

from alphagate.core.strategy_idea import StrategyIdea
from alphagate.strategies.base import BaseStrategy, build_idea


class DefensiveStrategy(BaseStrategy):
    """防御思路：高波动或衰退环境降低仓位、增配债券与现金等价物。"""

    slug = "defensive"
    display_name = "防御"

    def idea(self) -> StrategyIdea:
        return build_idea(
            name="防御",
            rationale="高波动或衰退环境降低仓位、增配债券与现金等价物",
            applicable_regimes=['high_volatility', 'risk_off', 'bear'],
            keywords=['defensive', '防御', '降仓', '债券'],
            default_weight=0.15,
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
        return "defensive"


STRATEGY = DefensiveStrategy()
