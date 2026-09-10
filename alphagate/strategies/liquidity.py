"""配置思路：流动性（liquidity）。"""
from __future__ import annotations

from typing import Dict, List, Optional

from alphagate.core.strategy_idea import StrategyIdea
from alphagate.strategies.base import BaseStrategy, build_idea


class LiquidityStrategy(BaseStrategy):
    """流动性思路：流动性极度宽松时资金面主导，利好高贝塔与估值扩张资产。"""

    slug = "liquidity"
    display_name = "流动性"

    def idea(self) -> StrategyIdea:
        return build_idea(
            name="流动性",
            rationale="流动性极度宽松时资金面主导，利好高贝塔与估值扩张资产",
            applicable_regimes=['liquidity_driven', 'bull'],
            keywords=['liquidity', '流动性', '资金面', '宽松'],
            default_weight=0.1,
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
        return "liquidity"


STRATEGY = LiquidityStrategy()
