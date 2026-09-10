"""指标单测。"""
from alphagate.data.indicators import max_drawdown, momentum_20d, sharpe, volatility_20d


def test_momentum():
    prices = list(range(1, 50))
    assert momentum_20d(prices) > 0


def test_max_drawdown_monotonic_zero():
    assert max_drawdown([1, 2, 3, 4]) == 0.0
