"""
Japanese stock news from Yahoo Finance Japan (yfinance returns nothing for
JP names). Scrapes the per-stock news page; sentiment uses Japanese keywords.
"""

from __future__ import annotations

import re
import requests

_UA   = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
_BASE = "https://finance.yahoo.co.jp"

_ITEM_RE = re.compile(
    r'<a href="(/news/detail/[^"]+)"[^>]*>'
    r'<h3 class="_NewsItem__heading_\w+">([^<]+)</h3>'
    r'(?:<ul[^>]*>(.*?)</ul>)?',
    re.DOTALL,
)
_SUPP_RE = re.compile(r'<li[^>]*>([^<]+)</li>')

_POS_JP = ("上昇", "急騰", "最高益", "増益", "上方修正", "黒字", "好調", "続伸",
           "増配", "過去最高", "好決算", "上振れ", "回復", "買い", "高値更新", "拡大")
_NEG_JP = ("下落", "急落", "赤字", "減益", "下方修正", "続落", "安値", "減配",
           "不正", "訴訟", "リコール", "下振れ", "悪化", "延期", "売り", "減少", "懸念")


def _sentiment_jp(title: str) -> str:
    pos = sum(w in title for w in _POS_JP)
    neg = sum(w in title for w in _NEG_JP)
    if pos > neg:
        return "pos"
    if neg > pos:
        return "neg"
    return "neutral"


def is_jp(ticker: str) -> bool:
    return bool(re.match(r"^\d{4}(\.T)?$", ticker))


def _get(url: str, retries: int = 3) -> str:
    import time
    for i in range(retries):
        try:
            r = requests.get(url, headers={"User-Agent": _UA}, timeout=15)
            r.raise_for_status()
            return r.text
        except Exception:
            if i == retries - 1:
                return ""
            time.sleep(2 * (i + 1))
    return ""


def fetch_jp(ticker: str, limit: int = 6) -> list[dict]:
    code = ticker.replace(".T", "")
    html = _get(f"{_BASE}/quote/{code}.T/news")
    if not html:
        return []

    out: list[dict] = []
    for href, title, supp in _ITEM_RE.findall(html):
        title = title.strip()
        if not title:
            continue
        bits = _SUPP_RE.findall(supp or "")
        publisher = bits[0].strip() if bits else "Yahoo!ファイナンス"
        when = bits[1].strip() if len(bits) > 1 else ""
        out.append({
            "title":     title,
            "publisher": publisher,
            "url":       _BASE + href,
            "time":      when,
            "sentiment": _sentiment_jp(title),
        })
        if len(out) >= limit:
            break
    return out
