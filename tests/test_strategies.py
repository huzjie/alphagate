"""策略库单测。"""
from alphagate.strategies.library import StrategyLibrary


def test_library_has_12_strategies():
    lib = StrategyLibrary()
    assert len(lib) == 12


def test_ideas_all_have_rationale():
    lib = StrategyLibrary()
    for idea in lib.ideas():
        assert idea.rationale, f"{idea.name} missing rationale"
