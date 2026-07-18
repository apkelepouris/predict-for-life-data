"""
Predict For Life - Date Parser

Provides helper functions for parsing dates returned by
lottery result sources.
"""

from __future__ import annotations

import re
from datetime import datetime, date


def parse_uk_date(date_text: str) -> date:
    """
    Parse UK date formats returned by lottery sources.

    Supported examples
    ------------------
    Thursday 16th July 2026
    Monday 1st March 2027
    Tue, 16 Jul 2026
    """

    cleaned = re.sub(
        r"(\d+)(st|nd|rd|th)",
        r"\1",
        date_text.strip(),
    )

    formats = [
        "%A %d %B %Y",   # Thursday 16 July 2026
        "%a, %d %b %Y",  # Thu, 16 Jul 2026
    ]

    for fmt in formats:
        try:
            return datetime.strptime(
                cleaned,
                fmt,
            ).date()
        except ValueError:
            pass

    raise ValueError(
        f"Unsupported UK date format: {date_text}"
    )