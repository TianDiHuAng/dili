# -*- coding: utf-8 -*-
"""第14轮复核补齐：related 语义、五大湖细节与SVG、polities标题、台账。"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]

REL={"五大湖":["北美冰盖","密西西比河","科罗拉多高原"],
     "科罗拉多高原":["落基山脉","大平原","北美冰盖"],
     "墨西哥湾":["密西西比河","加勒比海群岛","大平原"],
     "人口迁移":["人口地理","城市化水平","人口增长"],
     "湄公河三角洲":["中南半岛","马来群岛","吴哥"]}

docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
titles={e["title"]:e for d in docs.values() for e in d["entries"]}

for t,names in REL.items():
 e=titles.get(t)
 if not e: continue
 ids=[titles[n]["id"] for n in names if n in titles]
 e["related"]=list(dict.fromkeys(ids))[:3]
 e["last_update"]=TODAY

# 五大湖：改写无源断言 + 5 湖 SVG
gl=titles.get("五大湖")
if gl:
 gl["definition"]="五大湖：北美中东部的五个相连大型淡水湖群，位于美加交界地带，属圣劳伦斯水系。"
 gl["overview"]="北美中东部的五个相连大型淡水湖群，位于美加交界地带，属圣劳伦斯水系。"
 gl["geo"]="湖群由五个相连的大型淡水湖组成，分别是苏必利尔湖、密歇根湖、休伦湖、伊利湖与安大略湖。湖区属温带气候，季节水位变化是重要水文特征。"
 gl["connections"]="五个湖泊以水道相连，并汇入圣劳伦斯水系；具体通航与流域边界细节待专题页核验。"
 gl["svg"]=("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='五大湖示意图'>"
  "<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>"
  "<ellipse cx='250' cy='150' rx='85' ry='55' fill='none' stroke='var(--accent)' stroke-width='3'/>"
  "<ellipse cx='330' cy='245' rx='55' ry='45' fill='none' stroke='var(--accent)' stroke-width='3'/>"
  "<ellipse cx='430' cy='205' rx='60' ry='50' fill='none' stroke='var(--accent)' stroke-width='3'/>"
  "<ellipse cx='515' cy='275' rx='50' ry='32' fill='none' stroke='var(--accent)' stroke-width='3'/>"
  "<ellipse cx='585' cy='330' rx='45' ry='25' fill='none' stroke='var(--accent)' stroke-width='3'/>"
  "<path d='M585 330 L660 352' fill='none' stroke='var(--accent2)' stroke-width='3' stroke-dasharray='6 4'/>"
  "<circle cx='250' cy='150' r='5' class='pt'/><text x='175' y='120' class='lbl'>苏必利尔</text>"
  "<circle cx='330' cy='245' r='5' class='pt'/><text x='300' y='275' class='lbl'>密歇根</text>"
  "<circle cx='430' cy='205' r='5' class='pt'/><text x='405' y='180' class='lbl'>休伦</text>"
  "<circle cx='515' cy='275' r='5' class='pt'/><text x='495' y='300' class='lbl'>伊利</text>"
  "<circle cx='585' cy='330' r='5' class='pt'/><text x='570' y='300' class='lbl'>安大略</text>"
  "<text x='665' y='356' class='lbl'>圣劳伦斯</text>"
  "<text x='40' y='370' class='dim'>示意图，非精确测绘</text></svg>")
 gl["last_update"]=TODAY

for u,d in docs.items():
 json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("related 已修正:",list(REL))
print("五大湖 SVG 五湖:", "苏必利尔" in (titles["五大湖"]["svg"] or ""))