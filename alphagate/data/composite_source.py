"""多源组合：主源失败时回退备用源。"""
from __future__ import annotations

from typing import Dict, List

from alphagate.core.exceptions import DataError
from alphagate.data.base import DataSource
from alphagate.core.registry import DataSourceRegistry
from alphagate.data.market_data import MarketDataHub


@DataSourceRegistry.register("composite")
class CompositeDataSource(DataSource):
    """组合多个数据源，主源优先、失败回退。"""

    name = "composite"

    def __init__(self, sources: List[str], **kwargs) -> None:
        self.sources = sources
        self.kwargs = kwargs

    def _hubs(self):
        return [MarketDataHub(s, **self.kwargs) for s in self.sources]

    def get_prices(self, symbols: List[str], start: str, end: str) -> Dict[str, List[float]]:
        last_err = None
        for hub in self._hubs():
            try:
                return hub.get_prices(symbols, start, end)
            except Exception as e:  # noqa: BLE001
                last_err = e
        raise DataError(f"all sources failed: {last_err}")

    def get_features(self, symbols: List[str]) -> Dict[str, Dict[str, float]]:
        for hub in self._hubs():
            try:
                return hub.get_features(symbols)
            except Exception:  # noqa: BLE001
                continue
        return {s: {} for s in symbols}
