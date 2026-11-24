# REPORT.md — 第 86 轮摘要

- 日期：2026-11-24
- 状态：正常循环（**G3：26 → 20**）

## 1. 换了检索词策略：用综述性语汇

此前对这批政权类条目，我总是用「对象词 + 具体主题词（state/administration/economy）」检索，结果命中的多是侧面（钱币、铭文、墓葬、方言、医学、性别）。
本轮改用**综述性语汇**——`history`、`state formation`、`political economy`、`in crusading movement` 等，让检索偏向「整体研究」而非「某个专题」。

**结果：9/10 有候选，登记 6 条**：

| 条目 | 来源 | 被引 | 摘要 |
|---|---|---|---|
| 阿拉伯征服北非 | A History of the **Maghrib** in the Islamic Period (1987) | **400** | 1,108 |
| 桑海帝国 | The Fall of the Songhai Empire (2018) | 0 | 937 |
| 十字军东征 | The Fifth Crusade in Context: Crusading Movement (2016) | 8 | 1,247 |
| 克里特文明 | Understanding Minoan In-House Relationships (2017) | 4 | 2,001 |
| 萨珊波斯 | Sasanian Empire (2016) | 3 | 800 |
| 河中地区 | Mongol invasion of Transoxiana 1219–1221 (2022) | 3 | 1,310 |

**阿拉伯征服北非那条被引 400**——是马格里布伊斯兰时期的通史，正是本条整体背景所需。

## 2. 四条仍不行（三条还是侧面）

| 条目 | 候选主题 |
|---|---|
| 笈多王朝 | **钱币之美**（第二次命中钱币学，第76轮也命中过「Role of Coins」） |
| 明清 | **一本书的编辑与流传史**（书籍史） |
| 吠陀时代 | **非洲—印度的史前邻近性**（泛论，不涉吠陀） |
| 马来群岛 | 本轮 0 候选 |

**笈多王朝这条已经连续两轮命中钱币学**——该主题的英文文献确实以钱币研究为主。这不是检索问题。

## 3. R20 第四次逼我补别名

阿拉伯征服北非的来源标题用的是 **MAGHRIB**（不是 ARAB 或 NORTH AFRICA）→ 对象词补 `maghrib`、`north africa`。
前三次：indus→harappan、andes→andean、nazca→nasca。

## 4. 口径

- tools/check.py：ERRORS=0 ALL_PASS（243 条、737 来源；R1–R25）
- tools/check_links.py：BROKEN=0 LINKS_PASS
- 层级：**A 180** / B 50 / C 0 / D 13
- 内容源 ≥2：**214**；1 个：28；0 个：1
- 缺口：G1=0 / G2=3 / G3a=4 / **G3b=16**（重要 14 / 补充 2） / G4=243

| 条件 | 状态 |
|---|---|
| 全部 243 条 L2 | **已达成** |
| 每个条目都有强来源或属指标解读类（G1=0） | **已达成** |
| 判据单一实现 + 经主动审计 | **已达成** |
| R19–R25 七道机器校验 | 已上线，0 违规 |
| 检索失败与无结果分离（D144） | 已落地，本轮 1% 失败 |
| 每条（非 D 级）都有 ≥2 内容源 | 未达成（20 条，重要 14 / 补充 2） |
| G4 语义对题 | 50/243 已扫描 |
