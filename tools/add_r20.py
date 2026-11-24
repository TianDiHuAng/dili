# -*- coding: utf-8 -*-
"""第56轮：把 R19 第二层写入 check.py（对象词校验，排除已标旁证的来源）。"""
import json,os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data")
# 从 round56_r19b.json 取对象词表，并修正词形
obj=json.load(open(os.path.join(ROOT,"reports","round56_r19b.json"),encoding="utf-8"))["obj_map"]
obj["安第斯山脉"]=["andes","andean"]
obj["马里帝国"]=["mali"]
json.dump(obj,open(os.path.join(DATA,"object_words.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)

p=os.path.join(ROOT,"tools","check.py")
t=open(p,encoding="utf-8").read()
if "R20" in t:
    print("R20 已存在"); raise SystemExit
t=t.replace("            check_weak_as_primary(e, src_by_id)",
            "            check_weak_as_primary(e, src_by_id)\n            check_object_word(e, src_by_id, OBJ_MAP)")
t=t.replace("def main():",
'''OBJ_MAP = {}
_ob_path = os.path.join(DATA, "object_words.json")
if os.path.exists(_ob_path):
    OBJ_MAP = load_json(_ob_path)


def _norm_text(s):
    import unicodedata
    s = unicodedata.normalize("NFKD", (s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def check_object_word(e, sources, objmap):
    """R20（D105 第二层）：核心条目的学术来源标题须含条目对象词；已标「旁证」者豁免。"""
    title = e.get("title")
    objs = objmap.get(title)
    if not objs:
        return
    pn = e.get("pending_notes") or ""
    for sid in e.get("sources", []):
        if not sid.startswith("openalex-"):
            continue
        # 已在本条备注中被标为旁证/弱来源/剔除者豁免
        seg = ""
        idx = pn.find(sid)
        if idx >= 0:
            seg = pn[max(0, idx - 120): idx + 60]
        if any(k in seg for k in ("旁证", "弱来源", "剔除", "降级", "不作")):
            continue
        ti = _norm_text((sources.get(sid) or {}).get("title"))
        if not any(_norm_text(o) in ti for o in objs):
            err(f"R20 {e['id']}: 来源 {sid} 标题不含对象词 {objs[:2]}（D105 第二层）")


def main():''')
open(p,"w",encoding="utf-8").write(t)
print("R20 已加入 check.py；object_words.json 已写入", len(obj), "条映射")