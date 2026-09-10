"""配置思路：一条候选资产配置逻辑及其「经济逻辑说明书」。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class StrategyIdea:
    """一条配置思路 = 名字 + 逻辑说明书(rationale) + 适配环境 + 权重建议。"""

    name: str
    rationale: str
    applicable_regimes: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    default_weight: float = 0.0
    min_weight: float = 0.0
    max_weight: float = 1.0
    risk_level: str = "medium"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_text(self) -> str:
        """拼接逻辑说明书用于语义匹配。"""
        return f"{self.name}：{self.rationale}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "rationale": self.rationale,
            "applicable_regimes": self.applicable_regimes,
            "keywords": self.keywords,
            "default_weight": self.default_weight,
            "min_weight": self.min_weight,
            "max_weight": self.max_weight,
            "risk_level": self.risk_level,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "StrategyIdea":
        return cls(
            name=d["name"],
            rationale=d.get("rationale", ""),
            applicable_regimes=d.get("applicable_regimes", []),
            keywords=d.get("keywords", []),
            default_weight=float(d.get("default_weight", 0.0)),
            min_weight=float(d.get("min_weight", 0.0)),
            max_weight=float(d.get("max_weight", 1.0)),
            risk_level=d.get("risk_level", "medium"),
            metadata=d.get("metadata", {}),
        )
