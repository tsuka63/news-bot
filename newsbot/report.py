"""
HTML report: a news feed grouped by ticker (with sentiment tags) plus the
macro → sector impact reference table. Decision material, not predictions.
"""

from __future__ import annotations

from datetime import datetime, timezone, timedelta
from html import escape

from newsbot.macro import SECTOR_IMPACT

_SENT = {
    "pos":     ("◎ ポジ", "sent-pos"),
    "neg":     ("▼ ネガ", "sent-neg"),
    "neutral": ("— 中立", "sent-neu"),
}


def _fmt_time(s: str) -> str:
    if not s:
        return ""
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        jst = dt.astimezone(timezone(timedelta(hours=9)))
        return jst.strftime("%m/%d %H:%M")
    except Exception:
        return s[:16]


def _li(it: dict) -> str:
    label, cls = _SENT.get(it["sentiment"], _SENT["neutral"])
    title = escape(it["title"])
    if it["url"]:
        title = f'<a href="{escape(it["url"])}" target="_blank">{title}</a>'
    meta = " ／ ".join(x for x in (escape(it["publisher"]), _fmt_time(it["time"])) if x)
    return (f'<li><span class="{cls}">{label}</span> {title}'
            f'<span class="news-meta">{meta}</span></li>')


def _stock_blocks(entries: list[dict]) -> str:
    blocks = []
    for entry in entries:
        rows = "".join(_li(it) for it in entry["items"])
        blocks.append(
            f'<div class="ticker"><h3>{escape(entry["name"])} '
            f'<span class="tk">{escape(entry["ticker"])}</span></h3>'
            f'<ul class="news">{rows}</ul></div>'
        )
    return "".join(blocks)


def _market_block(entries: list[dict]) -> str:
    """JP-source entries are market-wide news, not company-specific — dedupe."""
    seen, items = set(), []
    for entry in entries:
        for it in entry["items"]:
            if it["title"] not in seen:
                seen.add(it["title"])
                items.append(it)
    if not items:
        return ""
    rows = "".join(_li(it) for it in items)
    return (
        '<div class="ticker"><h3>🇯🇵 日本市場ニュース '
        '<span class="tk">市況・為替・東証全体（個別企業ではない）</span></h3>'
        f'<ul class="news">{rows}</ul></div>'
    )


def _macro_table() -> str:
    rows = "".join(
        "<tr>"
        f'<td class="ev">{escape(r["event"])}</td>'
        f'<td class="tail">{escape(r["tail"])}</td>'
        f'<td class="head">{escape(r["head"])}</td>'
        f'<td class="mn">{escape(r["note"])}</td>'
        "</tr>"
        for r in SECTOR_IMPACT
    )
    return (
        '<table class="macro"><thead><tr>'
        '<th>マクロ要因</th><th>追い風 ◎</th><th>逆風 ▼</th><th>補足</th>'
        f'</tr></thead><tbody>{rows}</tbody></table>'
    )


def render(feed: list[dict], title: str = "マーケット・ニュース＆マクロ") -> str:
    from newsbot.jp_news import is_jp
    jst       = timezone(timedelta(hours=9))
    generated = datetime.now(jst).strftime("%Y-%m-%d %H:%M")
    n_items   = sum(len(e["items"]) for e in feed)
    _jp       = [e for e in feed if is_jp(e["ticker"])]
    _stocks   = [e for e in feed if not is_jp(e["ticker"])]

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} — {generated}</title>
<style>
  body {{ font-family:-apple-system,"Hiragino Sans",sans-serif; background:#0f1115;
         color:#e6e6e6; padding:24px; max-width:980px; margin:0 auto; }}
  a {{ color:#9ec5ff; text-decoration:none; }} a:hover {{ text-decoration:underline; }}
  h1 {{ font-size:20px; margin:0 0 4px; }}
  h2 {{ font-size:16px; margin:26px 0 8px; }}
  h3 {{ font-size:15px; margin:16px 0 4px; }}
  .tk {{ color:#8a93a2; font-size:12px; font-weight:400; }}
  .meta {{ color:#8a93a2; font-size:13px; margin-bottom:8px; }}
  ul.news {{ list-style:none; padding:0; margin:0; }}
  ul.news li {{ padding:7px 0; border-bottom:1px solid #1d2230; line-height:1.5; }}
  .news-meta {{ display:block; color:#6b7280; font-size:11px; margin-top:2px; }}
  .sent-pos {{ color:#34d399; font-weight:700; font-size:12px; margin-right:6px; }}
  .sent-neg {{ color:#f87171; font-weight:700; font-size:12px; margin-right:6px; }}
  .sent-neu {{ color:#8a93a2; font-size:12px; margin-right:6px; }}
  table.macro {{ border-collapse:collapse; width:100%; font-size:13px; margin-top:6px; }}
  table.macro th, table.macro td {{ padding:8px 10px; border-bottom:1px solid #232733;
                                    text-align:left; vertical-align:top; }}
  table.macro th {{ color:#b8c0cc; background:#161a22; }}
  td.ev {{ font-weight:700; color:#e6e6e6; white-space:nowrap; }}
  td.tail {{ color:#34d399; }}
  td.head {{ color:#f87171; }}
  td.mn {{ color:#9aa3b2; }}
  .note {{ background:#161a22; border:1px solid #232733; border-radius:10px;
           padding:12px 16px; margin-top:22px; font-size:12px; color:#9aa3b2; line-height:1.7; }}
</style>
</head>
<body>
  <h1>📰 {escape(title)}</h1>
  <div class="meta">🕒 最終更新: {generated}（JST） ／ {n_items}件のニュース</div>

  <h2>🗞 保有・注目銘柄のニュース</h2>
  {(_stock_blocks(_stocks) + _market_block(_jp)) or "<p>ニュースが取得できませんでした。</p>"}

  <h2>🧭 マクロ → セクター影響リファレンス</h2>
  <div class="meta">利上げ・為替などが「どのセクターに有利／不利か」の教科書的な傾向。</div>
  {_macro_table()}

  <div class="note">
    ⚠️ これは<b>判断材料</b>であって株価予測ではありません。感情タグ（◎/▼）は見出しの
    キーワード判定で、参考程度に。マクロの影響は「想定通りか／サプライズか」で変わり、
    ニュースが出た時点で多くは織り込み済みです。最終判断はご自身で。
  </div>
</body>
</html>"""


def save(feed: list[dict], out_path: str, title: str = "マーケット・ニュース＆マクロ") -> str:
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(render(feed, title))
    return out_path
