# PROGRESS.md — 每次启动先读本文件（AUTONOMOUS 协议 ledger）

- 状态：正常循环（NORMAL）
- 当前轮次：**第 74 轮已完成，下一轮为第 75 轮**
- **第74轮：第二批核心 G3，登记 6 条；G3 88→83，G1 4→3**
  | 条目 | 新第二来源 | 被引 | 摘要 |
  |---|---|---|---|
  | 安第斯山脉 | Amazonia Through Time: **Andean Uplift**, Climate Change… (2010) | **2762** | 802 |
  | 澳大利亚大陆 | Climate change and Australia: Trends, projections and impacts (2003) | **941** | 3,793 |
  | 玛雅文明 | Ancestral Maya Economies in Archaeological Perspective (2010) | 191 | 1,121 |
  | 河流三角洲 | High-Resolution Stratigraphy of a Mississippi Subdelta-Lobe (2006) | 23 | 1,150 |
  | 大平原 | Ethnicity on the Great Plains (1980) | 12 | — |
  | 波利尼西亚 | Micronesian and Polynesian Voyaging (1976) | 5 | 2,690 |
  - **安第斯（2762）与澳大利亚大陆（941）是质量最高的两条**：前者直接讲「隆升如何改变气候与景观」，后者讲「全澳气候趋势与影响」，与本条 geo 段一一对得上。澳大利亚大陆的补上也解掉了 G1 一条。
- **两条不采用（如实记录）**：
  - **印加帝国** ← Machu Picchu（2005）：对象是**遗址**，第55轮已判不撑疆域/道路/行政，本轮再次不采用
  - 澳大利亚原住民 ← Reempowering Ourselves: Aboriginal **Women**（2010）：性别侧面
- 第74轮收尾：243 条全部 L2，677 来源。层级 **A123 / B117 / C1 / D2**。缺口 **G1=3 / G2=3 / G3=83 / G4=243**。`check.py` R1–R25，0 错误。
- **目标达成度**：
  | 条件 | 状态 |
  |---|---|
  | 全部 243 条 L2 | **已达成** |
  | 判据单一实现（D138） | **已达成** |
  | R19–R25 七道机器校验 | 已上线，0 违规 |
  | 每个条目都有强来源（G1=0） | 未达成（3 条：阿卡德帝国、隋唐、水资源管理） |
  | 每条都有 ≥2 内容源 | 未达成（84 条不足：83 + 1） |
  | G4 语义对题 | 38/243 已扫描 |
- 下一轮起点（第75轮）：
  1. **进入重要条目（43 条）**的 G3 补源——核心已基本处理完（仅印加、澳原住民、撒哈拉、东非大裂谷仍未获，已记录）。
  2. G1 三条：阿卡德帝国、隋唐、水资源管理（后者可能属指标解读类，可考虑判据调整）。
  3. 印加帝国已成为最难的一条（多次命中马丘比丘/玉米酒，均不撑国家层面）。
- 不再写 ALL_DONE。
