# REPORT.md — 第 84 轮摘要

- 日期：2026-11-24
- 状态：正常循环（**G3：44 → 33**）

## 1. Crossref 路线非常稳定：12/12 命中、0% 失败

沿用上轮 D144 合规脚本（记录 HTTP 状态、失败率阈值），本轮 12 条补充条目**全部命中，HTTP 失败 0 次**（成功 485）。

| 条目 | 来源 | 被引 | 摘要 |
|---|---|---|---|
| 的的喀喀湖 | Geology of the Lake Titicaca Region (1949) | **122** | 614 |
| 奇穆帝国 | Imperialist Expansion in Peruvian Prehistory (1983) | **82** | 1,766 |
| 纳斯卡文化 | Beyond the Nasca Lines (2016) | 22 | 1,434 |
| 密克罗尼西亚 | Traditional Micronesian Societies (2017) | 22 | 2,141 |
| 美拉尼西亚 | Change and Resilience in Melanesian Societies (2018) | 0 | **13,669** |
| 基辅罗斯 | Position and Role of the Kyivan Rus' (2019) | 4 | 3,466 |
| 南美贸易网络 | The Jaén Stone Bowl Tradition (2022) | 4 | 1,275 |
| 新法兰西 | Power and Subsistence: Political Economy (2018) | 6 | 1,323 |
| 查文文化 | Chavin culture (pre-Moche) (2016) | 2 | 909 |
| 欧洲冰期地貌 | Dynamics of the Pleistocene glaciation (1986) | 0 | 953 |
| 阿巴拉契亚山脉 | Connecting Trail: International Appalachian Trail (2019) | 0 | 1,499 |

## 2. 一条不采用

**西北海岸** ←《Incorporating Culture: How Indigenous People Are Reshaping…》(2018)：主题是**文化旅游与文化商品化**（当代议题），不支撑「传统社会与资源管理」。

## 3. R20 又抓到两个别名

| 条目 | 来源标题实际用词 | 补入对象词 |
|---|---|---|
| 纳斯卡文化 | **NASCA**（非 NAZCA） | `nasca` |
| 欧洲冰期地貌 | **PLEISTOCENE / GLACIATION** | `pleistocene`、`glaciation` |

这是 R20 第三次逼我补别名（前两次：indus→harappan、andes→andean）。**它是目前性价比最高的规则**——每次都在我自以为完成时冒出来。

## 4. 口径

- tools/check.py：ERRORS=0 ALL_PASS（243 条、722 来源；R1–R25）
- tools/check_links.py：BROKEN=0 LINKS_PASS
- 层级：**A 166** / B 63 / C 1 / D 13
- 内容源 ≥2：**200**；1 个：41；0 个：2
- 缺口：G1=1 / G2=3 / G3a=4 / **G3b=29**（补充仅 9） / G4=243

| 条件 | 状态 |
|---|---|
| 全部 243 条 L2 | **已达成** |
| 判据单一实现 + 经主动审计 | **已达成** |
| R19–R25 七道机器校验 | 已上线，0 违规 |
| 检索失败与无结果分离（D144） | 已落地，实测 0% 失败 |
| 每个条目都有强来源或属 D 级 | 未达成（1 条：隋唐） |
| 每条（非 D 级）都有 ≥2 内容源 | 未达成（33 条） |
| G4 语义对题 | 50/243 已扫描 |
