# -*- coding: utf-8 -*-
"""第46轮返工B：12条因果断言弱化 + 地形类3条重新检索（领域词）。"""
import json,os,re,sys,subprocess,time,urllib.parse
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]}
have=set(S)

# ===== A 12 条因果断言：弱化为「与…相关」，并标待核 =====
WEAKEN={
"海洋保护区":("influence","划定受政治意愿与渔业利益制约；「覆盖面积」不等于「管理成效」，执法经费与能力**与**保护成效相关（具体归因待专门评估研究核验）。"),
"人口年龄结构":("influence","结构由生育率、死亡率与迁移共同决定（此为人口学的标准分解，属**教科书性表述**，未挂具体文献）；年龄结构一旦形成具有惯性，与劳动力供给、教育与养老支出相关。"),
"肉奶生产与土地":("influence","畜牧用地扩张**与**森林减少相关（相关不等于全部归因）；单位产品的土地与排放强度差异极大，取决于饲料与饲养方式。"),
"全球气温变化":("influence","变暖与温室气体累积相关，并叠加自然变率（如 ENSO、火山）造成年际波动（本条用 NOAA 温度序列，机制表述为常识性内容）；单年数值不能代表趋势。"),
"城市化水平":("influence","城市化与农村推力、城市拉力相关（此为教科书的经典框架，未挂具体文献）；比例本身不反映城市治理与生活质量。"),
"儿童发展地域差异":("influence","死亡率与分娩条件、疫苗覆盖、营养与饮水卫生相关；初级卫生系统可及性**被认为**比总支出更关键（属待核的判断，非本条来源所证）。"),
"碳排放空间差异":("influence","差异源于能源结构、产业结构与消费水平（教科书性分解）；国际贸易使排放发生「转移」，故按生产地统计与按消费地核算会给出不同图景——消费侧核算属专门研究领域，本条仅指出该问题的存在。"),
"能源转型":("geo","转型速度在地区间差异极大，但「可再生能源占比」不能区分传统生物质与现代可再生能源；撒哈拉以南非洲的高占比主要来自传统生物质，欧洲的高占比主要来自现代来源（该区分属指标解读，未挂文献）。"),
"肥料使用与环境":("influence","过量氮磷通过径流进入河湖与沿海，与富营养化与缺氧相关（机制为常识性表述）；施用效率比总量更能解释环境后果。"),
"湿地与水资源":("influence","水资源可得性与降水、蒸发及跨境河流相关；湿地则依赖水位节律，上游取水与筑坝会改变其存续条件（机制为常识性表述）。"),
"气候与健康风险":("influence","气候通过多条路径影响健康（直接伤害、病媒、食物与水的安全），其效应被卫生系统能力放大或削弱；单一指标只反映结果的一部分。"),
"全球营养状况":("influence","营养状况与食物供给、卫生条件、母亲健康与收入相关；仅提高热量供给不能解决微量营养素缺乏（常识性表述）。"),
}
n=0
for t,(fld,sentence) in WEAKEN.items():
    e=T.get(t)
    if not e: continue
    e[fld]=sentence
    if "【第46轮返工·因果弱化】" not in (e.get("pending_notes") or ""):
        e["pending_notes"]=((e.get("pending_notes") or "")+
          " 【第46轮返工·因果弱化】原句含「由…决定／是关键变量」类因果断言，而本条未挂能支撑该因果的文献；已改为「与…相关」等可支撑的弱表述，"
          "并标明哪部分属教科书性分解（不需文献）、哪部分待专门研究核验（D101 槽位化举证不通过者不得写成定论）。").strip()
    e["last_update"]=TODAY;n+=1
print("因果弱化:",n)

# ===== B 地形类 3 条：用领域词重新检索 =====
Q={
"古希腊城邦":("geomorphology of Greece physical geography","greece"),
"罗马共和国":("Tiber alluvial plain Roman agriculture","tiber"),
"克里特文明":("geodiversity geomorphology of Crete","crete"),
}
def cj(url):
    for _ in range(3):
        try:
            p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0",url],capture_output=True,timeout=35)
            s=p.stdout.decode("utf-8","ignore")
            if s.strip().startswith("{"): return json.loads(s)
            time.sleep(3)
        except Exception: time.sleep(3)
    return {}
def ab(w):
    inv=w.get("abstract_inverted_index")
    if not inv: return ""
    pos={}
    for k,ix in inv.items():
        for i in ix: pos[i]=k
    return " ".join(pos[i] for i in sorted(pos))
TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述"}
res={}
for t,(q,needle) in Q.items():
    best=None;seen=set()
    cr=cj("https://api.crossref.org/works?query.bibliographic="+urllib.parse.quote(q)+"&rows=15&select=title,DOI,type")
    for it in (cr.get("message") or {}).get("items") or []:
        doi=it.get("DOI")
        if not doi or doi in seen: continue
        seen.add(doi)
        if it.get("type") in ("book-review","component","dataset","peer-review","posted-content"): continue
        oa=cj(f"https://api.openalex.org/works/https://doi.org/{doi}")
        a=ab(oa) or ""
        if len(a)<300: continue
        ti=(oa.get("title") or "").lower(); al=a.lower()
        if needle not in ti and needle not in al: continue
        rec={"doi":doi,"title":oa.get("title"),"year":oa.get("publication_year"),
             "oa_id":(oa.get("id") or "").rsplit("/",1)[-1],"cited":oa.get("cited_by_count"),
             "type":oa.get("type"),"abs_len":len(a),"abstract":a,
             "host":(((oa.get("primary_location") or {}).get("source") or {}).get("display_name"))}
        if best is None or (rec.get("cited") or 0)>(best.get("cited") or 0): best=rec
        if len(seen)>=12: break
    res[t]=best
    print(f"{'OK' if best else '--'} {t:<12} {(best['title'][:50] if best else '-')} ({best.get('year') if best else ''}) cite={best.get('cited') if best else ''}",flush=True)
    time.sleep(1.2)

m=0
for t,c in res.items():
    e=T.get(t)
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
          "note":f"OpenAlex 作品 {oid}（DOI {c['doi']}）；{c.get('year')}年；{c.get('host') or '出版方未标'}；被引 {c.get('cited')}。HTTP {code}，{size} 字节。摘要长度 {c['abs_len']} 字符。"})
        have.add(sid)
    e["sources"]=list(dict.fromkeys((e["sources"] or [])+[sid]))
    e["pending_notes"]=re.sub(r" 【第46轮来源性质】[^【]*","",e.get("pending_notes") or "")
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第46轮补源·领域词重检】{sid}（{c.get('year')}年，《{c['title']}》，DOI {c['doi']}，被引 {c.get('cited')}）："
      f"前一轮称「无对应专题文献」系检索不力（只用一次 bibliographic 查询、缺领域词）；改用 geomorphology/physical geography 等领域词后取得该文献，已登记。").strip()
    e["last_update"]=TODAY;m+=1
print("地形类补源:",m)
save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=46
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)