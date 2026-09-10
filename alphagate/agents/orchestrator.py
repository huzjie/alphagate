"""编排器：研究员 -> 配置官 -> 风控官 -> 报告官。"""
from __future__ import annotations

from typing import Any, Dict, List

from alphagate.agents.allocator import AllocatorAgent
from alphagate.agents.base import AgentResult
from alphagate.agents.reporter import ReporterAgent
from alphagate.agents.researcher import ResearcherAgent
from alphagate.agents.risk import RiskAgent


class AgentOrchestrator:
    """四智能体串行流水线。"""

    def __init__(self, data_source: str = "mock", threshold: float = 0.20) -> None:
        self.researcher = ResearcherAgent(data_source)
        self.allocator = AllocatorAgent(threshold)
        self.risk = RiskAgent()
        self.reporter = ReporterAgent()

    def run(self, symbols: List[str], **kwargs) -> Dict[str, Any]:
        """执行完整流水线，返回聚合结果。"""
        results: List[AgentResult] = []
        ctx: Dict[str, Any] = {"symbols": symbols, **kwargs}

        r1 = self.researcher.run(ctx)
        results.append(r1)
        if not r1.ok:
            return {"ok": False, "results": [r.to_dict() if hasattr(r, "to_dict") else r for r in results], "error": r1.error}
        ctx["regime"] = r1.payload["regime"]

        r2 = self.allocator.run(ctx)
        results.append(r2)
        if not r2.ok:
            return {"ok": False, "results": results, "error": r2.error}
        ctx["decision"] = r2.payload["decision"]
        ctx["weights"] = r2.payload["weights"]

        r3 = self.risk.run(ctx)
        results.append(r3)
        ctx["risk"] = r3.payload if r3.ok else {"passed": False, "issues": [r3.error]}

        r4 = self.reporter.run(ctx)
        results.append(r4)

        return {
            "ok": all(r.ok for r in results[:3]),
            "regime": ctx.get("regime"),
            "weights": ctx.get("weights"),
            "risk": ctx.get("risk"),
            "report": r4.payload.get("report", "") if r4.ok else "",
            "results": results,
        }
