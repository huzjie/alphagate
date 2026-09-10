"""API 数据模型（pydantic）。"""
from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class RegimeRequest(BaseModel):
    indicators: Dict[str, float] = Field(default_factory=dict)
    news: List[str] = Field(default_factory=list)


class GateRequest(BaseModel):
    symbols: List[str] = Field(default_factory=lambda: ["600000.SH", "000001.SZ"])
    indicators: Optional[Dict[str, float]] = None
    news: Optional[List[str]] = None


class IdeaOut(BaseModel):
    name: str
    allowed: bool
    score: float
    reason: str
    weight: float


class GateResponse(BaseModel):
    regime: str
    regime_text: str
    ideas: List[IdeaOut]
    weights: Dict[str, float]
    rationale: str


class BacktestRequest(BaseModel):
    symbols: List[str] = Field(default_factory=lambda: ["600000.SH", "000001.SZ"])
    start: str = "2025-01-01"
    end: str = "2026-01-01"
    initial_capital: float = 1_000_000.0


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = "alphagate-r1"
    messages: List[ChatMessage]
    temperature: float = 0.1
    max_tokens: int = 1024
