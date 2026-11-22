# PROGRESS.md — 进度（每次启动先读本文件）

- 状态：**ALL_DONE**（本轮搭建完成）
- 当前阶段：阶段5 完成；阶段0–5 全部执行
- 当前轮次：第 1 轮（已用满 40 条配额）
- 下一轮起点：第 2 轮从 core 列表中未标记「L1完成」的条目继续；优先补齐 REPORT.md 列出的 8 个空白格子，再按 核心→重要→补充 升级 L2。

## 已完成
- [x] 阅读 TASK_geo.md 与 WORKFLOW.md
- [x] 建立目录骨架、DECISIONS.md
- [x] 阶段0：scope.md（169 条，三份权威大纲取并集）、data/coverage.json、reports/coverage_matrix.md
- [x] 阶段1：data/sources.json（163 条来源，103 条 curl 实测核验，超过 80 条要求）
- [x] 阶段2：tools/check.py（R1–R13），ERRORS=0
- [x] 阶段3：2 个 L2 样板（尼罗河谷、黄河流域），SVG 通过出界/脚本检查
- [x] 阶段4：169 条全部达到 L1 骨架；第 1 轮处理 40 条
- [x] 阶段5：site/ 184 个 HTML（首页/8 单元/169 条目/索引/时间线/来源/覆盖/覆盖明细/关于），REPORT.md
- [x] tools/check_links.py：3193 条内部链接，BROKEN=0
- [x] 样式：统一 CSS 变量、深色模式、内联 SVG、无图片零 JS

## 验证命令（全部通过）
```
python -X utf8 tools/check.py        # ERRORS=0 ALL_PASS
python -X utf8 tools/gen_site.py     # 生成完成
python -X utf8 tools/check_links.py  # BROKEN=0 LINKS_PASS
python -X utf8 tools/write_report.py # REPORT.md 已生成
```

## 未完成（后续轮次，不属于本次「搭建」范围）
- 167 条仍为 L1 骨架并标待核实；按任务书每轮 40 条继续升级 L2。
- 8 个覆盖矩阵空白格子待补条目。
- 现状数据（人口、面积、边界）未写具体数值，待按年份与权威来源补齐。
