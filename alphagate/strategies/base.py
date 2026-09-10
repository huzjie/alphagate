"""策略基类与思路构造工具。"""
from __future__ import annotations

from typing import Dict, List, Optional

from alphagate.core.strategy_idea import StrategyIdea


def build_idea(
    name: str,
    rationale: str,
    applicable_regimes: Optional[List[str]] = None,
    keywords: Optional[List[str]] = None,
    default_weight: float = 0.0,
    min_weight: float = 0.0,
    max_weight: float = 1.0,
    risk_level: str = "medium",
) -> StrategyIdea:
    return StrategyIdea(
        name=name,
        rationale=rationale,
        applicable_regimes=applicable_regimes or [],
        keywords=keywords or [],
        default_weight=default_weight,
        min_weight=min_weight,
        max_weight=max_weight,
        risk_level=risk_level,
    )


class BaseStrategy:
    """所有配置思路的基类。子类实现 idea() 与 weights()。"""

    slug: str = ""
    display_name: str = ""

    def idea(self) -> StrategyIdea:  # pragma: no cover - 抽象
        raise NotImplementedError

    def weights(self, universe: Dict[str, Dict[str, float]], **kwargs) -> Dict[str, float]:  # pragma: no cover
        raise NotImplementedError

    def factor_key(self) -> str:
        return self.slug
