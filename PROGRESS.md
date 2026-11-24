# PROGRESS.md — 每次启动先读本文件（AUTONOMOUS 协议 ledger）

- 状态：正常循环（NORMAL）
- **检索路线：Crossref `query.bibliographic` → DOI → OpenAlex by-ID**（OpenAlex search 429 不可用）
- 当前轮次：**第 101 轮已完成，下一轮为第 102 轮**
- **🏁 第101轮：核心缺口全部清零**
  | 条目 | 新第二来源 | 被引 |
  |---|---|---|
  | **尼罗河谷** | Re-Examination of Evidence for **Agricultural Origins in the Nile Valley** (1971) | **94** |
  | 黄河流域 | Evolution of agricultural civilization in the **Yellow River Basin** (2020) | 7 |
  | 长江流域 | Starch granule analysis…**Yangtze River Basin** Neolithic (2021) | 3 |
  | 古埃及早王朝 | Early Dynastic **Sealing Practices** as Reflection of State Formation (2018) | 3 |
  - **G3a 核心 1→0、G3b 核心 3→0。** 剩余 27 条全部为重要或补充级。
  - **D156 教训**：为古埃及早王朝找源时，我一开始去找《EARLY DYNASTIC EGYPT》（462引）——**它本来就在条目里**。真正缺的是第二个独立来源（Livius 首页被 D149 判 weak）。**补源前须先看条目已有 strong 来源。**
- 第101轮收尾：243 条全部 L2，781 来源（引用数见 SATURATION）。层级 **A194 / B27 / C0 / D22**。缺口 **G1=0 / G2=3 / G3a=13（核心0/重要3/补充10）/ G3b=14（核心0/重要10/补充4）/ G4=243**。`check.py` R1–R25，0 错误。
- **目标达成度**：
  | 条件 | 状态 |
  |---|---|
  | 全部 243 条 L2 | **已达成** |
  | A 级来源真实对位（全量复核） | **已达成** |
  | 每个条目都有强来源（G1=0） | **已达成** |
  | **核心条目全部有 ≥2 内容源** | **已达成（本轮清零）** |
  | 判据单一实现 + 收敛（D155） | **已达成** |
  | 机器校验 R19–R25 | 已上线，0 违规 |
  | 每条（非 D 级）都有 ≥2 内容源 | 未达成（**27 条，全为重要/补充级**） |
  | G4 语义对题 | 243/243 已扫描 |
- **剩余 27 条**：
  - G3a：重要 3（朝鲜半岛、中南半岛、黎凡特）/ 补充 10（多指标解读类）
  - G3b：重要 10（笈多、隋唐、明清、威尼斯、巴西高原、拉普拉塔、大分水岭、南极条约、冲积平原、山地农业）/ 补充 4（非洲大湖、西北海岸、荒漠化、卫星遥感）
- 下一轮起点（第102轮）：
  1. **G3b 重要 10 条**——其中 3 条已判无解（笈多、巴西高原、拉普拉塔），可跳过。
  2. **G3a 补充 10 条**多为指标解读类，需判断是否应归 D 级（D141 的边界）。
  3. G3a 重要 3 条（朝鲜半岛、中南半岛、黎凡特）。
- 不再写 ALL_DONE。
