# -*- coding: utf-8 -*-
"""通用插图生成器：按主题生成真实底图定位图 + 主题示意图，替换全站占位曲线。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from locator import map_svg

UNIT_BBOX = {
 "africa": (-20, 55, -36, 38), "asia": (25, 150, -12, 56), "europe": (-12, 45, 34, 72),
 "north-america": (-170, -50, 6, 75), "south-america": (-85, -33, -56, 13),
 "oceania": (110, 180, -48, -6), "antarctica": (-180, 180, -90, -58),
 "global-themes": (-170, 190, -58, 84),
}

def build(entry, coords=None):
    unit = entry.get("unit_id", "global-themes"); theme = entry.get("theme", "区域")
    title = entry["title"]
    lon = coords[0] if coords else None; lat = coords[1] if coords else None
    bb = list(UNIT_BBOX.get(unit, UNIT_BBOX["global-themes"]))
    if lon is not None:
        bb = [min(bb[0], lon - 4), max(bb[1], lon + 4), min(bb[2], lat - 4), max(bb[3], lat + 4)]
    loc = map_svg((30, 34, 840, 196), tuple(bb), lon, lat, label=title if coords else None)
    diagram = THEME.get(theme, theme_region)(entry)
    parts = [
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 600' role='img' aria-label='%s 示意图'>" % title,
        "<rect x='20' y='20' width='860' height='560' rx='12' fill='none' stroke='var(--line)'/>",
        "<text x='40' y='30' class='lbl'>%s · %s</text>" % (title, theme),
        "<text x='30' y='46' class='lbl-s'>所在区域（真实陆地轮廓；红点为该条目所在）</text>",
        loc,
        "<path d='M30 244 L870 244' stroke='var(--line)'/>",
        diagram,
        "<text x='40' y='572' class='dim'>示意图，非精确测绘；底图仅示意相对位置，不涉政治主张</text>",
        "</svg>",
    ]
    return "".join(parts)

# ---------- 主题示意图（y 256..548 区域）----------
def _t(x, y, s, cls="lbl"): return "<text x='%d' y='%d' class='%s'>%s</text>" % (x, y, cls, s)

def theme_terrain(e):
    t = e["title"]; s = [t and _t(40, 268, "地貌剖面（按类型示意）", "lbl")]
    if any(k in t for k in ("山", "岭")):
        s.append("<polygon points='60,520 200,320 260,380 340,290 430,390 520,300 640,400 760,320 840,520' fill='#b7a58c' stroke='#7a6a55' stroke-width='1.4'/>")
        s.append("<polygon points='300,318 340,290 380,318' fill='#ffffff' opacity='.85'/>" + _t(300, 300, "雪线/高峰", "lbl-s"))
        s.append("<path d='M120 500 C300 470 560 500 820 470' fill='none' stroke='#5b93b8' stroke-width='3'/>" + _t(560, 466, "河流下切", "lbl-s"))
    elif any(k in t for k in ("河", "江", "流域", "三角洲")):
        s.append("<polygon points='60,520 60,360 300,320 560,360 840,380 840,520' fill='#d9c9a6' stroke='#a08a5f'/>")
        s.append("<path d='M80 340 C300 360 520 372 820 392' fill='none' stroke='#5b93b8' stroke-width='6'/>")
        s.append("<path d='M700 392 C740 400 800 420 860 430' fill='none' stroke='#5b93b8' stroke-width='9' opacity='.8'/>")
        s.append(_t(120, 330, "山地源头", "lbl-s") + _t(430, 360, "中游/河漫滩", "lbl-s") + _t(690, 372, "下游三角洲", "lbl-s"))
    elif "盆地" in t:
        s.append("<polygon points='60,520 60,300 200,300 300,470 600,470 700,300 840,300 840,520' fill='#c9b48c' stroke='#8a7452'/>")
        s.append("<rect x='300' y='470' width='300' height='50' fill='#8f8a80' stroke='#5f5a52'/>" + _t(380, 500, "刚性基底", "lbl-s"))
        s.append(_t(360, 350, "盆内充填", "lbl-s") + _t(90, 320, "盆缘山地", "lbl-s") + _t(720, 320, "盆缘山地", "lbl-s"))
    elif "高原" in t:
        s.append("<polygon points='60,520 60,340 360,340 420,300 840,300 840,520' fill='#d9b26a' stroke='#a9822f'/>")
        s.append(_t(120, 330, "高原面", "lbl-s") + _t(600, 290, "边缘陡坎/裂谷", "lbl-s"))
    elif any(k in t for k in ("平原",)):
        s.append("<rect x='60' y='420' width='780' height='100' fill='#cbb98a' stroke='#a08a5f'/>")
        s.append("<g stroke='#9aa77a' stroke-width='1.4'>" + "".join("<path d='M%d 430 v80'/>" % (120 + i * 90) for i in range(8)) + "</g>")
        s.append("<path d='M60 470 C300 460 600 480 840 466' fill='none' stroke='#5b93b8' stroke-width='4'/>")
        s.append(_t(120, 410, "冲积平原/耕地", "lbl-s") + _t(600, 460, "河渠", "lbl-s"))
    elif any(k in t for k in ("沙漠", "戈壁")):
        s.append("<rect x='60' y='420' width='780' height='100' fill='#e4cf94' stroke='#b99b4e'/>")
        s.append("<g fill='none' stroke='#c2a45c' stroke-width='1.4'>" + "".join("<path d='M%d 490 q22 -20 44 0'/>" % (100 + i * 90) for i in range(8)) + "</g>")
        s.append(_t(120, 410, "沙丘（风向自左向右）", "lbl-s"))
    else:
        s.append("<polygon points='60,520 220,360 320,430 440,330 560,430 700,360 840,520' fill='#b7a58c' stroke='#7a6a55'/>")
        s.append("<path d='M60 500 C300 480 600 500 840 484' fill='none' stroke='#5b93b8' stroke-width='3'/>")
        s.append(_t(360, 350, "山地—平原过渡", "lbl-s"))
    return "".join(s)

def theme_climate(e):
    ax = ["<path d='M80 520 L80 300 L840 300' fill='none' stroke='var(--line)' stroke-width='1.5'/>"]
    ax.append(_t(40, 300, "气温", "lbl-s") + _t(830, 520, "月份", "lbl-s"))
    # 温度曲线（定性）
    ax.append("<path d='M90 380 C260 330 420 480 560 430 C680 388 780 420 830 400' fill='none' stroke='#c0392b' stroke-width='3'/>")
    # 降水柱（定性）
    for i, h in enumerate([40, 60, 90, 140, 180, 150, 120, 130, 100, 70, 50, 40]):
        x = 95 + i * 61
        ax.append("<rect x='%d' y='%d' width='32' height='%d' fill='#5b93b8' opacity='.7'/>" % (x, 500 - h, h))
    ax.append(_t(150, 496, "雨季（降水多）", "lbl-s") + _t(560, 496, "旱季", "lbl-s"))
    ax.append(_t(90, 286, "%s 气候：气温与降水年内变化（定性示意，无数值）" % e["title"], "lbl-s"))
    return "".join(ax)

def theme_agriculture(e):
    s = ["<rect x='60' y='320' width='780' height='200' fill='#dcc9a0' stroke='#a08a5f'/>"]
    s.append("<g stroke='#8aa66a' stroke-width='1.6'>" + "".join("<path d='M%d 330 v180'/>" % (110 + i * 80) for i in range(10)) + "</g>")
    s.append("<path d='M60 360 C300 352 600 372 840 360' fill='none' stroke='#5b93b8' stroke-width='5'/>" + _t(360, 350, "灌溉渠", "lbl-s"))
    s.append("<g fill='#6f9a5a'><circle cx='180' cy='420' r='5'/><circle cx='420' cy='440' r='5'/><circle cx='680' cy='420' r='5'/></g>")
    s.append(_t(120, 314, "%s · 农业系统（耕地—灌排—作物，示意）" % e["title"], "lbl-s"))
    return "".join(s)

def theme_trade(e):
    s = ["<rect x='60' y='310' width='780' height='220' fill='#e7ecf0' stroke='var(--line)'/>"]
    nodes = [(150, 380), (300, 460), (470, 360), (650, 440), (760, 360)]
    for i in range(len(nodes) - 1):
        s.append("<path d='M%d %d Q %d %d %d %d' fill='none' stroke='#a4501a' stroke-width='2' stroke-dasharray='6 4'/>" % (
            nodes[i][0], nodes[i][1], (nodes[i][0] + nodes[i+1][0]) // 2, min(nodes[i][1], nodes[i+1][1]) - 40,
            nodes[i+1][0], nodes[i+1][1]))
    for (x, y) in nodes:
        s.append("<circle cx='%d' cy='%d' r='7' fill='#2f6f8f'/>" % (x, y))
    s.append(_t(120, 300, "%s · 贸易网络（节点—路线，示意）" % e["title"], "lbl-s"))
    return "".join(s)

def theme_polity(e):
    tp = (e.get("time_or_place") or "")[:40]
    s = ["<path d='M80 430 H840' stroke='var(--line)' stroke-width='2'/>"]
    for i, (x, lab) in enumerate([(140, "兴起"), (340, "鼎盛"), (560, "转折"), (760, "终结")]):
        s.append("<circle cx='%d' cy='430' r='8' fill='#a4501a'/>" % x)
        s.append(_t(x - 16, 470, lab, "lbl-s"))
    s.append("<rect x='120' y='330' width='660' height='26' fill='#c98a6a' opacity='.55' stroke='#8a5636'/>")
    s.append(_t(130, 320, "%s · 政权更替时间轴（%s）" % (e["title"], tp), "lbl-s"))
    return "".join(s)

def theme_region(e):
    s = ["<rect x='60' y='310' width='780' height='220' fill='#eef1f3' stroke='var(--line)'/>"]
    s.append("<path d='M90 470 C300 420 520 500 810 440' fill='none' stroke='#2f6f8f' stroke-width='2' stroke-dasharray='7 5'/>")
    s.append("<rect x='330' y='360' width='240' height='120' fill='none' stroke='#a4501a' stroke-width='2' stroke-dasharray='8 6'/>")
    s.append("<circle cx='450' cy='420' r='6' fill='#c0392b'/>")
    s.append(_t(120, 300, "%s · 区域范围与联系（虚线为对外联系，示意）" % e["title"], "lbl-s"))
    return "".join(s)

THEME = {"地形": theme_terrain, "气候": theme_climate, "农业": theme_agriculture,
         "贸易": theme_trade, "政权更替": theme_polity, "区域": theme_region}
