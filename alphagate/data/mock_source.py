"""离线 Mock 数据源：确定性合成行情与因子，无网络即可跑通全链路。"""
from __future__ import annotations

import hashlib
import math
from datetime import datetime, timedelta
from typing import Dict, List

from alphagate.data.base import DataSource
from alphagate.core.registry import DataSourceRegistry


@DataSourceRegistry.register("mock")
class MockDataSource(DataSource):
    """用确定性伪随机生成行情，保证可复现、可离线。"""

    name = "mock"

    def __init__(self, seed: int = 42) -> None:
        self.seed = seed

    def _rng(self, sym: str, i: int) -> float:
        h = hashlib.md5(f"{self.seed}:{sym}:{i}".encode("utf-8")).digest()
        return int.from_bytes(h[:4], "big") / 0xFFFFFFFF

    def get_prices(self, symbols: List[str], start: str, end: str) -> Dict[str, List[float]]:
        n = 250  # 约一年交易日
        out: Dict[str, List[float]] = {}
        for s, sym in enumerate(symbols):
            base = 10 + self._rng(sym, 0) * 90
            drift = 0.0003 + self._rng(sym, 1) * 0.0008
            prices = []
            px = base
            for i in range(n):
                shock = (self._rng(sym, i + 2) - 0.5) * 0.04
                px = max(px * (1 + drift + shock), 0.5)
                prices.append(round(px, 4))
            out[sym] = prices
        return out

    def get_features(self, symbols: List[str]) -> Dict[str, Dict[str, float]]:
        out: Dict[str, Dict[str, float]] = {}
        for s, sym in enumerate(symbols):
            out[sym] = {
                "value": round(self._rng(sym, 100), 4),
                "momentum": round(self._rng(sym, 101), 4),
                "quality": round(self._rng(sym, 102), 4),
                "low_volatility": round(1 - self._rng(sym, 103), 4),
                "dividend": round(self._rng(sym, 104), 4),
                "growth": round(self._rng(sym, 105), 4),
                "reversal": round(self._rng(sym, 106), 4),
                "trend_following": round(self._rng(sym, 107), 4),
                "defensive": round(self._rng(sym, 108), 4),
                "liquidity": round(self._rng(sym, 109), 4),
                "size": round(self._rng(sym, 110), 4),
                "risk_parity": round(1 / 12, 4),
                "beta": round(self._rng(sym, 111), 4),
                "pe": round(5 + self._rng(sym, 112) * 40, 2),
                "roe": round(0.02 + self._rng(sym, 113) * 0.28, 4),
                "volatility": round(0.10 + self._rng(sym, 114) * 0.5, 4),
                "score": round(self._rng(sym, 115), 4),
            }
        return out

    def get_news(self, symbols: List[str], limit: int = 20) -> List[str]:
        samples = [
            "央行维持流动性合理充裕，政策利率维持不变",
            "制造业 PMI 回升至荣枯线上方，经济景气度改善",
            "北向资金连续净流入，外资增配核心资产",
            "多家上市公司中报盈利超预期",
            "国际油价波动加剧，能源板块分化",
            "科技成长板块估值处于历史中高位",
        ]
        out = []
        for i in range(min(limit, len(samples))):
            out.append(samples[(i + self.seed) % len(samples)])
        return out
