"""信号生成：把权重/因子转为离散交易信号。"""
from __future__ import annotations

from typing import Dict, List


def weights_to_signals(weights: Dict[str, float], top_n: int = 3) -> Dict[str, str]:
    """按权重排序，前 top_n 给 BUY，其余 HOLD。"""
    ranked = sorted(weights.items(), key=lambda x: -x[1])
    sig = {}
    for i, (name, w) in enumerate(ranked):
        if w <= 0:
            sig[name] = "HOLD"
        elif i < top_n:
            sig[name] = "BUY"
        else:
            sig[name] = "HOLD"
    return sig


def crossover(a: List[float], b: List[float]) -> List[int]:
    """金叉/死叉信号序列：1 金叉，-1 死叉，0 无。"""
    sig = []
    prev = 0
    for i in range(1, len(a)):
        diff = a[i] - b[i]
        pdiff = a[i - 1] - b[i - 1]
        if pdiff <= 0 < diff:
            sig.append(1)
        elif pdiff >= 0 > diff:
            sig.append(-1)
        else:
            sig.append(0)
    return sig
