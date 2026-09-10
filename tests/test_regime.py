"""市场状态建模单测。"""
from alphagate.gate.regime_builder import RegimeBuilder
from alphagate.core.market_regime import RegimeType


def test_bull_regime():
    b = RegimeBuilder()
    r = b.build({"momentum_20d": 0.1, "volatility_20d": 0.2})
    assert r.regime == RegimeType.BULL


def test_high_vol_regime():
    b = RegimeBuilder()
    r = b.build({"momentum_20d": 0.0, "volatility_20d": 0.5})
    assert r.regime == RegimeType.HIGH_VOL
