"""市场状态构建：从行情指标 + 新闻摘要综合出 MarketRegime。"""
from __future__ import annotations

from typing import Dict, List, Optional

from alphagate.core.market_regime import MarketRegime, RegimeType


class RegimeBuilder:
    """把原始指标映射为结构化的市场状态，附新闻摘要。"""

    def __init__(self, thresholds: Optional[Dict[str, float]] = None) -> None:
        self.thresholds = thresholds or {
            "bull_momentum": 0.05,
            "bear_momentum": -0.05,
            "high_vol": 0.35,
        }

    def build(self, indicators: Dict[str, float], news: Optional[List[str]] = None) -> MarketRegime:
        news = news or []
        momentum = indicators.get("momentum_20d", indicators.get("return_20d", 0.0))
        vol = indicators.get("volatility_20d", indicators.get("volatility", 0.0))
        regime = RegimeType.SIDEWAYS
        description = "市场横盘震荡，动量与波动均处于中性区间"

        if momentum >= self.thresholds["bull_momentum"] and vol < self.thresholds["high_vol"]:
            regime = RegimeType.BULL
            description = "市场上行趋势确立，动量强劲且波动可控，风险偏好抬升"
        elif momentum <= self.thresholds["bear_momentum"] and vol < self.thresholds["high_vol"]:
            regime = RegimeType.BEAR
            description = "市场下行趋势，动量转弱，避险情绪升温"
        elif vol >= self.thresholds["high_vol"]:
            regime = RegimeType.HIGH_VOL
            description = "市场波动显著放大，不确定性上升，配置需强调防御与分散"
        elif indicators.get("liquidity_ratio", 0.0) > 0.8:
            regime = RegimeType.LIQUIDITY_DRIVEN
            description = "流动性极度宽松驱动，估值与资金面主导行情"

        confidence = 0.5 + min(abs(momentum) * 2.0, 0.4) + (0.1 if news else 0.0)
        confidence = min(confidence, 0.99)

        return MarketRegime(
            regime=regime,
            description=description,
            indicators=indicators,
            news_summaries=news,
            confidence=confidence,
        )
