# -*- coding: utf-8 -*-
"""第92轮B：修 2 处具体虚高（尼罗河三角洲重金属、古埃及中王国诗歌）。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

e=T["尼罗河三角洲"]
if "openalex-W2220441068" in e["sources"]:
    e["pending_notes"]=((e.get("pending_notes") or "")+
      " 【第92轮审计修正·对象碰撞】`openalex-W2220441068`（《Heavy metal concentrations in surface river water and "
      "channel sediments…》, 被引达标）研究的是**河水泥沙中的重金属污染**，属现代环境监测，"
      "不支撑本条的三角洲沉积与河道演变叙述。**现降为旁证**。").strip()
    e["last_update"]=TODAY; print("尼罗河三角洲：重金属已降旁证")

e=T["古埃及中王国"]
if "openalex-W4322713864" in e["sources"]:
    e["pending_notes"]=((e.get("pending_notes") or "")+
      " 【第92轮审计修正·侧面】`openalex-W4322713864`（《**Poetry and Culture** in Middle Kingdom Egypt》"
      "《中王国埃及的诗歌与文化》）研究的是**文学**，属文化史侧面，不支撑本条的中央行政叙述。"
      "**现降为旁证**；本条的行政部分由《Setting a State Anew》（中央行政）支撑。").strip()
    e["last_update"]=TODAY; print("古埃及中王国：诗歌已降旁证")

save_docs(docs); update_coverage(docs)
print("完成")