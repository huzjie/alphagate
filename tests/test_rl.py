"""两阶段 RL 单测。"""
from alphagate.rl.trainer import TwoStageTrainer


def test_two_stage_trainer_runs():
    strategies = ["value", "momentum", "quality", "defensive"]
    trainer = TwoStageTrainer(strategies)
    report = trainer.run(iterations=5)
    assert "stage2_best_threshold" in report
    assert 0.05 <= report["stage2_best_threshold"] <= 0.95
