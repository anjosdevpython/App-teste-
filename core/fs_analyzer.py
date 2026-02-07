"""Filesystem heuristics for recovery-focused scans."""

from __future__ import annotations

import struct
from dataclasses import dataclass
from typing import Any

from core.disk_reader import DiskReader


@dataclass(slots=True)
class FSAnalysisResult:
    fs_type: str
    quick_format_suspected: bool
    deleted_entries: list[dict[str, Any]]
    orphan_inodes: list[int]
    notes: list[str]


class FileSystemAnalyzer:
    def __init__(self, reader: DiskReader) -> None:
        self.reader = reader

    def detect_fs(self) -> str:
        first = next(self.reader.iter_blocks(0, 4096), (0, b""))[1]
        if len(first) < 1024:
            return "unknown"
        if first[3:11] == b"NTFS    ":
            return "ntfs"
        if first[82:90] == b"FAT32   " or first[54:62] == b"FAT16   ":
            return "fat"
        if first[3:11] == b"EXFAT   ":
            return "exfat"
        if first[1080:1082] == b"\x53\xef":
            return "ext4"
        return "unknown"

    def analyze(self) -> FSAnalysisResult:
        fs_type = self.detect_fs()
        deleted_entries: list[dict[str, Any]] = []
        orphan_inodes: list[int] = []
        notes: list[str] = []

        if fs_type == "ntfs":
            deleted_entries, notes = self._analyze_ntfs()
        elif fs_type in {"fat", "exfat"}:
            deleted_entries, notes = self._analyze_fat_like()
        elif fs_type == "ext4":
            orphan_inodes, notes = self._analyze_ext4()

        quick = self._detect_quick_format(fs_type, deleted_entries, orphan_inodes)

        return FSAnalysisResult(
            fs_type=fs_type,
            quick_format_suspected=quick,
            deleted_entries=deleted_entries,
            orphan_inodes=orphan_inodes,
            notes=notes,
        )

    def _analyze_ntfs(self) -> tuple[list[dict[str, Any]], list[str]]:
        notes = ["NTFS: varredura heurística de registros MFT iniciada."]
        deleted: list[dict[str, Any]] = []
        scanned = 0
        for offset, chunk in self.reader.iter_blocks(0, 128 * 1024 * 1024):
            scanned += len(chunk)
            start = 0
            while True:
                idx = chunk.find(b"FILE", start)
                if idx < 0:
                    break
                rec = chunk[idx : idx + 1024]
                if len(rec) < 24:
                    break
                flags = struct.unpack_from("<H", rec, 22)[0]
                if not (flags & 0x01):
                    deleted.append(
                        {
                            "offset": offset + idx,
                            "type": "mft_record",
                            "reason": "not_in_use",
                        }
                    )
                start = idx + 4
        notes.append(f"NTFS: {len(deleted)} registros deletados candidatos em {scanned} bytes.")
        return deleted, notes

    def _analyze_fat_like(self) -> tuple[list[dict[str, Any]], list[str]]:
        notes = ["FAT/exFAT: busca por entradas deletadas (0xE5) em diretórios."]
        deleted = []
        for offset, chunk in self.reader.iter_blocks(0, 32 * 1024 * 1024):
            for i in range(0, len(chunk) - 32, 32):
                entry = chunk[i : i + 32]
                if entry[0] == 0xE5:
                    deleted.append({"offset": offset + i, "type": "dir_entry", "reason": "deleted_marker"})
        notes.append(f"FAT/exFAT: {len(deleted)} entradas deletadas identificadas.")
        return deleted, notes

    def _analyze_ext4(self) -> tuple[list[int], list[str]]:
        notes = ["EXT4: leitura de superbloco e verificação de inodes órfãos (heurística)."]
        superblock = next(self.reader.iter_blocks(1024, 2048), (0, b""))[1]
        orphan_count = 0
        if len(superblock) >= 236:
            orphan_count = struct.unpack_from("<I", superblock, 232)[0]
        orphans = list(range(1, min(orphan_count, 256) + 1))
        notes.append(f"EXT4: contagem estimada de inodes órfãos: {orphan_count}.")
        return orphans, notes

    @staticmethod
    def _detect_quick_format(fs_type: str, deleted_entries: list[dict[str, Any]], orphan_inodes: list[int]) -> bool:
        if fs_type in {"ntfs", "fat", "exfat"} and len(deleted_entries) > 20:
            return True
        if fs_type == "ext4" and len(orphan_inodes) > 10:
            return True
        return False
