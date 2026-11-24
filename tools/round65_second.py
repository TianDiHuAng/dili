# -*- coding: utf-8 -*-
"""第65轮B：统一测量口径（取最新 strip 值）+ 为 4 条补充类检索学术来源。"""
import json,os,re,sys,subprocess,urllib.parse,time,unicodedata
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]}

# ===== A 统一 s074 测量值（以第64轮 strip 实测为准）=====
s=S.get("s074-unicef-org")
if s:
    note=s.get("note") or ""
    # 标注冲突：旧文本提取 5455 vs 新 strip 750
    if "口径冲突" not in note:
        s["note"]=note+" 【口径冲突说明】本条曾记「正文 5,455 字符」（文本提取口径），第64轮 strip HTML 后实测为 **750 字符**（多为导航与卡片摘要）。两值并存时以 strip 值为准；750 < 800，故本条仅作入口页与案例引用，不作正文依据。"
        print("s074 已标注口径冲突（750 < 800）")

# ===== B 为 4 条补充类检索学术来源 =====
def norm(x):
    x=unicodedata.normalize("NFKD",(x or "").lower())
    return "".join(c for c in x if not unicodedata.combining(c))
Q={
"海洋生态系统":dict(objs=["ocean","marine","sea"],qs=["marine ecosystem services assessment","ocean ecosystem functioning review"],
  slots=["ecosystem","marine","ocean","service","function"]),
"保护与保育区体系":dict(objs=["protected area","conservation"],qs=["protected areas conservation effectiveness","global protected area network"],
  slots=["protected area","conservation","network","effectiveness","coverage"]),
"教育机会地域差异":dict(objs=["education"],qs=["education inequality geography","spatial inequality schooling access"],
  slots=["education","inequal","access","school","spatial"]),
"农业企业与价值链":dict(objs=["agribusiness","value chain","agricultur"],qs=["agricultural value chain development","agribusiness smallholder integration"],
  slots=["value chain","agribusiness","smallholder","market","integrat"]),
}
def cj(url):
    for _ in range(3):
        try:
            p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0",url],capture_output=True,timeout=35)
            s2=p.stdout.decode("utf-8","ignore")
            if s2.strip().startswith("{"): return json.loads(s2)
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
for t,spec in Q.items():
    best=None
    for q in spec["qs"]:
        for _ in range(3):
            d=cj("https://api.openalex.org/works?search="+urllib.parse.quote(q)+"&per_page=15&mailto=geo-encyclopedia@example.com")
            if d.get("results") is not None: break
            time.sleep(8)
        for w in (d.get("results") or []):
            a=ab(w)
            if len(a)<800: continue
            ti=norm(w.get("title")); al=norm(a)
            if not any(norm(o) in ti for o in spec["objs"]): continue
            hit=[s2 for s2 in spec["slots"] if norm(s2) in al or norm(s2) in ti]
            if len(hit)<2: continue
            cited=w.get("cited_by_count") or 0
            if cited<10: continue
            rec={"oid":(w.get("id") or "").rsplit("/",1)[-1],"title":w.get("title"),"year":w.get("publication_year"),
                 "cited":cited,"abs_len":len(a),"slots":hit,"doi":w.get("doi","")}
            if best is None or cited>best["cited"]: best=rec
        time.sleep(1)
    res[t]=best
    print(f"{'OK' if best else '--'} {t:<16} {(best['title'][:44] if best else '-')} ({best.get('year') if best else ''}) cite={best.get('cited') if best else ''}",flush=True)
json.dump(res,open(os.path.join(ROOT,"reports","round65_second.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n命中:",sum(1 for v in res.values() if v),"/",len(Q),flush=True)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)