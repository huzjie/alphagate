"""服务端推理管线：行情 -> 状态 -> 门控 -> 决策。"""
from __future__ import annotations

from typing import Dict, List, Optional

from alphagate.core.market_regime import MarketRegime
from alphagate.core.strategy_idea import StrategyIdea
from alphagate.data.indicators import compute_regime_indicators
from alphagate.data.market_data import MarketDataHub
from alphagate.gate.engine import SemanticGate
from alphagate.gate.regime_builder import RegimeBuilder
from alphagate.strategies.library import StrategyLibrary


class InferencePipeline:
    """端到端推理管线：数据 -> 门控 -> 可解释配置决策。"""

    def __init__(
        self,
        data_source: str = "mock",
        embedder: str = "hash",
        threshold: float = 0.20,
    ) -> None:
        self.hub = MarketDataHub(data_source)
        self.regime_builder = RegimeBuilder()
        self.gate = SemanticGate(embedder=embedder, threshold=threshold)
        self.library = StrategyLibrary()

    def decide(
        self,
        symbols: List[str],
        indicators: Optional[Dict[str, float]] = None,
        news: Optional[List[str]] = None,
        start: str = "2025-01-01",
        end: str = "2026-01-01",
    ):
        """执行一次配置决策。"""
        if indicators is None:
            prices = self.hub.get_prices(symbols, start, end)
            indicators = compute_regime_indicators(prices)
        if news is None:
            news = self.hub.get_news(symbols, limit=10)
        regime: MarketRegime = self.regime_builder.build(indicators, news)
        ideas: List[StrategyIdea] = self.library.ideas()
        decision = self.gate.decide(regime, ideas)
        return regime, decision
