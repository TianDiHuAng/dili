# PROGRESS.md — 每次启动先读本文件（AUTONOMOUS 协议 ledger）

- 状态：正常循环（NORMAL）
- **检索路线：Crossref `query.bibliographic` → DOI → OpenAlex by-ID**（OpenAlex search 429 不可用）
- 当前轮次：**第 86 轮已完成，下一轮为第 87 轮**
- **第86轮：换检索策略（综述性语汇），G3 26→20**
  - 此前用「对象词 + 具体主题词」总命中侧面；本轮改用 **`history`/`state formation`/`political economy`/"in X movement"** 等综述语汇。
  - **9/10 有候选，登记 6 条**：
    | 条目 | 来源 | 被引 |
    |---|---|---|
    | 阿拉伯征服北非 | A History of the **Maghrib** in the Islamic Period (1987) | **400** |
    | 十字军东征 | The Fifth Crusade in Context (2016) | 8 |
    | 克里特文明 | Minoan In-House Relationships (2017) | 4 |
    | 河中地区 | Mongol invasion of Transoxiana 1219–1221 (2022) | 3 |
    | 萨珊波斯 | Sasanian Empire (2016) | 3 |
    | 桑海帝国 | The Fall of the Songhai Empire (2018) | 0 |
  - **四条仍不行**：笈多←**钱币**（连续两轮命中钱币学）、明清←**书籍流传史**、吠陀←非洲-印度泛论、马来群岛←0 候选。
  - **R20 第四次逼补别名**：Maghrib（前三次 indus→harappan、andes→andean、nazca→nasca）。
- 第86轮收尾：243 条全部 L2，737 来源。层级 **A180 / B50 / C0 / D13**。缺口 **G1=0 / G2=3 / G3a=4 / G3b=16（重要14/补充2）/ G4=243**。`check.py` R1–R25，0 错误。
- **目标达成度**：
  | 条件 | 状态 |
  |---|---|
  | 全部 243 条 L2 | **已达成** |
  | 每个条目都有强来源或属指标解读类（G1=0） | **已达成** |
  | 判据单一实现 + 经主动审计 | **已达成** |
  | R19–R25 七道机器校验 | 已上线，0 违规 |
  | 检索失败与无结果分离（D144） | 已落地，本轮 1% 失败 |
  | 每条（非 D 级）都有 ≥2 内容源 | 未达成（20 条：重要 14 + 补充 2 + G3a 4） |
  | G4 语义对题 | 50/243 已扫描 |
- 下一轮起点（第87轮）：
  1. **重要 G3b 剩 14 条**：吠陀时代、笈多王朝、明清、马来群岛、威尼斯、巴西高原、拉普拉塔平原、巴西殖民经济、大分水岭、毛利人、南极条约体系、洋流、气候带…
  2. 补充 G3b 剩 2 条（非洲大湖、西北海岸）+ G3a 4 条。
  3. **笈多王朝**已连续两轮只命中钱币学——若下轮再不行，建议按 D140 接受「钱币学侧面 + 正文限定」，或列为无整体研究。
- 不再写 ALL_DONE。
