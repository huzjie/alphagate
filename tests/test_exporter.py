"""导出单测。"""
from alphagate.tools.exporter import Exporter


def test_to_json():
    s = Exporter.to_json({"a": 1})
    assert '"a": 1' in s


def test_to_markdown_table():
    s = Exporter.to_markdown_table([{"x": 1}, {"x": 2}])
    assert "| x |" in s
