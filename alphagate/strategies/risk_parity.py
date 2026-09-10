"""配置思路：风险平价（risk_parity）。"""
from __future__ import annotations

from typing import Dict, List, Optional

from alphagate.core.strategy_idea import StrategyIdea
from alphagate.strategies.base import BaseStrategy, build_idea


class RiskParityStrategy(BaseStrategy):
    """风险平价思路：跨资产风险预算平衡，降低单一资产集中度与组合波动。"""

    slug = "risk_parity"
    display_name = "风险平价"

    def idea(self) -> StrategyIdea:
        return build_idea(
            name="风险平价",
            rationale="跨资产风险预算平衡，降低单一资产集中度与组合波动",
            applicable_regimes=['sideways', 'high_volatility'],
            keywords=['risk_parity', '风险平价', '分散', '风险预算'],
            default_weight=0.1,
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
        return "risk_parity"


STRATEGY = RiskParityStrategy()
