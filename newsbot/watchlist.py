"""
Tickers to track for news.

yfinance news is strongest for US equities, major indices and FX (these
surface macro/rate news); Japanese small caps usually return nothing, so
focus the watchlist on names with real coverage. Edit freely.
"""

# (ticker, 表示名) — your holdings + macro indicators
# 4桁コード（例 "4179"）は日本株 → Yahoo!ファイナンスJPからニュース取得。
WATCHLIST: list[tuple[str, str]] = [
    # 保有・注目の個別株
    ("SPCX",      "SpaceX"),
    ("4179",      "ジーネクスト"),
    # 日本株の総合市況（任意の主力株でも市場全体ニュースが拾える）
    ("7203",      "トヨタ（市況）"),
    # 指数（マクロニュースの入口）
    ("^GSPC",     "S&P500"),
    ("^N225",     "日経平均"),
    # 為替・金利（利上げ/利下げの影響）
    ("USDJPY=X",  "ドル円"),
    ("^TNX",      "米10年債利回り"),
]
