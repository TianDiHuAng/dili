# -*- coding: utf-8 -*-
"""第65轮A：R23——空壳页不得被称内容来源/第二来源。"""
import os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p=os.path.join(ROOT,"tools","check.py")
t=open(p,encoding="utf-8").read()
if "R23" in t:
    print("R23 已存在"); raise SystemExit
t=t.replace("            check_level_consistency(e, EV_MAP, src_by_id)",
            "            check_level_consistency(e, EV_MAP, src_by_id)\n            check_shell_not_content(e, src_by_id)")
t=t.replace("MIN_STRONG_CITED = 10",
'''SHELL_MARK = "空壳页判定"


def check_shell_not_content(e, sources):
    """R23（D125）：被标为「空壳页」的来源，不得在备注中被称作内容来源/第二来源/互证。"""
    pn = e.get("pending_notes") or ""
    for sid in e.get("sources", []):
        s = sources.get(sid) or {}
        if SHELL_MARK not in (s.get("note") or ""):
            continue
        # 该 sid 所属段落里若出现「第二来源/互证/内容来源/主来源」等字样 → 报错
        seg = ""
        for part in re.split(r"【", pn):
            if sid in part:
                seg = part
                break
        if any(k in seg for k in ("第二来源", "互证", "内容来源", "主来源")):
            err(f"R23 {e['id']}: 空壳页 {sid} 被备注称作内容来源/互证（D125）")


MIN_STRONG_CITED = 10''')
open(p,"w",encoding="utf-8").write(t)
print("R23 已加入 check.py")