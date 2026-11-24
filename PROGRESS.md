# PROGRESS.md — 每次启动先读本文件（AUTONOMOUS 协议 ledger）

- 状态：正常循环（NORMAL）
- **检索路线：Crossref `query.bibliographic` → DOI → OpenAlex by-ID**（OpenAlex search 429 不可用）
- 当前轮次：**第 84 轮已完成，下一轮为第 85 轮**
- **第84轮：Crossref 路线 12/12 命中、HTTP 失败 0%**
  | 条目 | 来源 | 被引 | 摘要 |
  |---|---|---|---|
  | 的的喀喀湖 | Geology of the Lake Titicaca Region (1949) | **122** | 614 |
  | 奇穆帝国 | Imperialist Expansion in Peruvian Prehistory (1983) | **82** | 1,766 |
  | 纳斯卡文化 | Beyond the Nasca Lines (2016) | 22 | 1,434 |
  | 密克罗尼西亚 | Traditional Micronesian Societies (2017) | 22 | 2,141 |
  | 美拉尼西亚 | Change and Resilience in Melanesian Societies (2018) | 0 | **13,669** |
  | 基辅罗斯 | Position and Role of the Kyivan Rus' (2019) | 4 | 3,466 |
  | 南美贸易网络 | The Jaén Stone Bowl Tradition (2022) | 4 | 1,275 |
  | 新法兰西 | Power and Subsistence (2018) | 6 | 1,323 |
  | 查文文化 | Chavin culture (pre-Moche) (2016) | 2 | 909 |
  | 欧洲冰期地貌 | Dynamics of the Pleistocene glaciation (1986) | 0 | 953 |
  | 阿巴拉契亚山脉 | International Appalachian Trail (2019) | 0 | 1,499 |
  - 西北海岸不采用（当代文化旅游/商品化议题）。
- **R20 第三次逼我补别名**：纳斯卡实际用 **NASCA**（非 NAZCA）；冰期地貌用 **PLEISTOCENE/GLACIATION**。前两次是 indus→harappan、andes→andean。
- 第84轮收尾：243 条全部 L2，722 来源。层级 **A166 / B63 / C1 / D13**。缺口 **G1=1 / G2=3 / G3a=4 / G3b=29（补充仅 9）/ G4=243**。`check.py` R1–R25，0 错误。
- **目标达成度**：
  | 条件 | 状态 |
  |---|---|
  | 全部 243 条 L2 | **已达成** |
  | 判据单一实现 + 经主动审计 | **已达成** |
  | R19–R25 七道机器校验 | 已上线，0 违规 |
  | 检索失败与无结果分离（D144） | 已落地，实测 0% 失败 |
  | 每个条目都有强来源或属 D 级 | 未达成（1 条：隋唐） |
  | 每条（非 D 级）都有 ≥2 内容源 | 未达成（33 条） |
  | G4 语义对题 | 50/243 已扫描 |
- 下一轮起点（第85轮）：
  1. **补充 G3b 仅剩 9 条**：沙漠化、横贯南极山脉、罗斯海、南极科考站、太平洋殖民航线、室利佛逝、满者伯夷、非洲大湖地区、西北海岸。
  2. **重要 G3b 剩 19 条**：多为「文献只研究侧面」的政权类。
  3. 核心 1 条（澳大利亚原住民）、G1 1 条（隋唐）——再做最后一次尝试后列无解。
- 不再写 ALL_DONE。
