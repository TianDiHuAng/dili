# -*- coding: utf-8 -*-
"""第62轮B：SATURATION 采用新缺口定义；evidence.html 显示侧面文献统计。"""
import json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
g=json.load(open(os.path.join(ROOT,"reports","round62_gaps.json"),encoding="utf-8"))
se=json.load(open(os.path.join(DATA,"side_evidence.json"),encoding="utf-8"))
ev=json.load(open(os.path.join(DATA,"evidence_level.json"),encoding="utf-8"))
sp=os.path.join(ROOT,"SATURATION.json");sat=json.load(open(sp,encoding="utf-8"))
sat["zero_gap_rounds"]=0
sat["saturated"]=False
sat["last_round"]=62
sat["all_l2"]=True
sat["gap_model"]={
 "note":"第62轮重定义：不再用模糊的「多维缺口」，改为四类可陈述、可计数的缺口",
 "definitions":g["gap_definitions"],
 "close_condition":"G1=0 且 G2 记为既有结论（不再重试）且 G3=0 后，方可讨论 saturation；G4（语义对题）不可自动化，须以人工扫描记录为准"}
sat["evidence"]={
 "ge2_has_body":g["gap_definitions"][2]["count"] and None,
 "levels":ev["summary"],
 "side_evidence":se["counts"],
 "note":"R19/R20/R21/R22 四道机器校验；侧面文献与剔除记录已结构化"}
# 修正 ge2：从 gaps 里没有直接给，用 243-G3
sat["evidence"]["ge2_has_body"]=243-g["gap_definitions"][2]["count"]
json.dump(sat,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("SATURATION gap_model 已更新")

# evidence.html 增加侧面文献统计段
p=os.path.join(ROOT,"tools","gen_site.py")
t=open(p,encoding="utf-8").read()
if "侧面文献统计" not in t:
    t=t.replace('''<div class="section"><h2>什么叫「强来源」</h2>''',
'''<div class="section"><h2>侧面文献统计</h2><p>「对象同一但只涉一个侧面」的文献共 <b>{se_counts.get('side',0)}</b> 条，已全部降为旁证；被判定对象/时期/学科错配并撤出的共 <b>{se_counts.get('dropped',0)}</b> 条；被引与篇幅均不足、仅供辅助的共 <b>{se_counts.get('weak_claim',0)}</b> 条。结构化记录见 <code>data/side_evidence.json</code>。</p>
<p class="dim">例：拜占庭帝国条目引用医院史、元代条目引用高丽青瓷、印加条目引用玉米酒——这些都「对」但只涉一面，不能作整条的主来源。</p></div>
<div class="section"><h2>什么叫「强来源」</h2>''')
    # 载入 se_counts
    t=t.replace('ev_doc = _evfull','''ev_doc = _evfull
_sep = os.path.join(DATA, "side_evidence.json")
se_counts = (json.load(open(_sep, encoding="utf-8")).get("counts", {}) if os.path.exists(_sep) else {})''')
    open(p,"w",encoding="utf-8").write(t)
    print("evidence.html 已加侧面文献统计")
