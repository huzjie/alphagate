"""语义门控单测。"""
from alphagate.core.market_regime import MarketRegime, RegimeType
from alphagate.core.strategy_idea import StrategyIdea
from alphagate.gate.engine import SemanticGate


def test_gate_decide_allows_relevant():
    regime = MarketRegime(regime=RegimeType.BULL, description="上行趋势", indicators={"momentum_20d": 0.1})
    ideas = [
        StrategyIdea("动量", "趋势延续时顺势加仓强势板块", ["bull"], ["momentum"]),
        StrategyIdea("防御", "高波动环境降低仓位", ["high_volatility"], ["defensive"]),
    ]
    gate = SemanticGate(threshold=0.01)
    decision = gate.decide(regime, ideas)
    assert decision.allowed, "should allow at least one"
    total = sum(g.weight for g in decision.allowed)
    assert abs(total - 1.0) < 1e-6


def test_gate_empty_ideas_raises():
    from alphagate.core.exceptions import GateError
    gate = SemanticGate()
    try:
        gate.decide(MarketRegime(), [])
    except GateError:
        pass
    else:
        raise AssertionError("expected GateError")
