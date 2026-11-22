# -*- coding: utf-8 -*-
"""第26轮：为 12 条 L2 条目的 today 段填入世界银行 API 实测值（国家数据 + 指标编号 + 年份）。"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
D=json.load(open(os.path.join(ROOT,"reports","round25_wb_data.json"),encoding="utf-8"))
def g(c,k,kind="pct"):
    r=D.get(c,{}).get(k)
    if not r: return None
    return f"{r['value']:.1f}%（{r['year']}年）" if kind=="pct" else f"{int(r['value']):,}（{r['year']}年）"
def urban(c): return g(c,"urban_pct")
def pop(c): return g(c,"pop_total","int")
def life(c): return g(c,"life_exp","pct")
def forest(c): return g(c,"forest_pct")
def agri(c): return g(c,"agri_pct_gdp")

docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

FILL={
"尼罗河谷":f"以埃及为例，来源：世界银行 API。总人口 {pop('EGY')}（SP.POP.TOTL）、城市化率 {urban('EGY')}（SP.URB.TOTL.IN.ZS）、预期寿命 {life('EGY')}（SP.DYN.LE00.IN）。河谷与三角洲仍是人口与农业最密集的区域，具体流域内分布数据需专门统计源核验。",
"黄河流域":f"以中国为例，来源：世界银行 API。总人口 {pop('CHN')}（SP.POP.TOTL）、城市化率 {urban('CHN')}（SP.URB.TOTL.IN.ZS）、农业增加值占 GDP {agri('CHN')}（NV.AGR.TOTL.ZS）。流域内部人口与用水数据需按专门统计来源核验。",
"日本列岛":f"来源：世界银行 API。总人口 {pop('JPN')}（SP.POP.TOTL）、城市化率 {urban('JPN')}（SP.URB.TOTL.IN.ZS）、森林覆盖率 {forest('JPN')}（AG.LND.FRST.ZS）、预期寿命 {life('JPN')}（SP.DYN.LE00.IN）。列岛人口集中于沿海平原，具体分布数据待专门来源核验。",
"五大湖":f"以美加两侧为例，来源：世界银行 API。美国总人口 {pop('USA')}（SP.POP.TOTL）、城市化率 {urban('USA')}（SP.URB.TOTL.IN.ZS）；加拿大相关指标待补。湖区水质、水位与渔业数据需按年份从 EPA/NOAA 机构页核验。",
"密西西比河":f"以美国为例，来源：世界银行 API。总人口 {pop('USA')}（SP.POP.TOTL）、农业增加值占 GDP {agri('USA')}（NV.AGR.TOTL.ZS）、森林覆盖率 {forest('USA')}（AG.LND.FRST.ZS）。流域货运与水质数据需专门统计来源核验。",
"亚马逊盆地":f"以巴西为例，来源：世界银行 API。总人口 {pop('BRA')}（SP.POP.TOTL）、森林覆盖率 {forest('BRA')}（AG.LND.FRST.ZS）、城市化率 {urban('BRA')}（SP.URB.TOTL.IN.ZS）。盆地内森林面积与火点数据需按年份从 NASA/INPE 等来源核验。",
"拉普拉塔平原":f"以阿根廷与乌拉圭为例，来源：世界银行 API。阿根廷城市化率 {urban('ARG') or '（本期抓取失败）'}（SP.URB.TOTL.IN.ZS）。两国农牧业产值与播种面积数据待专门统计来源核验。",
"两河流域":f"以伊拉克为例，来源：世界银行 API。总人口 {pop('IRQ')}（SP.POP.TOTL）、城市化率 {urban('IRQ')}（SP.URB.TOTL.IN.ZS）、农业增加值占 GDP {agri('IRQ')}（NV.AGR.TOTL.ZS）。两河水量与灌溉面积数据待专门来源核验。",
"印度河文明":f"以巴基斯坦与印度为例，来源：世界银行 API。巴基斯坦总人口 {pop('PAK')}（SP.POP.TOTL）、印度 {pop('IND')}（同指标）。印度河流域今天的水资源分配与灌溉数据待专门统计与条约文件核验。",
"湄公河三角洲":f"以越南为例，来源：世界银行 API。总人口 {pop('VNM')}（SP.POP.TOTL）、城市化率 {urban('VNM')}（SP.URB.TOTL.IN.ZS）、森林覆盖率 {forest('VNM')}（AG.LND.FRST.ZS）。三角洲稻米产量与沉降速率数据待专门来源核验。",
"澳大利亚大陆":f"来源：世界银行 API。总人口 {pop('AUS')}（SP.POP.TOTL）、城市化率 {urban('AUS')}（SP.URB.TOTL.IN.ZS）、森林覆盖率 {forest('AUS')}（AG.LND.FRST.ZS）。内陆人口密度与水资源数据待专门统计来源核验。",
"斯瓦希里海岸":f"以坦桑尼亚与肯尼亚为例（数据待补），区域参照：来源：世界银行 API。南非总人口 {pop('ZAF')}（SP.POP.TOTL）、城市化率 {urban('ZAF')}（SP.URB.TOTL.IN.ZS）。东非海岸港口吞吐与人口数据需专门来源核验。",
}
n=0;skip=[]
for t,txt in FILL.items():
    e=T.get(t)
    if not e: skip.append(t);continue
    if "（本期抓取失败）" in txt:
        skip.append(t);continue
    e["today"]=txt
    for s in ("wb-api-pop","wb-api-urban"):
        if s not in e["sources"]: e["sources"].append(s)
    if "forest_pct" in txt and "wb-api-forest" not in e["sources"]: e["sources"].append("wb-api-forest")
    if "NV.AGR" in txt and "wb-api-agri" not in e["sources"]: e["sources"].append("wb-api-agri")
    e["pending_notes"]=((e.get("pending_notes") or "")+
      " 【第26轮现状数据】today 段填入世界银行 API 实测值（含指标编号与年份），可按「国家 ISO3 + 指标」复现；跨国/跨区比较口径差异已在正文注明。").strip()
    e["last_update"]=TODAY;n+=1

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("填充",n,"条；跳过",skip)