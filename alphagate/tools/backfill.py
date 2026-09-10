"""数据回填：前向/插值填充缺失价格。"""
from __future__ import annotations

from typing import Dict, List


def forward_fill(values: List[float]) -> List[float]:
    out: List[float] = []
    last = None
    for v in values:
        if v is None:
            out.append(last)
        else:
            last = v
            out.append(v)
    return out


def linear_interpolate(values: List[float]) -> List[float]:
    out = list(values)
    for i in range(len(out)):
        if out[i] is not None:
            continue
        lo = next((j for j in range(i, -1, -1) if out[j] is not None), None)
        hi = next((j for j in range(i + 1, len(out)) if out[j] is not None), None)
        if lo is not None and hi is not None:
            out[i] = out[lo] + (out[hi] - out[lo]) * (i - lo) / (hi - lo)
        elif lo is not None:
            out[i] = out[lo]
        elif hi is not None:
            out[i] = out[hi]
    return out


def backfill_prices(prices: Dict[str, List[float]], method: str = "ffill") -> Dict[str, List[float]]:
    fn = forward_fill if method == "ffill" else linear_interpolate
    return {k: fn(v) for k, v in prices.items()}
