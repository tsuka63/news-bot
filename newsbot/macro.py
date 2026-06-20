"""
Macro → sector impact reference.

A timeless cheat-sheet of how major macro moves *tend* to push sectors and
markets. This is textbook tendency, not a forecast — actual moves depend on
whether the event was already expected (markets price in expectations).
"""

# event → list of (方向, 追い風セクター, 逆風セクター, 補足)
SECTOR_IMPACT = [
    {
        "event": "利上げ（金利↑）",
        "tail":  "銀行・保険（利ざや拡大）",
        "head":  "グロース／ハイテク・REIT・公益（割引率↑で割高に）",
        "note":  "通貨高（円なら円高）要因。ただし想定内なら織り込み済みで動かないことも。",
    },
    {
        "event": "利下げ（金利↓）",
        "tail":  "グロース／ハイテク・REIT・不動産",
        "head":  "銀行（利ざや縮小）",
        "note":  "通貨安（円安）要因。景気刺激で全体的にはプラスに働きやすい。",
    },
    {
        "event": "円安（ドル円↑）",
        "tail":  "輸出株（自動車・電機・機械・半導体製造装置）",
        "head":  "輸入・内需（小売・電力・食品）",
        "note":  "海外売上比率が高い企業ほど追い風。",
    },
    {
        "event": "円高（ドル円↓）",
        "tail":  "輸入・内需",
        "head":  "輸出株",
        "note":  "外貨建て資産（米国株）は円換算で目減り。",
    },
    {
        "event": "原油・資源高",
        "tail":  "エネルギー・商社・資源（石油・非鉄）",
        "head":  "運輸・素材・電力（コスト増）",
        "note":  "インフレ加速→利上げ観測につながることも。",
    },
    {
        "event": "景気後退観測",
        "tail":  "ディフェンシブ（食品・医薬・公益・生活必需品）",
        "head":  "景気敏感（鉄鋼・海運・化学・自動車）",
        "note":  "シクリカル株は景気の谷で仕込む逆張りの好機にもなる。",
    },
]
