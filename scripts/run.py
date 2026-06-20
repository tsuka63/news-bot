"""
news-bot CLI — fetch watchlist news + macro reference, print and/or save HTML.

  python scripts/run.py
  python scripts/run.py --report
  python scripts/run.py --tickers SPCX,AAPL,^N225
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from newsbot.news      import fetch_watchlist
from newsbot.watchlist import WATCHLIST
from newsbot.report    import save

_MARK = {"pos": "◎", "neg": "▼", "neutral": "—"}


def main() -> int:
    ap = argparse.ArgumentParser(description="マーケット・ニュース＆マクロ")
    ap.add_argument("--tickers", help="カンマ区切りのティッカー（例: SPCX,AAPL）")
    ap.add_argument("--report", action="store_true", help="HTMLも出力")
    ap.add_argument("--out", default="data/news.html")
    args = ap.parse_args()

    wl = ([(t.strip(), t.strip()) for t in args.tickers.split(",")]
          if args.tickers else WATCHLIST)

    print(f"ニュース取得中: {len(wl)} 銘柄 …")
    feed = fetch_watchlist(wl)
    for e in feed:
        print(f"\n=== {e['name']} ({e['ticker']}) ===")
        for it in e["items"]:
            print(f"  {_MARK.get(it['sentiment'],'—')} {it['title'][:70]}")

    if args.report:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        print(f"\nHTML → {save(feed, args.out)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
