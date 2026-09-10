"""两阶段强化学习训练框架（Alpha-R1 范式）。

Stage 1（偏好对齐）：用监督/偏好数据让模型学会「读懂市场 → 匹配思路」；
Stage 2（GRPO/RLHF）：用奖励信号强化「放行正确思路、拦截不相关思路」的决策。
"""
from alphagate.rl.trainer import TwoStageTrainer
from alphagate.rl.reward import RewardModel
from alphagate.rl.environment import AllocationEnv

__all__ = ["TwoStageTrainer", "RewardModel", "AllocationEnv"]
