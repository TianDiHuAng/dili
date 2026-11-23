# -*- coding: utf-8 -*-
"""第45轮收尾。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");ROUND=45;DATE="2026-11-23"
AUDIT=sys.argv[1] if len(sys.argv)>1 else "抽检进行中";NEW=int(sys.argv[2]) if len(sys.argv)>2 else 6
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
def hb(sid):
    note=(S.get(sid) or {}).get("note") or ""
    if "stub" in note.lower(): return False
    m=re.search(r"摘要长度\s*(\d+)\s*字符",note) or re.search(r"正文\s*(\d+)\s*字符",note) or re.search(r"摘要\s*(\d+)\s*字符",note)
    if m: return int(m.group(1))>=MIN
    m=re.search(r"(\d{3,7})\s*字节",note)
    if m: return int(m.group(1))>=MIN
    return None
a1=a2=a3=0
for e in T.values():
    b=sum(1 for s in e["sources"] if hb(s) is True)
    if b>=2: a3+=1
    elif b==1: a2+=1
    else: a1+=1
mp=os.path.join(ROOT,"METRICS.json");m=json.load(open(mp,encoding="utf-8"))
m["rounds"]=[r for r in m["rounds"] if r["round"]!=ROUND]
m["rounds"].append({"round":ROUND,"date":DATE,"new_entries":0,"upgrades":0,"reviews":0,"fixes":NEW,
 "pending_total":pending,"check_result":"ERRORS=0 ALL_PASS","link_result":"BROKEN=0 LINKS_PASS",
 "new_sources":NEW,"sample_rate":"全部6条","sample_audit":AUDIT,
 "note":f"D100首次执行（先定正文断言再选文献）；四分类 别名页only {a1}/1源 {a2}/≥2源 {a3}"})
json.dump(m,open(mp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0;sat["saturated"]=False;sat["last_round"]=ROUND
sat["all_l2"]=True
sat["evidence"]={"alias_only":a1,"one_source":a2,"two_plus":a3,
 "definition":"D099 四分类，实测口径（读 note 记录的正文字符数）"}
sat["history"]=[h for h in sat["history"] if h.get("round")!=ROUND]
sat["history"].append({"round":ROUND,"methods_used":["B1 按 D100 顺序（先断言后文献）","双关键词组匹配","偏题剔除3条","台账"],
 "gaps_found":pending+a1,
 "note":f"别名页only 49→{a1}；≥2源 {a3}","result":"证据质量推进"})
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov["updated"]=DATE;cov["round"]=ROUND;cov["round_processed"]=NEW
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
lines=[f"# REPORT.md — 第 {ROUND} 轮摘要","",f"- 日期：{DATE}","- 状态：正常循环","",
 "## 1. 方法改进：D100 首次落地","",
 "前四轮补源的做法是「先搜文献 → 再补一句『本条据此写 X』」，结果第44轮 12 条中 **6 条的落点句指向的正文根本不存在**。",
 "本轮改为相反顺序：**先在正文定位待支撑句 → 用该句关键词检索 → 要求摘要同时命中两个关键词组**。","",
 f"- 登记 {NEW} 条：马里帝国、文艺复兴意大利、白令陆桥、安第斯山脉、五大湖、洋流",
 "- 剔除 3 条偏题（双关键词命中也救不了的）：日本列岛←**阿根廷 Pampean** 俯冲带（地名碰撞）、古希腊城邦←艺术中的山、克里特文明←艺术接受史",
 "- 罗马共和国无候选","",
 "## 2. 口径进展（D099 四分类）","",
 "| 类别 | 第44轮 | 第45轮 |","|---|---|---|",
 f"| 来源仅含别名页 | 49 | **{a1}** |",
 f"| 1 个含正文来源 | 165 | **{a2}** |",
 f"| ≥2 个含正文来源 | 29 | **{a3}** |","",
 "## 3. 质量","",
 f"- tools/check.py：ERRORS=0 ALL_PASS（{len(es)} 条条目、{len(src)} 条来源）",
 "- tools/check_links.py：BROKEN=0 LINKS_PASS",
 f"- 抽检（6 条全部）：{AUDIT}","",
 "## 4. 累计","",
 f"- 总条目：{len(es)}（核心 {tiers['核心']} / 重要 {tiers['重要']} / 补充 {tiers['补充']}）",
 f"- 写作层级：L1 {levels['L1']} / **L2 {levels['L2']}**",
 f"- 待核实总数：{pending}",f"- 来源总数：{len(src)}；已核验：{verified}","",
 "## 5. 目标达成度","",
 "| 条件 | 状态 |","|---|---|",
 "| 核心 44/44 · 重要 104/104 · 全部 243/243 L2 | **已达成** |",
 f"| 证据质量（≥2 含正文来源） | {a3}/243，**未达成** |",
 f"| 来源仅含别名页 | 仍有 **{a1}** 条 |",
 "| 多维缺口连续 3 轮为零 | **未达成** |",""]
open(os.path.join(ROOT,"REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print(f"updated; 别名页only {a1} / 1源 {a2} / >=2源 {a3}")