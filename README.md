# news-bot — マーケット・ニュース＆マクロ

保有・注目銘柄のニュースと、マクロ→セクターの影響リファレンスを毎日自動で
集約する**判断材料ツール**（株価予測ではない）。stock-bot / tachan-bot とは独立。

## できること
- 📰 ウォッチリスト銘柄のニュース集約（Yahoo Finance）＋感情タグ（◎/▼/中立）
- 🧭 マクロ要因（利上げ/利下げ・円安/円高・原油高など）→ 有利/不利セクターの早見表

## 正直な制約
- ニュースは**米国株・主要指数・為替**に強く、**日本の小型株はほぼ取れない**（英語ソース中心）
- 感情タグは見出しのキーワード判定（簡易・参考程度）
- **株価の上下は予測しない**。市場は予想を織り込むため、ニュースで方向を当てるのは困難

## 使い方
```bash
pip install -r requirements.txt
python scripts/run.py --report           # ウォッチリスト
python scripts/run.py --tickers SPCX,AAPL,^N225
```
`--report` で `data/news.html` を生成。

ウォッチリストは `newsbot/watchlist.py` を編集。

## 構成
```
news-bot/
├── newsbot/
│   ├── watchlist.py   追跡するティッカー
│   ├── news.py        ニュース取得＋感情タグ
│   ├── macro.py       マクロ→セクター影響リファレンス
│   └── report.py      HTML生成
└── scripts/
    ├── run.py         CLI
    └── cloud_run.py   GitHub Actions用（docs/index.html）
```
