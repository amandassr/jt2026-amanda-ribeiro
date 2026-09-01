#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Etapa 3 — Características associadas a diárias e receitas maiores (ASSOCIAÇÃO, não causa)
Hackathon Jovens Talentos AI Builder 2026 (Seazone) — Itapema (SC)

Apenas descreve relações entre características do imóvel e diária/receita estimada.
Não estabelece causalidade. Dados: diária mediana por imóvel (mediana das noites)
e receita anual estimada (cenário base, ver config.py).
"""
import os
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(ROOT, "output", "processed")
OUT = os.path.join(ROOT, "output")

rev = pd.read_csv(os.path.join(PROC, "revenue_per_imovel.csv"))
base = pd.read_csv(os.path.join(PROC, "base_airbnb.csv"))
m = rev.merge(base[["airbnb_listing_id", "number_of_bathrooms", "number_of_guests",
                    "number_of_reviews", "star_rating", "cleaning_fee", "min_nights",
                    "is_superhost"]], on="airbnb_listing_id", how="left")
m = m.dropna(subset=["diaria_mediana"])

L = []
L.append("# Características associadas a diárias e receitas maiores (associação, NÃO causalidade)\n")
L.append(f"Base: {len(m)} imóveis com preço. Diária = mediana das noites. "
         f"Receita = estimada (cenário base). **Correlação de Spearman** (ordem, robusta a outliers).\n")

rows = []
for feat in ["number_of_bedrooms", "number_of_bathrooms", "number_of_guests",
             "number_of_reviews", "star_rating", "cleaning_fee", "min_nights"]:
    sub = m[m[feat].notna()]
    if sub[feat].nunique() < 2:
        rows.append({"característica": feat, "diária": "n/d (sem variação)",
                     "receita_base": "n/d"})
        continue
    r1 = sub[feat].rank().corr(sub["diaria_mediana"].rank())
    r2 = sub[feat].rank().corr(sub["receita_anual_base"].rank())
    rows.append({"característica": feat,
                 "diária": f"{r1:+.3f}",
                 "receita_base": f"{r2:+.3f}"})
L.append(pd.DataFrame(rows).to_string(index=False) + "\n")

L.append("\n**Leitura:** valores positivos indicam que imóveis com mais daquela característica "
         "têm, em média, diária/receita maiores (associação). Não implica causalidade.\n")

L.append("\n**Diária mediana por tipo de superhost:**")
sup = m.groupby("is_superhost")["diaria_mediana"].median().round(0)
L.append(sup.to_string() + "\n")

L.append("\n**Diária mediana por tipo de imóvel:**")
L.append(m.groupby("listing_type")["diaria_mediana"].median().round(0).to_string() + "\n")

L.append("\n**Diária mediana por nº de quartos:**")
L.append(m.groupby("number_of_bedrooms")["diaria_mediana"].median().round(0).to_string() + "\n")

content = "\n".join(L)
with open(os.path.join(OUT, "features_report.md"), "w", encoding="utf-8") as f:
    f.write(content)
print("features_report.md gerado. n =", len(m))