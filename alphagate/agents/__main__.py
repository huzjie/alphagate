"""python -m alphagate.agents 多智能体流水线 demo。"""
from alphagate.agents.orchestrator import AgentOrchestrator


def main() -> int:
    orch = AgentOrchestrator()
    out = orch.run(["600000.SH", "000001.SZ", "600519.SH"])
    print("ok:", out["ok"])
    print("regime:", out.get("regime", {}).get("regime"))
    print("weights:", {k: round(v, 4) for k, v in (out.get("weights") or {}).items()})
    print("risk:", out.get("risk", {}))
    print(out.get("report", ""))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
