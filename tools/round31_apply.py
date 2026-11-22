# -*- coding: utf-8 -*-
"""第31轮：4 条 today 填数据（南极条约体系/二氧化碳/农业企业/城市地理）。"""
import json,os,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]

P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}
NEW=[
 ("ats-parties","Antarctic Treaty Secretariat — Parties","https://www.ats.aq/devAS/Parties?lang=e",
  "官方页；页面载明原始签署国为参与 1957–58 国际地球物理年的 12 国；缔约方名录随批准情况更新。",200,5345,17),
 ("wb-wld-co2","World Bank API — CO₂ emissions (EN.GHG.CO2.MT.CE.AR5, 全球)",
  "https://api.worldbank.org/v2/country/WLD/indicator/EN.GHG.CO2.MT.CE.AR5?format=json&per_page=100&date=2015:2025",
  "2024 年 39,632.66 Mt CO₂e（含土地利用口径 AR5）",200,2163,48),
 ("wb-wld-agriland","World Bank API — Agricultural land (% of land area, 全球)",
  "https://api.worldbank.org/v2/country/WLD/indicator/AG.LND.AGRI.ZS?format=json&per_page=100&date=2015:2025",
  "2023 年 36.9%",200,2508,44),
 ("wb-wld-urbangrow","World Bank API — Urban population growth (annual %, 全球)",
  "https://api.worldbank.org/v2/country/WLD/indicator/SP.URB.GROW?format=json&per_page=100&date=2015:2025",
  "2025 年 1.36%",200,2497,44),
]
for sid,title,url,latest,code,n,h in NEW:
    if sid in have: continue
    sd["sources"].append({"id":sid,"title":title,
      "author":"Antarctic Treaty Secretariat" if sid.startswith("ats") else "World Bank",
      "year":None,"type":"官方机构" if sid.startswith("ats") else "数据端点",
      "url":url,"url2":None,"link_ok":True,"verified":True,"page_title":title,
      "note":f"HTTP {code}；剥离后正文 {n} 字符、主题命中 {h}；{latest}" +
             ("；本页为缔约方名录，随批准更新，以页面当前状态为准。" if sid.startswith("ats") else "；年度指标，随年度更新与历史修订变化。")})
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
FILL={
"南极条约体系":("来源：南极条约秘书处（ATS）官方缔约方名录页：条约原始签署国为参与 1957–58 年国际地球物理年的 12 个国家，"
  "其后缔约方数量随批准与加入持续增加。具体缔约方名单与最新数量以 ATS 页面当前状态为准（名录随批准更新，本站不写死数字）。"),
"二氧化碳排放清单":("来源：世界银行 API（指标 EN.GHG.CO2.MT.CE.AR5，含土地利用的 CO₂ 当量排放）：全球 2024 年约 39,632.66 Mt CO₂e。"
  "该口径与仅计能源燃烧的清单不同，跨国比较须核对核算范围。"),
"农业企业与价值链":("来源：世界银行 API（指标 AG.LND.AGRI.ZS，农业用地占土地面积比例）：全球 2023 年 36.9%。"
  "农业用地占比反映生产空间基础，不等于价值链组织程度；加工、物流与合同关系的指标需专门调查数据。"),
"城市地理":("来源：世界银行 API（指标 SP.URB.GROW，城市人口年增长率）：全球 2025 年 1.36%。"
  "该值为全球合计增速，各地区差异显著；城市内部结构与首位度等指标需城市统计资料核验。"),
}
n=0
for t,txt in FILL.items():
    e=T.get(t)
    if not e: continue
    e["today"]=txt
    sid={"南极条约体系":"ats-parties","二氧化碳排放清单":"wb-wld-co2",
         "农业企业与价值链":"wb-wld-agriland","城市地理":"wb-wld-urbangrow"}[t]
    if sid not in e["sources"]: e["sources"].append(sid)
    e["pending_notes"]=((e.get("pending_notes") or "")+
      " 【第31轮现状数据】today 填入官方/机构端点实测或名录信息（含年份或更新说明；对动态名录不写死数量）。").strip()
    e["last_update"]=TODAY;n+=1
for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("填充",n,"条")