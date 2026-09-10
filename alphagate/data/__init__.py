"""数据层：行情接入、新闻、因子、指标计算。"""
from alphagate.data.market_data import MarketDataHub
from alphagate.data.indicators import compute_regime_indicators
from alphagate.data.factors import compute_factor_exposures

__all__ = ["MarketDataHub", "compute_regime_indicators", "compute_factor_exposures"]
