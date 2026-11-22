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
