# 条目任务书（供后续批次使用）

## 目标
按 `scope.md` 指定条目，把 L1 骨架升级到 L2 或 L3。先核心、后重要、后补充。每轮最多 40 条，L1 未全部完成前不深写个别条目。

## 数据位置
- 单元文件：`data/<unit_id>.json`，每单元一个 `entries` 数组。
- 来源白名单：`data/sources.json`，只能引用其中 `verified=true` 的 id。
- 状态记录：`data/coverage.json`，每条含 id/level/tier/status/source_count/pending_count/last_update。
- 三份大纲取并集依据：UN M49、Britannica Regions、Wikipedia Regions of the world（见 DECISIONS.md D003）。

## L1（骨架，每条必须）
`id,title,tier,unit_id,region,theme,level,status,definition,time_or_place,overview,related,sources,needs_verification,pending_notes`

## L2 固定结构（七节）
1. `geo`：地形、气候、水系、资源
2. `influence`：地理条件如何影响定居、农业、贸易、政治；区分学界公认与假说，避免地理决定论
3. `polities`：主要文明或政权更替
4. `connections`：与相邻区域的联系
5. `today`：人口/语言等现状；每个数字标注年份与来源；查不到写待补充
6. `svg`：内联简笔示意地图，viewBox 必填，元素不出界，文字用 CSS 变量色，图下注明「示意图，非精确测绘」
7. `pending_notes`：待核实清单

## 硬性规则
- 不编造数字、日期、人名、引文、出处；查不到标待核实。
- 关键事实至少两个独立 `verified=true` 来源，否则 `needs_verification=true` 且 `pending_notes` 非空。
- 争议并列各方说法，不替读者下结论；争议边界不画线。
- id 仅 `a-z0-9-`；字符串内用中文引号，避免 ASCII 引号破坏 JSON。
- SVG 自闭合标签写 `'/>`；禁止脚本；元素白名单见 `tools/check.py`。

## 校验循环
`python -X utf8 tools/check.py` → 修错 → `python -X utf8 tools/gen_site.py` → `python -X utf8 tools/check_links.py` → 抽查页面 → 更新 PROGRESS.md。
