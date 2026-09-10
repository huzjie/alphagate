"""财经新闻抓取与摘要。"""
from __future__ import annotations

from typing import List, Optional

from alphagate.data.base import NewsSource


class RegexNewsSource(NewsSource):
    """基于关键词的轻量新闻摘要器（演示/离线用）。"""

    name = "regex"

    def fetch(self, query: str, limit: int = 20) -> List[str]:
        snippets = [
            f"{query}相关：政策环境维持稳定，市场情绪中性偏乐观",
            f"{query}相关：行业景气度边际改善，龙头公司份额提升",
            f"{query}相关：海外波动传导有限，A 股独立性增强",
            f"{query}相关：资金面延续宽松，估值修复仍在途",
        ]
        return snippets[:limit]
