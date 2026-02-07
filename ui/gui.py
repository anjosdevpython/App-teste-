"""GUI opcional em Tkinter para operações básicas."""

from __future__ import annotations

import threading
import tkinter as tk
from tkinter import filedialog, messagebox

from ui.cli import run_cli


class RecoverXApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("RecoverX")
        self.geometry("640x220")

        self.source_var = tk.StringVar()
        self.dest_var = tk.StringVar()

        self._build()

    def _build(self) -> None:
        tk.Label(self, text="Origem (dispositivo/imagem)").pack(anchor="w", padx=10, pady=5)
        tk.Entry(self, textvariable=self.source_var, width=85).pack(padx=10)

        tk.Label(self, text="Destino").pack(anchor="w", padx=10, pady=5)
        row = tk.Frame(self)
        row.pack(fill="x", padx=10)
        tk.Entry(row, textvariable=self.dest_var, width=70).pack(side="left")
        tk.Button(row, text="Selecionar", command=self._pick_dest).pack(side="left", padx=6)

        tk.Button(self, text="Iniciar Scan", command=self._start_scan).pack(pady=20)

    def _pick_dest(self) -> None:
        selected = filedialog.askdirectory(title="Escolha o diretório de destino")
        if selected:
            self.dest_var.set(selected)

    def _start_scan(self) -> None:
        source = self.source_var.get().strip()
        dest = self.dest_var.get().strip()
        if not source or not dest:
            messagebox.showerror("Erro", "Preencha origem e destino.")
            return

        def worker() -> None:
            code = run_cli(["scan", "--source", source, "--destination", dest])
            if code == 0:
                messagebox.showinfo("RecoverX", "Scan finalizado com sucesso.")
            else:
                messagebox.showerror("RecoverX", f"Falha no scan (código {code}).")

        threading.Thread(target=worker, daemon=True).start()


def run_gui() -> None:
    app = RecoverXApp()
    app.mainloop()
