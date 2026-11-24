# -*- coding: utf-8 -*-
"""第67轮收尾。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=67;DATE="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
S={s["id"]:s for s in json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));src=json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]
S={s["id"]:s for s in src}
ev=json.load(open(os.path.join(DATA,"evidence_level.json"),encoding="utf-8"))
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
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":15,"fixes":11,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":0,"sample_rate":"15条语义全查（21个来源摘要逐句对读）","sample_audit":"4 PASS / 10 SOFT / 1 FAIL",
 "note":"R24上线（悬空落点检测）；落实11条语义修改；站点加层级悬停与「如何读懂」"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["last_round"]=ROUND
sat["gap_model"]["definitions"]=g["gap_definitions"]
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=11
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**语义抽检**）","",
 "## 1. 15 条语义抽检：4 PASS / 10 SOFT / 1 FAIL","",
 "派 subagent 拉取 15 条核心/重要条目涉及的全部 **21 个来源**的摘要，逐句与正文断言对读。","",
 "| 判定 | 条数 | 条目 |","|---|---|---|",
 "| **PASS** | **4** | 澳大利亚大陆、南极条约体系、威尼斯、古埃及古王国 |",
 "| **SOFT** | **10** | 苏美尔城邦、黄河流域、蒂亚瓦纳科、澳大利亚内陆干旱气候、马丘比丘、维京时代、安纳托利亚、莫斯科公国、马格里布、中南半岛 |",
 "| **FAIL** | **1** | 丝绸之路 |","",
 "## 2. 最典型的四类问题","",
 "**① 因果反转**（蒂亚瓦纳科）——摘要讨论「已存在的国家**内部**的生产组织」，我写成「技术—组织是国家**形成**的条件」。",
 "**② 区域/主题错位**（澳大利亚内陆干旱气候）——所引研究是**东南澳森林火险**，我拿它撑「内陆干旱」的通例；该文通篇限定 southeast Australia。",
 "**③ 摘要里根本没有的东西**（维京时代、马丘比丘）——「劫掠」「拜占庭」「山地适应能力」在摘要中零命中，却被并进「据此」句。",
 "**④ 个案升格**（丝绸之路·FAIL）——拉达克**单点商埠的民族史个案**（且断代在 20 世纪边界划定），被记为整条网络的「第二独立来源」。",
 "**⑤ 术语溢出**（中南半岛）——摘要测的是流域**化学风化强度**，我外推为「**景观**一致」。",
 "**⑥ 一处硬错**（安纳托利亚）——「中全新世」应为「**早全新世**」（约前 9 千纪中叶 ≈ 8500 cal BC）。","",
 "## 3. 三个系统性缺陷","",
 "| 缺陷 | 说明 | 机器可否检出 |","|---|---|---|",
 "| **题目级错位** | `sources.title` 是章节名，OpenAlex 返回的却是**整卷导论**摘要 | R18–R23 全过，**查不出** |",
 "| **悬空落点** | 「本条『X』据此」的 X 在正文字段中不存在 | **本轮 R24 已实现**（当前数据该句式已极少） |",
 "| **模板化登记** | 第42轮把「可作年代/机制断言的第二来源」套用到摘要缺机制/缺年代的文献上 | **查不出**，须改登记习惯 |","",
 "## 4. 处置","",
 "- 11 条全部落实修改（1 FAIL 降级 + 10 SOFT 改措辞），`check.py` 0 错误；",
 "- 结论追加至 `data/semantic_scan.json`；",
 "- **R24 上线**：落点声明中引号括起的短语须在正文出现（D131）。","",
 "## 5. 站点可用性","",
 "- 条目页「证据 A/B/C/D」标签加**悬停说明**（215 页）；",
 "- `/evidence.html` 新增「如何读懂本页」：解释四档含义、强来源门槛、降级常见原因。","",
 "## 6. 口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条、{len(src)} 来源；**R1–R24**）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 内容源 ≥2：{g2}；1 个：{o1}；层级 A {evs['A']} / B {evs['B']} / C {evs['C']} / D {evs['D']}",
 f"- 缺口：G1={gd['G1']} / G2={gd['G2']} / G3={gd['G3']} / G4=243（本轮新增 15 条人工扫描记录）","",
 "| 条件 | 状态 |","|---|---|",
 "| 核心/重要/全部 243 条 L2 | **已达成** |",
 "| 每个条目都有强来源（G1=0） | **已达成** |",
 "| 证据层级 C/D 清零 | **已达成** |",
 "| R19–R24 六道机器校验 | 已上线，0 违规 |",
 "| 限制与能力边界对读者公开 | 已达成 |",
 "| G4 语义对题 | **15/243 已人工扫描**（本轮），结论存档 |",
 "| 多维缺口连续 3 轮为零 | 未达成 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; ge2={g2} one={o1} levels={evs}")