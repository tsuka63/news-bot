"""Cloud daily run (GitHub Actions) → docs/index.html for GitHub Pages."""

from __future__ import annotations

import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_DIR))

from newsbot.news      import fetch_watchlist
from newsbot.watchlist import WATCHLIST
from newsbot.report    import save

TODAY = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d")
OUT   = str(PROJECT_DIR / "docs" / "index.html")


def main() -> int:
    Path(OUT).parent.mkdir(parents=True, exist_ok=True)
    print(f"[{TODAY}] Fetching news for {len(WATCHLIST)} tickers …")
    feed = fetch_watchlist(WATCHLIST)
    save(feed, OUT)
    n = sum(len(e["items"]) for e in feed)
    print(f"  Report → {OUT}  ({n} news items)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
