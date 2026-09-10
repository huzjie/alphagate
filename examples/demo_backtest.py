"""示例：回测。"""
import json
from alphagate.backtest.engine import run_backtest

result = run_backtest(["600000.SH", "000001.SZ", "600519.SH", "300750.SZ", "601318.SH"])
print(json.dumps({
    "regime": result["regime"]["regime"],
    "strategy_weights": {k: round(v, 4) for k, v in result["strategy_weights"].items()},
    "metrics": result["metrics"],
}, ensure_ascii=False, indent=2))
