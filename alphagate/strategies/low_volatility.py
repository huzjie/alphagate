"""配置思路：低波（low_volatility）。"""
from __future__ import annotations

from typing import Dict, List, Optional

from alphagate.core.strategy_idea import StrategyIdea
from alphagate.strategies.base import BaseStrategy, build_idea


class LowVolatilityStrategy(BaseStrategy):
    """低波思路：低波动资产在不确定环境下下行保护更好，风险调整后收益更优。"""

    slug = "low_volatility"
    display_name = "低波"

    def idea(self) -> StrategyIdea:
        return build_idea(
            name="低波",
            rationale="低波动资产在不确定环境下下行保护更好，风险调整后收益更优",
            applicable_regimes=['high_volatility', 'risk_off'],
            keywords=['low_volatility', '低波', '下行保护'],
            default_weight=0.12,
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
        return "low_volatility"


STRATEGY = LowVolatilityStrategy()
