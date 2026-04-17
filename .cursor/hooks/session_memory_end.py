#!/usr/bin/env python3
"""Session end hook: persist memory and evolve long-term rules."""

from __future__ import annotations

import json
import re
import sys
import threading
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

MIN_PROMOTE_FREQ = 3

SYNONYM_MAP = {
    "cursor 慢": "cursor性能慢",
    "cursor很慢": "cursor性能慢",
    "scan 全仓": "避免全仓扫描",
    "全仓扫描": "避免全仓扫描",
    "重新扫描": "避免全量重扫",
    "resume": "简历",
    "cv": "简历",
}

STOP_TOKENS = {
    "preferences:",
    "mistakes/regressions:",
    "improvement proposals:",
    "promote policy:",
}


def _read_stdin_json(timeout_sec: float = 1.5) -> dict:
    """Best-effort stdin read.

    Hooks provide JSON via stdin, but manual command execution may leave stdin open
    and block forever. This timeout keeps the script non-blocking in both modes.
    """

    buf: dict[str, str] = {"raw": ""}

    def _reader() -> None:
        try:
            buf["raw"] = sys.stdin.read()
        except Exception:
            buf["raw"] = ""

    t = threading.Thread(target=_reader, daemon=True)
    t.start()
    t.join(timeout_sec)
    raw = (buf.get("raw") or "").strip()
    if not raw:
        return {}
    try:
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _pick_text(payload: dict[str, Any], keys: list[str]) -> str:
    for key in keys:
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _normalize_list(value: Any) -> list[str]:
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            if isinstance(item, str) and item.strip():
                out.append(item.strip())
        return out
    return []


def _canonicalize_text(text: str) -> str:
    clean = text.strip().lower()
    clean = re.sub(r"\s+", " ", clean)
    clean = clean.replace("，", ",").replace("。", ".")
    for src, dst in SYNONYM_MAP.items():
        clean = clean.replace(src, dst)
    return clean


def _extract_summary(payload: dict[str, Any]) -> dict[str, Any]:
    summary = {
        "goal": _pick_text(payload, ["current_goal", "goal", "objective"]),
        "completed": _normalize_list(payload.get("completed") or payload.get("done")),
        "in_progress": _pick_text(payload, ["in_progress", "active_task", "current_task"]),
        "blockers": _normalize_list(payload.get("blockers")),
        "next_action": _pick_text(payload, ["next_action", "next_step"]),
        "touched_files": _normalize_list(payload.get("touched_files") or payload.get("files")),
        "preferences": _normalize_list(payload.get("preferences") or payload.get("user_preferences")),
        "mistakes": _normalize_list(payload.get("mistakes") or payload.get("regressions")),
        "improvements": _normalize_list(payload.get("improvements") or payload.get("lessons")),
    }
    summary["preferences"] = [_canonicalize_text(x) for x in summary["preferences"]]
    summary["mistakes"] = [_canonicalize_text(x) for x in summary["mistakes"]]
    summary["improvements"] = [_canonicalize_text(x) for x in summary["improvements"]]
    return summary


def _quality_check(summary: dict[str, Any]) -> tuple[bool, list[str]]:
    missing: list[str] = []
    if not summary["goal"]:
        missing.append("goal")
    if not summary["next_action"]:
        missing.append("next_action")
    if not summary["improvements"]:
        missing.append("improvements")
    return len(missing) == 0, missing


def _item_score(item: str, count: int) -> tuple[int, float]:
    impact = 3 if any(k in item for k in ["阻断", "失败", "quality_fail", "回归"]) else 2
    confidence = 0.9 if count >= 5 else 0.75 if count >= 3 else 0.6
    return impact, confidence


def _validation_for_item(item: str) -> str:
    if any(k in item for k in ["facts", "yaml", "schema", "kb", "数据"]):
        return "python app/backend/validate.py"
    if any(k in item for k in ["test", "regression", "回归", "bug", "失败"]):
        return "pytest"
    return "python app/backend/validate.py && pytest"


def _build_markdown_block(summary: dict[str, Any], ts: str, quality_ok: bool, missing: list[str]) -> str:
    goal = summary["goal"] or "（自动总结缺少 goal，需补充）"
    completed = summary["completed"] or ["（自动总结缺少 completed，需补充）"]
    in_progress = summary["in_progress"] or "（自动总结缺少 in_progress，需补充）"
    blockers = summary["blockers"] or ["（无）"]
    next_action = summary["next_action"] or "（自动总结缺少 next_action，需补充）"
    touched_files = summary["touched_files"] or ["（未检测到）"]

    block = ["", f"## Session Memory - {ts}", f"- Goal: {goal}", "- Completed:"]
    block.extend([f"  - {item}" for item in completed])
    block.append(f"- In Progress: {in_progress}")
    block.append("- Blockers:")
    block.extend([f"  - {item}" for item in blockers])
    block.append(f"- Next Action: {next_action}")
    block.append("- Last Touched Files:")
    block.extend([f"  - {item}" for item in touched_files])
    block.append(f"- Quality Gate: {'PASS' if quality_ok else 'QUALITY_FAIL'}")
    if missing:
        block.append(f"- Missing Required Fields: {', '.join(missing)}")
    return "\n".join(block) + "\n"


def _build_learning_block(summary: dict[str, Any], ts: str) -> str:
    prefs = summary["preferences"] or ["（未提供）"]
    mistakes = summary["mistakes"] or ["（未提供）"]
    improvements = summary["improvements"] or ["（未提供）"]
    lines = ["", f"## Learning Candidate - {ts}", "- Preferences:"]
    lines.extend([f"  - {item}" for item in prefs])
    lines.append("- Mistakes/Regressions:")
    lines.extend([f"  - {item}" for item in mistakes])
    lines.append("- Improvement Proposals:")
    lines.extend([f"  - {item}" for item in improvements])
    lines.append("- Promote Policy:")
    lines.append(f"  - 若同类偏好连续出现 >= {MIN_PROMOTE_FREQ} 次，提升到 L0/L2 规则层。")
    return "\n".join(lines) + "\n"


def _load_or_init_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"last_daily_merge_date": "", "last_weekly_compact_key": "", "last_merged_line": 0}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return {
                "last_daily_merge_date": str(data.get("last_daily_merge_date", "")),
                "last_weekly_compact_key": str(data.get("last_weekly_compact_key", "")),
                "last_merged_line": int(data.get("last_merged_line", 0)),
            }
    except Exception:
        pass
    return {"last_daily_merge_date": "", "last_weekly_compact_key": "", "last_merged_line": 0}


def _extract_candidates(lines: list[str]) -> list[str]:
    candidates: list[str] = []
    for line in lines:
        s = line.strip()
        if not s.startswith("-"):
            continue
        text = s.lstrip("-").strip()
        if not text:
            continue
        if text.lower() in STOP_TOKENS:
            continue
        if "（未提供）" in text or "同类偏好连续出现" in text:
            continue
        candidates.append(_canonicalize_text(text))
    return candidates


def _append_failure_patterns(failure_file: Path, summary: dict[str, Any], ts: str) -> int:
    mistakes = summary["mistakes"]
    if not mistakes:
        return 0
    if not failure_file.exists():
        failure_file.write_text(
            "# Failure Patterns\n\n"
            "> 记录触发条件 -> 错误行为 -> 正确做法 -> 检查点，避免重复踩坑。\n",
            encoding="utf-8",
        )
    lines = [""]
    for item in mistakes:
        lines.extend(
            [
                f"## Pattern - {ts}",
                f"- Trigger: {item}",
                "- Wrong Behavior: 发生回归或重复低效动作",
                "- Correct Practice: 写入规则并绑定验证命令",
                "- Checkpoint: 执行 `python app/backend/validate.py && pytest`",
                "",
            ]
        )
    with failure_file.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return len(mistakes)


def _daily_merge_learning(learning_queue: Path, evolved_rules: Path, state_file: Path, today: str) -> tuple[bool, list[dict[str, Any]], int]:
    state = _load_or_init_state(state_file)
    if state["last_daily_merge_date"] == today or not learning_queue.exists():
        return False, [], int(state["last_merged_line"])

    all_lines = learning_queue.read_text(encoding="utf-8").splitlines()
    start_line = max(0, int(state["last_merged_line"]))
    new_lines = all_lines[start_line:]
    counter = Counter(_extract_candidates(new_lines))

    promoted: list[dict[str, Any]] = []
    for item, count in sorted(counter.items(), key=lambda x: (-x[1], x[0])):
        if count < MIN_PROMOTE_FREQ:
            continue
        impact, confidence = _item_score(item, count)
        promoted.append(
            {
                "item": item,
                "count": count,
                "impact": impact,
                "confidence": confidence,
                "validation": _validation_for_item(item),
            }
        )

    evolved_rules.parent.mkdir(parents=True, exist_ok=True)
    if not evolved_rules.exists():
        evolved_rules.write_text(
            "# L2 进化规则（每日归并）\n\n"
            "> 来源：L1 学习队列的每日归并结果。\n"
            "> 规则：同类经验当日新增出现 >= 3 次，提升为长期偏好候选。\n",
            encoding="utf-8",
        )

    block = [
        "",
        f"## Daily Merge - {today}",
        f"- Processed learning lines: {len(new_lines)}",
        f"- Promoted count: {len(promoted)}",
        "- Promoted items:",
    ]
    if promoted:
        for p in promoted:
            block.append(
                f"  - [{p['count']}x][impact={p['impact']}][confidence={p['confidence']}] {p['item']} | verify: `{p['validation']}`"
            )
    else:
        block.append("  - （今日无满足>=3次的新增经验）")
    with evolved_rules.open("a", encoding="utf-8") as f:
        f.write("\n".join(block) + "\n")

    new_state = {
        "last_daily_merge_date": today,
        "last_weekly_compact_key": state.get("last_weekly_compact_key", ""),
        "last_merged_line": len(all_lines),
    }
    state_file.write_text(json.dumps(new_state, ensure_ascii=False, indent=2), encoding="utf-8")
    return True, promoted, len(all_lines)


def _weekly_compact(learning_queue: Path, weekly_file: Path, state_file: Path, today: datetime) -> tuple[bool, int]:
    state = _load_or_init_state(state_file)
    week_key = f"{today.strftime('%Y')}-W{today.isocalendar().week:02d}"
    if state.get("last_weekly_compact_key") == week_key or not learning_queue.exists():
        return False, 0

    lines = learning_queue.read_text(encoding="utf-8").splitlines()
    counter = Counter(_extract_candidates(lines))
    top = sorted(counter.items(), key=lambda x: (-x[1], x[0]))[:20]

    if not weekly_file.exists():
        weekly_file.write_text(
            "# Weekly Learnings\n\n"
            "> 每周压缩高价值经验，防止记忆膨胀。\n",
            encoding="utf-8",
        )
    block = [
        "",
        f"## {week_key}",
        f"- Source lines: {len(lines)}",
        "- Top learnings:",
    ]
    if top:
        block.extend([f"  - [{count}x] {item}" for item, count in top])
    else:
        block.append("  - （本周无有效学习项）")
    with weekly_file.open("a", encoding="utf-8") as f:
        f.write("\n".join(block) + "\n")

    state["last_weekly_compact_key"] = week_key
    state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    return True, len(top)


def _retain_recent_sections(path: Path, section_prefix: str, keep: int) -> int:
    """Keep only recent N markdown sections by heading prefix."""
    if not path.exists():
        return 0
    lines = path.read_text(encoding="utf-8").splitlines()
    idx: list[int] = []
    for i, line in enumerate(lines):
        if line.startswith(section_prefix):
            idx.append(i)
    if len(idx) <= keep:
        return 0
    cut_count = len(idx) - keep
    cut_line = idx[cut_count]
    new_lines = lines[: max(0, idx[0])] + lines[cut_line:]
    path.write_text("\n".join(new_lines).rstrip() + "\n", encoding="utf-8")
    return cut_count


def main() -> int:
    payload = _read_stdin_json()
    root = Path(__file__).resolve().parents[2]
    memory_dir = root / "memory"
    log_file = memory_dir / ".session_end_log.md"
    session_state = memory_dir / "L1_SESSION_STATE.md"
    learning_queue = memory_dir / "L1_LEARNING_QUEUE.md"
    evolved_rules = memory_dir / "L2_EVOLVED_RULES.md"
    weekly_file = memory_dir / "WEEKLY_LEARNINGS.md"
    failure_file = memory_dir / "FAILURE_PATTERNS.md"
    merge_state = memory_dir / ".daily_merge_state.json"
    memory_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    ts = now.strftime("%Y-%m-%d %H:%M:%S")
    today = now.strftime("%Y-%m-%d")

    summary = _extract_summary(payload)
    quality_ok, missing = _quality_check(summary)
    with session_state.open("a", encoding="utf-8") as f:
        f.write(_build_markdown_block(summary, ts, quality_ok, missing))
    with learning_queue.open("a", encoding="utf-8") as f:
        f.write(_build_learning_block(summary, ts))

    failure_count = _append_failure_patterns(failure_file, summary, ts)
    merged, promoted, merged_line = _daily_merge_learning(learning_queue, evolved_rules, merge_state, today)
    compacted, compact_count = _weekly_compact(learning_queue, weekly_file, merge_state, now)
    pruned_session = _retain_recent_sections(session_state, "## Session Memory - ", keep=120)
    pruned_learning = _retain_recent_sections(learning_queue, "## Learning Candidate - ", keep=240)

    with log_file.open("a", encoding="utf-8") as f:
        f.write(
            f"- [{ts}] sessionEnd quality={'PASS' if quality_ok else 'QUALITY_FAIL'} "
            f"missing={','.join(missing) if missing else '-'} "
            f"daily_merge={'yes' if merged else 'no'} promoted={len(promoted)} merged_line={merged_line} "
            f"weekly_compact={'yes' if compacted else 'no'} weekly_items={compact_count} "
            f"failure_patterns={failure_count} pruned_session={pruned_session} pruned_learning={pruned_learning}\n"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
