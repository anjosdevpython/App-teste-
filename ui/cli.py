"""Command line interface for RecoverX."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path

from core.disk_reader import DiskReader
from core.file_carver import FileCarver, SignatureRegistry
from core.fs_analyzer import FileSystemAnalyzer
from utils.logger import build_logger
from utils.report import write_json_report


ETHICAL_WARNING = (
    "Uso permitido apenas em dispositivos com autorização legal. "
    "A recuperação forense deve preservar cadeia de custódia."
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="recoverx", description="Ferramenta de recuperação de arquivos (forense/read-only).")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="Lista discos/partições detectados")

    scan = sub.add_parser("scan", help="Executa análise e recuperação")
    scan.add_argument("--source", required=True, help="Dispositivo ou imagem (.img/.dd)")
    scan.add_argument("--destination", required=True, help="Diretório de saída")
    scan.add_argument("--signatures", default="signatures/signatures.json")
    scan.add_argument("--deep", action="store_true", help="Ativa deep scan (sobreposição maior)")
    scan.add_argument("--workers", type=int, default=4)

    return parser


def run_cli(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    logger = build_logger("reports")
    logger.info(ETHICAL_WARNING)

    if args.command == "list":
        for dev in DiskReader.list_devices():
            print(f"{dev.path:25} {dev.fs_type:8} {dev.size_bytes:>12} bytes ro={dev.readonly}")
        return 0

    reader = DiskReader(args.source)
    analyzer = FileSystemAnalyzer(reader)
    analysis = analyzer.analyze()

    registry = SignatureRegistry(args.signatures)
    carver = FileCarver(reader, registry, args.destination, deep_scan=args.deep, workers=max(args.workers, 1))
    hits = carver.carve()

    report_path = Path("reports") / "recovery_report.json"
    write_json_report(
        str(report_path),
        {
            "source": args.source,
            "destination": args.destination,
            "analysis": asdict(analysis),
            "recovered_count": len(hits),
            "recovered_files": [asdict(hit) for hit in hits],
            "ethical_warning": ETHICAL_WARNING,
        },
    )

    logger.info("Análise concluída: %s arquivos recuperados.", len(hits))
    logger.info("Relatório salvo em %s", report_path)
    return 0
