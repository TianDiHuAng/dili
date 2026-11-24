# REPORT.md — 第 104 轮摘要

- 日期：2026-11-24
- 状态：正常循环（**G3：16 → 11**）

## 1. G3a 剩余 7 条：5 条命中

| 条目 | 新补第二来源 | 被引 | 说明 |
|---|---|---|---|
| 古埃及中王国 | The Middle Kingdom of Ancient Egypt: History, Archaeology and Society (2006) | **107** | 历史与考古的社会视角 |
| 争议边界处理原则 | Equitable Principles of Maritime Boundary Delimitation (2015) | **117** | 仅海洋划界，已在条目注明 |
| 黎凡特 | Structural Transformations in Settlement Systems of the Northern Levant (2007) | **98** | 阿姆克谷地聚落，已注明样本范围 |
| 朝鲜半岛 | Learning Geography of Korea by Mountains and Island (2024) | 1 | 教学性概述，证据强度有限，已注明 |
| 中南半岛 | Land Use History in Montane Mainland Southeast Asia (2005) | 2 | 仅山地大陆东南亚，被引很少，已注明 |

## 2. 未命中与碰撞

- 教育机会地域差异、人文地理学：本轮无通过候选，需换检索角度。
- 中南半岛的另一候选（2007，被引 21）研究季风对流起始，属大气科学，不采用。

## 3. 流程教训

登记后首次校验出现 R22 与一致性共 10 处问题，原因是 `evidence_level.json` 与缺口报告未重新生成（数据本身无误）。
**登记后须先依次运行 `round68_levels.py` → `round62_gaps.py` → `round77_split.py`，再做校验与收尾。**

## 4. 口径与验证

- tools/check.py：ERRORS=0 ALL_PASS（243 条、790 来源）
- tools/check_links.py：BROKEN=0 LINKS_PASS
- `round100_consist.py`：一致性 0 问题
- 层级：**A 203** / B 11 / C 0 / D 29
- 内容源 ≥2：**203**；1 个：38；0 个：2
- 缺口：G1=0 / G2=3 / G3a=2 / G3b=9 / G4=243

## 5. 剩余 11 条

| 类别 | 条数 | 内容 |
|---|---|---|
| G3a 补充 | 2 | 教育机会地域差异、人文地理学 |
| G3b 重要 | 6 | 笈多（无解）、隋唐、巴西高原（无解）、拉普拉塔（无解）、大分水岭、冲积平原 |
| G3b 补充 | 3 | 非洲大湖、西北海岸、荒漠化 |

扣掉 3 条无解，实际在追 8 条。
