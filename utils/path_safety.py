from __future__ import annotations

import re


def safe_filename(name: str) -> str:
    sanitized = re.sub(r"[^a-zA-Z0-9._-]", "_", name)
    return sanitized[:255]
