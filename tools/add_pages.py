# -*- coding: utf-8 -*-
"""第61轮B：gen_site 插入 evidence.html 与 limits.html。"""
import os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p=os.path.join(ROOT,"tools","gen_site.py")
t=open(p,encoding="utf-8").read()
if "limits.html" in t:
    print("已存在"); raise SystemExit
anchor = '    print(f"生成完成：{total} 条目页'
insert = '''    # ---- 第61轮：证据层级说明 ----
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
<div class="section"><h2>四档定义</h2><table><thead><tr><th>层级</th><th>判据</th><th>条数</th></tr></thead><tbody>
<tr><td><b>A</b></td><td>≥2 个<b>强来源</b></td><td>{evs.get('A',0)}</td></tr>
<tr><td><b>B</b></td><td>1 个强来源 + 旁证/弱来源</td><td>{evs.get('B',0)}</td></tr>
<tr><td><b>C</b></td><td>无强来源（仅旁证或弱来源）</td><td>{evs.get('C',0)}</td></tr>
<tr><td><b>D</b></td><td>仅数据端点与机构页（指标解读类）</td><td>{evs.get('D',0)}</td></tr>
</tbody></table></div>
<div class="section"><h2>什么叫「强来源」</h2><p>满足以下<b>任一</b>条件即为强来源：被引 ≥ 10；或正文/摘要 ≥ 800 字符。</p>
<p class="dim">初版曾要求两者同时满足，把被引 458、摘要 795 字符的经典著作误判为弱来源，故改为「满足其一」（D117）。数据端点（世界银行、NOAA、USGS 等 JSON）一律不计为内容来源，只支撑数值（D107）。</p></div>
<div class="section"><h2>旁证与弱来源</h2><p>以下情况会被降为<b>旁证</b>：来源与条目<b>对象同一但只涉其中一个侧面</b>（如「拜占庭帝国」条目引用医院史）；或来源标题<b>不含条目对象词</b>（R20）；或被引与篇幅均不足（R19）。降级理由写在条目页的「待核实」区。</p></div>
<div class="section"><h2>C / D 级清单（共 {len(cd)} 条）</h2>
<table><thead><tr><th>条目</th><th>层级</th><th>强</th><th>弱</th><th>旁证</th><th>数据</th></tr></thead><tbody>{''.join(_evrow(k) for k in cd_sorted)}</tbody></table></div>"""
    with open(os.path.join(SITE, "evidence.html"), "w", encoding="utf-8") as f:
        f.write(page("证据层级说明", ev_body))

    # ---- 第61轮：已知限制 ----
    lim_body = """<h1>已知限制</h1><p class="lead">本页如实列出当前无法解决、或经多轮检索确认无解的问题，不作掩饰。</p>
<div class="section"><h2>一、经检索确认「无合格主来源」的条目</h2>
<p>以下条目经<b>两个库（Crossref + OpenAlex）、多条检索式</b>检索后仍无合格主来源，原因多为对象稀有、主题属概念性、或现有文献只涉侧面。本站不作硬配。</p>
<table><thead><tr><th>条目</th><th>现状</th><th>已试过的检索</th></tr></thead><tbody>
<tr><td>河中地区（绿洲灌溉与商路）</td><td>仅有侧面向来源（粟特宗教文献、多学科泛论）</td><td>Samarkand/Bukhara oasis trade；Sogdian trade network；Transoxiana</td></tr>
<tr><td>库什与努比亚（商路与商品结构）</td><td>商路部分无来源；政体与冶铁已有来源</td><td>Meroe trade network commodities；Kushite Red Sea trade</td></tr>
<tr><td>莫切文化（灌溉与河谷政治）</td><td>仅有手工业专门化的都城个案</td><td>Moche irrigation canals；Moche political organization</td></tr>
</tbody></table></div>
<div class="section"><h2>二、语义对题只能人工判断</h2>
<p>机器校验能保证「来源存在、有正文、标题含对象词、非弱来源」（R18–R22），但<b>不能判断一篇只讲「该对象某个侧面」的文献能否支撑整条断言</b>。这类判断依赖人工逐条扫描；本站已把降级理由写在条目页。</p></div>
<div class="section"><h2>三、环境限制</h2><ul>
<li>Wikipedia、Britannica、archive.org 在本环境不可达（HTTP 000/403），相关条目改用机构页与学术库。</li>
<li>Wikidata 时通时断；断线期间登记的实体标为 verified=false，并在条目页标「待核」。</li>
<li>OpenAlex 的 search 端点常触发 429 限流，检索脚本需重试；DOI 桥（Crossref 检索 → 按 DOI 向 OpenAlex 取摘要）是主要绕行路径。</li>
</ul></div>
<div class="section"><h2>四、未达成项</h2>
<table><thead><tr><th>条件</th><th>状态</th></tr></thead><tbody>
<tr><td>核心/重要/全部条目达到 L2</td><td><b>已达成</b>（243/243）</td></tr>
<tr><td>每条至少 1 个内容来源</td><td><b>已达成</b>（243/243）</td></tr>
<tr><td>证据层级 C 级清零</td><td><b>已达成</b>（C=0）</td></tr>
<tr><td>每条均有主来源</td><td>未达成（见上表三处 + D 级指标解读条目）</td></tr>
<tr><td>多维缺口连续 3 轮为零</td><td>未达成，<code>saturated=false</code></td></tr>
</tbody></table></div>"""
    with open(os.path.join(SITE, "limits.html"), "w", encoding="utf-8") as f:
        f.write(page("已知限制", lim_body))

'''
t=t.replace(anchor, insert + anchor)
# 载入 ev_doc
if "ev_doc =" not in t:
    t=t.replace('EV = (json.load(open(_evp, encoding="utf-8"))["levels"] if os.path.exists(_evp) else {})',
'''_evfull = json.load(open(_evp, encoding="utf-8")) if os.path.exists(_evp) else {"levels": {}, "summary": {}}
EV = _evfull["levels"]
ev_doc = _evfull''')
open(p,"w",encoding="utf-8").write(t)
print("gen_site 已插入 evidence/limits")