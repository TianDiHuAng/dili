# -*- coding: utf-8 -*-
"""第93轮C：修 Rhine 书评；记录 D150/D151。"""
import json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from round2_apply import update_coverage, save_docs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data");TODAY="2026-11-24"
UNITS=["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
docs={u:json.load(open(os.path.join(DATA,u+".json"),encoding="utf-8")) for u in UNITS}
T={e["title"]:e for d in docs.values() for e in d["entries"]}
e=T["莱茵河"]
if "openalex-W2041834890" in e["sources"]:
    e["pending_notes"]=((e.get("pending_notes") or "")+
      " 【第93轮审计修正·书评】`openalex-W2041834890`（《The Rhine: An Eco-Biography, 1815-2000》**(review)**）"
      "标题括注 **(review)**、DOI 为 10.1353/tech.2005.0070（Technology and Culture 期刊的**书评**）、被引仅 1。"
      "OpenAlex 的 type 字段标为「学术文献」，**R25 只看 type 因而漏检**（D136 的再一次实例）。现降为旁证。").strip()
    e["last_update"]=TODAY; print("莱茵河：书评已降旁证")
save_docs(docs); update_coverage(docs)
print("完成")