"""目录卡单测。"""
from alphagate.catalog import list_models, list_strategies


def test_catalog_loads():
    assert len(list_models()) >= 5
    assert len(list_strategies()) >= 12
