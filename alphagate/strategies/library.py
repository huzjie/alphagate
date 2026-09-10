"""策略思路库：汇总所有注册思路，供语义门控消费。"""
from __future__ import annotations

from typing import Dict, List

from alphagate.core.strategy_idea import StrategyIdea
from alphagate.strategies.value import STRATEGY as _value
from alphagate.strategies.momentum import STRATEGY as _momentum
from alphagate.strategies.quality import STRATEGY as _quality
from alphagate.strategies.low_volatility import STRATEGY as _low_volatility
from alphagate.strategies.dividend import STRATEGY as _dividend
from alphagate.strategies.growth import STRATEGY as _growth
from alphagate.strategies.reversal import STRATEGY as _reversal
from alphagate.strategies.trend_following import STRATEGY as _trend_following
from alphagate.strategies.defensive import STRATEGY as _defensive
from alphagate.strategies.liquidity import STRATEGY as _liquidity
from alphagate.strategies.size import STRATEGY as _size
from alphagate.strategies.risk_parity import STRATEGY as _risk_parity
from alphagate.strategies.industry_rotation import STRATEGY as _industry_rotation
from alphagate.strategies.macro import STRATEGY as _macro
from alphagate.strategies.event_driven import STRATEGY as _event_driven
from alphagate.strategies.technical import STRATEGY as _technical
from alphagate.strategies.capital_flow import STRATEGY as _capital_flow
from alphagate.strategies.sentiment import STRATEGY as _sentiment


class StrategyLibrary:
    """策略库：按 slug 索引，提供 idea/weights 统一入口。"""

    def __init__(self) -> None:
        self._strategies = [
        _value,
        _momentum,
        _quality,
        _low_volatility,
        _dividend,
        _growth,
        _reversal,
        _trend_following,
        _defensive,
        _liquidity,
        _size,
        _risk_parity,
        _industry_rotation,
        _macro,
        _event_driven,
        _technical,
        _capital_flow,
        _sentiment,
        ]
        self._by_slug = {s.slug: s for s in self._strategies}

    def ideas(self) -> List[StrategyIdea]:
        return [s.idea() for s in self._strategies]

    def names(self) -> List[str]:
        return [s.slug for s in self._strategies]

    def get(self, slug: str):
        if slug not in self._by_slug:
            raise KeyError(f"unknown strategy: {slug!r}")
        return self._by_slug[slug]

    def __len__(self) -> int:
        return len(self._strategies)

    def __iter__(self):
        return iter(self._strategies)


def load_all_ideas() -> List[StrategyIdea]:
    """便捷函数：一次性加载全部候选配置思路。"""
    return StrategyLibrary().ideas()
