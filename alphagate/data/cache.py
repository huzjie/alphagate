"""轻量磁盘缓存：键 -> JSON，带 TTL。"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any, Optional


class DiskCache:
    """简单文件缓存，路径在 ~/.cache/alphagate。"""

    def __init__(self, cache_dir: str = "~/.cache/alphagate") -> None:
        self.root = Path(cache_dir).expanduser()
        self.root.mkdir(parents=True, exist_ok=True)

    def _key(self, key: str) -> Path:
        h = hashlib.md5(key.encode("utf-8")).hexdigest()
        return self.root / f"{h}.json"

    def get(self, key: str, ttl: int = 3600) -> Optional[Any]:
        p = self._key(key)
        if not p.exists():
            return None
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if time.time() - data.get("ts", 0) > ttl:
                return None
            return data.get("value")
        except (json.JSONDecodeError, OSError):
            return None

    def set(self, key: str, value: Any) -> None:
        self._key(key).write_text(
            json.dumps({"ts": time.time(), "value": value}, ensure_ascii=False),
            encoding="utf-8",
        )
