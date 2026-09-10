"""CSV 数据源：从本地 CSV 读取行情（列：date,symbol,close,volume）。"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List

from alphagate.core.exceptions import DataError
from alphagate.data.base import DataSource
from alphagate.core.registry import DataSourceRegistry


@DataSourceRegistry.register("csv")
class CsvDataSource(DataSource):
    """读取本地 CSV 文件作为行情来源。"""

    name = "csv"

    def __init__(self, path: str) -> None:
        self.path = Path(path)
        if not self.path.exists():
            raise DataError(f"csv not found: {self.path}")
        self._rows = self._load()

    def _load(self) -> List[dict]:
        with self.path.open("r", encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))

    def get_prices(self, symbols: List[str], start: str, end: str) -> Dict[str, List[float]]:
        out: Dict[str, List[float]] = {}
        for row in self._rows:
            sym = row.get("symbol", "")
            if sym not in symbols:
                continue
            try:
                px = float(row.get("close", "0"))
            except ValueError:
                continue
            out.setdefault(sym, []).append(px)
        return out

    def get_features(self, symbols: List[str]) -> Dict[str, Dict[str, float]]:
        # CSV 无因子时返回空暴露，交由因子计算模块派生
        return {s: {} for s in symbols}
