# Python 极速包与项目管理教程（`uv`）

面向科研实验与 Python 工程整理的 **[`uv`](https://docs.astral.sh/uv/)** 入门指南与高频命令速查。`uv` 是由 Astral 团队用 Rust 打造的新一代一体化 Python 包与项目管理器。

- **完整学习笔记（推荐阅读）**：[UV 学习记录 - HMT](https://blog.homura.work/posts/uv-learning/)
- **官方文档**：[https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

---

## 核心亮点

- **极致速度**：依赖解析与包安装速度较传统 `pip` 提升 10–100 倍，配置深度学习大环境不再漫长等待。
- **全能替代**：单一轻量命令行工具统一接管 `pip`、`virtualenv`/`venv`、`pip-tools`、`poetry`、`pipx` 与 `pyenv`（支持自动按需下载指定版本 Python）。
- **实验严格可复现**：基于标准 `pyproject.toml` 与跨平台锁文件 `uv.lock`，确保本地调试代码迁移到服务器后环境零偏差。

---

## 快速安装

```bash
# Linux / macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```powershell
# Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## 高频命令速查表

| 常见任务 | 命令写法 | 说明 |
| --- | --- | --- |
| **新建指定版本项目** | `uv init --python 3.11 exp-proj` | 自动生成标准项目目录、`pyproject.toml` 与 `.python-version` |
| **创建虚拟环境** | `uv venv --python 3.11` | 在当前项目下秒级生成 `.venv` 虚拟环境 |
| **安装并记录依赖** | `uv add torch torchvision matplotlib` | 安装包并自动更新 `pyproject.toml` 与 `uv.lock` |
| **一键同步实验环境** | `uv sync` | 在新机器拉取仓库后，按锁文件精确还原所有依赖 |
| **免激活运行脚本** | `uv run python main.py` | 自动使用项目虚拟环境运行程序，免去手动 `activate` |
| **兼容传统 `pip` 用法** | `uv pip install -r requirements.txt` | 在旧项目中无缝享受 Rust 级并行下载与缓存加速 |

> 进阶配置（如国内镜像源加速、PyTorch CUDA 独立索引源绑定、依赖导出与版本切换）详见 [UV 学习记录全文](https://blog.homura.work/posts/uv-learning/)。
