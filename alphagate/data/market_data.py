"""行情数据中枢：统一多源适配，缓存 + 因子派生。"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from alphagate.core.exceptions import DataError
from alphagate.core.registry import DataSourceRegistry
from alphagate.data.base import DataSource
from alphagate.core.registry import DataSourceRegistry
from alphagate.data.csv_source import CsvDataSource
from alphagate.data.mock_source import MockDataSource
from alphagate.data.akshare_source import AkShareDataSource  # noqa: F401 - 注册


class MarketDataHub:
    """统一数据入口：按配置路由到具体数据源。"""

    def __init__(self, source: str = "mock", **kwargs) -> None:
        self.source_name = source
        self.kwargs = kwargs
        self._source: Optional[DataSource] = None

    def source(self) -> DataSource:
        if self._source is None:
            self._source = DataSourceRegistry.get(self.source_name, **self.kwargs)
        return self._source

    def get_prices(self, symbols: List[str], start: str, end: str) -> Dict[str, List[float]]:
        return self.source().get_prices(symbols, start, end)

    def get_features(self, symbols: List[str]) -> Dict[str, Dict[str, float]]:
        feats = self.source().get_features(symbols)
        from alphagate.data.factors import compute_factor_exposures
        # 若源未给因子，则从价格派生
        for sym in symbols:
            if not feats.get(sym):
                feats[sym] = {}
        return feats

    def get_news(self, symbols: List[str], limit: int = 20) -> List[str]:
        return self.source().get_news(symbols, limit)
