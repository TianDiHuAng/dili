# -*- coding: utf-8 -*-
"""第39轮 B1：23 条剩余补充 L1 的 OpenAlex 检索（精确词 + 退避）。"""
import subprocess,json,os,urllib.parse,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q={
# 南极/极地
"横贯南极山脉":[("Transantarctic Mountains","transantarctic"),("Transantarctic Mountains geology","antarctic")],
"罗斯海":[("Ross Sea","ross sea"),("Ross Sea ecology","ross")],
"南极科考站":[("Antarctic research stations","antarctic"),("Antarctic stations science support","station")],
"南极洲无农业的环境约束":[("Antarctica agriculture impossible","antarctic"),("Antarctic environment constraints","antarctic")],
"南极特别保护区":[("Antarctic Specially Protected Area","specially protected"),("Antarctic protected areas","protected area")],
# 方法/概念
"沙漠化":[("desertification","desertification"),("desertification land degradation drylands","desertification")],
"争议边界处理原则":[("boundary dispute cartography map","boundary dispute"),("territorial dispute cartography","territorial")],
"生物多样性分布":[("biodiversity distribution patterns","biodiversity"),("global biodiversity spatial patterns","biodiversity")],
"城市热岛":[("urban heat island","heat island"),("urban heat island intensity","heat island")],
"自然灾害风险":[("natural hazard risk","hazard risk"),("disaster risk geography","disaster risk")],
"极端天气预警":[("extreme weather warning systems","warning"),("early warning systems extreme weather","early warning")],
"城市贫困":[("urban poverty","urban poverty"),("urban poverty geography","poverty")],
"可持续交通":[("sustainable transport","sustainable transport"),("sustainable mobility transport","mobility")],
"环境治理":[("environmental governance","environmental governance"),("environmental governance institutions","governance")],
"火灾生态":[("fire ecology","fire ecology"),("fire regime ecology","fire regime")],
# 历史（换词重试）
"法蒂玛王朝":[("Fatimid dynasty","fatimid dynasty"),("Fatimid caliphate Egypt history","fatimid caliphate")],
"非洲大湖地区":[("East African Great Lakes region geography","great lakes region"),("African Great Lakes lakes","great lakes")],
"古巴岛":[("Cuba island geography Caribbean","cuba"),("Cuban archipelago","cuban")],
"查文文化":[("Chavin de Huantar","chavin de huantar"),("Chavin culture Andes","chavin culture")],
"南美贸易网络":[("prehispanic exchange networks South America","exchange"),("Andean long distance trade","long-distance trade")],
"南锥体":[("Southern Cone South America geography","southern cone"),("Southern Cone countries","cone")],
}
def get(u):
    for _ in range(4):
        try:
            p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",u],capture_output=True,timeout=40)
            raw=p.stdout.decode("utf-8","ignore")
            if "__HTTP__" not in raw: time.sleep(4);continue
            b,c=raw.rsplit("\n__HTTP__",1);code=int(c.strip() or 0)
            if code==200: return b
            time.sleep(6)
        except Exception: time.sleep(4)
    return "{}"
def ab(w):
    inv=w.get("abstract_inverted_index")
    if not inv: return None
    pos={}
    for k,ix in inv.items():
        for i in ix: pos[i]=k
    return " ".join(pos[i] for i in sorted(pos))
res={}
for t,pairs in Q.items():
    best=None
    for q,needle in pairs:
        u=("https://api.openalex.org/works?search="+urllib.parse.quote(q)+"&per_page=15&mailto=geo-encyclopedia@example.com")
        try: d=json.loads(get(u))
        except Exception: d={}
        for w in d.get("results",[]):
            a=ab(w)
            if not a or len(a)<300: continue
            ti=(w.get("title") or "").lower()
            if needle not in ti: continue
            if w.get("type") in ("book-review","paratext","editorial","letter","erratum"): continue
            cand={"id":(w.get("id") or "").rsplit("/",1)[-1],"title":w.get("title"),"year":w.get("publication_year"),
              "doi":w.get("doi"),"cited":w.get("cited_by_count"),"type":w.get("type"),"abstract":a,
              "host":(((w.get("primary_location") or {}).get("source") or {}).get("display_name"))}
            if best is None or (cand.get("cited") or 0)>(best.get("cited") or 0): best=cand
        if best: break
        time.sleep(3)
    res[t]=best
    print(f"{'OK' if best else '--'} {t:<18} {(best['title'][:50] if best else '-')} ({best.get('year') if best else ''})",flush=True)
    time.sleep(2.5)
json.dump(res,open(os.path.join(ROOT,"reports","round39_openalex.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n可用:",sum(1 for v in res.values() if v),"/",len(Q),flush=True)