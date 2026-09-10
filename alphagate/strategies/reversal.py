"""配置思路：反转（reversal）。"""
from __future__ import annotations

from typing import Dict, List, Optional

from alphagate.core.strategy_idea import StrategyIdea
from alphagate.strategies.base import BaseStrategy, build_idea


class ReversalStrategy(BaseStrategy):
    """反转思路：超跌资产在情绪修复时均值回归，逆向布局错杀标的。"""

    slug = "reversal"
    display_name = "反转"

    def idea(self) -> StrategyIdea:
        return build_idea(
            name="反转",
            rationale="超跌资产在情绪修复时均值回归，逆向布局错杀标的",
            applicable_regimes=['bear', 'high_volatility'],
            keywords=['reversal', '超跌', '均值回归', '逆向'],
            default_weight=0.08,
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
        return "reversal"


STRATEGY = ReversalStrategy()
