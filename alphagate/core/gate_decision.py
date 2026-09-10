"""门控决策结果：哪些思路被放行、各多少权重、为何。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class GatedIdea:
    """一条被门控后的思路：放行与否 + 语义匹配分 + 解释。"""

    name: str
    allowed: bool
    score: float
    reason: str
    weight: float = 0.0


@dataclass
class GateDecision:
    """一次门控决策的完整结果。"""

    regime_text: str = ""
    ideas: List[GatedIdea] = field(default_factory=list)
    rationale: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def allowed(self) -> List[GatedIdea]:
        return [i for i in self.ideas if i.allowed]

    @property
    def active_weights(self) -> Dict[str, float]:
        return {i.name: i.weight for i in self.ideas if i.allowed}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "regime_text": self.regime_text,
            "ideas": [
                {"name": i.name, "allowed": i.allowed, "score": round(i.score, 4),
                 "reason": i.reason, "weight": round(i.weight, 6)}
                for i in self.ideas
            ],
            "rationale": self.rationale,
            "metadata": self.metadata,
        }
