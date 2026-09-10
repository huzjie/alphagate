"""研究员 Agent：采集数据，产出市场状态。"""
from __future__ import annotations

from typing import Any, Dict

from alphagate.agents.base import AgentResult, BaseAgent
from alphagate.data.indicators import compute_regime_indicators
from alphagate.data.market_data import MarketDataHub
from alphagate.gate.regime_builder import RegimeBuilder


class ResearcherAgent(BaseAgent):
    """研究员：拉行情、算指标、构建市场状态。"""

    name = "researcher"

    def __init__(self, data_source: str = "mock") -> None:
        self.hub = MarketDataHub(data_source)
        self.builder = RegimeBuilder()

    def run(self, ctx: Dict[str, Any]) -> AgentResult:
        try:
            symbols = ctx.get("symbols", ["600000.SH", "000001.SZ"])
            prices = self.hub.get_prices(symbols, ctx.get("start", "2025-01-01"), ctx.get("end", "2026-01-01"))
            indicators = compute_regime_indicators(prices)
            news = self.hub.get_news(symbols, limit=10)
            regime = self.builder.build(indicators, news)
            return self._ok({"regime": regime.to_dict(), "prices": {k: v[-60:] for k, v in list(prices.items())[:20]}})
        except Exception as e:  # noqa: BLE001
            return self._err(e)
