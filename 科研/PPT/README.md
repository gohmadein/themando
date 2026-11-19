# 学术幻灯片制作（LaTeX Beamer）

基于 **LaTeX Beamer** 的现代化 16:9 学术演示文稿模板与自动化辅助技能（完整支持中文与英文排版），适用于**课题组组会汇报、论文精读分享、课程讲义与学位答辩**。

---

## 核心功能亮点

- **从论文/提纲规划演讲结构**：围绕核心论点与支撑证据（架构图、三线表、关键公式、消融实验）组织幻灯片节奏。
- **内置 `tealnav` 16:9 宽屏主题**：自带顶部章节进度导航栏、分节配色标题栏、分栏对比布局与代码/结果高亮框；同时兼容高校或学术会议自定义 `.sty` 主题。
- **多引擎自动编译**：脚本自动识别本地可用的编译引擎（`XeLaTeX`、`LuaLaTeX`、`pdfLaTeX` 或 `Tectonic`），中文文稿原生适配 `ctexbeamer`。
- **按页定位错误与溢出**：自动解析 `.log` 日志，将 `Overfull \hbox` / `\vbox` 内容超界警告精确关联到具体幻灯片页码。
- **版面渲染巡检与双屏备注**：支持将 PDF 渲染为页面缩略图检查视觉留白，并可通过 `--notes` 生成带第二屏演讲者备注的辅助版本。

---

## 技能与模板文件清单

完整技能包位于 [`beamer-slides/`](beamer-slides/) 目录下：

| 路径 | 角色定位 | 内容说明 |
| --- | --- | --- |
| [`beamer-slides/SKILL.md`](beamer-slides/SKILL.md) | 技能工作流说明 | 涵盖需求梳理、结构大纲、LaTeX 编写、编译排错与视觉复核全流程规范 |
| [`beamer-slides/assets/template.tex`](beamer-slides/assets/template.tex) | 起步源码模板 | 16:9 标准空白模板（内含中文 `ctexbeamer` 一键切换说明与双屏备注开关） |
| [`beamer-slides/assets/beamerthemetealnav.sty`](beamer-slides/assets/beamerthemetealnav.sty) | 主题样式文件 | 内置青色导航栏学术主题宏包 |
| [`beamer-slides/assets/example.tex`](beamer-slides/assets/example.tex) | 完整版式示例源码 | 演示封面、目录、分节页、双栏图文、公式定理框、三线表与致谢页写法 |
| [`beamer-slides/assets/example.pdf`](beamer-slides/assets/example.pdf) | 示例成品 PDF | 编译生成的完整效果预览，直观查看所有内置版式 |
| [`beamer-slides/scripts/slides.py`](beamer-slides/scripts/slides.py) | 自动化构建脚本 | 封装编译、备注页生成、溢出警告页码映射与页面缩略图导出 |
| [`beamer-slides/references/design.md`](beamer-slides/references/design.md) | 视觉设计准则 | 学术幻灯片字号梯度、信息密度控制与图表排版建议 |
| [`beamer-slides/references/beamer.md`](beamer-slides/references/beamer.md) | Beamer 语法速查 | 常用环境、宏包搭配与常见编译报错排查参考 |
| [`beamer-slides/agents/openai.yaml`](beamer-slides/agents/openai.yaml) | AI 技能配置 | 供支持 Skill 协议的 AI 编码助手识别与调用的元数据配置 |

---

## 快速使用指南

1. **环境准备**：安装 TeX Live、MiKTeX 或 Tectonic（制作中文幻灯片需确保包含 `ctex` 宏包，推荐使用 `XeLaTeX` 编译）。
2. **手工新建文稿**：将 [`template.tex`](beamer-slides/assets/template.tex) 与 [`beamerthemetealnav.sty`](beamer-slides/assets/beamerthemetealnav.sty) 复制到你的工作目录；若使用中文，将首行改为 `\documentclass[aspectratio=169,11pt,fontset=fandol]{ctexbeamer}`。
3. **配合 AI 智能体自动生成**：将 `beamer-slides/` 目录放入项目的 `.agents/skills/` 或 `.claude/skills/` 下，即可直接上传论文 PDF 让 AI 自动完成幻灯片编写、编译与版面检查。
