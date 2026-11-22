# -*- coding: utf-8 -*-
"""第29轮返工：宋代回退、澳/日建专用端点、共享端点退役、措辞。"""
import json,os,re,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

# 1) 宋代回退
song=T["宋代"]
song["status"]="已复核(第29轮·非实证)"
song["pending_notes"]=("【第29轮·非实证复核】实测 britannica-regions（UNSD M49 国别清单页）=200/正文 137675 字符/"
  "正则 han|song|china 命中 12，但**逐词核对为噪声**：han 的命中全部来自 Handbook / Ghana / Afghanistan，"
  "china 为国名，song=0、宋=0、dynasty=0；wikipedia-regions（UN SDG 门户）=200/正文 5 字符/命中 0。"
  "按 D071（别名页命中不计达标），本条**不构成实证复核、不判达标**。"
  "本环境内可达的宋代专题页（Britannica/Met/Wikipedia 中文站）均 403 或连接失败，待找到可达机构专题页后用 song|宋 重测命中≥3 方可恢复。")

# 2) 澳/日专用端点
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}
MET={"pop":"SP.POP.TOTL","urban":"SP.URB.TOTL.IN.ZS","life":"SP.DYN.LE00.IN","forest":"AG.LND.FRST.ZS"}
LABEL={"pop":"总人口","urban":"城市化率","life":"预期寿命","forest":"森林覆盖率"}
CNM={"AUS":"澳大利亚","JPN":"日本"}
add=0
for iso,mks in (("AUS",["pop","urban","forest"]),("JPN",["pop","urban","life","forest"])):
    for mk in mks:
        sid=f"wb-{iso.lower()}-{mk}"
        if sid in have: continue
        url=f"https://api.worldbank.org/v2/country/{iso}/indicator/{MET[mk]}?format=json&per_page=100&date=2015:2025"
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-o","-","-w","\n__HTTP__%{http_code}",url],capture_output=True,timeout=35)
        raw=p.stdout.decode("utf-8","ignore"); b,c=raw.rsplit("\n__HTTP__",1); code=int(c.strip() or 0)
        val=yr=None
        try:
            d=json.loads(b); rows=[r for r in d[1] if r.get("value") is not None]
            if rows: L=max(rows,key=lambda r:int(r["date"])); val=L["value"]; yr=L["date"]
        except Exception: pass
        sd["sources"].append({"id":sid,"title":f"World Bank API — {LABEL[mk]} ({MET[mk]}, {CNM[iso]})",
          "author":"World Bank","year":None,"type":"数据端点","url":url,"url2":None,
          "link_ok":bool(code==200),"verified":bool(code==200),
          "page_title":f"World Bank API — {LABEL[mk]} ({MET[mk]}, {CNM[iso]})",
          "note":f"JSON API {code}；国家 {iso}（{CNM[iso]}）＋指标 {MET[mk]}；最新值 {val}（{yr} 年）。"})
        add+=1
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("新增端点",add)

# 3) 替换共享端点为专用端点 + 补国名
SHARED={"wb-api-pop","wb-api-urban","wb-api-life","wb-api-forest","wb-api-agri"}
SUBS={"澳大利亚大陆":["wb-aus-pop","wb-aus-urban","wb-aus-forest"],
      "日本列岛":["wb-jpn-pop","wb-jpn-urban","wb-jpn-life","wb-jpn-forest"]}
for t,spec in SUBS.items():
    e=T.get(t)
    if not e: continue
    e["sources"]=[s for s in e["sources"] if s not in SHARED]
    for s in spec:
        if s not in e["sources"]: e["sources"].append(s)
    tod=e.get("today") or ""
    if "澳大利亚大陆"==t and "澳大利亚" not in tod.split("。")[0]:
        tod="以澳大利亚为例，" + tod
    if "日本列岛"==t and "日本" not in tod.split("。")[0]:
        tod="以日本为例，" + tod
    e["today"]=tod
    e["pending_notes"]=((e.get("pending_notes") or "")+
      " 【第29轮返工】来源端点由共享 wb-api-*（固定 CHN/WLD）替换为国别专用端点（D072），today 补写代表国名。").strip()
    e["last_update"]=TODAY

# 4) 措辞：两国数据
for t in ("拉普拉塔平原","印度河文明"):
    e=T.get(t)
    if not e: continue
    e["today"]=(e.get("today") or "").replace("上述为该代表国的全国口径数据","上述为两国全国口径数据")

# 5) 共享端点退役说明
sd=json.load(open(P,encoding="utf-8"))
for s in sd["sources"]:
    if s["id"] in SHARED:
        s["note"]=(s.get("note") or "")+" 【第29轮退役】本端点为「指标级样例」且 URL 固定指向单一国家（CHN/BRA/EGY/WLD），"
        "已由国别专用端点（wb-{iso3}-{metric}）取代，不再用于任何条文（D072）。"
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
# 残留共享端点统计
res=[(e["title"],[s for s in e["sources"] if s in SHARED]) for e in T.values() if any(s in SHARED for s in e["sources"])]
print("仍挂共享端点的条目:",res)