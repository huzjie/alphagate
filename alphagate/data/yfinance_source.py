"""Yahoo Finance 数据源（可选依赖）。"""
from __future__ import annotations

from typing import Dict, List

from alphagate.core.exceptions import DataError
from alphagate.data.base import DataSource
from alphagate.core.registry import DataSourceRegistry


@DataSourceRegistry.register("yfinance")
class YFinanceDataSource(DataSource):
    """通过 yfinance 获取海外市场行情。"""

    name = "yfinance"

    def __init__(self) -> None:
        try:
            import yfinance as yf  # type: ignore
            self.yf = yf
        except ImportError as e:
            raise DataError("yfinance not installed; pip install yfinance") from e

    def get_prices(self, symbols: List[str], start: str, end: str) -> Dict[str, List[float]]:
        out: Dict[str, List[float]] = {}
        for sym in symbols:
            df = self.yf.download(sym, start=start, end=end, progress=False)
            out[sym] = [float(x) for x in df["Close"].tolist()]
        return out

    def get_features(self, symbols: List[str]) -> Dict[str, Dict[str, float]]:
        return {s: {} for s in symbols}
