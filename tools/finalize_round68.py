# -*- coding: utf-8 -*-
"""第68轮收尾。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=68;DATE="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
S={s["id"]:s for s in json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));src=json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]
S={s["id"]:s for s in src}
ev=json.load(open(os.path.join(DATA,"evidence_level.json"),encoding="utf-8"))
se=json.load(open(os.path.join(DATA,"side_evidence.json"),encoding="utf-8"))
g=json.load(open(os.path.join(ROOT,"reports","round62_gaps.json"),encoding="utf-8"))
es=cov["entries"]
pending=sum(1 for e in es if e["pending_count"]>0);verified=sum(1 for s in src if s.get("verified"))
MIN=800
def is_data(sid): return sid.startswith(("wb-","usgs-eq","noaa-current","ats-parties","wikidata-"))
def hb(sid,e):
    """D138：与层级判定统一——被引≥10 或 正文/摘要≥800，满足其一即算有正文的内容源。
    别名页/数据端点不计（D107/D135）。"""
    if is_data(sid): return False
    if sid in ALIAS_EXCL: return False
    s = S.get(sid) or {}
    note = s.get("note") or ""
    pn = e.get("pending_notes") or ""
    for n in (note, pn):
        mc = re.search(r"被引\s*(\d+)", n)
        if mc and int(mc.group(1)) >= 10:
            return True
        for pat in (r"摘要长度\s*(\d+)\s*字符", r"正文节录\s*\*{0,2}([\d,]+)\s*字符",
                    r"正文\s*\*{0,2}([\d,]+)\s*字符", r"摘要\s*(\d+)\s*字符"):
            m = re.search(pat, n)
            if m and int(m.group(1).replace(",", "")) >= 800:
                return True
        m = re.search(r"(\d{3,7})\s*字节", n)
        if m and int(m.group(1)) >= 3000:      # 字节→字符约 3:1，3000 字节≈1000 字符
            return True
    return False


g2=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)>=2)
o1=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)==1)
evs=ev["summary"];gd={d["id"]:d["count"] for d in g["gap_definitions"]}
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":15,"fixes":14,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":0,"sample_rate":"15条语义全查（17个来源）","sample_audit":"2 PASS / 8 SOFT / 5 FAIL",
 "note":f"语义抽检5FAIL已剔6源、8SOFT改措辞；R25上线(书评拦截)；别名页不计强来源→A 213→{evs['A']}、G1 0→{gd['G1']}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["last_round"]=ROUND
sat["gap_model"]["definitions"]=g["gap_definitions"]
sat["evidence"]["levels"]=evs
sat["evidence"]["note"]="第68轮修正：别名页/索引页不计强来源后，A 由虚高 213 降至真实 119，G1 由 0 升至 10"
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=14
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**层级虚高被戳破**）","",
 "## 1. 语义抽检 15 条：2 PASS / 8 SOFT / 5 FAIL","",
 "| 判定 | 条目 |","|---|---|",
 "| **PASS** | 古埃及早王朝、波利尼西亚 |",
 "| **SOFT** | 撒哈拉沙漠、东非大裂谷、两河流域、青藏高原、爱琴海世界、罗马帝国、埃塞俄比亚高原、落基山脉 |",
 "| **FAIL** | 大平原、玛雅文明、印加帝国、克里特文明、十字军东征 |","",
 "## 2. 五条 FAIL 的具体原因","",
 "| 条目 | 问题 |","|---|---|",
 "| **玛雅文明** | 所引是 **Choice Reviews Online 的书评**（type=book-review，违反 D082），且讲**形成期兴起**而非古典期衰落 |",
 "| **大平原** | 加拿大冰碛大平原 **96 样地植被分类**（1961）——只涉植被，空间也不及美国主体 |",
 "| **印加帝国** | **玉米酒器物分布**研究；第50轮已判旁证，但第42轮 strong 标签未撤，自相矛盾 |",
 "| **克里特文明** | **印章学**专著（摘要 725 字符 <800）；与第45轮剔除的艺术接受史同判据 |",
 "| **十字军东征** | 纪念文集**导言**（793 字符）+ 布道史（**1305–1352**，落在 11–13 世纪时段外） |","",
 "已剔 6 个来源、8 条改措辞。","",
 "## 3. 本轮最大的发现：我的层级系统有一半是虚的","",
 "剔除错源后我核对层级，发现玛雅、大平原、印加、克里特竟都判 **A 级（3 个 strong）**——而它们的 sources 是：",
 "`britannica-regions`、`wikipedia-regions`、`un-m49`、`ap-human-geo`。",
 "**这四类是别名页/索引页，只证明「该对象存在」，不含主题正文。** 它们被层级系统当成了强来源。","",
 "修正后（D135）：",
 "| 指标 | 修正前（虚） | 修正后（实） |","|---|---|---|",
 f"| A 级 | 213 | **{evs['A']}** |",
 f"| B 级 | 30 | **{evs['B']}** |",
 f"| C 级 | 0 | **{evs['C']}** |",
 f"| D 级 | 0 | **{evs['D']}** |",
 f"| **G1（无强来源）** | **0** | **{gd['G1']}** |","",
 "G1 的 10 条：孔雀王朝、隋唐、克里特文明、维京时代、十字军东征、大平原、玛雅文明、印加帝国、澳大利亚大陆、澳大利亚原住民。","",
 "## 4. R25 上线","",
 "书评（type=book-review）不得作为内容来源——第43轮立 D082 时只靠人工，本轮做成机器校验，立刻抓出 **4 条**（玛雅、孔雀王朝、隋唐、法兰克王国）。`check.py` 现为 **R1–R25**。","",
 "## 5. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；**R1–R25**）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 内容源 ≥2：{g2}；1 个：{o1}",
 f"- 层级：A {evs['A']} / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 侧面文献：side {se['counts']['side']} / dropped {se['counts']['dropped']} / weak {se['counts']['weak_claim']}","",
 "| 编号 | 缺口 | 条数 |","|---|---|---|",
 f"| **G1** | **无强来源** | **{gd['G1']}**（上轮虚报 0） |",
 f"| G2 | 检索确认无解 | {gd['G2']} |",
 f"| G3 | 仅 1 内容源 | {gd['G3']} |",
 "| G4 | 语义对题未机器校验 | 243（已扫描 30 条） |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; A={evs['A']} B={evs['B']} C={evs['C']} D={evs['D']} G1={gd['G1']}")