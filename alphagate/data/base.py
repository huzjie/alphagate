"""数据源抽象基类。"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class DataSource(ABC):
    """行情数据源接口。"""

    name: str = "base"

    @abstractmethod
    def get_prices(self, symbols: List[str], start: str, end: str) -> Dict[str, List[float]]:
        """返回 {symbol: [close, ...]} 时间序列。"""

    @abstractmethod
    def get_features(self, symbols: List[str]) -> Dict[str, Dict[str, float]]:
        """返回 {symbol: {factor: value}} 因子暴露。"""

    def get_news(self, symbols: List[str], limit: int = 20) -> List[str]:
        """返回财经新闻摘要列表。"""
        return []


class NewsSource(ABC):
    """新闻源接口。"""

    name: str = "news"

    @abstractmethod
    def fetch(self, query: str, limit: int = 20) -> List[str]:
        """抓取新闻摘要。"""
