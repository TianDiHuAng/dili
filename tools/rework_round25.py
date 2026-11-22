# -*- coding: utf-8 -*-
"""第25轮返工：修正 A1 失实陈述、补指标编号与新来源、L1 渲染 today、逐条化 30 条备注。"""
import json,os,re,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]

# 1) 补 NGA/USA 城市化率
D=json.load(open(os.path.join(ROOT,"reports","round25_wb_data.json"),encoding="utf-8"))
D.setdefault("NGA",{})["urban_pct"]={"value":63.7754180467872,"year":"2025","country":"Nigeria"}
D.setdefault("USA",{})["urban_pct"]={"value":80.1921733027869,"year":"2025","country":"United States"}
json.dump(D,open(os.path.join(ROOT,"reports","round25_wb_data.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)

# 2) 登记森林/农业指标来源
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}
ADDS=[("wb-api-forest","World Bank Indicator API — Forest area (% of land area) AG.LND.FRST.ZS","World Bank",
   "https://api.worldbank.org/v2/country/BRA/indicator/AG.LND.FRST.ZS?format=json&per_page=100&date=2015:2025",
   "JSON API 200；返回逐年年森林覆盖率（巴西 2024 年 58.5%）；正则为 forest|value。"),
 ("wb-api-agri","World Bank Indicator API — Agriculture, value added (% of GDP) NV.AGR.TOTL.ZS","World Bank",
   "https://api.worldbank.org/v2/country/EGY/indicator/NV.AGR.TOTL.ZS?format=json&per_page=100&date=2015:2025",
   "JSON API 200；返回逐年农业增加值占 GDP 比重（埃及 2025 年 16.6%）；正则为 agr|value。")]
for sid,title,author,url,note in ADDS:
    if sid in have: continue
    sd["sources"].append({"id":sid,"title":title,"author":author,"year":None,"type":"数据端点","url":url,"url2":None,
      "link_ok":True,"verified":True,"page_title":title,"note":note})
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
def u(c):
    r=D[c]["urban_pct"]; return f"{r['value']:.1f}%（{r['year']}年）"
def p(c):
    r=D[c]["pop_total"]; return f"{int(r['value']):,}（{r['year']}年）"
def f(c):
    r=D[c]["forest_pct"]; return f"{r['value']:.1f}%（{r['year']}年）"
def a(c):
    r=D[c]["agri_pct_gdp"]; return f"{r['value']:.1f}%（{r['year']}年）"

# 3) 重写 5 条 today（补指标编号 + 修 A1）
FILL={
"城市化水平":f"来源：世界银行 API。城市人口占比（指标 SP.URB.TOTL.IN.ZS）：中国 {u('CHN')}、印度 {u('IND')}、巴西 {u('BRA')}、墨西哥 {u('MEX')}、埃及 {u('EGY')}、尼日利亚 {u('NGA')}、美国 {u('USA')}。各国统计口径与年份不完全一致，跨国比较需注意定义差异。",
"人口地理":f"来源：世界银行 API。总人口（指标 SP.POP.TOTL）：印度 {p('IND')}、中国 {p('CHN')}、美国 {p('USA')}、尼日利亚 {p('NGA')}、巴西 {p('BRA')}、墨西哥 {p('MEX')}、埃及 {p('EGY')}。数据按世界银行口径，可能与各国普查结果略有差异。",
"拉丁美洲与加勒比区域发展":f"以代表性国家为例，来源：世界银行 API。巴西城市化率 {u('BRA')}（SP.URB.TOTL.IN.ZS）、墨西哥 {u('MEX')}（同指标）；巴西总人口 {p('BRA')}（SP.POP.TOTL）、墨西哥 {p('MEX')}；巴西森林覆盖率 {f('BRA')}（AG.LND.FRST.ZS）。区域内部差异大，本数据仅示量级，不代表区域整体。",
"中东与北非区域发展":f"以埃及为例，来源：世界银行 API。城市化率 {u('EGY')}（SP.URB.TOTL.IN.ZS）、总人口 {p('EGY')}（SP.POP.TOTL）、农业增加值占 GDP {a('EGY')}（NV.AGR.TOTL.ZS）。区域内产油国与进口国差异显著，不宜以单一国家代表全域。",
"南亚区域发展":f"以印度为例，来源：世界银行 API。城市化率 {u('IND')}（SP.URB.TOTL.IN.ZS）、总人口 {p('IND')}（SP.POP.TOTL）、森林覆盖率 {f('IND')}（AG.LND.FRST.ZS）。南亚各国差异大，本数据仅示量级。",
}
for t,txt in FILL.items():
    e=T[t]; e["today"]=txt
    for s in ("wb-api-pop","wb-api-urban"):
        if s not in e["sources"]: e["sources"].append(s)
    if "forest_pct" in txt and "wb-api-forest" not in e["sources"]: e["sources"].append("wb-api-forest")
    if "NV.AGR" in txt and "wb-api-agri" not in e["sources"]: e["sources"].append("wb-api-agri")
    # 修失实表述
    pn=e.get("pending_notes") or ""
    pn=pn.replace("数据可从 api.worldbank.org 按国家+指标复现","数据可从 api.worldbank.org 按「国家 ISO3 + 指标编号」复现（见 sources 中的 wb-api-* 端点）")
    e["pending_notes"]=pn+" 第25轮二次返工：正文已补指标编号；尼日利亚/美国城市化率此前因抓取脚本请求失败而缺失，已补实测值（非指标未返回）。"

for uu,d in docs.items(): json.dump(d,open(os.path.join(DATA,uu+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("A组修正完成；sources",len(json.load(open(P,encoding='utf-8'))['sources']))