"""报告官 Agent：把决策与风控结果写成报告。"""
from __future__ import annotations

from typing import Any, Dict

from alphagate.agents.base import AgentResult, BaseAgent


class ReporterAgent(BaseAgent):
    """报告官：生成 Markdown 报告。"""

    name = "reporter"

    def run(self, ctx: Dict[str, Any]) -> AgentResult:
        try:
            regime = ctx.get("regime", {})
            decision = ctx.get("decision", {})
            risk = ctx.get("risk", {})
            lines = ["# AlphaGate 配置决策报告", ""]
            lines.append(f"- 市场状态：{regime.get('regime', 'unknown')}")
            lines.append(f"- 状态描述：{regime.get('description', '')}")
            lines.append("")
            lines.append("## 放行思路与权重")
            for i in decision.get("ideas", []):
                if i.get("allowed"):
                    lines.append(f"- {i['name']}：{i['weight']*100:.1f}%（{i['reason']}）")
            lines.append("")
            lines.append(f"## 风控结论：{'通过' if risk.get('passed') else '未通过'}")
            for issue in risk.get("issues", []):
                lines.append(f"- ⚠️ {issue}")
            lines.append("")
            lines.append(f"> 结论：{decision.get('rationale', '')}")
            report = "\n".join(lines)
            return self._ok({"report": report, "markdown": report})
        except Exception as e:  # noqa: BLE001
            return self._err(e)
