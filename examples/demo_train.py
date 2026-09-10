"""示例：两阶段 RL 训练。"""
from alphagate.rl.trainer import TwoStageTrainer
from alphagate.strategies.library import StrategyLibrary

trainer = TwoStageTrainer(StrategyLibrary().names())
report = trainer.run(iterations=20)
print("最佳阈值:", round(report["stage2_best_threshold"], 4))
print("最终奖励:", round(report["final_reward"], 4))
