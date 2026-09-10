"""回测引擎：端到端跑一遍门控决策 + 组合表现。"""
from __future__ import annotations

from typing import Dict, List, Optional

from alphagate.backtest.metrics import performance_metrics
from alphagate.backtest.portfolio import build_portfolio
from alphagate.data.market_data import MarketDataHub
from alphagate.serving.pipeline import InferencePipeline


def run_backtest(
    symbols: List[str],
    start: str = "2025-01-01",
    end: str = "2026-01-01",
    initial_capital: float = 1_000_000.0,
    data_source: str = "mock",
) -> Dict[str, object]:
    """执行回测：决策 -> 权重 -> 组合净值 -> 绩效。"""
    hub = MarketDataHub(data_source)
    prices = hub.get_prices(symbols, start, end)
    pipe = InferencePipeline(data_source=data_source)
    regime, decision = pipe.decide(symbols, start=start, end=end)
    weights = decision.active_weights

    # 把策略权重映射到资产：用因子暴露 + 策略权重合成资产权重
    feats = hub.get_features(symbols)
    asset_weights: Dict[str, float] = {}
    for sym in symbols:
        w = 0.0
        for idea_name, idea_w in weights.items():
            f = feats.get(sym, {}).get(idea_name, 0.0)
            w += idea_w * max(f, 0.0)
        asset_weights[sym] = w
    total = sum(asset_weights.values()) or 1.0
    asset_weights = {s: w / total for s, w in asset_weights.items() if w > 0}

    nav_map = build_portfolio(asset_weights, prices)
    nav = nav_map.get("portfolio", [])
    metrics = performance_metrics(nav)

    return {
        "regime": regime.to_dict(),
        "strategy_weights": weights,
        "asset_weights": {k: round(v, 4) for k, v in asset_weights.items()},
        "metrics": metrics,
        "nav": [round(x, 4) for x in nav],
    }
