# REPORT.md — 第 70 轮摘要

- 日期：2026-11-24
- 状态：正常循环（**G1：5 → 2，D 级清零**）

## 1. 换检索角度，补上 3 条强来源

上一轮用窄检索词（对象+主题槽全命中）在剩余 5 条上多无所获。本轮改用**宽对象词 + 至少一个主题槽**，并扩大检索式数量，结果：

| 条目 | 新强来源 | 被引 | 摘要 |
|---|---|---|---|
| 十字军东征 | Settlement, Identity, and Memory in the **Latin East** (2020) | 29 | 1,644 |
| 大平原 | Decadal heat and drought drive body size of North American **bison** (2019) | 27 | 1,706 |
| 克里特文明 | Seals, Craft, and Community in Bronze Age Crete (2016) | 31 | 955 |

三条都通过了摘要对读：
- **十字军**：摘要明确列出第一次十字军后形成的**四个政体**（耶路撒冷王国、安条克公国、埃德萨伯国、的黎波里伯国）；
- **大平原**：摘要写「大平原草原自史前以来一直支撑着数量最多的野牛」，并以数十年尺度检验热与干旱；
- **克里特**：标题是「印章」，但摘要讨论的是**「宫殿社会」的起源**——这正是本条需要的主题（上一轮剔除的那篇印章学是纯类型学，这篇不是）。

## 2. 两条未获（如实记录）

| 条目 | 候选 | 为何不用 |
|---|---|---|
| 隋唐 | Maintaining Gods in Medieval China（寺庙崇拜，引5）／Dressing for the Times（唐代服饰，引8） | 均属社会侧面，不撑「政体与制度」 |
| 澳大利亚大陆 | Land surface phenological response（引143） | 摘要未出现 Australia，不覆盖全境 |

## 3. 口径

- tools/check.py：ERRORS=0 ALL_PASS（243 条、665 来源；R1–R25）
- tools/check_links.py：BROKEN=0 LINKS_PASS
- 内容源 ≥2：237；1 个：6
- 层级：A 119 / B 122 / C 2 / **D 0（清零）**
- 侧面文献：side 34 / dropped 37 / weak 12

| 编号 | 缺口 | 条数 |
|---|---|---|
| **G1** | 无强来源 | **2**（上轮 5） |
| G2 | 检索确认无解 | 3 |
| G3 | 仅 1 内容源 | 6 |
| G4 | 语义对题未机器校验 | 243（已扫描 30 条） |
