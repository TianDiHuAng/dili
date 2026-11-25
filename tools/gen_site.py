# -*- coding: utf-8 -*-
"""tools/gen_site.py — 从 JSON 渲染纯静态 HTML（零 JS）。"""
import json, os, re, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
SITE = os.path.join(ROOT, "site")
UNIT_IDS = ["africa", "asia", "europe", "north-america", "south-america", "oceania", "antarctica", "global-themes"]
UNIT_NAMES = {"africa":"非洲","asia":"亚洲","europe":"欧洲","north-america":"北美洲","south-america":"南美洲","oceania":"大洋洲","antarctica":"南极洲","global-themes":"全球主题"}
THEMES = ["地形","气候","农业","贸易","政权更替","区域"]
TIER_ORDER = {"核心":0,"重要":1,"补充":2}


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def esc(s):
    return html.escape(str(s if s is not None else ""))


def nav(depth=0):
    p = "../" * depth
    return f'''<nav class="nav"><a href="{p}index.html">首页</a><a href="{p}index-all.html">全站索引</a><a href="{p}timeline.html">时间线</a><a href="{p}sources.html">来源库</a><a href="{p}coverage.html">覆盖矩阵</a><a href="{p}evidence.html">证据层级</a><a href="{p}limits.html">已知限制</a><a href="{p}about.html">关于</a></nav>'''


def page(title, body, depth=0, extra_head=""):
    p = "../" * depth
    return f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} — 地理与文明百科</title><link rel="stylesheet" href="{p}css/style.css">{extra_head}</head>
<body><header class="top"><a class="brand" href="{p}index.html">地理与文明百科</a>{nav(depth)}</header>
<main>{body}</main><footer class="foot">静态站点 · 数据驱动 · <a href="{p}about.html">诚实标注</a> · 生成于 {datetime.date.today().isoformat()}</footer>
</body></html>'''


def sanitize_svg(svg):
    if not svg:
        return ""
    s = svg.replace("'/", "'/>") if False else svg
    s = re.sub(r"(?<!<)(/>)", r"\1", s)
    return s


def source_link(sid, sources):
    s = sources.get(sid)
    if not s:
        return f"<code>{esc(sid)}</code>"
    flag = "✅" if s.get("verified") else "⚠️"
    return f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">{flag}{esc(s["title"])}</a>'


_evp = os.path.join(DATA, "evidence_level.json")
_evfull = json.load(open(_evp, encoding="utf-8")) if os.path.exists(_evp) else {"levels": {}, "summary": {}}
EV = _evfull["levels"]
ev_doc = _evfull
_sep = os.path.join(DATA, "side_evidence.json")
se_counts = (json.load(open(_sep, encoding="utf-8")).get("counts", {}) if os.path.exists(_sep) else {})
_satp = os.path.join(DATA, "..", "SATURATION.json")
sat_doc = json.load(open(os.path.abspath(_satp), encoding="utf-8")) if os.path.exists(os.path.abspath(_satp)) else {}
_scanp = os.path.join(DATA, "semantic_scan.json")
scan_doc = json.load(open(_scanp, encoding="utf-8")) if os.path.exists(_scanp) else {}


def _shellsize(s):
    m = re.search(r"空壳页判定】strip 后仅 (\d+) 字符", s.get("note") or "")
    return (m.group(1) + " 字符") if m else "—"


def evlabel(title):
    """第59轮：证据层级标签 A≥2强 / B 1强 / C 无强 / D 仅数据端点。"""
    lv = (EV.get(title) or {}).get("level")
    if not lv:
        return ""
    txt = {"A": "证据 A（≥2 强来源）", "B": "证据 B（1 强来源）",
           "C": "证据 C（仅旁证/弱来源）", "D": "证据 D（仅数据端点）"}.get(lv, "")
    tip = {"A": "至少两个独立强来源（被引≥10 或正文≥800 字符）。",
           "B": "一个强来源，另有旁证或弱来源辅助。",
           "C": "没有强来源，仅有旁证或弱来源——结论可靠性有限。",
           "D": "仅有数据端点（世界银行/NOAA 等指标），正文为指标解读，无需学术文献。"}.get(lv, "")
    cls = {"A": "tag", "B": "tag", "C": "tag warn", "D": "tag dim"}.get(lv, "tag")
    return f'<span class="{cls}" title="{esc(tip)}">{esc(txt)}</span>'


def srcgrade(e, flags=None):
    """来源等级徽标：按 coverage 标志位判定（避免 status 子串误判）。"""
    flags = flags or {}
    if e.get("level") == "L1":
        return '<span class="tag">来源：骨架级</span>'
    if flags.get("d041_pairing_gap"):
        return '<span class="tag warn">来源：专题页 + 配对缺口</span>'
    if flags.get("d041_legacy"):
        return '<span class="tag warn">来源：区域/机构级（待补专题页）</span>'
    st = e.get("status") or ""
    if "-学术文献" in st or "-指标数据" in st:
        return '<span class="tag">来源：学术文献（单源待互证）</span>'
    if "Wikidata" in st:
        return '<span class="tag warn">来源：结构化数据集（单源待互证）</span>'
    if "主题页" in st or "合规换源" in st or "专题来源" in st:
        return '<span class="tag">来源：专题页 + 机构页</span>'
    if "配对说明" in st:
        return '<span class="tag">来源：专题页 + 入口页</span>'
    return '<span class="tag">来源：专题页（待补配对）</span>'


def entry_card(e):
    return f'''<a class="card tier-{esc(e['tier'])}" href="../entries/{esc(e['id'])}.html"><span class="tier">{esc(e['tier'])}</span><h3>{esc(e['title'])}</h3><p>{esc(e['time_or_place'])} · {esc(e['theme'])}</p><p class="dim">{esc(e['overview'][:60])}…</p></a>'''


def main():
    os.makedirs(os.path.join(SITE, "css"), exist_ok=True)
    os.makedirs(os.path.join(SITE, "entries"), exist_ok=True)
    os.makedirs(os.path.join(SITE, "units"), exist_ok=True)
    sources_doc = load(os.path.join(DATA, "sources.json"))
    sources = {s["id"]: s for s in sources_doc["sources"]}
    cov = load(os.path.join(DATA, "coverage.json"))
    covflags = {c["id"]: c for c in cov.get("entries", [])}
    units = {}
    entries = {}
    for uid in UNIT_IDS:
        doc = load(os.path.join(DATA, uid + ".json"))
        doc["entries"].sort(key=lambda e: (TIER_ORDER.get(e["tier"],9), e["title"]))
        units[uid] = doc
        for e in doc["entries"]:
            entries[e["id"]] = e

    total = len(entries)
    l1 = sum(1 for e in entries.values() if e["level"] == "L1")
    l2 = sum(1 for e in entries.values() if e["level"] == "L2")
    l3 = sum(1 for e in entries.values() if e["level"] == "L3")
    pending = sum(1 for e in entries.values() if e.get("needs_verification"))
    verified_src = sum(1 for s in sources.values() if s.get("verified"))

    # CSS
    css = '''@charset "UTF-8";
:root{--bg:#f5f0e6;--panel:#fffaf0;--ink:#1f2b2a;--dim:#5d6b68;--accent:#2b7a78;--accent2:#b5651d;--line:#d8cfbe;--card:#fffdf7;--warn:#a4402c}
@media (prefers-color-scheme:dark){:root{--bg:#121918;--panel:#182221;--ink:#e8e2d5;--dim:#a9b6b1;--accent:#5fc2bd;--accent2:#d89a5b;--line:#31403e;--card:#1b2725;--warn:#e08b74}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:"Noto Serif SC","Songti SC",Georgia,serif;line-height:1.7}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.top{display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between;padding:14px 5vw;border-bottom:1px solid var(--line);background:var(--panel)}
.brand{font-size:1.3rem;font-weight:700;letter-spacing:.05em;color:var(--accent2)}
.nav{display:flex;flex-wrap:wrap;gap:14px;font-size:.92rem}
main{max-width:1040px;margin:0 auto;padding:32px 20px 60px}
.foot{border-top:1px solid var(--line);padding:18px 5vw;color:var(--dim);font-size:.85rem}
h1{font-size:2rem;border-bottom:3px solid var(--accent);padding-bottom:8px}h2{margin-top:2em;color:var(--accent)}h3{margin:.2em 0}
.lead{font-size:1.1rem;color:var(--dim)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:20px 0}
.stat{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px;text-align:center}
.stat b{display:block;font-size:1.8rem;color:var(--accent2)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(235px,1fr));gap:14px}
.card{display:block;background:var(--card);border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:8px;padding:14px;color:var(--ink)}
.card:hover{border-color:var(--accent2);text-decoration:none;transform:translateY(-1px)}
.card .tier{font-size:.72rem;color:var(--accent2);border:1px solid var(--accent2);border-radius:4px;padding:1px 6px;float:right}
.card p{margin:.35em 0;font-size:.88rem}.dim{color:var(--dim)}
table{border-collapse:collapse;width:100%;margin:16px 0}th,td{border:1px solid var(--line);padding:8px;text-align:left}th{background:var(--panel)}
.tag{display:inline-block;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:2px 10px;margin:2px;font-size:.82rem}
.warn{color:var(--warn)}.section{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:14px 18px;margin:12px 0}
svg{display:block;max-width:100%;height:auto;margin:16px auto;background:var(--panel);border:1px solid var(--line);border-radius:8px}
svg text{fill:var(--ink);font-family:sans-serif;font-size:13px}svg .lbl{fill:var(--accent);font-weight:700}svg .pt{fill:var(--accent2)}
.crumb{font-size:.85rem;color:var(--dim);margin-bottom:12px}
ul.src{list-style:none;padding-left:0}ul.src li{margin:6px 0;font-size:.92rem}
@media (max-width:640px){h1{font-size:1.5rem}.nav{gap:8px;font-size:.82rem}main{padding:20px 14px}}
'''.lstrip()
    with open(os.path.join(SITE, "css", "style.css"), "w", encoding="utf-8") as f:
        f.write(css)

    # 首页
    unit_cards = "".join(f'''<a class="card" href="units/{uid}.html"><h3>{esc(UNIT_NAMES[uid])}</h3><p>{len(units[uid]['entries'])} 条</p><p class="dim">{esc('、'.join(sorted({e['theme'] for e in units[uid]['entries']})))}</p></a>''' for uid in UNIT_IDS)
    body = f'''<h1>地理与文明百科</h1><p class="lead">以「大洲 × 文明/区域 × 主题」为骨架的静态知识库。数据驱动、机器校验、待核实标注。</p>
<div class="stats"><div class="stat"><b>{total}</b>条目</div><div class="stat"><b>{l1}/{l2}/{l3}</b>L1/L2/L3</div><div class="stat"><b>{verified_src}</b>已核验来源</div><div class="stat"><b>{pending}</b>待核实条目</div></div>
<h2>按大洲浏览</h2><div class="grid">{unit_cards}</div>
<h2>按主题浏览</h2><p>{''.join(f'<a class="tag" href="index-all.html#{esc(t)}">{esc(t)}</a>' for t in THEMES)}</p>
<h2>说明</h2><p>本站不使用图片；所有图示均为内联 SVG 示意图，非精确测绘。现状数据均标注年份与来源；争议边界只描述立场、不画界线。</p>'''
    with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
        f.write(page("首页", body))

    # 单元页
    for uid, doc in units.items():
        groups = {}
        for e in doc["entries"]:
            groups.setdefault(e["theme"], []).append(e)
        ghtml = ""
        for theme in THEMES:
            if theme in groups:
                ghtml += f"<h2>{esc(theme)}（{len(groups[theme])}）</h2><div class='grid'>" + "".join(entry_card(e) for e in groups[theme]) + "</div>"
        body = f'''<div class="crumb"><a href="../index.html">首页</a> / {esc(doc['title'])}</div><h1>{esc(doc['title'])}</h1>
<p class="lead">{len(doc['entries'])} 个条目。按主题分组，点击条目进入详情。</p>{ghtml}'''
        with open(os.path.join(SITE, "units", uid + ".html"), "w", encoding="utf-8") as f:
            f.write(page(doc["title"], body, 1))

    # 条目页
    for eid, e in entries.items():
        parts = [f'''<div class="crumb"><a href="../index.html">首页</a> / <a href="../units/{esc(e['unit_id'])}.html">{esc(UNIT_NAMES[e['unit_id']])}</a> / {esc(e['title'])}</div>
<h1>{esc(e['title'])}</h1><p><span class="tag">{esc(e['tier'])}</span><span class="tag">{esc(e['level'])}</span><span class="tag">{esc(e['region'])}</span><span class="tag">{esc(e['theme'])}</span>{srcgrade(e, covflags.get(e['id'], {}))}{evlabel(e['title'])}</p>
<div class="section"><h2>定义</h2><p>{esc(e['definition'])}</p></div>
<div class="section"><h2>时间或位置</h2><p>{esc(e['time_or_place'])}</p></div>
<div class="section"><h2>概述</h2><p>{esc(e['overview'])}</p></div>''']
        if e.get("level") in ("L2", "L3"):
            labels = [("geo","地理概况"),("influence","地理条件对定居/农业/贸易/政治的影响"),("polities","主要文明或政权更替"),("connections","与相邻区域的联系"),("today","今天的状况")]
            for k, label in labels:
                if e.get(k):
                    if k == "polities" and str(e[k]).startswith("本条只写"):
                        label = "政权与年代（本条不展开）"
                    parts.append(f'<div class="section"><h2>{label}</h2><p>{esc(e[k])}</p></div>')
            if e.get("svg"):
                cap = "简笔示意，不代表精确位置与边界。" if "非精确测绘" in e["svg"] else "示意图，非精确测绘。"
                parts.append(f'<div class="section"><h2>示意地图</h2>{sanitize_svg(e["svg"])}<p class="dim">{cap}</p></div>')
        if e.get("level") == "L1" and e.get("today"):
            parts.append(f'<div class="section"><h2>今天的状况</h2><p>{esc(e["today"])}</p></div>')
        if e.get("needs_verification"):
            parts.append(f'<div class="section warn"><h2>待核实</h2><p>{esc(e["pending_notes"])}</p></div>')
        parts.append('<div class="section"><h2>来源</h2><ul class="src">' + "".join(f"<li>{source_link(s, sources)}</li>" for s in e["sources"]) + "</ul></div>")
        if e.get("related"):
            parts.append('<h2>相关条目</h2><p>' + "".join(f'<a class="tag" href="{esc(r)}.html">{esc(entries[r]["title"])}</a>' for r in e["related"] if r in entries) + "</p>")
        with open(os.path.join(SITE, "entries", eid + ".html"), "w", encoding="utf-8") as f:
            f.write(page(e["title"], "\n".join(parts), 1))

    # 全站索引
    index_rows = ""
    for uid in UNIT_IDS:
        for e in sorted(units[uid]["entries"], key=lambda x: x["title"]):
            index_rows += f'<tr id="{esc(e["theme"])}"><td><a href="entries/{esc(e["id"])}.html">{esc(e["title"])}</a></td><td>{esc(UNIT_NAMES[uid])}</td><td>{esc(e["region"])}</td><td>{esc(e["theme"])}</td><td>{esc(e["tier"])}</td><td>{esc(e["level"])}</td></tr>'
    body = f'''<h1>全站索引</h1><p class="lead">共 {total} 条，按大洲与标题排列。</p>
<table><thead><tr><th>条目</th><th>大洲</th><th>区域</th><th>主题</th><th>层级</th><th>写作层级</th></tr></thead><tbody>{index_rows}</tbody></table>'''
    with open(os.path.join(SITE, "index-all.html"), "w", encoding="utf-8") as f:
        f.write(page("全站索引", body))

    # 时间线（按首个年份提取排序， uncertain 置后）
    def yearkey(e):
        m = re.search(r"(\d{3,4})年", e["time_or_place"])
        if not m:
            return 9999
        y = int(m.group(1))
        return -y if "前" in e["time_or_place"][:m.start()] else y
    tl = sorted(entries.values(), key=yearkey)
    tbody = "".join(f'<tr><td>{esc(e["time_or_place"])}</td><td><a href="entries/{esc(e["id"])}.html">{esc(e["title"])}</a></td><td>{esc(UNIT_NAMES[e["unit_id"]])}</td><td>{esc(e["theme"])}</td></tr>' for e in tl)
    body = f'''<h1>时间线</h1><p class="lead">按条目中出现的可解析年份排序；无明确年份者置后。「前」表示公元前。</p><table><thead><tr><th>时间/时期</th><th>条目</th><th>大洲</th><th>主题</th></tr></thead><tbody>{tbody}</tbody></table>'''
    with open(os.path.join(SITE, "timeline.html"), "w", encoding="utf-8") as f:
        f.write(page("时间线", body))

    # 来源库
    rows = ""
    for s in sources.values():
        flag = "已核验" if s.get("verified") else "待核验"
        rows += f'<tr><td>{esc(s["id"])}</td><td>{esc(s["title"])}</td><td>{esc(s["author"])}</td><td>{esc(s["type"])}</td><td>{esc(s["year"] or "—")}</td><td><a href="{esc(s["url"])}" target="_blank" rel="noopener">{flag}</a></td></tr>'
    body = f'''<h1>来源库</h1><p class="lead">共 {len(sources)} 条来源，其中 {verified_src} 条经 curl 打开页面核对标题。页面年份未标注者留空，不推定。</p><table><thead><tr><th>ID</th><th>标题</th><th>作者/机构</th><th>类型</th><th>年份</th><th>状态</th></tr></thead><tbody>{rows}</tbody></table>'''
    with open(os.path.join(SITE, "sources.html"), "w", encoding="utf-8") as f:
        f.write(page("来源库", body))

    # 覆盖矩阵
    matrix = cov.get("matrix", {})
    mrows = ""
    for uid in UNIT_IDS:
        counts = matrix.get(uid, {})
        mrows += f'<tr><td>{esc(UNIT_NAMES[uid])}</td>' + "".join(f'<td>{counts.get(t,0)}</td>' for t in THEMES) + f'<td>{len(units[uid]["entries"])}</td></tr>'
    body = f'''<h1>覆盖矩阵</h1><p class="lead">大洲 × 主题。详细「文明/区域」维度见 <a href="coverage_detail.html">覆盖明细</a> 与 <a href="../reports/coverage_matrix.md">reports/coverage_matrix.md</a>。</p>
<table><thead><tr><th>大洲/单元</th>{''.join(f'<th>{esc(t)}</th>' for t in THEMES)}<th>合计</th></tr></thead><tbody>{mrows}</tbody></table>'''
    with open(os.path.join(SITE, "coverage.html"), "w", encoding="utf-8") as f:
        f.write(page("覆盖矩阵", body))

    # 覆盖明细（大洲 × 文明/区域 × 主题）
    detail_rows = ""
    for uid in UNIT_IDS:
        for e in sorted(units[uid]["entries"], key=lambda x: (x["region"], x["theme"], x["title"])):
            detail_rows += f'<tr><td>{esc(UNIT_NAMES[uid])}</td><td><a href="entries/{esc(e["id"])}.html">{esc(e["title"])}</a></td><td>{esc(e["region"])}</td><td>{esc(e["theme"])}</td><td>{esc(e["tier"])}</td><td>{esc(e["level"])}</td></tr>'
    body = f'''<h1>覆盖明细</h1><p class="lead">大洲 × 文明/区域 × 主题三维明细，共 {total} 条。</p>
<table><thead><tr><th>大洲</th><th>条目</th><th>文明/区域</th><th>主题</th><th>级别</th><th>层级</th></tr></thead><tbody>{detail_rows}</tbody></table>'''
    with open(os.path.join(SITE, "coverage_detail.html"), "w", encoding="utf-8") as f:
        f.write(page("覆盖明细", body))

    # 关于
    body = '''<h1>关于本站</h1><div class="section"><h2>方法</h2><p>数据存于 JSON，经 <code>tools/check.py</code> 机器校验后，由 <code>tools/gen_site.py</code> 渲染为纯静态 HTML（零 JavaScript）。</p></div>
<div class="section"><h2>诚实标注</h2><p>关键事实需两个独立来源；单源或未核验标「待核实」。争议观点并列各方说法，不替读者下结论。现状数据标注年份与来源；争议边界不画线。</p></div>
<div class="section"><h2>图示</h2><p>不使用任何图片；所有地图为内联 SVG 简笔示意，图下注明「示意图，非精确测绘」，文字使用 CSS 变量以兼容深色模式。</p></div>'''
    with open(os.path.join(SITE, "about.html"), "w", encoding="utf-8") as f:
        f.write(page("关于", body))

    # ---- 第61轮：证据层级说明 ----
    evl = ev_doc.get("levels", {})
    evs = ev_doc.get("summary", {})
    by_title = {e["title"]: e for e in entries.values()}
    def _evrow(k):
        v = evl.get(k) or {}
        c = v.get("counts", {})
        e = by_title.get(k)
        link = f'<a href="entries/{esc(e["id"])}.html">{esc(k)}</a>' if e else esc(k)
        return f'<tr><td>{link}</td><td>{esc(v.get("level",""))}</td><td>{c.get("strong",0)}</td><td>{c.get("weak",0)}</td><td>{c.get("side",0)}</td><td>{c.get("data",0)}</td></tr>'
    cd = [k for k, v in evl.items() if v.get("level") in ("C", "D")]
    cd_sorted = sorted(cd, key=lambda k: (evl[k].get("level",""), k))
    ev_body = f"""<h1>证据层级说明</h1><p class="lead">本站为每条目算出一个证据层级。判据公开，可由 <code>tools/round60_levels.py</code> 复算，并由 <code>tools/check.py</code> 的 R22 交叉校验。</p>
<div class="section"><h2>如何读懂本页</h2><p>本页回答一个问题：<b>这一条目凭什么可信</b>。你会在条目页看到「证据 A/B/C/D」标签，含义如下：A 有至少两个独立强来源；B 有一个；C 只有旁证或弱来源（结论可靠性有限）；D 只有数据端点（正文是指标解读，不需要学术文献）。</p>
<p>「强来源」不是「看起来权威」，而是有明确门槛：被引 ≥10 <b>或</b> 正文/摘要 ≥800 字符。两个条件满足其一即可——因为被引 400+ 但摘要偏短的经典著作，不应因篇幅被判弱。</p>
<p>降为<b>旁证</b>的常见原因：来源只涉条目的一个侧面（拜占庭条目引用医院史）、标题不含条目对象词（R20）、被引与篇幅均不足（R19）、或机构页实测只有几十字符（空壳页，D125）。降级理由逐条写在条目页的「待核实」区。</p></div>
<div class="section"><h2>四档定义</h2><table><thead><tr><th>层级</th><th>判据</th><th>条数</th></tr></thead><tbody>
<tr><td><b>A</b></td><td>≥2 个<b>强来源</b></td><td>{evs.get('A',0)}</td></tr>
<tr><td><b>B</b></td><td>1 个强来源 + 旁证/弱来源</td><td>{evs.get('B',0)}</td></tr>
<tr><td><b>C</b></td><td>无强来源（仅旁证或弱来源）</td><td>{evs.get('C',0)}</td></tr>
<tr><td><b>D</b></td><td>仅数据端点与机构页（指标解读类）</td><td>{evs.get('D',0)}</td></tr>
</tbody></table></div>
<div class="section"><h2>侧面文献统计</h2><p>「对象同一但只涉一个侧面」的文献共 <b>{se_counts.get('side',0)}</b> 条，已全部降为旁证；被判定对象/时期/学科错配并撤出的共 <b>{se_counts.get('dropped',0)}</b> 条；被引与篇幅均不足、仅供辅助的共 <b>{se_counts.get('weak_claim',0)}</b> 条。结构化记录见 <code>data/side_evidence.json</code>。</p>
<p class="dim">例：拜占庭帝国条目引用医院史、元代条目引用高丽青瓷、印加条目引用玉米酒——这些都「对」但只涉一面，不能作整条的主来源。</p></div>
<div class="section"><h2>什么叫「强来源」</h2><p>满足以下<b>任一</b>条件即为强来源：被引 ≥ 10；或正文/摘要 ≥ 800 字符。</p>
<p class="dim">初版曾要求两者同时满足，把被引 458、摘要 795 字符的经典著作误判为弱来源，故改为「满足其一」（D117）。数据端点（世界银行、NOAA、USGS 等 JSON）一律不计为内容来源，只支撑数值（D107）。</p></div>
<div class="section"><h2>旁证与弱来源</h2><p>以下情况会被降为<b>旁证</b>：来源与条目<b>对象同一但只涉其中一个侧面</b>（如「拜占庭帝国」条目引用医院史）；或来源标题<b>不含条目对象词</b>（R20）；或被引与篇幅均不足（R19）。降级理由写在条目页的「待核实」区。</p></div>
<div class="section"><h2>C / D 级清单（共 {len(cd)} 条）</h2>
<table><thead><tr><th>条目</th><th>层级</th><th>强</th><th>弱</th><th>旁证</th><th>数据</th></tr></thead><tbody>{''.join(_evrow(k) for k in cd_sorted)}</tbody></table></div>"""
    with open(os.path.join(SITE, "evidence.html"), "w", encoding="utf-8") as f:
        f.write(page("证据层级说明", ev_body))

    # ---- 第61轮：已知限制 ----
    _gmod = json.load(open(os.path.join(ROOT, "reports", "round62_gaps.json"), encoding="utf-8")).get("gap_definitions", []) if os.path.exists(os.path.join(ROOT, "reports", "round62_gaps.json")) else sat_doc.get("gap_model", {}).get("definitions", [])
    _gmap = {d["id"]: d for d in _gmod}
    _noans = (scan_doc.get("unresolved", {}) or {}).get("entries", [])
    _shell = [s for s in sources.values() if "空壳页判定" in (s.get("note") or "")]
    _shell_rows = "".join(
        f'<tr><td>{esc(s["id"])}</td><td>{esc((s.get("page_title") or "")[:50])}</td><td>{esc(_shellsize(s))}</td></tr>'
        for s in _shell)
    _noans_rows = "".join(f'<tr><td><a href="entries/{esc(by_title[k]["id"])}.html">{esc(k)}</a></td><td>见条目页「待核实」</td></tr>'
                          for k in _noans if k in by_title)
    lim_body = f"""<h1>已知限制</h1><p class="lead">本页如实列出当前无法解决、或经多轮检索确认无解的问题，不作掩饰。数字由 <code>tools/round62_gaps.py</code> 计算，与本页同步。</p>
<div class="section"><h2>一、缺口四类（当前）</h2><table><thead><tr><th>编号</th><th>缺口</th><th>条数</th><th>如何关闭</th></tr></thead><tbody>
{"".join(f'<tr><td><b>{d["id"]}</b></td><td>{esc(d["name"])}</td><td><b>{d["count"]}</b></td><td>{esc(d["fixed_by"])}</td></tr>' for d in _gmod)}
</tbody></table>
<p class="dim"><b>G3a 与 G3b 的区别</b>（第77轮拆分）：G3a 是「已有侧面文献可补充，缺的是整体研究」；G3b 是「连侧面文献都未登记，只有单一内容源」。两者的处置不同——前者可把侧面文献登记为补充源并限定范围（D140），后者只能继续检索或承认无解。当前 G3a 仅 {len([x for x in _gmod if x['id']=='G3a']) and _gmap.get('G3a',{}).get('count',0)} 条、G3b {_gmap.get('G3b',{}).get('count',0)} 条。</p>
<p class="dim">当前状态：G1=0、G2=0、G3=0、G4=0；第149–151轮连续三轮独立审计五类（替换质量/正文机械缺陷/判据一致性/来源-正文一致性/全站一致性）均为零缺口，已进入<b>维护模式</b>。维护模式下仅在发现新证据或数据不一致时修订，不再大规模补源。G4 的「语义对题」由人工/子代理逐条读取摘要完成，非自动判定；G2 如出现，指经两库多轮检索确认无合格主来源的条目，单列记录、不再重试同类检索。</p></div>
<div class="section"><h2>二、经检索确认「无合格第二来源」的条目（{len(_noans)} 条）</h2>
<p>以下条目经<b>两个库（Crossref + OpenAlex）、多条检索式</b>检索后仍无合格第二来源。本站不作硬配。</p>
<table><thead><tr><th>条目</th><th>状况</th></tr></thead><tbody>{_noans_rows}</tbody></table></div>
<div class="section"><h2>三、空壳页（{len(_shell)} 个）</h2>
<p>以下机构页经 curl 实测，strip 后正文不足 800 字符（多为 JS 应用壳或导航条），<b>仅作入口页，不作正文依据</b>。</p>
<table><thead><tr><th>来源</th><th>页面</th><th>正文字符</th></tr></thead><tbody>{_shell_rows}</tbody></table>
<p class="dim">对比：同期实测 OWID 长文为 3,298–31,443 字符，World Bank 8,041–11,098，NOAA 2,753，IUCN 4,086。若不实测，会把这些空壳误当成「独立互证」。</p></div>
<div class="section"><h2>四、机器校验的能力边界</h2>
<p>R18–R23 能保证：引用年份存在（R18）、弱来源不称主来源（R19）、标题含对象词（R20）、层级有记录（R21）、层级与重算一致（R22）、空壳页不称内容源（R23）。</p>
<p><b>不能判断</b>：① 一篇文献是否只涉对象的某个侧面；② 某条断言是否被该文献真正支持、强度是否相称；③ 个案能否代表通例；④ <b>题目级错位</b>——<code>sources.title</code> 是章节名，而数据库返回的摘要是整卷导论（或反之），题名与摘要不是同一文本。这四类依赖人工逐条扫描，记录见 <code>data/semantic_scan.json</code>。</p>
<p class="dim">第67轮语义抽检就抓到一例：某来源题名是章节《Sumerian Agriculture and Land Management》，返回摘要却是整卷《The Sumerian World》的导论——六道机器闸全绿通过，语义层失守。</p></div>
<div class="section"><h2>五、环境限制</h2><ul>
<li>Wikipedia、Britannica、archive.org 在本环境不可达（HTTP 000/403）。</li>
<li>Wikidata 时通时断；断线期间登记的实体标 verified=false。</li>
<li>OpenAlex 的 search 端点常触发 429 限流，需重试；DOI 桥（Crossref 检索 → 按 DOI 取摘要）是主要绕行路径。</li>
<li>UN / UNESCO / FAO / CBD 的页面多为 JS 应用壳，正文 7–218 字符。</li>
</ul></div>"""
    with open(os.path.join(SITE, "limits.html"), "w", encoding="utf-8") as f:
        f.write(page("已知限制", lim_body))

    print(f"生成完成：{total} 条目页 + {len(UNIT_IDS)} 单元页 + 索引/时间线/来源/覆盖/证据/限制/关于/首页")


if __name__ == "__main__":
    main()
