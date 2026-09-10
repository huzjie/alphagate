"""决策解释器：把门控结果转成「人话」配置建议。"""
from __future__ import annotations

from typing import List

from alphagate.core.gate_decision import GateDecision, GatedIdea


def explain(decision: GateDecision) -> str:
    """生成面向普通投资者的可读解释。"""
    lines = ["=" * 56, "AlphaGate 语义门控 · 配置决策", "=" * 56, ""]
    lines.append(f"【市场状态】{decision.regime_text}")
    lines.append("")
    lines.append("【放行思路】（按语义匹配分排序）")
    for i, g in enumerate(decision.ideas, 1):
        if g.allowed:
            lines.append(f"  {i}. {g.name:<18} 权重 {g.weight*100:5.1f}%  匹配分 {g.score:.3f}")
            lines.append(f"     └─ {g.reason}")
    lines.append("")
    lines.append("【拦截思路】")
    blocked = [g for g in decision.ideas if not g.allowed]
    if blocked:
        for g in blocked:
            lines.append(f"  × {g.name:<18} 匹配分 {g.score:.3f}  {g.reason}")
    else:
        lines.append("  （无）")
    lines.append("")
    lines.append(f"【结论】{decision.rationale}")
    lines.append("=" * 56)
    return "\n".join(lines)
