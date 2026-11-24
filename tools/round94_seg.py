# -*- coding: utf-8 -*-
"""第94轮D：D152——strength 须检查 sid 的**所有**出现位置，任一含豁免词即降级。"""
import os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p=os.path.join(ROOT,"tools","assess.py")
t=open(p,encoding="utf-8").read()
if "D152" in t:
    print("已存在"); raise SystemExit(1)
# 找到 strength 内的 seg 计算逻辑并替换
old_pat = re.compile(r'    # 在条目备注里找该 sid 的段落.*?\n    seg = .*?\n', re.S)
m = old_pat.search(t)
print("匹配到 seg 逻辑:", bool(m))
if m:
    seg_block = m.group(0)
    print(seg_block[:400])
else:
    # 直接搜 seg 相关行
    for mm in re.finditer(r'.{0,200}seg.{0,300}', t, re.S):
        print("---", mm.group(0)[:400])
PY = None