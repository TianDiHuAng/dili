# REPORT.md — 第 52 轮摘要

- 日期：2026-11-24
- 状态：正常循环

## 1. 本轮完成：为 6 条侧面文献条目补主来源

| 条目 | 新主来源 | 被引 |
|---|---|---|
| 文艺复兴意大利 | The collapse of city-states and the role of urban centres… (2012, 剑桥) | 8 |
| 拜占庭帝国 | The Middle Byzantine Economy (600–1204) (2009) | 21 |
| 维京时代 | Viking-Age Trade: Silver, Slaves and Gotland (2020) | 13 |
| 大自流盆地 | Structure, stratigraphy, and hydrogeology of… (1968) | 16 |
| 落基山脉 | Laramide (Late Cretaceous-Early Tertiary) Orogeny (1975) | **223** |
| 美国西进 | The course of westward expansion (2020) | 0（标注为弱点，仅辅助） |

## 2. 按 D110 如实记录的「无候选」

本轮每条「无来源」结论都写明引擎、两条检索式、条数与逐项拒绝理由（记录在 `reports/round52_primary.json` / `round52b_primary.json`）：
- **库什与努比亚**（商路与商品结构）：40 条结果中无一条同时满足「标题含 kush/meroe」与「两个主题槽」。**确无**。
- **古埃及新王国**：过筛者仍是《Afterglow of Empire: Egypt from the **Fall** of the New Kingdom…》——该书讲的是新王国**灭亡之后**（前11–前6世纪），第48轮已剔除，**本轮再次排除**。书名含 New Kingdom 而主题在其之后，是 D108「同名不同时」的典型。
- **印加帝国**：过筛者《The Sacred Landscape of the Inca: The Cusco Ceque System》主题是**库斯科的 ceque 仪式系统**（宗教地理侧面），不撑「疆域、道路与行政」。
- **亚马逊盆地**：过筛者《Extractive Reserves and Participatory Research…》主题是**采掘保护区与参与式研究**（土地政策侧面），不撑地貌水文。

## 3. 质量

- tools/check.py：ERRORS=0 ALL_PASS（243 条条目、632 条来源；R1–R18）
- tools/check_links.py：BROKEN=0 LINKS_PASS
- 抽检：本轮为6条侧面条目补主来源（文艺复兴意大利/拜占庭/维京/大自流盆地/落基山脉/美国西进）；库什商路、古埃及新王国（二次命中「新王国之后」）、印加（ceque仪式系统）、亚马逊（采掘保护区）均按D110如实记录无合格候选

## 4. 累计与达成度

- 条目：243（核心 44 / 重要 104 / 补充 95）；**全部 L2**
- 内容源（≥800 字符）≥2 个：**223**；1 个：**20**；0 个：**0**
- 侧面文献已标注：30 条；本轮新增主来源：6 条
- 来源 632（已核验 553）；待核实 241

| 条件 | 状态 |
|---|---|
| 核心 44/44 · 重要 104/104 · 全部 243/243 L2 | **已达成** |
| 每条至少 1 个内容源 | **已达成 243/243** |
| 每条均有**主**来源 | 未达成（约 19 条仍以侧面文献为主要来源） |
| 内容对题（R19 全量机器校验） | 未实现 |
| 多维缺口连续 3 轮为零 | 未达成 |
