# -*- coding: utf-8 -*-
"""第61轮A：R22——层级记录须与实际来源一致（重算比对）。"""
import os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p=os.path.join(ROOT,"tools","check.py")
t=open(p,encoding="utf-8").read()
if "R22" in t:
    print("R22 已存在"); raise SystemExit
t=t.replace("            check_evidence_level(e, EV_MAP)",
            "            check_evidence_level(e, EV_MAP)\n            check_level_consistency(e, EV_MAP, src_by_id)")
t=t.replace("def check_evidence_level(e, evmap):",
'''MIN_STRONG_CITED = 10
MIN_STRONG_BODY = 800


def _is_data_src(sid):
    return sid.startswith(("wb-", "usgs-eq", "noaa-current", "ats-parties", "wikidata-"))


def _seg_for(sid, e):
    """D119：按【】分段取该 sid 所属段落，避免相邻来源字样污染。"""
    pn = e.get("pending_notes") or ""
    for seg in re.split(r"【", pn):
        if sid in seg:
            return seg
    return ""


def _grade_one(sid, e, sources):
    if _is_data_src(sid):
        return "data"
    note = (sources.get(sid) or {}).get("note") or ""
    seg = _seg_for(sid, e)
    if any(k in seg for k in ("旁证", "剔除", "不作", "降级")):
        return "side"
    if "证据强度：weak" in note:
        return "weak"
    if "证据强度：strong" in note:
        return "strong"
    mc = re.search(r"被引\\s*(\\d+)", note)
    cited = int(mc.group(1)) if mc else None
    ma = re.search(r"(?:摘要长度|正文节录|正文|摘要)\\s*\\*{0,2}([\\d,]+)\\s*字符", note)
    abslen = int(ma.group(1).replace(",", "")) if ma else None
    mb = re.search(r"(\\d{3,7})\\s*字节", note)
    bytelen = int(mb.group(1)) if mb else None
    body = abslen if abslen is not None else bytelen
    if (cited is not None and cited >= MIN_STRONG_CITED) or (body is not None and body >= MIN_STRONG_BODY):
        return "strong"
    if (cited is not None and cited < MIN_STRONG_CITED) or (body is not None and body < MIN_STRONG_BODY):
        return "weak"
    return None


def check_level_consistency(e, evmap, sources):
    """R22（第61轮）：evidence_level.json 记录的层级须与按来源重算的结果一致。"""
    rec = evmap.get(e.get("title"))
    if not rec:
        return
    c = {"strong": 0, "weak": 0, "side": 0, "data": 0, "unknown": 0}
    for sid in e.get("sources", []):
        g = _grade_one(sid, e, sources)
        c[g if g else "unknown"] += 1
    if c["strong"] >= 2:
        expect = "A"
    elif c["strong"] == 1:
        expect = "B"
    elif c["data"] > 0 and c["side"] == 0:
        expect = "D"
    else:
        expect = "C"
    if rec.get("level") != expect:
        err(f"R22 {e['id']}: 层级记录为 {rec.get('level')}，按来源重算应为 {expect}（{c}）")


def check_evidence_level(e, evmap):''')
open(p,"w",encoding="utf-8").write(t)
print("R22 已加入 check.py")