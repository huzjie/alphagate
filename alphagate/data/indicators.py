"""市场状态指标：动量、波动、流动性、趋势等。"""
from __future__ import annotations

import statistics
from typing import Dict, List


def _returns(prices: List[float]) -> List[float]:
    return [(prices[i] / prices[i - 1] - 1) for i in range(1, len(prices))]


def momentum_20d(prices: List[float]) -> float:
    if len(prices) < 21:
        return 0.0
    return prices[-1] / prices[-21] - 1


def volatility_20d(prices: List[float]) -> float:
    r = _returns(prices)
    if len(r) < 2:
        return 0.0
    return statistics.pstdev(r[-20:]) * (252 ** 0.5)


def max_drawdown(prices: List[float]) -> float:
    peak = prices[0] if prices else 0.0
    mdd = 0.0
    for p in prices:
        peak = max(peak, p)
        if peak > 0:
            mdd = max(mdd, (peak - p) / peak)
    return mdd


def sharpe(prices: List[float], rf: float = 0.02) -> float:
    r = _returns(prices)
    if len(r) < 2:
        return 0.0
    mu = statistics.mean(r)
    sd = statistics.pstdev(r) or 1e-9
    return (mu * 252 - rf) / (sd * (252 ** 0.5))


def compute_regime_indicators(prices: Dict[str, List[float]]) -> Dict[str, float]:
    """聚合多资产价格为一组市场状态指标（等权合成指数）。"""
    if not prices:
        return {}
    n = min(len(p) for p in prices.values())
    if n == 0:
        return {}
    idx = []
    for i in range(n):
        avg = sum(p[i] for p in prices.values()) / len(prices)
        idx.append(avg)
    return {
        "momentum_20d": momentum_20d(idx),
        "volatility_20d": volatility_20d(idx),
        "max_drawdown": max_drawdown(idx),
        "sharpe": sharpe(idx),
        "return_20d": idx[-1] / idx[max(0, n - 21)] - 1 if n > 1 else 0.0,
        "liquidity_ratio": 0.5,  # 缺资金面数据时中性
    }
