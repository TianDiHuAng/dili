# -*- coding: utf-8 -*-
"""第27轮：16 条 L2 的 today 填世界银行实测值（严格区域—国家匹配、单位正确、含指标编号）。"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
D=json.load(open(os.path.join(ROOT,"reports","round25_wb_data.json"),encoding="utf-8"))
CN={"EGY":"埃及","DZA":"阿尔及利亚","TUN":"突尼斯","IRQ":"伊拉克","IRN":"伊朗","CHN":"中国","GRC":"希腊",
 "ITA":"意大利","GBR":"英国","NOR":"挪威","USA":"美国","GTM":"危地马拉","MEX":"墨西哥","PER":"秘鲁",
 "CHL":"智利","BRA":"巴西","NZL":"新西兰","FJI":"斐济","MLI":"马里","ETH":"埃塞俄比亚","WLD":"全球"}
def f(c,k):
    r=D.get(c,{}).get(k)
    if not r: return None
    if k=="pop_total": return f"{int(r['value']):,}（{r['year']}年）"
    if k=="life_exp": return f"{r['value']:.1f} 岁（{r['year']}年）"
    return f"{r['value']:.1f}%（{r['year']}年）"
def seg(c,keys):
    out=[]
    for k,lab,ind in keys:
        v=f(c,k)
        if v: out.append(f"{lab} {v}（{ind}）")
    return "、".join(out)

P_POP=("pop_total","总人口","SP.POP.TOTL")
P_URB=("urban_pct","城市化率","SP.URB.TOTL.IN.ZS")
P_LIFE=("life_exp","预期寿命","SP.DYN.LE00.IN")
P_FRST=("forest_pct","森林覆盖率","AG.LND.FRST.ZS")
P_AGR=("agri_pct_gdp","农业增加值占 GDP","NV.AGR.TOTL.ZS")

FILL={
"撒哈拉沙漠":(f"以阿尔及利亚与埃及为例，来源：世界银行 API。{CN['DZA']} {seg('DZA',[P_POP,P_URB])}；{CN['EGY']} {seg('EGY',[P_POP,P_URB])}。沙哈拉腹地人口稀少，两国人口集中于沿海与河谷；沙漠区内人口与绿洲面积数据待遥感与专门统计核验。",["DZA","EGY"]),
"古埃及早王朝":(f"以埃及为例，来源：世界银行 API。{seg('EGY',[P_POP,P_URB,P_LIFE])}。早期王朝时期的遗址保护与考古研究现状需专门来源核验。",["EGY"]),
"古埃及古王国":(f"以埃及为例，来源：世界银行 API。{seg('EGY',[P_POP,P_LIFE])}。金字塔区遗址保护与游客数据待专门来源核验。",["EGY"]),
"迦太基":(f"以突尼斯为例，来源：世界银行 API。{seg('TUN',[P_POP,P_URB,P_LIFE])}。迦太基遗址位于今突尼斯境内，遗产保护与游客数据待核验。",["TUN"]),
"两河流域":(f"以伊拉克为例，来源：世界银行 API。{seg('IRQ',[P_POP,P_URB,P_AGR])}。两河水量分配与灌溉面积数据待专门统计与流域机构核验。",["IRQ"]),
"苏美尔城邦":(f"以伊拉克为例，来源：世界银行 API。{seg('IRQ',[P_POP,P_URB])}。南部遗址群保护状况与考古进展待专门来源核验。",["IRQ"]),
"阿卡德帝国":(f"以伊拉克为例，来源：世界银行 API。{seg('IRQ',[P_POP,P_AGR])}。相关遗址与文献释读进展待专门来源核验。",["IRQ"]),
"阿契美尼德波斯":(f"以伊朗为例，来源：世界银行 API。{seg('IRN',[P_POP,P_URB,P_LIFE])}。波斯波利斯等遗址保护与游客数据待核验。",["IRN"]),
"宋代":(f"以中国为例，来源：世界银行 API。{seg('CHN',[P_POP,P_URB,P_AGR])}。宋代经济与人口数据的现代重建属史学议题，需专门研究核验。",["CHN"]),
"爱琴海世界":(f"以希腊为例，来源：世界银行 API。{seg('GRC',[P_POP,P_URB,P_LIFE])}。爱琴海岛屿的人口与旅游数据待专门统计核验。",["GRC"]),
"克里特文明":(f"以希腊为例，来源：世界银行 API。{seg('GRC',[P_POP,P_URB])}。克里特岛遗址保护与游客数据待核验。",["GRC"]),
"古希腊城邦":(f"以希腊为例，来源：世界银行 API。{seg('GRC',[P_POP,P_URB,P_LIFE])}。古典时期人口规模的估计属史学争论，需专门研究核验。",["GRC"]),
"罗马共和国":(f"以意大利为例，来源：世界银行 API。{seg('ITA',[P_POP,P_URB,P_LIFE])}。罗马城遗址与遗产旅游数据待核验。",["ITA"]),
"文艺复兴意大利":(f"以意大利为例，来源：世界银行 API。{seg('ITA',[P_POP,P_URB,P_LIFE])}。北部城市带仍是制造业与文化中心；具体游客与经济数据待核验。",["ITA"]),
"不列颠群岛":(f"以英国为例，来源：世界银行 API。{seg('GBR',[P_POP,P_URB,P_LIFE])}。爱尔兰相关指标待补；群岛内港口货运数据需专门统计核验。",["GBR"]),
"维京时代":(f"以挪威为例，来源：世界银行 API。{seg('NOR',[P_POP,P_URB,P_LIFE])}。北欧各国差异明显，本数据仅示量级。",["NOR"]),
}
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
n=0;skip=[]
for t,(txt,cs) in FILL.items():
    e=T.get(t)
    if not e: skip.append(t);continue
    e["today"]=txt
    for s in ("wb-api-pop","wb-api-urban"):
        if s not in e["sources"]: e["sources"].append(s)
    if "SP.DYN" in txt and "wb-api-life" not in e["sources"]:
        pass  # 寿命用 wb-api-pop 端点涵盖？否，需独立端点
    if "AG.LND" in txt and "wb-api-forest" not in e["sources"]: e["sources"].append("wb-api-forest")
    if "NV.AGR" in txt and "wb-api-agri" not in e["sources"]: e["sources"].append("wb-api-agri")
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第27轮现状数据】today 段填入世界银行 API 实测值（代表国：{'、'.join(CN[c] for c in cs)}），含指标编号与年份；国家与条目区域已逐一核对（D068）。").strip()
    e["last_update"]=TODAY;n+=1
# 登记 life_exp 端点
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))
if not any(s["id"]=="wb-api-life" for s in sd["sources"]):
    sd["sources"].append({"id":"wb-api-life","title":"World Bank Indicator API — Life expectancy at birth (SP.DYN.LE00.IN)",
      "author":"World Bank","year":None,"type":"数据端点",
      "url":"https://api.worldbank.org/v2/country/WLD/indicator/SP.DYN.LE00.IN?format=json&per_page=100&date=2015:2025",
      "url2":None,"link_ok":True,"verified":True,"page_title":"World Bank Indicator API — Life expectancy at birth",
      "note":"JSON API 200；返回逐年出生时预期寿命（**单位为年，非百分比**）；正则为 life|value。全球 2024 年 73.48 岁。"})
    json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
# 给含寿命的条目挂 wb-api-life
for t,e in T.items():
    if "SP.DYN.LE00.IN" in (e.get("today") or "") and "wb-api-life" not in e["sources"]:
        e["sources"].append("wb-api-life")
for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("填充",n,"条；跳过",skip)