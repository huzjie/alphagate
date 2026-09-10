"""Wind 数据源骨架（需 WindPy 与授权，占位可扩展）。"""
from __future__ import annotations

from typing import Dict, List

from alphagate.core.exceptions import DataError
from alphagate.data.base import DataSource
from alphagate.core.registry import DataSourceRegistry


@DataSourceRegistry.register("wind")
class WindDataSource(DataSource):
    """Wind 金融终端数据源。需安装 WindPy 并登录。"""

    name = "wind"

    def __init__(self) -> None:
        try:
            from WindPy import w  # type: ignore
            self.w = w
        except ImportError as e:
            raise DataError("WindPy not installed") from e

    def get_prices(self, symbols: List[str], start: str, end: str) -> Dict[str, List[float]]:
        self.w.start()
        out: Dict[str, List[float]] = {}
        for sym in symbols:
            err, df = self.w.wsd(sym, "close", start, end)
            if err:
                raise DataError(f"wind fetch {sym} failed")
            out[sym] = [float(x) for x in df.Data[0]]
        return out

    def get_features(self, symbols: List[str]) -> Dict[str, Dict[str, float]]:
        return {s: {} for s in symbols}
