"""配置思路：小盘（size）。"""
from __future__ import annotations

from typing import Dict, List, Optional

from alphagate.core.strategy_idea import StrategyIdea
from alphagate.strategies.base import BaseStrategy, build_idea


class SizeStrategy(BaseStrategy):
    """小盘思路：流动性宽松与风险偏好抬升阶段小盘股弹性更大。"""

    slug = "size"
    display_name = "小盘"

    def idea(self) -> StrategyIdea:
        return build_idea(
            name="小盘",
            rationale="流动性宽松与风险偏好抬升阶段小盘股弹性更大",
            applicable_regimes=['liquidity_driven', 'bull'],
            keywords=['size', '小盘', '弹性', '中小市值'],
            default_weight=0.08,
            risk_level="high",
        )

    def weights(self, universe: Dict[str, Dict[str, float]], **kwargs) -> Dict[str, float]:
        """基于因子暴露给出权重：因子分越高权重越大。"""
        factor = self.factor_key()
        scored = []
        for sym, feats in universe.items():
            score = feats.get(factor, feats.get("score", 0.0))
            scored.append((sym, max(score, 0.0)))
        if not scored:
            return {}
        total = sum(s for _, s in scored) or 1.0
        return {sym: s / total for sym, s in scored if s > 0}

    def factor_key(self) -> str:
        return "size"


STRATEGY = SizeStrategy()
