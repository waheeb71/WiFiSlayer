# -*- coding: utf-8 -*-
"""
WiFiSlayerTool v3.0 — Logger Module
Logs all operations with timestamps for documentation and auditing.
"""

import os
import logging
from datetime import datetime

from config import LOGS_DIR


def setup_logger(name="main"):
    """Initialize and return a configured logger instance."""
    os.makedirs(LOGS_DIR, exist_ok=True)

    log_file = os.path.join(
        LOGS_DIR, f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # ─── Prevent duplicate handlers on re-init ───────────────
    if logger.handlers:
        return logger

    # ─── File handler (detailed) ─────────────────────────────
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    file_fmt = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s │ %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    fh.setFormatter(file_fmt)

    # ─── Console handler (minimal — we use Rich for display) ─
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    console_fmt = logging.Formatter("%(levelname)s: %(message)s")
    ch.setFormatter(console_fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info("=" * 60)
    logger.info(f"  Session started — {datetime.now().isoformat()}")
    logger.info("=" * 60)

    return logger


# ─── Global logger instance ─────────────────────────────────
log = setup_logger()
