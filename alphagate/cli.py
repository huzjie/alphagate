"""命令行入口：doctor / gate / serve / backtest / train / report。"""
from __future__ import annotations

import argparse
import json
import sys

from alphagate.core.logging import setup_logging
from alphagate.version import __version__


def cmd_doctor(args) -> int:
    from alphagate.serving.pipeline import InferencePipeline
    from alphagate.strategies.library import StrategyLibrary
    from alphagate.catalog import list_models

    print("AlphaGate doctor 自检")
    print("=" * 50)
    lib = StrategyLibrary()
    print(f"  ✓ 配置思路：{len(lib)} 条 -> {lib.names()}")
    models = list_models()
    print(f"  ✓ 模型卡：{len(models)} 张 -> {models[:4]}...")
    pipe = InferencePipeline()
    regime, decision = pipe.decide(["600000.SH", "000001.SZ"])
    print(f"  ✓ 门控决策：regime={regime.regime.value}, active={len(decision.allowed)}")
    print("  ✓ 全链路 OK（mock 数据源）")
    return 0


def cmd_gate(args) -> int:
    from alphagate.serving.pipeline import InferencePipeline
    from alphagate.gate.explainer import explain

    pipe = InferencePipeline()
    symbols = args.symbols.split(",") if args.symbols else ["600000.SH", "000001.SZ"]
    regime, decision = pipe.decide(symbols)
    print(explain(decision))
    return 0


def cmd_serve(args) -> int:
    import uvicorn
    from alphagate.serving.app import create_app
    uvicorn.run(create_app(), host=args.host, port=args.port)
    return 0


def cmd_backtest(args) -> int:
    from alphagate.backtest.engine import run_backtest
    symbols = args.symbols.split(",") if args.symbols else ["600000.SH", "000001.SZ"]
    result = run_backtest(symbols, start=args.start, end=args.end, initial_capital=args.capital)
    print(json.dumps({k: result[k] for k in ("regime", "strategy_weights", "metrics")},
                     ensure_ascii=False, indent=2))
    return 0


def cmd_train(args) -> int:
    from alphagate.rl.trainer import TwoStageTrainer
    from alphagate.strategies.library import StrategyLibrary
    trainer = TwoStageTrainer(StrategyLibrary().names())
    report = trainer.run(iterations=args.iterations)
    print(json.dumps({
        "stage1_regime_mapping": report["stage1_regime_mapping"],
        "stage2_best_threshold": report["stage2_best_threshold"],
        "final_reward": report["final_reward"],
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_report(args) -> int:
    from alphagate.agents.orchestrator import AgentOrchestrator
    symbols = args.symbols.split(",") if args.symbols else ["600000.SH", "000001.SZ"]
    out = AgentOrchestrator().run(symbols)
    print(out.get("report", ""))
    if args.output:
        from pathlib import Path
        Path(args.output).write_text(out.get("report", ""), encoding="utf-8")
        print(f"\n[report] saved -> {args.output}")
    return 0 if out.get("ok") else 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="alphagate", description="语义门控金融推理与资产配置平台")
    p.add_argument("--version", action="version", version=f"alphagate {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor", help="环境自检")

    g = sub.add_parser("gate", help="语义门控配置决策")
    g.add_argument("--symbols", type=str, help="逗号分隔代码")

    s = sub.add_parser("serve", help="启动 REST 服务")
    s.add_argument("--host", default="0.0.0.0")
    s.add_argument("--port", type=int, default=8000)

    b = sub.add_parser("backtest", help="回测")
    b.add_argument("--symbols", type=str)
    b.add_argument("--start", default="2025-01-01")
    b.add_argument("--end", default="2026-01-01")
    b.add_argument("--capital", type=float, default=1_000_000.0)

    t = sub.add_parser("train", help="两阶段强化学习训练")
    t.add_argument("--iterations", type=int, default=20)

    r = sub.add_parser("report", help="多智能体生成配置报告")
    r.add_argument("--symbols", type=str)
    r.add_argument("--output", type=str, help="报告输出路径")

    return p


def main(argv=None) -> int:
    setup_logging()
    args = build_parser().parse_args(argv)
    handlers = {
        "doctor": cmd_doctor,
        "gate": cmd_gate,
        "serve": cmd_serve,
        "backtest": cmd_backtest,
        "train": cmd_train,
        "report": cmd_report,
    }
    return handlers[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
