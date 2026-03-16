# DaVinci Resolve Develop Skill

为 AI 大模型打造的达芬奇开发技能，让 AI 能够直接操作 DaVinci Resolve，并开发脚本、插件和自动化工作流。

[English](README.md) | **中文** | [更新日志](CHANGELOG_CN.md)

---

<div align="center">

![Banner](assets/banner.svg)

</div>

---

## 功能特性

![Features](assets/features_cn.svg)

### 核心功能

- **直接操控 Resolve** - 通过内联 Python 代码直接操作 DaVinci Resolve
- **本机 API 参考** - 读取本机 Resolve 安装目录中的 API 文档，始终与安装版本一致
- **工作流自动化** - 自动化剪辑、调色、渲染和交付等常见任务

### 高级功能

- **Fusion 合成** - 通过 AI 提示创建 Fusion 合成和节点式视觉效果
- **DCTL 色彩效果** - 生成 GPU 加速的色彩变换和效果
- **OpenFX / LUT / Fuse** - 开发插件、查找表和自定义 Fusion 工具
- **工作流集成** - 构建 Electron 或 Python 工作流集成插件

---

## 系统要求

| 组件 | 最低版本 |
|------|---------|
| DaVinci Resolve | 18.0+ |
| Python | 3.6+ |
| 操作系统 | Windows 10+ / macOS 11+ / Linux |

---

## 安装

### 作为 Claude Code Skill 安装

将 Skill 目录复制到 Claude Code 技能目录：

```bash
# 克隆仓库
git clone https://github.com/Tonyhzk/davinci-resolve-develop-skill.git

# 复制到项目中
cp -r davinci-resolve-develop-skill/src/davinci-resolve-develop-skill/ your-project/.claude/skills/
```

---

## 快速开始

安装后，AI 助手可以直接操作 DaVinci Resolve：

- 实时执行 Python 代码控制 Resolve
- 生成时间线、媒体池、渲染的自动化脚本
- 通过文字描述创建 Fusion 合成
- 开发 DCTL 效果、LUT、OpenFX 插件和 Fuse 工具

技能直接读取本机 Resolve 安装目录中的 API 文档，确保与当前安装版本完全一致。

---

## 项目结构

```
src/davinci-resolve-develop-skill/
├── SKILL.md           # Skill 定义和指令
└── scripts/
    └── resolve_run.py # 执行入口（自动连接 Resolve）
```

---

## 工作原理

技能使用 `resolve_run.py` 连接正在运行的 DaVinci Resolve 实例，并在预注入常用变量（`resolve`、`project`、`timeline`、`mediapool` 等）的环境中执行 Python 代码。

API 参考文档直接读取本机 Resolve 安装目录，而非随技能打包，因此始终与安装版本匹配。

---

## 开发指南

### 环境要求

- DaVinci Resolve（免费版或 Studio 版）- 必须处于运行状态
- Python 3.6+
- Claude Code CLI

### 参与贡献

欢迎提交 Pull Request！提交前请确保：

1. 代码通过所有测试
2. 文档已更新
3. 提交信息清晰明了

---

## 致谢

- [DaVinci Resolve](https://www.blackmagicdesign.com/products/davinciresolve) - Blackmagic Design
- [Claude Code](https://claude.com/claude-code) - Anthropic

## 许可证

[Apache License 2.0](LICENSE)

## 作者

**Tonyhzk**

- GitHub: [@Tonyhzk](https://github.com/Tonyhzk)
- 项目地址: [davinci-resolve-develop-skill](https://github.com/Tonyhzk/davinci-resolve-develop-skill)

---

<div align="center">

如果这个项目对你有帮助，欢迎给个 Star！

</div>
