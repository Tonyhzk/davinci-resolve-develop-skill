# 更新日志

本项目的所有重要更改都将记录在此文件中。

[English](CHANGELOG.md) | **中文**

---

## [Unreleased]

### 新增

- **resolve_run.py** - 执行入口脚本，自动连接本机 Resolve 并注入常用变量（`resolve`、`project`、`timeline`、`mediapool`）
- **内联代码执行** - AI 现在可以直接执行 Python 代码实时操作 DaVinci Resolve

### 变更

- **API 参考来源** - 从打包文档改为读取本机 Resolve 安装目录的文档，确保 API 与安装版本一致
- **SKILL.md 描述** - 更新描述，新增操作相关触发词（操控、时间线、媒体池、项目管理）

### 移除

- **打包参考文档** - 移除随技能打包的 Developer 文档（约 100+ 文件），改为读取本机 Resolve 安装目录

---

## [1.0.0] - 2026-03-16

### 首次发布

- **脚本生成** - 自动生成 Lua 和 Python 脚本，实现 DaVinci Resolve 自动化操作
- **API 参考** - 内置 Resolve 脚本 API 文档
- **工作流自动化** - 自动化剪辑、调色、渲染和交付等常见任务
- **Fusion 合成** - 通过 AI 创建 Fusion 合成和节点式视觉效果
- **调色辅助** - AI 辅助调色脚本生成和 LUT 管理工具
- **项目模板** - 开箱即用的项目和时间线模板
