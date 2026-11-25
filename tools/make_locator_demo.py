# -*- coding: utf-8 -*-
"""生成定位图样板页：位置图（真实大陆轮廓）+ 原剖面图合版。"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from locator import locator_svg
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); DATA = os.path.join(ROOT, "data")

def combine(existing_svg, lon, lat, label):
    inner = existing_svg.strip()
    inner = inner[inner.index(">") + 1: inner.rindex("</svg>")]
    loc = locator_svg(lon, lat, label)
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 760' role='img' aria-label='位置图与剖面示意图'>"
            + loc + "<g transform='translate(0,258)'>" + inner + "</g></svg>")

entries = {e["title"]: e for e in json.load(open(os.path.join(DATA, "asia.json"), encoding="utf-8"))["entries"]}
COORD = {"黄土高原": (108.5, 36.5), "云贵喀斯特": (106.0, 25.5), "四川盆地": (105.5, 30.5), "塔里木盆地": (83.5, 39.5)}
title = "黄土高原"
svg = combine(entries[title]["svg"], *COORD[title], title)

html = f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>位置图样板 — 黄土高原</title><style>
:root{{--bg:#fbf9f4;--ink:#22201c;--dim:#6b6459;--line:#d9d2c4;--accent:#a4501a;--accent2:#2f6f8f}}
@media (prefers-color-scheme:dark){{:root{{--bg:#171614;--ink:#eae4d8;--dim:#a49c8e;--line:#3a3730;--accent:#e08a4a;--accent2:#6fa8c8}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.7 "Noto Serif SC",Georgia,serif}}
.wrap{{max-width:920px;margin:0 auto;padding:28px 20px 60px}} h1{{font-size:23px;margin:0 0 4px}}
.lead{{color:var(--dim);margin:0 0 18px}} svg{{width:100%;height:auto;display:block;border:1px solid var(--line);border-radius:12px}}
.lbl{{fill:var(--ink);font-size:13px;font-family:"Noto Sans SC",sans-serif}} .lbl-s{{fill:var(--dim);font-size:11px;font-family:"Noto Sans SC",sans-serif}}
.dim{{fill:var(--dim);font-size:11px;font-family:"Noto Sans SC",sans-serif}}
</style></head><body><div class="wrap">
<h1>位置图 + 剖面图（合版样板）</h1>
<p class="lead">上半部为真实国界轮廓下的定位图（红点为该地貌所在），下半部为成因剖面示意。底图为示意轮廓，非精确测绘；国界不作政治主张。</p>
{svg}
</div></body></html>"""
os.makedirs(os.path.join(ROOT, "site", "demo"), exist_ok=True)
open(os.path.join(ROOT, "site", "demo", "locator-sample.html"), "w", encoding="utf-8").write(html)
print("written", len(svg))
