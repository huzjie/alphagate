"""配置思路：技术面（technical）。"""
from __future__ import annotations

from typing import Dict

from alphagate.core.strategy_idea import StrategyIdea
from alphagate.strategies.base import BaseStrategy, build_idea


class TechnicalStrategy(BaseStrategy):
    """技术面思路：量价、均线、形态等技术信号择时，捕捉短期趋势与拐点。"""

    slug = "technical"
    display_name = "技术面"

    def idea(self) -> StrategyIdea:
        return build_idea(
            name="技术面",
            rationale="量价、均线、形态等技术信号择时，捕捉短期趋势与拐点",
            applicable_regimes=['bull', 'bear', 'high_volatility'],
            keywords=['technical', '技术面', '量价', '均线', '择时'],
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
        return "technical"


STRATEGY = TechnicalStrategy()
