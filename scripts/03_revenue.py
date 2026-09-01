#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Etapa 2 — Estimativa de receita potencial
Hackathon Jovens Talentos AI Builder 2026 (Seazone) — Itapema (SC)

Método (conforme BRIEF.md):
- Diária representativa por imóvel = MEDIANA das noites observadas (robusta a outliers)
  cada imóvel conta como UM valor (sem peso extra p/ quem tem mais datas).
- Sazonalidade mensal: para jan-abr (meses observados) usa-se a mediana REAL do mês;
  para mai-dez (não observados) aplica-se um FATOR de sazonalidade, que é SUPOSIÇÃO declarada.
- Receita anual por imóvel = soma de (diária_m x ocupação_m x dias_do_mês) nos 12 meses.
- 3 cenários (conservador/base/otimista) com premissas explícitas.
- NÃO faz ranking nem escolhe recomendação.
"""
import os
import calendar
import pandas as pd
import numpy as np

from config import OCCUPANCY, SEASON_OUT, OBSERVED_MONTHS, DAYS, PREMSA_MOTIVACAO

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(ROOT, "output", "processed")
OUT = os.path.join(ROOT, "output")
os.makedirs(PROC, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

REPORT = []
def log(line=""):
    REPORT.append(line)
def table(df):
    log(df.to_string() + "\n")
def num(x):
    try:
        return f"{x:,.0f}".replace(",", ".")
    except (TypeError, ValueError):
        return str(x)

# ---------------------------------------------------------------------------
# Carrega dados limpos
# ---------------------------------------------------------------------------
price = pd.read_csv(os.path.join(PROC, "price_clean.csv"))
base = pd.read_csv(os.path.join(PROC, "base_airbnb.csv"))
price["date"] = pd.to_datetime(price.date)
price["price"] = pd.to_numeric(price.price, errors="coerce")
price["month"] = price.date.dt.month

# ---------------------------------------------------------------------------
# Premissas dos cenários — ver config.py (CENÁRIOS ILUSTRATIVOS, não fatos)
# ---------------------------------------------------------------------------
price["date"] = pd.to_datetime(price.date)
rep = price.groupby("airbnb_listing_id")["price"].median().rename("diaria_mediana")
n_obs = price.groupby("airbnb_listing_id")["date"].nunique().rename("ndatas")
# mediana por mês observado (jan-abr), por imóvel — para usar o preço REAL do mês
month_med = price.groupby(["airbnb_listing_id", "month"])["price"].median().unstack(fill_value=np.nan)

df = pd.DataFrame({"diaria_mediana": rep, "ndatas": n_obs})
df = df.join(month_med.rename(columns={m: f"diaria_m{m}" for m in OBSERVED_MONTHS}))

# Exclui os 6 imóveis do Price que NÃO existem no Details (registrado na auditoria):
# sem bairro/tipo/quartos, não podem entrar em qualquer comparação de grupos.
det_ids = set(base["airbnb_listing_id"].unique())
ids_fora = sorted(set(df.index) - det_ids)
df = df.loc[list(det_ids & set(df.index))]

# ---------------------------------------------------------------------------
# Receita anual por cenário
# ---------------------------------------------------------------------------
for cen in OCCUPANCY:
    rev = []
    for lid, r in df.iterrows():
        annual = 0.0
        for m in range(1, 13):
            occ = OCCUPANCY[cen][m]
            if m in OBSERVED_MONTHS:
                # preço REAL do mês (se observado), senão cai para a mediana geral
                d = r[f"diaria_m{m}"]
                if pd.isna(d):
                    d = r["diaria_mediana"]
            else:
                # meses não observados: diária representativa x fator de sazonalidade
                d = r["diaria_mediana"] * SEASON_OUT[cen]
            annual += d * occ * DAYS[m]
        rev.append(annual)
    df[f"receita_anual_{cen}"] = rev

df = df.reset_index()
df = df.merge(base[["airbnb_listing_id", "listing_type", "number_of_bedrooms", "suburb"]],
              on="airbnb_listing_id", how="left")

# ---------------------------------------------------------------------------
# Relatório
# ---------------------------------------------------------------------------
log("# Relatório — Etapa 2: Estimativa de receita potencial\n")
log("**Gerado por:** `scripts/03_revenue.py`\n\n---\n")

log("## 1. Premissas dos cenários (SUPOSIÇÕES, não fatos)\n")
log(PREMSA_MOTIVACAO + "\n")
log("**Ocupação mensal (fração dos dias do mês ocupados)**")
occ_tab = pd.DataFrame({cen: [f"{OCCUPANCY[cen][m]:.0%}" for m in range(1, 13)] for cen in OCCUPANCY},
                       index=[f"{calendar.month_abbr[m]} ({DAYS[m]}d)" for m in range(1, 13)])
table(occ_tab)
log("**Fator de sazonalidade p/ meses não observados (mai–dez):** "
    f"conservador {SEASON_OUT['conservador']}, base {SEASON_OUT['base']}, otimista {SEASON_OUT['otimista']}")
log("- jan–abr: usa a **mediana real** do preço de cada mês (dado observado).")
log("- mai–dez: diária representativa × fator de sazonalidade (**suposição declarada**, "
    "edite em `scripts/config.py`).")
log("- Estes valores foram escolhidos como referências e **serão testados por sensibilidade** "
    "(o resultado por imóvel pode mudar; o ranking comparativo de grupos tende a ser mais estável).\n")

log("## 2. Diária representativa por imóvel (mediana das noites observadas)\n")
log(f"- Imóveis com preço **e presentes no Details (base de análise)**: {num(len(df))}")
log(f"  (removidos {len(ids_fora)} imóveis sem bairro/tipo/quartos por não constarem no Details)")
log(f"- Diária mediana (imóvel): p25 {df['diaria_mediana'].quantile(.25):.0f} | "
    f"p50 {df['diaria_mediana'].median():.0f} | p75 {df['diaria_mediana'].quantile(.75):.0f}")
log(f"- Noites observadas por imóvel: min {df['ndatas'].min()}, mediana {df['ndatas'].median():.0f}, "
    f"máx {df['ndatas'].max()}\n")

log("## 3. Receita anual estimada por cenário (distribuição por imóvel)\n")
cols = ["receita_anual_conservador", "receita_anual_base", "receita_anual_otimista"]
agg = df[cols].describe(percentiles=[.25, .5, .75]).T[["mean", "25%", "50%", "75%","max"]]
agg.columns = ["média", "p25", "p50 (mediana)", "p75", "máx"]
table(agg.round(0))

log("## 4. Receita por grupo (bairro | tipo | quartos) — cenário BASE\n")
log("(Apenas descrição da distribuição; **sem ranking**.)")
grp = df.groupby("grp" if "grp" in df.columns else
                 (df["suburb"].fillna("(sem bairro)") + "|" + df["listing_type"] + "|" +
                  df["number_of_bedrooms"].fillna(0).astype(int).astype(str)))
g = grp.agg(n=("airbnb_listing_id", "size"),
            rec_base_p50=("receita_anual_base", "median"),
            rec_base_p75=("receita_anual_base", lambda s: s.quantile(.75)),
            diaria_p50=("diaria_mediana", "median"))
g = g[g["n"] >= 10]  # corte padrão de amostra mínima só para apresentação
g = g.sort_values("n", ascending=False)
g["rec_base_p50"] = g["rec_base_p50"].round(0)
g["rec_base_p75"] = g["rec_base_p75"].round(0)
g["diaria_p50"] = g["diaria_p50"].round(0)
log(f"Grupos com n>=10 imóveis com preço: {len(g)}")
table(g.head(30))

# sanity: % imóveis que são "outliers" de diária
log("\n## 5. Sanity check (diária)\n")
hi = df["diaria_mediana"] > df["diaria_mediana"].quantile(.99)
log(f"- Imóveis com diária mediana acima do p99: {int(hi.sum())} — mantidos para análise; "
    f"são relevantes avaliar seu impacto.")
log(f"- Imóveis com <15 noites observadas: {int((df['ndatas']<15).sum())} — receita menos confiável; "
    f"serão identificados nas comparações.")

# ---------------------------------------------------------------------------
# Gravação
# ---------------------------------------------------------------------------
df.to_csv(os.path.join(PROC, "revenue_per_imovel.csv"), index=False)
content = "# ".join(["", "#"])
with open(os.path.join(OUT, "revenue_report.md"), "w", encoding="utf-8") as f:
    f.write("\n\n".join(REPORT))
print("revenue_report.md gerado. Resumo:")
print(f"  Imóveis com preço na análise: {len(df)} (removidos {len(ids_fora)} sem Details)")
for c in cols:
    print(f"  {c}: mediana {df[c].median():,.0f} | média {df[c].mean():,.0f}")
