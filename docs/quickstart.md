# 快速开始

## 安装

```bash
git clone https://github.com/huzjie/alphagate.git
cd alphagate
pip install -e .
```

无需 GPU、无需网络即可跑通全链路（mock 数据源）。

## 三步上手

```bash
# 1. 自检
alphagate doctor

# 2. 语义门控配置决策
alphagate gate --symbols 600000.SH,000001.SZ,600519.SH

# 3. 启动 REST 服务
alphagate serve --port 8000
# 打开 http://localhost:8000/docs 交互文档
```

## Python SDK

```python
from alphagate.serving.pipeline import InferencePipeline

pipe = InferencePipeline()
regime, decision = pipe.decide(["600000.SH", "000001.SZ"])
print(regime.regime.value)        # 市场状态
print(decision.active_weights)    # 各思路权重
print(decision.rationale)         # 可解释结论
```

## 回测

```bash
alphagate backtest --symbols 600000.SH,000001.SZ --start 2025-01-01 --end 2026-01-01
```

## 两阶段 RL 训练

```bash
alphagate train --iterations 30
```

## 多智能体报告

```bash
alphagate report --symbols 600000.SH,000001.SZ --output report.md
```

## 接入真实数据（A 股）

```bash
pip install akshare
# 改 config.yaml: data.source=akshare
```
