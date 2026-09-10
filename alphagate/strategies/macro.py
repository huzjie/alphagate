"""配置思路：宏观（macro）。"""
from __future__ import annotations

from typing import Dict

from alphagate.core.strategy_idea import StrategyIdea
from alphagate.strategies.base import BaseStrategy, build_idea


class MacroStrategy(BaseStrategy):
    """宏观思路：利率、通胀、增长等宏观变量驱动的自上而下大类资产配置。"""

    slug = "macro"
    display_name = "宏观"

    def idea(self) -> StrategyIdea:
        return build_idea(
            name="宏观",
            rationale="利率、通胀、增长等宏观变量驱动的自上而下大类资产配置",
            applicable_regimes=['sideways', 'bear', 'risk_off'],
            keywords=['macro', '宏观', '利率', '通胀', '大类资产'],
            default_weight=0.12,
            risk_level="medium",
        )

    def weights(self, universe: Dict[str, Dict[str, float]], **kwargs) -> Dict[str, float]:
        factor = self.factor_key()
        scored = [(sym, max(feats.get(factor, feats.get("score", 0.0)), 0.0))
                  for sym, feats in universe.items()]
        total = sum(s for _, s in scored) or 1.0
        return {sym: s / total for sym, s in scored if s > 0}

    def factor_key(self) -> str:
        return "macro"


STRATEGY = MacroStrategy()
