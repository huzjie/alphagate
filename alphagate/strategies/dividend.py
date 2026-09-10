"""配置思路：红利（dividend）。"""
from __future__ import annotations

from typing import Dict, List, Optional

from alphagate.core.strategy_idea import StrategyIdea
from alphagate.strategies.base import BaseStrategy, build_idea


class DividendStrategy(BaseStrategy):
    """红利思路：高股息资产提供稳定现金流，在利率下行与避险时吸引力上升。"""

    slug = "dividend"
    display_name = "红利"

    def idea(self) -> StrategyIdea:
        return build_idea(
            name="红利",
            rationale="高股息资产提供稳定现金流，在利率下行与避险时吸引力上升",
            applicable_regimes=['bear', 'risk_off', 'sideways'],
            keywords=['dividend', '红利', '高股息', '现金流'],
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
        return "dividend"


STRATEGY = DividendStrategy()
