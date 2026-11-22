# -*- coding: utf-8 -*-
"""第16轮：1条换源合规 + 8条新增L1 + 31条复核，分4批。"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import sid,update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
NAT="本条只写自然地理与生态背景，不叙述具体政权、王朝与年代序列（相关历史条目待专门史料核验）。"

NEW=[
 ("拉丁美洲与加勒比区域发展","补充","全球","区域","现代统计（年份以来源页面为准）",
  "该区域包含多种气候带与经济体，发展指标差异大，需结合收入分组与统计口径阅读。",
  ["s066-worldbank-org","s057-databank-worldbank-org"],"南锥体"),
 ("中东与北非区域发展","补充","全球","区域","现代统计（年份以来源页面为准）",
  "该区域以干旱气候与能源经济为特征，发展指标受资源结构与人口结构影响。",
  ["s067-worldbank-org","s057-databank-worldbank-org"],"马格里布"),
 ("南亚区域发展","补充","全球","区域","现代统计（年份以来源页面为准）",
  "该区域人口密集、季风主导农业，发展指标与灌溉、城市化相关。",
  ["s068-worldbank-org","s057-databank-worldbank-org"],"印度河文明"),
 ("全球气温距平","补充","全球","气候","现代观测（年份以来源页面为准）",
  "以长期平均为基准的温度偏离量，是描述全球变暖进程的核心指标，需说明基准期与观测方法。",
  ["s053-climate-gov","s026-ourworldindata-org"],"全球气温变化"),
 ("二氧化碳排放清单","补充","全球","气候","现代统计（年份以来源页面为准）",
  "按国家或部门统计的二氧化碳排放量，口径差异影响跨国比较，需注明来源与核算方法。",
  ["s027-ourworldindata-org","s035-ourworldindata-org"],"碳排放空间差异"),
 ("保护与保育区体系","补充","全球","区域","现代管理实践（年份以来源页面为准）",
  "由国际公约与国内法设立的陆地与海洋保护空间，管理目标与治理模式因地区而异。",
  ["s072-cbd-int","s091-iucn-org"],"陆地保护区"),
 ("农业企业与价值链","补充","全球","农业","现代产业实践（年份以来源页面为准）",
  "从投入品、生产、加工到销售的链条组织方式，影响小农参与市场的方式与收益分配。",
  ["s059-worldbank-org","s014-fao-org"],"作物单产差异"),
 ("水资源供给概览","补充","全球","地形","现代统计（年份以来源页面为准）",
  "可再生水资源量与取用水结构是评估水压力的基础，跨流域与跨边界分配是常见议题。",
  ["s017-fao-org","s013-fao-org"],"水资源管理"),
]

GAP={"地形":"地貌形成年代与关键地形节点的专题来源","气候":"气候机制与长期变化数据的专题来源",
 "农业":"作物制度、农业起源与水利细节的专题来源","贸易":"商路节点、商品结构与转运机制的专题来源",
 "政权更替":"政权年代序列与制度细节的专题来源","区域":"区域边界、人口与现状数据的专题来源"}
POOL={"地形":["s017-fao-org","s038-earthobservatory-nasa-gov"],
 "气候":["s053-climate-gov","s048-climate-gov"],"农业":["s018-fao-org","s059-worldbank-org"],
 "贸易":["s057-databank-worldbank-org","s025-ourworldindata-org"],"政权更替":["s011-unesco-org","s058-worldbank-org"],
 "区域":["un-m49","s075-aag-org"]}

def add_new(docs):
 out=[]
 for title,tier,region,theme,tp,ov,srcs,rel in NEW:
  if any(e["title"]==title for e in docs["global-themes"]["entries"]): continue
  rid=None
  for d in docs.values():
   for e in d["entries"]:
    if e["title"]==rel: rid=e["id"];break
   if rid:break
  e={"id":"global-themes-"+sid(title),"title":title,"tier":tier,"unit_id":"global-themes","region":region,
   "theme":theme,"level":"L1","status":"L1完成(第16轮)","definition":title+"："+ov,
   "time_or_place":tp,"overview":ov,"related":[rid] if rid else [],"sources":srcs,
   "needs_verification":True,"pending_notes":"B6 未使用来源补入；具体年份、口径与数值需按来源页面逐条核验。",
   "outlines":["World Bank 区域/专题页","NOAA/OWID/CBD/IUCN/FAO 机构页"],"last_update":TODAY}
  docs["global-themes"]["entries"].append(e);out.append(e["id"])
 return out

def fix_achaemenid(docs):
 for d in docs.values():
  for e in d["entries"]:
   if e["title"]=="阿契美尼德波斯":
    e["sources"]=["livius-cyrus","livius-mesopotamia","s013-fao-org"]
    e["status"]="L2合规换源(第16轮)"
    e["pending_notes"]="第16轮合规换源：原用 s011（UNESCO，间歇可达）等；现改用 Livius『Cyrus the Great』（正文 9220 字节、achaemenid/cyrus 命中 45）作专题页，Livius Mesopotamia 与 AQUASTAT 作区域/机构页。政权年代序列仍待专门史料逐条核验。"
    e["last_update"]=TODAY
    # 去掉旧遗产标记
    e["status"]=e["status"].replace("（D041 前遗产 L2·待补专题页）","")
    return e["id"]
 raise SystemExit("未找到阿契美尼德波斯")

def review_titles(docs):
 out=[]
 for u in UNITS:
  for e in docs[u]["entries"]:
   if e["tier"]=="重要" and e["level"]=="L1" and "已复核(第15轮)" not in e["status"]:
    out.append(e["title"])
 return out[:31]

def review(docs,title):
 for d in docs.values():
  for e in d["entries"]:
   if e["title"]==title:
    gap=GAP.get(e["theme"],"专题来源");pool=POOL.get(e["theme"],["un-m49"]);added=None
    for s in pool:
     if s not in e["sources"]: e["sources"].append(s);added=s;break
    e["pending_notes"]=(f"第16轮复核：{e['region']}×{e['theme']}；新增背景来源 {added or '无'}；"
      f"按 D041/D044 仍缺含主题关键词的专题正文页（{gap}）。")
    e["last_update"]=TODAY;e["status"]="已复核(第16轮)"
    return e["id"]
 raise SystemExit("未找到复核:"+title)

def append_scope(titles):
 p=os.path.join(ROOT,"scope.md");t=open(p,encoding="utf-8").read();marker="## 纳入/排除规则"
 block="### 第16轮补充（B6 未使用来源）\n\n"+"".join(f"- **{x}**（补充；全球主题）— 已核验机构来源补入。\n" for x in titles)+"\n"
 if "### 第16轮补充" not in t: t=t.replace(marker,block+marker)
 open(p,"w",encoding="utf-8").write(t)

def main():
 b=int(sys.argv[1]);docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS};done=[]
 if b==1:
  done.append("FIX:"+fix_achaemenid(docs))
  done+=["NEW:"+x for x in add_new(docs)]
  append_scope([n[0] for n in NEW])
  for t in review_titles(docs)[:1]: done.append("REVIEW:"+review(docs,t))
 else:
  start=(b-2)*10+1
  for t in review_titles(docs)[start:start+10]: done.append("REVIEW:"+review(docs,t))
 for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
 update_coverage(docs)
 print(f"batch {b}: {len(done)} tasks -> "+", ".join(done[:3])+(" ..." if len(done)>3 else ""))
if __name__=="__main__": main()