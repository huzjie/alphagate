"""python -m alphagate.gate 快速自检。"""
from alphagate.gate.engine import SemanticGate
from alphagate.core.market_regime import MarketRegime, RegimeType
from alphagate.core.strategy_idea import StrategyIdea
from alphagate.gate.explainer import explain


def main() -> int:
    regime = MarketRegime(
        regime=RegimeType.BULL,
        description="市场上行趋势确立，动量强劲且波动可控",
        indicators={"momentum_20d": 0.12, "volatility_20d": 0.18, "liquidity_ratio": 0.6},
        news_summaries=["央行维持宽松流动性", "企业盈利超预期"],
    )
    ideas = [
        StrategyIdea("动量", "趋势延续时顺势加仓强势板块，动量因子收益显著", ["bull"], ["momentum"], 0.3, risk_level="high"),
        StrategyIdea("价值", "低估值资产在均值回归时提供安全边际", ["sideways"], ["value"], 0.2),
        StrategyIdea("防御", "高波动环境降低仓位、增配红利与债券", ["high_volatility"], ["defensive"], 0.2),
        StrategyIdea("质量", "盈利质量稳定公司穿越周期", ["bull", "sideways"], ["quality"], 0.3),
    ]
    gate = SemanticGate(threshold=0.20)
    decision = gate.decide(regime, ideas)
    print(explain(decision))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
