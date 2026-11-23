# -*- coding: utf-8 -*-
"""第39轮：南极 3 条补充条目 → L2。"""
import json,os,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round39_openalex.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));have={s["id"] for s in sd["sources"]}
TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述"}

BODY={
"横贯南极山脉":dict(span="地质尺度（新生代以来；所引研究为其隆升机制）",
 defn="横贯南极山脉：横贯南极大陆、分隔东南极与西南极的山脉，全长约3000千米。",
 geo="山脉沿东南极与西南极的边界延伸，长约3000千米；山脉北侧为罗斯海与维多利亚地盆地，南侧为东南极冰盖。山体被冰盖覆盖，仅山脊与少数冰原岛峰出露。",
 infl="所引 1989 年研究指出，该山脉形成于东南极与西南极的陆—陆边界，高热流、薄地壳、正断层与火山活动表明这条约3000千米的边界具有**张裂性质**，并发育出横贯南极山脉、威尔克斯盆地与维多利亚地盆地三个主要构造。这为理解山脉隆升提供了机制解释。",
 conn="山脉把东南极冰盖与西南极冰盖分隔，影响冰流路径；其北侧为罗斯海与罗斯冰架，是南极物质平衡研究的关键区。"),
"罗斯海":dict(span="现代海洋观测（所引研究覆盖近40年记录）",
 defn="罗斯海：南太平洋扇形海域，南接罗斯冰架，是南极洲附近最深的边缘海。",
 geo="海域南部被罗斯冰架覆盖，北部通向开阔洋；大陆架水深较大，是南极底层水形成的重要区域之一。海冰与冰架的季节变化显著。",
 infl="所引 2002 年研究以近四十年的海洋观测（南极附近最长的记录之一）指出：陆架水盐度与罗斯环流表层盐度**明显下降**（即淡化），同期罗斯岛大气增温、陆架以北约300米深处海水增温、南方涛动指数更偏负、并伴有冰层减薄。这些变化同向出现，提示海冰—淡水通量—环流的耦合。",
 conn="与罗斯冰架、南极底层水形成、南大洋环流相连，是全球热盐环流的重要源区之一。"),
"南极科考站":dict(span="科考活动现状（所引 2009 年调查，覆盖28国站点）",
 defn="南极科考站：各国在南极大陆及其岛屿设立的常年或夏季科学考察站。",
 geo="站点分布不均：南极半岛与沿岸岛屿最密集，东南极内陆与高原站稀少；内陆站海拔高、气温极低，补给线长。选址受冰况、地形与后勤可达性约束。",
 infl="所引 2009 年研究由瑞典极地研究秘书处发起，就南极 28 国站点的废水与灰水处置实践做问卷普查（2005年秋发出）。研究以瑞典 Wasa 站（毛德皇后地）为参照，说明科考站的**环境管理**已成为南极治理的一部分，而非仅是科研后勤问题。",
 conn="通过海运与空运补给线连接各国本土与南极，站点之间通过条约体系下的信息网络（如环境官员网络）协调。"),
}
n=0;up=[]
for t,b in BODY.items():
    e=T.get(t);c=F.get(t)
    if not e or not c: continue
    oa=(c.get("id") or "").rsplit("/",1)[-1];sid=f"openalex-{oa}"
    if sid not in have:
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
        sd["sources"].append({"id":sid,"title":f"OpenAlex {oa} — {c.get('title')}","author":"OpenAlex（开放学术知识图谱，CC0 元数据）",
          "year":c.get("year"),"type":TYP.get(c.get("type"),"学术文献"),
          "url":f"https://api.openalex.org/works/{oa}","url2":c.get("doi"),
          "link_ok":bool(code==200),"verified":bool(code==200),"page_title":(c.get("title") or "")[:200],
          "note":f"OpenAlex 作品 {oa}；{c.get('year')}年；{c.get('host') or '出版方未标'}；DOI {c.get('doi') or '无'}；被引 {c.get('cited')}。HTTP {code}，{size} 字节。摘要节录：{(c.get('abstract') or '')[:240]}…"})
        have.add(sid)
    e.update({"level":"L2","status":"L2完成(第39轮)-学术文献",
      "definition":b["defn"],"overview":b["defn"],"time_or_place":b["span"],
      "geo":b["geo"],"influence":b["infl"],
      "polities":e.get("polities") or "本条为自然地理/科考主题条目，不展开政权序列。",
      "connections":b["conn"],"today":e.get("today") or "（本条的当代指标不在本页展开。）",
      "sources":list(dict.fromkeys((e.get("sources") or [])+[sid,"s010-unesco-org"])),"needs_verification":True,
      "pending_notes":((e.get("pending_notes") or "")+
        f" 【第39轮升级 L2】第二来源为 OpenAlex {sid}（{c.get('year')}年，《{c.get('title')}》，{c.get('host') or '出版方未标'}，DOI {c.get('doi') or '无'}，被引 {c.get('cited')}）。"
        f" 机制/影响段据其摘要撰写，geo 为常识性地理描述（未挂学术来源）。").strip(),
      "last_update":TODAY})
    e["svg"]=("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 400' role='img' aria-label='示意图'>"
      "<rect x='20' y='20' width='720' height='360' rx='10' fill='none' stroke='var(--line)'/>"
      "<path d='M100 260 C220 225 350 210 480 218 C580 224 650 240 690 258' fill='none' stroke='var(--accent)' stroke-width='4'/>"
      f"<circle cx='380' cy='214' r='7' class='pt'/><text x='290' y='192' class='lbl'>{t}</text>"
      f"<text x='40' y='370' class='dim'>{t} · 简笔示意，非精确测绘</text></svg>")
    n+=1;up.append(t)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
import collections
print("升级",n,"：","、".join(up))
print("剔除：南极洲无农业的环境约束（候选为「生物入侵」文献，不支撑「无农业」判断）")
print(collections.Counter((e["tier"],e["level"]) for e in T.values()))