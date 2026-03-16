#!/usr/bin/env python3
"""
规则文件同步管理工具
将 .claude/rules 中的文档逐个复制到 .clinerules 目录
支持：同步文件、移除文件、查看状态、清理备份
"""

import os
import sys
import shutil
import filecmp
from pathlib import Path


# ============================================================
# 配置
# ============================================================

SOURCE_SUBDIR = Path(".claude") / "rules"
TARGET_DIR_NAME = ".clinerules"

# 额外需要同步到 .clinerules 的文件（相对于项目根目录）
EXTRA_FILES = [
    "CLAUDE.md",
]

# 排除文件列表（.claude/rules 中不需要同步的文件名）
EXCLUDE_FILES = [
    # "某个不需要的规则.md",
]


# ============================================================
# 工具函数
# ============================================================

def get_paths():
    """获取源目录和目标目录路径"""
    project_dir = Path.cwd()
    source = project_dir / SOURCE_SUBDIR
    target = project_dir / TARGET_DIR_NAME
    return project_dir, source, target


def get_source_files(source_resolved: Path):
    """获取源目录中的所有非隐藏、非排除文件"""
    if not source_resolved.exists():
        return []
    return sorted([
        f for f in source_resolved.iterdir()
        if f.is_file() and not f.name.startswith('.') and f.name not in EXCLUDE_FILES
    ])


def get_all_managed_files(source_resolved: Path, project_dir: Path):
    """获取所有受管理的源文件（.claude/rules 下的 + 额外文件）"""
    files = get_source_files(source_resolved)
    for extra in EXTRA_FILES:
        extra_path = (project_dir / extra).resolve()
        if extra_path.is_file():
            files.append(extra_path)
    return files


def get_file_status(target_path: Path, source_file: Path):
    """
    检查文件同步状态
    返回: 'synced' | 'outdated' | 'symlink' | 'not_exist'
    """
    if target_path.is_symlink():
        return 'symlink'
    elif target_path.exists():
        if filecmp.cmp(str(source_file), str(target_path), shallow=False):
            return 'synced'
        return 'outdated'
    return 'not_exist'


# ============================================================
# 核心操作
# ============================================================

def show_status():
    """显示当前同步状态"""
    project_dir, source, target = get_paths()

    print(f"项目目录: {project_dir}")
    print(f"源目录:   {source}")

    # 检查源目录
    if not source.exists():
        print(f"  状态: ❌ 不存在")
        return

    source_resolved = source.resolve()
    if source != source_resolved:
        print(f"  真实路径: {source_resolved}")

    print(f"目标目录: {target}")
    if not target.exists():
        print(f"  状态: ❌ 不存在")
        return
    print()

    # 扫描源文件（含额外文件）
    source_files = get_all_managed_files(source_resolved, project_dir)
    if not source_files:
        print("没有找到受管理的文件")
        return

    # 显示每个文件的同步状态
    print(f"{'文件名':<40} {'状态'}")
    print("-" * 60)

    synced = 0
    outdated = 0
    missing = 0
    symlinks = 0

    for sf in source_files:
        target_path = target / sf.name
        status = get_file_status(target_path, sf)

        if status == 'synced':
            print(f"  {sf.name:<38} ✅ 已同步")
            synced += 1
        elif status == 'outdated':
            print(f"  {sf.name:<38} 🔄 需要更新")
            outdated += 1
        elif status == 'symlink':
            print(f"  {sf.name:<38} 🔗 是符号链接（需转为实际文件）")
            symlinks += 1
        else:
            print(f"  {sf.name:<38} ❌ 未同步")
            missing += 1

    print("-" * 60)
    print(f"合计: {len(source_files)} 个源文件 | ✅ {synced} 已同步 | 🔄 {outdated} 需更新 | ❌ {missing} 未同步 | 🔗 {symlinks} 符号链接")

    # 显示 .clinerules 中的独有文件
    source_names = {f.name for f in source_files}
    extra_files = sorted([
        f for f in target.iterdir()
        if f.is_file() and not f.name.startswith('.')
        and not f.name.endswith('.bak')
        and f.name not in source_names
    ])
    if extra_files:
        print(f"\n.clinerules 中的独有文件（不受管理）:")
        for f in extra_files:
            sym = " 🔗" if f.is_symlink() else ""
            print(f"  {f.name}{sym}")

    # 显示备份文件
    bak_files = sorted([
        f for f in target.iterdir()
        if f.name.endswith('.bak')
    ])
    if bak_files:
        print(f"\n备份文件:")
        for f in bak_files:
            print(f"  {f.name}")


def sync_rules():
    """同步文件（复制）"""
    project_dir, source, target = get_paths()

    if not source.exists():
        print(f"错误：源目录不存在: {source}")
        return

    source_resolved = source.resolve()
    source_files = get_all_managed_files(source_resolved, project_dir)

    if not source_files:
        print("没有找到受管理的文件")
        return

    # 确保目标目录存在
    target.mkdir(exist_ok=True)

    # 显示将要处理的文件
    print(f"源目录: {source_resolved}")
    print(f"额外文件: {', '.join(EXTRA_FILES)}")
    print(f"目标目录: {target}")
    print(f"\n找到 {len(source_files)} 个受管理文件:\n")

    needs_action = []
    for i, sf in enumerate(source_files, 1):
        target_path = target / sf.name
        status = get_file_status(target_path, sf)

        if status == 'synced':
            print(f"  {i}. {sf.name} — 已同步，跳过")
        elif status == 'outdated':
            print(f"  {i}. {sf.name} — 内容已变更，将更新")
            needs_action.append((sf, 'update'))
        elif status == 'symlink':
            print(f"  {i}. {sf.name} — 是符号链接，将替换为实际文件")
            needs_action.append((sf, 'replace_symlink'))
        else:
            print(f"  {i}. {sf.name} — 将复制")
            needs_action.append((sf, 'create'))

    if not needs_action:
        print("\n所有文件已同步，无需操作。")
        return

    print(f"\n将执行 {len(needs_action)} 个操作。")
    print("\n选项:")
    print("  1. 全部执行")
    print("  2. 逐个确认")
    print("  q. 取消")
    print()
    choice = input("请选择 [1/2/q]: ").strip().lower()

    if choice in ('q', 'quit', 'exit'):
        print("已取消")
        return

    confirm_each = (choice == '2')

    copied = 0
    skipped = 0

    for sf, action in needs_action:
        target_path = target / sf.name

        if confirm_each:
            yn = input(f"  同步 {sf.name}? [y/n]: ").strip().lower()
            if yn != 'y':
                print(f"    跳过: {sf.name}")
                skipped += 1
                continue

        # 处理已有文件/链接
        if action == 'replace_symlink':
            os.unlink(target_path)
        elif action == 'update':
            # 备份旧文件
            backup_path = target_path.with_suffix(target_path.suffix + ".bak")
            counter = 1
            while backup_path.exists():
                backup_path = target_path.with_suffix(f"{target_path.suffix}.bak{counter}")
                counter += 1
            shutil.copy2(str(target_path), str(backup_path))
            print(f"    备份: {sf.name} -> {backup_path.name}")

        # 复制文件
        shutil.copy2(str(sf), str(target_path))
        print(f"    复制: {sf.name}")
        copied += 1

    print(f"\n完成！复制: {copied}, 跳过: {skipped}")


def sync_rules_auto():
    """自动同步文件（非交互式，全部执行）"""
    project_dir, source, target = get_paths()

    if not source.exists():
        print(f"错误：源目录不存在: {source}")
        return

    source_resolved = source.resolve()
    source_files = get_all_managed_files(source_resolved, project_dir)

    if not source_files:
        print("没有找到受管理的文件")
        return

    # 确保目标目录存在
    target.mkdir(exist_ok=True)

    copied = 0
    skipped = 0

    for sf in source_files:
        target_path = target / sf.name
        status = get_file_status(target_path, sf)

        if status == 'synced':
            skipped += 1
            continue

        # 移除符号链接
        if status == 'symlink':
            os.unlink(target_path)

        # 复制文件
        shutil.copy2(str(sf), str(target_path))
        print(f"  同步: {sf.name}")
        copied += 1

    if copied == 0:
        print("所有文件已是最新，无需操作。")
    else:
        print(f"\n完成！同步: {copied}, 跳过（已最新）: {skipped}")


def remove_rules():
    """移除已同步的文件（只移除受管理的文件，不动独有文件）"""
    project_dir, source, target = get_paths()

    if not target.exists():
        print(f"目标目录不存在: {target}")
        return

    source_resolved = source.resolve() if source.exists() else None

    # 构建所有受管理文件名集合
    managed_names = set()
    if source_resolved:
        for sf in get_source_files(source_resolved):
            managed_names.add(sf.name)
    for extra in EXTRA_FILES:
        managed_names.add(Path(extra).name)

    # 找出 .clinerules 中属于受管理的文件
    managed_files = sorted([
        f for f in target.iterdir()
        if f.is_file() and f.name in managed_names
    ])

    if not managed_files:
        print("没有找到需要移除的受管理文件")
        return

    print(f"找到 {len(managed_files)} 个受管理的文件:\n")
    for i, f in enumerate(managed_files, 1):
        sym = " (符号链接)" if f.is_symlink() else ""
        print(f"  {i}. {f.name}{sym}")

    print("\n选项:")
    print("  1. 全部移除")
    print("  2. 逐个确认")
    print("  q. 取消")
    print()
    choice = input("请选择 [1/2/q]: ").strip().lower()

    if choice in ('q', 'quit', 'exit'):
        print("已取消")
        return

    confirm_each = (choice == '2')

    removed = 0

    for f in managed_files:
        if confirm_each:
            yn = input(f"  移除 {f.name}? [y/n]: ").strip().lower()
            if yn != 'y':
                continue

        f.unlink()
        print(f"  移除: {f.name}")
        removed += 1

    print(f"\n完成！移除: {removed}")


def clean_backups():
    """清理 .clinerules 中的 .bak 备份文件"""
    _, _, target = get_paths()

    if not target.exists():
        print(f"目标目录不存在: {target}")
        return

    bak_files = sorted([f for f in target.iterdir() if f.name.endswith('.bak')])

    if not bak_files:
        print("没有备份文件需要清理")
        return

    print(f"找到 {len(bak_files)} 个备份文件:\n")
    for i, f in enumerate(bak_files, 1):
        size = f.stat().st_size
        print(f"  {i}. {f.name} ({size} bytes)")

    print("\n确认删除所有备份文件?")
    yn = input("[y/n]: ").strip().lower()
    if yn == 'y':
        for f in bak_files:
            f.unlink()
            print(f"  删除: {f.name}")
        print(f"\n已清理 {len(bak_files)} 个备份文件")
    else:
        print("已取消")


# ============================================================
# 交互式菜单
# ============================================================

def interactive_menu():
    """交互式菜单"""
    while True:
        print("\n" + "=" * 50)
        print("规则文件同步管理工具")
        print(f".claude/rules -> .clinerules（实际复制）")
        print("=" * 50)
        print()
        show_status()
        print()
        print("操作选项:")
        print("  1. 同步文件 (sync)")
        print("  2. 移除文件 (remove)")
        print("  3. 清理备份文件 (clean)")
        print("  4. 刷新状态 (status)")
        print("  q. 退出")
        print()

        choice = input("请选择 [1/2/3/4/q]: ").strip().lower()

        if choice in ("1", "sync"):
            print()
            sync_rules()
        elif choice in ("2", "remove"):
            print()
            remove_rules()
        elif choice in ("3", "clean"):
            print()
            clean_backups()
        elif choice in ("4", "status"):
            continue
        elif choice in ("q", "quit", "exit"):
            print("退出")
            break
        else:
            print("无效选项")


def main():
    usage = """
规则文件同步管理工具（实际复制，非符号链接）

用法:
    python3 sync_rules_to_clinerules.py           交互式菜单
    python3 sync_rules_to_clinerules.py sync       同步文件（交互式）
    python3 sync_rules_to_clinerules.py auto       自动同步（非交互式）
    python3 sync_rules_to_clinerules.py remove     移除受管理文件
    python3 sync_rules_to_clinerules.py status     显示当前状态
    python3 sync_rules_to_clinerules.py clean      清理备份文件
"""

    if len(sys.argv) < 2:
        interactive_menu()
    else:
        cmd = sys.argv[1]
        if cmd == "sync":
            sync_rules()
        elif cmd == "auto":
            sync_rules_auto()
        elif cmd == "remove":
            remove_rules()
        elif cmd == "status":
            show_status()
        elif cmd == "clean":
            clean_backups()
        # 兼容旧命令
        elif cmd == "link":
            print("提示：link 命令已改为 sync（实际复制文件）")
            sync_rules()
        elif cmd == "unlink":
            print("提示：unlink 命令已改为 remove")
            remove_rules()
        else:
            print(usage)
            sys.exit(1)


if __name__ == "__main__":
    main()
