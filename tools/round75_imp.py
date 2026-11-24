# -*- coding: utf-8 -*-
"""第75轮：批量处理 G3 条目（按 tier），自动生成对象词与检索式。"""
import subprocess,json,os,urllib.parse,time,unicodedata,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
def norm(x):
    x=unicodedata.normalize("NFKD",(x or "").lower())
    return "".join(c for c in x if not unicodedata.combining(c))

# 条目 → (对象词, 两条检索式, 主题槽)
SPEC={
"埃塞俄比亚高原":(["ethiopia","ethiopian"],["Ethiopian highlands geology climate","Ethiopia highland environment"],["ethiopia","highland","geolog","climate","environment"]),
"马格里布":(["maghreb","maghrib"],["Maghreb history society","Maghrib region economy"],["maghreb","maghrib","history","society","econom"]),
"古埃及新王国":(["new kingdom","egypt"],["New Kingdom Egypt empire","Egypt New Kingdom administration"],["new kingdom","egypt","empire","administrat","state"]),
"阿拉伯征服北非":(["arab conquest","islamic conquest"],["Arab conquest North Africa","Islamic conquest Maghrib"],["conquest","north africa","maghrib","islamic","arab"]),
"加纳帝国":(["ghana","wagadu"],["Ghana empire Wagadu","Wagadu state trade"],["ghana","wagadu","empire","state","trade"]),
"桑海帝国":(["songhai"],["Songhai empire Niger","Songhai state administration"],["songhai","empire","state","niger","administrat"]),
"大津巴布韦":(["zimbabwe","great zimbabwe"],["Great Zimbabwe state society","Zimbabwe archaeology state"],["zimbabwe","state","society","archaeolog","trade"]),
"斯瓦希里海岸":(["swahili"],["Swahili coast trade towns","Swahili city states Indian Ocean"],["swahili","trade","town","city","indian ocean"]),
"古巴比伦":(["babylon","babylonia"],["Babylonia state society","Babylon city administration"],["babylon","babylonia","state","society","administrat"]),
"亚述帝国":(["assyria","assyrian"],["Neo-Assyrian empire administration","Assyrian state ideology"],["assyria","empire","administrat","state","ideolog"]),
"帕提亚帝国":(["parthia","parthian"],["Parthian empire administration","Parthia state society"],["parthia","empire","administrat","state","society"]),
"萨珊波斯":(["sasanian","sassanian"],["Sasanian empire state","Sasanian Iran administration"],["sasanian","sassanian","empire","state","administrat"]),
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
res={}
for t,(objs,qs,slots) in SPEC.items():
    cands=[]
    for q in qs:
        for _ in range(3):
            d=cj("https://api.openalex.org/works?search="+urllib.parse.quote(q)+"&per_page=20&mailto=geo-encyclopedia@example.com")
            if d.get("results") is not None: break
            time.sleep(8)
        for w in (d.get("results") or []):
            if (w.get("type") or "")=="book-review": continue
            a=ab(w)
            if len(a)<400: continue
            ti=norm(w.get("title")); al=norm(a)
            if not any(norm(o) in ti for o in objs): continue
            h=[s for s in slots if norm(s) in al or norm(s) in ti]
            if len(h)<2: continue
            cited=w.get("cited_by_count") or 0
            if cited<10 and len(a)<800: continue
            cands.append({"oid":(w.get("id") or "").rsplit("/",1)[-1],"title":w.get("title"),
              "year":w.get("publication_year"),"cited":cited,"abs_len":len(a),"slots":h,"doi":w.get("doi","")})
        time.sleep(0.7)
    seen=set();u=[]
    for c in cands:
        if c["oid"] in seen: continue
        seen.add(c["oid"]);u.append(c)
    u.sort(key=lambda x:(len(x["slots"]),x["cited"]),reverse=True)
    res[t]={"cand":u[:3],"n":len(u)}
    print(f"{'OK' if u else '--'} {t:<12} {(u[0]['title'][:44] if u else '-')} ({u[0]['year'] if u else ''}) cite={u[0]['cited'] if u else ''} 候选{len(u)}",flush=True)
json.dump(res,open(os.path.join(ROOT,"reports","round75_imp1.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n命中:",sum(1 for v in res.values() if v["cand"]),"/",len(SPEC),flush=True)