# -*- coding: utf-8 -*-
"""第52轮：登记文艺复兴意大利主来源；按 D110 如实记录印加/亚马逊/库什的检索结论。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
F=json.load(open(os.path.join(ROOT,"reports","round52_primary.json"),encoding="utf-8"))
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)
TYP={"article":"期刊论文","book":"专著","book-chapter":"专著章节","review":"综述"}

# ===== 1 文艺复兴意大利：登记主来源 =====
e=T["文艺复兴意大利"];c=F["文艺复兴意大利"]["best"]
oid=c["oa_id"];sid=f"openalex-{oid}"
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
      "note":f"OpenAlex 作品 {oid}（DOI {c['doi']}）；{c.get('year')}年；Cambridge UP；被引 {c.get('cited')}。HTTP {code}，{size} 字节。摘要长度 {c['abs_len']} 字符；主题槽命中 {c['slots']}。意大利语摘要：14–15 世纪意大利城邦国家的危机与区域国家的形成。"})
    have.add(sid)
e["sources"]=list(dict.fromkeys(e["sources"]+[sid]))
e["influence"]=("所引 2012 年研究（剑桥大学出版社，意大利语）描述 14–15 世纪**意大利城邦国家的危机**，并分析各城市及其统治阶层在**区域国家**形成过程中的处境；"
  "本条据此写「城邦竞争与区域国家的兴替构成文艺复兴的政治背景」。艺术赞助与商业财富的具体关系另由本条已列的赞助研究作旁证。")
e["pending_notes"]=((e.get("pending_notes") or "")+
  f" 【第52轮补主来源】{sid}（{c.get('year')}年，《{c['title']}》，DOI {c['doi']}，被引 {c.get('cited')}）："
  f"待支撑断言「{F['文艺复兴意大利']['claim']}」；主题槽命中 {c['slots']}；已在本条 influence 段落点。此前的两篇（街头艺人社会史、雕塑赞助）仍为旁证。").strip()
e["last_update"]=TODAY

# ===== 2 按 D110 如实记录其余 3 条的检索结论 =====
REC={
"印加帝国":"两条检索式、共 40 条 Crossref 结果中，过对象词与两主题槽者只有《The Sacred Landscape of the Inca: The Cusco Ceque System》(1998, 被引230)——但该书的主题是**库斯科的 ceque 仪式系统**（328 处 huaca／42 条 ceque 线的神圣空间组织），属宗教地理侧面，**不支撑「疆域、道路与行政」**。故本条主来源**仍缺**。",
"亚马逊盆地":"两条检索式、共 40 条结果中过筛者只有《Extractive Reserves and Participatory Research as Factors in the Biogeochemistry…》(2001, 被引3)——主题是**采掘保护区与参与式研究**（土地利用与政策侧面），不涉盆地地貌与水文。主来源**仍缺**。",
"库什与努比亚":"两条检索式（Meroe trade routes goods exchange／Kushite long-distance trade）、共 40 条结果中**无一条**同时满足「标题含 kush/meroe」与「两个主题槽」。商路与商品结构的主来源**确无**（此结论已按 D110 记录引擎、检索式、条数与逐项拒绝理由）。",
}
for t,why in REC.items():
    e=T.get(t)
    if not e: continue
    if "【第52轮检索记录】" in (e.get("pending_notes") or ""): continue
    e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第52轮检索记录】引擎 Crossref（DOI→OpenAlex 取摘要）；{why}").strip()
    e["last_update"]=TODAY

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=52
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
print(f"登记 1 条；重算 ≥2 {g2} / 1个 {o1}")