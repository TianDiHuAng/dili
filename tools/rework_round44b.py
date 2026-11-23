# -*- coding: utf-8 -*-
"""第44轮返工：把「0源」表述改为「来源无实测正文记录」；台账。"""
import json,os,re,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-23"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
S={s["id"]:s for s in json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]}
MIN=800
def hb(sid):
    note=(S.get(sid) or {}).get("note") or ""
    if "stub" in note.lower(): return False
    m=re.search(r"摘要长度\s*(\d+)\s*字符",note) or re.search(r"正文\s*(\d+)\s*字符",note) or re.search(r"摘要\s*(\d+)\s*字符",note)
    if m: return int(m.group(1))>=MIN
    m=re.search(r"(\d{3,7})\s*字节",note)
    if m: return int(m.group(1))>=MIN
    return None

# 修正措辞：所有「没有带正文/摘要的学术来源」表述
fixed=0
for e in T.values():
    pn=e.get("pending_notes") or ""
    if "经复核，本条在" in pn and "没有带正文/摘要的学术来源" in pn:
        pn=pn.replace("没有带正文/摘要的学术来源",
          "**没有可判定含正文的学术来源**（其来源记录中未记实测字符数，无法确认有无正文，第44轮统一口径记为「待实测」）")
        e["pending_notes"]=pn;fixed+=1

# 为「无实测记录」的来源补记实测（用 openalex API 取摘要长度）
unknown_sids=[]
for e in T.values():
    for sid in e["sources"]:
        if not sid.startswith("openalex-"): continue
        if hb(sid) is None: unknown_sids.append(sid)
unknown_sids=list(dict.fromkeys(unknown_sids))
print("待实测的 openalex 来源:",len(unknown_sids))
n=0
for sid in unknown_sids[:80]:
    oid=sid.replace("openalex-","")
    try:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","15","-A","Mozilla/5.0",
          f"https://api.openalex.org/works/{oid}?select=abstract_inverted_index,title"],capture_output=True,timeout=25)
        d=json.loads(p.stdout.decode("utf-8","ignore"))
        inv=d.get("abstract_inverted_index") or {}
        ln=sum(len(v) for v in inv.values())
        s=S.get(sid)
        if s is not None and ln>0 and "摘要长度" not in (s.get("note") or ""):
            s["note"]=(s.get("note") or "")+f" 摘要长度 {ln} 字符（第44轮实测）。"
            n+=1
    except Exception: pass
print("补记实测:",n)
save_docs(docs)
json.dump(list(S.values()),open(os.path.join(DATA,"sources.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=44
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("措辞修正:",fixed)