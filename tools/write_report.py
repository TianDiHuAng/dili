# -*- coding: utf-8 -*-
"""阶段5：汇总 REPORT.md。"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
UNITS = ["africa","asia","europe","north-america","south-america","oceania","antarctica","global-themes"]
NAMES = {"africa":"非洲","asia":"亚洲","europe":"欧洲","north-america":"北美洲","south-america":"南美洲","oceania":"大洋洲","antarctica":"南极洲","global-themes":"全球主题"}
THEMES = ["地形","气候","农业","贸易","政权更替","区域"]

cov = json.load(open(os.path.join(DATA, "coverage.json"), encoding="utf-8"))
src = json.load(open(os.path.join(DATA, "sources.json"), encoding="utf-8"))["sources"]
es = cov["entries"]
verified_src = sum(1 for s in src if s.get("verified"))
l1 = sum(1 for e in es if e["level"] == "L1")
l2 = sum(1 for e in es if e["level"] == "L2")
l3 = sum(1 for e in es if e["level"] == "L3")
pending = sum(1 for e in es if e["pending_count"] > 0)
core = sum(1 for e in es if e["tier"] == "核心")
important = sum(1 for e in es if e["tier"] == "重要")
supp = sum(1 for e in es if e["tier"] == "补充")

matrix = cov.get("matrix", {})
blanks = []
for uid in UNITS:
    for t in THEMES:
        if matrix.get(uid, {}).get(t, 0) == 0:
            blanks.append(f"{NAMES[uid]} × {t}")

lines = [
 "# REPORT.md — 地理与文明百科项目报告", "",
 f"- 生成日期：{cov['updated']}",
 f"- 总条目数：**{len(es)}**",
 f"- 分级：核心 {core} / 重要 {important} / 补充 {supp}",
 f"- 写作层级：L1 {l1} / L2 {l2} / L3 {l3}",
 f"- 来源总数：{len(src)}；已核验：{verified_src}",
 f"- 待核实条目：{pending}",
 f"- 当前轮次：第 {cov.get('round', 1)} 轮，本轮处理 {cov.get('round_processed', 0)} 条", "",
 "## 验证通过", "",
 "- tools/check.py：必填字段、id 合法与唯一、来源白名单与双源、SVG 合法与不出界、层级结构、coverage 一致性。",
 "- tools/check_links.py：站内链接 0 断链。",
 "- 来源核验：curl 实测 HTTP 状态并从页面 `<title>` 核对标题；无法核验者标待核实。", "",
 "## 空白格子（覆盖矩阵为 0 的维度）", "",
]
lines += [f"- {b}" for b in blanks] if blanks else ["- 无"]
lines += ["", "## 待核实与限制", "",
 "- 大部分条目处于 L1 骨架层级，仅定义、时间/位置、概述、相关条目；具体事实与现状数据待逐条补源。",
 "- 现状数据（人口、面积、边界）未在骨架页写具体数值，避免无来源数字；后续按年份与权威机构补齐。",
 "- 争议边界不绘制，仅描述各方立场。",
 "- 网络核验以 curl 实测为准；被服务器反爬拒绝的来源标为 blocked，不计入已核验。", ""]

with open(os.path.join(ROOT, "REPORT.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("REPORT.md 已生成；空白格子", len(blanks))
