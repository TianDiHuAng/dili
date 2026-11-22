# -*- coding: utf-8 -*-
"""第3轮二次返工：来源不足的5条L2降级为L1，保留可支撑的最小定义。"""
import json, os, sys, re, html, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]

# 新增 EPA 大湖专题来源（curl 核验）
u="https://www.epa.gov/greatlakes"
p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",u],capture_output=True,timeout=30)
raw=p.stdout.decode("utf-8","ignore")
code=0;pt=None
if "__HTTP__" in raw:
    b,c=raw.rsplit("\n__HTTP__",1);code=int(c.strip())
    m=re.search(r"<title[^>]*>(.*?)</title>",b,re.I|re.S)
    pt=re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>","",m.group(1)))).strip() if m else None
sp=os.path.join(DATA,"sources.json")
doc=json.load(open(sp,encoding="utf-8"))
if not any(s["id"]=="epa-great-lakes" for s in doc["sources"]):
    doc["sources"].append({"id":"epa-great-lakes","title":"The Great Lakes","author":"US EPA","year":None,
      "type":"官方机构","url":u,"url2":None,"link_ok":True if code==200 else False,
      "verified":bool(code==200 and pt),"page_title":pt,
      "note":f"curl 实测 HTTP {code}；页面标题：{pt}；年份未标注。"})
    json.dump(doc,open(sp,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

# L2 -> L1 降级
DOWN={
"尼罗河三角洲":(
 "尼罗河三角洲：尼罗河入地中海处的冲积平原，地势低平、水网密布，是埃及重要农业区。",
 ["fao-aquastat-basins","br-nile"],
 "二次返工：专题来源不足，五段深度内容降级为 L1；三角洲演化年代、盐水入侵与海平面风险待专门来源核验。"),
"长江流域":(
 "长江流域：长江干流及其支流覆盖的广阔区域，水网密集，是重要农业与城市密集区。",
 ["fao-aquastat-basins","s022-ourworldindata-org"],
 "二次返工：专题来源不足，五段深度内容降级为 L1；稻作起源、经济重心南移与运河史待专门来源核验。"),
"阿尔卑斯山":(
 "阿尔卑斯山：横贯中欧的山地系统，河谷与山口影响区域交通。",
 ["s056-earthquake-usgs-gov","s038-earthobservatory-nasa-gov"],
 "二次返工：移除欧洲最高山脉表述并降级为 L1；山地形成年代、冰川与垂直气候带待专题来源核验。"),
"五大湖":(
 "五大湖：北美中东部的淡水湖群，通过圣劳伦斯河与大西洋相连。",
 ["epa-great-lakes","noaa-glerl"],
 "二次返工：降级为 L1；航道、工业带与美加边界专题来源待补。"),
"南极半岛":(
 "南极半岛：南极大陆向北伸出的半岛，靠近南美洲。",
 ["s038-earthobservatory-nasa-gov","s049-ncei-noaa-gov"],
 "二次返工：移除科考站密集与气温温和表述并降级为 L1；半岛地质与生态专题来源待补。"),
}

docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
done=[]
for d in docs.values():
    for e in d["entries"]:
        if e["title"] in DOWN:
            definition,sources,note=DOWN[e["title"]]
            for k in ["geo","influence","polities","connections","today","svg"]:
                e.pop(k,None)
            e.update({"level":"L1","status":"二次返工降级L1(第3轮)","definition":definition,
                      "overview":definition.split("：",1)[1],"sources":sources,
                      "needs_verification":True,"pending_notes":note,"last_update":TODAY})
            done.append(e["title"])
for u,d in docs.items():
    json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("EPA",code,pt)
print("降级",len(done),"条：","、".join(done))
