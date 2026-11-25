# 地理与文明百科

一个**数据驱动、机器校验、诚实标注**的静态知识库：按「大洲 × 文明/区域 × 主题」组织 **243 个条目**，每条都配有可核对的来源、证据等级标注与反查链接。

- 纯静态 HTML + CSS，**零 JavaScript**
- 渲染后站点：`site/`（入口 `site/index.html`）
- 数据层：`data/*.json`（单元、来源库、覆盖状态、证据等级、侧面证据、语义扫描）

---

## 当前状态（第 151 轮，维护模式）

| 指标 | 值 |
|---|---|
| 条目总数 | **243**，全部 L2 |
| 证据等级 | **A 215 / B 0 / C 0 / D 28** |
| 缺口 | **G1=0 / G2=0 / G3=0 / G4=0** |
| 语义对题扫描 | **243 / 243** 逐条完成 |
| 来源 | 登记 809、被引用 669（未引用 140 为抓取失败/未采用候选，留作凭证） |
| 质量闸 | `check.py` 0 错误 · `check_links.py` 0 断链 · `sum 自检` 一致 |
| 判定 | 第 149–151 连续三轮独立审计五类缺口全为 0 → **维护模式**（`saturated=true`） |

### 按层级
| 层级 | A | D |
|---|---|---|
| 核心 | 44 | 0 |
| 重要 | 104 | 0 |
| 补充 | 67 | 28 |

**所有「核心」「重要」条目均为 A 级（每条 ≥2 篇独立、对题的学术文献互证）。** 28 条 D 级全部是「补充」类的**指标解读型条目**（人口、城市化率、区域发展数据等），按规则（D141）以「机构长文 + 官方数据端点」为依据，不要求第二篇学术论文。

---

## 证据分级口径（`tools/assess.py`，唯一实现）

| 级别 | 含义 |
|---|---|
| **A** | ≥2 个**独立**的内容来源（同一域名多页只算 1 个） |
| **B** | 1 个内容来源 |
| **C** | 无强来源 |
| **D** | 指标解读类：1 篇机构长文（非 openalex 论文）+ 数据端点，或 `today` 自述指标数值 |

- **强来源**：被引 ≥10 **或** 正文/摘要 ≥800 字符（满足其一）；
- 别名页、机构首页、书评、空壳页（抓取正文过短的页面）、数据端点一律**不计**为内容来源；
- 同一域名下多个页面最多计 1 个内容来源（互证须来自不同出版者）；
- 「旁证」标记（在条目 `pending_notes` 内）一旦出现即降级、且不可逆。

## 缺口定义（`reports/round62_gaps.json`）

| 编号 | 含义 |
|---|---|
| G1 | 无强来源（仅 C 级；D 级指标解读类不计） |
| G2 | 检索确认无合格主来源（名单见 `data/no_solution.json`，当前为空） |
| G3 | 内容源仅 1 个、需第二互证（排除 D 级） |
| G4 | 未经人工逐条语义扫描（当前 0，已扫 243/243） |

---

## 目录结构

```
data/            数据层
  {unit}.json      8 个大洲/主题单元的条目
  sources.json     来源库（{"sources":[...]}）
  coverage.json    覆盖与轮次状态
  evidence_level.json  每条的证据等级记录
  object_words.json    条目→对象词（别名）映射，供 R20 校验
  object_equiv.json    R20 摘要通道的等价词（人工认定）
  side_evidence.json   侧面/剔除来源登记
  semantic_scan.json   语义扫描存档（scanned_entries / unresolved）
  no_solution.json     G2 名单（经检索确认无合格主来源）
tools/           校验器与生成器
  assess.py        证据判据唯一实现（A/B/C/D、内容源计数）
  check.py         机器闸 R1–R25
  check_links.py   内部链接检查
  gen_site.py      渲染静态站
  selfcheck_aggregates.py  汇总字段互相对齐自检
  round*_*.py      各轮补源/审计脚本（保留可复现）
site/            渲染后的静态站点（零 JS）
reports/         各轮检索与审计报告（JSON，可追溯）
DECISIONS.md     无人值守决策记录（D001–D155+）
PROGRESS.md      逐轮进度台账
REPORT.md        最近一轮统计摘要
SATURATION.json  饱和/维护模式状态与缺口模型
```

---

## 运行

```bash
# 机器闸（R1–R25）
python -X utf8 tools/check.py
# 链接检查
python -X utf8 tools/check_links.py
# 汇总字段一致性
python -X utf8 tools/selfcheck_aggregates.py
# 重新渲染站点
python -X utf8 tools/gen_site.py
```

本地预览（任选其一）：

```bash
# 方式一：直接打开
#   浏览器打开 site/index.html
# 方式二：起一个静态服务器（推荐，避免 file:// 相对路径问题）
python -m http.server 8000 --directory site
#   然后访问 http://127.0.0.1:8000/
```

---

## 机器闸（`check.py`）做了什么

R1–R25 覆盖：字段完整性、ID 合法性、来源合法性与 verified 标记、SVG 仅内联且带「示意图，非精确测绘」、无 Markdown 残留、悬空引用、弱来源不得称主来源、对象词匹配（R20）、层级记录与重算一致（R22）、空壳页不作内容源（R23）、落点句存在（R24）、书评不作学术来源（R25）等。

## 设计原则

- **不编造**：数字、日期、人名、引文、出处一律不虚构；拿不到摘要就不据此写断言。
- **只用可核验来源**：`sources.json` 中 `verified=true` 的接口/文献。
- **争议并列**：有分歧的表述并列呈现，不单方面下结论；示意图不画争议边界。
- **诚实标注**：每条标注证据等级，并在「限制」页公开缺口与已知问题。
- **可复现**：每轮检索/审计报告落在 `reports/`，检索路线、HTTP 状态、被拒候选均留痕。

## 已知边界（诚实披露）

- **28 条 D 级是指标解读类**，依赖机构长文与官方数据端点，不是学术综述；如需学术文献支撑属另一套标准。
- **未引用来源 140 条**多为此前抓取失败（404/空壳页）或未采用的候选，保留为「哪些 URL 查不到」的可复现凭证，不删除。
- **G4 语义对题**由人工/子代理逐条阅读摘要完成，非自动判定；机器只保证结构与记录一致。

详见 `DECISIONS.md`（决策与教训）、`PROGRESS.md`（逐轮台账）、`REPORT.md`（本轮统计）、站点「限制」页。

---

## 在线访问 / GitHub Pages 部署

站点通过 GitHub Actions 自动部署到 **GitHub Pages**：

- 工作流：`.github/workflows/pages.yml`（push 到 `main` 触发；也可手动 Run workflow）
- 发布内容：`site/` 目录
- 预期地址：**https://tiandihuang.github.io/dili/**
- 兜底：仓库同时保留 `gh-pages` 分支（内容同为 `site/`）。若在 Settings → Pages 选择 “Deploy from a branch” → `gh-pages` / `/ (root)`，也会从该分支发布。

> 说明：Actions 方式用 `actions/configure-pages` 的 `enablement: true` 自动启用 Pages，无需手动在设置里点开关。首次部署后若 404，通常需等待 1–2 分钟生效。
