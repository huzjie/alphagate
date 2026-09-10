"""配置思路：事件驱动（event_driven）。"""
from __future__ import annotations

from typing import Dict

from alphagate.core.strategy_idea import StrategyIdea
from alphagate.strategies.base import BaseStrategy, build_idea


class EventDrivenStrategy(BaseStrategy):
    """事件驱动思路：并购重组、财报、政策等事件催化的短期超额收益。"""

    slug = "event_driven"
    display_name = "事件驱动"

    def idea(self) -> StrategyIdea:
        return build_idea(
            name="事件驱动",
            rationale="并购重组、财报、政策等事件催化的短期超额收益",
            applicable_regimes=['bull', 'liquidity_driven'],
            keywords=['event', '事件驱动', '并购', '政策', '财报'],
            default_weight=0.06,
            risk_level="high",
        )

    def weights(self, universe: Dict[str, Dict[str, float]], **kwargs) -> Dict[str, float]:
        factor = self.factor_key()
        scored = [(sym, max(feats.get(factor, feats.get("score", 0.0)), 0.0))
                  for sym, feats in universe.items()]
        total = sum(s for _, s in scored) or 1.0
        return {sym: s / total for sym, s in scored if s > 0}

    def factor_key(self) -> str:
        return "event_driven"


STRATEGY = EventDrivenStrategy()
