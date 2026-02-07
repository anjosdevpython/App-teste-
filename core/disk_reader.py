"""Disk and image reader utilities with read-only guarantees."""

from __future__ import annotations

import os
import platform
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Generator, Iterable, Optional


@dataclass(slots=True)
class DeviceInfo:
    name: str
    path: str
    size_bytes: int
    fs_type: str
    mountpoint: str
    readonly: bool
    is_physical: bool


class DiskReader:
    """Read block devices or image files in strict read-only mode."""

    def __init__(self, source: str, block_size: int = 1024 * 1024) -> None:
        self.source = source
        self.block_size = block_size

    @staticmethod
    def list_devices() -> list[DeviceInfo]:
        """List devices and partitions cross-platform with best effort fallback."""
        system = platform.system().lower()
        if system == "linux":
            return DiskReader._list_linux()
        if system == "windows":
            return DiskReader._list_windows()
        return []

    @staticmethod
    def _list_linux() -> list[DeviceInfo]:
        cmd = ["lsblk", "-b", "-J", "-o", "NAME,PATH,SIZE,FSTYPE,MOUNTPOINT,RO,TYPE"]
        try:
            raw = subprocess.check_output(cmd, text=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            return []

        import json

        devices: list[DeviceInfo] = []
        payload = json.loads(raw)
        for entry in payload.get("blockdevices", []):
            devices.extend(DiskReader._flatten_linux_device(entry))
        return devices

    @staticmethod
    def _flatten_linux_device(entry: dict) -> list[DeviceInfo]:
        items: list[DeviceInfo] = []
        item = DeviceInfo(
            name=entry.get("name", ""),
            path=entry.get("path", ""),
            size_bytes=int(entry.get("size") or 0),
            fs_type=entry.get("fstype") or "unknown",
            mountpoint=entry.get("mountpoint") or "",
            readonly=bool(int(entry.get("ro") or 0)),
            is_physical=(entry.get("type") == "disk"),
        )
        items.append(item)
        for child in entry.get("children", []) or []:
            items.extend(DiskReader._flatten_linux_device(child))
        return items

    @staticmethod
    def _list_windows() -> list[DeviceInfo]:
        ps_script = (
            "Get-PhysicalDisk | Select FriendlyName,DeviceId,Size | ConvertTo-Json"
        )
        cmd = ["powershell", "-NoProfile", "-Command", ps_script]
        try:
            raw = subprocess.check_output(cmd, text=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            return []

        import json

        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            return []

        if isinstance(payload, dict):
            payload = [payload]

        devices = []
        for item in payload:
            did = item.get("DeviceId")
            devices.append(
                DeviceInfo(
                    name=item.get("FriendlyName", f"PhysicalDrive{did}"),
                    path=rf"\\.\PhysicalDrive{did}",
                    size_bytes=int(item.get("Size") or 0),
                    fs_type="unknown",
                    mountpoint="",
                    readonly=True,
                    is_physical=True,
                )
            )
        return devices

    def open_readonly(self):
        """Open source strictly read-only."""
        if os.name == "nt" and self.source.lower().startswith("\\\\.\\physicaldrive"):
            return open(self.source, "rb", buffering=0)
        return open(self.source, "rb", buffering=0)

    def iter_blocks(self, start_offset: int = 0, end_offset: Optional[int] = None) -> Generator[tuple[int, bytes], None, None]:
        with self.open_readonly() as fh:
            fh.seek(start_offset)
            offset = start_offset
            while True:
                if end_offset is not None and offset >= end_offset:
                    break
                to_read = self.block_size
                if end_offset is not None:
                    to_read = min(to_read, end_offset - offset)
                chunk = fh.read(to_read)
                if not chunk:
                    break
                yield offset, chunk
                offset += len(chunk)


def is_image_path(path: str) -> bool:
    ext = Path(path).suffix.lower()
    return ext in {".img", ".dd", ".raw", ".bin"}
