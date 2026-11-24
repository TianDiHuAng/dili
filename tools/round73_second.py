# -*- coding: utf-8 -*-
"""第73轮：为核心 G3 条目检索第二内容源（宽口径+摘要对读，两批）。"""
import subprocess,json,os,urllib.parse,time,unicodedata,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def norm(x):
    x=unicodedata.normalize("NFKD",(x or "").lower())
    return "".join(c for c in x if not unicodedata.combining(c))
BATCH=sys.argv[1] if len(sys.argv)>1 else "1"
Q={
"撒哈拉沙漠":dict(objs=["sahara","saharan"],qs=["Sahara desert climate history","Saharan environment change"],
  slots=["sahara","desert","climate","environment","change"]),
"东非大裂谷":dict(objs=["east african rift","rift valley"],qs=["East African Rift geology","rift valley lakes evolution"],
  slots=["rift","geolog","volution","lake","tecton"]),
"马里帝国":dict(objs=["mali"],qs=["Mali empire West Africa","medieval Mali state trade"],
  slots=["mali","empire","state","trade","west africa"]),
"两河流域":dict(objs=["mesopotamia"],qs=["Mesopotamia irrigation salinization","ancient Mesopotamia agriculture environment"],
  slots=["mesopotamia","irrigation","salin","agricultur","environment"]),
"爱琴海世界":dict(objs=["aegean"],qs=["Aegean Bronze Age trade network","Aegean prehistory society"],
  slots=["aegean","bronze age","trade","society","network"]),
"罗马帝国":dict(objs=["roman empire","rome"],qs=["Roman empire economy trade","Roman imperial administration roads"],
  slots=["roman","empire","econom","trade","administrat","road"]),
"文艺复兴意大利":dict(objs=["renaissance","italy"],qs=["Italian Renaissance economy art","Renaissance city state culture"],
  slots=["renaissance","italy","econom","city","art","culture"]),
"白令陆桥":dict(objs=["bering","beringia"],qs=["Beringia land bridge peopling","Bering Strait paleogeography"],
  slots=["bering","bridge","peopling","paleogeograph","migration"]),
}
Q2={
"大平原":dict(objs=["great plains"],qs=["Great Plains grassland history","North American Great Plains settlement agriculture"],
  slots=["great plains","grassland","settle","agricultur","history"]),
"玛雅文明":dict(objs=["maya"],qs=["Maya civilization society politics","Maya lowlands state"],
  slots=["maya","civiliz","society","politic","state"]),
"安第斯山脉":dict(objs=["andes","andean"],qs=["Andes mountain geology","Andean uplift climate"],
  slots=["andes","andean","geolog","uplift","climate"]),
"印加帝国":dict(objs=["inca"],qs=["Inca empire administration","Inca road system state"],
  slots=["inca","empire","administrat","road","state"]),
"澳大利亚大陆":dict(objs=["australia","australian"],qs=["Australia continent geology overview","Australia climate continent"],
  slots=["australia","geolog","climate","continent","arid"]),
"澳大利亚原住民":dict(objs=["aboriginal","indigenous australian"],qs=["Aboriginal Australians society land","Australian Aboriginal prehistory"],
  slots=["aboriginal","indigenous","society","land","prehistor"]),
"波利尼西亚":dict(objs=["polynesia","polynesian"],qs=["Polynesian settlement navigation","Polynesian society islands"],
  slots=["polynesia","polynesian","settle","navigat","island","society"]),
"河流三角洲":dict(objs=["delta"],qs=["river delta evolution sediment","delta stratigraphy progradation"],
  slots=["delta","sediment","evolution","stratigraph","prograd"]),
}
spec_set = Q if BATCH=="1" else Q2
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
res={}
for t,spec in spec_set.items():
    cands=[]
    for q in spec["qs"]:
        for _ in range(3):
            d=cj("https://api.openalex.org/works?search="+urllib.parse.quote(q)+"&per_page=20&mailto=geo-encyclopedia@example.com")
            if d.get("results") is not None: break
            time.sleep(8)
        for w in (d.get("results") or []):
            if (w.get("type") or "")=="book-review": continue
            a=ab(w)
            if len(a)<400: continue
            ti=norm(w.get("title")); al=norm(a)
            if not any(norm(o) in ti for o in spec["objs"]): continue
            h=[s for s in spec["slots"] if norm(s) in al or norm(s) in ti]
            if len(h)<2: continue
            cited=w.get("cited_by_count") or 0
            if cited<10 and len(a)<800: continue
            cands.append({"oid":(w.get("id") or "").rsplit("/",1)[-1],"title":w.get("title"),
              "year":w.get("publication_year"),"cited":cited,"abs_len":len(a),"slots":h,"doi":w.get("doi","")})
        time.sleep(0.8)
    seen=set();u=[]
    for c in cands:
        if c["oid"] in seen: continue
        seen.add(c["oid"]);u.append(c)
    u.sort(key=lambda x:(len(x["slots"]),x["cited"]),reverse=True)
    res[t]={"cand":u[:3],"n":len(u)}
    print(f"== {t}: 候选{len(u)}")
    for c in u[:2]:
        print(f"     {c['cited']:>5}引 {c['abs_len']:>5}字 {c['year']} 《{c['title'][:54]}》 槽{c['slots'][:3]}")
out=f"round73_batch{BATCH}.json"
json.dump(res,open(os.path.join(ROOT,"reports",out),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n写入",out)