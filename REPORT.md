# REPORT.md — 第 99 轮摘要

- 日期：2026-11-24
- 状态：正常循环（**G3：37 → 31，G3a 核心仅剩 1**）

## 1. 登记 6 条

| 条目 | 新第二来源 | 被引 | 摘要 |
|---|---|---|---|
| **澳大利亚大陆** | Tectonic Framework and Evolution of the **Gawler Craton** (2007) | **283** | 4,228 |
| 南锥体 | Biogeographical history of Petunia/Calibrachoa（**潘帕斯**禾草） (2012) | **115** | 1,122 |
| 波利尼西亚 | The **Polynesian settlement** of the Hawaiian Archipelago (1995) | **82** | 944 |
| 南极科考站 | Antarctic Research Stations: Parallels for… (2010) | 11 | 759 |
| 南极特别保护区 | Antarctic **Specially Protected Species** conservation tool (2024) | 8 | 1,689 |
| 大自流盆地 | Silica springs of the **eastern Great Artesian Basin** (2025) | 1 | 1,590 |

**大自流盆地这次对位了**：上一轮命中南非 Uitenhage 盆地（同名碰撞），这轮换了 `Great Artesian Basin` 全称 + `hydrogeology` 组合，命中「澳大利亚东北部 Great Artesian Basin 东缘 50 处 silica 温泉」，摘要明白写着 northeastern Australia。
**同一个条目、两轮不同的结果**——上一轮是碰撞，这一轮是对的。这说明碰撞不等于无解，**换检索词能救回来**。

## 2. 四条不采用

| 条目 | 候选 | 问题 |
|---|---|---|
| 朝鲜半岛 | Inventing History: Two **Historical Fictions** | 文学 |
| 黎凡特 | Size Matters – **Donkeys and Horses** | 动物考古 |
| 长江流域 | Severe **Drought** on Freshwater (2026) | 现代干旱 |
| 中南半岛 / 争议边界处理原则 | 本轮 **0 候选** |

**古埃及中王国**那条（《Poetry and Culture》, 被引95）这次登记了——它第92轮曾因「文学侧面」被判过。区别在于：**本轮落点句明确限定「该文聚焦文学，不涉经济与行政」**，而它对象对位（中王国）、被引 95。
这是 D140 的思路：**侧面文献在明确限定的前提下可以登记**，而不是一概判退。

## 3. R20 第九次逼我补别名

南锥体的来源标题用 **PAMPAS**（潘帕斯）→ 补 `pampas`、`pampa`、`patagonia`。
九次：indus、andes、nazca、maghrib、biome、southeast asia、sahel、mesopotamian、**pampas**。

## 4. 口径

- tools/check.py：ERRORS=0 ALL_PASS（243 条、777 来源；R1–R25）
- tools/check_links.py：BROKEN=0 LINKS_PASS
- 层级：**A 190** / B 31 / C 0 / D 22
- 内容源 ≥2：**190**；1 个：51；0 个：2
- 缺口：G1=0 / G2=3 / **G3a=14**（核心 1 / 重要 3 / 补充 10） / G3b=17 / G4=243

| 条件 | 状态 |
|---|---|
| 全部 243 条 L2 | **已达成** |
| A 级来源真实对位（全量复核） | **已达成** |
| 每个条目都有强来源（G1=0） | **已达成** |
| 判据单一实现 | 已达成（四次收敛） |
| 机器校验 R19–R25 | 已上线，0 违规 |
| 每条（非 D 级）都有 ≥2 内容源 | 未达成（31 条，核心 4） |
| G4 语义对题 | 243/243 已扫描 |

## 5. 剩余 31 条的结构

| 类别 | 条数 | 备注 |
|---|---|---|
| G3a 核心 | **1** | 长江流域 |
| G3a 重要 | 3 | 朝鲜半岛、中南半岛、黎凡特 |
| G3a 补充 | 10 | 多为指标解读类（人口年龄结构、预期寿命、全球人口规模…） |
| **G3b 核心** | **3** | 尼罗河谷、古埃及早王朝、黄河流域 |
| G3b 重要 | 10 | 笈多、隋唐、明清、威尼斯、巴西高原、拉普拉塔、大分水岭、南极条约、冲积平原、山地农业 |
| G3b 补充 | 4 | 非洲大湖、西北海岸、荒漠化、卫星遥感 |

**核心共 4 条**（G3a 1 + G3b 3），比上轮的 6 条又少了 2 条。
