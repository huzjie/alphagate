"""扩展策略单测。"""
from alphagate.strategies.library import StrategyLibrary


def test_library_has_18_strategies():
    lib = StrategyLibrary()
    assert len(lib) == 18
    names = set(lib.names())
    assert "industry_rotation" in names
    assert "sentiment" in names
