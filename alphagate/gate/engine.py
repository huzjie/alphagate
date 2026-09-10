"""语义门控引擎：核心决策器。

流程：市场状态文本 + 每条配置思路的逻辑说明书 -> 语义匹配打分 -> 阈值门控
-> 归一化权重 -> 生成可解释决策（为什么此刻该这样配置）。
"""
from __future__ import annotations

from typing import Dict, List, Optional

from alphagate.core.context import GateContext
from alphagate.core.exceptions import GateError
from alphagate.core.gate_decision import GateDecision, GatedIdea
from alphagate.core.market_regime import MarketRegime
from alphagate.core.registry import EmbedderRegistry
from alphagate.core.strategy_idea import StrategyIdea
from alphagate.gate.embedders import cosine


class SemanticGate:
    """语义门控：为当下市场环境匹配「对症」的配置思路。"""

    def __init__(
        self,
        embedder: str = "hash",
        threshold: float = 0.35,
        top_k: int = 5,
        max_active: int = 6,
    ) -> None:
        self.embedder_name = embedder
        self.threshold = threshold
        self.top_k = top_k
        self.max_active = max_active
        self._embedder = None

    def _get_embedder(self):
        if self._embedder is None:
            self._embedder = EmbedderRegistry.get(self.embedder_name)
        return self._embedder

    def decide(self, regime: MarketRegime, ideas: List[StrategyIdea]) -> GateDecision:
        """执行一次门控决策。"""
        if not ideas:
            raise GateError("no strategy ideas to gate")
        emb = self._get_embedder()
        regime_text = regime.to_text()
        regime_vec = emb.encode(regime_text)

        scored: List[GatedIdea] = []
        for idea in ideas:
            idea_vec = emb.encode(idea.to_text())
            sim = cosine(regime_vec, idea_vec)
            allowed = sim >= self.threshold
            reason = (
                f"语义匹配分 {sim:.3f} >= 阈值 {self.threshold}，逻辑与当前环境吻合"
                if allowed
                else f"语义匹配分 {sim:.3f} < 阈值 {self.threshold}，逻辑与当前环境不符"
            )
            scored.append(GatedIdea(name=idea.name, allowed=allowed, score=sim, reason=reason))

        # 取 top_k 中放行的
        ranked = sorted(scored, key=lambda x: x.score, reverse=True)
        allowed = [g for g in ranked if g.allowed][: self.max_active]

        if not allowed:
            # 兜底：全部不放行时，放行 top_k 里分最高的一个，避免空组合
            fallback = ranked[0]
            fallback.allowed = True
            fallback.reason += "（兜底放行：无思路通过阈值，取语义最接近者）"
            allowed = [fallback]

        # 权重：按匹配分 softmax 归一化
        total = sum(g.score for g in allowed) or 1.0
        for g in allowed:
            g.weight = g.score / total

        rationale = self._build_rationale(regime, allowed)
        decision = GateDecision(regime_text=regime_text, ideas=ranked, rationale=rationale)
        decision.metadata["embedder"] = self.embedder_name
        decision.metadata["threshold"] = self.threshold
        return decision

    @staticmethod
    def _build_rationale(regime: MarketRegime, allowed: List[GatedIdea]) -> str:
        names = "、".join(g.name for g in allowed)
        return (
            f"当前市场处于「{regime.regime.value}」状态（{regime.description}），"
            f"语义门控放行了 {len(allowed)} 条配置思路：{names}。"
            f"这些思路的经济逻辑与当下行情相吻合，其余思路被拦截。"
        )

    def context(self, regime: MarketRegime, ideas: List[StrategyIdea]) -> GateContext:
        decision = self.decide(regime, ideas)
        return GateContext(
            regime=regime,
            ideas=ideas,
            candidate_weights=decision.active_weights,
            metadata={"decision": decision.to_dict()},
        )
