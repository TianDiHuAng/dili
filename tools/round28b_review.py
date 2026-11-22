# -*- coding: utf-8 -*-
"""第28轮：8 条剩余无复核标记 L2 的实证复核（英文正则，D070）。"""
import json,os,re,sys,subprocess,html
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-22"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
src={s["id"]:s for s in json.load(open(os.path.join(DATA,"sources.json"),encoding="utf-8"))["sources"]}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
RX={"全球气温距平":"global temperature|temperature anomaly","二氧化碳排放清单":"co2|emission",
 "农业企业与价值链":"agribusiness|value chain|farm","渔业资源":"fisher","水资源管理":"water",
 "卫星遥感地表观测":"landsat|satellite","荒漠化":"desertif","沙尘暴":"dust|sandstorm",
 "大洋洲":"oceania|pacific"}
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
cnt=0
for t,rx in RX.items():
    e=T.get(t)
    if not e: continue
    parts=[]
    for sid in e["sources"][:2]:
        s=src.get(sid)
        if not s: continue
        code,n,h=measure(s["url"],rx)
        parts.append((sid,code,n,h))
    if not parts: continue
    mx=max(p[3] for p in parts); mb=max(p[2] for p in parts)
    gate=5000 if mx>=30 else 8000
    ok=mb>=gate and mx>=3
    det="；".join(f"{sid}={code}/正文{n}字符/本条命中{h}" for sid,code,n,h in parts)
    tier="档①5000" if mx>=30 else "档②/③8000"
    verdict=f"达标（{tier}：正文{mb}、命中{mx}）" if ok else f"未达标（{tier}：正文{mb}、命中{mx}）"
    e["pending_notes"]=((e.get("pending_notes") or "")+
      f" 【第28轮实证复核·{t}】本条正则 {rx}（英文源用英文，D070）；{det}。档位判定：{tier}。D055 判定：{verdict}。"
      + ("" if ok else f"缺口为「{t}」主题专题页。")).strip()
    e["status"]=(e.get("status") or "")+"·已复核(第28轮)"
    e["last_update"]=TODAY;cnt+=1
for u,d in docs.items(): json.dump(d,open(os.path.join(DATA,u+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
notes=[e.get("pending_notes") or "" for e in T.values() if "第28轮实证复核" in (e.get("pending_notes") or "")]
print("复核",cnt,"唯一",len(set(notes)),"/",len(notes))