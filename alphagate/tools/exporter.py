"""导出：决策/回测结果导出为 JSON / CSV / Markdown。"""
from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import Any, Dict, List


class Exporter:
    """统一导出工具。"""

    @staticmethod
    def to_json(obj: Any, path: str | None = None, indent: int = 2) -> str:
        s = json.dumps(obj, ensure_ascii=False, indent=indent)
        if path:
            Path(path).write_text(s, encoding="utf-8")
        return s

    @staticmethod
    def to_markdown_table(rows: List[Dict[str, Any]], path: str | None = None) -> str:
        if not rows:
            return ""
        cols = list(rows[0].keys())
        header = "| " + " | ".join(cols) + " |"
        sep = "| " + " | ".join("---" for _ in cols) + " |"
        body = []
        for r in rows:
            body.append("| " + " | ".join(str(r.get(c, "")) for c in cols) + " |")
        out = "\n".join([header, sep] + body)
        if path:
            Path(path).write_text(out, encoding="utf-8")
        return out

    @staticmethod
    def to_csv(rows: List[Dict[str, Any]], path: str | None = None) -> str:
        if not rows:
            return ""
        cols = list(rows[0].keys())
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
        out = buf.getvalue()
        if path:
            Path(path).write_text(out, encoding="utf-8", newline="")
        return out
