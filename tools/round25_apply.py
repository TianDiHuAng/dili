# -*- coding: utf-8 -*-
"""第25轮：用世界银行 API 实测数值填充 today 段（标注年份+指标编号+口径说明）。"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
D=json.load(open(os.path.join(ROOT,"reports","round25_wb_data.json"),encoding="utf-8"))

def v(c,k):
    r=D.get(c,{}).get(k)
    return f"{r['value']:.1f}%（{r['year']} 年）" if r and k=="urban_pct" else (
           f"{int(r['value']):,}（{r['year']} 年）" if r and k=="pop_total" else None)

docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

FILL={
"城市化水平":("世界银行 API（指标 SP.URB.TOTL.IN.ZS，城市人口占总人口比例）2025 年：中国 "
    + (v("CHN","urban_pct") or "—") + "、印度 " + (v("IND","urban_pct") or "—")
    + "、巴西 " + (v("BRA","urban_pct") or "—") + "、尼日利亚 " + (v("NGA","urban_pct") or "—")
    + "、美国 " + (v("USA","urban_pct") or "—") + "。各国口径与统计年份不完全一致，跨国比较需注意定义差异。"),
"人口地理":("世界银行 API（指标 SP.POP.TOTL，总人口）2025 年：中国 "
    + (v("CHN","pop_total") or "—") + "、印度 " + (v("IND","pop_total") or "—")
    + "、美国 " + (v("USA","pop_total") or "—") + "、巴西 " + (v("BRA","pop_total") or "—")
    + "、尼日利亚 " + (v("NGA","pop_total") or "—") + "。数据按世界银行口径，可能与各国普查结果略有差异。"),
"拉丁美洲与加勒比区域发展":("以代表性国家为例，世界银行 API 2025 年：巴西城市化率 "
    + (v("BRA","urban_pct") or "—") + "、墨西哥 " + (v("MEX","urban_pct") or "—")
    + "；巴西总人口 " + (v("BRA","pop_total") or "—") + "、墨西哥 " + (v("MEX","pop_total") or "—")
    + "。区域内部差异大，本数据仅示量级，不代表区域整体。"),
"中东与北非区域发展":("以埃及为例，世界银行 API 2025 年：城市化率 " + (v("EGY","urban_pct") or "—")
    + "、总人口 " + (v("EGY","pop_total") or "—") + "；农业增加值占 GDP "
    + (f"{D['EGY']['agri_pct_gdp']['value']:.1f}%（{D['EGY']['agri_pct_gdp']['year']} 年）" if D.get('EGY',{}).get('agri_pct_gdp') else "—")
    + "。区域内产油国与进口国差异显著，不宜以单一国家代表全域。"),
"南亚区域发展":("以印度为例，世界银行 API 2025 年：城市化率 " + (v("IND","urban_pct") or "—")
    + "、总人口 " + (v("IND","pop_total") or "—") + "；森林覆盖率 "
    + (f"{D['IND']['forest_pct']['value']:.1f}%（{D['IND']['forest_pct']['year']} 年）" if D.get('IND',{}).get('forest_pct') else "—")
    + "。南亚各国差异大，本数据仅示量级。"),
}
n=0
for t,txt in FILL.items():
    e=T.get(t)
    if not e: continue
    e["today"]=txt
    if "wb-api-pop" not in e["sources"]: e["sources"].append("wb-api-pop")
    if "wb-api-urban" not in e["sources"]: e["sources"].append("wb-api-urban")
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第25轮现状数据】today 段已填入世界银行 API 实测值（含指标编号与年份），数据可从 api.worldbank.org 按国家+指标复现；"
      f"跨国比较的口径差异已在正文注明。").strip()
    e["last_update"]=TODAY;n+=1

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("填充 today 段",n,"条")
for t in FILL: print("\n--",t,"\n",T[t]["today"][:120],"...")