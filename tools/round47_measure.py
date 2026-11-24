# -*- coding: utf-8 -*-
"""第47轮：为「有来源但未实测」的条目实测各来源正文字符数（D104 补测量）。"""
import json,os,re,sys,subprocess,html as H,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]}
MIN=800
def hb(sid,e=None):
    notes=[(S.get(sid) or {}).get("note") or ""]
    if e is not None: notes.append(e.get("pending_notes") or "")
    for note in notes:
        if "stub" in note.lower(): return False
        for pat in (r"摘要长度\s*(\d+)\s*字符",r"正文\s*(\d+)\s*字符",r"摘要\s*(\d+)\s*字符",
                    r"正文\s*\*{0,2}([\d,]+)\s*字符"):
            m=re.search(pat,note)
            if m: return int(m.group(1).replace(",",""))>=MIN
        m=re.search(r"(\d{3,7})\s*字节",note)
        if m: return int(m.group(1))>=MIN
    return None
UNK=[]
for t,e in T.items():
    if any(hb(s,e) is None for s in e["sources"]): UNK.append(t)
print("未实测条目:",len(UNK),flush=True)

def strip_tags(h):
    for x in ("nav","header","footer","aside","script","style","form","noscript"):
        h=re.sub(rf"<{x}\b.*?</{x}>"," ",h,flags=re.I|re.S)
    return h
def measure(url,rx=None):
    try:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0",
                          "-o","-","-w","\n__HTTP__%{http_code}",url],capture_output=True,timeout=30)
        raw=p.stdout.decode("utf-8","ignore")
        if "__HTTP__" not in raw: return 0,0,0
        b,c=raw.rsplit("\n__HTTP__",1)
        code=int(c.strip() or 0)
        txt=re.sub(r"\s+"," ",H.unescape(re.sub(r"<[^>]+>"," ",strip_tags(b)))).strip()
        hits=len(re.findall(rx,txt,re.I)) if rx else 0
        return code,len(txt),hits
    except Exception: return 0,0,0

done=0
for t in UNK:
    e=T[t]
    changed=False
    for sid in e["sources"]:
        if hb(sid,e) is not None: continue
        s=S.get(sid) or {}
        url=s.get("url")
        if not url: continue
        rx=re.escape(t[:2]) if len(t)>=2 else None
        code,n,hits=measure(url,rx)
        tail=f" 【第47轮实测】strip 后正文 {n:,} 字符（HTTP {code}）。"
        if "第47轮实测" not in (s.get("note") or ""):
            s["note"]=(s.get("note") or "")+tail
            changed=True
        print(f"  {t:<16} {sid:<28} HTTP {code} 正文 {n:>7} 字符",flush=True)
        time.sleep(0.6)
    if changed:
        e["last_update"]=TODAY;done+=1
print("补测量条目:",done)
save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=47
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)

# 重算五分类
cat={"ge2":0,"one":0,"unmeasured":0}
for t,e in T.items():
    b=sum(1 for s in e["sources"] if hb(s,e) is True)
    u=sum(1 for s in e["sources"] if hb(s,e) is None)
    if b>=2: cat["ge2"]+=1
    elif b==1: cat["one"]+=1
    else: cat["unmeasured"]+=1
print("新分类：",cat)