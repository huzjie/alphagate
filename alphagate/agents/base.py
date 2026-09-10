"""Agent 基类。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class AgentResult:
    """Agent 输出。"""

    agent: str
    ok: bool
    payload: Dict[str, Any] = field(default_factory=dict)
    error: str = ""


class BaseAgent:
    """多智能体流水线中的单个角色。"""

    name: str = "base"

    def run(self, ctx: Dict[str, Any]) -> AgentResult:  # pragma: no cover - 抽象
        raise NotImplementedError

    def _ok(self, payload: Dict[str, Any]) -> AgentResult:
        return AgentResult(agent=self.name, ok=True, payload=payload)

    def _err(self, e: Exception) -> AgentResult:
        return AgentResult(agent=self.name, ok=False, error=str(e))
