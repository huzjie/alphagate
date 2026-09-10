"""示例：导出结果。"""
from alphagate.backtest.engine import run_backtest
from alphagate.tools.exporter import Exporter

result = run_backtest(["600000.SH", "000001.SZ", "600519.SH"])
print(Exporter.to_json(result["metrics"]))
Exporter.to_markdown_table(
    [{"asset": k, "weight": v} for k, v in result["asset_weights"].items()],
    path="weights.md",
)
print("已导出 weights.md")
