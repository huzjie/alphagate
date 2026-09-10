"""数据清洗：缺失值、异常值、时间对齐。"""
from __future__ import annotations

import statistics
from typing import Dict, List


class Cleaner:
    """行情数据清洗工具。"""

    @staticmethod
    def drop_missing(prices: Dict[str, List[float]]) -> Dict[str, List[float]]:
        return {k: [p for p in v if p is not None] for k, v in prices.items()}

    @staticmethod
    def clip_outliers(values: List[float], k: float = 3.0) -> List[float]:
        if len(values) < 3:
            return values
        mu = statistics.mean(values)
        sd = statistics.pstdev(values) or 1e-9
        lo, hi = mu - k * sd, mu + k * sd
        return [max(lo, min(hi, v)) for v in values]

    @staticmethod
    def align_length(prices: Dict[str, List[float]]) -> Dict[str, List[float]]:
        if not prices:
            return prices
        n = min(len(v) for v in prices.values())
        return {k: v[:n] for k, v in prices.items()}
