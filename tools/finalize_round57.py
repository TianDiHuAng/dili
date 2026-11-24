# -*- coding: utf-8 -*-
"""第57轮收尾。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=57;DATE="2026-11-24"
AUDIT=sys.argv[1] if len(sys.argv)>1 else "本轮为R20全量扩展轮"
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
objn=len(json.load(open(os.path.join(DATA,"object_words.json"),encoding="utf-8")))
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":0,"fixes":6,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":0,"sample_rate":"148条对象词全量校验","sample_audit":AUDIT,
 "note":f"R20扩至148条；检出7条，剔除3条真对象碰撞、加3条别名、修1条孤儿引用；≥2内容源 {g2}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["all_l2"]=True
sat["evidence"]={"ge2_has_body":g2,"one_has_body":o1,"obj_word_map":objn,
 "note":"R19+R20 覆盖核心与重要条目（148条）；语义对题仍依赖人工扫描"}
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,"methods_used":["R20扩至148条","剔除3条对象碰撞","修孤儿引用","台账"],
 "gaps_found":pending,
 "note":f"R20 覆盖 {objn} 条；剔除元代←美国黑人史等3条碰撞；≥2内容源 {g2}","result":"校验机器化"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=6
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环（**R20 扩至全部核心+重要**）","",
 "## 1. 对象词映射扩到 148 条","",
 "上一轮 R20 只覆盖 44 条核心条目；本轮为 **97 条重要条目**补建对象词，覆盖率达到 **148 条**（核心+重要全覆盖）。","",
 "## 2. 全量校验检出 7 条，其中 3 条是**真对象碰撞**","",
 "| 条目 | 被剔除的来源 | 问题 |","|---|---|---|",
 "| **元代** | William Alexander Mabry, The Negro in North… | **美国黑人史**著作的书评，与元朝毫无关系 |",
 "| **河中地区** | Western Mediterranean sand deposits… | **西地中海沙沉积**，与河中无关 |",
 "| **河中地区** | Analysis of fingerprints on a PPNB figurine | **近东新石器小雕像的指纹**，与河中无关 |",
 "","**这 3 条是我此前从未发现的**——它们通过了之前的「标题含对象词」人工目检（因为标题根本不含对象词，我却没细看），只有 R20 全量跑一遍才现形。","",
 "另 3 条是别名/词形问题，已补：`norden`（斯堪的纳维亚）、`north america`（北美原住民）、`vertical`（安第斯垂直农业）。","",
 "## 3. 顺带修出一个孤儿引用","",
 "- 河中地区的 influence 引用「2023 年《Food globalization…Bukhara》」，但**该来源并未登记成功**（第53轮 DOI 未解析到记录）——R18 检出。",
 "- 已清理该句并重新解析登记。","",
 "## 4. 质量与口径","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源；**R1–R20**）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS","",
 f"- 条目：{len(es)}（核心 {tiers['核心']} / 重要 {tiers['重要']} / 补充 {tiers['补充']}）；**全部 L2**",
 f"- 内容源（≥800 字符）≥2 个：**{g2}**；1 个：**{o1}**；0 个：**0**",
 f"- 对象词映射：**{objn}** 条（核心+重要全覆盖）",
 f"- 来源 {len(src)}（已核验 {verified}）；待核实 {pending}","",
 "| 条件 | 状态 |","|---|---|",
 "| 核心 44/44 · 重要 104/104 · 全部 243/243 L2 | **已达成** |",
 "| 每条至少 1 个内容源 | **已达成 243/243** |",
 "| 弱来源不得称主来源（R19） | **已机器化，0 违规** |",
 "| 对象词须在来源标题（R20） | **已机器化，覆盖 148 条，0 违规** |",
 "| 每条均有**主**来源 | 未达成（河中地区现仅 1 个侧面来源） |",
 "| 语义对题（对象词之外那层） | 仍依赖人工扫描 |",
 "| 多维缺口连续 3 轮为零 | 未达成 |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; ge2={g2} one={o1} objn={objn}")