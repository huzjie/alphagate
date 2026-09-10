"""配置思路：情绪面（sentiment）。"""
from __future__ import annotations

from typing import Dict

from alphagate.core.strategy_idea import StrategyIdea
from alphagate.strategies.base import BaseStrategy, build_idea


class SentimentStrategy(BaseStrategy):
    """情绪面思路：市场情绪指标（换手、涨跌比、波动率）驱动的顺势或逆向操作。"""

    slug = "sentiment"
    display_name = "情绪面"

    def idea(self) -> StrategyIdea:
        return build_idea(
            name="情绪面",
            rationale="市场情绪指标（换手、涨跌比、波动率）驱动的顺势或逆向操作",
            applicable_regimes=['high_volatility', 'bear'],
            keywords=['sentiment', '情绪', '换手', '涨跌比', '逆向'],
            default_weight=0.08,
            risk_level="high",
        )

    def weights(self, universe: Dict[str, Dict[str, float]], **kwargs) -> Dict[str, float]:
        factor = self.factor_key()
        scored = [(sym, max(feats.get(factor, feats.get("score", 0.0)), 0.0))
                  for sym, feats in universe.items()]
        total = sum(s for _, s in scored) or 1.0
        return {sym: s / total for sym, s in scored if s > 0}

    def factor_key(self) -> str:
        return "sentiment"


STRATEGY = SentimentStrategy()
