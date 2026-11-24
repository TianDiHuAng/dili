# -*- coding: utf-8 -*-
"""第90轮C：修 content_count——排除 side（D146）。这是 D138「单一实现」的第三次破裂。"""
import os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p=os.path.join(ROOT,"tools","assess.py")
t=open(p,encoding="utf-8").read()
if "D146" in t:
    print("已存在"); raise SystemExit
old='''def content_count(entry, sources):
    """该条目「有正文的内容来源」个数。"""
    return sum(1 for sid in entry.get("sources", [])
               if has_content(sid, sources.get(sid) or {}, entry))'''
new='''def content_count(entry, sources):
    """该条目「有正文的内容来源」个数。
    D146：必须与 strength() 同源——被标为 side（旁证/剔除/降级/不作）、alias、data、
    书评、空壳页的来源**一律不计**。此前直接用 has_content()，而 has_content 不认 side 标记，
    导致「已降旁证」的来源仍被算作内容源，虚增内容源个数、虚低 G3。"""
    n = 0
    for sid in entry.get("sources", []):
        g = strength(sid, sources.get(sid) or {}, entry)
        if g != "strong":
            continue
        if not has_content(sid, sources.get(sid) or {}, entry):
            continue
        n += 1
    return n'''
if old in t:
    t=t.replace(old,new); print("content_count 已修（D146）")
else:
    m=re.search(r'def content_count\(entry, sources\):.*?(?=\ndef )', t, re.S)
    if not m: print("⚠ 未找到 content_count"); raise SystemExit(1)
    t=t[:m.start()]+new+"\n\n"+t[m.end():]
    print("content_count 已替换（D146）")
open(p,"w",encoding="utf-8").write(t)