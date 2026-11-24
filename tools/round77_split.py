# -*- coding: utf-8 -*-
"""第77轮：G3 拆分为 G3a（有侧面/弱辅助源）与 G3b（只有单一内容源，无任何辅助）。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, count_entry, level_of, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
S=load_sources();T=load_entries(UNITS)

g3a=[];g3b=[]
for t,e in T.items():
    if content_count(e,S)!=1: continue
    c=count_entry(e,S)
    # 是否有侧面/弱来源可用作补充（side 或 weak 计数>0）
    if c["side"]>0 or c["weak"]>0:
        g3a.append({"entry":t,"tier":e["tier"],"counts":c})
    else:
        g3b.append({"entry":t,"tier":e["tier"],"counts":c})

def tier_count(lst):
    from collections import Counter
    return dict(Counter(x["tier"] for x in lst))

out={"round":77,"date":TODAY,
 "definitions":{
   "G3a":"内容源仅 1 个，但**有侧面文献或弱来源可作补充**（已降旁证，正文已限定范围）——缺的是「整体研究」",
   "G3b":"内容源仅 1 个，**且无任何其他来源可补充**——缺的是「任何第二来源」"},
 "G3a":{"count":len(g3a),"tiers":tier_count(g3a),"entries":[x["entry"] for x in g3a]},
 "G3b":{"count":len(g3b),"tiers":tier_count(g3b),"entries":[x["entry"] for x in g3b]},
 "note":"这是第77轮的结构性改进：把「找过但只有侧面」与「什么都没找到」分开，两者性质不同、处置也不同。"}
json.dump(out,open(os.path.join(ROOT,"reports","round77_g3split.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("G3a（有侧面/弱辅助）:",len(g3a),tier_count(g3a))
print("G3b（无任何辅助）:",len(g3b),tier_count(g3b))
print("\nG3b 明细（这些最难）:")
for x in g3b[:20]: print(f"  [{x['tier']}] {x['entry']}  {x['counts']}")