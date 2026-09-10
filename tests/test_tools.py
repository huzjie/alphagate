"""工具模块单测。"""
from alphagate.tools.cleaner import Cleaner
from alphagate.tools.visualizer import Visualizer
from alphagate.tools.screener import Screener


def test_sparkline():
    s = Visualizer.sparkline([1, 2, 3, 4, 5])
    assert len(s) > 0


def test_clip_outliers():
    v = Cleaner.clip_outliers([1, 2, 3, 100])
    assert max(v) < 100


def test_screener():
    universe = {"A": {"roe": 0.2}, "B": {"roe": 0.05}}
    out = Screener().add("roe", ">", 0.1).screen(universe)
    assert out == ["A"]
