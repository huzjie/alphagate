"""文本嵌入后端：从轻量哈希到可插拔模型，统一 encode() 接口。"""
from __future__ import annotations

import hashlib
import math
import re
from typing import Dict, List

from alphagate.core.registry import EmbedderRegistry


def _tokenize(text: str) -> List[str]:
    text = text.lower()
    # 中英文都按非字母数字切分
    toks = re.findall(r"[a-z0-9]+|[\u4e00-\u9fff]", text)
    return toks


@EmbedderRegistry.register("hash", "hashing")
class HashEmbedder:
    """特征哈希嵌入：无模型、确定性、离线可用。"""

    def __init__(self, dim: int = 256) -> None:
        self.dim = dim

    def _hash(self, token: str, seed: int) -> int:
        h = hashlib.md5(f"{seed}:{token}".encode("utf-8")).hexdigest()
        return int(h[:8], 16) % self.dim

    def encode(self, text: str) -> List[float]:
        vec = [0.0] * self.dim
        for tok in _tokenize(text):
            idx = self._hash(tok, 0)
            sign = 1.0 if self._hash(tok, 1) % 2 == 0 else -1.0
            vec[idx] += sign
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]


@EmbedderRegistry.register("bow", "bagofwords")
class BagOfWordsEmbedder:
    """词袋嵌入：固定词表 one-hot 计数。"""

    def __init__(self, vocab: List[str] | None = None) -> None:
        self.vocab: Dict[str, int] = {}
        if vocab:
            self.vocab = {w: i for i, w in enumerate(vocab)}

    def fit(self, texts: List[str]) -> "BagOfWordsEmbedder":
        vocab: Dict[str, int] = {}
        for t in texts:
            for tok in _tokenize(t):
                if tok not in vocab:
                    vocab[tok] = len(vocab)
        self.vocab = vocab
        return self

    def encode(self, text: str) -> List[float]:
        vec = [0.0] * len(self.vocab)
        for tok in _tokenize(text):
            if tok in self.vocab:
                vec[self.vocab[tok]] += 1.0
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]


@EmbedderRegistry.register("tfidf", "tf-idf")
class TFIDFEmbedder:
    """TF-IDF 嵌入：带语料逆文档频率的加权词袋。"""

    def __init__(self) -> None:
        self.vocab: Dict[str, int] = {}
        self.idf: List[float] = []

    def fit(self, texts: List[str]) -> "TFIDFEmbedder":
        vocab: Dict[str, int] = {}
        for t in texts:
            for tok in set(_tokenize(t)):
                if tok not in vocab:
                    vocab[tok] = len(vocab)
        self.vocab = vocab
        n = max(len(texts), 1)
        df = [0] * len(vocab)
        for t in texts:
            for tok in set(_tokenize(t)):
                if tok in vocab:
                    df[vocab[tok]] += 1
        self.idf = [math.log((1 + n) / (1 + d)) + 1.0 for d in df]
        return self

    def encode(self, text: str) -> List[float]:
        vec = [0.0] * len(self.vocab)
        for tok in _tokenize(text):
            if tok in self.vocab:
                vec[self.vocab[tok]] += 1.0
        for i in range(len(vec)):
            vec[i] *= self.idf[i]
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]


def cosine(a: List[float], b: List[float]) -> float:
    """余弦相似度。"""
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    return dot  # 向量已归一化
