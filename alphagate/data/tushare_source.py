"""Tushare 数据源（可选依赖）。"""
from __future__ import annotations

from typing import Dict, List

from alphagate.core.exceptions import DataError
from alphagate.data.base import DataSource
from alphagate.core.registry import DataSourceRegistry


@DataSourceRegistry.register("tushare")
class TushareDataSource(DataSource):
    """通过 tushare pro 获取 A 股数据。需 TUSHARE_TOKEN 与 pip install tushare。"""

    name = "tushare"

    def __init__(self, token: str = "") -> None:
        try:
            import tushare as ts  # type: ignore
            self.ts = ts
        except ImportError as e:
            raise DataError("tushare not installed; pip install tushare") from e
        self.token = token
        if token:
            ts.set_token(token)

    def get_prices(self, symbols: List[str], start: str, end: str) -> Dict[str, List[float]]:
        pro = self.ts.pro_api(self.token)
        out: Dict[str, List[float]] = {}
        for sym in symbols:
            code = sym.split(".")[0]
            df = pro.daily(ts_code=sym, start_date=start.replace("-", ""), end_date=end.replace("-", ""))
            out[sym] = [float(x) for x in df["close"].tolist()]
        return out

    def get_features(self, symbols: List[str]) -> Dict[str, Dict[str, float]]:
        return {s: {} for s in symbols}
