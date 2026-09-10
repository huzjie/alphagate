"""python -m alphagate.data 快速自检。"""
from alphagate.data.market_data import MarketDataHub
from alphagate.data.indicators import compute_regime_indicators


def main() -> int:
    hub = MarketDataHub("mock")
    symbols = ["600000.SH", "000001.SZ", "600519.SH", "300750.SZ", "601318.SH"]
    prices = hub.get_prices(symbols, "2025-01-01", "2026-01-01")
    ind = compute_regime_indicators(prices)
    for k, v in ind.items():
        print(f"  {k:20s} = {v:.4f}")
    news = hub.get_news(symbols, limit=3)
    print("  新闻样本:", news[:2])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
