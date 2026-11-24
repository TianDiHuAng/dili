# -*- coding: utf-8 -*-
"""第77轮B：把 G3a/G3b 写入 SATURATION 与 limits 页；立 D140 政策。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assess import load_sources, load_entries, content_count, count_entry, level_of, UNITS
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
S=load_sources();T=load_entries(UNITS)
g=json.load(open(os.path.join(ROOT,"reports","round62_gaps.json"),encoding="utf-8"))
sp=json.load(open(os.path.join(ROOT,"reports","round77_g3split.json"),encoding="utf-8"))

# 更新缺口定义：G3 → G3a + G3b
defs=g["gap_definitions"]
new=[]
for d in defs:
    if d["id"]=="G3":
        new.append({"id":"G3a","name":"仅 1 内容源，但有侧面/弱来源可补充","count":sp["G3a"]["count"],
                    "fixed_by":"把侧面文献登记为补充源并限定范围（D140），或补整体研究"})
        new.append({"id":"G3b","name":"仅 1 内容源，且无任何其他来源","count":sp["G3b"]["count"],
                    "fixed_by":"需找到至少一条对位文献（多为该主题文献只研究侧面所致）"})
    else:
        new.append(d)
g["gap_definitions"]=new
json.dump(g,open(os.path.join(ROOT,"reports","round62_gaps.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)

sat=json.load(open(os.path.join(ROOT,"SATURATION.json"),encoding="utf-8"))
sat["last_round"]=77
sat["gap_model"]["definitions"]=new
sat["gap_model"]["note"]=("第62轮重定义、第77轮细分：G3 拆为 G3a（有侧面文献可补充）与 G3b（无任何其他来源）。"
  "两者的处置不同——G3a 可把侧面文献登记为补充源并限定范围，G3b 只能继续找或承认无解。")
json.dump(sat,open(os.path.join(ROOT,"SATURATION.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("缺口定义已拆分:",{d["id"]:d["count"] for d in new})
print("G3b 层级分布:",sp["G3b"]["tiers"])

# limits.html 增加一段（动态）
p=os.path.join(ROOT,"tools","gen_site.py")
t=open(p,encoding="utf-8").read()
if "G3a 与 G3b 的区别" not in t:
    t=t.replace('<p class="dim">关闭条件：G1=0 且 G3=0 后方可讨论「饱和」',
'''<p class="dim"><b>G3a 与 G3b 的区别</b>（第77轮拆分）：G3a 是「已有侧面文献可补充，缺的是整体研究」；G3b 是「连侧面文献都未登记，只有单一内容源」。两者的处置不同——前者可把侧面文献登记为补充源并限定范围（D140），后者只能继续检索或承认无解。当前 G3a 仅 {len([x for x in _gmod if x['id']=='G3a']) and _gmap.get('G3a',{}).get('count',0)} 条、G3b {_gmap.get('G3b',{}).get('count',0)} 条。</p>
<p class="dim">关闭条件：G1=0 且 G3=0 后方可讨论「饱和」''')
    open(p,"w",encoding="utf-8").write(t)
    print("limits 页已加 G3a/G3b 说明")
else:
    print("limits 已有说明")