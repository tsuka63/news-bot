"""
News fetching + lightweight sentiment tagging.

News comes from Yahoo Finance via yfinance. Sentiment is a simple keyword
heuristic on the (mostly English) headline — a quick positive / negative read,
NOT a price prediction. The point is to surface material to read, fast.
"""

from __future__ import annotations

from datetime import datetime, timezone

_POSITIVE = (
    "surge", "soar", "jump", "rally", "gain", "rise", "beat", "record",
    "high", "upgrade", "profit", "boost", "win", "strong", "growth", "rebound",
    "buyback", "raise", "tops", "climb", "optimism", "deal", "approval",
)
_NEGATIVE = (
    "plunge", "slump", "sink", "fall", "drop", "tumble", "miss", "loss",
    "cut", "downgrade", "weak", "warn", "lawsuit", "probe", "decline", "slash",
    "fear", "recession", "selloff", "crash", "default", "layoff", "halt", "ban",
)


def _sentiment(title: str) -> str:
    t = title.lower()
    pos = sum(w in t for w in _POSITIVE)
    neg = sum(w in t for w in _NEGATIVE)
    if pos > neg:
        return "pos"
    if neg > pos:
        return "neg"
    return "neutral"


def _pick(d: dict, *keys, default=""):
    for k in keys:
        v = d.get(k)
        if v:
            return v
    return default


def _parse_item(raw: dict) -> dict | None:
    c = raw.get("content", raw)          # newer yfinance nests under 'content'
    title = _pick(c, "title")
    if not title:
        return None
    provider = c.get("provider") or {}
    publisher = provider.get("displayName") if isinstance(provider, dict) else ""
    publisher = publisher or _pick(raw, "publisher")
    url = ""
    for k in ("canonicalUrl", "clickThroughUrl"):
        u = c.get(k)
        if isinstance(u, dict) and u.get("url"):
            url = u["url"]
            break
    url = url or _pick(raw, "link")
    when = _pick(c, "pubDate", "displayTime") or ""
    if not when and raw.get("providerPublishTime"):
        when = datetime.fromtimestamp(raw["providerPublishTime"], tz=timezone.utc).isoformat()
    return {
        "title":     title,
        "publisher": publisher,
        "url":       url,
        "time":      when,
        "sentiment": _sentiment(title),
    }


def fetch_for(ticker: str, limit: int = 6) -> list[dict]:
    import yfinance as yf
    try:
        raw = yf.Ticker(ticker).news or []
    except Exception:
        return []
    out = []
    for item in raw[:limit]:
        parsed = _parse_item(item)
        if parsed:
            out.append(parsed)
    return out


def fetch_watchlist(watchlist: list[tuple[str, str]], limit: int = 6) -> list[dict]:
    """Return [{ticker, name, items[]}] for each watchlist entry with news."""
    feed = []
    for ticker, name in watchlist:
        items = fetch_for(ticker, limit=limit)
        if items:
            feed.append({"ticker": ticker, "name": name, "items": items})
    return feed
