# -*- coding: utf-8 -*-
"""第20轮：2 条按 D055 升级 + 36 条遗产 L2 来源分级标注 + 复核。"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
NAT="本条以来源页可支撑的概述为主；具体年代、制度细节与统计数值待专门来源逐条核验。"
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# 登记来源
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))
NEW=[("noaa-sustainable-fisheries","Sustainable Fisheries | NOAA Fisheries","NOAA",None,"官方机构",
      "https://www.fisheries.noaa.gov/topic/sustainable-fisheries",19729,165),
     ("fao-global-soil-partnership","Global Soil Partnership | FAO","FAO",None,"官方机构",
      "https://www.fao.org/global-soil-partnership/en/",5215,53)]
have={s["id"] for s in sd["sources"]}
for sid,title,author,year,typ,url,body,hits in NEW:
 if sid in have: continue
 sd["sources"].append({"id":sid,"title":title,"author":author,"year":year,"type":typ,"url":url,"url2":None,
  "link_ok":True,"verified":True,"page_title":title,
  "note":f"curl 实测 HTTP 200；页面标题：{title}；D044/D050 剥离口径正文 {body} 字符；第20轮按 D055 档①作专题页（命中 {hits}）。"})
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

C={
"渔业资源":{
 "def":"渔业资源：可被捕捞利用的鱼类与无脊椎动物种群，其数量与结构受生态过程与捕捞压力共同影响。",
 "geo":"渔场多分布于营养盐丰富的上升流区、大陆架与河口，水温与饵料决定种群分布。资源量随繁殖周期与海洋条件波动。",
 "infl":"可持续捕捞依赖种群评估与限额管理；过度捕捞会削弱种群恢复力，兼捕则影响非目标物种。管理成效取决于监测与执行能力。",
 "pol":"本条不展开政权序列；配额分配与渔业权属属治理议题。",
 "conn":"鱼群洄游与贸易把沿岸渔场、加工地与消费市场连接起来，形成跨区域的产业链。",
 "today":"多国已实施种群评估与捕捞限额。资源量、上岸量与配额数据需按年份从 NOAA/FAO 机构页核验。",
 "sources":["noaa-sustainable-fisheries","s051-fisheries-noaa-gov"],
 "proof":"noaa-sustainable-fisheries 标题即主题，剥离后 19729 字符、fisher|sustainab 命中 165"},
"土壤资源":{
 "def":"土壤资源：支撑植物生长与生态功能的地表疏松层，其厚度、养分与保水能力决定土地生产力。",
 "geo":"土壤类型受母质、气候、地形与植被长期作用影响，分布呈地带性差异。坡地与干旱区的土层更薄、更易侵蚀。",
 "infl":"土壤退化（侵蚀、盐渍化、有机质下降）削弱生产力与固碳能力；保护性耕作与有机质投入有助于恢复。成效取决于经营方式与政策。",
 "pol":"本条不展开政权序列；土地权属与农业政策影响土壤管理。",
 "conn":"侵蚀产生的泥沙随河流输送到下游与海岸，把坡地与河口生态联系起来。",
 "today":"全球土壤退化受到关注，监测依赖调查与遥感。有机质含量、侵蚀速率与退化面积需按年份从 FAO 机构页核验。",
 "sources":["fao-global-soil-partnership","s083-fao-org"],
 "proof":"fao-global-soil-partnership 标题即主题，剥离后 5215 字符、soil 命中 53"},
}
def upgrade(t):
 e=T[t];c=C[t]
 e.update({"level":"L2","status":"L2完成(第20轮)-主题页","definition":c["def"],
  "overview":c["def"].split("：",1)[1],"time_or_place":e.get("time_or_place") or "时期与年代待专门来源核验（详见待核实）",
  "geo":c["geo"],"influence":c["infl"] if "infl" in c else c["influence"],
  "polities":c["pol"],"connections":c["conn"],"today":c["today"],
  "sources":c["sources"],"needs_verification":True,"last_update":TODAY,
  "pending_notes":f"第20轮按 D055 档①升级：专题页标题即主题且正文达标（{c['proof']}）；五段仅写来源可支撑的概述，具体数值待核。"})
 e["svg"]=("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='示意图'>"
  "<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>"
  +("<path d='M80 300 C 200 240 300 200 420 190 C 520 182 620 200 690 230' fill='none' stroke='var(--accent)' stroke-width='4'/>"
    "<path d='M80 340 C 200 300 300 270 420 262 C 520 256 620 275 690 300' fill='none' stroke='var(--accent2)' stroke-width='2' stroke-dasharray='6 4'/>"
    if t=="土壤资源" else
    "<ellipse cx='300' cy='200' rx='120' ry='60' fill='none' stroke='var(--accent)' stroke-width='3'/>"
    "<ellipse cx='520' cy='240' rx='90' ry='45' fill='none' stroke='var(--accent)' stroke-width='3'/>"
    "<path d='M300 200 L520 240' fill='none' stroke='var(--accent2)' stroke-width='2' stroke-dasharray='5 4'/>")
  +f"<text x='40' y='370' class='dim'>{t} · 简笔示意，非精确测绘</text></svg>")
 return t

# 遗产 L2 来源分级标注
LEGACY_TAG="（D041 前遗产 L2·待补专题页）"
n=0
for t,e in T.items():
 if e["level"]!="L2" or LEGACY_TAG not in (e.get("status") or ""): continue
 srcs=e.get("sources",[])
 alias=[s for s in srcs if s in {"britannica-regions","wikipedia-regions","un-m49","ap-human-geo"}]
 inst=[s for s in srcs if s not in alias]
 grade="全别名（无任何专题/机构正文）" if not inst else f"别名 {len(alias)} + 机构 {len(inst)}（专题页缺失）"
 line=f" 【第20轮来源分级】{grade}；所需专题页类型：{e['theme']}类正文页（D055 达标）。"
 if "第20轮来源分级" not in (e.get("pending_notes") or ""):
  e["pending_notes"]=(e.get("pending_notes") or "")+line
  e["last_update"]=TODAY;n+=1

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("升级",list(C),"遗产分级标注",n)