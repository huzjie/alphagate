"""AlphaGate — 语义门控金融推理与资产配置平台。

围绕财跃星辰 + 上海交大开源金融推理大模型 Alpha-R1（8B）的核心技术
「语义门控」(Semantic Gating) 与「两阶段强化学习」构建的工程化平台：
在开源金融推理模型之上，把「市场状态建模 → 配置思路库 → 语义门控匹配 →
可解释配置决策 → 两阶段 RL 训练 → 回测评估」工程化为一个填配置即运行、
可直接部署的生产级金融智能平台。

顶层入口，导出版本与常用符号。
"""
from alphagate.version import __version__, __author__, __license__, __description__

__all__ = ["__version__", "__author__", "__license__", "__description__"]
