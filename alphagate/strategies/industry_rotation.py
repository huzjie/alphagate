"""配置思路：行业轮动（industry_rotation）。"""
from __future__ import annotations

from typing import Dict

from alphagate.core.strategy_idea import StrategyIdea
from alphagate.strategies.base import BaseStrategy, build_idea


class IndustryRotationStrategy(BaseStrategy):
    """行业轮动思路：经济周期不同阶段行业景气轮动，把握强势行业切换带来的结构收益。"""

    slug = "industry_rotation"
    display_name = "行业轮动"

    def idea(self) -> StrategyIdea:
        return build_idea(
            name="行业轮动",
            rationale="经济周期不同阶段行业景气轮动，把握强势行业切换带来的结构收益",
            applicable_regimes=['bull', 'sideways'],
            keywords=['industry_rotation', '行业轮动', '景气', '结构行情'],
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
        return "industry_rotation"


STRATEGY = IndustryRotationStrategy()
