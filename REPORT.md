# REPORT.md — 第 81 轮摘要

- 日期：2026-11-24
- 状态：正常循环（**核心 G3b：5 → 1**）

## 1. 4 条核心条目全部找到对位来源

| 条目 | 新第二来源 | 被引 | 摘要 |
|---|---|---|---|
| 东非大裂谷 | Evolution of the East African Rift System from trap- to plate-scale rifting (2022) | **101** | 2,889 |
| 印加帝国 | Imperial Expansion and Local Agency: A Case Study of Labor Organization (2017) | **43** | 1,411 |
| 撒哈拉沙漠 | Late–Mesozoic and Tertiary palaeoenvironments of the Sahara region (2020) | 5 | 1,905 |
| 印度河文明 | Origin and Growth of the Principal Elements of the Harappan Civilization (2025) | 0 | 862 |

**印加终于找到了**——此前三次检索都只命中「马丘比丘遗址」或「玉米酒器物」，这两条都是遗址/器物层面。这次换成「帝国扩张 + 劳役组织」对象词，命中一篇**直接讨论行省经济集约化与地方能动性**的研究，正是本条要的国家层面。

**东非大裂谷**此前命中「死海裂谷」（地名碰撞），这次加了 `great rift` 与 `plume` 等词，找到裂谷系统演化的综述（被引 101）。

## 2. 重要条目 7 条全部 0 候选

萨珊波斯、吠陀时代、明清、马来群岛、河中地区、洋流、气候带——本轮宽检索**均无过筛者**。这些条目前几轮命中的都是侧面（钱币学、女性地位、医学制度、方言、铭文），说明**该主题的英文学术文献确实以侧面研究为主**。

## 3. 一个校验修复

R20 报错：印度河文明的新来源标题用的是 **HARAPPAN**（不是 INDUS），对象词表缺 `harappan`。已补 → 对象词变为 `['indus','harappan','indus valley']`。
这也是 R20 的价值：**它逼我为每个条目想清「这个对象还有哪些别名」**。

## 4. 口径

- tools/check.py：ERRORS=0 ALL_PASS（243 条、702 来源；R1–R25）
- tools/check_links.py：BROKEN=0 LINKS_PASS
- 层级：**A 146** / B 83 / C 1 / D 13
- 内容源 ≥2：**180**；1 个：61；0 个：2
- 缺口：G1=1 / G2=3 / G3a=4 / **G3b=49**（核心仅 1） / G4=243

| 条件 | 状态 |
|---|---|
| 全部 243 条 L2 | **已达成** |
| 判据单一实现 + 经主动审计 | **已达成** |
| R19–R25 七道机器校验 | 已上线，0 违规 |
| 每个条目都有强来源或属 D 级 | 未达成（1 条：隋唐） |
| 每条（非 D 级）都有 ≥2 内容源 | 未达成（53 条，其中核心仅 1 条） |
| G4 语义对题 | 50/243 已扫描 |
