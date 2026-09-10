"""奖励模型：把「正确门控」转化为数值信号。"""
from __future__ import annotations

from typing import Dict, List

from alphagate.core.gate_decision import GatedIdea


class RewardModel:
    """规则化奖励：放行应放行的、拦截应拦截的、组合表现好。"""

    def __init__(self, hit_bonus: float = 1.0, miss_penalty: float = 0.5) -> None:
        self.hit_bonus = hit_bonus
        self.miss_penalty = miss_penalty

    def gating_reward(
        self,
        decisions: List[GatedIdea],
        ground_truth_allowed: List[str],
    ) -> float:
        """按 ground-truth 放行集合给出门控奖励。"""
        allowed_names = [g.name for g in decisions if g.allowed]
        gt = set(ground_truth_allowed)
        hits = len([n for n in allowed_names if n in gt])
        false_pos = len([n for n in allowed_names if n not in gt])
        false_neg = len([n for n in gt if n not in allowed_names])
        return self.hit_bonus * hits - self.miss_penalty * (false_pos + false_neg)

    def total_reward(
        self,
        decisions: List[GatedIdea],
        ground_truth_allowed: List[str],
        portfolio_return: float,
        alpha: float = 0.5,
    ) -> float:
        """综合门控正确性 + 组合收益。"""
        g = self.gating_reward(decisions, ground_truth_allowed)
        return alpha * g + (1 - alpha) * portfolio_return
