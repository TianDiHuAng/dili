# -*- coding: utf-8 -*-
"""第27轮返工二：别名页命中不计达标。"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
ALIAS={"britannica-regions","wikipedia-regions","un-m49","ap-human-geo"}
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
REPL=("D055 判定：形式达标但**不作升级依据**——本次命中来自数据层别名页"
      "（UNSD M49 国码表 / UNSDG 门户），非本条专题正文。")
changed=[]
for t,e in T.items():
    pn=e.get("pending_notes") or ""
    if "第27轮实证复核" not in pn or "D055 判定：达标" not in pn: continue
    srcs=set(e["sources"][:2])
    if srcs and not (srcs-ALIAS):
        i=pn.find("D055 判定：达标"); j=pn.find("。",i)
        if j>i:
            e["pending_notes"]=pn[:i]+REPL+pn[j+1:]
            e["last_update"]=TODAY; changed.append(t)
for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
trueok=[t for t,e in T.items() if "第27轮实证复核" in (e.get("pending_notes") or "") and "D055 判定：达标" in (e.get("pending_notes") or "")]
print("降为形式达标:",len(changed))
print("真达标:",len(trueok),trueok)