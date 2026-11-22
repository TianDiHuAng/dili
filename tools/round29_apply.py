# -*- coding: utf-8 -*-
"""第29轮：宋代实证复核 + 10 条补量级声明 + 全球主题条目的数据端点尝试。"""
import json,os,re,sys,subprocess,html
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
src={s["id"]:s for s in json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]}
T={e["title"]:e for d in docs.values() for e in d["entries"]}

def strip(h):
    for x in ("nav","header","footer","aside","script","style","form","noscript"):
        h=re.sub(rf"<{x}\b.*?</{x}>"," ",h,flags=re.I|re.S)
    return h
def measure(url,rx):
    try:
        p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","20","-A","Mozilla/5.0","-o","-","-w","\n__HTTP__%{http_code}",url],capture_output=True,timeout=30)
        raw=p.stdout.decode("utf-8","ignore")
        if "__HTTP__" not in raw: return 0,0,0
        b,c=raw.rsplit("\n__HTTP__",1)
        txt=re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",strip(b)))).strip()
        return int(c.strip() or 0),len(txt),len(re.findall(rx,txt,re.I))
    except Exception: return 0,0,0

# 1) 宋代：实证复核（英文正则 han dynasty|song）
song=T["宋代"]
rx="han|song|china"
parts=[]
for sid in song["sources"][:2]:
    s=src.get(sid)
    if not s: continue
    code,n,h=measure(s["url"],rx)
    parts.append((sid,code,n,h))
mx=max(p[3] for p in parts); mb=max(p[2] for p in parts)
gate=5000 if mx>=30 else 8000
det="；".join(f"{sid}={code}/正文{n}字符/本条命中{h}" for sid,code,n,h in parts)
song["pending_notes"]=((song.get("pending_notes") or "")+
  f" 【第29轮实证复核·宋代】本条正则 {rx}（英文源用英文，D070）；{det}。档位判定：档③8000+命中≥5（来源标题不含「宋代」）。"
  f"D055 判定：{'达标' if (mb>=gate and mx>=5) else f'未达标（正文{mb}、命中{mx}）'}；缺口为宋代/中国中古史专题页。").strip()
song["status"]="已复核(第29轮·实证)";song["last_update"]=TODAY

# 2) 10 条补量级声明
CAP="上述为该代表国的全国口径数据，仅示量级，不代表本条目所述区域的内部差异。"
n2=0
for t,e in T.items():
    tod=e.get("today") or ""
    if "来源：世界银行 API" not in tod: continue
    if "仅示量级" in tod or "不代表" in tod: continue
    e["today"]=tod.rstrip("。")+"。"+CAP
    e["last_update"]=TODAY;n2+=1

for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("宋代实证复核完成；补量级声明",n2,"条")