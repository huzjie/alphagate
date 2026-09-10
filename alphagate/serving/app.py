"""FastAPI 应用工厂。"""
from __future__ import annotations

from typing import Dict

from fastapi import FastAPI

from alphagate.serving.pipeline import InferencePipeline
from alphagate.serving.schemas import (
    BacktestRequest,
    ChatCompletionRequest,
    ChatMessage,
    GateRequest,
    GateResponse,
    IdeaOut,
    RegimeRequest,
)

_pipeline: InferencePipeline | None = None


def get_pipeline() -> InferencePipeline:
    global _pipeline
    if _pipeline is None:
        _pipeline = InferencePipeline()
    return _pipeline


def create_app() -> FastAPI:
    app = FastAPI(
        title="AlphaGate",
        description="语义门控金融推理与资产配置平台 API（Alpha-R1 范式）",
        version="1.0.0",
    )

    @app.get("/health")
    def health() -> Dict[str, str]:
        return {"status": "ok", "service": "alphagate"}

    @app.post("/gate", response_model=GateResponse)
    def gate(req: GateRequest) -> GateResponse:
        pipe = get_pipeline()
        regime, decision = pipe.decide(req.symbols, req.indicators, req.news)
        ideas = [
            IdeaOut(name=i.name, allowed=i.allowed, score=round(i.score, 4),
                    reason=i.reason, weight=round(i.weight, 6))
            for i in decision.ideas
        ]
        return GateResponse(
            regime=regime.regime.value,
            regime_text=decision.regime_text,
            ideas=ideas,
            weights={k: round(v, 6) for k, v in decision.active_weights.items()},
            rationale=decision.rationale,
        )

    @app.post("/regime")
    def regime(req: RegimeRequest) -> Dict[str, object]:
        pipe = get_pipeline()
        r, _ = pipe.decide(["600000.SH"], req.indicators, req.news)
        return r.to_dict()

    @app.post("/backtest")
    def backtest(req: BacktestRequest) -> Dict[str, object]:
        from alphagate.backtest.engine import run_backtest
        return run_backtest(
            symbols=req.symbols,
            start=req.start,
            end=req.end,
            initial_capital=req.initial_capital,
        )

    @app.post("/v1/chat/completions")
    def chat(req: ChatCompletionRequest) -> Dict[str, object]:
        """OpenAI 兼容端点：把最后一个 user 消息解释为门控查询。"""
        pipe = get_pipeline()
        user_msg = next((m.content for m in reversed(req.messages) if m.role == "user"), "")
        symbols = _extract_symbols(user_msg) or ["600000.SH", "000001.SZ"]
        regime, decision = pipe.decide(symbols)
        content = (
            f"市场状态：{regime.regime.value}\n"
            f"配置建议：{decision.rationale}\n"
            f"权重：{ {k: round(v, 4) for k, v in decision.active_weights.items()} }"
        )
        return {
            "id": "chatcmpl-alphagate",
            "object": "chat.completion",
            "created": 0,
            "model": req.model,
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop",
            }],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        }

    return app


def _extract_symbols(text: str) -> list[str]:
    import re
    return re.findall(r"\b\d{6}\.(?:SH|SZ|BJ)\b", text.upper())
