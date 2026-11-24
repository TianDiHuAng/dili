# REPORT.md — 第 75 轮摘要

- 日期：2026-11-24
- 状态：正常循环（**G3：83 → 74**）

## 1. 重要条目首批 12 条：登记 9 条

| 条目 | 新第二来源 | 被引 | 摘要 |
|---|---|---|---|
| 埃塞俄比亚高原 | Ethiopian vegetation types, climate and topography (2020) | **281** | — |
| 大津巴布韦 | The Rise and Fall of Zimbabwe (1972) | **114** | — |
| 古埃及新王国 | State Correspondence in the Ancient World (2014) | 24 | — |
| 亚述帝国 | Emblems of Power: Ideology and Identity in L… (2016) | 15 | — |
| 马格里布 | Trade and Religious Boundaries in the Medieval Maghrib (2019) | 4 | 5,197 |
| 古巴比伦 | Foreign Ruling Elites in Traditional State Societies (2014) | 4 | 4,076 |
| 加纳帝国 | Pioneers in Ancient Ghana (2014) | 0 | 858 |
| 斯瓦希里海岸 | The Swahili World (2022) | 0 | **13,723** |
| 帕提亚帝国 | Parthian kingdom – state of Iranians-Zoroastrians (2024) | 0 | 8,926 |

**中低被引但摘要长**是这批的特点：斯瓦希里那篇摘要 13,723 字符、被引 0；帕提亚 8,926 字符、被引 0。按 D117「被引≥10 **或** 正文≥800」，它们成立。

## 2. 三条不采用（两条对象碰撞）

| 条目 | 候选 | 问题 |
|---|---|---|
| **桑海帝国** | Assessment of farmers' perception of the effectiveness of **Songhai-Delta fish culture training programme** (2011) | 「Songhai」在此是**现代尼日尔河三角洲的养鱼培训项目名**，与桑海帝国无关 |
| 萨珊波斯 | Are Georgian-Sasanian **Coins** an Indicator of… (2016) | 钱币学，物质文化侧面，不撑国家与行政 |
| 阿拉伯征服北非 | Concepts, conquests, and contexts (2021) | 摩洛哥**民族主义史学**如何叙述征服，史学史侧面 |

## 3. 口径（tools/assess.py）

- tools/check.py：ERRORS=0 ALL_PASS（243 条、686 来源；R1–R25）
- tools/check_links.py：BROKEN=0 LINKS_PASS
- 层级：A 132 / B 108 / C 1 / D 2
- 内容源 ≥2：**168**；1 个：**74**；0 个：**1**
- 缺口：G1=3 / G2=3 / **G3=74** / G4=243

| 条件 | 状态 |
|---|---|
| 全部 243 条 L2 | **已达成** |
| 判据单一实现（D138） | **已达成** |
| R19–R25 七道机器校验 | 已上线，0 违规 |
| 每个条目都有强来源（G1=0） | 未达成（3 条） |
| 每条都有 ≥2 内容源 | 未达成（75 条不足） |
| G4 语义对题 | 38/243 已扫描 |
