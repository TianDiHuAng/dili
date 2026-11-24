# PROGRESS.md — 每次启动先读本文件（AUTONOMOUS 协议 ledger）

- 状态：正常循环（NORMAL）
- **检索路线：Crossref `query.bibliographic` → DOI → OpenAlex by-ID**（OpenAlex search 429 不可用）
- 当前轮次：**第 104 轮已完成，下一轮为第 105 轮**
- **第104轮：G3 16→11，A 198→203**（G3a 7→2）
  | 条目 | 新第二来源 | 被引 | 备注 |
  |---|---|---|---|
  | 古埃及中王国 | The Middle Kingdom of Ancient Egypt: History, Archaeology and Society | **107** | 历史与考古视角 |
  | 争议边界处理原则 | Equitable Principles of Maritime Boundary Delimitation | **117** | 仅海洋划界，已注明 |
  | 黎凡特 | Structural Transformations in Settlement Systems of the Northern Levant | **98** | 阿姆克谷地，已注明 |
  | 朝鲜半岛 | Learning Geography of Korea by Mountains and Island | 1 | 教学性概述，证据弱，已注明 |
  | 中南半岛 | Land Use History in Montane Mainland Southeast Asia | 2 | 仅山地区域，已注明 |
  - 中南半岛另一候选（季风对流，被引 21）属大气科学，对象碰撞，不采用。
  - 教育机会地域差异、人文地理学：无通过候选，需换检索角度。
- **流程教训（第104轮）**：登记后须先依次运行 `tools/round68_levels.py` → `tools/round62_gaps.py` → `tools/round77_split.py` 重新生成 evidence_level.json 与缺口报告，再跑 check / check_links / round100_consist，最后 finalize。漏做会出现 R22 与一致性共约 10 处假报错（数据本身无误）。
- 第104轮收尾：243 条全部 L2。层级 **A203 / B11 / C0 / D29**。缺口 **G1=0 / G2=3 / G3=11（G3a 补充 2 / G3b 重要 6 + 补充 3）/ G4=243**。`check.py` 0 错误；`check_links.py` 0 断链；`round100_consist.py` 0 问题。
- **目标达成度**：
  | 条件 | 状态 |
  |---|---|
  | 全部 243 条 L2 | 已达成 |
  | A 级来源真实对位（全量复核） | 已达成 |
  | 每个条目都有强来源（G1=0） | 已达成 |
  | 核心条目全部有 ≥2 内容源 | 已达成 |
  | 每条（非 D 级）都有 ≥2 内容源 | 未达成（11 条，扣 3 条无解实追 8） |
  | G4 语义对题 | 243/243 已扫描 |
- **剩余 11 条**：
  - G3a 补充 2：教育机会地域差异、人文地理学
  - G3b 重要 6：笈多（无解）、隋唐、巴西高原（无解）、拉普拉塔（无解）、大分水岭、冲积平原
  - G3b 补充 3：非洲大湖、西北海岸、荒漠化
- 下一轮起点（第105轮）：
  1. G3a 补充 2 条换检索角度（教育机会、人文地理学）。
  2. G3b 可追 3 条重要（隋唐、大分水岭、冲积平原）+ 补充 3 条。
- 不再写 ALL_DONE。
