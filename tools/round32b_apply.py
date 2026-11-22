# -*- coding: utf-8 -*-
"""第32轮：升级 长江流域（Wikidata 长度）与 印度河文明（Wikidata 年代）为核心 L2。"""
import json,os,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]

P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}
NEW=[("wikidata-q5413","Wikidata Q5413 — Yangtze River","https://www.wikidata.org/wiki/Q5413",
   "英文描述「longest river in Asia and third-longest in the world」；P2043（长度）= 6300 千米（精度=1）。"),
 ("wikidata-q42534","Wikidata Q42534 — Indus Valley Civilization","https://www.wikidata.org/wiki/Q42534",
   "英文描述「Bronze Age civilisation in South Asia」；P580（起始）= 前3000年、P582（结束）= 前1800年（精度=年）。")]
for sid,title,url,desc in NEW:
    if sid in have: continue
    q=url.rsplit("/",1)[-1]
    code=200
    p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0","-o","-","-w","%{http_code}",
                      f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={q}&props=claims&format=json"],capture_output=True,timeout=35)
    code=int(p.stdout.decode("utf-8","ignore").strip()[-3:]) if p.stdout else 0
    sd["sources"].append({"id":sid,"title":title,"author":"Wikidata（Wikimedia 社区，CC0）","year":None,
      "type":"开放数据集","url":url,"url2":f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={q}&props=claims&format=json",
      "link_ok":bool(code==200),"verified":bool(code==200),"page_title":title,
      "note":f"{desc}；API 查询 HTTP {code}。众包数据，按 TASK 规则仅作双源之一。"})
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
C={
"长江流域":{
 "def":"长江流域：长江干流及其支流覆盖的区域，据 Wikidata 记录长江全长约 6300 千米，为亚洲最长河流。",
 "over":"长江干流及其支流覆盖的区域，据 Wikidata 记录长江全长约 6300 千米，为亚洲最长河流。",
 "geo":"流域自青藏高原发源，经四川盆地、长江中下游平原注入东海，跨越高原、盆地与平原多种地貌。水量丰沛、湖泊与支流众多，中下游形成密集水网与洪泛平原。",
 "infl":"水运条件降低大宗物资运输成本，冲积平原与稻作条件支撑人口密集。流域水利与国家治理互为条件，地理条件提供基础，制度与技术在决定性环节同样关键。",
 "pol":"本条不展开具体政权序列；流域内的政治整合与行政沿革待专门史学来源核验。",
 "conn":"通过大运河与黄河流域整合，通过长江口与沿海港口连接海上贸易网络，形成内陆—沿海双重联系。",
 "today":"以中国为例，来源：世界银行 API。总人口 1,406,585,000 人（2025年）（SP.POP.TOTL）、城市化率 66.3%（2025年）（SP.URB.TOTL.IN.ZS）、农业增加值占 GDP 6.7%（2025年）（NV.AGR.TOTL.ZS）。上述为全国口径，仅示量级；流域内人口、径流量与水质数据需专门统计与遥感来源核验。",
 "sources":["wikidata-q5413","fao-aquastat-basins","wb-chn-pop","wb-chn-urban","wb-chn-agri"],
 "note":"第32轮升级：河长数据（约6300千米）来自 Wikidata Q5413 的 P2043（精度=1千米）；FAO AQUASTAT 流域目录页作机构背景、世界银行作现状数据。流域内具体数据待专门来源核验。"},
"印度河文明":{
 "def":"印度河文明：南亚青铜时代文明，据 Wikidata 记录约为公元前 3000 年至前 1800 年。",
 "over":"南亚青铜时代文明，据 Wikidata 记录约为公元前 3000 年至前 1800 年。",
 "geo":"分布于印度河及其支流沿岸的冲积平原，另有季节河与沿海遗址。季风降水与河流洪水共同塑造农业条件，洪水既带来肥沃沉积物也要求排水与防洪安排。",
 "infl":"河流灌溉支撑城市与人口集中，城市规划与排水设施反映较高的组织能力。文明衰落的原因存在多种解释（气候干旱、河流改道、贸易变化），学界尚无定论。",
 "pol":"据 Wikidata 记录，该文明约为前 3000 年至前 1800 年（精度=年）；学界对起始与成熟期年代有不同表述。是否形成统一国家尚无定论，城市体系的治理形态待专门考古研究核验。",
 "conn":"通过海上与陆路与美索不达米亚、中亚及印度洋沿岸交换铜、棉织品与奢侈品，是早期跨区域贸易网络的一环。",
 "today":"以巴基斯坦与印度为例，来源：世界银行 API。巴基斯坦总人口 251,269,164 人（2025年）（SP.POP.TOTL）、印度 1,463,865,525 人（同指标）。上述为两国全国口径，仅示量级；印度河流域今天的水资源分配与灌溉数据需专门统计与条约文件核验。",
 "sources":["wikidata-q42534","s013-fao-org","wb-pak-pop","wb-ind-pop"],
 "note":"第32轮升级：年代（约前3000–前1800年）来自 Wikidata Q42534 的 P580/P582（精度=年）；FAO AQUASTAT 作机构背景、世界银行作现状端点。学界对年代上限与衰落原因有不同表述，已并列注明。"},
}
for t,c in C.items():
    e=T.get(t)
    if not e: continue
    e.update({"level":"L2","status":"L2完成(第32轮)-Wikidata",
      "definition":c["def"],"overview":c["over"],
      "time_or_place":("长江全长约6300千米（Wikidata P2043）" if t=="长江流域" else "约前3000年–前1800年（Wikidata P580/P582，精度=年）"),
      "geo":c["geo"],"influence":c["infl"],"polities":c["pol"],"connections":c["conn"],"today":c["today"],
      "sources":c["sources"],"needs_verification":True,"pending_notes":c["note"],"last_update":TODAY})
    e["svg"]=("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='示意图'>"
      "<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>"
      "<path d='M80 160 C 200 140 300 200 420 220 C 520 236 620 250 690 280' fill='none' stroke='var(--accent)' stroke-width='5'/>"
      + ("<path d='M300 200 C 330 250 360 300 380 350' fill='none' stroke='var(--accent2)' stroke-width='2' stroke-dasharray='6 4'/>"
         "<circle cx='120' cy='155' r='6' class='pt'/><text x='100' y='135' class='lbl'>源区</text>"
         "<circle cx='420' cy='220' r='6' class='pt'/><text x='400' y='200' class='lbl'>中游</text>"
         "<circle cx='680' cy='278' r='6' class='pt'/><text x='620' y='262' class='lbl'>入海</text>"
         if t=="长江流域" else
         "<path d='M200 120 L240 320' fill='none' stroke='var(--accent2)' stroke-width='4'/>"
         "<circle cx='240' cy='200' r='6' class='pt'/><text x='250' y='200' class='lbl'>河谷</text>"
         "<circle cx='460' cy='250' r='6' class='pt'/><text x='470' y='250' class='lbl'>平原</text>")
      +f"<text x='40' y='370' class='dim'>{t} · 简笔示意，非精确测绘</text></svg>")

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
import collections
print(collections.Counter((e["tier"],e["level"]) for e in T.values()))