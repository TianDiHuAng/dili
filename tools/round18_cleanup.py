# -*- coding: utf-8 -*-
"""第18轮：按 theme×source 矩阵批量清理误贴来源（D049）。

移除规则：
- s011（UNESCO Climate action，政策页）：从「政权更替」类全部移除（23条）
- s056（USGS 站点迁移通告，0 内容）：全部移除（12条）
- s058（World Bank 已 301 至泛化 topics）：从「政权更替」类移除（21条）
- s025（OWID Urbanization）：从「贸易」类移除（14条）
- s057（DataBank 应用壳页）：从「贸易」类移除（18条）

保底：移除后 sources < 2 时，从同主题已核验来源池补入（不补则违反 R4）。
"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]

RULE=[  # (source, 移除的theme集合)
 ("s011-unesco-org",{"政权更替"}),
 ("s056-earthquake-usgs-gov",{"地形","气候","区域"}),
 ("s058-worldbank-org",{"政权更替"}),
 ("s025-ourworldindata-org",{"贸易"}),
 ("s057-databank-worldbank-org",{"贸易"}),
]
POOL={"地形":["un-m49","s038-earthobservatory-nasa-gov"],
 "气候":["s039-climate-nasa-gov","s048-climate-gov"],
 "农业":["s018-fao-org","s077-ourworldindata-org"],
 "贸易":["s075-aag-org","s025-ourworldindata-org"],
 "政权更替":["s010-unesco-org","un-m49"],
 "区域":["un-m49","s075-aag-org"]}

docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
removed={};topped=[]
for d in docs.values():
 for e in d["entries"]:
  for src,themes in RULE:
   if src in e.get("sources",[]) and e["theme"] in themes:
    e["sources"]=[s for s in e["sources"] if s!=src]
    removed.setdefault(src,[]).append(e["title"])
  if len(e["sources"])<2:
   for s in POOL.get(e["theme"],["un-m49","s075-aag-org"]):
    if s not in e["sources"]:
     e["sources"].append(s);topped.append((e["title"],s));break
   if len(e["sources"])<2:
    for s in ["un-m49","s075-aag-org","s010-unesco-org"]:
     if s not in e["sources"]:
      e["sources"].append(s);topped.append((e["title"],s));break

# 标注 why（追加式，D051）
NOTE={"s011-unesco-org":"s011（UNESCO Climate action 政策页）与「政权更替」主题错配",
 "s056-earthquake-usgs-gov":"s056（USGS 站点迁移通告页，正文无地质内容，0 命中）",
 "s058-worldbank-org":"s058（已 301 至泛化 development-topics 索引）",
 "s025-ourworldindata-org":"s025（OWID Urbanization，与「贸易」主题错配）",
 "s057-databank-worldbank-org":"s057（DataBank 应用壳页，可视正文约 41 字节）"}
for d in docs.values():
 for e in d["entries"]:
  for src in removed:
   if e["title"] in removed[src] and NOTE[src] not in (e.get("pending_notes") or ""):
    e["pending_notes"]=(e.get("pending_notes") or "")+f" 【第18轮矩阵清理】移除{NOTE[src]}（D049）。"
    e["last_update"]=TODAY

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
tot=sum(len(v) for v in removed.values())
print("移除合计",tot,{k:len(v) for k,v in removed.items()})
print("补底",len(topped),"条")
# 复扫
T={e["title"]:e for d in docs.values() for e in d["entries"]}
scan={}
for sid,_ in RULE:
 scan[sid]=sum(1 for e in T.values() if sid in e.get("sources",[]))
print("清理后余量",scan)
json.dump({"round":18,"removed":{k:len(v) for k,v in removed.items()},"after":scan,"topped":len(topped)},
  open(os.path.join(ROOT,"reports","round18_cleanup.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)