"""Binary signature carving engine."""

from __future__ import annotations

import json
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from core.disk_reader import DiskReader
from utils.hashing import sha256_file
from utils.path_safety import safe_filename


@dataclass(slots=True)
class CarveHit:
    signature: str
    start_offset: int
    end_offset: int
    output_path: str
    sha256: str
    fragmented: bool


class SignatureRegistry:
    def __init__(self, signatures_path: str) -> None:
        self.signatures_path = signatures_path
        self.signatures = self._load()

    def _load(self) -> list[dict]:
        with open(self.signatures_path, "r", encoding="utf-8") as fh:
            payload = json.load(fh)
        return payload["signatures"]


class FileCarver:
    def __init__(
        self,
        reader: DiskReader,
        registry: SignatureRegistry,
        output_dir: str,
        deep_scan: bool = False,
        workers: int = 4,
    ) -> None:
        self.reader = reader
        self.registry = registry
        self.output_dir = Path(output_dir)
        self.deep_scan = deep_scan
        self.workers = workers
        self._lock = threading.Lock()

    def carve(self) -> list[CarveHit]:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        futures = []
        hits: list[CarveHit] = []
        with ThreadPoolExecutor(max_workers=self.workers) as pool:
            for sig in self.registry.signatures:
                futures.append(pool.submit(self._carve_signature, sig))
            for fut in futures:
                hits.extend(fut.result())
        return sorted(hits, key=lambda h: h.start_offset)

    def _carve_signature(self, sig: dict) -> list[CarveHit]:
        header = bytes.fromhex(sig["header"])
        footer = bytes.fromhex(sig["footer"]) if sig.get("footer") else None
        extension = sig["extension"]
        max_size = sig.get("max_size", 50 * 1024 * 1024)

        hits: list[CarveHit] = []
        overlap = 4096 if self.deep_scan else 512
        previous_tail = b""
        previous_offset = 0

        for offset, chunk in self.reader.iter_blocks():
            combined = previous_tail + chunk
            base_offset = previous_offset

            start = 0
            while True:
                idx = combined.find(header, start)
                if idx < 0:
                    break
                absolute_start = base_offset + idx
                carve_end, fragmented = self._find_end(absolute_start, header, footer, max_size)
                out = self._write_recovered_file(absolute_start, carve_end, extension)
                digest = sha256_file(out)
                hits.append(
                    CarveHit(
                        signature=sig["name"],
                        start_offset=absolute_start,
                        end_offset=carve_end,
                        output_path=str(out),
                        sha256=digest,
                        fragmented=fragmented,
                    )
                )
                start = idx + len(header)

            previous_tail = combined[-overlap:]
            previous_offset = offset + len(chunk) - len(previous_tail)
        return hits

    def _find_end(self, start_offset: int, header: bytes, footer: Optional[bytes], max_size: int) -> tuple[int, bool]:
        with self.reader.open_readonly() as fh:
            fh.seek(start_offset)
            data = fh.read(max_size)

        if footer:
            idx = data.find(footer, len(header))
            if idx >= 0:
                return start_offset + idx + len(footer), False
        return start_offset + len(data), True

    def _write_recovered_file(self, start: int, end: int, extension: str) -> Path:
        filename = safe_filename(f"recovered_{start:012x}.{extension}")
        out = self.output_dir / filename
        with self.reader.open_readonly() as source, open(out, "wb") as target:
            source.seek(start)
            remaining = end - start
            while remaining > 0:
                chunk = source.read(min(1024 * 1024, remaining))
                if not chunk:
                    break
                target.write(chunk)
                remaining -= len(chunk)
        return out
