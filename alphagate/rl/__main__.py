"""python -m alphagate.rl 快速自检：跑一个两阶段训练 demo。"""
from alphagate.rl.trainer import TwoStageTrainer


def main() -> int:
    strategies = ["value", "momentum", "quality", "low_volatility", "dividend",
                  "growth", "reversal", "trend_following", "defensive", "liquidity",
                  "size", "risk_parity"]
    trainer = TwoStageTrainer(strategies)
    report = trainer.run(iterations=15)
    print("Stage1 regime mapping:")
    for k, v in report["stage1_regime_mapping"].items():  # type: ignore
        print(f"  {k}: {v}")
    print(f"Stage2 best threshold = {report['stage2_best_threshold']:.4f}")
    print(f"Final reward = {report['final_reward']:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
