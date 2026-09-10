"""组合风控：VaR、CVaR、波动率目标等。"""
from __future__ import annotations

import math
from typing import List, Optional


def historical_var(returns: List[float], alpha: float = 0.05) -> float:
    """历史模拟 VaR。"""
    if not returns:
        return 0.0
    sorted_ret = sorted(returns)
    idx = max(0, int(len(sorted_ret) * alpha) - 1)
    return -sorted_ret[idx]


def historical_cvar(returns: List[float], alpha: float = 0.05) -> float:
    """历史模拟 CVaR（ES）。"""
    if not returns:
        return 0.0
    sorted_ret = sorted(returns)
    cutoff = int(len(sorted_ret) * alpha)
    tail = sorted_ret[:max(cutoff, 1)]
    return -(sum(tail) / len(tail))


def vol_target_weights(cov: List[List[float]], target: float = 0.15) -> List[float]:
    """按目标波动率做风险预算（等风险贡献近似）。"""
    n = len(cov)
    if n == 0:
        return []
    inv_vol = [1.0 / (math.sqrt(max(cov[i][i], 1e-9))) for i in range(n)]
    total = sum(inv_vol) or 1.0
    return [v / total for v in inv_vol]
