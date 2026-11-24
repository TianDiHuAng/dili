# PROGRESS.md — 每次启动先读本文件（AUTONOMOUS 协议 ledger）

- 状态：正常循环（NORMAL）
- **检索路线：Crossref `query.bibliographic` → DOI → OpenAlex by-ID**（OpenAlex search 429 不可用）
- 当前轮次：**第 93 轮已完成，下一轮为第 94 轮**
- **第93轮：A 级全量复核 europe+north-america（42 条）——查出同域名多页问题**
  - 三类问题：
    1. **同一网站多页当独立来源（12 条）**：古希腊城邦用 livius.org **3 页**（Polis+Athens+Greece）、罗马共和国用 2 页、湄公河/亚马逊/土壤用 fao.org 2 页、板块构造用 usgs.gov 2 页、科罗拉多高原用 nps.gov 2 页、OWID/WHO/NCEI/NASA EO 各 2 页。
    2. **层级与内容源口径不一致**：`content_count` 认域名、`level_of` 不认（D146 同类换维度）。
    3. **书评 type 标成「学术文献」**：莱茵河 ←《The Rhine: An Eco-Biography…》**(review)**，DOI 为 Technology and Culture 书评，R25 漏检（D136 再实例）。
  - **D150**：`content_count` 按域名去重（openalex/wikidata 除外）。
  - **D151**：`level_of` 判 A 须 `strong>=2` **且** `content_count>=2`。
  - **数字**：**A 171→168、D 19→22、G3 53（G3a 34 / G3b 19）**。
- 第93轮收尾：243 条全部 L2，742 来源。层级 **A168 / B53 / C0 / D22**。缺口 **G1=0 / G2=3 / G3a=34 / G3b=19 / G4=243**。`check.py` R1–R25，0 错误。
- **目标达成度**：
  | 条件 | 状态 |
  |---|---|
  | 全部 243 条 L2 | **已达成** |
  | 每个条目都有强来源或属指标解读类（G1=0） | **已达成** |
  | 判据单一实现 | **已达成（D146+D150+D151 三次收敛）** |
  | 机器校验 R19–R25 | 已上线，0 违规 |
  | **A 级来源真实对位** | **已复核 94/168（africa/asia/europe/n-america）** |
  | 每条（非 D 级）都有 ≥2 内容源 | 未达成（53 条） |
  | G4 语义对题 | 164/243 已扫描 |
- 下一轮起点（第94轮）：
  1. **继续 A 级全量复核**：south-america / oceania / antarctica / global-themes（剩余 74 条）。
  2. 之后 G3a 34 条补源。
- 不再写 ALL_DONE。
