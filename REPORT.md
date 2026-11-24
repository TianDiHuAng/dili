# REPORT.md — 第 96 轮摘要

- 日期：2026-11-24
- 状态：正常循环（**G3：62 → 56，核心 G3a 9→3**）

## 1. 核心 G3a 9 条：登记 6 条

| 条目 | 新第二来源 | 被引 | 摘要 |
|---|---|---|---|
| 苏美尔城邦 | Early Mesopotamian urbanism: a new view (2007) | **244** | 1,067 |
| 撒哈拉沙漠 | The impact of Sahara **desertification** on Arctic cooling (2015) | 21 | 1,150 |
| 汉代 | **War economy** during the Western Han Dynasty (2019) | 1 | 945 |
| 大平原 | The Great Plains: **Agriculture and the Environment** (2001) | 1 | 999 |
| 马里帝国 | The Grand Empires of the **Sahel**: Gold, Trade (2025) | 0 | 935 |
| 南极冰盖 | Present and future **Ross Ice Shelf** dynamics (2023) | 0 | 3,172 |

**撒哈拉那条是意外的好**：研究的是「撒哈拉沙漠化对全新世北极降温的影响」——正是本条要的「干旱化与全球气候耦合」机制，而不是又一次「20 世纪非洲气候」。
**苏美尔**那条被引 244，是本轮最高。

## 2. 三条不采用

| 条目 | 候选 | 问题 |
|---|---|---|
| 澳大利亚大陆 | Australian Participation in the **IPCC** | 国际气候治理的政策史 |
| 波利尼西亚 | Southeast **Solomon Islands** in regional perspective | **所罗门群岛属美拉尼西亚**，与波利尼西亚文化圈不同（对象偏差） |
| 长江流域 | Geographic patterns of **industrial water consumption** | 现代工业用水的地理格局 |

## 3. R20 第七、第八次逼我补别名

| 条目 | 来源标题实际用词 | 补入 |
|---|---|---|
| 马里帝国 | **SAHEL**（萨赫勒） | `sahel`、`saharan` |
| 苏美尔城邦 | **MESOPOTAMIAN** | `mesopotamia`、`mesopotamian` |

前六次：indus→harappan、andes→andean、nazca→nasca、conquest→maghrib、zone→biome、malay→southeast asia。
**R20 现在是全项目触发次数最多的规则（8 次）**，每次都在我自以为完成时冒出来——它的价值就在这。

## 4. 口径

- tools/check.py：ERRORS=0 ALL_PASS（243 条、752 来源；R1–R25）
- tools/check_links.py：BROKEN=0 LINKS_PASS
- 层级：**A 165** / B 56 / C 0 / D 22
- 内容源 ≥2：**165**；1 个：76；0 个：2
- 缺口：G1=0 / G2=3 / **G3a=39**（核心 3） / G3b=17 / G4=243

| 条件 | 状态 |
|---|---|
| 全部 243 条 L2 | **已达成** |
| A 级来源真实对位（全量复核） | **已达成** |
| 每个条目都有强来源（G1=0） | **已达成** |
| 判据单一实现 | 已达成（四次收敛） |
| 机器校验 R19–R25 | 已上线，0 违规 |
| 每条（非 D 级）都有 ≥2 内容源 | 未达成（56 条，核心仅 6） |
| G4 语义对题 | 243/243 已扫描 |
