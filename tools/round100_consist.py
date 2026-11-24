# -*- coding: utf-8 -*-
"""第100轮：D147 交叉一致性检查——strength / content_count / level_of / G3 分类。"""
import sys,os,json,importlib
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import assess; importlib.reload(assess)
from assess import (load_sources, load_entries, strength, has_content,
                    content_count, count_entry, level_of, src_domain, UNITS)
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S=load_sources();T=load_entries(UNITS)
BAD=[]
def bad(msg):
    BAD.append(msg); print("  ⚠", msg)

print("=== 1. content_count 只能 ≤ strong 数 ===")
for t,e in T.items():
    c=count_entry(e,S); cc=content_count(e,S)
    if cc>c["strong"]: bad(f"{t}: content_count={cc} > strong={c['strong']}")

print("=== 2. strong>0 且全部通过 has_content 时，content_count 应等于去重后的域数 ===")
for t,e in T.items():
    strong_ok=[sid for sid in e["sources"]
               if strength(sid,S.get(sid,{}),e)=="strong" and has_content(sid,S.get(sid,{}),e)]
    doms=[]
    for sid in strong_ok:
        d=src_domain(sid,S.get(sid,{}))
        doms.append(d if d else f"__{sid}")
    uniq=len(set(doms))
    cc=content_count(e,S)
    if uniq!=cc: bad(f"{t}: 去重域数={uniq} vs content_count={cc}")

print("=== 3. level_of 与 strong/content_count 的对应 ===")
for t,e in T.items():
    lv=level_of(e,S); c=count_entry(e,S); cc=content_count(e,S)
    if lv=="A" and not (c["strong"]>=2 and cc>=2): bad(f"{t}: A 但 strong={c['strong']} cc={cc}")
    if lv=="A" and cc<2: bad(f"{t}: A 但 content_count={cc}<2")
    if lv=="B" and c["strong"]!=1: bad(f"{t}: B 但 strong={c['strong']}")
    if lv=="C" and c["strong"]>0: bad(f"{t}: C 但 strong={c['strong']}")

print("=== 4. G3 分类与 content_count 一致 ===")
sp=json.load(open(os.path.join(ROOT,"reports","round77_g3split.json"),encoding="utf-8"))
g3=set(sp["G3a"]["entries"])|set(sp["G3b"]["entries"])
for t,e in T.items():
    cc=content_count(e,S); lv=level_of(e,S)
    should = (cc==1 and lv!="D")
    if should and t not in g3: bad(f"{t}: cc=1 非D 但未列入 G3")
    if (not should) and t in g3: bad(f"{t}: 列入 G3 但 cc={cc} lv={lv}")
    if t in sp["G3a"]["entries"]:
        c=count_entry(e,S)
        if not (c["side"]>0 or c["weak"]>0): bad(f"{t}: 在 G3a 但无 side/weak")
    if t in sp["G3b"]["entries"]:
        c=count_entry(e,S)
        if (c["side"]>0 or c["weak"]>0): bad(f"{t}: 在 G3b 但有 side/weak={c['side']}/{c['weak']}")

print("=== 5. evidence_level.json 与实时重算一致 ===")
ev=json.load(open(os.path.join(ROOT,"data","evidence_level.json"),encoding="utf-8"))["levels"]
for t,e in T.items():
    rec=ev.get(t) or {}
    if rec.get("level")!=level_of(e,S): bad(f"{t}: 记录 {rec.get('level')} vs 重算 {level_of(e,S)}")

print("=== 6. 无效/未使用的来源 id ===")
allsrc=set(S)
used=set()
for e in T.values(): used.update(e.get("sources",[]))
print(f"  库中来源 {len(allsrc)}，被引用 {len(used & allsrc)}，未被引用 {len(allsrc-used)}")

print(f"\n{'='*54}\n一致性问题 {len(BAD)} 处")
sys.exit(1 if BAD else 0)