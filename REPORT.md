# REPORT.md — 第 85 轮摘要

- 日期：2026-11-24
- 状态：正常循环（**里程碑：G1 清零、C 级清零、核心 G3b 清零**）

## 1. 三个清零

| 指标 | 上轮 | **本轮** |
|---|---|---|
| G1 无强来源 | 1 | **0** |
| C 级（无强来源且非指标类） | 1 | **0** |
| 核心 G3b（仅 1 内容源） | 1 | **0** |
| A 级 | 166 | **174** |
| G3 总量 | 33 | **26** |

**含义**：243 条条目中，每一条要么有 ≥1 个强来源（A/B 级 230 条），要么属指标解读类（D 级 13 条，其机构长文即主体）。**没有一条是「无强来源」的。**

## 2. 本轮登记 9 条

| 条目 | 来源 | 被引 | 摘要 |
|---|---|---|---|
| 隋唐（**G1 最后一条**） | State Strengthening in the Tang Dynasty (2022) | 0 | 992 |
| 横贯南极山脉 | The Transantarctic Mountains of southern Victoria Land (1992) | **249** | 2,406 |
| 沙漠化 | Projected Global Dryland Expansion Discrepancy (2025) | 30 | 1,412 |
| 满者伯夷 | De Kraton van Majapahit (1948, **荷兰语**) | 20 | 2,567 |
| 南极科考站 | On thick ice: scientific internationalism (2008) | 45 | 1,025 |
| 太平洋殖民航线 | Lapita and Western Pacific Settlement (2007) | 35 | 441 |
| 罗斯海 | Quaternary Benthic Foraminiferal Distribution in the Ross Sea (1999) | 3 | 2,278 |
| 室利佛逝 | Srivijaya, Kingdom of (2016) | 3 | 932 |
| 澳大利亚原住民（**核心最后一条**） | Heritage archaeology in Australia (2000) | 0 | 1,726 |

**隋唐**这条是 G1 的最后一条——多次检索都命中墓碑、服饰、寺庙崇拜等侧面，这次用「State Strengthening」对象词命中一篇专论唐代国家强化的章节。

## 3. 一条对象碰撞

**非洲大湖地区** ←《Cement Production and Trade on the **Great Lakes**》(1944)——研究对象是**北美五大湖**的水泥工业与航运。`Great Lakes` 在地理上指两个完全不同的湖群，纯靠对象词无法区分。

## 4. 口径

- tools/check.py：ERRORS=0 ALL_PASS（243 条、731 来源；R1–R25）
- tools/check_links.py：BROKEN=0 LINKS_PASS
- 层级：**A 174** / B 56 / **C 0** / D 13
- 内容源 ≥2：**208**；1 个：34；0 个：1
- 缺口：**G1=0** / G2=3 / G3a=4 / G3b=22（重要 20 / 补充 2） / G4=243

| 条件 | 状态 |
|---|---|
| 全部 243 条 L2 | **已达成** |
| **每个条目都有强来源或属指标解读类（G1=0）** | **已达成** |
| 判据单一实现 + 经主动审计 | **已达成** |
| R19–R25 七道机器校验 | 已上线，0 违规 |
| 检索失败与无结果分离（D144） | 已落地，连续两轮 0% 失败 |
| 每条（非 D 级）都有 ≥2 内容源 | 未达成（26 条，其中补充类仅 2） |
| G4 语义对题 | 50/243 已扫描 |
