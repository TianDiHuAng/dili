# PROGRESS.md — 每次启动先读本文件（AUTONOMOUS 协议 ledger）

- 状态：正常循环（NORMAL）——**注意：OpenAlex search 端点配额耗尽，须用 Crossref 路线**
- 当前轮次：**第 82 轮已完成，下一轮为第 83 轮**
- **第82轮：识别出 API 故障，撤销 12 条错误结论**
  - 本轮检索 12 条补充条目，**全部 0 候选**——数字本身可疑（赫梯、神圣罗马帝国、汉萨同盟都是文献极丰富的主题）。
  - 按 D065 去验证 API：
    | 端点 | 结果 |
    |---|---|
    | `openalex works?**search**=` | **HTTP 429**（free daily budget used up, $0 remaining） |
    | `openalex works/`**`{ID}`** | 200 ✅ |
    | `crossref query.bibliographic` | 200 ✅ |
  - **结论：OpenAlex search 日配额耗尽**（全网络 IP 共享），脚本把失败静默当成「0 候选」。
  - **撤销 12 条错误记录**，改用 **Crossref 路线**（`query.bibliographic` → DOI → `openalex works/{ID}`）验证 **3/3 命中**：
    | 条目 | 来源 | 被引 |
    |---|---|---|
    | 神圣罗马帝国 | Associative Political Culture in the Holy Roman Empire (2018) | **39** |
    | 赫梯王国 | The Hittite Empire from Textual Evidence (2012) | 21 |
    | 汉萨同盟 | The Hanseatic League (2024) | 0（摘要≥800） |
- 第82轮收尾：243 条全部 L2，705 来源。层级 **A149 / B80 / C1 / D13**。缺口 **G1=1 / G2=3 / G3a=4 / G3b=46 / G4=243**。`check.py` R1–R25，0 错误。
- **目标达成度**：
  | 条件 | 状态 |
  |---|---|
  | 全部 243 条 L2 | **已达成** |
  | 判据单一实现 + 经主动审计 | **已达成** |
  | R19–R25 七道机器校验 | 已上线，0 违规 |
  | 检索失败与无结果分离（D144） | **本轮建立** |
  | 每个条目都有强来源或属 D 级 | 未达成（1 条：隋唐） |
  | 每条（非 D 级）都有 ≥2 内容源 | 未达成（50 条） |
  | G4 语义对题 | 50/243 已扫描 |
- 下一轮起点（第83轮）：
  1. **必须用 Crossref 路线**（`tools/round82_crossref.py` 可复用），OpenAlex search 不可靠。
  2. **重跑上轮那 12 条**中被撤销的 9 条：古埃及中王国、法蒂玛王朝、非洲大湖地区、贵霜帝国、仰韶文化、室利佛逝、满者伯夷、帖木儿帝国、迈锡尼文明。
  3. 剩余：重要 G3b 19 条、补充 G3b 26 条、核心 1 条（澳大利亚原住民）、G1 1 条（隋唐）。
- 不再写 ALL_DONE。
