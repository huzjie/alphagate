"""示例：多智能体报告。"""
from alphagate.agents.orchestrator import AgentOrchestrator

out = AgentOrchestrator().run(["600000.SH", "000001.SZ", "600519.SH"])
print(out["report"])
