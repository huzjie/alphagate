"""Stage 2：GRPO 风格组相对策略优化（轻量、无框架依赖实现）。"""
from __future__ import annotations

import math
from typing import Callable, List, Tuple


class GRPOOptimizer:
    """极简 GRPO：对一组采样动作按相对优势做策略梯度式更新。

    这里以「阈值微调」为可学习参数，演示组内相对奖励驱动的更新。
    """

    def __init__(self, lr: float = 0.01, clip: float = 0.2) -> None:
        self.lr = lr
        self.clip = clip
        self.threshold = 0.35

    def sample_group(self, base: float, n: int = 8) -> List[float]:
        """围绕 base 采样一组阈值。"""
        return [base + (i - n / 2) * 0.02 for i in range(n)]

    def advantages(self, rewards: List[float]) -> List[float]:
        mu = sum(rewards) / len(rewards)
        sigma = math.sqrt(sum((r - mu) ** 2 for r in rewards) / len(rewards)) or 1.0
        return [(r - mu) / sigma for r in rewards]

    def update(
        self,
        evaluate: Callable[[float], float],
        iterations: int = 20,
    ) -> Tuple[float, List[float]]:
        """迭代更新阈值，最大化评估函数。返回最终阈值与历史奖励。"""
        history: List[float] = []
        best = (self.threshold, -1e9)
        for _ in range(iterations):
            group = self.sample_group(self.threshold)
            rewards = [evaluate(t) for t in group]
            advs = self.advantages(rewards)
            for t, a in zip(group, advs):
                self.threshold += self.lr * a * self.clip
            self.threshold = max(0.05, min(0.95, self.threshold))
            r = evaluate(self.threshold)
            history.append(r)
            if r > best[1]:
                best = (self.threshold, r)
        self.threshold = best[0]
        return self.threshold, history
