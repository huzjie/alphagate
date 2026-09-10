"""运行时上下文：贯穿一次配置决策的请求与状态。"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from alphagate.core.market_regime import MarketRegime
from alphagate.core.strategy_idea import StrategyIdea


@dataclass
class GateContext:
    """一次语义门控决策的完整上下文。"""

    as_of: datetime = field(default_factory=datetime.now)
    regime: Optional[MarketRegime] = None
    ideas: List[StrategyIdea] = field(default_factory=list)
    candidate_weights: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "as_of": self.as_of.isoformat(),
            "regime": self.regime.to_dict() if self.regime else None,
            "ideas": [i.to_dict() for i in self.ideas],
            "candidate_weights": self.candidate_weights,
            "metadata": self.metadata,
        }
