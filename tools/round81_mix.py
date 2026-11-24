# -*- coding: utf-8 -*-
"""第81轮：核心 G3b 5 条 + 重要剩余 7 条。"""
import subprocess,json,os,urllib.parse,time,unicodedata
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def norm(x):
    x=unicodedata.normalize("NFKD",(x or "").lower())
    return "".join(c for c in x if not unicodedata.combining(c))
SPEC={
# 核心 5（换角度）
"撒哈拉沙漠":(["sahara","saharan"],["Sahara desert geomorphology","Sahara environment human history","Sahara aridification"],
  ["sahara","desert","geomorph","environment","history","aridif"]),
"东非大裂谷":(["east african rift","rift valley","great rift"],["East African Rift system evolution","East African rift lakes climate"],
  ["rift","evolution","lake","climate","tecton","plume"]),
"印度河文明":(["indus","harappan"],["Indus Valley Civilization urbanization","Harappan state society"],
  ["indus","harappan","urban","state","society","civiliz"]),
"印加帝国":(["inca","tawantinsuyu"],["Inca state economy labor","Inca political organization empire"],
  ["inca","state","econom","labor","politic","organiz"]),
"澳大利亚原住民":(["aboriginal","indigenous australian"],["Australian Aboriginal land management","Aboriginal Australia culture language"],
  ["aboriginal","indigenous","land","culture","language","management"]),
# 重要剩余 7
"萨珊波斯":(["sasanian","sassanian"],["Sasanian empire state society","Sasanian Iran polity"],
  ["sasanian","empire","state","society","polity"]),
"吠陀时代":(["vedic"],["Vedic period social organization","Vedic India polity"],
  ["vedic","social","organiz","polity","india"]),
"明清":(["ming","qing"],["Ming Qing economy state","late imperial China society"],
  ["ming","qing","econom","state","society"]),
"马来群岛":(["malay","srivijaya","majapahit"],["Srivijaya maritime state","Malay archipelago polities"],
  ["srivijaya","malay","maritime","state","polities"]),
"河中地区":(["transoxiana","sogdian","samarkand"],["Sogdian trade network urban","Transoxiana cities economy"],
  ["sogdian","transoxiana","trade","urban","econom","city"]),
"洋流":(["ocean current","circulation"],["global ocean circulation","meridional overturning circulation"],
  ["circulation","current","ocean","global","overturning"]),
"气候带":(["climate zone","koppen"],["Koppen climate classification","global climate zones mapping"],
  ["climate zone","classification","koppen","global","mapping"]),
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
    print(f"{'OK' if u else '--'} {t:<12} {(u[0]['title'][:42] if u else '-')} ({u[0]['year'] if u else ''}) cite={u[0]['cited'] if u else ''} abs={u[0]['abs_len'] if u else ''} 候选{len(u)}",flush=True)
json.dump(res,open(os.path.join(ROOT,"reports","round81_mix.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n命中:",sum(1 for v in res.values() if v["cand"]),"/",len(SPEC),flush=True)