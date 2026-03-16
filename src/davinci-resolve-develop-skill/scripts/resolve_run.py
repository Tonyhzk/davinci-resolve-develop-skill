#!/usr/bin/env python3
"""
DaVinci Resolve 脚本执行入口。
自动连接本机 Resolve，暴露常用变量后执行传入的 Python 代码。

用法:
    python3 resolve_run.py "print(project.GetName())"
    python3 resolve_run.py -f script.py
    echo "print(project.GetName())" | python3 resolve_run.py
"""

import sys
import os
import argparse


def connect_resolve():
    """连接本机 DaVinci Resolve，返回 resolve 对象。"""
    try:
        import DaVinciResolveScript as bmd
    except ImportError:
        if sys.platform.startswith("darwin"):
            module_path = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules/"
        elif sys.platform.startswith("win") or sys.platform.startswith("cygwin"):
            module_path = os.path.join(
                os.getenv("PROGRAMDATA", ""),
                "Blackmagic Design",
                "DaVinci Resolve",
                "Support",
                "Developer",
                "Scripting",
                "Modules",
            )
        elif sys.platform.startswith("linux"):
            module_path = "/opt/resolve/Developer/Scripting/Modules/"
        else:
            raise RuntimeError(f"不支持的平台: {sys.platform}")

        sys.path.insert(0, module_path)
        try:
            import DaVinciResolveScript as bmd
        except ImportError:
            raise RuntimeError(
                f"无法导入 DaVinciResolveScript，请确认 DaVinci Resolve 已安装。\n"
                f"尝试的模块路径: {module_path}"
            )

    resolve = bmd.scriptapp("Resolve")
    if not resolve:
        raise RuntimeError("无法连接 DaVinci Resolve，请确认 Resolve 正在运行。")
    return resolve


def build_context(resolve):
    """构建脚本执行上下文，返回包含常用变量的字典。"""
    pm = resolve.GetProjectManager()
    project = pm.GetCurrentProject() if pm else None
    timeline = project.GetCurrentTimeline() if project else None
    mediapool = project.GetMediaPool() if project else None

    return {
        "resolve": resolve,
        "pm": pm,
        "project": project,
        "timeline": timeline,
        "mediapool": mediapool,
        "fusion": resolve.Fusion() if hasattr(resolve, "Fusion") else None,
    }


def main():
    parser = argparse.ArgumentParser(description="执行 DaVinci Resolve Python 脚本")
    parser.add_argument("code", nargs="?", default=None, help="要执行的 Python 代码字符串")
    parser.add_argument("-f", "--file", default=None, help="要执行的 Python 脚本文件路径")
    args = parser.parse_args()

    # 确定要执行的代码
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            code = f.read()
    elif args.code:
        code = args.code
    elif not sys.stdin.isatty():
        code = sys.stdin.read()
    else:
        parser.print_help()
        sys.exit(1)

    # 连接 Resolve 并构建上下文
    try:
        resolve = connect_resolve()
        ctx = build_context(resolve)
    except RuntimeError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

    # 执行用户代码
    try:
        exec(code, ctx)
    except Exception as e:
        print(f"执行错误: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
