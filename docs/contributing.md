# 贡献指南

欢迎贡献。请遵循：

1. Fork 本仓库，创建特性分支
2. 代码通过 `ruff check alphagate` 与 `pytest -q`
3. 新策略在 `alphagate/strategies/` 下新增模块，并同步 YAML 策略卡
4. 提交信息清晰描述改动

## 新增配置思路

```python
# alphagate/strategies/my_factor.py
from alphagate.strategies.base import BaseStrategy, build_idea

class MyFactorStrategy(BaseStrategy):
    slug = "my_factor"
    display_name = "我的因子"

    def idea(self):
        return build_idea(name="我的因子", rationale="...", default_weight=0.1)

    def weights(self, universe, **kwargs):
        ...
```

在 `library.py` 中 import 即可注册。
