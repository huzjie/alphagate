"""配置思路：资金流（capital_flow）。"""
from __future__ import annotations

from typing import Dict

from alphagate.core.strategy_idea import StrategyIdea
from alphagate.strategies.base import BaseStrategy, build_idea


class CapitalFlowStrategy(BaseStrategy):
    """资金流思路：跟踪北向、主力资金流向，跟随聪明钱布局。"""

    slug = "capital_flow"
    display_name = "资金流"

    def idea(self) -> StrategyIdea:
        return build_idea(
            name="资金流",
            rationale="跟踪北向、主力资金流向，跟随聪明钱布局",
            applicable_regimes=['bull', 'liquidity_driven'],
            keywords=['capital_flow', '资金流', '北向', '主力', '聪明钱'],
            default_weight=0.08,
            risk_level="medium",
        )

    def weights(self, universe: Dict[str, Dict[str, float]], **kwargs) -> Dict[str, float]:
        factor = self.factor_key()
        scored = [(sym, max(feats.get(factor, feats.get("score", 0.0)), 0.0))
                  for sym, feats in universe.items()]
        total = sum(s for _, s in scored) or 1.0
        return {sym: s / total for sym, s in scored if s > 0}

    def factor_key(self) -> str:
        return "capital_flow"


STRATEGY = CapitalFlowStrategy()
