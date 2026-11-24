# -*- coding: utf-8 -*-
"""第68轮A：R25——openalex 来源 type 不得为书评/数据集等非内容类型。"""
import os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p=os.path.join(ROOT,"tools","check.py")
t=open(p,encoding="utf-8").read()
if "R25" in t:
    print("R25 已存在"); raise SystemExit
t=t.replace("            check_dangling_landing(e)",
            "            check_dangling_landing(e)\n            check_source_type(e, src_by_id)")
t=t.replace("BODY_FIELDS = (",
'''BAD_TYPES = ("书评", "book-review", "数据集", "component", "peer-review", "posted-content")


def check_source_type(e, sources):
    """R25（D082/D134）：书评等非内容类型不得作为内容来源被引用。"""
    pn = e.get("pending_notes") or ""
    for sid in e.get("sources", []):
        s = sources.get(sid) or {}
        note = s.get("note") or ""
        typ = (s.get("type") or "") + " " + note
        if any(b in typ for b in BAD_TYPES):
            err(f"R25 {e['id']}: 来源 {sid} 类型为书评/非内容文献（type={s.get('type')}），按 D082 不得作内容来源")


BODY_FIELDS = (''')
open(p,"w",encoding="utf-8").write(t)
print("R25 已加入")