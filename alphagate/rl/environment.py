"""配置决策环境：状态 = 市场状态，动作 = 各思路权重，奖励 = 组合表现。"""
from __future__ import annotations

from typing import Dict, List, Tuple

import math


class AllocationEnv:
    """简化单步配置环境，用于 GRPO 风格的奖励计算。"""

    def __init__(self, n_assets: int = 12, risk_aversion: float = 1.0) -> None:
        self.n_assets = n_assets
        self.risk_aversion = risk_aversion

    def reward(self, weights: List[float], returns: List[float]) -> float:
        """奖励 = 组合收益 - 风险厌恶 * 集中度惩罚。"""
        if not weights or len(weights) != len(returns):
            return 0.0
        port_return = sum(w * r for w, r in zip(weights, returns))
        # Herfindahl 集中度
        concentration = sum(w * w for w in weights)
        penalty = self.risk_aversion * concentration
        return port_return - penalty

    def normalize(self, weights: List[float]) -> List[float]:
        total = sum(max(w, 0.0) for w in weights) or 1.0
        return [max(w, 0.0) / total for w in weights]


class AllocationTrajectory:
    """一段回测轨迹，用于计算分步奖励。"""

    def __init__(self, env: AllocationEnv) -> None:
        self.env = env
        self.returns_history: List[List[float]] = []
        self.weight_history: List[List[float]] = []

    def step(self, weights: List[float], returns: List[float]) -> float:
        w = self.env.normalize(weights)
        self.weight_history.append(w)
        self.returns_history.append(returns)
        return self.env.reward(w, returns)

    def mean_reward(self) -> float:
        if not self.weight_history:
            return 0.0
        rs = [
            self.env.reward(w, r)
            for w, r in zip(self.weight_history, self.returns_history)
        ]
        return sum(rs) / len(rs)
