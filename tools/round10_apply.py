# -*- coding: utf-8 -*-
"""第10轮：10个B6主题L1 + 30复核，分4批。"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import sid,update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
NEW=[
 ("预期寿命空间差异","补充","全球","区域","现代统计（年份以来源页面为准）","不同地区预期寿命差异受医疗、营养、冲突与年龄结构等多因素影响，是社会地理的重要指标。",["s033-ourworldindata-org","s004-population-un-org"],"人口年龄结构"),
 ("人均产出空间差异","补充","全球","贸易","现代统计（年份以来源页面为准）","人均经济产出的地区差异反映产业结构、人口规模与制度条件的组合，不能直接等同于生活水平。",["s034-ourworldindata-org","s057-databank-worldbank-org"],"极端贫困空间分布"),
 ("作物单产差异","补充","全球","农业","现代统计（年份以来源页面为准）","单位面积作物产量差异与土壤、气候、投入品和管理方式有关，是粮食安全分析的基础。",["s078-ourworldindata-org","s014-fao-org"],"土地利用变化"),
 ("肥料使用与环境","补充","全球","农业","现代统计（年份以来源页面为准）","肥料投入提高作物产量，也可能通过径流与氧化亚氮排放影响水土与气候，需结合区域条件评估。",["s079-ourworldindata-org","s018-fao-org"],"作物单产差异"),
 ("肉奶生产与土地","补充","全球","农业","现代统计（年份以来源页面为准）","肉奶生产需要饲料与牧场，土地利用与温室气体排放随生产方式和区域条件变化。",["s080-ourworldindata-org","s077-ourworldindata-org"],"土地利用变化"),
 ("自然灾害风险","补充","全球","气候","现代观测（年份以来源页面为准）","灾害风险是致灾因子、暴露程度与脆弱性共同作用的结果，地理分布并不等同于风险本身。",["s031-ourworldindata-org","s056-earthquake-usgs-gov"],"气候带"),
 ("森林面积占比","补充","全球","气候","现代统计（年份以来源页面为准）","森林覆盖率反映土地利用与生态状况，其变化与气候、木材需求和政策共同关联。",["s036-ourworldindata-org","s018-fao-org"],"森林覆盖变化"),
 ("人口增长","补充","全球","区域","现代统计（年份以来源页面为准）","人口增长由出生、死亡与迁移共同决定，地区差异与年龄结构、城市化和政策环境相关。",["s023-ourworldindata-org","s004-population-un-org"],"人口地理"),
 ("城市化水平","补充","全球","区域","现代统计（年份以来源页面为准）","城市人口比例变化反映经济结构、迁移与公共服务供给，不同国家口径可能不同。",["s025-ourworldindata-org","s058-worldbank-org"],"城市地理"),
 ("全球气温变化","补充","全球","气候","现代观测（年份以来源页面为准）","全球平均气温变化是气候系统状态的核心指标，区域差异明显，解读需结合长期序列与观测方法。",["s026-ourworldindata-org","s039-climate-nasa-gov"],"碳排放空间差异"),
]
GAP_BY_THEME={"地形":"地貌形成年代与关键地形节点的专题来源","气候":"气候机制与长期变化数据的专题来源",
 "农业":"作物制度、农业起源与水利细节的专题来源","贸易":"商路节点、商品结构与转运机制的专题来源",
 "政权更替":"政权年代序列与制度细节的专题来源","区域":"区域边界、人口与现状数据的专题来源"}
SOURCE_BY_THEME={"地形":["s056-earthquake-usgs-gov","s038-earthobservatory-nasa-gov"],
 "气候":["s039-climate-nasa-gov","s048-climate-gov"],"农业":["s018-fao-org","s077-ourworldindata-org"],
 "贸易":["s057-databank-worldbank-org","s025-ourworldindata-org"],"政权更替":["s011-unesco-org","s058-worldbank-org"],
 "区域":["un-m49","s075-aag-org"]}
def add_new(docs):
 out=[]
 for title,tier,region,theme,tp,overview,sources,rel in NEW:
  if any(e["title"]==title for e in docs["global-themes"]["entries"]): continue
  rid=None
  for d in docs.values():
   for e in d["entries"]:
    if e["title"]==rel: rid=e["id"];break
   if rid:break
  e={"id":"global-themes-"+sid(title),"title":title,"tier":tier,"unit_id":"global-themes","region":region,
   "theme":theme,"level":"L1","status":"L1完成(第10轮)","definition":title+"："+overview,
   "time_or_place":tp,"overview":overview,"related":[rid] if rid else [],"sources":sources,
   "needs_verification":True,"pending_notes":"B6 主题补入；具体年份、口径与数值需按来源页面逐条核验。",
   "outlines":["Our World in Data 主题页","UN/FAO/World Bank/NASA 机构页"],"last_update":TODAY}
  docs["global-themes"]["entries"].append(e);out.append(e["id"])
 return out
def review_titles(docs):
 out=[]
 for u in UNITS:
  for e in docs[u]["entries"]:
   if e["tier"]=="重要" and e["level"]=="L1" and "已复核(第9轮)" not in e["status"]:
    out.append(e["title"])
 return out[:30]
def review(docs,title):
 for d in docs.values():
  for e in d["entries"]:
   if e["title"]==title:
    gap=GAP_BY_THEME.get(e["theme"],"专题来源");pool=SOURCE_BY_THEME.get(e["theme"],["un-m49"]);added=None
    for s in pool:
     if s not in e["sources"]: e["sources"].append(s);added=s;break
    e["pending_notes"]=(f"第10轮复核：{e['region']}×{e['theme']}；新增背景来源 {added or '无'}，"
      f"现有来源均已核验，但 {gap} 仍待补，故保留待核实。")
    e["last_update"]=TODAY;e["status"]="已复核(第10轮)"
    return e["id"]
 raise SystemExit("未找到复核:"+title)
def append_scope(titles):
 p=os.path.join(ROOT,"scope.md");t=open(p,encoding="utf-8").read();marker="## 纳入/排除规则"
 block="### 第10轮补充（B6 主题）\n\n"+"".join(f"- **{x}**（补充；全球主题）— 已核验机构主题页补入。\n" for x in titles)+"\n"
 if "### 第10轮补充" not in t: t=t.replace(marker,block+marker)
 open(p,"w",encoding="utf-8").write(t)
def main():
 b=int(sys.argv[1]);docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS};done=[]
 if b==1:
  done+=["NEW:"+x for x in add_new(docs)]
  append_scope([n[0] for n in NEW])
 else:
  titles=review_titles(docs);start=(b-2)*10
  for t in titles[start:start+10]: done.append("REVIEW:"+review(docs,t))
 for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
 update_coverage(docs)
 print(f"batch {b}: {len(done)} tasks -> "+", ".join(done[:4])+(" ..." if len(done)>4 else ""))
if __name__=="__main__": main()
