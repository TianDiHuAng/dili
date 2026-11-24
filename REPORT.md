# REPORT.md — 第 80 轮摘要

- 日期：2026-11-24
- 状态：正常循环（**G3：64 → 57**）

## 1. 重要条目第三批 12 条：登记 7 条

| 条目 | 新第二来源 | 被引 | 摘要 |
|---|---|---|---|
| 特奥蒂瓦坎 | Human Sacrifice, Militarism, and Rulership (2005) | **189** | 1,058 |
| 马其顿与亚历山大 | Alexander the Great and His Empire (2010) | **107** | 1,799 |
| 加勒比海群岛 | In the shadow of the plantation: Caribbean… (2002) | 75 | 1,889 |
| 法兰克王国 | Frankish military duty and the fate of Roman… (2008) | 28 | 982 |
| 十三殖民地 | Colonial America: A History to 1763 (2011) | 27 | 4,323 |
| 奥尔梅克 | Discovering the Olmecs (2014) | 15 | 1,641 |
| 莱茵河 | The Rhine: An Eco-Biography, 1815–2000 (2005) | 1 | 4,440 |

## 2. 四条不采用（两条是时段/局部错位）

| 条目 | 候选 | 问题 |
|---|---|---|
| 十字军东征 | Military Orders and **Women of the Nobility** (2023) | 性别侧面 |
| 威尼斯 | Negotiating Transcultural Relations… (2014) | 时段是 **16–17 世纪**，而本条讲威尼斯**鼎盛期 13–15 世纪**（D108 时期错配） |
| 巴西高原 | GIS relief mapping of **central Brazilian highlands** (2020) | 只覆盖一处**喀斯特保护区**（局部） |
| 拉普拉塔平原 | Sustainable intensification of agriculture (2022) | 摘要以泛论开场，无针对潘帕斯的具体结论 |
| 大分水岭 | 本轮 **0 候选** |

## 3. 口径

- tools/check.py：ERRORS=0 ALL_PASS（243 条、698 来源；R1–R25）
- tools/check_links.py：BROKEN=0 LINKS_PASS
- 层级：A 142 / B 87 / C 1 / D 13
- 内容源 ≥2：**176**；1 个：65；0 个：2
- 缺口：G1=1 / G2=3 / G3a=4 / **G3b=53** / G4=243

| 条件 | 状态 |
|---|---|
| 全部 243 条 L2 | **已达成** |
| 判据单一实现 + 经主动审计（D138/D143） | **已达成** |
| R19–R25 七道机器校验 | 已上线，0 违规 |
| 每个条目都有强来源或属 D 级 | 未达成（1 条：隋唐） |
| 每条（非 D 级）都有 ≥2 内容源 | 未达成（57 条） |
| G4 语义对题 | 50/243 已扫描 |
