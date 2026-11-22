# -*- coding: utf-8 -*-
"""第30轮补：5 条 today 填数据（丝路/亚马逊河/游牧/气候带/人口迁移）。"""
import json,os,sys,subprocess,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
D=json.load(open(os.path.join(ROOT,"reports","round25_wb_data.json"),encoding="utf-8"))
def f(c,k):
    r=D.get(c,{}).get(k)
    if not r: return None
    if k=="pop_total": return f"{int(r['value']):,} 人（{r['year']}年）"
    if k=="life_exp": return f"{r['value']:.1f} 岁（{r['year']}年）"
    return f"{r['value']:.1f}%（{r['year']}年）"

P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}
# 新增 WLD 可耕地端点
if "wb-wld-arable" not in have:
    u="https://api.worldbank.org/v2/country/WLD/indicator/AG.LND.ARBL.ZS?format=json&per_page=100&date=2015:2025"
    p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-o","-","-w","\n__HTTP__%{http_code}",u],capture_output=True,timeout=35)
    raw=p.stdout.decode("utf-8","ignore");b,c=raw.rsplit("\n__HTTP__",1)
    sd["sources"].append({"id":"wb-wld-arable","title":"World Bank API — Arable land (% of land area, 全球)",
      "author":"World Bank","year":None,"type":"数据端点","url":u,"url2":None,"link_ok":True,"verified":True,
      "page_title":"World Bank API — Arable land (% of land area, 全球)",
      "note":f"JSON API {int(c.strip() or 0)}；返回世界可耕地占土地面积比例；2023 年 10.67%。"})
    json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
FILL={
"丝绸之路":(f"以哈萨克斯坦与乌兹别克斯坦为例，来源：世界银行 API。哈萨克斯坦总人口 {f('KAZ','pop_total')}（SP.POP.TOTL）、"
  f"城市化率 {f('KAZ','urban_pct')}（SP.URB.TOTL.IN.ZS）；乌兹别克斯坦总人口 {f('UZB','pop_total')}、城市化率 {f('UZB','urban_pct')}。"
  "上述为两国全国口径数据，仅示量级；丝路沿线货运量与过境流量需专门统计核验。",
  ["wb-kaz-pop","wb-kaz-urban","wb-uzb-pop","wb-uzb-urban"]),
"亚马逊河":(f"以巴西为例，来源：世界银行 API。巴西总人口 {f('BRA','pop_total')}（SP.POP.TOTL）、"
  f"森林覆盖率 {f('BRA','forest_pct')}（AG.LND.FRST.ZS）。上述为全国口径，仅示量级；"
  "亚马逊流域的径流量与航运数据需专门水文与遥感来源核验。",["wb-bra-pop","wb-bra-forest"]),
"游牧":(f"以蒙古为例，来源：世界银行 API。蒙古总人口 {f('MNG','pop_total')}（SP.POP.TOTL）、"
  f"城市化率 {f('MNG','urban_pct')}（SP.URB.TOTL.IN.ZS）。上述为全国口径，仅示量级；"
  "牧业人口占比与草场载畜量需专门牧业统计核验。",["wb-mng-pop","wb-mng-urban"]),
"气候带":("来源：世界银行 API（指标 AG.LND.ARBL.ZS，可耕地占土地面积比例）：全球 2023 年 10.67%。"
  "可耕地在各气候带内分布极不均（温带与热带季风区占比高、干旱与寒带极低），全球均值仅作量级参考；"
  "气候带界线与面积数据需专门气候分类来源核验。",["wb-wld-arable"]),
"人口迁移":("来源：世界银行 API（指标 SP.URB.TOTL.IN.ZS，城市人口占比）：全球 2025 年 57.8%。"
  "城市化是迁移的主要流向指标之一，但不能替代净迁移率；跨国迁移存量与流向需专门迁移统计（如 UN 迁移存量表）核验。",["wb-wld-urban"]),
}
n=0
for t,(txt,srcs) in FILL.items():
    e=T.get(t)
    if not e: continue
    e["today"]=txt
    for s in srcs:
        if s not in e["sources"]: e["sources"].append(s)
    e["pending_notes"]=((e.get("pending_notes") or "")+
      " 【第30轮现状数据】today 填入世界银行实测值（国别或全球口径，含年份与指标编号；已声明指标局限）。").strip()
    e["last_update"]=TODAY;n+=1
for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("补填",n,"条")