# -*- coding: utf-8 -*-
"""第28轮返工 R1：为 today 中出现的 (国家, 指标) 生成专用端点并替换引用。"""
import json,os,re,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:d for d in docs.values() for e in d["entries"]}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
D=json.load(open(os.path.join(ROOT,"reports","round25_wb_data.json"),encoding="utf-8"))

CN2ISO={v:k for k,v in {
 "CHN":"中国","IND":"印度","NGA":"尼日利亚","BRA":"巴西","USA":"美国","EGY":"埃及","IDN":"印度尼西亚",
 "JPN":"日本","IRQ":"伊拉克","PAK":"巴基斯坦","VNM":"越南","AUS":"澳大利亚","DZA":"阿尔及利亚",
 "ZAF":"南非","TUR":"土耳其","DEU":"德国","FRA":"法国","RUS":"俄罗斯","TZA":"坦桑尼亚","KEN":"肯尼亚",
 "ARG":"阿根廷","URY":"乌拉圭","CAN":"加拿大","TUN":"突尼斯","IRN":"伊朗","GRC":"希腊","ITA":"意大利",
 "GBR":"英国","NOR":"挪威","GTM":"危地马拉","MEX":"墨西哥","PER":"秘鲁","CHL":"智利","NZL":"新西兰",
 "FJI":"斐济","ETH":"埃塞俄比亚","MLI":"马里","KAZ":"哈萨克斯坦","KOR":"韩国","COD":"刚果民主共和国",
 "UZB":"乌兹别克斯坦","GRL":"格陵兰","PNG":"巴布亚新几内亚","NER":"尼日尔","SEN":"塞内加尔",
 "GHA":"加纳","TCD":"乍得","MNG":"蒙古","BGD":"孟加拉国","LKA":"斯里兰卡","NPL":"尼泊尔","WLD":"全球"}.items()}
IND={"SP.POP.TOTL":"pop","SP.URB.TOTL.IN.ZS":"urban","SP.DYN.LE00.IN":"life",
     "AG.LND.FRST.ZS":"forest","NV.AGR.TOTL.ZS":"agri"}
LABEL={"pop":"总人口","urban":"城市化率","life":"预期寿命","forest":"森林覆盖率","agri":"农业增加值占 GDP"}

# 1) 解析每条 today 的 (国家, 指标) 对
need={}   # (iso, metric) -> set of acronyms
for t,e in T.items():
    tod=e.get("today") or ""
    if "来源：世界银行 API" not in tod: continue
    # 找该条最早出现的国家名
    isos=[iso for name,iso in CN2ISO.items() if name in tod]
    for ind,mk in IND.items():
        if ind in tod:
            for iso in isos:
                need.setdefault((iso,mk),set()).add(t)

print("需生成端点组合:",len(need))

# 2) 登记端点（含核验）
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"))
have={s["id"] for s in sd["sources"]}
added=0
MET={"pop":"SP.POP.TOTL","urban":"SP.URB.TOTL.IN.ZS","life":"SP.DYN.LE00.IN",
     "forest":"AG.LND.FRST.ZS","agri":"NV.AGR.TOTL.ZS"}
for (iso,mk),titles in sorted(need.items()):
    sid=f"wb-{iso.lower()}-{mk}"
    if sid in have: continue
    url=f"https://api.worldbank.org/v2/country/{iso}/indicator/{MET[mk]}?format=json&per_page=100&date=2015:2025"
    p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25",url],capture_output=True,timeout=35)
    raw=p.stdout.decode("utf-8","ignore")
    code=0
    try:
        d=json.loads(raw); code=200 if isinstance(d,list) and len(d)>1 else 0
    except Exception: code=0
    val=None; yr=None
    try:
        rows=[r for r in d[1] if r.get("value") is not None]
        if rows:
            L=max(rows,key=lambda r:int(r["date"])); val=L["value"]; yr=L["date"]
    except Exception: pass
    sd["sources"].append({"id":sid,
      "title":f"World Bank API — {LABEL[mk]} ({MET[mk]}, {CN2ISO.get(iso,iso)})",
      "author":"World Bank","year":None,"type":"数据端点","url":url,"url2":None,
      "link_ok":bool(code==200),"verified":bool(code==200),
      "page_title":f"World Bank API — {LABEL[mk]} ({MET[mk]}, {CN2ISO.get(iso,iso)})",
      "note":f"JSON API {code}；国家/聚合 {iso}（{CN2ISO.get(iso,iso)}）＋指标 {MET[mk]}；最新值 {val}（{yr} 年）。本条专用端点，读者点开即为正文所述国家/指标。"})
    added+=1
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("新增专用端点",added)

# 3) 替换引用：去掉共享 wb-api-*，换成该条实际用到的专用端点
SHARED={"wb-api-pop","wb-api-urban","wb-api-life","wb-api-forest","wb-api-agri"}
fixed=0
for t,e in T.items():
    tod=e.get("today") or ""
    if "来源：世界银行 API" not in tod: continue
    isos=[iso for name,iso in CN2ISO.items() if name in tod]
    spec=[f"wb-{iso.lower()}-{mk}" for ind,mk in IND.items() if ind in tod for iso in isos]
    spec=list(dict.fromkeys(spec))
    if not spec: continue
    newsrc=[s for s in e["sources"] if s not in SHARED]
    for s in spec:
        if s not in newsrc: newsrc.append(s)
    if newsrc!=e["sources"]:
        e["sources"]=newsrc
        e["pending_notes"]=(e.get("pending_notes") or "").replace("DN068","D068")
        e["last_update"]=TODAY;fixed+=1
for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("替换引用",fixed,"条")