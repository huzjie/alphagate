"""绩效与风控指标：年化收益、波动、夏普、最大回撤、卡玛。"""
from __future__ import annotations

import statistics
from typing import Dict, List

from alphagate.data.indicators import max_drawdown, sharpe, volatility_20d


def _annual_return(nav: List[float], periods_per_year: int = 252) -> float:
    if len(nav) < 2 or nav[0] <= 0:
        return 0.0
    years = (len(nav) - 1) / periods_per_year
    if years <= 0:
        return 0.0
    return (nav[-1] / nav[0]) ** (1 / years) - 1


def performance_metrics(nav: List[float], rf: float = 0.02) -> Dict[str, float]:
    """计算一组绩效指标。"""
    if not nav:
        return {}
    vol = volatility_20d(nav)
    shp = sharpe(nav, rf)
    mdd = max_drawdown(nav)
    ann = _annual_return(nav)
    calmar = ann / mdd if mdd > 0 else 0.0
    return {
        "annual_return": round(ann, 4),
        "annual_volatility": round(vol, 4),
        "sharpe_ratio": round(shp, 4),
        "max_drawdown": round(mdd, 4),
        "calmar_ratio": round(calmar, 4),
        "final_nav": round(nav[-1], 4) if nav else 0.0,
    }
