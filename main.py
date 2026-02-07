from __future__ import annotations

import argparse

from ui.cli import run_cli
from ui.gui import run_gui


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RecoverX launcher")
    parser.add_argument("--gui", action="store_true", help="Abre interface gráfica Tkinter")
    args, remaining = parser.parse_known_args()

    if args.gui:
        run_gui()
    else:
        raise SystemExit(run_cli(remaining))
