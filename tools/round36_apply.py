# -*- coding: utf-8 -*-
"""第36轮：用真正的北美文献升级「北美原住民」→ 重要 104/104。"""
import json,os,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}

NEW=[("W2109701276","Beringian Standstill and Spread of Native American Founders",2007,
      "PLoS ONE","https://doi.org/10.1371/journal.pone.0000829",797),
     ("W2568445233","Earliest Human Presence in North America Dated to the Last Glacial Maximum: New Radiocarbon Dates from Bluefish Caves, Canada",2017,
      "PLoS ONE","https://doi.org/10.1371/journal.pone.0169486",210)]
for oa,title,yr,host,doi,cite in NEW:
    sid=f"openalex-{oa}"
    if sid in have: continue
    code=0;size=0
    for _ in range(3):
        try:
            p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",f"https://api.openalex.org/works/{oa}"],capture_output=True,timeout=30)
            raw=p.stdout.decode("utf-8","ignore")
            if "__HTTP__" in raw:
                bb,cc=raw.rsplit("\n__HTTP__",1);code=int(cc.strip() or 0);size=len(bb)
                if code==200: break
            time.sleep(5)
        except Exception: time.sleep(5)
    sd["sources"].append({"id":sid,"title":f"OpenAlex {oa} — {title}","author":"OpenAlex（开放学术知识图谱，CC0 元数据）",
      "year":yr,"type":"期刊论文","url":f"https://api.openalex.org/works/{oa}","url2":doi,
      "link_ok":bool(code==200),"verified":bool(code==200),"page_title":title,
      "note":(f"OpenAlex 作品 {oa}；{yr}年；{host}；DOI {doi}；被引 {cite}。HTTP {code}，{size} 字节。"
              + ("摘要要点：美洲原住民源自少数亚洲奠基人群，很可能经白令地区（Beringia）抵达；分析 623 份完整 mtDNA，"
                 "发现奠基人群内的遗传多样性高于此前报告，系统发育结构支持在 Beringia 停留（standstill）后扩散。" if oa=="W2109701276"
                 else "摘要要点：人类首次进入北美的时间仍在争论；育空 Bluefish Caves 的放射性碳测年支持末次盛冰期（LGM）期间进入东白令地区"
                      "（阿拉斯加与育空），该假说因缺少同期遗址与地层疑虑而受质疑。"))})
    have.add(sid)

e=T["北美原住民"]
e.update({"level":"L2","status":"L2完成(第36轮)-学术文献双源",
  "definition":"北美原住民：在欧洲人到来之前即生活于北美的原住民族群，其祖源人群很可能经白令地区（Beringia）自亚洲进入美洲。",
  "overview":("北美原住民的祖源与进入时间属于活跃研究领域。2017 年发表于 PLoS ONE 的研究指出，人类首次进入北美的时间"
    "「仍在科学界激烈争论」；育空 Bluefish Caves 的测年支持末次盛冰期（LGM）期间进入东白令地区（阿拉斯加与育空），"
    "但因缺少同期遗址与地层疑虑而受质疑。另一项 2007 年 PLoS ONE 研究以 623 份完整线粒体 DNA 分析指出，"
    "美洲原住民源自少数亚洲奠基人群，很可能经白令地区抵达，并支持在 Beringia 停留（standstill）后扩散的模型。"),
  "time_or_place":"进入时间与路线仍在争论（末次盛冰期前后为候选窗口；Beringia 停留模型）；两处来源均强调不确定性",
  "geo":("北美原住民的分布跨越北极、亚寒带、温带与干旱区，聚落形态随生态带变化显著。"
    "就进入路径而言，白令地区（今白令海峡两侧）是亚洲与美洲之间的陆桥区；末次盛冰期海平面下降使该陆桥出露，"
    "冰川消退的先后则决定内陆通道与沿海通道何时可用。**这些路径假说的具体时间仍属研究议题**，本条不给出确定年代。"),
  "influence":("所引 2007 年研究以大规模线粒体 DNA 分析表明：美洲原住民源自**少数亚洲奠基人群**，其内部遗传多样性高于此前报告，"
    "系统发育结构支持人群在 Beringia 有停留期后向南北扩散。所引 2017 年研究则以育空 Bluefish Caves 的测年"
    "支持末次盛冰期期间已进入东白令地区，同时明确指出该结论仍受质疑。两项证据分别来自遗传学与考古测年，"
    "**相互补充但都不构成定论**。"),
  "polities":"本条不展开具体族群的政治序列；不同区域的社会组织形态差异极大，待专门的民族志与考古研究核验。",
  "connections":("经白令地区与东北亚相连，是美洲人群扩散的入口；此后南北美洲之间的走廊（中美洲地峡）成为继续南向扩散的通道。"
    "这一「自西北向东南」的扩散方向是遗传学与考古学共同支持的框架，具体路线与年代待核。"),
  "sources":["openalex-W2109701276","openalex-W2568445233","s010-unesco-org"],
  "needs_verification":True,
  "pending_notes":("第36轮返工后重新升级：已撤下原误用的 OpenAlex W2020901419（研究对象为**巴西亚马孙** Monte Alegre 洞穴）。"
    "本轮的兩個来源均以北美/白令地区为对象：W2109701276（2007，PLoS ONE，被引 797，mtDNA 与 Beringia 停留模型）与 "
    "W2568445233（2017，PLoS ONE，被引 210，育空 Bluefish Caves 测年，明确标注该结论受质疑）。"
    " 正文对进入时间与路线均保留「仍在争论」的表述，未给出确定年代。"),
  "last_update":TODAY})
e["svg"]=("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='示意图'>"
  "<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>"
  "<path d='M120 200 L250 180 L380 200 L520 230 L640 260' fill='none' stroke='var(--accent)' stroke-width='4'/>"
  "<circle cx='250' cy='180' r='8' class='pt'/><text x='200' y='160' class='lbl'>白令地区</text>"
  "<circle cx='380' cy='200' r='6' class='pt'/><text x='360' y='180' class='lbl'>北美</text>"
  "<circle cx='520' cy='230' r='5' class='pt'/><text x='500' y='212' class='lbl'>中美</text>"
  "<text x='40' y='370' class='dim'>北美原住民扩散示意（路线与年代仍有争议），非精确测绘</text></svg>")

json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
import collections
print(collections.Counter((e["tier"],e["level"]) for e in T.values()))
print("重要L1:",[x["title"] for x in T.values() if x["tier"]=="重要" and x["level"]=="L1"])