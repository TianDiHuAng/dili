# REPORT.md — 第 72 轮摘要

- 日期：2026-11-24
- 状态：正常循环（**判据单一实现完成**）

## 1. D138 落地：建立 `tools/assess.py`

上一轮发现 `hb()`（内容源统计）与层级判定是两套标准，导致数字虚报。本轮把它们抽成**唯一实现**：

```
tools/assess.py
  ALIAS_PAGES / DATA_PREFIX / BAD_TYPES      常量集中
  has_content(sid, src, entry)               内容源判定
  strength(sid, src, entry)                  层级判定（strong/weak/side/data/alias）
  content_count(entry, sources)               条目内容源数
  level_of(entry, sources)                    A/B/C/D
```

**`check.py`（R22）、`round62_gaps.py`、`round68_levels.py` 全部改为引用它**——此前三处各写一份，任何一处改动都会造成不一致。

切换过程中 R22 立刻报出 3 条不一致（印度河文明、水资源管理、水资源供给概览），证明三处确实在算不同的东西；统一后 **0 错误**。

## 2. 统一后的权威数字

| 指标 | 数值 |
|---|---|
| 层级 A / B / C / D | **114 / 125 / 2 / 2** |
| 内容源 ≥2 | **149** |
| 内容源 1 个 | **93** |
| 内容源 0 个 | **1** |
| G1 无强来源 | **4** |
| G3 仅 1 内容源 | **93** |

G1 明细：阿卡德帝国、隋唐、澳大利亚大陆、水资源管理。

## 3. 口径

- tools/check.py：ERRORS=0 ALL_PASS（243 条、665 来源；R1–R25）
- tools/check_links.py：BROKEN=0 LINKS_PASS
- 侧面文献：side 34 / dropped 37 / weak 12
- 来源 665（已核验 586）；待核实 241

| 条件 | 状态 |
|---|---|
| 全部 243 条 L2 | **已达成** |
| R19–R25 七道机器校验 | 已上线，0 违规 |
| **判据单一实现（D138）** | **已达成** |
| 每个条目都有强来源（G1=0） | 未达成（4 条） |
| 每条都有 ≥2 内容源 | 未达成（94 条不足） |
| G4 语义对题 | 30/243 已扫描 |
