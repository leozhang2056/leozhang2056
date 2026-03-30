"""Load generation config with safe defaults."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml

DEFAULT_CONFIG: Dict[str, Any] = {
    "role_inference": {
        "keywords": {
            "android": [
                "android", "kotlin", "jetpack", "compose", "gradle", "adb", "ndk", "jni",
                "mvvm", "room", "coroutines", "retrofit", "okhttp",
            ],
            "ai": [
                "pytorch", "tensorflow", "llm", "diffusion", "computer vision", "cv", "onnx", "cuda",
                "transformer", "fine-tuning", "finetuning", "rag", "embedding", "prompt", "ml", "machine learning",
            ],
            "backend": [
                "spring", "spring boot", "spring cloud", "java", "microservice", "rest", "api",
                "mybatis", "hibernate", "jpa", "redis", "kafka",
            ],
        }
    },
    "project_ranking": {
        "default_priority": 9999,
        "priority_offset": 200,
        "role_project_order": {
            "android": [
                "enterprise-messaging", "smart-factory", "iot-solutions", "chatclothes", "picture-book-locker", "visual-gateway",
            ],
            "ai": [
                "chatclothes", "device-maintenance-prediction", "chinese-herbal-recognition", "exhibition-robot", "enterprise-messaging", "smart-factory",
            ],
            "backend": [
                "enterprise-messaging", "smart-factory", "live-streaming-system", "chatclothes", "iot-solutions", "visual-gateway",
            ],
            "fullstack": [
                "chatclothes", "enterprise-messaging", "smart-factory", "live-streaming-system", "iot-solutions",
            ],
        },
        "base_priority": {
            "chatclothes": 10,
            "enterprise-messaging": 20,
            "smart-factory": 30,
            "live-streaming-system": 40,
            "visual-gateway": 50,
            "device-maintenance-prediction": 60,
            "chinese-herbal-recognition": 70,
            "iot-solutions": 80,
            "exhibition-robot": 90,
            "picture-book-locker": 100,
            "forest-patrol-inspection": 110,
            "smart-power": 120,
            "boobit": 130,
            "broadcast-control": 140,
            "visit-system": 150,
            "school-attendance": 160,
            "patent-search-system": 170,
        },
    },
}


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(base)
    for key, val in (override or {}).items():
        if isinstance(val, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], val)
        else:
            result[key] = val
    return result


def load_generation_config() -> Dict[str, Any]:
    """Load kb/generation_config.yaml and merge with defaults."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    cfg_path = repo_root / "kb" / "generation_config.yaml"
    if not cfg_path.exists():
        return dict(DEFAULT_CONFIG)

    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            loaded = yaml.safe_load(f) or {}
        if not isinstance(loaded, dict):
            return dict(DEFAULT_CONFIG)
        return _deep_merge(DEFAULT_CONFIG, loaded)
    except Exception:
        return dict(DEFAULT_CONFIG)

