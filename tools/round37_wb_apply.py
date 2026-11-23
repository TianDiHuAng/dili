# -*- coding: utf-8 -*-
"""第37轮：世行指标类 9 条补充条目 → L2。"""
import json,os,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
W=json.load(open(os.path.join(ROOT,"reports","round37_wb.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}
AGGN={"WLD":"全球","EAS":"东亚与太平洋","LCN":"拉丁美洲与加勒比","MEA":"中东与北非","SAS":"南亚"}

def disp(name):
    d=W[name];v=float(d["value"]);c=d["code"]
    if c=="SP.POP.TOTL": return f"{int(v):,} 人"
    if c=="AG.PRD.CREL.MT": return f"{v:,.0f} 吨"
    return f"{v:.1f}%"

BODY={
"森林覆盖变化":("森林覆盖变化：森林面积在时间上的增减及其空间分布。",
 "高覆盖率集中于热带雨林（亚马孙、刚果盆地、东南亚）与北方针叶林带；净减少的热点长期在热带，温带则因农业退耕有局部恢复。",
 "变化由采伐、农业扩张、火灾与人工造林共同决定；净面积掩盖了原始林退化——成熟林的生态价值不能由新植林等量替代。",
 "与碳汇、生物多样性、水循环、畜牧用地相关。",True),
"土地利用变化":("土地利用变化：地表被人类使用方式的转变（农地、牧地、林地、建设用地）。",
 "农业用地占全球土地约三分之一，但分布极不均：南美与非洲有大片牧场，亚洲有密集农田；城市用地占比小而扩张快。",
 "变化由人口、收入、贸易与政策共同驱动；土地是有限的，各类用途之间存在竞争，因此「全球总量」掩盖了区域间的置换。",
 "与森林覆盖、粮食安全、碳排放、水资源相关。",False),
"保护与保育区体系":("保护与保育区体系：以法律或协议划定、用于维护生物多样性的陆域与海域网络。",
 "陆地保护区覆盖比例在部分拉美与非洲国家较高，小岛国与高纬度地区亦高；海洋保护区覆盖低于陆地。",
 "覆盖比例不等于管理成效；「纸上保护区」与经费不足使实际保护效果需与实地评估并用。",
 "与生物多样性、森林覆盖、海洋保护区、气候适应相关。",False),
"东亚与太平洋区域发展":("东亚与太平洋区域发展：世界银行东亚与太平洋地区的人口与经济指标概览。",
 "区域内差异极大：从高收入经济体到太平洋岛国，人口规模、城市化与收入水平相距悬殊。",
 "区域聚合值主要由人口大国拉动，不能代表小岛国或内陆国家的情形。",
 "与人口增长、城市化、贫困、气候风险相关。",False),
"拉丁美洲与加勒比区域发展":("拉丁美洲与加勒比区域发展：该区域的人口与经济指标概览。",
 "城市化率全球最高之列，人口集中于大城市与沿海；加勒比小岛国的人口规模与拉美大陆国家差异极大。",
 "区域聚合掩盖了大陆国家与小岛国之间的结构性差异。",
 "与城市化、贫困、自然灾害风险相关。",False),
"中东与北非区域发展":("中东与北非区域发展：该区域的人口与经济指标概览。",
 "人口集中于河谷、绿洲与沿海，干旱区面积广大；区域内既有高收入产油国，也有受冲突影响的国家。",
 "水资源稀缺与油气收入共同塑造区域经济；聚合值掩盖了国家间的巨大分化。",
 "与水资源、能源、贫困、人口年龄结构相关。",False),
"南亚区域发展":("南亚区域发展：该区域的人口与经济指标概览。",
 "人口高度密集于印度河—恒河平原与沿海，季风降水决定农业年景。",
 "区域内差异显著：人口大国与山地小国的指标水平相距很远；聚合值主要由人口大国主导。",
 "与人口增长、贫困、农业单产、季风相关。",False),
"农业统计体系":("农业统计体系：用于测量农业生产、投入与产出的数据体系。",
 "统计能力在各国不均衡：耕地面积、单产与产量的口径（FAO 与国家统计）常有差异，影响跨国比较。",
 "统计口径差异本身构成「数据地理」的一部分；产量数据与面积数据须同时核对才能判断集约程度。",
 "与作物单产、肥料使用、粮食安全相关。",False),
"气候适应政策":("气候适应政策：为降低气候风险影响而采取的措施与制度安排。",
 "适应需求与水资源紧张、海岸低地、干旱农业区高度相关；淡水取用强度高的流域适应压力更大。",
 "适应措施受财政与技术能力约束；单一指标（如取水强度）只能指示压力，不能衡量适应成效。",
 "与水资源、农业气候风险、极端天气、城市贫困相关。",False),
}
n=0;up=[]
for name,b in BODY.items():
    e=T.get(name)
    if not e or name not in W: continue
    d=W[name];code=d["code"];agg=d["agg"];v=disp(name)
    sid=f"wb-{agg.lower()}-{code.lower().replace('.','-')}"
    if sid not in have:
        u=f"https://api.worldbank.org/v2/country/{agg}/indicator/{code}?format=json&per_page=100&date=2015:2025"
        c2=0;size=0
        try:
            p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-o","-","-w","\n__HTTP__%{http_code}",u],capture_output=True,timeout=30)
            raw=p.stdout.decode("utf-8","ignore")
            if "__HTTP__" in raw:
                bb,cc=raw.rsplit("\n__HTTP__",1);c2=int(cc.strip() or 0);size=len(bb)
        except Exception: pass
        sd["sources"].append({"id":sid,"title":f"World Bank API — {d['label']} ({code}, {agg})",
          "author":"World Bank","year":None,"type":"数据端点","url":u,"url2":None,
          "link_ok":bool(c2==200),"verified":bool(c2==200),"page_title":f"World Bank API — {code} ({agg})",
          "note":f"JSON API {c2}；聚合 {agg}（{AGGN.get(agg,agg)}）＋指标 {code}；最新 {v}（{d['year']}年）。年度指标，随年度更新与历史修订变化。"})
        have.add(sid)
    e.update({"level":"L2","status":"L2完成(第37轮)-指标数据",
      "definition":b[0],"overview":b[0]+" 本条以可核验的指标序列为数据基础，最新值见「今天的状况」。",
      "time_or_place":f"{AGGN.get(agg,agg)}口径（{d['year']}年数据）",
      "geo":b[1],"influence":b[2],"connections":b[3],
      "polities":e.get("polities") or "本条为全球/区域主题条目，不展开具体政权序列。",
      "today":(f"来源：世界银行 API（指标 {code}，{d['label']}）：{AGGN.get(agg,agg)} {v}（{d['year']}年）。"
        "该值为合计或均值，掩盖内部差异，跨国/跨区比较须核对口径。"),
      "sources":list(dict.fromkeys((e.get("sources") or [])+[sid])),
      "needs_verification":True,
      "pending_notes":((e.get("pending_notes") or "")+
        f" 【第37轮升级 L2】数据来源 {sid}，实测 {v}（{d['year']}年）；空间差异与机制描述为常识性地理概述，未逐国引用。").strip(),
      "last_update":TODAY})
    e["svg"]=("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='示意图'>"
      "<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>"
      "<rect x='100' y='150' width='150' height='150' fill='none' stroke='var(--accent)' stroke-width='3'/>"
      "<rect x='300' y='190' width='150' height='110' fill='none' stroke='var(--accent2)' stroke-width='3'/>"
      "<rect x='500' y='225' width='150' height='75' fill='none' stroke='var(--accent2)' stroke-width='3'/>"
      f"<text x='100' y='140' class='lbl'>{name}</text>"
      f"<text x='100' y='340' class='dim'>分档示意（非实际数值） · {v}</text></svg>")
    n+=1;up.append(name)

json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
import collections
print("升级",n,"：","、".join(up))
print(collections.Counter((e["tier"],e["level"]) for e in T.values()))