"""核心基础模块：类型、异常、注册表、配置、日志、运行时上下文。"""
from alphagate.core.exceptions import (
    AlphaGateError,
    ConfigError,
    DataError,
    GateError,
    StrategyError,
    InferenceError,
    BacktestError,
    TrainingError,
    ModelLoadError,
    MarketDataUnavailableError,
)
from alphagate.core.registry import (
    StrategyRegistry,
    EmbedderRegistry,
    ModelRegistry,
    DataSourceRegistry,
)

__all__ = [
    "AlphaGateError",
    "ConfigError",
    "DataError",
    "GateError",
    "StrategyError",
    "InferenceError",
    "BacktestError",
    "TrainingError",
    "ModelLoadError",
    "MarketDataUnavailableError",
    "StrategyRegistry",
    "EmbedderRegistry",
    "ModelRegistry",
    "DataSourceRegistry",
]
