# -*- coding: utf-8 -*-
"""第79轮：修 assess.py 两处偏离——多值取严格值、空壳页排除（D142）。"""
import os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p=os.path.join(ROOT,"tools","assess.py")
t=open(p,encoding="utf-8").read()
if "D142" in t:
    print("已存在"); raise SystemExit

# 1 _nums 改为取所有匹配中的最小值（严格）
old_nums = '''def _nums(note):
    """从 note 文本中抽取（被引数、正文字符数）。"""
    cited = None
    m = re.search(r"被引\\s*(\\d+)", note or "")
    if m:
        cited = int(m.group(1))
    body = None
    for pat in (r"摘要长度\\s*(\\d+)\\s*字符", r"正文节录\\s*\\*{0,2}([\\d,]+)\\s*字符",
                r"正文\\s*\\*{0,2}([\\d,]+)\\s*字符", r"摘要\\s*(\\d+)\\s*字符"):
        m = re.search(pat, note or "")
        if m:
            body = int(m.group(1).replace(",", ""))
            break
    if body is None:
        m = re.search(r"(\\d{3,7})\\s*字节", note or "")
        if m and int(m.group(1)) >= MIN_BYTES:
            body = int(m.group(1)) // 3
    return cited, body'''
new_nums = '''def _nums(note):
    """从 note 文本中抽取（被引数、正文字符数）。
    D142：若 note 中并存多个字符数（如文本提取 5,455 与 strip 后 750），取**最小值**
    （更严格者），避免用旧口径大数字掩盖空壳页。"""
    note = note or ""
    cited = None
    m = re.search(r"被引\\s*(\\d+)", note)
    if m:
        cited = int(m.group(1))
    bodies = []
    for pat in (r"摘要长度\\s*(\\d+)\\s*字符", r"正文节录\\s*\\*{0,2}([\\d,]+)\\s*字符",
                r"正文\\s*\\*{0,2}([\\d,]+)\\s*字符", r"摘要\\s*(\\d+)\\s*字符"):
        for mm in re.finditer(pat, note):
            v = int(mm.group(1).replace(",", ""))
            if v > 0:
                bodies.append(v)
    body = min(bodies) if bodies else None
    if body is None:
        mb = re.findall(r"(\\d{3,7})\\s*字节", note)
        if mb:
            vals = [int(x) for x in mb if int(x) >= MIN_BYTES]
            if vals:
                body = min(vals) // 3
    return cited, body'''
if old_nums in t:
    t = t.replace(old_nums, new_nums)
    print("_nums 已改为取严格值")
else:
    print("⚠ 未匹配 _nums 原文，改用正则替换")
    m=re.search(r"def _nums\(note\):.*?(?=\ndef )", t, re.S)
    if m: t=t[:m.start()]+new_nums+"\n"+t[m.end():]

# 2 has_content 排除空壳页
t=t.replace('''    if is_data(sid) or is_alias(sid):
        return False
    src = src or {}
    if is_bad_type(src):
        return False''',
'''    if is_data(sid) or is_alias(sid):
        return False
    src = src or {}
    if is_bad_type(src):
        return False
    # D142：已被实测标为「空壳页」的来源一律不算内容来源
    if SHELL_MARK in (src.get("note") or ""):
        return False''')
t=t.replace('BAD_TYPES = ("书评", "book-review")',
            'BAD_TYPES = ("书评", "book-review")\nSHELL_MARK = "空壳页判定"')

# 3 strength 同样排除空壳页
t=t.replace('''    src = src or {}
    if is_bad_type(src):
        return "side"''',
'''    src = src or {}
    if is_bad_type(src):
        return "side"
    if SHELL_MARK in (src.get("note") or ""):
        return "weak"      # 空壳页最多算弱来源''')
open(p,"w",encoding="utf-8").write(t)
print("assess.py 已修（D142）")