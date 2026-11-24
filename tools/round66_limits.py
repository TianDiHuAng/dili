# -*- coding: utf-8 -*-
"""第66轮A：limits.html 改为动态读取缺口；建立 semantic_scan.json（人工扫描存档）。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
S={s["id"]:s for s in json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]}
g=json.load(open(os.path.join(ROOT,"reports","round62_gaps.json"),encoding="utf-8"))

# ===== 1 人工扫描存档 =====
scan={
 "round":66,"date":TODAY,
 "purpose":"机器校验（R18–R23）只能判断「来源存在/有正文/标题含对象词/非弱来源/非空壳」，无法判断「这篇讲的是对象的侧面还是整体」。本文件存档人工逐条扫描的结论。",
 "scans_done":[
   {"round":49,"scope":"196 条含学术来源条目全量标题扫描","found":["罗马共和国←地质学岩相建模","澳大利亚原住民←板球访英","阿拉伯半岛←单峰驼遗传","马格里布←人群线粒体DNA","汉代←论狗文集","植物物候←软件包","北美冰盖←讨论通信"]},
   {"round":50,"scope":"30 条侧面文献逐条定性","found":"全部标注旁证并说明为何不能作主来源"},
   {"round":57,"scope":"R20 扩至 148 条后全量","found":["元代←美国黑人史书评","河中地区←西地中海沙沉积","河中地区←PPN B 小雕像指纹"]},
   {"round":58,"scope":"R20 扩至 198 条（含补充条目）","found":["极端天气预警←对象词表不全（补映射，非剔除）"]},
   {"round":63,"scope":"9 条政权类第二来源检索","found":["古埃及新王国←文字与社会（不专新王国）","周代/桑海/笈多←无过筛"]},
   {"round":65,"scope":"4 条补充类第二来源检索","found":["3 条为国家个案，已在正文限定"]}
 ],
 "unresolved":{
   "note":"以下 5 条经多轮两库检索确认无合格第二来源；不再重试同类检索（D110）",
   "entries":["古埃及新王国","加纳帝国","桑海帝国","笈多王朝","周代"],
   "reason":"均为古代政权，主题文献多集中于单一侧写（如某遗址、某文本），无「对象+政体/经济」双槽同时命中且被引≥10、摘要≥800 的研究"
 },
 "cannot_automate":["某篇文献是否只涉对象的一个侧面","某条断言是否被该文献真正支持（强度是否相称）","个案能否代表通例（须靠正文限定）"]
}
json.dump(scan,open(os.path.join(DATA,"semantic_scan.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("semantic_scan.json 已建立")

# ===== 2 limits.html 改为动态 =====
p=os.path.join(ROOT,"tools","gen_site.py")
t=open(p,encoding="utf-8").read()
if "lim_body" in t and "G3 仅 1 内容源" not in t:
    start=t.find('    lim_body = """<h1>已知限制</h1>')
    end=t.find('    with open(os.path.join(SITE, "limits.html")', start)
    if start>0 and end>start:
        new_block = '''    _gmod = sat_doc.get("gap_model", {}).get("definitions", [])
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
<p class="dim">关闭条件：G1=0 且 G3=0 后方可讨论「饱和」；G2 记为既有结论，不再重试同类检索；G4 不可自动化。</p></div>
<div class="section"><h2>二、经检索确认「无合格第二来源」的条目（{len(_noans)} 条）</h2>
<p>以下条目经<b>两个库（Crossref + OpenAlex）、多条检索式</b>检索后仍无合格第二来源。本站不作硬配。</p>
<table><thead><tr><th>条目</th><th>状况</th></tr></thead><tbody>{_noans_rows}</tbody></table></div>
<div class="section"><h2>三、空壳页（{len(_shell)} 个）</h2>
<p>以下机构页经 curl 实测，strip 后正文不足 800 字符（多为 JS 应用壳或导航条），<b>仅作入口页，不作正文依据</b>。</p>
<table><thead><tr><th>来源</th><th>页面</th><th>正文字符</th></tr></thead><tbody>{_shell_rows}</tbody></table>
<p class="dim">对比：同期实测 OWID 长文为 3,298–31,443 字符，World Bank 8,041–11,098，NOAA 2,753，IUCN 4,086。若不实测，会把这些空壳误当成「独立互证」。</p></div>
<div class="section"><h2>四、机器校验的能力边界</h2>
<p>R18–R23 能保证：引用年份存在（R18）、弱来源不称主来源（R19）、标题含对象词（R20）、层级有记录（R21）、层级与重算一致（R22）、空壳页不称内容源（R23）。</p>
<p><b>不能判断</b>：① 一篇文献是否只涉对象的某个侧面；② 某条断言是否被该文献真正支持、强度是否相称；③ 个案能否代表通例。这三类依赖人工逐条扫描，记录见 <code>data/semantic_scan.json</code>。</p></div>
<div class="section"><h2>五、环境限制</h2><ul>
<li>Wikipedia、Britannica、archive.org 在本环境不可达（HTTP 000/403）。</li>
<li>Wikidata 时通时断；断线期间登记的实体标 verified=false。</li>
<li>OpenAlex 的 search 端点常触发 429 限流，需重试；DOI 桥（Crossref 检索 → 按 DOI 取摘要）是主要绕行路径。</li>
<li>UN / UNESCO / FAO / CBD 的页面多为 JS 应用壳，正文 7–218 字符。</li>
</ul></div>"""
'''
        t = t[:start] + new_block + t[end:]
        # 载入 sat_doc / scan_doc / by_title / _shellsize
        t=t.replace('se_counts = (json.load(open(_sep, encoding="utf-8")).get("counts", {}) if os.path.exists(_sep) else {})',
'''se_counts = (json.load(open(_sep, encoding="utf-8")).get("counts", {}) if os.path.exists(_sep) else {})
_satp = os.path.join(DATA, "..", "SATURATION.json")
sat_doc = json.load(open(os.path.abspath(_satp), encoding="utf-8")) if os.path.exists(os.path.abspath(_satp)) else {}
_scanp = os.path.join(DATA, "semantic_scan.json")
scan_doc = json.load(open(_scanp, encoding="utf-8")) if os.path.exists(_scanp) else {}


def _shellsize(s):
    m = re.search(r"空壳页判定】strip 后仅 (\\d+) 字符", s.get("note") or "")
    return (m.group(1) + " 字符") if m else "—"''')
        open(p,"w",encoding="utf-8").write(t)
        print("limits.html 已改为动态生成")
    else:
        print("未找到 lim_body 块")
else:
    print("跳过（已动态或未找到）")