# -*- coding: utf-8 -*-
"""第71轮A：统一 hb() 口径——别名页不计内容源（与 D135 层级判定一致）。"""
import os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 修 round62_gaps.py
p=os.path.join(ROOT,"tools","round62_gaps.py")
t=open(p,encoding="utf-8").read()
if "ALIAS_EXCL" not in t:
    t=t.replace('def is_data(sid): return sid.startswith(("wb-","usgs-eq","noaa-current","ats-parties","wikidata-"))',
'''ALIAS_EXCL = ("britannica-regions", "wikipedia-regions", "un-m49", "ap-human-geo", "s010-unesco-org")

def is_data(sid): return sid.startswith(("wb-","usgs-eq","noaa-current","ats-parties","wikidata-"))''')
    t=t.replace('''def hb(sid,e):
    if is_data(sid): return False''',
'''def hb(sid,e):
    if is_data(sid): return False
    if sid in ALIAS_EXCL: return False      # D135：别名页/索引页不计内容源''')
    open(p,"w",encoding="utf-8").write(t)
    print("round62_gaps.py 已排除别名页")
else:
    print("已存在")

# 修 check.py 的 hb 等价逻辑不受影响（R22 已排除）；修 finalize 脚本模板
for f in ("finalize_round69.py","finalize_round70.py"):
    fp=os.path.join(ROOT,"tools",f)
    if not os.path.exists(fp): continue
    s=open(fp,encoding="utf-8").read()
    if "ALIAS_EXCL" not in s:
        s=s.replace('def is_data(sid): return sid.startswith(("wb-","usgs-eq","noaa-current","ats-parties","wikidata-"))',
'''ALIAS_EXCL = ("britannica-regions", "wikipedia-regions", "un-m49", "ap-human-geo", "s010-unesco-org")

def is_data(sid): return sid.startswith(("wb-","usgs-eq","noaa-current","ats-parties","wikidata-"))''')
        s=s.replace('''    if is_data(sid): return False
    for note in''','''    if is_data(sid): return False
    if sid in ALIAS_EXCL: return False
    for note in''')
        open(fp,"w",encoding="utf-8").write(s)
print("finalize 模板已同步")