<h1 align="center">AlphaGate</h1>
<p align="center">
  <b>语义门控金融推理与资产配置平台</b><br/>
  基于 Alpha-R1（财跃星辰 × 上海交大 · 8B 金融推理大模型）范式
</p>
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue" alt="Python"/>
  <img src="https://img.shields.io/badge/License-Apache%202.0-green" alt="License"/>
  <img src="https://img.shields.io/badge/Model-Alpha--R1--8B-red" alt="Model"/>
  <img src="https://img.shields.io/badge/CI-passing-brightgreen" alt="CI"/>
</p>

---

## 这是什么

2026 年 9 月 10 日，财跃星辰（FinStep）联合上海交大安泰经济与管理学院开源金融推理
大模型 **Alpha-R1（8B）**。它用独创的「**语义门控**」推理技术与「**两阶段强化学习**」
训练框架，在金融推理任务样本外评测大幅领先通用模型——能实时读懂市场环境，从成百上千条
候选配置思路中动态挑出当下真正有效的少数几条，并用「人话」解释为什么此刻该这样配置。

**AlphaGate** 把这项能力工程化为一个**填配置即运行、可直接部署**的生产级金融智能平台：

- 不训练模型，而是在开源金融推理模型之上，落地「市场状态建模 → 语义门控 → 可解释配置」
- 内置 **12 条配置思路**（价值/动量/质量/低波/红利/成长/反转/趋势/防御/流动性/小盘/风险平价），
  每条附「经济逻辑说明书」
- 提供 **两阶段强化学习**训练框架、**回测引擎**、**多智能体流水线**与 **REST 服务**
- 完全**离线可跑**（mock 数据源 + 无模型嵌入），无 GPU 无网络端到端跑通

## 快速开始（无需 GPU）

```bash
git clone https://github.com/huzjie/alphagate.git
cd alphagate
pip install -e .

alphagate doctor                                    # 自检
alphagate gate --symbols 600000.SH,000001.SZ       # 语义门控配置决策
alphagate backtest --symbols 600000.SH,000001.SZ   # 回测
alphagate serve --port 8000                         # REST 服务（/docs 交互文档）
alphagate report --symbols 600000.SH --output r.md  # 多智能体报告
alphagate train --iterations 20                     # 两阶段 RL 训练
```

## 核心能力

| 能力 | 说明 |
|---|---|
| 🧠 语义门控引擎 | 市场状态 × 思路说明书 语义匹配，只放行「对症」思路 |
| 📊 12 条配置思路 | 每条附经济逻辑说明书 + YAML 策略卡 |
| 🤖 多智能体 | 研究员 → 配置官 → 风控官 → 报告官 |
| 🎯 两阶段 RL | Stage1 偏好对齐 + Stage2 GRPO |
| 📈 回测系统 | 组合构建 + 绩效 + 归因 + 风控（VaR/CVaR/Calmar） |
| 🔌 可插拔 | 数据源（mock/csv/akshare）+ 嵌入（hash/bow/tfidf） |
| 🌐 REST API | FastAPI + OpenAI 兼容端点 |
| 🐳 完整交付 | Docker + Compose + K8s + GitHub Actions CI |

## 语义门控原理

```
市场状态描述（行情 + 新闻）
        │
        ▼   语义匹配（余弦相似度）
配置思路库（每条带经济逻辑说明书）
        │
        ▼   阈值门控 + softmax 归一化
只放行「逻辑与当下环境吻合」的少数思路 + 人话解释
```

> 传统配置「背熟药典却不会看病」，语义门控是「先读市场、再对症下药」。

## Python SDK

```python
from alphagate.serving.pipeline import InferencePipeline

pipe = InferencePipeline()
regime, decision = pipe.decide(["600000.SH", "000001.SZ"])
print(regime.regime.value)      # 市场状态
print(decision.active_weights)  # 各思路权重
print(decision.rationale)       # 可解释结论
```

## 接入真实 A 股数据

```bash
pip install akshare
# config.yaml: data.source = akshare
```

## 文档

- [架构设计](docs/architecture.md)
- [快速开始](docs/quickstart.md)
- [语义门控原理](docs/semantic-gating.md)
- [REST API](docs/api.md)
- [部署](docs/deployment.md)
- [贡献指南](docs/contributing.md)

## 目录结构

```
alphagate/
├── alphagate/
│   ├── core/           # 类型/异常/配置/注册表/上下文
│   ├── gate/           # 语义门控引擎 + 嵌入后端
│   ├── strategies/     # 12 条配置思路
│   ├── data/           # 行情/因子/指标/新闻/缓存
│   ├── rl/             # 两阶段强化学习
│   ├── serving/        # FastAPI + OpenAI 兼容
│   ├── backtest/       # 回测 + 绩效 + 归因 + 风控
│   ├── agents/         # 多智能体
│   ├── catalog/        # 模型卡 + 策略卡
│   └── cli.py          # 命令行
├── tests/              # 测试套件
├── examples/           # 示例脚本
├── docs/               # 文档
├── k8s/                # Kubernetes 清单
├── Dockerfile / docker-compose.yml
└── .github/workflows/  # CI
```

## 热点背景

- 模型：财跃星辰 Alpha-R1（8B），「语义门控」推理 + 两阶段 RL
- 技术报告：arxiv.org/abs/2512.23515
- 模型：huggingface.co/FinStep-AI/Alpha-R1

## License

Apache-2.0
