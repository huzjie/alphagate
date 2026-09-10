"""数据层单测。"""
from alphagate.data.market_data import MarketDataHub
from alphagate.data.indicators import compute_regime_indicators


def test_mock_prices_and_indicators():
    hub = MarketDataHub("mock")
    prices = hub.get_prices(["600000.SH", "000001.SZ"], "2025-01-01", "2026-01-01")
    assert len(prices) == 2
    ind = compute_regime_indicators(prices)
    assert "momentum_20d" in ind
