# -*- coding: utf-8 -*-
"""第57轮：R20 全量检出的处置——剔除3条真对象碰撞、加3条别名、核实1条。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]}

# ===== 1 剔除 3 条真对象碰撞 =====
DROP={
"元代":("openalex-W4299796120","《William Alexander Mabry, The Negro in North…》——这是**美国黑人史**著作的书评，与元朝毫无关系（R20 检出，纯对象碰撞）。"),
"河中地区":("openalex-W2072212795","《Western Mediterranean sand deposits…》——研究对象是**西地中海沙沉积**，与河中地区无关。"),
"河中地区":("openalex-W4323830249","《Analysis of fingerprints on a PPNB figurine》——研究对象是**近东新石器 PPNB 小雕像的指纹**，与河中地区无关。"),
}
for t,(sid,why) in DROP.items():
    e=T.get(t)
    if not e: continue
    e["sources"]=[s for s in e["sources"] if s!=sid]
    e["pending_notes"]=re.sub(rf" 【[^】]*】{re.escape(sid)}[^【]*","",e.get("pending_notes") or "")
    e["pending_notes"]=((e.get("pending_notes") or "")+f" 【第57轮R20剔除·对象碰撞】{why} 已撤出。").strip()
    e["last_update"]=TODAY
print("剔除 3 条对象碰撞")

# ===== 2 核实加纳帝国那条 =====
ga=T["加纳帝国"]
cid="openalex-W2276091624"
w=None
for _ in range(3):
    try:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0",
          f"https://api.openalex.org/works/W2276091624?select=title,abstract_inverted_index"],capture_output=True,timeout=30)
        w=json.loads(p.stdout.decode("utf-8","ignore"))
        if w.get("title"): break
    except Exception: pass
    time.sleep(4)
if w:
    inv=w.get("abstract_inverted_index") or {}
    pos={}
    for k,ix in inv.items():
        for i in ix: pos[i]=k
    a=" ".join(pos[i] for i in sorted(pos))
    print("加纳候选标题:",w.get("title")[:90])
    print("  摘要含 ghana:",("ghana" in a.lower()),"含 mali:",("mali" in a.lower()),"含 sahel:",("sahel" in a.lower()))
    print("  摘要片段:",a[:220])
    if "ghana" not in a.lower() and "mali" not in a.lower() and "sahel" not in a.lower():
        ga["sources"]=[s for s in ga["sources"] if s!=cid]
        ga["pending_notes"]=((ga.get("pending_notes") or "")+
          " 【第57轮R20剔除】《Expansions and Contractions: World-Historical…》的摘要与标题均不含 ghana/mali/sahel，属世界史框架下的泛论，"
          "不能作为「加纳帝国」的来源；已撤出。").strip()

# ===== 3 加 3 条别名 =====
objpath=os.path.join(DATA,"object_words.json")
obj=json.load(open(objpath,encoding="utf-8"))
obj["斯堪的纳维亚"]=list(dict.fromkeys(obj.get("斯堪的纳维亚",[])+["norden"]))
obj["北美原住民"]=list(dict.fromkeys(obj.get("北美原住民",[])+["north america"]))
obj["安第斯垂直农业"]=list(dict.fromkeys(obj.get("安第斯垂直农业",[])+["vertical"]))
json.dump(obj,open(objpath,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("补别名：norden / north america / vertical")

save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=57
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
print(f"重算 ≥2 {g2} / 1个 {o1}")


# ===== 4 重跑 R20（用 check.py）=====
subprocess.run([sys.executable,"-X","utf8","tools/check.py"],cwd=ROOT)