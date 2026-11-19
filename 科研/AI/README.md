# AI 研发与模型工具箱

面向日常科研编程、前后端工程开发与大模型能力监控精选的实用 AI 工具集合。

---

## 收录工具一览

| 工具名称 | 分类标签 | 访问地址 | 核心价值 |
| --- | --- | --- | --- |
| **Orca** | Vibe Coding · 智能体编排 | [https://github.com/stablyai/orca](https://github.com/stablyai/orca) | 复用个人现有订阅并行运行和管理多个编码智能体（Claude Code、Codex 等） |
| **ModelTrace** | 模型评测 · 降智检测 | [https://xqy2006.github.io/ModelTrace/](https://xqy2006.github.io/ModelTrace/) | 持续监测主流大模型推理表现波动，直观判断当前时段模型是否出现“降智” |
| **Mirasim** | 协作空间 · 接口中转 | [https://mirasim.ai/](https://mirasim.ai/) | 支持多人与多智能体在同一空间协同开发，并提供稳定的模型中转接入 |

---

## 分项介绍与适用场景

### 1. 好用的 Vibe Coding：[Orca](https://github.com/stablyai/orca)
- **功能特点**：支持桌面端、移动端与远程运行时（Remote Runtime），可将 Claude Code、Codex 等主流 AI 编程助手统一接入同一界面并行调度。
- **推荐使用场景**：同时推进多个实验分支、前后端同步开发、跨会话接力长耗时重构任务。

### 2. 测试 AI 是否降智：[ModelTrace](https://xqy2006.github.io/ModelTrace/)
- **功能特点**：通过周期性基准探针追踪各厂商模型的真实响应与逻辑推理稳定性。
- **推荐使用场景**：当发现复杂代码调试或数学推导表现突然下滑时，快速验证是提示词问题还是上游模型波动。

### 3. 一般好用的协作与中转：[Mirasim](https://mirasim.ai/)
- **功能特点**：提供高吞吐的多人 AI 协作空间与统一中转通道，方便团队共同引导编码 Agent 完成项目。
- **推荐使用场景**：课题组联合开发、主力官方客户端受限时的备用接入方案。
