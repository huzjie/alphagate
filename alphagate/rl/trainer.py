"""两阶段训练编排：Stage1 偏好对齐 -> Stage2 GRPO 优化。"""
from __future__ import annotations

from typing import Callable, Dict, List, Optional

from alphagate.rl.reward import RewardModel
from alphagate.rl.stage1 import Stage1PreferenceAligner
from alphagate.rl.stage2 import GRPOOptimizer


class TwoStageTrainer:
    """端到端编排两阶段强化学习训练。"""

    def __init__(self, strategies: List[str]) -> None:
        self.strategies = strategies
        self.reward = RewardModel()
        self.stage1 = Stage1PreferenceAligner(strategies)
        self.stage2 = GRPOOptimizer()

    def run(
        self,
        evaluate_fn: Optional[Callable[[float], float]] = None,
        iterations: int = 20,
    ) -> Dict[str, object]:
        """执行完整训练，返回报告。"""
        mapping = self.stage1.align()
        if evaluate_fn is None:
            evaluate_fn = lambda t: t * (1 - t)  # 默认抛物线，最优在 0.5
        best_threshold, history = self.stage2.update(evaluate_fn, iterations)
        return {
            "stage1_regime_mapping": mapping,
            "stage2_best_threshold": best_threshold,
            "stage2_reward_history": history,
            "final_reward": history[-1] if history else 0.0,
        }
