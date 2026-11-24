# -*- coding: utf-8 -*-
"""第46轮：4 条地形常识类如实标注（无对应专题文献），并做最终口径统计。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
sd=json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"));S={s["id"]:s for s in sd["sources"]}

TERRAIN={
"古希腊城邦":"希腊本土的地形（多山、平原狭小、海岸曲折、岛屿众多）",
"罗马共和国":"台伯河畔拉丁姆平原的农业与交通条件",
"克里特文明":"克里特岛的山地与海岸交错格局",
}
for t,what in TERRAIN.items():
    e=T.get(t)
    if not e: continue
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第46轮来源性质】本条 geo 段的「{what}」属**教科书级的常识性地理描述**：以三槽位（对象+地形+过程）核对多轮检索，"
      f"学术文献中相关表述多为背景句而非论文主题，**无对应专题文献可引**。故不为该句强行配文献（强行配即会重演第45轮「关键词命中但语义不符」的失败），"
      f"该句如实标为常识性描述。").strip()
    e["last_update"]=TODAY
# 五大湖同样标注（其水文特征已改引 NOAA/EPA 机构页）
gl=T.get("五大湖")
if gl:
    gl["pending_notes"]=((gl.get("pending_notes") or "")+
      " 【第46轮来源性质】「五个相连的大型淡水湖」为常识性事实；水文特征已改引 NOAA GLERL / EPA 机构页作背景，"
      "该两组页面无对应字符数记录，按实测口径不计入「含正文来源」，但其为可核验的机构专题页。").strip()

save_docs(docs)
json.dump(sd,open(os.path.join(DATA,"sources.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=46
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)

# ===== 三类口径统计 =====
MIN=800
def hb(sid):
    note=(S.get(sid) or {}).get("note") or ""
    if "stub" in note.lower(): return False
    m=re.search(r"摘要长度\s*(\d+)\s*字符",note) or re.search(r"正文\s*(\d+)\s*字符",note) or re.search(r"摘要\s*(\d+)\s*字符",note)
    if m: return int(m.group(1))>=MIN
    m=re.search(r"(\d{3,7})\s*字节",note)
    if m: return int(m.group(1))>=MIN
    return None
cat={"ge2":0,"one":0,"indicator":0,"terrain_common":0,"alias_other":0}
for t,e in T.items():
    b=sum(1 for s in e["sources"] if hb(s) is True)
    pn=e.get("pending_notes") or ""
    if b>=2: cat["ge2"]+=1
    elif b==1: cat["one"]+=1
    elif "【第46轮来源性质】本条为**指标解读类**" in pn: cat["indicator"]+=1
    elif "【第46轮来源性质】" in pn and "常识性地理描述" in pn: cat["terrain_common"]+=1
    else: cat["alias_other"]+=1
print("五分类：",cat)
json.dump({"round":46,"date":TODAY,"categories":cat,
 "note":"补充分类：指标解读类与地形常识类不构成「缺学术来源」，其正文无需文献支撑；剩余 alias_other 才是真缺口"},
 open(os.path.join(ROOT,"reports","round46_categories.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)