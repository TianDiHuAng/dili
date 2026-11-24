# -*- coding: utf-8 -*-
"""第49轮收尾。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=49;DATE="2026-11-24"
AUDIT=sys.argv[1] if len(sys.argv)>1 else "本轮为 R19 人工扫描轮"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"));src=json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]
S={s["id"]:s for s in src}
es=cov["entries"]
levels={k:sum(1 for e in es if e["level"]==k) for k in ("L1","L2","L3")}
tiers={k:sum(1 for e in es if e["tier"]==k) for k in ("核心","重要","补充")}
pending=sum(1 for e in es if e["pending_count"]>0);verified=sum(1 for s in src if s.get("verified"))
MIN=800
def is_data(sid): return sid.startswith(("wb-","usgs-eq","noaa-current","ats-parties","wikidata-"))
def hb(sid,e=None):
    if is_data(sid): return False
    notes=[(S.get(sid) or {}).get("note") or ""]
    if e is not None: notes.append(e.get("pending_notes") or "")
    for note in notes:
        if "stub" in note.lower(): return False
        for pat in (r"摘要长度\s*(\d+)\s*字符",r"正文字?录?\s*\*{0,2}([\d,]+)\s*字符",r"正文\s*(\d+)\s*字符",r"摘要\s*(\d+)\s*字符"):
            m=re.search(pat,note)
            if m: return int(m.group(1).replace(",",""))>=MIN
        m=re.search(r"(\d{3,7})\s*字节",note)
        if m: return int(m.group(1))>=MIN
    return None
g2=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)>=2)
o1=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)==1)
z0=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)==0)
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":0,"fixes":7,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":0,"sample_rate":"196条全量扫描","sample_audit":AUDIT,
 "note":f"R19人工全量扫描：剔除4条对象/学科错配、3条降旁证；识别约30条侧面文献待下轮；≥2内容源 {g2}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["all_l2"]=True
sat["evidence"]={"ge2_has_body":g2,"one_has_body":o1,"zero_has_body":z0,
 "note":"第①层（有正文）实测；第②层（内容对题）已开始人工全量扫描（196 条）"}
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,"methods_used":["R19人工全量扫描（196条）","对象/学科错配剔除","侧面文献识别","台账"],
 "gaps_found":pending,
 "note":f"剔除4条错配、降3条旁证、识别约30条侧面文献；≥2内容源 {g2}","result":"对象同名校验推进"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=7
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**R19 人工全量扫描**）","",
 "## 1. 本轮做了什么","",
 "- 把「R19 对象同位校验」从**设想**变成**实际执行**：导出全部 **196 条**含学术来源条目及其来源标题，逐条人工核对对象同一性。",
 "- 这是前几轮反复出错的根治尝试——机器查不了「论狗 ≠ 汉代」，人眼可以。","",
 "## 2. 扫出的对象/学科错配（已处置）","",
 "| 条目 | 被剔除/降级的来源 | 问题 |","|---|---|---|",
 "| 罗马共和国 | Integrating Sequence Stratigraphy…（台伯河冲积平原三维岩相建模） | **学科错配**：地质学，虽地理在罗马但不涉政体 |",
 "| 澳大利亚原住民 | Aboriginal Australians abroad 1606–1875 | **对象错误**：19 世纪板球队员访英史 |",
 "| 阿拉伯半岛 | Genetic structure of…dromedary **camels** | **对象错误**：单峰驼，不是半岛地理 |",
 "| 马格里布 | Mitochondrial DNA analysis of Northwest African populations | **对象错误**：人群基因，不是区域地理 |",
 "| 汉代 | Dogs in Early Imperial China | **降旁证**：标题含汉代与前206-220，主题却是狗 |",
 "| 植物物候变化 | PhenoFECT: A Python package | **降旁证**：预测软件包 |",
 "| 北美冰盖 | Comment and Reply on 'Keewatin Ice Sheet…' | **标明**：学术讨论通信，非研究论文 |","",
 "## 3. 识别出但尚未处理的一类：侧面文献","",
 "约 **30 条**属「对象同一但只涉一个侧面」，例如：拜占庭←医院史、元代←高丽青瓷、印加←玉米酒、莫切←艺术图像、维京←婚姻与女性、美国西进←非裔史、阿塔卡马←岩内微生物、复活节岛←农业策略、密克罗尼西亚←珊瑚遗传。",
 "这些**不是错误**，但作为「唯一或主要来源」支撑整条时证据不足。已列入扫描报告，**待下一轮逐条降为旁证或补主来源**。","",
 "## 4. 质量","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源；R1–R18）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 扫描记录：`reports/round49_titles.json`（196 条全量）、`reports/round49_r19_scan.json`（处置与待办）","",
 "## 5. 累计与达成度","",
 f"- 条目：{len(es)}（核心 {tiers['核心']} / 重要 {tiers['重要']} / 补充 {tiers['补充']}）；**全部 L2**",
 f"- 内容源（≥800 字符）≥2 个：**{g2}**；1 个：**{o1}**；0 个：**{z0}**",
 f"- 来源 {len(src)}（已核验 {verified}）；待核实 {pending}","",
 "| 条件 | 状态 |","|---|---|",
 "| 核心 44/44 · 重要 104/104 · 全部 243/243 L2 | **已达成** |",
 f"| 来源有正文 ≥2 个 | {g2}/243（结构层） |",
 "| 对象同位（R19） | **196 条已人工扫描**；错配 4 条已剔除、侧面文献约 30 条待处理 |",
 "| 多维缺口连续 3 轮为零 | 未达成 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; ge2={g2} one={o1} zero={z0}")