"""多源组合单测。"""
from alphagate.data.composite_source import CompositeDataSource


def test_composite_mock():
    src = CompositeDataSource(["mock", "mock"])
    prices = src.get_prices(["600000.SH"], "2025-01-01", "2026-01-01")
    assert "600000.SH" in prices
