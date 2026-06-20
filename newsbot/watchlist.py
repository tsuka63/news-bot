"""
Tickers to track for news.

yfinance news is strongest for US equities, major indices and FX (these
surface macro/rate news); Japanese small caps usually return nothing, so
focus the watchlist on names with real coverage. Edit freely.
"""

# (ticker, 表示名) — your holdings + macro indicators
WATCHLIST: list[tuple[str, str]] = [
    # 保有・注目の個別株（米国）
    ("SPCX",      "SpaceX"),
    # 指数（マクロニュースの入口）
    ("^GSPC",     "S&P500"),
    ("^IXIC",     "NASDAQ"),
    ("^N225",     "日経平均"),
    # 為替・金利（利上げ/利下げの影響）
    ("USDJPY=X",  "ドル円"),
    ("^TNX",      "米10年債利回り"),
]
