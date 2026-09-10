"""组合监控：偏离告警、再平衡触发。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class DriftAlert:
    asset: str
    target: float
    actual: float
    drift: float


class PortfolioMonitor:
    """监控目标权重与实际权重的偏离。"""

    def __init__(self, tolerance: float = 0.05) -> None:
        self.tolerance = tolerance

    def check_drift(self, target: Dict[str, float], actual: Dict[str, float]) -> List[DriftAlert]:
        alerts = []
        for asset, t in target.items():
            a = actual.get(asset, 0.0)
            drift = a - t
            if abs(drift) > self.tolerance:
                alerts.append(DriftAlert(asset=asset, target=t, actual=a, drift=drift))
        return alerts

    def needs_rebalance(self, alerts: List[DriftAlert]) -> bool:
        return bool(alerts)
