"""可视化：净值曲线（ASCII）、权重条形、门控热力（纯文本，无重依赖）。"""
from __future__ import annotations

from typing import Dict, List


class Visualizer:
    """无 matplotlib 的轻量可视化，输出 ASCII / Unicode 图表。"""

    @staticmethod
    def sparkline(values: List[float], width: int = 48) -> str:
        if not values:
            return "(empty)"
        lo, hi = min(values), max(values)
        if hi == lo:
            return "-" * width
        chars = "▁▂▃▄▅▆▇█"
        out = []
        for v in values:
            idx = int((v - lo) / (hi - lo) * (len(chars) - 1))
            out.append(chars[idx])
        s = "".join(out)
        # 下采样到 width
        if len(s) <= width:
            return s
        step = len(s) / width
        return "".join(s[int(i * step)] for i in range(width))

    @staticmethod
    def weight_bars(weights: Dict[str, float], width: int = 40) -> str:
        lines = []
        for name, w in sorted(weights.items(), key=lambda x: -x[1]):
            bar_len = int(w * width)
            lines.append(f"  {name:<18} {'█' * bar_len} {w*100:5.1f}%")
        return "\n".join(lines)

    @staticmethod
    def bar(series: Dict[str, float], width: int = 40) -> str:
        return Visualizer.weight_bars(series, width)
