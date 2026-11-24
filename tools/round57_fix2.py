# -*- coding: utf-8 -*-
"""第57轮B：修河中地区（删碰撞源、清理孤儿引用、补登记2023 Bukhara）。"""
import json,os,re,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
P=os.path.join(DATA,"sources.json");sd=json.load(open(P,encoding="utf-8"));S={s["id"]:s for s in sd["sources"]};have=set(S)

tr=T["河中地区"]
# 1 删除碰撞源（西地中海沙沉积）
for bad in ("openalex-W2072212795","openalex-W4323830249"):
    if bad in tr["sources"]: tr["sources"]=[s for s in tr["sources"] if s!=bad]
# 2 清理孤儿引用（2023 Bukhara 的句子，该来源不在 sources）
tr["influence"]=re.sub(r" 所引 2023 年《Food globalization[^。]*。","",tr.get("influence") or "")
tr["pending_notes"]=((tr.get("pending_notes") or "")+
  " 【第57轮修·两点】① 撤出 W2072212795（西地中海沙沉积）与 W4323830249（PPNB 小雕像指纹）——两者均与河中无关；"
  "② 清理 influence 中引用 2023 年《Food globalization…Bukhara》的句子——**该来源并未实际登记成功**（第53轮登记的 DOI 未能解析到 OpenAlex 记录），属孤儿引用，R18 已检出。").strip()
tr["last_update"]=TODAY

# 3 补登记 2023 Bukhara（重新解析 DOI）
CAND=["10.1007/s12520-023-01730-7","10.1007/s12520-023-01730-8"]
done=False
for doi in CAND:
    for _ in range(3):
        try:
            p=subprocess.run(["curl","-L","-sS","--ssl-no-revoke","--compressed","-m","25","-A","Mozilla/5.0",
              f"https://api.openalex.org/works/https://doi.org/{doi}"],capture_output=True,timeout=35)
            w=json.loads(p.stdout.decode("utf-8","ignore"))
            if w.get("id"):
                oid=(w.get("id") or "").rsplit("/",1)[-1];sid=f"openalex-{oid}"
                if sid not in have:
                    sd["sources"].append({"id":sid,"title":f"OpenAlex {oid} — {w.get('title')}",
                      "author":"OpenAlex（开放学术知识图谱，CC0 元数据）","year":w.get("publication_year"),
                      "type":"学术文献","url":f"https://api.openalex.org/works/{oid}","url2":f"https://doi.org/{doi}",
                      "link_ok":True,"verified":True,"page_title":(w.get("title") or "")[:200],
                      "note":f"OpenAlex 作品 {oid}（DOI {doi}）；{w.get('publication_year')}年；被引 {w.get('cited_by_count')}。第57轮重新解析登记。"})
                    have.add(sid)
                tr["sources"]=list(dict.fromkeys(tr["sources"]+[sid]))
                tr["influence"]=((tr.get("influence") or "")+
                  f" 所引 {w.get('publication_year')} 年《{(w.get('title') or '')[:60]}》以布哈拉的植物考古讨论作物与商路带来的食物交流；本条「河中作为东西作物与技术转运地」据此。").strip()
                tr["pending_notes"]=((tr.get("pending_notes") or "")+f" 【第57轮补登记】{sid}（DOI {doi}）已重新解析登记。").strip()
                done=True
                break
        except Exception: pass
        time.sleep(4)
    if done: break
print("Bukhara 补登记:",done)
save_docs(docs)
json.dump(sd,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
cov=json.load(open(os.path.join(DATA,"coverage.json"),encoding="utf-8"))
cov["updated"]=TODAY;cov["round"]=57
json.dump(cov,open(os.path.join(DATA,"coverage.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
update_coverage(docs)
print("河中 sources:",T["河中地区"]["sources"])