"""统一异常体系。"""


class AlphaGateError(Exception):
    """AlphaGate 顶层异常基类。"""


class ConfigError(AlphaGateError):
    """配置缺失或非法。"""


class DataError(AlphaGateError):
    """数据获取或解析失败。"""


class MarketDataUnavailableError(DataError):
    """行情数据不可用。"""


class GateError(AlphaGateError):
    """语义门控推理失败。"""


class StrategyError(AlphaGateError):
    """配置思路加载或执行失败。"""


class InferenceError(AlphaGateError):
    """模型推理失败。"""


class BacktestError(AlphaGateError):
    """回测引擎异常。"""


class TrainingError(AlphaGateError):
    """两阶段强化学习训练失败。"""


class ModelLoadError(AlphaGateError):
    """模型加载失败。"""
