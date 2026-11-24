# REPORT.md — 第 74 轮摘要

- 日期：2026-11-24
- 状态：正常循环（**G3：88 → 83，G1：4 → 3**）

## 1. 第二批核心 G3：登记 6 条

| 条目 | 新第二来源 | 被引 | 摘要 |
|---|---|---|---|
| 安第斯山脉 | Amazonia Through Time: **Andean Uplift**, Climate Change, Landscape Evolution (2010) | **2762** | 802 |
| 澳大利亚大陆 | Climate change and Australia: Trends, projections and impacts (2003) | **941** | 3,793 |
| 玛雅文明 | Ancestral Maya Economies in Archaeological Perspective (2010) | 191 | 1,121 |
| 河流三角洲 | High-Resolution Stratigraphy of a Mississippi Subdelta-Lobe (2006) | 23 | 1,150 |
| 大平原 | Ethnicity on the Great Plains (1980) | 12 | — |
| 波利尼西亚 | Micronesian and Polynesian Voyaging: Three Readings (1976) | 5 | 2,690 |

其中**安第斯**那篇（被引 2762）与**澳大利亚大陆**那篇（941）是本轮质量最高的两条——两篇都直接讨论「隆升如何改变气候与景观」「全澳气候趋势与影响」，与本条 geo 段一一对得上。

## 2. 两条不采用（如实记录）

| 条目 | 候选 | 问题 |
|---|---|---|
| **印加帝国** | Machu Picchu: Unveiling the Mystery of the Incas (2005) | 对象是**遗址**（皇家庄园），第55轮已判不撑国家的疆域/道路/行政，本轮再次不采用 |
| 澳大利亚原住民 | Reempowering Ourselves: Australian Aboriginal **Women** (2010) | 性别侧面，不撑「适应干旱生态、语言与文化传统」总体 |

## 3. 口径（tools/assess.py）

- tools/check.py：ERRORS=0 ALL_PASS（243 条、677 来源；R1–R25）
- tools/check_links.py：BROKEN=0 LINKS_PASS
- 层级：A 123 / B 117 / C 1 / D 2
- 内容源 ≥2：**159**；1 个：**83**；0 个：**1**
- 缺口：G1=3 / G2=3 / **G3=83** / G4=243

| 条件 | 状态 |
|---|---|
| 全部 243 条 L2 | **已达成** |
| 判据单一实现（D138） | **已达成** |
| R19–R25 七道机器校验 | 已上线，0 违规 |
| 每个条目都有强来源（G1=0） | 未达成（3 条：阿卡德帝国、隋唐、水资源管理） |
| 每条都有 ≥2 内容源 | 未达成（84 条不足） |
| G4 语义对题 | 38/243 已扫描 |
