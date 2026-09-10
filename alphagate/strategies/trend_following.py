"""配置思路：趋势跟踪（trend_following）。"""
from __future__ import annotations

from typing import Dict, List, Optional

from alphagate.core.strategy_idea import StrategyIdea
from alphagate.strategies.base import BaseStrategy, build_idea


class TrendFollowingStrategy(BaseStrategy):
    """趋势跟踪思路：用均线与通道跟踪指数趋势，右侧确认后跟随。"""

    slug = "trend_following"
    display_name = "趋势跟踪"

    def idea(self) -> StrategyIdea:
        return build_idea(
            name="趋势跟踪",
            rationale="用均线与通道跟踪指数趋势，右侧确认后跟随",
            applicable_regimes=['bull', 'bear'],
            keywords=['trend_following', '均线', '右侧', '通道'],
            default_weight=0.12,
            risk_level="medium",
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
        return "trend_following"


STRATEGY = TrendFollowingStrategy()
