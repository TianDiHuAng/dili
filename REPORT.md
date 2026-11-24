# REPORT.md — 第 73 轮摘要

- 日期：2026-11-24
- 状态：正常循环（**G3：93 → 88**）

## 1. 为首批 8 条核心 G3 找第二内容源

| 条目 | 新第二来源 | 被引 | 摘要 |
|---|---|---|---|
| 爱琴海世界 | Modelling maritime interaction in the Aegean Bronze Age (2008) | **251** | 749 |
| 白令陆桥 | The Colonization of Beringia and the Peopling of the New World (1993) | **241** | 742 |
| 罗马帝国 | Market-Days in the Roman Empire (1970) | 198 | 1,995 |
| 两河流域 | Soil Salinity Mapping…in Mesopotamia (2014) | 129 | 1,552 |
| 文艺复兴意大利 | The Economy of Renaissance Italy (2022) | 11 | 1,333 |
| 马里帝国 | Sociological reflections on the empire of Mali (2004) | 9 | 848 |

**两条须注意限定**：
- **两河流域**：那篇是**现代伊拉克**的土壤盐渍化遥感测绘，不是古代灌溉史——落点句已写明「该文是现代测绘，不作古代灌溉史的定论」。
- **马里帝国**：被引仅 9（<10），但摘要 848 字符 ≥800，按 D117「满足其一」成立。

## 2. 两条对象碰撞（不采用）

| 条目 | 候选 | 问题 |
|---|---|---|
| 撒哈拉沙漠 | Global warming drives changes in **carnivore communities** (2017) | 主题是食肉动物，与沙漠无关 |
| **东非大裂谷** | …paleohydrology of the **Dead Sea** rift valley (2006) | **死海裂谷**，地名碰撞 |

## 3. 口径（全部来自 tools/assess.py）

- tools/check.py：ERRORS=0 ALL_PASS（243 条、671 来源；R1–R25）
- tools/check_links.py：BROKEN=0 LINKS_PASS
- 层级：A 120 / B 119 / C 2 / D 2
- 内容源 ≥2：**154**；1 个：**88**；0 个：**1**
- 缺口：G1=4 / G2=3 / **G3=88** / G4=243
- 侧面文献：side 34 / dropped 37 / weak 12

| 条件 | 状态 |
|---|---|
| 全部 243 条 L2 | **已达成** |
| 判据单一实现（D138） | **已达成** |
| R19–R25 七道机器校验 | 已上线，0 违规 |
| 每个条目都有强来源（G1=0） | 未达成（4 条） |
| 每条都有 ≥2 内容源 | 未达成（89 条不足） |
| G4 语义对题 | 38/243 已扫描 |
