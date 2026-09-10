"""多智能体单测。"""
from alphagate.agents.orchestrator import AgentOrchestrator


def test_orchestrator_runs():
    out = AgentOrchestrator().run(["600000.SH", "000001.SZ"])
    assert "report" in out
    assert out.get("ok") in (True, False)
