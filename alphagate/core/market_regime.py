"""市场状态建模：把行情 + 新闻综合为结构化的「当前市场状态描述」。"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class RegimeType(str, Enum):
    """市场状态类别。"""

    BULL = "bull"
    BEAR = "bear"
    SIDEWAYS = "sideways"
    HIGH_VOL = "high_volatility"
    LIQUIDITY_DRIVEN = "liquidity_driven"
    RISK_OFF = "risk_off"
    UNKNOWN = "unknown"


@dataclass
class MarketRegime:
    """当前市场状态：行情指标 + 新闻摘要 + 结构化描述。"""

    regime: RegimeType = RegimeType.UNKNOWN
    description: str = ""
    indicators: Dict[str, float] = field(default_factory=dict)
    news_summaries: List[str] = field(default_factory=list)
    confidence: float = 0.0
    as_of: datetime = field(default_factory=datetime.now)

    def to_text(self) -> str:
        """拼成一段可供嵌入/匹配的自然语言市场状态描述。"""
        parts = [f"市场状态: {self.regime.value}", f"描述: {self.description}"]
        if self.indicators:
            kv = ", ".join(f"{k}={v:.3f}" for k, v in list(self.indicators.items())[:20])
            parts.append(f"指标: {kv}")
        if self.news_summaries:
            parts.append("新闻: " + " ".join(self.news_summaries[:5]))
        return "；".join(parts)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "regime": self.regime.value,
            "description": self.description,
            "indicators": self.indicators,
            "news_summaries": self.news_summaries,
            "confidence": self.confidence,
            "as_of": self.as_of.isoformat(),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "MarketRegime":
        try:
            regime = RegimeType(d.get("regime", "unknown"))
        except ValueError:
            regime = RegimeType.UNKNOWN
        return cls(
            regime=regime,
            description=d.get("description", ""),
            indicators=d.get("indicators", {}),
            news_summaries=d.get("news_summaries", []),
            confidence=float(d.get("confidence", 0.0)),
            as_of=datetime.fromisoformat(d.get("as_of", datetime.now().isoformat())),
        )
