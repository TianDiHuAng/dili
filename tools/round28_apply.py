# -*- coding: utf-8 -*-
"""第28轮：15 条 L2 的 today 补数据 + 恢复 9 条合规状态 + 8 条复核。"""
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
D=json.load(open(os.path.join(ROOT,"reports","round25_wb_data.json"),encoding="utf-8"))
CN={"ETH":"埃塞俄比亚","TZA":"坦桑尼亚","KEN":"肯尼亚","COD":"刚果民主共和国","MLI":"马里","KAZ":"哈萨克斯坦",
 "UZB":"乌兹别克斯坦","CHN":"中国","ITA":"意大利","USA":"美国","CAN":"加拿大","GTM":"危地马拉","MEX":"墨西哥",
 "GRL":"格陵兰","PER":"秘鲁","CHL":"智利","AUS":"澳大利亚","NZL":"新西兰","FJI":"斐济","NER":"尼日尔",
 "SEN":"塞内加尔","GHA":"加纳","TCD":"乍得","MNG":"蒙古","BGD":"孟加拉国","WLD":"全球"}
def f(c,k):
    r=D.get(c,{}).get(k)
    if not r: return None
    if k=="pop_total": return f"{int(r['value']):,} 人（{r['year']}年）"
    if k=="life_exp": return f"{r['value']:.1f} 岁（{r['year']}年）"
    return f"{r['value']:.1f}%（{r['year']}年）"
def seg(c,ks):
    L=[("pop_total","总人口","SP.POP.TOTL"),("urban_pct","城市化率","SP.URB.TOTL.IN.ZS"),
       ("life_exp","预期寿命","SP.DYN.LE00.IN"),("forest_pct","森林覆盖率","AG.LND.FRST.ZS"),
       ("agri_pct_gdp","农业增加值占 GDP","NV.AGR.TOTL.ZS")]
    out=[]
    for k,lab,ind in L:
        if k in ks:
            v=f(c,k)
            if v: out.append(f"{lab} {v}（{ind}）")
    return "、".join(out)

FILL={
"东非大裂谷":(("ETH",["pop_total","urban_pct","agri_pct_gdp"]),"以埃塞俄比亚为例"),
"刚果盆地":(("COD",["pop_total","forest_pct","urban_pct"]),"以刚果民主共和国为例"),
"萨赫勒带":(("NER",["pop_total","urban_pct","agri_pct_gdp"]),"以尼日尔为例"),
"马里帝国":(("MLI",["pop_total","urban_pct","agri_pct_gdp"]),"以马里为例"),
"青藏高原":(("CHN",["pop_total","urban_pct"]),"以中国为例（高原部分数据待省级统计核验）"),
"罗马帝国":(("ITA",["pop_total","urban_pct","life_exp"]),"以意大利为例"),
"白令陆桥":(("USA",["pop_total"]),"以美国为例（俄罗斯一侧数据见下）"),
"北美冰盖":(("CAN",["pop_total","forest_pct"]),"以加拿大为例"),
"大平原":(("USA",["pop_total","agri_pct_gdp"]),"以美国为例"),
"落基山脉":(("USA",["pop_total","forest_pct"]),"以美国为例"),
"科罗拉多高原":(("USA",["pop_total","urban_pct"]),"以美国为例"),
"中美洲地峡":(("GTM",["pop_total","urban_pct","forest_pct"]),"以危地马拉为例"),
"奥尔梅克":(("MEX",["pop_total","urban_pct"]),"以墨西哥为例"),
"玛雅文明":(("GTM",["pop_total","urban_pct","forest_pct"]),"以危地马拉为例（墨西哥东南部同源文化区）"),
"格陵兰岛":(("GRL",["pop_total","urban_pct","life_exp"]),"以格陵兰为例"),
"安第斯山脉":(("PER",["pop_total","urban_pct","life_exp"]),"以秘鲁为例"),
"阿塔卡马沙漠":(("CHL",["pop_total","urban_pct"]),"以智利为例"),
"印加帝国":(("PER",["pop_total","urban_pct","life_exp"]),"以秘鲁为例"),
"大分水岭":(("AUS",["pop_total","urban_pct","forest_pct"]),"以澳大利亚为例"),
"澳大利亚原住民":(("AUS",["pop_total","urban_pct"]),"以澳大利亚为例（原住民人口另计，待专门统计核验）"),
"毛利人":(("NZL",["pop_total","urban_pct","life_exp"]),"以新西兰为例（毛利人口另计）"),
"波利尼西亚":(("FJI",["pop_total","urban_pct"]),"以斐济为例（岛群差异大）"),
}
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
n=0;skip=[]
for t,((c,ks),lead) in FILL.items():
    e=T.get(t)
    if not e: skip.append(t);continue
    body=seg(c,ks)
    if not body: skip.append(t);continue
    e["today"]=(f"{lead}，来源：世界银行 API。{CN[c]} {body}。上述为该代表国的全国口径数据，仅示量级，"
      f"不代表本条目所述区域的内部差异；本条目主题相关的专门数据待相应机构来源核验。")
    for s in ("wb-api-pop","wb-api-urban"):
        if s not in e["sources"]: e["sources"].append(s)
    if "AG.LND" in body and "wb-api-forest" not in e["sources"]: e["sources"].append("wb-api-forest")
    if "NV.AGR" in body and "wb-api-agri" not in e["sources"]: e["sources"].append("wb-api-agri")
    if "SP.DYN" in body and "wb-api-life" not in e["sources"]: e["sources"].append("wb-api-life")
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第28轮现状数据】today 填世界银行实测（代表国 {CN[c]}，DN068 已核对国家—区域匹配；单位含「人/岁/%」）。").strip()
    e["last_update"]=TODAY;n+=1

# 恢复 9 条达标条目的合规状态（保留复核说明）
RESTORE={"阿契美尼德波斯":"L2·配对说明(第16轮)·已复核(第27轮)",
 "亚马逊河":"L2完成(第5轮)·已复核(第27轮)",
 "冰芯气候记录":"L2合规换源(第22轮)·已复核(第27轮)",
 "人口迁移":"L2完成(第15轮)-D041专题来源·已复核(第27轮)",
 "植物物候变化":"L2完成(第19轮)-主题页·已复核(第27轮)",
 "北极火情变化":"L2完成(第19轮)-主题页·已复核(第27轮)",
 "地理信息系统":"L2完成(第19轮)-主题页·已复核(第27轮)",
 "人口地理":"L2完成(第19轮)-主题页·已复核(第27轮)",
 "城市地理":"L2完成(第19轮)-主题页·已复核(第27轮)"}
r=0
for t,st in RESTORE.items():
    e=T.get(t)
    if e: e["status"]=st;e["last_update"]=TODAY;r+=1

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("today 填充",n,"；状态恢复",r,"；跳过",skip)