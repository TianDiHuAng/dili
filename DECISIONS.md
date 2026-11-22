# DECISIONS.md — 决策记录

> 无人值守模式：不确定时选保守方案，记录决定与理由。每次变更追加，不覆盖历史。

## D001 — 样式标杆缺失
- 决定：项目文件夹为空，无样板页。自行设计一套统一风格，见 `site/css/style.css`。
- 风格：纸张/地图色调（浅色 #f5f0e6 底、墨色 #1f2b2a 字、青绿 #2b7a78 强调、赭石 #b5651d 次强调），深色模式用 CSS `prefers-color-scheme: dark` 自动切换（深墨底 #121918、浅字 #e8e2d5）。
- 理由：任务要求"如果没有样板页，就自行设计一套简洁统一的风格，并在 DECISIONS.md 记录"。地图/地理主题适合纸本地图配色；纯 CSS 变量保证 SVG 与正文双模式可读。

## D002 — 单元划分
- 决定：按大洲划分 7 个单元（非洲、亚洲、欧洲、北美洲、南美洲、大洋洲、南极洲），另设「全球主题」跨洲单元；每个单元内按"文明/区域 × 主题"组织条目。
- 理由：任务书指定"大洲×文明或区域×主题"；大洲是权威大纲（UN M49、Britannica、Wikipedia 区域列表）的共同最大公约数，便于取并集。

## D003 — "全"的口径与来源
- 决定：对照三份权威大纲取并集：
  1. UN M49 标准地理分区（联合国统计司）https://unstats.un.org/unsd/methodology/m49/
  2. Encyclopaedia Britannica — Continents & Regions 分类树 https://www.britannica.com/place/continent
  3. Wikipedia — List of regions of the world https://en.wikipedia.org/wiki/List_of_regions_of_the_world
  - 补充参考：AP Human Geography Course and Exam Description（主题框架）。
- 理由：任务要求至少 3 份权威大纲/目录取并集。三份均为公开可访问的分类体系；网络检索通过 curl 核验可达性（见 sources.json）。

## D004 — 来源核验口径
- 决定：
  - `verified=true`：用 curl 实际打开页面，记录 HTTP 200 且从 `<title>` 核到标题/机构名；作者/年份缺失时写 null 并在 note 说明，不编造。
  - `link_ok` 三态：true=HTTP<400；"blocked"=401/403/429/503；false=404/DNS 失败/超时。
  - 无法打开或标题不符的来源标 `verified=false`，内容引用它必须 `needs_verification=true`。
- 理由：任务要求"打开页面核对标题、作者、年份后才能 verified=true"与"不编造数字、日期、人名、引文、出处"。

## D005 — 条目层级与配额
- 决定：
  - L1：全部条目的骨架（定义、时间/位置、一两句概述、相关条目）。
  - L2：固定七节结构，核心条目优先；本项目先完成 2 个样板条目到 L2（尼罗河谷农业、黄河流域定居），通过 check.py 后再批量升级。
  - L3：仅在核心条目且资料充分时做争议/数据/复杂图示；本轮不铺开。
  - 每轮最多 40 个条目；本项目当前轮为第 1 轮（骨架轮），处理 40 个 L1 条目，剩余在 PROGRESS.md 记录下一轮起点。
- 理由：任务硬性要求"每轮最多处理40个条目"且"L1 未全部完成前不得深写个别条目"；2 个 L2 样板属阶段 3 例外（先做 2 个到 L2 通过检查后再继续）。

## D006 — 争议边界与现状数据
- 决定：争议边界只描述各方立场，不画争议线；SVG 仅示意轮廓与城市点。人口/面积等数字标注年份和来源，缺失写"待补充"，不估算。
- 理由：任务专用规则。

## D007 — 生成器与数据分离
- 决定：采用 WORKFLOW.md 架构：JSON 数据层 → tools/check.py 机器校验 → tools/gen_site.py 渲染 → site/ 纯静态 HTML/CSS（零 JS）。数据文件按大洲分目录 `data/<unit>.json`，来源全局 `data/sources.json`，覆盖状态 `data/coverage.json`。
- 理由：工作流核心思想"数据驱动、机器校验、诚实标注、逐层丰富"；便于离线部署与后续增补。

## D008 — 网络工具限制
- 决定：Web MCP 工具（web_search/web_fetch）在本会话后端未配置，改用 curl 直接访问权威站点核验；核验脚本落盘为 `tools/verify_sources.py`，可重复运行。
- 理由：无人值守，不等待用户修复配置；curl 实测可访问 unstats.un.org。

## D009 — 单元 id 规范化
- 决定：单元 id 由下划线改为连字符（`north-america`、`south-america`、`global-themes`）。
- 理由：`tools/check.py` 的 R2 规则要求条目 id 仅含 `a-z0-9-`；单元 id 是条目 id 前缀，下划线会破坏链接与文件名约定。

## D010 — 来源核验实测结果
- 决定：Web MCP 搜索/抓取后端不可用；Britannica 返回 403、Wikipedia 连接超时。改用 curl（`--ssl-no-revoke --compressed`）访问联合国系统、FAO、UNESCO、WHO、NASA、NOAA、USGS、World Bank、Our World in Data、IUCN 等官方/数据机构页面。
- 结果：探测 150 个权威 URL，103 条通过核验（HTTP<400 且 `<title>` 可核对）；全部写入 `data/sources.json`。条目中沿用旧 id 的引用通过来源别名指向已核验页面，别名在 note 中注明。
- 理由：任务要求来源 verified=true 必须打开页面核对；无法核验的来源保留但标 verified=false，且条目保持待核实。

## D011 — 本轮内容与待核实比例
- 决定：169 条全部建立 L1 骨架，其中第 1 轮正式处理 40 条；2 条样板升级 L2；其余 167 条保持 `needs_verification=true` 并写明待核实原因。
- 理由：硬性规则「不编造数字、日期、人名、出处」与「关键事实至少两个独立来源」。在逐条核对前不把骨架写成确定事实；高待核实比例如实反映进度，后续轮次逐条消减。

## D012 — 覆盖空白格子
- 决定：REPORT.md 列出 8 个空白格子，不在本轮硬凑条目。
- 理由：本轮 40 条配额已用满；空白格子列入下一轮起点，符合「每轮最多 40 条」与「L1 未全部完成前不得深写个别条目」。

## D013 — 自动模式执行裁定（Ruling）
- 决定：不建立独立 worktree；按 AUTONOMOUS.md 要求直接在当前仓库 main 分支逐轮提交并推送。以 BACKLOG.md / METRICS.json / SATURATION.json / PROGRESS.md 作为执行 ledger。
- 理由：AUTONOMOUS.md 明确「不修改项目文件夹之外」「每轮结束 git commit」，且用户已要求推送到 GitHub；独立 worktree 会引入额外合并步骤，与逐轮可审计提交冲突。
- 可逆方式：如需隔离，可用 `git worktree add` 从任意轮次提交切出分支；当前历史可完整回溯。
- 成本：若同一轮出现并发写入，需靠顺序执行避免冲突；本轮严格串行批次执行。

## D014 — 第2轮任务配比
- 决定：第2轮 40 任务 = 8 新条目（填 8 个空白格子，低于 169×10% 上限）+ 24 核心条目升级 L2（每个大洲/全球主题各 3 条）+ 8 条复核。
- 理由：AUTONOMOUS.md 要求复核与修复优先、核心优先、稀疏维度优先；均匀分配避免只深写单一洲。
- 成本：重要 L1 仍余 93 条，需后续轮次继续升级。

## D015 — 第2轮抽检失败与返工
- 决定：抽检 5 条中「东亚季风」FAIL（无来源的「约前6000年至今」与「决定」式绝对表述），按 AUTONOMOUS.md 整批返工；实际修正 7 个新条目，移除或软化无源年代与决定论措辞。复核 7/7 PASS。第 3 轮抽检比例提高到 25%。
- 理由：硬性规则「不编造数字、日期」「地理决定论要谨慎」；抽检失败不得只修单条，必须整批处理疑似同类问题。
- 可逆方式：每处修改都有独立提交 `20a9cc5` 与前序提交，可 git revert 单批恢复。
- 成本：多花一轮抽检预算；第3轮需抽检约 10 条而非 5 条。

## D016 — 报告空白格子口径
- 决定：REPORT.md 第 5 节从当前 `coverage.json` 矩阵实时计算，不从轮初缺口快照读取。
- 理由：轮初发现 8 个空白格子，本轮已补平；沿用快照会误报「仍空白 8 格」。
- 成本：需在每批修改后更新 coverage.json（已由 round2_apply.py 完成）。
