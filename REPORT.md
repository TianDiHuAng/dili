# REPORT.md — 第 93 轮摘要

- 日期：2026-11-24
- 状态：正常循环（**A 级全量复核 europe+42 条；查出同域名多页问题**）

## 1. 复核范围：europe 23 条 + north-america 19 条

逐条读完 42 条 A 级，发现三类问题。

### 问题一：同一网站的多个页面被当成「两个独立来源」（12 条）

| 条目 | 同域来源 |
|---|---|
| **古希腊城邦** | `livius.org` 的 **Polis + Athens + Greece 三页** |
| **罗马共和国** | `livius.org` 的 Roman Republic + Italy 两页 |
| 湄公河三角洲 / 亚马逊河 / 土壤资源 | `fao.org` 的 AQUASTAT + Forestry 两页 |
| 科罗拉多高原 | `nps.gov` 的 Geologic Formations + 公园主页 |
| 板块构造 | `usgs.gov` 的 Understanding plate motions + This Dynamic Earth |
| 肉奶生产与土地 | `ourworldindata.org` 两页 |
| 健康地理数据 | `who.int` 两页 |
| 环境数据访问 | `ncei.noaa.gov` 两页 |
| 亚马逊盆地 / 火灾生态 | `earthobservatory.nasa.gov` 两页 |

**同一出版者的两个页面不能互证**——这与 D135「别名页」同源，只是维度从「同一页被多处引用」变成「同一站的多页」。
（`openalex-` 来源不受影响：它们是不同论文，URL 同为 API 端点只是接口形式。）

### 问题二：层级与内容源判定又不一致（D146 同类，换维度）

加了域名去重后，`content_count` 变了，但 `level_of` 仍在用 `c["strong"]>=2` ——**一个看域名、一个不看**。
结果：古希腊城邦（4 个 strong，其中 3 个同属 livius）仍算 **A 级**，而它的独立内容源只有 2（Livius 计 1 + 海岸地貌 1）。
**这是 D146「两套逻辑」的同一形态换了个维度**（D146 是 side 标记，这次是域名）。

### 问题三：书评的 type 字段标成了「学术文献」

**莱茵河** ←《The Rhine: An Eco-Biography, 1815–2000》**(review)**，DOI 是 `10.1353/tech.2005.0070`（Technology and Culture 期刊的书评），被引仅 1。
OpenAlex 的 `type` 标为「学术文献」，**R25 只看 type 因而漏检**——D136 的再一次实例。

## 2. 修复

| 编号 | 内容 |
|---|---|
| **D150** | `content_count` 按**域名去重**：同一域名下多个页面最多计 1 个内容源（`openalex-`/`wikidata-` 除外） |
| **D151** | `level_of` 的 A 级判定改为 **`strong>=2` 且 `content_count>=2`**，与 D150 同口径 |
| — | 莱茵河标签为旁证 |

## 3. 数字修正

| 指标 | 修正前 | 修正后 |
|---|---|---|
| **A 级** | 171 | **168** |
| **D 级** | 19 | **22** |
| **G3** | 53 | **53** |
| G3a | 34 | **34**（核心6/重要18/补充10） |
| G3b | 19 | **19** |

## 4. 口径

- tools/check.py：ERRORS=0 ALL_PASS（243 条、742 来源；R1–R25）
- tools/check_links.py：BROKEN=0 LINKS_PASS
- 层级：**A 168** / B 53 / C 0 / D 22
- 内容源 ≥2：**168**；1 个：73；0 个：2
- 缺口：G1=0 / G2=3 / G3a=34 / G3b=19 / G4=243

| 条件 | 状态 |
|---|---|
| 全部 243 条 L2 | **已达成** |
| 每个条目都有强来源或属指标解读类（G1=0） | **已达成**（D150/D151 后仍为 0） |
| 判据单一实现 | **已达成（D146 + D150 + D151 三次收敛）** |
| 机器校验 R19–R25 | 已上线，0 违规 |
| **A 级来源真实对位** | **africa/asia/europe/n-america 已复核（94/168）** |
| 每条（非 D 级）都有 ≥2 内容源 | 未达成（53 条） |
| G4 语义对题 | 164/243 已扫描 |
