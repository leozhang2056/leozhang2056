#!/usr/bin/env python3
"""Session start hook: nudge layered-memory bootstrap."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def _read_tail_lines(path: Path, max_lines: int = 40) -> list[str]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    lines = [line for line in text.splitlines() if line.strip()]
    return lines[-max_lines:]


def _read_stdin_json() -> dict:
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def main() -> int:
    _ = _read_stdin_json()
    root = Path(__file__).resolve().parents[2]
    marker = root / "memory" / ".session_hint_start.txt"
    learning_queue = root / "memory" / "L1_LEARNING_QUEUE.md"
    marker.parent.mkdir(parents=True, exist_ok=True)
    learning_tail = _read_tail_lines(learning_queue, max_lines=30)
    learning_preview = "\n".join(learning_tail[-8:]) if learning_tail else "No learning candidates yet."
    marker.write_text(
        (
            "Read in order: memory/L0_BOOTSTRAP.md -> memory/L1_SESSION_STATE.md -> memory/L2_DEEP_INDEX.md\n"
            "\nRecent learning candidates (latest excerpt):\n"
            f"{learning_preview}\n"
        ),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
