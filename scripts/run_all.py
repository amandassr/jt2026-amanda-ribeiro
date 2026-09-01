#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all.py — executa toda a análise na ordem correta.

Uso:
    python3 scripts/run_all.py

Executa: 01_audit -> 02_clean -> 03_revenue -> 04_return -> 06_features -> 05_charts.
Saídas em output/.
"""
import subprocess
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = [
    "01_audit.py",
    "02_clean.py",
    "03_revenue.py",
    "04_return.py",
    "06_features.py",
    "05_charts.py",
]

fail = False
for s in SCRIPTS:
    path = os.path.join(ROOT, "scripts", s)
    print(f"\n=== rodando {s} ===")
    rc = subprocess.call([sys.executable, path], cwd=os.path.join(ROOT, "scripts"))
    if rc != 0:
        print(f"ERRO em {s} (código {rc})")
        fail = True
        break

if fail:
    sys.exit(1)
print("\nAnálise concluída com sucesso. Saídas em output/.")
