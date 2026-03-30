#!/usr/bin/env python3
"""
简单的 facts.yaml 验证脚本
"""

import sys
from pathlib import Path

try:
    from kb_validation import validate_all_projects
except ModuleNotFoundError:
    from app.backend.kb_validation import validate_all_projects


def main():
    # 尽量在 Windows 控制台下使用 UTF-8，避免输出编码问题。
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    projects_dir = Path(__file__).parent.parent.parent / "projects"
    
    print("=" * 60)
    print("Facts.yaml 验证结果")
    print("=" * 60)
    
    all_pass = True
    results = validate_all_projects(projects_dir)

    for project_name, errors in results.items():
        if errors:
            print(f"\n[ERROR] {project_name}:")
            for e in errors:
                print(f"   - {e}")
            all_pass = False
        else:
            print(f"[OK] {project_name}")

    print("\n" + "=" * 60)
    if all_pass:
        print("[PASS] 所有项目验证通过！")
    else:
        print("[FAIL] 存在验证错误")
    print("=" * 60)


if __name__ == "__main__":
    main()
