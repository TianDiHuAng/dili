# -*- coding: utf-8 -*-
"""第72轮：建立唯一的判据实现 tools/assess.py（D138）。所有统计与校验都应引用本模块。"""
import json, os, re

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

# ---- 常量：单一来源 ----
ALIAS_PAGES = ("britannica-regions", "wikipedia-regions", "un-m49", "ap-human-geo", "s010-unesco-org")
DATA_PREFIX = ("wb-", "usgs-eq", "noaa-current", "ats-parties", "wikidata-")
MIN_CITED = 10      # 强来源：被引门槛
MIN_BODY = 800      # 强来源：正文/摘要字符门槛
MIN_BYTES = 3000    # 字节门槛（约 1000 字符）
BAD_TYPES = ("书评", "book-review")   # 非内容类型（D082/D134）


def is_data(sid):
    """数据端点：返回结构化数值，非内容来源（D107）。"""
    return sid.startswith(DATA_PREFIX)


def is_alias(sid):
    """别名页/索引页：只证明对象存在，不含主题正文（D135）。"""
    return sid in ALIAS_PAGES


def is_bad_type(src):
    """书评等非内容类型（D082/D134）。"""
    t = (src.get("type") or "") + " " + (src.get("note") or "")
    return any(b in t for b in BAD_TYPES)


def _nums(note):
    """从 note 文本中抽取（被引数、正文字符数）。"""
    cited = None
    m = re.search(r"被引\s*(\d+)", note or "")
    if m:
        cited = int(m.group(1))
    body = None
    for pat in (r"摘要长度\s*(\d+)\s*字符", r"正文节录\s*\*{0,2}([\d,]+)\s*字符",
                r"正文\s*\*{0,2}([\d,]+)\s*字符", r"摘要\s*(\d+)\s*字符"):
        m = re.search(pat, note or "")
        if m:
            body = int(m.group(1).replace(",", ""))
            break
    if body is None:
        m = re.search(r"(\d{3,7})\s*字节", note or "")
        if m and int(m.group(1)) >= MIN_BYTES:
            body = int(m.group(1)) // 3
    return cited, body


def has_content(sid, src, entry=None):
    """该来源是否算「有正文的内容来源」（D138 统一判据）。
    排除：数据端点、别名页、书评。门槛：被引≥10 或 正文≥800。"""
    if is_data(sid) or is_alias(sid):
        return False
    src = src or {}
    if is_bad_type(src):
        return False
    texts = [src.get("note") or ""]
    if entry is not None:
        texts.append(entry.get("pending_notes") or "")
    for t in texts:
        cited, body = _nums(t)
        if cited is not None and cited >= MIN_CITED:
            return True
        if body is not None and body >= MIN_BODY:
            return True
    return False


def strength(sid, src, entry=None):
    """层级判定用的四类：strong / weak / side / data / alias / None。"""
    if is_data(sid):
        return "data"
    if is_alias(sid):
        return "alias"
    src = src or {}
    if is_bad_type(src):
        return "side"
    # 备注中被判旁证/剔除者
    seg = ""
    for part in re.split(r"【", (entry or {}).get("pending_notes") or ""):
        if sid in part:
            seg = part
            break
    if any(k in seg for k in ("旁证", "剔除", "不作", "降级")):
        return "side"
    note = src.get("note") or ""
    if "证据强度：weak" in note:
        return "weak"
    if "证据强度：strong" in note:
        return "strong"
    cited, body = _nums(note)
    if (cited is not None and cited >= MIN_CITED) or (body is not None and body >= MIN_BODY):
        return "strong"
    if (cited is not None and cited < MIN_CITED) or (body is not None and body < MIN_BODY):
        return "weak"
    return None


def count_entry(entry, sources):
    """返回某条目的各类来源计数。"""
    c = {"strong": 0, "weak": 0, "side": 0, "data": 0, "alias": 0, "unknown": 0}
    for sid in entry.get("sources", []):
        g = strength(sid, sources.get(sid) or {}, entry)
        c[g if g else "unknown"] += 1
    return c


def content_count(entry, sources):
    """该条目「有正文的内容来源」个数。"""
    return sum(1 for sid in entry.get("sources", [])
               if has_content(sid, sources.get(sid) or {}, entry))


def _strong_sids(entry, sources):
    return [sid for sid in entry.get("sources", [])
            if strength(sid, sources.get(sid) or {}, entry) == "strong"]


def level_of(entry, sources):
    """A/B/C/D 四档。
    D141：若仅有 1 个强来源、且该强来源是**机构长文**（非 openalex- 学术论文）、
    同时条目带数据端点——判为 D（指标解读类），因为其正文是指标解释与空间差异概述，
    机构长文即主体，不要求第二篇学术文献。"""
    c = count_entry(entry, sources)
    if c["strong"] >= 2:
        return "A"
    if c["strong"] == 1:
        sids = _strong_sids(entry, sources)
        is_institutional = sids and not any(s.startswith("openalex-") for s in sids)
        if is_institutional and c["data"] > 0 and c["side"] == 0:
            return "D"
        return "B"
    if c["data"] > 0 and c["side"] == 0 and c["weak"] == 0:
        return "D"
    return "C"


def load_sources():
    with open(os.path.join(DATA, "sources.json"), encoding="utf-8") as f:
        return {s["id"]: s for s in json.load(f)["sources"]}


def load_entries(units):
    out = {}
    for u in units:
        with open(os.path.join(DATA, u + ".json"), encoding="utf-8") as f:
            for e in json.load(f)["entries"]:
                out[e["title"]] = e
    return out


UNITS = ["africa", "asia", "europe", "north-america", "south-america", "oceania", "antarctica", "global-themes"]

if __name__ == "__main__":
    S = load_sources()
    T = load_entries(UNITS)
    from collections import Counter
    levels = Counter(); content = Counter()
    for t, e in T.items():
        levels[level_of(e, S)] += 1
        n = content_count(e, S)
        content[n if n < 2 else 2] += 1
    print("层级:", dict(levels))
    print("内容源数（2 表示 ≥2）:", dict(content))
    print("合计:", sum(levels.values()))