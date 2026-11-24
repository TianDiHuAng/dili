# PROGRESS.md — 每次启动先读本文件（AUTONOMOUS 协议 ledger）

- 状态：正常循环（NORMAL）
- **检索路线：Crossref `query.bibliographic` → DOI → OpenAlex by-ID**（OpenAlex search 429 不可用）
- 当前轮次：**第 98 轮已完成，下一轮为第 99 轮**
- **第98轮：单轮登记 11 条（最多）；G3 48→37，A 173→184**
  | 条目 | 新第二来源 | 被引 |
  |---|---|---|
  | **阿塔卡马沙漠** | Oligocene–Miocene age of aridity in the Atacama (2005) | **505** |
  | **格陵兰岛** | Greenland ice sheet hydrology: A review (2013) | **239** |
  | **莱茵河** | Holocene **avulsion** history of the River Rhine (1994) | **194** |
  | 多瑙河 | Hydrology and floodplain processes (1999) | 55 |
  | 落基山脉 | Large-scale geomorphology and fission-track (1998) | 39 |
  | 维京时代 | Viking Expansion Northwards (1995) | 18 |
  | 新西兰南岛 | Stratigraphy and Paleoecology (1975) | 15 |
  | 马丘比丘 | **Inca Foundations**, Site Preparation, Drainage (2012) | 5 |
  | 大堡礁 | Taxonomy and ecology of corals (2002) | 2（摘要5705） |
  | 巴尔干半岛 | The Balkans: History, Religion and Society (2024) | 0（摘要**7541**） |
  | **元代** | The **Mongol Yuan Dynasty** in China (2023) | 0 |
  - **元代终于找到对位的**（此前是 Yuan=人民币汇率碰撞）。
  - **第五种同名碰撞**：大自流盆地 ←《Uitenhage Artesian Basin》实为**南非东开普省**的盆地，与澳大利亚 Great Artesian Basin 不同。
- 第98轮收尾：243 条全部 L2，771 来源。层级 **A184 / B37 / C0 / D22**。缺口 **G1=0 / G2=3 / G3a=20（核心3/重要4/补充13）/ G3b=17（核心3/重要10/补充4）/ G4=243**。`check.py` R1–R25，0 错误。
- **目标达成度**：
  | 条件 | 状态 |
  |---|---|
  | 全部 243 条 L2 | **已达成** |
  | A 级来源真实对位（全量复核） | **已达成** |
  | 每个条目都有强来源（G1=0） | **已达成** |
  | 判据单一实现 | 已达成（四次收敛） |
  | 机器校验 R19–R25 | 已上线，0 违规 |
  | 每条（非 D 级）都有 ≥2 内容源 | 未达成（37 条，**核心 6**） |
  | G4 语义对题 | 243/243 已扫描 |
- 三轮回补 **25 条**（96→98），且**未出现新的虚高**——判据已收敛。
- 下一轮起点（第99轮）：
  1. **G3a 剩余 20 条**（核心3/重要4/补充13）。
  2. **G3b 17 条**（核心3/重要10/补充4，含无解 3 条）。
  3. 五种同名碰撞清单：Songhai 养鱼、Great Lakes 水泥、Dead Sea rift、Yuan 人民币、Uitenhage 盆地。
- 不再写 ALL_DONE。
