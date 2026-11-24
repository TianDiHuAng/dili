# REPORT.md — 第 69 轮摘要

- 日期：2026-11-24
- 状态：正常循环（**G1：10 → 5**）

## 1. 为 G1 十条找真正的强来源

| 条目 | 新强来源 | 被引 |
|---|---|---|
| 玛雅文明 | Climate and the **Collapse of Maya Civilization** (2003) | **1145** |
| 维京时代 | Population genomics of the Viking world (2020) | **398** |
| 澳大利亚原住民 | Visions from the Past: Archaeology of Australian Aboriginal Art (2002) | 169 |
| 印加帝国 | Segmentary State Formation and the Ritual Control of Water (1993) | 162 |
| 孔雀王朝 | The Mauryan empire in early India (2006) | 24 |

**G1：10 → 5**；层级 A 119 / B 119 / C 3 / D 2。

## 2. 一条重要教训：书评的标题可能就是书名

我为「隋唐」检索到一个看起来完美的候选：《Son of Heaven and Heavenly Qaghan: Sui-Tang China and Its Neighbors》(1999, 被引 82)。
**标题就是那本书的书名**——但它是一条 **book-review**，即对这本书的**书评**，不是书本身。
R25 当场报错拦下，我随即清理了据此写下的落点句（否则又是一次「用书评撑正文」）。
教训：**不能凭标题判断一条记录是著作还是书评**，必须看 `type`（D136）。

## 3. 四条未获强来源（如实记录）

| 条目 | 候选 | 为何不用 |
|---|---|---|
| 澳大利亚大陆 | Refining Rodinia: Australia–Western U.S. connection (1999, 引668) | 讲**前寒武超大陆拼合**，不支撑大陆地形气候总体 |
| 十字军东征 | Commerce of Amalfi **Before the Crusades** (1968, 引155) | 时段是「十字军**之前**」，D108 时期槽否决 |
| 大平原 | Water quality in the **Canadian** Great Plains (1999, 引407) | 只涉加拿大段水质，与农业/野牛/交通/沙尘暴无对应 |
| 克里特文明 | The Volcanic Destruction of Minoan Crete (**1939**, 引224) | 对象对位但为 1939 年火山摧毁说，学界后多修正 |

## 4. 口径

- tools/check.py：ERRORS=0 ALL_PASS（243 条、662 来源；R1–R25）
- tools/check_links.py：BROKEN=0 LINKS_PASS
- 内容源 ≥2：236；1 个：7
- 层级：A 119 / B 119 / C 3 / D 2
- 侧面文献：side 34 / dropped 37 / weak 12

| 编号 | 缺口 | 条数 |
|---|---|---|
| **G1** | 无强来源 | **5**（上轮 10） |
| G2 | 检索确认无解 | 3 |
| G3 | 仅 1 内容源 | 7 |
| G4 | 语义对题未机器校验 | 243（已扫描 30 条） |
