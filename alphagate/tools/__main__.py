"""python -m alphagate.tools 工具自检。"""
from alphagate.tools.visualizer import Visualizer
from alphagate.tools.exporter import Exporter


def main() -> int:
    w = {"动量": 0.34, "质量": 0.28, "价值": 0.22, "红利": 0.16}
    print(Visualizer.weight_bars(w))
    print(Exporter.to_markdown_table([
        {"name": "动量", "weight": 0.34}, {"name": "质量", "weight": 0.28},
    ]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
