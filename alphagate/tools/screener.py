"""选股筛选器：按因子阈值过滤股票池。"""
from __future__ import annotations

from typing import Dict, List, Tuple


class Screener:
    """基于因子暴露的简单筛选器。"""

    def __init__(self) -> None:
        self._conditions: List[Tuple[str, str, float]] = []

    def add(self, factor: str, op: str, value: float) -> "Screener":
        self._conditions.append((factor, op, value))
        return self

    def screen(self, universe: Dict[str, Dict[str, float]]) -> List[str]:
        out = list(universe.keys())
        for factor, op, value in self._conditions:
            if op == ">":
                out = [s for s in out if universe[s].get(factor, 0.0) > value]
            elif op == ">=":
                out = [s for s in out if universe[s].get(factor, 0.0) >= value]
            elif op == "<":
                out = [s for s in out if universe[s].get(factor, 0.0) < value]
            elif op == "<=":
                out = [s for s in out if universe[s].get(factor, 0.0) <= value]
        return out
