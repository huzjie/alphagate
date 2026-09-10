"""AKShare 数据源：A 股实时行情（可选依赖，无则抛错提示）。"""
from __future__ import annotations

from typing import Dict, List

from alphagate.core.exceptions import DataError
from alphagate.data.base import DataSource
from alphagate.core.registry import DataSourceRegistry


@DataSourceRegistry.register("akshare")
class AkShareDataSource(DataSource):
    """通过 akshare 获取 A 股行情与财务因子。需 pip install akshare。"""

    name = "akshare"

    def __init__(self) -> None:
        try:
            import akshare as ak  # type: ignore
            self.ak = ak
        except ImportError as e:
            raise DataError("akshare not installed; pip install akshare") from e

    def get_prices(self, symbols: List[str], start: str, end: str) -> Dict[str, List[float]]:
        out: Dict[str, List[float]] = {}
        for sym in symbols:
            try:
                df = self.ak.stock_zh_a_hist(symbol=sym, period="daily",
                                              start_date=start.replace("-", ""),
                                              end_date=end.replace("-", ""), adjust="qfq")
                out[sym] = [float(x) for x in df["收盘"].tolist()]
            except Exception as e:  # noqa: BLE001
                raise DataError(f"fetch {sym} failed: {e}") from e
        return out

    def get_features(self, symbols: List[str]) -> Dict[str, Dict[str, float]]:
        return {s: {} for s in symbols}
