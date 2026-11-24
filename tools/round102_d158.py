# -*- coding: utf-8 -*-
"""第102轮B：D158——指标解读类的数据证据可来自 today 字段，不限于 wb- 端点。"""
import os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p=os.path.join(ROOT,"tools","assess.py")
t=open(p,encoding="utf-8").read()
if "D158" in t:
    print("已存在"); raise SystemExit(1)
old='''        if is_institutional and c["data"] > 0:
            return "D"'''
new='''        # D158：数据证据不限于 wb-/usgs- 等 API 端点——
        # 若 today 字段自述「来源：…指标…」且**只说明数值、不作叙事断言**，同样属指标解读类。
        td = (entry.get("today") or "")
        has_indicator = ("指标" in td) or ("Climate at a Glance" in td) or ("世界银行 API" in td)
        is_numeric_today = bool(td) and has_indicator and ("（本条的当代指标不在本页展开。）" not in td)
        if is_institutional and (c["data"] > 0 or is_numeric_today):
            return "D"'''
if old in t:
    t=t.replace(old,new); open(p,"w",encoding="utf-8").write(t); print("D158 已应用")
else:
    print("⚠ 未匹配"); raise SystemExit(1)