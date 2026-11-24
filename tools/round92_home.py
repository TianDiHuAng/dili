# -*- coding: utf-8 -*-
"""第92轮A：D149——机构「首页/导航页」不算内容来源。"""
import os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p=os.path.join(ROOT,"tools","assess.py")
t=open(p,encoding="utf-8").read()
if "D149" in t:
    print("已存在"); raise SystemExit(1)
t=t.replace('SHELL_MARK = "空壳页判定"',
'''SHELL_MARK = "空壳页判定"
# D149：机构首页/导航页即便字符数达标，也不是内容页（抓到的多为导航与新闻列表）
HOME_TITLES = ("home", "home -", "home |", "homepage", "index", "welcome")


def is_homepage(src):
    """标题形如「Home - 某某」/「Home | 某某」者判为机构首页。"""
    ti = ((src or {}).get("title") or "").strip().lower()
    if not ti:
        return False
    # 去掉站点名后缀后判断第一个词
    head = re.split(r"[|\\-–—]", ti)[0].strip()
    return head in HOME_TITLES''')
t=t.replace('''    if SHELL_MARK in (src.get("note") or ""):
        return False''',
'''    if SHELL_MARK in (src.get("note") or ""):
        return False
    if is_homepage(src):
        return False''')
t=t.replace('''    if SHELL_MARK in (src.get("note") or ""):
        return "weak"      # 空壳页最多算弱来源''',
'''    if SHELL_MARK in (src.get("note") or ""):
        return "weak"      # 空壳页最多算弱来源
    if is_homepage(src):
        return "weak"      # D149：首页/导航页最多算弱来源''')
open(p,"w",encoding="utf-8").write(t)
print("D149 已加入 assess.py")