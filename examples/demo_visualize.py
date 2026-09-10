"""示例：可视化净值与权重。"""
from alphagate.backtest.engine import run_backtest
from alphagate.tools.visualizer import Visualizer

result = run_backtest(["600000.SH", "000001.SZ", "600519.SH"])
print("净值曲线:", Visualizer.sparkline(result["nav"]))
print("资产权重:")
print(Visualizer.weight_bars(result["asset_weights"]))
