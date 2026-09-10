"""风控官 Agent：对配置方案做风控校验。"""
from __future__ import annotations

from typing import Any, Dict

from alphagate.agents.base import AgentResult, BaseAgent


class RiskAgent(BaseAgent):
    """风控官：检查集中度、单思路权重上限、空组合等。"""

    name = "risk"

    def __init__(self, max_single: float = 0.6, max_hhi: float = 0.35) -> None:
        self.max_single = max_single
        self.max_hhi = max_hhi

    def run(self, ctx: Dict[str, Any]) -> AgentResult:
        try:
            weights = ctx.get("weights", {})
            if not weights:
                return self._err(ValueError("empty portfolio"))
            max_w = max(weights.values())
            hhi = sum(w * w for w in weights.values())
            issues = []
            if max_w > self.max_single:
                issues.append(f"单思路权重 {max_w:.2f} 超上限 {self.max_single}")
            if hhi > self.max_hhi:
                issues.append(f"集中度 HHI {hhi:.2f} 超上限 {self.max_hhi}")
            return self._ok({
                "passed": not issues,
                "issues": issues,
                "max_weight": max_w,
                "hhi": hhi,
            })
        except Exception as e:  # noqa: BLE001
            return self._err(e)
