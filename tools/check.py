# -*- coding: utf-8 -*-
"""tools/check.py — 地理与文明百科质量守门员。
运行：python -X utf8 tools/check.py
规则：R1 必填字段 / R2 id 合法 / R3 全局唯一 / R4 来源合法与双源 / R5 层级与层级结构 /
      R6 SVG 合法与不出界 / R7 日期数字合法 / R8 现状数据年份与来源 / R9 内部链接 /
      R10 coverage 一致 / R11 标题去重 / R12 sources.json 结构 / R13 同数据跨页一致。
"""
import json, os, re, sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
UNIT_IDS = ["africa", "asia", "europe", "north-america", "south-america", "oceania", "antarctica", "global-themes"]
REQUIRED = ["id", "title", "tier", "unit_id", "region", "theme", "level", "status",
            "definition", "time_or_place", "overview", "related", "sources", "needs_verification", "pending_notes"]
L2_REQUIRED = ["geo", "influence", "polities", "connections", "today", "svg"]
SVG_TAGS = {"svg", "g", "path", "rect", "circle", "ellipse", "line", "polyline", "polygon", "text", "tspan", "title", "desc"}

errors = []
warns = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warns.append(msg)


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    src_doc = load_json(os.path.join(DATA, "sources.json"))
    sources = {s["id"]: s for s in src_doc["sources"]}
    cov = load_json(os.path.join(DATA, "coverage.json"))
    cov_by_id = {e["id"]: e for e in cov["entries"]}

    all_entries = []
    seen_ids = {}
    for uid in UNIT_IDS:
        p = os.path.join(DATA, uid + ".json")
        doc = load_json(p)
        # R12 sources.json 结构与来源合法性
        titles = {}
        for e in doc["entries"]:
            eid = e.get("id", "?")
            # R1
            for k in REQUIRED:
                if k not in e or e[k] in (None, "", []):
                    if k not in ("related",):  # related 允许空
                        err(f"R1 {eid}: 必填字段 {k} 缺失或为空")
            # R2
            if not re.fullmatch(r"[a-z0-9-]+", eid):
                err(f"R2 {eid}: id 只允许 a-z0-9-")
            # R3
            if eid in seen_ids:
                err(f"R3 {eid}: 与 {seen_ids[eid]} 重复")
            seen_ids[eid] = uid
            if e.get("unit_id") != uid:
                err(f"R3 {eid}: unit_id 与文件不一致")
            # R11
            t = e.get("title", "")
            if t in titles:
                err(f"R11 {uid}: 标题重复 {t}")
            titles[t] = eid
            # R5
            if e.get("tier") not in ("核心", "重要", "补充"):
                err(f"R5 {eid}: tier 非法 {e.get('tier')}")
            if e.get("level") not in ("L1", "L2", "L3"):
                err(f"R5 {eid}: level 非法 {e.get('level')}")
            # R4 来源
            sids = e.get("sources", [])
            if len(sids) < 2:
                err(f"R4 {eid}: sources 少于 2 个")
            for sid in sids:
                if sid not in sources:
                    err(f"R4 {eid}: 来源 id 未定义 {sid}")
                elif not sources[sid].get("verified"):
                    if not e.get("needs_verification"):
                        err(f"R4 {eid}: 引用未核验来源 {sid} 却未标待核实")
            if len(set(sids)) != len(sids):
                err(f"R4 {eid}: 来源 id 重复")
            if e.get("needs_verification") and not e.get("pending_notes"):
                err(f"R4 {eid}: needs_verification=true 但 pending_notes 为空")
            # R7 数字/日期：time_or_place 中的年份须为合理范围
            for m in re.finditer(r"(前?)(\d{3,5})年", e.get("time_or_place", "")):
                y = int(m.group(2))
                limit = 10000 if m.group(1) else 2100
                if y > limit:
                    err(f"R7 {eid}: 年份超出合理范围 {m.group(0)}")
            # R10 coverage 一致
            c = cov_by_id.get(eid)
            if not c:
                err(f"R10 {eid}: coverage.json 缺少条目")
            else:
                if c.get("level") != e.get("level") or c.get("tier") != e.get("tier"):
                    err(f"R10 {eid}: coverage 层级/级别不一致")
                if c.get("status") != e.get("status"):
                    err(f"R10 {eid}: coverage 状态不一致")
            # L2 结构
            if e.get("level") in ("L2", "L3"):
                for k in L2_REQUIRED:
                    if k not in e or e[k] in (None, "", {}):
                        err(f"R5 {eid}: L2 缺少节 {k}")
                if "today" in e and isinstance(e["today"], str):
                    check_today(eid, e["today"])
                if e.get("svg"):
                    check_svg(eid, e["svg"])
            all_entries.append(e)

    # R9 内部链接（相关条目）
    ids = {e["id"] for e in all_entries}
    for e in all_entries:
        for rid in e.get("related", []):
            if rid not in ids:
                err(f"R9 {e['id']}: related 指向不存在条目 {rid}")

    # coverage 多余条目
    for cid in cov_by_id:
        if cid not in ids:
            err(f"R10 coverage 多余条目 {cid}")

    # R12 sources.json
    for sid, s in sources.items():
        for k in ("id", "title", "author", "type", "url"):
            if k not in s or s[k] in (None, ""):
                err(f"R12 来源 {sid}: 字段 {k} 缺失")
        if s.get("link_ok") not in (True, False, "blocked"):
            err(f"R12 来源 {sid}: link_ok 三态非法")
        if s.get("verified") and s.get("link_ok") is not True:
            err(f"R12 来源 {sid}: verified=true 但 link_ok 非 true")
        if s.get("verified") and not s.get("page_title"):
            err(f"R12 来源 {sid}: verified=true 但无页面标题核验记录")

    # R13 同数据跨页一致：以 title 为键，overview 必须一致
    bytitle = {}
    for e in all_entries:
        if e["title"] in bytitle and bytitle[e["title"]] != e["overview"]:
            err(f"R13 标题 {e['title']} 的概述跨条目不一致")
        bytitle[e["title"]] = e["overview"]

    print(f"检查条目 {len(all_entries)} 条，来源 {len(sources)} 条")
    if warns:
        print("警告:")
        for w in warns:
            print("  !", w)
    if errors:
        print(f"ERRORS={len(errors)}")
        for e in errors[:200]:
            print("  X", e)
        sys.exit(1)
    print("ERRORS=0 ALL_PASS")


def check_today(eid, text):
    """现状数据须含年份与来源标注。"""
    if re.search(r"\d", text):
        if not re.search(r"(19|20)\d{2}年", text):
            err(f"R8 {eid}: today 含数字但无年份标注")
        if "来源" not in text and "source" not in text.lower():
            err(f"R8 {eid}: today 含数字但无来源标注")


def check_svg(eid, svg):
    try:
        root = ET.fromstring(svg)
    except Exception as ex:
        err(f"R6 {eid}: SVG XML 解析失败 {ex}")
        return
    if root.tag.split("}")[-1] != "svg" or "viewBox" not in root.attrib:
        err(f"R6 {eid}: SVG 根或 viewBox 缺失")
        return
    vb = [float(x) for x in re.split(r"[ ,]+", root.attrib["viewBox"].strip())]
    if len(vb) != 4:
        err(f"R6 {eid}: viewBox 格式非法")
        return
    for el in root.iter():
        tag = el.tag.split("}")[-1]
        if tag not in SVG_TAGS:
            err(f"R6 {eid}: SVG 元素不在白名单 {tag}")
        if "onclick" in el.attrib or "onload" in el.attrib or tag == "script":
            err(f"R6 {eid}: SVG 含脚本")
        for k in ("x", "y", "cx", "cy", "x1", "x2", "y1", "y2"):
            if k in el.attrib:
                try:
                    v = float(el.attrib[k])
                    axis = 0 if k in ("x", "cx", "x1", "x2") else 1
                    lo = vb[axis]
                    hi = vb[axis] + vb[axis + 2]
                    if v < lo - 2 or v > hi + 2:
                        err(f"R6 {eid}: SVG 元素 {tag} 的 {k}={v} 超出 viewBox [{lo},{hi}]")
                except ValueError:
                    err(f"R6 {eid}: SVG 属性 {k} 非数字")


if __name__ == "__main__":
    main()
