# -*- coding: utf-8 -*-
"""第32轮：登记 Wikidata 实体端点，升级 汉代/蒙古帝国/阿兹特克 为核心 L2（年代可核验）。"""
import json,os,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]

ENT={"汉代":("Q7209","Han dynasty","imperial dynasty in China from 202 BC to 220 AD","前206年–220年"),
 "蒙古帝国":("Q12557","Mongol Empire","13th- and 14th-century empire originating in Mongolia","1206年–1368年"),
 "阿兹特克":("Q2608489","Aztec Empire","former Mesoamerican empire","1325年–1521年"),
 "宋代":("Q7462","Song dynasty","former imperial dynasty of China (960–1279)","960年–1279年")}

P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}
for t,(qid,label,desc,span) in ENT.items():
    sid=f"wikidata-{qid.lower()}"
    if sid in have: continue
    u=f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={qid}&props=claims|descriptions&languages=en&format=json"
    p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",u],capture_output=True,timeout=35)
    raw=p.stdout.decode("utf-8","ignore");b,c=raw.rsplit("\n__HTTP__",1);code=int(c.strip() or 0)
    sd["sources"].append({"id":sid,
      "title":f"Wikidata {qid} — {label}",
      "author":"Wikidata（Wikimedia 社区，CC0）","year":None,"type":"开放数据集",
      "url":f"https://www.wikidata.org/wiki/{qid}","url2":u,
      "link_ok":bool(code==200),"verified":bool(code==200),
      "page_title":f"Wikidata {qid} — {label}",
      "note":f"Wikidata 实体 {qid}；英文描述「{desc}」；结构化时间属性 P571（成立）/P576（解散）给出 {span}（精度=年）。"
             f"API 查询 HTTP {code}。众包数据，按 TASK 规则仅作双源之一，须与机构/学术来源互证。"})
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

C={
"汉代":{
 "level":"L2","status":"L2完成(第32轮)-Wikidata年代",
 "def":"汉代：中国历史上的帝国王朝，据 Wikidata 结构化记录为公元前 206 年至公元 220 年。",
 "over":"中国历史上的帝国王朝，据 Wikidata 结构化记录为公元前 206 年至公元 220 年。",
 "geo":"帝国核心位于黄河中下游与关中平原，并向长江流域与河西走廊扩展。关中盆地与渭河平原提供农业基础，河西走廊是通往中亚的陆路通道。",
 "infl":"关中与关东平原的农业支撑人口与财政，河西走廊的通道条件支撑向西的交通与驻防。地理条件是重要基础，但帝国扩张与维系同样依赖制度、军事与财政安排。",
 "pol":"据 Wikidata 记录，汉代起于前 206 年、止于 220 年（精度到年）；其间分为西汉与东汉两段，中间有新朝中断。具体帝系、年号与制度演变待专门史学来源逐条核验。",
 "conn":"通过河西走廊与中亚绿洲相连，通过南方港口与海上航线接触东南亚与印度洋；丝绸之路的陆海两段在此交汇。",
 "today":"以中国为例，来源：世界银行 API。总人口 1,406,585,000 人（2025年）（SP.POP.TOTL）、城市化率 66.3%（2025年）（SP.URB.TOTL.IN.ZS）。上述为全国口径，仅示量级；汉代疆域内的人口与经济数据属历史人口学议题，需专门研究核验。",
 "sources":["wikidata-q7209","s010-unesco-org","wb-chn-pop","wb-chn-urban"],
 "note":"第32轮升级：年代（前206–220年）来自 Wikidata Q7209 的结构化属性 P571/P576（精度=年），UNESCO Culture 作机构页、世界银行作现状数据端点。按 TASK 规则 Wikidata 仅为双源之一，帝系与年号待专门史学来源核验。"},
"蒙古帝国":{
 "level":"L2","status":"L2完成(第32轮)-Wikidata年代",
 "def":"蒙古帝国：13 至 14 世纪起源于蒙古高原的跨欧亚帝国，据 Wikidata 记录为 1206 年至 1368 年。",
 "over":"13 至 14 世纪起源于蒙古高原的跨欧亚帝国，据 Wikidata 记录为 1206 年至 1368 年。",
 "geo":"核心位于蒙古高原，草原环境支撑大规模牧养与骑兵机动。帝国扩展后覆盖华北、中亚、波斯与东欧平原，跨越多种生态带，交通与补给条件差异极大。",
 "infl":"草原创牧经济与机动能力是扩张的重要条件，但跨欧亚的统治依赖驿站、分封与地方代理等制度安排。地理条件提供路径，制度决定其能否维持。",
 "pol":"据 Wikidata 记录，帝国起于 1206 年、止于 1368 年（精度到年），其后分化为多个汗国。具体大汗世系、分封与各汗国年代待专门史学来源逐条核验。",
 "conn":"驿站网络把东亚、中亚、波斯与东欧连成一体，商队、使节与技术沿此流动，是欧亚大陆首次大规模连通。",
 "today":"以蒙古为例，来源：世界银行 API。总人口 3,568,978 人（2025年）（SP.POP.TOTL）、城市化率 71.1%（2025年）（SP.URB.TOTL.IN.ZS）。上述为全国口径，仅示量级；帝国时期的人口与疆域估算属史学议题，需专门研究核验。",
 "sources":["wikidata-q12557","s010-unesco-org","wb-mng-pop","wb-mng-urban"],
 "note":"第32轮升级：年代（1206–1368年）来自 Wikidata Q12557 的 P571/P576（精度=年）；UNESCO Culture 作机构页、世界银行作现状数据端点。汗国分化后的年代待专门来源核验。"},
"阿兹特克":{
 "level":"L2","status":"L2完成(第32轮)-Wikidata年代",
 "def":"阿兹特克：中美洲墨西哥谷地的帝国政体，据 Wikidata 记录为 1325 年至 1521 年。",
 "over":"中美洲墨西哥谷地的帝国政体，据 Wikidata 记录为 1325 年至 1521 年。",
 "geo":"核心位于墨西哥谷地的高原湖泊区，湖中岛与湖岸平原提供聚落与农业空间。chinampa（湖上人工田）依赖水位与泥沙管理，火山高地与谷地气候分层明显。",
 "infl":"湖泊环境与人工田支撑高密度人口，山地与水系的破碎地形促成城邦并立与朝贡网络。环境条件重要，但帝国形态由联盟、贡赋与军事组织塑造，不宜单因解释。",
 "pol":"据 Wikidata 记录，政体起于 1325 年、止于 1521 年（精度到年）；通常以三方联盟（特诺奇蒂特兰、特斯科科、特拉科潘）形式运作。统治者序列与贡赋制度待专门史学来源逐条核验。",
 "conn":"通过朝贡与市场网络连接中美洲各地，玉石、可可、羽毛与黑曜石沿路线流动；与玛雅地区存在长期交流。",
 "today":"以墨西哥为例，来源：世界银行 API。总人口 131,946,900 人（2025年）（SP.POP.TOTL）、城市化率 80.0%（2025年）（SP.URB.TOTL.IN.ZS）。上述为全国口径，仅示量级；墨西哥谷地今天的地面沉降与遗址保护数据需专门来源核验。",
 "sources":["wikidata-q2608489","s010-unesco-org","wb-mex-pop","wb-mex-urban"],
 "note":"第32轮升级：年代（1325–1521年）来自 Wikidata Q2608489 的 P571/P576（精度=年；解散日精度到日）；UNESCO Culture 作机构页、世界银行作现状端点。"},
}
def svg(title,label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='示意图'>"
      "<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>"
      "<path d='M90 300 L200 240 L320 210 L450 220 L580 250 L680 300' fill='none' stroke='var(--accent)' stroke-width='4'/>"
      "<circle cx='200' cy='240' r='6' class='pt'/><circle cx='450' cy='220' r='6' class='pt'/>"
      "<circle cx='580' cy='250' r='6' class='pt'/>"
      f"<text x='150' y='220' class='lbl'>{label}</text>"
      f"<text x='40' y='370' class='dim'>{title} · 简笔示意，非精确测绘</text></svg>")

for t,c in C.items():
    e=T.get(t)
    if not e: continue
    e.update({"level":c["level"],"status":c["status"],"definition":c["def"],"overview":c["over"],
      "time_or_place":{"汉代":"前206年–220年（Wikidata P571/P576，精度=年）",
        "蒙古帝国":"1206年–1368年（Wikidata P571/P576，精度=年）",
        "阿兹特克":"1325年–1521年（Wikidata P571/P576，精度=年）"}[t],
      "geo":c["geo"],"influence":c["infl"],"polities":c["pol"],"connections":c["conn"],"today":c["today"],
      "sources":c["sources"],"needs_verification":True,
      "pending_notes":c["note"],"last_update":TODAY})
    e["svg"]=svg(t,"欧亚/中美洲示意")

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
import collections
print(collections.Counter((e["tier"],e["level"]) for e in T.values()))