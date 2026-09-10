"""示例：组合偏离监控。"""
from alphagate.tools.monitor import PortfolioMonitor

target = {"股票": 0.6, "债券": 0.3, "现金": 0.1}
actual = {"股票": 0.7, "债券": 0.25, "现金": 0.05}
monitor = PortfolioMonitor(tolerance=0.05)
alerts = monitor.check_drift(target, actual)
print("需要再平衡:" , monitor.needs_rebalance(alerts))
for a in alerts:
    print(f"  {a.asset}: 目标 {a.target:.2f} 实际 {a.actual:.2f} 偏离 {a.drift:+.2f}")
