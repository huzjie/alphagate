"""python -m alphagate.backtest 快速回测 demo。"""
import json

from alphagate.backtest.engine import run_backtest


def main() -> int:
    symbols = ["600000.SH", "000001.SZ", "600519.SH", "300750.SZ", "601318.SH",
               "000858.SZ", "600036.SH", "601398.SH"]
    result = run_backtest(symbols, initial_capital=1_000_000.0)
    print("regime:", result["regime"]["regime"])
    print("strategy_weights:", {k: round(v, 4) for k, v in result["strategy_weights"].items()})
    print("metrics:", json.dumps(result["metrics"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
