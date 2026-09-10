"""绩效归因：把组合收益拆到各策略/资产贡献。"""
from __future__ import annotations

from typing import Dict, List, Tuple


def attribute_returns(
    asset_weights: Dict[str, float],
    prices: Dict[str, List[float]],
) -> List[Tuple[str, float, float]]:
    """返回 [(asset, weight, contribution)]，贡献 = 权重 * 期间收益。"""
    out: List[Tuple[str, float, float]] = []
    for sym, w in asset_weights.items():
        px = prices.get(sym)
        if not px or len(px) < 2:
            continue
        ret = px[-1] / px[0] - 1
        out.append((sym, w, w * ret))
    out.sort(key=lambda x: -x[2])
    return out
