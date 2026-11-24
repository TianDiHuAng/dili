# PROGRESS.md — 每次启动先读本文件（AUTONOMOUS 协议 ledger）

- 状态：正常循环（NORMAL）
- **检索路线：Crossref `query.bibliographic` → DOI → OpenAlex by-ID**（OpenAlex search 429 不可用）
- 当前轮次：**第 97 轮已完成，下一轮为第 98 轮**
- **第97轮：G3 56→48，重要 G3a 23→15，A 165→173**
  - 登记 8 条（12/12 命中、0% 失败）：
    | 条目 | 新第二来源 | 被引 |
    |---|---|---|
    | **拜占庭帝国** | A History of the Byzantine State and Society (1997) | **590** |
    | 尼罗河三角洲 | Clay Distributions, Grain Sizes, Sediment Transport (2013) | 35 |
    | 高卢 | Gaul (1996) | 34 |
    | 宋代 | Schooling, State, and Society in Song and Jin (2023) | 0 |
    | 古埃及古王国 | Egyptian Economic History (2014) | 0 |
    | 古埃及新王国 | Egypt: Ancient (New Kingdom) (2016) | 1 |
    | 伊比利亚半岛 | Iberian Peninsula: A Geographical Study (**1920 年教科书**) | 1 |
    | 突厥 | 高句丽—突厥汗国接触 (2016) | 1 |
  - **元代 ← 人民币汇率碰撞**：《Chinese **Yuan** after Exchange Rate Reform》（被引77）——**第四次纯同名碰撞**（前三次：Songhai 养鱼、Great Lakes 水泥、Dead Sea rift）。
  - 另三条不采用：黎凡特←性别考古、朝鲜半岛←当代和平协议、中南半岛←经济走廊。
- 第97轮收尾：243 条全部 L2，760 来源。层级 **A173 / B48 / C0 / D22**。缺口 **G1=0 / G2=3 / G3a=31（核心3/重要15/补充13）/ G3b=17（核心3/重要10/补充4）/ G4=243**。`check.py` R1–R25，0 错误。
- **目标达成度**：
  | 条件 | 状态 |
  |---|---|
  | 全部 243 条 L2 | **已达成** |
  | A 级来源真实对位（全量复核） | **已达成** |
  | 每个条目都有强来源（G1=0） | **已达成** |
  | 判据单一实现 | 已达成（四次收敛） |
  | 机器校验 R19–R25 | 已上线，0 违规 |
  | 每条（非 D 级）都有 ≥2 内容源 | 未达成（48 条，核心 6） |
  | G4 语义对题 | 243/243 已扫描 |
- 下一轮起点（第98轮）：
  1. **G3a 重要剩 15 条**（多瑙河、莱茵河、维京时代、巴尔干半岛、落基山脉、格陵兰岛、阿塔卡马沙漠、马丘比丘、大自流盆地、新西兰南岛、大堡礁 + 元代等）。
  2. G3a 补充 13 条；G3b 17 条（含无解 3 条）。
  3. 核心 G3a 3 条 + 核心 G3b 3 条 = 6 条核心缺口。
- **四种同名碰撞**（需记住的形态）：桑海←Songhai 养鱼项目、非洲大湖←Great Lakes 水泥、东非裂谷←Dead Sea rift、元代←Yuan 人民币。
- 不再写 ALL_DONE。
