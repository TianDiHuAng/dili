# REPORT.md — 第 82 轮摘要

- 日期：2026-11-24
- 状态：正常循环（**识别 API 故障，撤销 12 条错误结论**）

## 1. 异常：12 条补充条目全部「0 候选」

本轮按计划检索 12 条补充类历史/地理条目，结果**全部 0 候选**。这个数字本身就可疑——它们中的赫梯、神圣罗马帝国、汉萨同盟都是文献极丰富的主题。

按 D065「抓取失败 ≠ 数据缺失」，我没有把「0 候选」直接写成「无解」，而是去验证 API：

| 端点 | 结果 |
|---|---|
| `api.openalex.org/works?**search**=…` | **HTTP 429** — `Rate limit exceeded. Insufficient budget… free daily budget shared by everyone on your network's IP address, and that budget is used up ($0 remaining)` |
| `api.openalex.org/works/**{ID}**`（单条） | HTTP 200 ✅ |
| `api.crossref.org/works?query.bibliographic=…` | HTTP 200 ✅ |

**结论：OpenAlex 的 search 端点日配额耗尽**（全网络 IP 共享），而我这轮的检索脚本全靠它，且**把失败静默当成「0 候选」**。

## 2. 撤销与改道

- **撤销 12 条错误记录**：在条目备注中写明「本轮首次检索时 OpenAlex search 返回 429，脚本把失败静默当成 0 候选，该结论无效」；

- **改用 Crossref 路线**：`Crossref query.bibliographic` → 取 DOI → `OpenAlex works/{ID}` 取摘要。这条路线不依赖 search 端点。

验证：用新路线跑 3 条，**3/3 命中**：

| 条目 | 来源 | 被引 |
|---|---|---|
| 神圣罗马帝国 | Associative Political Culture in the Holy Roman Empire (2018) | **39** |
| 赫梯王国 | The Hittite Empire from Textual Evidence (2012) | 21 |
| 汉萨同盟 | The Hanseatic League (2024) | 0（摘要≥800） |

**这直接否证了上一步的「0 候选」**——它们只是一时检索不到。

## 3. 口径

- tools/check.py：ERRORS=0 ALL_PASS（243 条、705 来源；R1–R25）
- tools/check_links.py：BROKEN=0 LINKS_PASS
- 层级：**A 149** / B 80 / C 1 / D 13
- 内容源 ≥2：**183**；1 个：58；0 个：2
- 缺口：G1=1 / G2=3 / G3a=4 / **G3b=46** / G4=243

| 条件 | 状态 |
|---|---|
| 全部 243 条 L2 | **已达成** |
| 判据单一实现 + 经主动审计 | **已达成** |
| R19–R25 七道机器校验 | 已上线，0 违规 |
| 每个条目都有强来源或属 D 级 | 未达成（1 条：隋唐） |
| 每条（非 D 级）都有 ≥2 内容源 | 未达成（50 条） |
| G4 语义对题 | 50/243 已扫描 |

## 4. 这轮值在哪

**如果我不验证 API，就会得出「12 条补充条目全部无解」的结论，并写进 limits.html。**
那会是一个由基础设施故障制造的、看起来很像学术结论的错误。
这也是同一个错误的第三次变形：第 51 轮「只查一个库」、第 53 轮「变音被正则漏杀」、本轮「配额耗尽静默变 0 候选」——**共同点是「检索失败」被当成了「检索结果」**。
