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
    return f'''<nav class="nav"><a href="{p}index.html">首页</a><a href="{p}index-all.html">全站索引</a><a href="{p}timeline.html">时间线</a><a href="{p}sources.html">来源库</a><a href="{p}coverage.html">覆盖矩阵</a><a href="{p}about.html">关于</a></nav>'''


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
<h1>{esc(e['title'])}</h1><p><span class="tag">{esc(e['tier'])}</span><span class="tag">{esc(e['level'])}</span><span class="tag">{esc(e['region'])}</span><span class="tag">{esc(e['theme'])}</span>{srcgrade(e, covflags.get(e['id'], {}))}</p>
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

    print(f"生成完成：{total} 条目页 + {len(UNIT_IDS)} 单元页 + 索引/时间线/来源/覆盖/关于/首页")


if __name__ == "__main__":
    main()
