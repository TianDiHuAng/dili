# -*- coding: utf-8 -*-
"""第93轮A：D150——同一域名下多页最多计 1 个内容源；修 Rhine 书评。"""
import os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p=os.path.join(ROOT,"tools","assess.py")
t=open(p,encoding="utf-8").read()
if "D150" in t:
    print("已存在"); raise SystemExit(1)

# 加域名工具函数
t=t.replace('''def is_homepage(src):''',
'''def src_domain(sid, src):
    """来源所属域名；openalex-/wikidata- 等数据类来源返回 None（不同论文视为独立）。"""
    if not sid or sid.startswith("openalex-") or sid.startswith("wikidata-"):
        return None
    m = re.match(r"https?://([^/]+)", (src or {}).get("url") or "")
    return m.group(1).lower() if m else None


def is_homepage(src):''')

# content_count 加同域去重
old='''    n = 0
    for sid in entry.get("sources", []):
        g = strength(sid, sources.get(sid) or {}, entry)
        if g != "strong":
            continue
        if not has_content(sid, sources.get(sid) or {}, entry):
            continue
        n += 1
    return n'''
new='''    n = 0
    seen_domains = set()
    for sid in entry.get("sources", []):
        src = sources.get(sid) or {}
        g = strength(sid, src, entry)
        if g != "strong":
            continue
        if not has_content(sid, src, entry):
            continue
        # D150：同一域名下多个页面最多计 1 个内容源（互证须来自不同出版者）
        dom = src_domain(sid, src)
        if dom:
            if dom in seen_domains:
                continue
            seen_domains.add(dom)
        n += 1
    return n'''
if old in t:
    t=t.replace(old,new); print("content_count 已加同域去重（D150）")
else:
    print("⚠ 未匹配 content_count 原文"); raise SystemExit(1)
open(p,"w",encoding="utf-8").write(t)