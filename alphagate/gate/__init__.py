"""语义门控引擎：市场状态建模 + 语义匹配 + 门控决策。"""
from alphagate.gate.engine import SemanticGate
from alphagate.gate.embedders import (
    HashEmbedder,
    BagOfWordsEmbedder,
    TFIDFEmbedder,
)
from alphagate.gate.regime_builder import RegimeBuilder

__all__ = [
    "SemanticGate",
    "HashEmbedder",
    "BagOfWordsEmbedder",
    "TFIDFEmbedder",
    "RegimeBuilder",
]
