#!/usr/bin/env python3
"""
Convenience wrapper: generate Android-focused CV (preferred entry).

This is a thin helper around the unified CLI:
  python generate.py cv --role android

For more control (JD keywords, max projects, custom output path), use:
  python generate.py cv --role android --jd-keywords Kotlin MVVM Jetpack ...
"""

import sys
import os
from pathlib import Path

root_dir   = Path(__file__).parent
backend_dir = root_dir / 'app' / 'backend'
sys.path.insert(0, str(backend_dir))

from generate_cv_from_kb import generate_cv_from_kb
import asyncio


def main():
    print("Generating Android-focused CV from Career KB...")
    print("-" * 60)
    en_path, zh_path = asyncio.run(generate_cv_from_kb(role_type='android'))
    print("-" * 60)
    print(f"EN: {en_path}")
    print(f"ZH: {zh_path}")


if __name__ == '__main__':
    main()
