# Changelog

All notable changes to this project will be documented in this file.

**English** | [中文](CHANGELOG_CN.md)

---

## [Unreleased]

### Added

- **resolve_run.py** - Execution entry point that auto-connects to local Resolve and injects common variables (`resolve`, `project`, `timeline`, `mediapool`)
- **Inline code execution** - AI can now directly execute Python code to operate DaVinci Resolve in real-time

### Changed

- **API reference source** - Switched from bundled documentation to reading from local Resolve installation directory, ensuring API accuracy with installed version
- **SKILL.md description** - Updated to include operation-related trigger keywords (control, operate, timeline, media pool, project management)

### Removed

- **Bundled reference docs** - Removed packaged Developer documentation (~100+ files) in favor of reading from local Resolve installation

---

## [1.0.0] - 2026-03-16

### First Release

- **Script Generation** - Generate Lua and Python scripts for DaVinci Resolve automation
- **API Reference** - Built-in Resolve Scripting API documentation
- **Workflow Automation** - Automate editing, color grading, rendering, and delivery tasks
- **Fusion Compositing** - Create Fusion compositions and node-based effects via AI
- **Color Grading** - AI-assisted color grading scripts and LUT management
- **Project Templates** - Ready-to-use project and timeline templates
