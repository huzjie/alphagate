"""组合构建：由门控权重 + 资产价格生成组合净值。"""
from __future__ import annotations

from typing import Dict, List


def build_portfolio(
    weights: Dict[str, float],
    prices: Dict[str, List[float]],
) -> Dict[str, List[float]]:
    """按权重合成组合净值序列（简单持有 + 定期再平衡）。"""
    syms = [s for s in weights if s in prices]
    if not syms:
        return {}
    n = min(len(prices[s]) for s in syms)
    nav = []
    nav_val = 1.0
    for i in range(n):
        day_ret = sum(weights[s] * (prices[s][i] / prices[s][max(0, i - 1)] - 1)
                      for s in syms if i > 0)
        if i == 0:
            nav_val = 1.0
        else:
            nav_val *= (1 + day_ret)
        nav.append(nav_val)
    return {"portfolio": nav}
