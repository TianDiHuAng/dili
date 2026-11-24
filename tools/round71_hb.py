# -*- coding: utf-8 -*-
"""第71轮B：hb() 统一为「被引≥10 或 正文≥800」（与 D117 层级判定一致），重算。"""
import os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NEW_HB = '''def hb(sid,e):
    """D138：与层级判定统一——被引≥10 或 正文/摘要≥800，满足其一即算有正文的内容源。
    别名页/数据端点不计（D107/D135）。"""
    if is_data(sid): return False
    if sid in ALIAS_EXCL: return False
    s = S.get(sid) or {}
    note = s.get("note") or ""
    pn = e.get("pending_notes") or ""
    for n in (note, pn):
        mc = re.search(r"被引\\s*(\\d+)", n)
        if mc and int(mc.group(1)) >= 10:
            return True
        for pat in (r"摘要长度\\s*(\\d+)\\s*字符", r"正文节录\\s*\\*{0,2}([\\d,]+)\\s*字符",
                    r"正文\\s*\\*{0,2}([\\d,]+)\\s*字符", r"摘要\\s*(\\d+)\\s*字符"):
            m = re.search(pat, n)
            if m and int(m.group(1).replace(",", "")) >= 800:
                return True
        m = re.search(r"(\\d{3,7})\\s*字节", n)
        if m and int(m.group(1)) >= 3000:      # 字节→字符约 3:1，3000 字节≈1000 字符
            return True
    return False
'''

def patch(path):
    t=open(path,encoding="utf-8").read()
    if "D138" in t:
        print(f"  {os.path.basename(path)} 已是新口径");return False
    # 替换旧的 hb 定义块（从 def hb( 到下一个 def 或空行后的语句）
    m=re.search(r"def hb\(sid,e\):.*?(?=\n(?:def |g2|print|one|for |if |[A-Z_]+ =))", t, re.S)
    if not m:
        m=re.search(r"def hb\(sid,e\):.*?(?=\Z)", t, re.S)
    if not m:
        print(f"  {os.path.basename(path)} 未找到 hb");return False
    t=t[:m.start()]+NEW_HB+"\n"+t[m.end():]
    # 确保 ALIAS_EXCL 定义存在
    if "ALIAS_EXCL" not in t:
        t=t.replace('def is_data(sid): return sid.startswith(("wb-","usgs-eq","noaa-current","ats-parties","wikidata-"))',
'''ALIAS_EXCL = ("britannica-regions", "wikipedia-regions", "un-m49", "ap-human-geo", "s010-unesco-org")

def is_data(sid): return sid.startswith(("wb-","usgs-eq","noaa-current","ats-parties","wikidata-"))''')
    # 确保 S 可用
    if "S = {s[\"id\"]: s for s in" not in t and "S={s['id']:s for s in" not in t and "S = {s['id']: s for s in" not in t:
        t=t.replace("T={e[\"title\"]:e","S={s[\"id\"]:s for s in json.load(open(os.path.join(DATA,\"sources.json\"),encoding=\"utf-8\"))[\"sources\"]}\nT={e[\"title\"]:e")
    open(path,"w",encoding="utf-8").write(t)
    print(f"  {os.path.basename(path)} 已更新")
    return True

for f in ("round62_gaps.py","finalize_round70.py","finalize_round69.py","finalize_round68.py","finalize_round67.py"):
    p=os.path.join(ROOT,"tools",f)
    if os.path.exists(p): patch(p)