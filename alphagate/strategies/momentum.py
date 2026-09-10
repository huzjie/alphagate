"""配置思路：动量（momentum）。"""
from __future__ import annotations

from typing import Dict, List, Optional

from alphagate.core.strategy_idea import StrategyIdea
from alphagate.strategies.base import BaseStrategy, build_idea


class MomentumStrategy(BaseStrategy):
    """动量思路：趋势延续时顺势加仓强势板块，动量因子在单边行情收益显著。"""

    slug = "momentum"
    display_name = "动量"

    def idea(self) -> StrategyIdea:
        return build_idea(
            name="动量",
            rationale="趋势延续时顺势加仓强势板块，动量因子在单边行情收益显著",
            applicable_regimes=['bull'],
            keywords=['momentum', 'trend', '强势', '趋势延续'],
            default_weight=0.2,
            risk_level="high",
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
        return "momentum"


STRATEGY = MomentumStrategy()
