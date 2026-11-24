# -*- coding: utf-8 -*-
"""第53轮：登记 6 条主来源；元代/河中地区按 D110 记录无候选。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round53_primary.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)
TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述"}

SPEC={
"莫切文化":("influence","所引 2010 年《Craft Specialists at Moche》（被引58）以莫切都城的手工业作坊为对象，指出陶工、冶金与宝石工匠构成城市人口的一部分，并在**南莫切国家的经济、政治与宗教领域**扮演重要角色；本条「河谷政治中心与手工业专门化相互支撑」据此。","strong"),
"阿塔卡马沙漠":("geo","所引 2003 年《The central Andean west-slope rainshadow…》（**被引 587**）分析安第斯中段西坡的**雨影效应**：15°–27°S 的降水主要来自亚马孙的夏季对流，降水随海拔的增减在雨影条件下呈指数关系；本条「阿塔卡马极端干旱源于西坡雨影与副热带高压叠加」据此。","strong"),
"意大利半岛":("geo","所引 2010 年《Geology and Tectonic Evolution of the Central-Southern Apennines, Italy》（被引192）以 1:250,000 地质图与 20 年野外数据重建**中南部亚平宁造山带的构造演化**；本条「半岛以亚平宁山系为脊、构造上属造山带」据此。","strong"),
"城市地理":("influence","所引 2004 年《Exploring Metropolitan Accessibility and Urban Structure》（被引132）用 GIS 分析**区位可达性**与**城市空间结构**的关系，指出可达性度量可用于刻画城市结构；本条「城市地理学以可达性与空间结构刻画城市」据此。","strong"),
"地理信息系统":("influence","所引 2006 年《Spatial (GIS-based) decision support system…》把 GIS 用于**空间决策支持**；本条「GIS 作为空间分析与决策支持的工具」据此。","weak"),
"突厥":("polities","所引 2023 年章节讨论**最早的突厥语游牧人群**与蒙古—准噶尔草原，指出突厥人建立了历史上第一个突厥帝国——**突厥汗国（552–745年）**；本条「突厥汗国起于 6 世纪中叶、以草原游牧为基础」据此。","weak"),
}
n=0;log=[]
for t,(fld,sentence,grade) in SPEC.items():
    c=F[t]["best"];e=T.get(t)
    if not c or not e: continue
    oid=c["oa_id"];sid=f"openalex-{oid}"
    if sid in e["sources"]: continue
    if sid not in have:
        code=0;size=0
        for _ in range(3):
            try:
                p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",f"https://api.openalex.org/works/{oid}"],capture_output=True,timeout=30)
                raw=p.stdout.decode("utf-8","ignore")
                if "__HTTP__" in raw:
                    bb,cc=raw.rsplit("\n__HTTP__",1);code=int(cc.strip() or 0);size=len(bb)
                    if code==200: break
                time.sleep(4)
            except Exception: time.sleep(4)
        sd["sources"].append({"id":sid,"title":f"OpenAlex {oid} — {c['title']}","author":"OpenAlex（开放学术知识图谱，CC0 元数据）",
          "year":c.get("year"),"type":TYP.get(c.get("type"),"学术文献"),
          "url":f"https://api.openalex.org/works/{oid}","url2":f"https://doi.org/{c['doi']}",
          "link_ok":bool(code==200),"verified":bool(code==200),"page_title":(c["title"] or "")[:200],
          "note":f"OpenAlex 作品 {oid}（DOI {c['doi']}）；{c.get('year')}年；{c.get('host') or '出版方未标'}；被引 {c.get('cited')}。HTTP {code}，{size} 字节。摘要长度 {c['abs_len']} 字符；主题槽命中 {c['slots']}。证据强度：{grade}。"})
        have.add(sid)
    e["sources"]=list(dict.fromkeys(e["sources"]+[sid]))
    e[fld]=((e.get(fld) or "")+" "+sentence).strip()
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第53轮补主来源（{grade}）】{sid}（{c.get('year')}年，《{c['title']}》，DOI {c['doi']}，被引 {c.get('cited')}）："
      f"待支撑断言「{F[t]['claim']}」；主题槽命中 {c['slots']}；已在本条 {fld} 段落点。").strip()
    e["last_update"]=TODAY;n+=1;log.append(t)

REC={
"元代":"两条检索式（Yuan dynasty state administration／Yuan empire transport communications）、共 36 条 Crossref 结果中，**无一条**同时满足「标题含 yuan」与「两个主题槽」——现有来源《Koryŏ inlay celadon…》(陶瓷贸易侧面) 仍为主要来源。主来源**缺**。",
"河中地区":"两条检索式（Transoxiana oasis irrigation trade／Central Asia Samarkand Bukhara irrigation）、共 36 条结果中无一过筛；现有来源《The Connection of the Genetic, Cultural and Geographic…》(多学科侧面) 仍为主要来源。主来源**缺**。",
}
for t,why in REC.items():
    e=T.get(t)
    if not e: continue
    e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第53轮检索记录】引擎 Crossref（DOI→OpenAlex 取摘要）；{why}").strip()
    e["last_update"]=TODAY

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=53
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
MIN=800
def is_data(sid): return sid.startswith(("wb-","usgs-eq","noaa-current","ats-parties","wikidata-"))
def hb(sid,e=None):
    if is_data(sid): return False
    notes=[(S.get(sid) or {}).get("note") or ""]
    if e is not None: notes.append(e.get("pending_notes") or "")
    for note in notes:
        if "stub" in note.lower(): return False
        for pat in (r"摘要长度\s*(\d+)\s*字符",r"正文字?录?\s*\*{0,2}([\d,]+)\s*字符",r"正文\s*(\d+)\s*字符",r"摘要\s*(\d+)\s*字符"):
            m=re.search(pat,note)
            if m: return int(m.group(1).replace(",",""))>=MIN
        m=re.search(r"(\d{3,7})\s*字节",note)
        if m: return int(m.group(1))>=MIN
    return None
g2=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)>=2)
o1=sum(1 for e in T.values() if sum(1 for s in e["sources"] if hb(s,e) is True)==1)
print("登记",n,"：","、".join(log))
print(f"重算 ≥2 {g2} / 1个 {o1}")