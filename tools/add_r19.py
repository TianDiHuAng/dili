# -*- coding: utf-8 -*-
"""第54轮：向 check.py 加入 R19——弱来源不得称主来源（D112 机器化）。"""
import os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p=os.path.join(ROOT,"tools","check.py")
t=open(p,encoding="utf-8").read()
if "R19" in t:
    print("R19 已存在"); raise SystemExit
t=t.replace("            check_orphan_citation(e, src_by_id)",
            "            check_orphan_citation(e, src_by_id)\n            check_weak_as_primary(e, src_by_id)")
t=t.replace("def check_orphan_citation(e, sources):",
'''MIN_ABS = 800
MIN_CITED_OK = 5

def _src_weak(s):
    """D112：被引≤5 / 摘要或正文<800 / note 自标 weak → 弱来源。"""
    note = s.get("note") or ""
    m = re.search(r"被引\\s*(\\d+)", note)
    cited = int(m.group(1)) if m else None
    a = re.search(r"(?:摘要长度|正文节录|正文|摘要)\\s*\\*{0,2}([\\d,]+)\\s*字符", note)
    abslen = int(a.group(1).replace(",", "")) if a else None
    b = re.search(r"(\\d{3,7})\\s*字节", note)
    bytelen = int(b.group(1)) if b else None
    weak=False; why=[]
    if cited is not None and cited <= MIN_CITED_OK:
        weak=True; why.append(f"被引{cited}<=5")
    if abslen is not None and abslen < MIN_ABS:
        weak=True; why.append(f"正文{abslen}字符<800")
    elif abslen is None and bytelen is not None and bytelen < MIN_ABS:
        weak=True; why.append(f"正文{bytelen}字节<800")
    if "证据强度：weak" in note:
        weak=True; why.append("note自标weak")
    return weak, why


def check_weak_as_primary(e, sources):
    """R19（D112）：备注中把弱来源称作「补主来源」即报错。"""
    pn = e.get("pending_notes") or ""
    for seg in re.findall(r"【[^】]*补主来源[^】]*】([^【]*)", pn):
        for sid in re.findall(r"(openalex-[A-Za-z0-9]+|[a-z]{1,6}-[a-z0-9\\-]{2,})", seg):
            s = sources.get(sid)
            if not s: continue
            weak, why = _src_weak(s)
            if weak:
                err(f"R19 {e['id']}: 备注把弱来源 {sid} 称作「主来源」（{'、'.join(why)}，D112）")


def check_orphan_citation(e, sources):''')
open(p,"w",encoding="utf-8").write(t)
print("R19 已加入 check.py")