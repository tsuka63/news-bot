"""Smoke tests (no network) — run: python tests/test_smoke.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from newsbot.news    import _sentiment
from newsbot.jp_news import is_jp, _sentiment_jp, _ITEM_RE


def test_sentiment_en():
    assert _sentiment("Stock surges to record high") == "pos"
    assert _sentiment("Shares plunge after profit miss") == "neg"
    assert _sentiment("Company holds annual meeting") == "neutral"


def test_sentiment_jp():
    assert _sentiment_jp("業績好調で株価が急騰") == "pos"
    assert _sentiment_jp("赤字拡大で急落、下方修正") == "neg"


def test_is_jp():
    assert is_jp("4179") and is_jp("7203.T")
    assert not is_jp("SPCX") and not is_jp("^N225")


def test_jp_news_regex():
    # Mirrors Yahoo Finance JP's per-stock news item structure
    sample = (
        '<a href="/news/detail/abc123" data-cl-params="x" class="_NewsItem__link_x">'
        '<h3 class="_NewsItem__heading_74d7w_17">東証グロード大引け＝値下がり</h3>'
        '<ul class="_NewsItem__supplements_x"><li>株探ニュース</li><li>6/22 15:30</li></ul>'
    )
    m = _ITEM_RE.findall(sample)
    assert m and m[0][0] == "/news/detail/abc123", "JP news regex broke — Yahoo structure?"
    assert "東証" in m[0][1]


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  ✓ {fn.__name__}")
    print(f"OK — {len(fns)} tests passed")
