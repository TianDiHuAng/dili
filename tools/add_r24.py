# -*- coding: utf-8 -*-
"""第67轮A：R24——落点声明中引号括起的短语必须在正文出现（悬空落点检测）。"""
import os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p=os.path.join(ROOT,"tools","check.py")
t=open(p,encoding="utf-8").read()
if "R24" in t:
    print("R24 已存在"); raise SystemExit
t=t.replace("            check_shell_not_content(e, src_by_id)",
            "            check_shell_not_content(e, src_by_id)\n            check_dangling_landing(e)")
t=t.replace('SHELL_MARK = "空壳页判定"',
'''BODY_FIELDS = ("definition", "overview", "geo", "influence", "polities", "connections", "today", "time_or_place")


def check_dangling_landing(e):
    """R24（D131）：备注里「本条『X』据此」的 X 必须出现在同条目某个正文字段中。"""
    pn = e.get("pending_notes") or ""
    body = " ".join((e.get(f) or "") for f in BODY_FIELDS)
    body_n = re.sub(r"\\s+", "", body)
    # 只检查「本条『…』据此 / 本条「…」据此」形态
    for m in re.finditer(r"本条[『「]([^』」]{6,120})[』」][^。]{0,20}据此", pn):
        phrase = re.sub(r"\\s+", "", m.group(1))
        # 去掉引号内常见的修饰符后比较
        probe = re.sub(r"[\\*\\s]", "", phrase)
        if probe and probe not in body_n:
            err(f"R24 {e['id']}: 落点句「{phrase[:30]}…」在正文字段中不存在（悬空落点，D131）")


SHELL_MARK = "空壳页判定"''')
open(p,"w",encoding="utf-8").write(t)
print("R24 已加入 check.py")