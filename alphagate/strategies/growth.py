"""配置思路：成长（growth）。"""
from __future__ import annotations

from typing import Dict, List, Optional

from alphagate.core.strategy_idea import StrategyIdea
from alphagate.strategies.base import BaseStrategy, build_idea


class GrowthStrategy(BaseStrategy):
    """成长思路：高成长赛道在流动性宽松、风险偏好抬升时获得估值溢价。"""

    slug = "growth"
    display_name = "成长"

    def idea(self) -> StrategyIdea:
        return build_idea(
            name="成长",
            rationale="高成长赛道在流动性宽松、风险偏好抬升时获得估值溢价",
            applicable_regimes=['bull', 'liquidity_driven'],
            keywords=['growth', '成长', '高增速', '估值溢价'],
            default_weight=0.15,
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
        return "growth"


STRATEGY = GrowthStrategy()
