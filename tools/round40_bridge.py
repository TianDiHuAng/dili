# -*- coding: utf-8 -*-
"""第40轮 B1：Crossref→OpenAlex DOI 桥（绕过 search 端点 429）。"""
import subprocess,json,os,urllib.parse,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q={
"沙漠化":["desertification land degradation drylands","desertification assessment"],
"城市热岛":["urban heat island intensity","urban heat island spatial pattern"],
"生物多样性分布":["global biodiversity spatial patterns","biodiversity distribution latitudinal"],
"自然灾害风险":["natural hazard risk assessment","disaster risk reduction geography"],
"极端天气预警":["early warning system extreme weather","extreme weather forecasting warning"],
"城市贫困":["urban poverty spatial","urban poverty developing countries"],
"可持续交通":["sustainable transport systems","sustainable urban mobility"],
"环境治理":["environmental governance","environmental governance effectiveness"],
"火灾生态":["fire ecology regime","fire regime ecosystem"],
"争议边界处理原则":["boundary dispute map cartography","international boundary delimitation"],
"南极特别保护区":["Antarctic Specially Protected Area","Antarctic protected area management"],
"南极洲无农业的环境约束":["Antarctic terrestrial environment constraints","Antarctica agriculture feasibility"],
"法蒂玛王朝":["Fatimid caliphate history","Fatimid state Egypt"],
"非洲大湖地区":["East African Great Lakes region limnology","African Great Lakes fisheries"],
"古巴岛":["Cuba island geography","Cuban archipelago geology"],
"查文文化":["Chavin de Huantar","Chavin culture archaeology"],
"南美贸易网络":["Andean prehispanic exchange networks","South America long distance trade prehispanic"],
"南锥体":["Southern Cone South America","Southern Cone agriculture geography"],
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
    if not inv: return None
    pos={}
    for k,ix in inv.items():
        for i in ix: pos[i]=k
    return " ".join(pos[i] for i in sorted(pos))

res={};detail={}
for topic,qs in Q.items():
    seen=set();best=None;tries=[]
    for q in qs:
        cr=cj("https://api.crossref.org/works?query.bibliographic="+urllib.parse.quote(q)+
              "&rows=12&select=title,DOI,issued,type")
        items=(cr.get("message") or {}).get("items") or []
        for it in items:
            doi=it.get("DOI")
            if not doi or doi in seen: continue
            seen.add(doi)
            if it.get("type") in ("book-review","component","dataset","peer-review"): continue
            oa=cj(f"https://api.openalex.org/works/https://doi.org/{doi}")
            ttl=(oa.get("title") or (it.get("title") or [""])[0] or "")
            a=ab(oa) or ""
            rec={"doi":doi,"title":ttl,"year":oa.get("publication_year"),
                 "oa_id":(oa.get("id") or "").rsplit("/",1)[-1],"cited":oa.get("cited_by_count"),
                 "type":oa.get("type"),"abs_len":len(a),"abstract":a,
                 "host":(((oa.get("primary_location") or {}).get("source") or {}).get("display_name"))}
            tries.append({"doi":doi,"title":ttl[:60],"abs_len":len(a)})
            if len(a)<300: continue
            if best is None or (rec.get("cited") or 0)>(best.get("cited") or 0): best=rec
        if best: break
        time.sleep(1.5)
    res[topic]=best;detail[topic]=tries[:12]
    print(f"{'OK' if best else '--'} {topic:<18} {(best['title'][:46] if best else '-')} ({best.get('year') if best else ''}) abs={best['abs_len'] if best else 0}",flush=True)
    time.sleep(1.5)
json.dump(res,open(os.path.join(ROOT,"reports","round40_bridge.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
json.dump(detail,open(os.path.join(ROOT,"reports","round40_bridge_detail.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n有摘要候选:",sum(1 for v in res.values() if v),"/",len(Q),flush=True)