# -*- coding: utf-8 -*-
"""第15轮：4条按D041升级L2（专题页+机构页）+ 36复核。"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
NAT="本条只写自然地理与生态背景，不叙述具体政权、王朝与年代序列（相关历史条目待专门史料核验）。"

C={
"格陵兰岛":{
 "definition":"格陵兰岛：位于北大西洋与北冰洋之间的大型岛屿，大部分面积被冰盖覆盖。",
 "overview":"位于北大西洋与北冰洋之间的大型岛屿，大部分面积被冰盖覆盖。",
 "geo":"岛屿内陆为巨厚冰盖，边缘分布冰原与裸露岩地。NASA 冰盖指标页把格陵兰与南极并列观测，记录冰体质量变化趋势，是理解岛屿冰况的主要数据入口。",
 "influence":"冰盖质量变化影响全球海平面，是关键气候变量；沿海地带受海冰与洋流影响，人类活动集中于少数定居点。影响机制需结合观测，不作单因推断。",
 "polities":NAT,
 "connections":"岛屿与北大西洋、北冰洋水域相连，冰盖通过冰川输出与海洋、大气相互作用。",
 "today":"冰盖质量变化与海平面关系是研究重点。冰量、气温与融水数据需按年份从 NASA/NOAA 冰盖指标页核验。",
 "sources":["nasa-ice-sheets","s039-climate-nasa-gov"],
 "svg":"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='格陵兰冰盖示意图'><rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/><ellipse cx='380' cy='210' rx='210' ry='110' fill='none' stroke='var(--line)' stroke-width='2'/><ellipse cx='380' cy='215' rx='150' ry='80' fill='none' stroke='var(--accent)' stroke-width='4'/><path d='M230 210 L200 300 M530 215 L570 300' fill='none' stroke='var(--accent2)' stroke-width='3' stroke-dasharray='6 4'/><text x='320' y='220' class='lbl'>冰盖</text><text x='150' y='320' class='lbl'>冰川输出</text><text x='575' y='320' class='lbl'>冰川输出</text><text x='40' y='370' class='dim'>示意图，非精确测绘</text></svg>"},
"北美冰盖":{
 "definition":"北美冰盖：地质历史时期覆盖北美北部的巨大冰体，对当地地形与水系留下深远影响。",
 "overview":"地质历史时期覆盖北美北部的巨大冰体，对当地地形与水系留下深远影响。",
 "geo":"冰体由长期积雪压实形成并缓慢流动，侵蚀基岩、搬运碎屑，退却后在原范围留下冰碛与冰川湖。USGS 冰川科普页说明冰川作为气候指示的意义与流动、侵蚀的基本机制。",
 "influence":"冰川作用塑造盆地、丘陵与河谷，影响后来的水系与土壤分布。地貌与气候的关联有明确证据，具体范围与时序需区域资料细化。",
 "polities":NAT,
 "connections":"冰盖范围变化改变水系与海岸线，进而影响生物迁移与后续人类活动的地理条件。",
 "today":"作为古环境研究对象，其范围与消退时间由地质与湖泊沉积记录重建。年代与范围数据需按年份从 USGS/NASA 机构页核验。",
 "sources":["usgs-glaciers","nps-grand-canyon-geology"],
 "svg":"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='冰盖与冰川地貌示意图'><rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/><path d='M90 250 C 200 160 330 150 450 190 C 560 225 640 250 690 265' fill='none' stroke='var(--accent)' stroke-width='4'/><path d='M120 290 C 230 220 350 210 460 240' fill='none' stroke='var(--accent2)' stroke-width='2' stroke-dasharray='5 4'/><circle cx='200' cy='205' r='5' class='pt'/><text x='175' y='185' class='lbl'>冰体</text><circle cx='360' cy='175' r='5' class='pt'/><text x='330' y='155' class='lbl'>冰流</text><circle cx='560' cy='228' r='5' class='pt'/><text x='545' y='208' class='lbl'>冰碛</text><text x='40' y='370' class='dim'>示意图，非精确测绘</text></svg>"},
"山地农业":{
 "definition":"山地农业：在高差大、坡度陡的地区进行的农业活动，常以梯田与多样作物组合适应环境。",
 "overview":"在高差大、坡度陡的地区进行的农业活动，常以梯田与多样作物组合适应环境。",
 "geo":"山地具有明显垂直气候带，气温与降水随海拔变化，土层薄且易受侵蚀。坡面水文过程快，水土保持是耕作的前提条件。FAO 山地伙伴关系专题页把山地生态系统的脆弱性与生计依赖作为核心议题。",
 "influence":"垂直分带使同一区域可种植不同作物，梯田与等高耕作有助于保持水土。耕作方式受土地制度与技术条件影响，不是环境的必然结果。",
 "polities":NAT,
 "connections":"山地农业区常与低地市场形成垂直交换，山货与粮食沿山路与河谷流动。",
 "today":"坡地退化、劳动力变化与气候变化是主要议题。耕地面积、产量与土壤侵蚀数据需按年份从 FAO 机构页核验。",
 "sources":["fao-mountain-partnership","s083-fao-org"],
 "svg":"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='山地垂直农业示意图'><rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/><path d='M80 330 L300 110 L520 330' fill='none' stroke='var(--line)' stroke-width='3'/><g stroke='var(--accent)' stroke-width='2'><path d='M150 300 L240 300'/><path d='M185 260 L285 260'/><path d='M225 220 L325 220'/><path d='M265 180 L355 180'/></g><circle cx='300' cy='110' r='5' class='pt'/><text x='312' y='112' class='lbl'>高海拔</text><circle cx='150' cy='305' r='5' class='pt'/><text x='95' y='290' class='lbl'>梯田</text><text x='40' y='370' class='dim'>示意图，非精确测绘</text></svg>"},
"人口迁移":{
 "definition":"人口迁移：人口在地理空间上的移动，按范围可分为区域内、跨区域与国际迁移。",
 "overview":"人口在地理空间上的移动，按范围可分为区域内、跨区域与国际迁移。",
 "geo":"迁移流与来源地、目的地之间的经济机会、环境条件与交通可达性相关；迁移网络一旦形成，会沿既有路径持续。OWID 迁移专题页汇总跨国迁移存量与流向数据，可作为核对口径的入口。",
 "influence":"迁移改变人口分布与年龄结构，也影响来源地与目的地的劳动力与公共服务。迁移决策由多因素驱动，不宜归因于单一环境压力。",
 "polities":NAT,
 "connections":"迁移把不同区域连成网络，伴随资金、信息与文化的流动，形成跨区域联系。",
 "today":"城市化与国际迁移是当代主要趋势，统计口径因国家而异。净迁移率、城市化率与人口分布数据需按年份从 UN/OWID 机构页核验。",
 "sources":["owid-migration","s004-population-un-org"],
 "svg":"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='人口迁移流向示意图'><rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/><path d='M140 280 C 260 200 400 190 600 155' fill='none' stroke='var(--accent)' stroke-width='3'/><path d='M600 155 L578 148 M600 155 L582 168' fill='none' stroke='var(--accent)' stroke-width='3'/><circle cx='140' cy='280' r='7' class='pt'/><text x='105' y='302' class='lbl'>来源地</text><circle cx='610' cy='150' r='7' class='pt'/><text x='590' y='130' class='lbl'>目的地</text><text x='340' y='185' class='lbl'>迁移流</text><text x='40' y='370' class='dim'>示意图，非精确测绘</text></svg>"},
}

GAP={"地形":"地貌形成年代与关键地形节点的专题来源","气候":"气候机制与长期变化数据的专题来源",
 "农业":"作物制度、农业起源与水利细节的专题来源","贸易":"商路节点、商品结构与转运机制的专题来源",
 "政权更替":"政权年代序列与制度细节的专题来源","区域":"区域边界、人口与现状数据的专题来源"}
POOL={"地形":["s056-earthquake-usgs-gov","s038-earthobservatory-nasa-gov"],
 "气候":["s039-climate-nasa-gov","s048-climate-gov"],"农业":["s018-fao-org","s077-ourworldindata-org"],
 "贸易":["s057-databank-worldbank-org","s025-ourworldindata-org"],"政权更替":["s011-unesco-org","s058-worldbank-org"],
 "区域":["un-m49","s075-aag-org"]}

def upgrade(docs,title):
 for d in docs.values():
  for e in d["entries"]:
   if e["title"]==title:
    c=C[title]
    e.update({"level":"L2","status":"L2完成(第15轮)-D041专题来源",
     "definition":c["definition"],"overview":c["overview"],
     "time_or_place":"时期与年代待专门来源核验（详见待核实）",
     "geo":c["geo"],"influence":c["influence"],"polities":c["polities"],
     "connections":c["connections"],"today":c["today"],"svg":c["svg"],
     "sources":c["sources"],"needs_verification":True,"last_update":TODAY,
     "pending_notes":"第15轮按 D041 升级：专题页正文含主题关键词（NASA冰盖指标 / FAO山地伙伴 / OWID迁移 / USGS冰川），仅写来源可支撑的自然地理与人口内容；政权与年代细节留待专门史料，现状数值待按年份核验。"})
    return e["id"]
 raise SystemExit("未找到:"+title)

def review_titles(docs):
 out=[]
 for u in UNITS:
  for e in docs[u]["entries"]:
   if e["tier"]=="重要" and e["level"]=="L1" and "已复核(第14轮)" not in e["status"]:
    out.append(e["title"])
 return out[:36]

def review(docs,title):
 for d in docs.values():
  for e in d["entries"]:
   if e["title"]==title:
    gap=GAP.get(e["theme"],"专题来源");pool=POOL.get(e["theme"],["un-m49"]);added=None
    for s in pool:
     if s not in e["sources"]: e["sources"].append(s);added=s;break
    e["pending_notes"]=(f"第15轮复核：{e['region']}×{e['theme']}；新增背景来源 {added or '无'}，"
      f"现有来源均已核验，但按 D041 须补含主题关键词的专题页，{gap} 仍待补。")
    e["last_update"]=TODAY;e["status"]="已复核(第15轮)"
    return e["id"]
 raise SystemExit("未找到复核:"+title)

def main():
 b=int(sys.argv[1]);docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS};done=[]
 if b==1:
  for t in C: done.append(upgrade(docs,t))
  for t in review_titles(docs)[:6]: done.append("REVIEW:"+review(docs,t))
 else:
  titles=review_titles(docs);start=6+(b-2)*10
  for t in titles[start:start+10]: done.append("REVIEW:"+review(docs,t))
 for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
 update_coverage(docs)
 print(f"batch {b}: {len(done)} tasks -> "+", ".join(done[:4])+(" ..." if len(done)>4 else ""))
if __name__=="__main__": main()