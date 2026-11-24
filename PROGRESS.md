# PROGRESS.md — 每次启动先读本文件（AUTONOMOUS 协议 ledger）

- 状态：正常循环（NORMAL）
- 当前轮次：**第 69 轮已完成，下一轮为第 70 轮**
- **第69轮：G1 从 10 降到 5**
  | 条目 | 新强来源 | 被引 |
  |---|---|---|
  | 玛雅文明 | Climate and the **Collapse of Maya Civilization** (2003) | **1145** |
  | 维京时代 | Population genomics of the Viking world (2020) | **398** |
  | 澳大利亚原住民 | Archaeology of Australian Aboriginal Art (2002) | 169 |
  | 印加帝国 | Segmentary State Formation and Ritual Control of Water (1993) | 162 |
  | 孔雀王朝 | The Mauryan empire in early India (2006) | 24 |
- **一条重要教训（D136）**：为「隋唐」找到的候选《Son of Heaven and Heavenly Qaghan: Sui-Tang China and Its Neighbors》(1999, 引82)——**标题就是书名**，但它是 **book-review（对该书的书评）**。R25 当场拦下，我已清理据此写的落点句。**不能凭标题判断是著作还是书评**。
- **四条未获强来源（如实记录）**：
  - 澳大利亚大陆 ← Rodinia 超大陆拼合（地质史，不撑地形气候总体）
  - 十字军东征 ←「Amalfi **Before the Crusades**」商业史（时段在十字军之前，D108 否决）
  - 大平原 ← **加拿大**大平原水质（侧面且空间不符）
  - 克里特文明 ← 1939 年火山摧毁说（对象对位但过旧，学界多修正）
- 第69轮收尾：243 条全部 L2，662 来源。层级 **A119 / B119 / C3 / D2**。缺口 **G1=5 / G2=3 / G3=7 / G4=243**。`check.py` R1–R25，0 错误。
- **目标达成度（诚实版）**：
  | 条件 | 状态 |
  |---|---|
  | 全部 243 条 L2 | **已达成** |
  | 每个条目都有强来源（G1=0） | 未达成（G1=5） |
  | 证据层级 C/D 清零 | 未达成（C=3 / D=2） |
  | R19–R25 七道机器校验 | 已上线，0 违规 |
  | G4 语义对题 | 30/243 已扫描 |
  | 多维缺口连续 3 轮为零 | 未达成，`saturated=false` |
- 下一轮起点（第70轮）：
  1. **剩余 G1 五条**（隋唐、克里特文明、十字军东征、大平原、澳大利亚大陆）——继续找真正对位的强来源，或如实列入「无解」。
  2. **C 级 3 条 / D 级 2 条**需逐条看（D 级是指标解读类，可能合理）。
  3. limits.html 已能自动反映 G1=5，但「无解条目」清单（现仍写 5 条政权类）需与新数据对齐。
- 不再写 ALL_DONE。
