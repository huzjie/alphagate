"""回测单测。"""
from alphagate.backtest.engine import run_backtest


def test_run_backtest_returns_metrics():
    result = run_backtest(["600000.SH", "000001.SZ", "600519.SH"])
    assert "metrics" in result
    assert "sharpe_ratio" in result["metrics"]
