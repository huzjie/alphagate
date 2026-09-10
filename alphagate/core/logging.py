"""日志初始化：控制台 + 可选文件双写。"""
from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional

_configured = False


def setup_logging(level: int = logging.INFO, log_file: Optional[str] = None) -> logging.Logger:
    """初始化根日志器，幂等。返回 alphagate 日志器。"""
    global _configured
    logger = logging.getLogger("alphagate")
    if _configured:
        return logger
    logger.setLevel(level)
    fmt = logging.Formatter("%(asctime)s | %(levelname)-7s | %(name)s | %(message)s")
    if not logger.handlers:
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(fmt)
        logger.addHandler(sh)
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    logger.propagate = False
    _configured = True
    return logger
