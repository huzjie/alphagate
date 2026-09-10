"""绩效指标单测。"""
from alphagate.backtest.metrics import performance_metrics


def test_metrics_on_up_series():
    nav = [1.0 + i * 0.01 for i in range(100)]
    m = performance_metrics(nav)
    assert m["annual_return"] > 0
    assert "sharpe_ratio" in m
