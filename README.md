# DaVinci Resolve Develop Skill

An AI-powered skill that enables large language models to develop scripts, plugins, and automated workflows for DaVinci Resolve.

**English** | [中文](README_CN.md) | [Changelog](CHANGELOG.md)

---

<div align="center">

![Banner](assets/banner.svg)

</div>

---

## Features

![Features](assets/features_en.svg)

### Core Features

- **Script Generation** - Generate Lua and Python scripts for DaVinci Resolve automation
- **API Reference** - Built-in Resolve Scripting API documentation for accurate code generation
- **Workflow Automation** - Automate editing, color grading, rendering, and delivery tasks

### Advanced Features

- **Fusion Compositing** - Create Fusion compositions and node-based effects via AI prompts
- **Color Grading Scripts** - AI-assisted color grading automation and LUT management
- **Project Templates** - Ready-to-use project and timeline templates for common scenarios

---

## System Requirements

| Component | Minimum Version |
|-----------|----------------|
| DaVinci Resolve | 18.0+ |
| Python | 3.6+ |
| OS | Windows 10+ / macOS 11+ / Linux |

---

## Installation

### As a Claude Code Skill

Copy the skill directory to your Claude Code skills folder:

```bash
# Clone the repository
git clone https://github.com/Tonyhzk/davinci-resolve-develop-skill.git

# Copy to your Claude Code project
cp -r davinci-resolve-develop-skill/src/davinci-resolve-develop-skill/ your-project/.claude/skills/
```

---

## Quick Start

Once installed, the AI assistant can help you with DaVinci Resolve development tasks:

- Generate automation scripts for timeline operations
- Create Fusion compositions from text descriptions
- Build rendering pipeline automation
- Manage media pool and project settings programmatically

---

## Project Structure

```
src/davinci-resolve-develop-skill/
├── SKILL.md           # Skill definition and instructions
├── docs/              # API reference documentation
│   ├── resolve-api/   # DaVinci Resolve Scripting API
│   └── examples/      # Script examples and templates
└── scripts/           # Utility scripts
```

---

## Development Guide

### Prerequisites

- DaVinci Resolve (Free or Studio)
- Python 3.6+
- Claude Code CLI

### Contributing

Contributions are welcome! Please ensure:

1. Code passes all tests
2. Documentation is updated
3. Commit messages are clear and descriptive

---

## Acknowledgements

- [DaVinci Resolve](https://www.blackmagicdesign.com/products/davinciresolve) by Blackmagic Design
- [Claude Code](https://claude.com/claude-code) by Anthropic

## License

[Apache License 2.0](LICENSE)

## Author

**Tonyhzk**

- GitHub: [@Tonyhzk](https://github.com/Tonyhzk)
- Project: [davinci-resolve-develop-skill](https://github.com/Tonyhzk/davinci-resolve-develop-skill)

---

<div align="center">

If this project helps you, please give it a Star!

</div>
