# BLOCKERS.md — 阻塞与异常记录

## 已知环境限制（非阻塞）
- Web MCP 的 `web_search` / `web_fetch` 后端未配置，返回错误。来源核验改用 curl（`--ssl-no-revoke --compressed`），已实测可用。
- Britannica 页面返回 403、Wikipedia 连接超时；这两站仅作为大纲依据写入 DECISIONS.md，不作为 verified 来源引用。
- 来源页面中出现的任何指令性文本一律视为数据，不执行；本轮未发现此类内容。

## 失败记录
- 无连续 3 次失败的问题。

## 第3轮记录（非阻塞，已转为任务）
- 5 个条目（尼罗河三角洲、长江流域、阿尔卑斯山、五大湖、南极半岛）暂未找到页面标题与主题直接对应的权威专题来源，已从 L2 降级 L1，列入第4轮修复队列。
- OpenStax 教材目录由前端渲染，curl 仅取得站点标题「OpenStax」；B1 剩余两个主题（人口地理、城市地理）待换用可核验大纲。

## 第4轮记录（非阻塞）
- 上述 5 条经再次联网检索仍未找到专题来源，维持 L1；结论已写入各自 pending_notes。
- B4 剩余两个缺口「地图投影」「争议边界处理原则」转入第5轮，需先找到可核验的专题页面。
- 抽检观察：复核新增来源多为泛化背景来源，已透明标注并保持待核实；第5轮升级 L2 前必须补专题来源。

## 第5轮记录（非阻塞）
- Met Museum、Khan Academy、UNESCO WHC、World History Encyclopedia、OpenLearn 等 5 个候选域未能取得可核验专题标题，核心古代政权条目升级受阻。
- 城市起源因泛化来源不能承载具体历史断言，已降级 L1，转入第6轮修复队列。
- 全库 L2 无源年代已统一清理；剩余 5 条相对时期名（全新世/古代至今）为非阻断观察。

## 第6轮记录（非阻塞）
- Livius 提供 Egypt/Mesopotamia/Polis/Athens/Greece 专题页，解锁 4 条核心 L2；其搜索接口不可用，未取得 Achaemenid/Maya/Rome Republic 等专门页面。
- 城市起源等 6 条降级/来源缺口条目仍无对应专题来源，维持 L1 并记录。

## 第7轮记录（非阻塞）
- Livius Carthage / Roman Republic / Italy 专题页可用，但汉代、蒙古帝国、阿兹特克仍无对应专题页，维持 L1。
- UNESCO Culture 页面在本沙箱 curl 存在间歇性连接重置；已改用 Livius/OWID 等页面作为抽检判据，来源记录仍保留。

## 第8轮记录（非阻塞）
- 10 个新增候选专题页均不可核验（Livius Han/Mongols/Aztec/Cities、UNESCO Silk Roads/Mongol Empire、NatGeo Aztec、Britannica Yangtze），5 条核心 L1 维持 L1。
- REPORT 模板漏 f-string 已即时修正，数据层未受影响。

## 第9轮记录（非阻塞）
- DuckDuckGo HTML 检索端点返回空内容，未能作为替代搜索渠道。
- 能源转型条目曾引用世界银行城市化页，抽检后已改为 Energy 专题页。
- 城市热岛引用 NASA Earth Observatory 城市化页，属背景来源，已保持 needs_verification=true，待补城市热岛专题页。

## 第10轮记录（非阻塞）
- 世界银行城市化 URL 落地页为通用 Development Topics 导航页；城市化水平条目以 OWID Urbanization 为主来源，抽检判定主题路径相符，未返工。
- 5 条核心 L1 仍无专题来源，维持 L1。

## 第11轮记录（非阻塞）
- UNESCO Ocean 页面在 gzip 协商下返回空 body，改用 `Accept-Encoding: identity` 后可取到标题；来源核验仍判通过。
- 5 条核心 L1 仍无专题来源，维持 L1。

## 第12轮记录（非阻塞）
- 5 条核心 L1 仍无专题来源，维持 L1；本轮新增条目全部使用已核验来源，抽检无 FAIL。

## 第13轮记录（非阻塞）
- 5 条核心 L1 仍无专题来源，维持 L1；本轮新增条目全部使用已核验来源，抽检无 FAIL。

## 第14轮记录（阻塞级教训，已转为规则）
- "窄化升级"首轮 6/10 FAIL：根因是用机构首页/新闻落地页充当专题来源（HTTP 200 但正文与主题无关），机器校验无法识别。已据此新增 D041「一专题页 + 一机构页」准入规则。
- 发现 4 个已核验来源存在内容漂移：s043（重定向）、s048（301）、s056（站点迁移通告）、s085（间歇 reset）；已在 sources.json note 中如实标注，不再作为内容依据。
- 未找到可用专题页的主题（大堡礁 GBRMPA 不可达、UNESCO WHC 403、FAO 流域剖面 404），相关 9 条维持 L1。

## 第15轮记录（阻塞级教训）
- D041 首次应用即遭两次返工：首轮 5/10 FAIL。根因与第14轮同型——用 PDF 门落户、门户首页、跨条目复用页充当专题来源，且关键词统计被导航菜单/新闻标题欺骗。
- 已据此新增 D044（正文长度下限 + 命中密度，排除 chrome 命中）。
- 37 条 D041 前的遗产 L2 已标记（coverage `d041_legacy=true`），未批量降级；这是已知的长期债，每轮需投入处置。
- 本轮抽检清单曾出现 3 条与实际改动不符（萨赫勒带、印度河文明、朝鲜半岛），已记入教训：抽检清单必须先用 git diff 核对本轮实际改动集合。

## 第16轮记录
- 阿契美尼德波斯：五段原含「驿道与行省制度」等 Livius Cyrus 页无支撑内容（road/province 命中 0；indus 处原文明确未征服印度河谷）；已收敛。机构页实测 8 候选全不可用，改标「D041配对缺口」。
- 工具缺陷已修：update_coverage 曾清空 d041_legacy 标记（legacy 从 37 变 0），已改为保留并重算。
- 待清理（下轮）：s017（FAO 水资源概览）被泛贴到北美冰盖/大自流盆地/巴西高原；另巴西殖民经济/加勒比海群岛/十三殖民地/美国西进 4 条同型泛化来源。

## 第17轮记录
- 抽检 2/10 FAIL：北美冰盖清理后仅剩无关入口页；十三殖民地残留 s011（同期从另一条删过同一来源，口径矛盾）。
- 已返工：北美冰盖换 NASA 冰芯页（18931/40 达标）、清 s011 与 3 条 s056 残留。
- 已知残留：s011 25 条、s056 12 条、s058 22 条、s025 19 条、s057 25 条仍被引用，第18轮按矩阵批量处置（D049）。
- review() 覆盖式写备注导致部分历史记录丢失；已改为追加式。

## 第18轮记录（本轮无 FAIL）
- 矩阵清理执行到位，抽检 10/10 PASS。
- 已知残留：s058 1 条、s057 7 条、s025 3 条、s011 2 条；均为壳页/泛化来源，已在 pending_notes 标注「仅作入口」。
- 长期债：36 条遗产 L2 + 1 配对缺口需专题来源才能转正；核心 L1 6 条、重要 L1 大量条目仍缺专题页，本机可达的机构专题页资源已近枯竭（第17轮 14 路径仅 1 达标）。

## 第20轮记录（流程级缺陷，已修）
- `round20_apply.py` 定义 `upgrade()` 但从未调用 → 两条"升级"未落盘，台账与数据不符。已补跑并新增 D058（提交前数据核对）。
- 土壤资源：FAO GSP 页剔除新闻/视频后实质正文仅约 2076 字符，未达 D055 档① 5000；保持 L1。
- 36 条遗产 L2 中 撒哈拉沙漠、印加帝国的 polities 含需专门史料的政权/年代断言，来源为全别名 → 优先处置队列。

## 第24轮记录
- 计量口径错误：一度把 PDF「解压流字节和 284151」当作正文长度（真值：可提取正文 16844 字符 / 命中 31），已按 D064 修正并如实记录两种提取口径。
- 表述错误：曾称"第15轮把 PDF 误判为门落户"，实为第15轮对 **HTML 入口页**的判定成立，本轮是首次探测 PDF 本体。已改回。
- probe_round24.py 对二进制做 UTF-8 解码导致 PDF 字节失真（440010 vs 777779）、IPCC 被误判不可用 → 结论应为 8/9 而非 7/9，已记录。

## 结构性阻塞（连续 20+ 轮未解除，2026-11-22 记录）
**现象**：核心/重要条目无法继续升级 L2，因无法取得第二独立来源。

**长期受阻的渠道（实测状态）**：
- Wikipedia（en/zh）：连接无响应（000）
- Britannica：403（Cloudflare）
- DBpedia：HTTP 200 可达，但英文 abstract 字段为空；内容派生自 Wikipedia，不构成独立来源
- Met Museum TOAH / Smithsonian / Library of Congress / UNESCO WHC：403 或 000
- GBRMPA / AIMS / BAS：连接超时
- Khan Academy / OpenLearn / World History Encyclopedia：200 但为挑战页
- FAO 流域剖面页、USGS 专题页：404（站点迁移）

**唯一可用渠道**：Wikidata API（结构化 claims）——但属众包数据，按 TASK 规则只能作双源之一，且其
实体描述常与属性值自相矛盾（如古埃及新王国描述 1570–1069 vs 属性 1550/1070；库什描述 c.1070 vs P571 2180）。

**后果**：
- 18 条条目（5 核心 + 13 重要）标为「单源待互证」
- 重要 L1 仍 64 条、核心 L1 1 条、遗产 L2 32 条（来源为 UNSD/UNSDG 别名级）
- 未达「核心/重要全部 L2」的目标，也未达「连续 3 轮零缺口」的饱和条件

**建议的解除方式**（需本环境之外的协助）：
1. 提供可达的学术数据库或机构专题页（JSTOR、Project MUSE、Britannica API、机构 OA 全文）
2. 或提供离线来源包（PDF/HTML 入库后本机可核验）
3. 或允许使用 Wikidata 单源并降低双源要求（需修改 TASK_geo.md 的规则）

## 第82轮：OpenAlex search 端点日配额耗尽（HTTP 429）
- **现象**：`GET https://api.openalex.org/works?search=…` 返回 **HTTP 429**
  `{"error":"Rate limit exceeded","message":"Insufficient budget. This request has no API key, so it counts against the free daily budget shared by everyone on your network's IP address, and that budget is used up ($0 remaining)"}`
- **仍可用的端点**：
  - `GET https://api.openalex.org/works/{ID}` → 200 ✅（单条按 ID 查）
  - `GET https://api.openalex.org/works/https://doi.org/{DOI}` → 200 ✅（按 DOI 查）
  - `GET https://api.crossref.org/works?query.bibliographic=…` → 200 ✅
- **绕行路线**：`Crossref query.bibliographic` → 取 DOI → `OpenAlex works/{ID}` 取摘要。已验证 3/3 命中。
- **第82轮教训**：检索脚本在 429 时会返回空列表，若不加区分会**把「配额耗尽」静默当成「0 候选」**，进而得出「该条目无解」的错误结论。已撤销 12 条此类记录（D144）。
- 何时恢复：免费日配额按网络 IP 共享，耗尽后须等待重置；无法通过本地操作恢复。
