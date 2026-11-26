# -*- coding: utf-8 -*-
"""通用插图生成器：按主题生成真实底图定位图 + 主题示意图，替换全站占位曲线。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from locator import map_svg
import ne

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
    ov = ne.overlay((30, 34, 840, 196), tuple(bb), title)
    loc = map_svg((30, 34, 840, 196), tuple(bb), lon, lat, label=title if coords else None, overlay=ov)
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


# ---------- Phase2 专用示意图（真实概念，无数值）----------
def theme_soil(e, coords=None):
    s = ["<rect x='60' y='256' width='360' height='290' fill='#efe8da' stroke='#b3a488'/>"]
    layers = [("O 枯枝落叶层", "#6b5a3a", 40), ("A 表土层(腐殖质)", "#4a3b28", 55),
              ("B 淀积层", "#a9762f", 70), ("C 母质层", "#c9a86a", 65), ("R 基岩", "#8f8a80", 60)]
    y = 256
    for name, col, h in layers:
        s.append(f"<rect x='60' y='{y}' width='360' height='{h}' fill='{col}' opacity='.85' stroke='#7a6a4a'/>")
        s.append(f"<text x='76' y='{y+int(h/2)+4}' class='lbl-s' style='fill:#fff'>{name}</text>")
        y += h
    s.append(_t(70, 250, "%s · 土壤剖面（层次示意）" % e["title"], "lbl-s"))
    # 质地三角
    A = (560, 300); B = (820, 300); C = (690, 520)
    s.append(f"<polygon points='{A[0]},{A[1]} {B[0]},{B[1]} {C[0]},{C[1]}' fill='#f3ece0' stroke='#8a7452' stroke-width='1.4'/>")
    s.append(f"<text x='{A[0]-6}' y='{A[1]-6}' class='lbl-s'>砂土</text>")
    s.append(f"<text x='{B[0]-36}' y='{B[1]-6}' class='lbl-s'>黏土</text>")
    s.append(f"<text x='{C[0]-6}' y='{C[1]+16}' class='lbl-s'>粉砂</text>")
    s.append(f"<text x='560' y='544' class='lbl-s'>土壤质地三角（砂—粉砂—黏土）</text>")
    return "".join(s)

def theme_water(e, coords=None):
    s = ["<rect x='60' y='256' width='780' height='290' fill='#eef4f6' stroke='var(--line)'/>"]
    # 分水岭
    s.append("<path d='M90 500 C220 360 380 360 470 420 C560 480 700 430 810 500' fill='none' stroke='#8a8272' stroke-width='1.6' stroke-dasharray='8 6'/>")
    s.append(_t(96, 348, "分水岭", "lbl-s"))
    # 支流汇聚到干流
    s.append("<path d='M200 380 C260 430 330 460 430 470' fill='none' stroke='#5b93b8' stroke-width='2'/>")
    s.append("<path d='M330 380 C360 430 410 460 440 470' fill='none' stroke='#5b93b8' stroke-width='2'/>")
    s.append("<path d='M430 470 C520 476 640 470 800 452' fill='none' stroke='#5b93b8' stroke-width='5'/>")
    s.append("<circle cx='800' cy='452' r='6' fill='#2f6f8f'/>" + _t(770, 440, "出口/河口", "lbl-s"))
    s.append(_t(70, 250, "%s · 流域与汇流（示意：支流—干流—出口）" % e["title"], "lbl-s"))
    return "".join(s)

def _climate_belt(lat):
    a = abs(lat)
    if a < 10: return "热带"
    if a < 23.5: return "热带/亚热带过渡"
    if a < 35: return "亚热带"
    if a < 50: return "温带"
    if a < 66.5: return "亚寒带"
    return "寒带"

def _theme_climate2(e, coords=None):
    base = theme_climate(e)
    extra = []
    if coords:
        belt = _climate_belt(coords[1])
        hemi = "北" if coords[1] >= 0 else "南"
        extra.append(_t(560, 300, "所在纬度带：%s（约 %d°%s）" % (belt, abs(int(coords[1])), hemi), "lbl-s"))
    extra.append(_t(560, 320, "气候带随纬度与海陆位置分异（示意）", "lbl-s"))
    return base + "".join(extra)

def build(entry, coords=None):
    unit = entry.get("unit_id", "global-themes"); theme = entry.get("theme", "区域"); title = entry["title"]
    lon = coords[0] if coords else None; lat = coords[1] if coords else None
    bb = list(UNIT_BBOX.get(unit, UNIT_BBOX["global-themes"]))
    if lon is not None:
        bb = [min(bb[0], lon - 4), max(bb[1], lon + 4), min(bb[2], lat - 4), max(bb[3], lat + 4)]
    ov = ne.overlay((30, 34, 840, 196), tuple(bb), title)
    loc = map_svg((30, 34, 840, 196), tuple(bb), lon, lat, label=title if coords else None, overlay=ov)
    if "土壤" in title:
        diagram = theme_soil(entry, coords)
    elif any(k in title for k in ("水资源", "湿地", "水文", "海洋保护区", "渔业资源", "海洋生态系统")):
        diagram = theme_water(entry, coords)
    elif theme == "气候":
        diagram = _theme_climate2(entry, coords)
    else:
        diagram = {"地形": theme_terrain, "农业": theme_agriculture, "贸易": theme_trade,
                   "政权更替": theme_polity, "区域": theme_region}.get(theme, theme_region)(entry)
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 600' role='img' aria-label='%s 示意图'>" % title
            + "<rect x='20' y='20' width='860' height='560' rx='12' fill='none' stroke='var(--line)'/>"
            + "<text x='40' y='30' class='lbl'>%s · %s</text>" % (title, theme)
            + "<text x='30' y='46' class='lbl-s'>所在区域（真实陆地轮廓；红点为该条目所在）</text>"
            + loc + "<path d='M30 244 L870 244' stroke='var(--line)'/>" + diagram
            + "<text x='40' y='572' class='dim'>示意图，非精确测绘；底图仅示意相对位置，不涉政治主张</text></svg>")


# ---------- Phase3 历史疆域快照 ----------
import histmap
YEAR = {
"古埃及早王朝":-3000,"古埃及古王国":-2000,"古埃及中王国":-1800,"古埃及新王国":-1300,"罗马阿非利加":200,
"阿拉伯征服北非":700,"法蒂玛王朝":1000,"桑海帝国":1500,"苏美尔城邦":-3000,"阿卡德帝国":-2000,
"古巴比伦":-1700,"亚述帝国":-700,"赫梯王国":-1500,"阿契美尼德波斯":-500,"萨珊波斯":500,"吠陀时代":-1000,
"孔雀王朝":-300,"笈多王朝":400,"商代":-1500,"周代":-700,"秦代":-200,"元代":1300,"吴哥":1200,
"匈奴":-200,"突厥":700,"蒙古帝国":1279,"帖木儿帝国":1400,"克里特文明":-1500,"迈锡尼文明":-1500,
"古希腊城邦":-500,"马其顿与亚历山大":-323,"罗马共和国":-100,"罗马帝国":200,"拜占庭帝国":1000,
"法兰克王国":800,"神圣罗马帝国":1600,"基辅罗斯":1000,"莫斯科公国":1500,"奥尔梅克":-1000,
"玛雅文明":700,"阿兹特克":1500,"十三殖民地":1700,"查文文化":-500,"蒂亚瓦纳科":800,"奇穆帝国":1200,
"印加帝国":1500,"巴西殖民经济":1700,"城市起源":-3000,
}

def _hist_diagram(e, coords):
    unit = e.get("unit_id","global-themes")
    bb = list(UNIT_BBOX.get(unit, UNIT_BBOX["global-themes"]))
    if coords:
        bb = [min(bb[0], coords[0]-4), max(bb[1], coords[0]+4), min(bb[2], coords[1]-4), max(bb[3], coords[1]+4)]
    y = histmap.nearest(YEAR[e["title"]])
    frag, hit = histmap.overlay((60, 268, 780, 268), tuple(bb), y, point=coords, title=e["title"])
    yr = ("公元前 %d 年" % (-y)) if y < 0 else ("公元 %d 年" % y)
    return ("<rect x='60' y='268' width='780' height='268' fill='#f4f1ea' stroke='var(--line)'/>" + frag
            + "<text x='66' y='262' class='lbl-s'>历史疆域快照：约 %s（红框为所含政权%s；historical-basemaps, CC BY 4.0，示意）</text>"
              % (yr, ("：" + hit) if hit else ""))

def build(entry, coords=None):
    unit = entry.get("unit_id","global-themes"); theme = entry.get("theme","区域"); title = entry["title"]
    lon = coords[0] if coords else None; lat = coords[1] if coords else None
    bb = list(UNIT_BBOX.get(unit, UNIT_BBOX["global-themes"]))
    if lon is not None:
        bb = [min(bb[0], lon-4), max(bb[1], lon+4), min(bb[2], lat-4), max(bb[3], lat+4)]
    ov = ne.overlay((30,34,840,196), tuple(bb), title)
    loc = map_svg((30,34,840,196), tuple(bb), lon, lat, label=title if coords else None, overlay=ov)
    if theme == "政权更替" and title in YEAR:
        diagram = _hist_diagram(entry, coords)
    elif "土壤" in title:
        diagram = theme_soil(entry, coords)
    elif any(k in title for k in ("水资源","湿地","水文","海洋保护区","渔业资源","海洋生态系统")):
        diagram = theme_water(entry, coords)
    elif theme == "气候":
        diagram = _theme_climate2(entry, coords)
    else:
        diagram = {"地形":theme_terrain,"农业":theme_agriculture,"贸易":theme_trade,"区域":theme_region}.get(theme, theme_region)(entry)
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 600' role='img' aria-label='%s 示意图'>" % title
            + "<rect x='20' y='20' width='860' height='560' rx='12' fill='none' stroke='var(--line)'/>"
            + "<text x='40' y='30' class='lbl'>%s · %s</text>" % (title, theme)
            + "<text x='30' y='46' class='lbl-s'>所在区域（真实陆地轮廓；红点为该条目所在）</text>"
            + loc + "<path d='M30 244 L870 244' stroke='var(--line)'/>" + diagram
            + "<text x='40' y='572' class='dim'>示意图，非精确测绘；底图仅示意相对位置，不涉政治主张</text></svg>")


# ---------- 全站地形：类型化剖面 ----------
import schematics

def _terrain_block(e):
    return "<g transform='translate(0,230) scale(1,0.75)'>" + schematics.draw(e["title"]) + "</g>"

def build(entry, coords=None):
    unit = entry.get("unit_id","global-themes"); theme = entry.get("theme","区域"); title = entry["title"]
    lon = coords[0] if coords else None; lat = coords[1] if coords else None
    bb = list(UNIT_BBOX.get(unit, UNIT_BBOX["global-themes"]))
    if lon is not None:
        bb = [min(bb[0], lon-4), max(bb[1], lon+4), min(bb[2], lat-4), max(bb[3], lat+4)]
    ov = ne.overlay((30,34,840,196), tuple(bb), title)
    loc = map_svg((30,34,840,196), tuple(bb), lon, lat, label=title if coords else None, overlay=ov)
    if theme == "政权更替" and title in YEAR:
        diagram = _hist_diagram(entry, coords)
    elif "土壤" in title:
        diagram = theme_soil(entry, coords)
    elif any(k in title for k in ("水资源","湿地","水文","海洋保护区","渔业资源","海洋生态系统")):
        diagram = theme_water(entry, coords)
    elif theme == "气候":
        diagram = _theme_climate2(entry, coords)
    elif theme == "地形":
        diagram = _terrain_block(entry)
    else:
        diagram = {"农业":theme_agriculture,"贸易":theme_trade,"区域":theme_region}.get(theme, theme_region)(entry)
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 600' role='img' aria-label='%s 示意图'>" % title
            + "<rect x='20' y='20' width='860' height='560' rx='12' fill='none' stroke='var(--line)'/>"
            + "<text x='40' y='30' class='lbl'>%s · %s</text>" % (title, theme)
            + "<text x='30' y='46' class='lbl-s'>所在区域（真实陆地轮廓；红点为该条目所在）</text>"
            + loc + "<path d='M30 244 L870 244' stroke='var(--line)'/>" + diagram
            + "<text x='40' y='572' class='dim'>示意图，非精确测绘；底图仅示意相对位置，不涉政治主张</text></svg>")


import topics

def build(entry, coords=None):
    unit = entry.get("unit_id","global-themes"); theme = entry.get("theme","区域"); title = entry["title"]
    lon = coords[0] if coords else None; lat = coords[1] if coords else None
    bb = list(UNIT_BBOX.get(unit, UNIT_BBOX["global-themes"]))
    if lon is not None:
        bb = [min(bb[0], lon-4), max(bb[1], lon+4), min(bb[2], lat-4), max(bb[3], lat+4)]
    ov = ne.overlay((30,34,840,196), tuple(bb), title)
    loc = map_svg((30,34,840,196), tuple(bb), lon, lat, label=title if coords else None, overlay=ov)
    if theme == "政权更替" and title in YEAR:
        diagram = _hist_diagram(entry, coords)
    elif "土壤" in title:
        diagram = theme_soil(entry, coords)
    elif any(k in title for k in ("水资源","湿地","水文","海洋保护区","渔业资源","海洋生态系统")):
        diagram = theme_water(entry, coords)
    elif theme == "地形":
        diagram = _terrain_block(entry)
    elif theme in ("气候","农业","贸易","区域"):
        diagram = topics.draw(theme, title)
    else:
        diagram = theme_region(entry)
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 600' role='img' aria-label='%s 示意图'>" % title
            + "<rect x='20' y='20' width='860' height='560' rx='12' fill='none' stroke='var(--line)'/>"
            + "<text x='40' y='30' class='lbl'>%s · %s</text>" % (title, theme)
            + "<text x='30' y='46' class='lbl-s'>所在区域（真实陆地轮廓；红点为该条目所在）</text>"
            + loc + "<path d='M30 244 L870 244' stroke='var(--line)'/>" + diagram
            + "<text x='40' y='572' class='dim'>示意图，非精确测绘；底图仅示意相对位置，不涉政治主张</text></svg>")


import koppen

def _climate_koppen(e, coords):
    unit = e.get("unit_id","global-themes")
    bb = list(UNIT_BBOX.get(unit, UNIT_BBOX["global-themes"]))
    if coords:
        bb = [min(bb[0], coords[0]-4), max(bb[1], coords[0]+4), min(bb[2], coords[1]-4), max(bb[3], coords[1]+4)]
    frag, hit = koppen.overlay((60, 268, 780, 264), tuple(bb), point=coords, max_polys=(45 if bb[1]-bb[0] > 150 else 70))
    lab = ""
    if hit:
        name, code = koppen.cn_of(hit[0]); lab = "；红点处：%s（%s）" % (name, code)
    legend = ("<rect x='64' y='538' width='12' height='10' fill='#6fae6a'/><text x='80' y='548' class='lbl-s'>A 热带</text>"
      + "<rect x='154' y='538' width='12' height='10' fill='#e0c078'/><text x='170' y='548' class='lbl-s'>B 干旱</text>"
      + "<rect x='244' y='538' width='12' height='10' fill='#a9d0a0'/><text x='260' y='548' class='lbl-s'>C 温带</text>"
      + "<rect x='334' y='538' width='12' height='10' fill='#9fb8d8'/><text x='350' y='548' class='lbl-s'>D 冷温带</text>"
      + "<rect x='436' y='538' width='12' height='10' fill='#dfe8ea'/><text x='452' y='548' class='lbl-s'>E 极地</text>")
    return ("<rect x='60' y='268' width='780' height='264' fill='#f4f1ea' stroke='var(--line)'/>" + frag
            + "<text x='66' y='262' class='lbl-s'>Köppen 气候分区（真实数据；Beck et al.，经 rjerue/koppen-map%s）</text>" % lab
            + legend)

def build(entry, coords=None):
    unit = entry.get("unit_id","global-themes"); theme = entry.get("theme","区域"); title = entry["title"]
    lon = coords[0] if coords else None; lat = coords[1] if coords else None
    bb = list(UNIT_BBOX.get(unit, UNIT_BBOX["global-themes"]))
    if lon is not None:
        bb = [min(bb[0], lon-4), max(bb[1], lon+4), min(bb[2], lat-4), max(bb[3], lat+4)]
    ov = ne.overlay((30,34,840,196), tuple(bb), title)
    loc = map_svg((30,34,840,196), tuple(bb), lon, lat, label=title if coords else None, overlay=ov)
    if theme == "政权更替" and title in YEAR:
        diagram = _hist_diagram(entry, coords)
    elif "土壤" in title:
        diagram = theme_soil(entry, coords)
    elif any(k in title for k in ("水资源","湿地","水文","海洋保护区","渔业资源","海洋生态系统")):
        diagram = theme_water(entry, coords)
    elif theme == "地形":
        diagram = _terrain_block(entry)
    elif theme == "气候":
        if unit != "global-themes":
            return _climate_full(entry, coords, bb, ov, loc, title, theme)
        diagram = topics.climate(title)
    elif theme in ("农业","贸易","区域"):
        diagram = topics.draw(theme, title)
    else:
        diagram = theme_region(entry)
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 600' role='img' aria-label='%s 示意图'>" % title
            + "<rect x='20' y='20' width='860' height='560' rx='12' fill='none' stroke='var(--line)'/>"
            + "<text x='40' y='30' class='lbl'>%s · %s</text>" % (title, theme)
            + "<text x='30' y='46' class='lbl-s'>所在区域（真实陆地轮廓；红点为该条目所在）</text>"
            + loc + "<path d='M30 244 L870 244' stroke='var(--line)'/>" + diagram
            + "<text x='40' y='572' class='dim'>示意图，非精确测绘；底图仅示意相对位置，不涉政治主张</text></svg>")


import wbdata
import owid
OWID_EXTRA={
 "森林覆盖变化":("land-use","World","forest_land__00006646__area__005110__hectares","全球森林面积","公顷"),
 "土地利用变化":("land-use","World","cropland__00006620__area__005110__hectares","全球耕地面积","公顷"),
}
WB_MAP = {
 "二氧化碳排放清单":("EN.GHG.CO2.PC.CE.AR5","人均二氧化碳排放","吨/人","WLD"),
 "城市化水平":("SP.URB.TOTL.IN.ZS","城镇人口占比","%","WLD"),
 "全球人口规模":("SP.POP.TOTL","总人口","人","WLD"),
 "人口增长":("SP.POP.GROW","人口年增长率","%","WLD"),
 "预期寿命空间差异":("SP.DYN.LE00.IN","出生预期寿命","岁","WLD"),
 "作物单产差异":("AG.YLD.CREL.KG","谷物单产","kg/公顷","WLD"),
 "森林面积占比":("AG.LND.FRST.ZS","森林覆盖率","%","WLD"),
 "农业统计体系":("AG.LND.AGRI.ZS","农业用地占比","%","WLD"),
 "极端贫困空间分布":("SI.POV.DDAY","极端贫困率","%","WLD"),
 "人均产出空间差异":("NY.GDP.PCAP.CD","人均GDP","现价美元","WLD"),
 "儿童发展地域差异":("SP.DYN.IMRT.IN","婴儿死亡率","‰","WLD"),
 "人口年龄结构":("SP.POP.65UP.TO.ZS","65岁以上人口占比","%","WLD"),
 "肥料使用与环境":("AG.CON.FERT.ZS","化肥施用量","kg/公顷","WLD"),
 "全球营养状况":("SN.ITK.DEFC.ZS","营养不良发生率","%","WLD"),
 "澳大利亚混合农业":("AG.YLD.CREL.KG","澳大利亚谷物单产","kg/公顷","AUS"),
 "农业企业与价值链":("EA.PRD.AGRI.KD","农业增加值/劳动者","2015美元","WLD"),
 "土地利用变化":("AG.LND.AGRI.ZS","农业用地占比","%","WLD"),
 "肉奶生产与土地":("AG.PRD.LVSK.XD","畜牧生产指数","2004-06=100","WLD"),
}

def build(entry, coords=None):
    unit = entry.get("unit_id","global-themes"); theme = entry.get("theme","区域"); title = entry["title"]
    lon = coords[0] if coords else None; lat = coords[1] if coords else None
    bb = list(UNIT_BBOX.get(unit, UNIT_BBOX["global-themes"]))
    if lon is not None:
        bb = [min(bb[0], lon-4), max(bb[1], lon+4), min(bb[2], lat-4), max(bb[3], lat+4)]
    ov = ne.overlay((30,34,840,196), tuple(bb), title)
    if theme in ("农业","区域") and unit != "global-themes":
        ov += koppen.faint((30,34,840,196), tuple(bb), coords)
    loc = map_svg((30,34,840,196), tuple(bb), lon, lat, label=title if coords else None, overlay=ov)
    if title in ("全球气温变化","全球气温距平"):
        diagram = owid.panel((60,268,780,264))
    elif title in OWID_EXTRA:
        _sl,_en,_co,_lb,_un = OWID_EXTRA[title]
        diagram = owid.panel2((60,268,780,264), _sl, _en, _co, _lb, _un)
    elif title in WB_MAP:
        ind, label, un = WB_MAP[title][:3]; ctry = WB_MAP[title][3] if len(WB_MAP[title]) > 3 else "WLD"
        diagram = wbdata.panel((60,268,780,264), wbdata.series(ind, ctry), ind, label, un, ctry)[0]
    elif theme == "政权更替" and title in YEAR:
        diagram = _hist_diagram(entry, coords)
    elif "土壤" in title:
        diagram = theme_soil(entry, coords)
    elif any(k in title for k in ("水资源","湿地","水文","海洋保护区","渔业资源","海洋生态系统")):
        diagram = theme_water(entry, coords)
    elif theme == "地形":
        diagram = _terrain_block(entry)
    elif theme == "气候":
        if unit != "global-themes":
            return _climate_full(entry, coords, bb, ov, loc, title, theme)
        diagram = topics.climate(title)
    elif theme in ("农业","贸易","区域"):
        diagram = topics.draw(theme, title)
    else:
        diagram = theme_region(entry)
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 600' role='img' aria-label='%s 示意图'>" % title
            + "<rect x='20' y='20' width='860' height='560' rx='12' fill='none' stroke='var(--line)'/>"
            + "<text x='40' y='30' class='lbl'>%s · %s</text>" % (title, theme)
            + "<text x='30' y='46' class='lbl-s'>所在区域（真实陆地轮廓；红点为该条目所在）</text>"
            + loc + "<path d='M30 244 L870 244' stroke='var(--line)'/>" + diagram
            + "<text x='40' y='572' class='dim'>示意图，非精确测绘；底图仅示意相对位置，不涉政治主张</text></svg>")


def _climate_full(entry, coords, bb, ov, loc, title, theme):
    kfrag, hit = koppen.overlay((60,262,780,236), tuple(bb), point=coords, max_polys=(45 if bb[1]-bb[0]>150 else 70))
    lab=""
    if hit:
        nm,code=koppen.cn_of(hit[0]); lab="；红点处：%s（%s）"%(nm,code)
    legend=("<rect x='64' y='500' width='12' height='10' fill='#6fae6a'/><text x='80' y='510' class='lbl-s'>A 热带</text>"
      +"<rect x='154' y='500' width='12' height='10' fill='#e0c078'/><text x='170' y='510' class='lbl-s'>B 干旱</text>"
      +"<rect x='244' y='500' width='12' height='10' fill='#a9d0a0'/><text x='260' y='510' class='lbl-s'>C 温带</text>"
      +"<rect x='334' y='500' width='12' height='10' fill='#9fb8d8'/><text x='350' y='510' class='lbl-s'>D 冷温带</text>"
      +"<rect x='436' y='500' width='12' height='10' fill='#dfe8ea'/><text x='452' y='510' class='lbl-s'>E 极地</text>")
    co2 = owid.panel((60,536,780,150))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 760' role='img' aria-label='%s 气候示意图'>"%title
      +"<rect x='20' y='20' width='860' height='720' rx='12' fill='none' stroke='var(--line)'/>"
      +"<text x='40' y='30' class='lbl'>%s · %s</text>"%(title,theme)
      +"<text x='30' y='46' class='lbl-s'>所在区域（真实陆地轮廓；红点为该条目所在）</text>"
      +loc+"<path d='M30 244 L870 244' stroke='var(--line)'/>"
      +"<rect x='60' y='262' width='780' height='236' fill='#f4f1ea' stroke='var(--line)'/>"+kfrag
      +"<text x='66' y='258' class='lbl-s'>Köppen 气候分区（真实数据；Beck et al.，经 rjerue/koppen-map%s）</text>"%lab
      +legend+co2
      +"<text x='40' y='740' class='dim'>示意图，非精确测绘；底图仅示意相对位置，不涉政治主张</text></svg>")



def _climate_full(entry, coords, bb, ov, loc, title, theme):
    kfrag, hit = koppen.overlay((60,262,780,186), tuple(bb), point=coords, max_polys=(40 if bb[1]-bb[0]>150 else 64))
    lab=""
    if hit:
        nm,code=koppen.cn_of(hit[0]); lab="；红点处：%s（%s）"%(nm,code)
    legend=("<rect x='64' y='452' width='12' height='10' fill='#6fae6a'/><text x='80' y='462' class='lbl-s'>A 热带</text>"
      +"<rect x='154' y='452' width='12' height='10' fill='#e0c078'/><text x='170' y='462' class='lbl-s'>B 干旱</text>"
      +"<rect x='244' y='452' width='12' height='10' fill='#a9d0a0'/><text x='260' y='462' class='lbl-s'>C 温带</text>"
      +"<rect x='334' y='452' width='12' height='10' fill='#9fb8d8'/><text x='350' y='462' class='lbl-s'>D 冷温带</text>"
      +"<rect x='436' y='452' width='12' height='10' fill='#dfe8ea'/><text x='452' y='462' class='lbl-s'>E 极地</text>")
    temp = owid.panel((60,470,780,150))
    precip = wbdata.panel((60,628,780,150), wbdata.series("AG.LND.PRCP.MM","WLD"), "AG.LND.PRCP.MM", "全球平均降水深度", "mm/年", "WLD")[0]
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 900' role='img' aria-label='%s 气候示意图'>"%title
      +"<rect x='20' y='20' width='860' height='860' rx='12' fill='none' stroke='var(--line)'/>"
      +"<text x='40' y='30' class='lbl'>%s · %s</text>"%(title,theme)
      +"<text x='30' y='46' class='lbl-s'>所在区域（真实陆地轮廓；红点为该条目所在）</text>"
      +loc+"<path d='M30 244 L870 244' stroke='var(--line)'/>"
      +"<rect x='60' y='262' width='780' height='186' fill='#f4f1ea' stroke='var(--line)'/>"+kfrag
      +"<text x='66' y='258' class='lbl-s'>Köppen 气候分区（真实数据；Beck et al.，经 rjerue/koppen-map%s）</text>"%lab
      +legend+temp+precip
      +"<text x='40' y='878' class='dim'>示意图，非精确测绘；底图仅示意相对位置，不涉政治主张</text></svg>")
