"""配置官 Agent：基于市场状态做语义门控配置决策。"""
from __future__ import annotations

from typing import Any, Dict

from alphagate.agents.base import AgentResult, BaseAgent
from alphagate.core.market_regime import MarketRegime
from alphagate.gate.engine import SemanticGate
from alphagate.strategies.library import StrategyLibrary


class AllocatorAgent(BaseAgent):
    """配置官：把市场状态门控为具体配置权重。"""

    name = "allocator"

    def __init__(self, threshold: float = 0.20) -> None:
        self.gate = SemanticGate(threshold=threshold)
        self.library = StrategyLibrary()

    def run(self, ctx: Dict[str, Any]) -> AgentResult:
        try:
            regime = MarketRegime.from_dict(ctx["regime"])
            ideas = self.library.ideas()
            decision = self.gate.decide(regime, ideas)
            return self._ok({"decision": decision.to_dict(), "weights": decision.active_weights})
        except Exception as e:  # noqa: BLE001
            return self._err(e)
