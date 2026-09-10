"""Stage 1：偏好对齐（监督/DPO 风格，规则合成数据版）。"""
from __future__ import annotations

from typing import Dict, List, Tuple

from alphagate.rl.dataset import PreferenceSample, make_rule_based_samples


class Stage1PreferenceAligner:
    """把「市场状态 -> 应放行思路」规则蒸馏为可评估的决策器。"""

    def __init__(self, strategies: List[str]) -> None:
        self.strategies = strategies
        self.samples = make_rule_based_samples(strategies)

    def align(self) -> Dict[str, List[str]]:
        """返回 regime -> allowed 的映射（规则直接可得，作为对齐结果）。"""
        mapping: Dict[str, List[str]] = {}
        for s in self.samples:
            regime = s.regime_text.split("；")[0].split(": ")[-1]
            mapping.setdefault(regime, list(dict.fromkeys(s.allowed)))
        return mapping

    def evaluate(self, decisions: List[Tuple[str, bool]], sample: PreferenceSample) -> float:
        """对单条样本评估门控准确率（F1 微平均）。"""
        d = dict(decisions)
        tp = sum(1 for a in sample.allowed if d.get(a))
        fp = sum(1 for b in sample.blocked if d.get(b))
        fn = sum(1 for a in sample.allowed if not d.get(a))
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        return 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
