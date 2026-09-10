"""推理提示词模板：用于接驳真实 LLM 后端的结构化提示。"""
from __future__ import annotations

from typing import Dict, List


def build_gate_prompt(regime_text: str, ideas: List[str]) -> str:
    ideas_block = "\n".join(f"{i+1}. {t}" for i, t in enumerate(ideas))
    return (
        "你是一名资深资产配置研究员。请先读懂当前市场环境，再从候选配置思路中"
        "只放行经济逻辑与当下行情相吻合的少数几条，并用普通人看得懂的语言解释"
        "「为什么此刻该这样配置」。\n\n"
        f"【当前市场状态】\n{regime_text}\n\n"
        f"【候选配置思路】\n{ideas_block}\n\n"
        "【输出要求】逐条给出：放行/拦截 判断、0~1 的置信度、以及一句人话解释。"
    )


def build_regime_summary_prompt(indicators: Dict[str, float], news: List[str]) -> str:
    kv = "\n".join(f"- {k}: {v:.4f}" for k, v in indicators.items())
    news_block = "\n".join(f"- {n}" for n in news[:10])
    return (
        "请综合以下行情指标与财经新闻，生成一段 150 字以内的「当前市场状态描述」，"
        "需覆盖：所处阶段、驱动因素、主要风险。\n\n"
        f"【行情指标】\n{kv}\n\n【财经新闻】\n{news_block}"
    )
