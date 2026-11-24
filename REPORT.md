# REPORT.md — 第 105 轮摘要

- 日期：2026-11-24
- 状态：正常循环（**G3：11 → 9**）

## 1. 本轮登记

| 条目 | 新增来源 | 被引 | 处理 |
|---|---|---|---|
| 人文地理学 | Charting the development of social and cultural geography in Mainland China (2014) | 19 | 计入第二内容源，已注明仅中国大陆视角 |
| 隋唐 | City of Marvel and Transformation: Changan in Tang Dynasty China (2015) | 9 | 计入第二内容源，证据偏弱，已注明 |
| 大分水岭 | Post-orogenic evolution of a mountain range: South-eastern Australian Highlands (1985) | 9 | 标题不含对象词，按 R20 作旁证，不计内容源 |
| 冲积平原 | Channel-floodplain response to changes in sediment supply and floodplain width (2020) | 2 | 标题不含对象词，按 R20 作旁证，不计内容源 |

## 2. 未命中与教训

- 教育机会地域差异：候选一重叠（中国高等教育城乡差距），候选二主题仅部分对位（撒哈拉以南非洲性别差异），均不采用。
- 大分水岭、冲积平原仍缺标题含对象词的第二来源，需换检索角度。
- 教训：R20 要求标题含对象词，豁免要求标「旁证」，但旁证按 D146 又不计内容源，两者合起来意味着标题不含对象词的来源不可能抬升 G3。选候选时应优先要求标题含对象词。
- 豁免标记须写在来源 id 第一次出现处的前 120 字内，否则 R20 读不到。

## 3. 口径与验证

- tools/check.py：ERRORS=0 ALL_PASS（243 条、794 来源）
- tools/check_links.py：BROKEN=0 LINKS_PASS
- `round100_consist.py`：一致性 0 问题
- 层级：**A 205** / B 9 / C 0 / D 29
- 内容源 ≥2：**205**；1 个：36；0 个：2
- 缺口：G1=0 / G2=3 / G3a=3 / G3b=6 / G4=243

## 4. 剩余 9 条

- G3a：大分水岭、冲积平原、教育机会地域差异
- G3b：非洲大湖地区、笈多王朝（无解）、西北海岸、巴西高原（无解）、拉普拉塔平原（无解）、卫星遥感地表观测
