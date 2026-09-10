"""因子暴露派生：从价格序列计算各策略所需的因子分（0~1 归一）。"""
from __future__ import annotations

from typing import Dict, List

from alphagate.data.indicators import momentum_20d, volatility_20d


def _norm01(vals: List[float]) -> List[float]:
    if not vals:
        return vals
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return [0.5 for _ in vals]
    return [(v - lo) / (hi - lo) for v in vals]


def compute_factor_exposures(prices: Dict[str, List[float]]) -> Dict[str, Dict[str, float]]:
    """从价格派生一套基础因子暴露（与策略 slug 对齐）。"""
    syms = list(prices.keys())
    feats: Dict[str, Dict[str, float]] = {s: {} for s in syms}

    momentum = {s: momentum_20d(p) for s, p in prices.items()}
    vol = {s: volatility_20d(p) for s, p in prices.items()}
    m_norm = _norm01([momentum[s] for s in syms])
    v_norm = _norm01([vol[s] for s in syms])

    for i, s in enumerate(syms):
        feats[s].update({
            "momentum": round(m_norm[i], 4),
            "trend_following": round(m_norm[i], 4),
            "reversal": round(1 - m_norm[i], 4),
            "low_volatility": round(1 - v_norm[i], 4),
            "defensive": round(1 - v_norm[i], 4),
            "volatility": round(vol[s], 4),
            "score": round(m_norm[i], 4),
        })
    return feats
