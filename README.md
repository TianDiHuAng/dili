# 地理与文明百科

静态知识库项目，按「大洲 × 文明/区域 × 主题」组织条目。

## 目录
- `scope.md` — 入选清单（三份权威大纲取并集）
- `DECISIONS.md` — 无人值守决策记录
- `PROGRESS.md` — 当前进度与下一轮起点
- `REPORT.md` — 最终统计与空白格子
- `data/` — JSON 数据层（单元、来源、覆盖状态）
- `tools/` — 校验器、生成器、来源核验、链接检查
- `site/` — 渲染后的纯静态站点（零 JavaScript），首页 `site/index.html`
- `reports/` — 来源核验日志、覆盖矩阵

## 运行
```bash
python -X utf8 tools/check.py
python -X utf8 tools/gen_site.py
python -X utf8 tools/check_links.py
python -X utf8 tools/write_report.py
```
浏览器打开 `site/index.html`。

## 设计原则
数据驱动、机器校验、诚实标注、逐层丰富。详见 `WORKFLOW.md` 原文档与 `DECISIONS.md`。
