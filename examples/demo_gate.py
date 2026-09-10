"""示例：语义门控配置决策。"""
from alphagate.serving.pipeline import InferencePipeline
from alphagate.gate.explainer import explain

pipe = InferencePipeline()
regime, decision = pipe.decide(["600000.SH", "000001.SZ", "600519.SH", "300750.SZ"])
print(explain(decision))
