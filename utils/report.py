from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def write_json_report(path: str, data: dict[str, Any]) -> None:
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        **data,
    }
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
