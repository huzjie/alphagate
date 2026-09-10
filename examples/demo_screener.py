"""示例：选股筛选器。"""
from alphagate.data.market_data import MarketDataHub
from alphagate.tools.screener import Screener

hub = MarketDataHub("mock")
symbols = ["600000.SH", "000001.SZ", "600519.SH", "300750.SZ", "601318.SH", "000858.SZ"]
feats = hub.get_features(symbols)
picked = Screener().add("roe", ">", 0.15).add("quality", ">", 0.5).screen(feats)
print("筛选结果:", picked)
