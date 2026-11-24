# -*- coding: utf-8 -*-
"""第102轮：D157——D141 不该要求 side==0；指标解读类有旁证是正常的。"""
import os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p=os.path.join(ROOT,"tools","assess.py")
t=open(p,encoding="utf-8").read()
if "D157" in t:
    print("已存在"); raise SystemExit(1)
old='''        if is_institutional and c["data"] > 0 and c["side"] == 0:
            return "D"'''
new='''        # D157：不再要求 side==0——指标解读类条目本来就只有一篇机构长文，
        # 其余来源被判旁证（side）是常态，不该因此阻止它归入 D。
        if is_institutional and c["data"] > 0:
            return "D"'''
if old in t:
    t=t.replace(old,new); open(p,"w",encoding="utf-8").write(t); print("D157 已应用")
else:
    print("⚠ 未匹配"); raise SystemExit(1)