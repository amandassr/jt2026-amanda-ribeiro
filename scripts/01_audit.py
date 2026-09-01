#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Etapa 1 — Auditoria, limpeza e organização dos dados
Hackathon Jovens Talentos AI Builder 2026 (Seazone) — Itapema (SC)

Reproduz de forma determinística todos os números de inspeção estrutural do BRIEF.md.
Não faz ranking nem escolhe recomendação. Gera output/audit_report.md.
"""
import os
import pandas as pd
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "output")
os.makedirs(OUT, exist_ok=True)

REPORT = []
def log(line=""):
    REPORT.append(line)

def header(t, level=2):
    log(f"\n{'#'*level} {t}\n")

def table(df):
    log(df.to_string() + "\n")

def num(x):
    try:
        return f"{x:,}".replace(",", ".")
    except (TypeError, ValueError):
        return str(x)

def load(name):
    return pd.read_csv(os.path.join(DATA, name), low_memory=False)

# ---------------------------------------------------------------------------
# 1. Estrutura
# ---------------------------------------------------------------------------
header("1. Estrutura das bases", 1)
FILES = [
    ("Details_Itapema.csv", "airbnb_listing_id"),
    ("Hosts_ids_Itapema.csv", "owner_id"),
    ("Mesh_Ids_Data_Itapema.csv", "airbnb_listing_id"),
    ("Price_AV_Itapema.csv", "airbnb_listing_id"),
    ("VivaReal_Itapema.csv", "listing_id"),
]
FRAMES = {}
rows = []
for name, key in FILES:
    df = load(name)
    FRAMES[name] = df
    rows.append({"arquivo": name, "linhas": f"{len(df):,}", "colunas": df.shape[1], "chave": key})
table(pd.DataFrame(rows))

# ---------------------------------------------------------------------------
# 2. Dados ausentes por coluna
# ---------------------------------------------------------------------------
header("2. Dados ausentes por coluna", 1)
for name, _ in FILES:
    df = FRAMES[name]
    header(f"2.{list(FRAMES).index(name)+1} {name}")
    miss = df.isna().sum()
    pc = (miss / len(df) * 100).round(1)
    m = pd.DataFrame({"coluna": miss.index, "ausentes": miss.values,
                      "%": pc.values})[miss.values > 0]
    if len(m) == 0:
        log("* Sem campos vazios.\n")
    else:
        table(m)

# ---------------------------------------------------------------------------
# 3. Duplicidades de chave
# ---------------------------------------------------------------------------
header("3. Duplicidades de chave", 1)

# 3.1 Details
det = FRAMES["Details_Itapema.csv"]
log(f"**Details:** duplicatas em `airbnb_listing_id`: {det.duplicated('airbnb_listing_id').sum()} "
    f"| ids únicos: {det.airbnb_listing_id.nunique()} / {len(det)}")

# 3.2 Mesh
mesh = FRAMES["Mesh_Ids_Data_Itapema.csv"]
log(f"**Mesh:** duplicatas em `airbnb_listing_id`: {mesh.duplicated('airbnb_listing_id').sum()} "
    f"| ids únicos: {mesh.airbnb_listing_id.nunique()} / {len(mesh)}")

# 3.3 Price: pares (listing, date)
price = FRAMES["Price_AV_Itapema.csv"]
price["price"] = pd.to_numeric(price.price, errors="coerce")
price["date"] = pd.to_datetime(price.date, errors="coerce")
price["aq"] = pd.to_datetime(price.aquisition_date, errors="coerce")
price_ids = set(price.airbnb_listing_id.unique())
dup_rows = price.duplicated(["airbnb_listing_id", "date"], keep=False).sum()
dup_pairs = price[price.duplicated(["airbnb_listing_id", "date"], keep=False)].groupby(
    ["airbnb_listing_id", "date"]).ngroups
mult_cap = price[price.duplicated(["airbnb_listing_id", "date"], keep=False)].groupby(
    ["airbnb_listing_id", "date"]).aq.nunique().value_counts().sort_index().to_dict()
log(f"**Price:** linhas duplicadas `(listing,date)`: {num(dup_rows)} | pares afetados: {num(dup_pairs)}")
log(f"  Nº de capturas distintas dentro de cada par duplicado: {mult_cap}")
log(f"  Listings únicos no Price: {len(price_ids)}")

# 3.4 Hosts
host = FRAMES["Hosts_ids_Itapema.csv"]
h_dup = host.duplicated("owner_id").sum()
h_dup_all = host.duplicated("owner_id", keep=False).sum()
h_uid = host.owner_id.nunique()
log(f"**Hosts:** duplicatas em `owner_id`: {num(h_dup)} linhas (repetições) | "
    f"linhas em chaves repetidas: {num(h_dup_all)} | donos únicos: {num(h_uid)} / {len(host)}")

# o que distingue as linhas repetidas do mesmo dono?
duph = host[host.owner_id.duplicated(keep=False)]
if len(duph) > 0:
    g = duph.groupby("owner_id")
    snap_nunique = g.host_snapshot_date.nunique().value_counts().sort_index().to_dict()
    log(f"  Das {num(len(duph))} linhas com chave repetida: nº de `host_snapshot_date` distintas por dono: {snap_nunique}")
    # are the repeated rows exact duplicates?
    cols = [c for c in host.columns if c != "owner_id"]
    exact_dup = duph.duplicated(subset=cols).sum()
    log(f"  Linhas repetidas que são IDÊNTICAS em todas as outras colunas: {num(exact_dup)} "
        f"| que DIFEREM em ao menos uma coluna: {num(len(duph) - exact_dup)}")

# 3.5 VivaReal
vv = FRAMES["VivaReal_Itapema.csv"]
log(f"**VivaReal:** duplicatas em `listing_id`: {vv.duplicated('listing_id').sum()} "
    f"| ids únicos: {vv.listing_id.nunique()} / {len(vv)}")

# ---------------------------------------------------------------------------
# 4. Chaves e relações entre bases
# ---------------------------------------------------------------------------
header("4. Chaves e relações entre bases", 1)
det_ids = set(det.airbnb_listing_id.unique())
mesh_ids = set(mesh.airbnb_listing_id.unique())
log(f"**Details ↔ Mesh:** todos os ids do Mesh existem no Details? "
    f"{mesh_ids <= det_ids}; todos do Details no Mesh? {det_ids <= mesh_ids} "
    f"| (Diferença: {len(mesh_ids ^ det_ids)})")

price_out = sorted(price_ids - det_ids)
with_price = det_ids & price_ids
log(f"**Price ↔ Details:** listings do Price fora do Details: {len(price_out)} -> {price_out}")
log(f"  Listings com pelo menos um preço: {len(with_price)} | sem preço: {len(det_ids - price_ids)}")

det_ow = set(pd.to_numeric(det.owner_id.dropna(), errors="coerce").astype("int64"))
host_ow = set(pd.to_numeric(host.owner_id.dropna(), errors="coerce").astype("int64"))
log(f"**Details ↔ Hosts:** owner_ids do Details existentes no Hosts: "
    f"{len(det_ow & host_ow)} / {len(det_ow)}")

common = set(det.columns) & set(vv.columns)
log(f"**VivaReal ↔ Airbnb:** colunas em comum: {sorted(common)} "
    f"| NÃO há coluna de id comum -> sem ligação direta confiável.")

# ---------------------------------------------------------------------------
# 5. Períodos das datas
# ---------------------------------------------------------------------------
header("5. Períodos das datas", 1)
per = []
date_cols = {
    "Details_Itapema.csv": "aquisition_date",
    "Hosts_ids_Itapema.csv": "host_snapshot_date",
    "Mesh_Ids_Data_Itapema.csv": "aquisition_date",
    "Price_AV_Itapema.csv": "aquisition_date",
    "VivaReal_Itapema.csv": "aquisition_date",
}
for name in date_cols:
    df = FRAMES[name]
    dt = pd.to_datetime(df[date_cols[name]], errors="coerce")
    per.append({"base": name, "coluna": date_cols[name],
                "min": dt.min(), "max": dt.max(), "qtde distinta": dt.nunique()})
table(pd.DataFrame(per))

pp = price.drop_duplicates(["airbnb_listing_id", "date"], keep="last")
log(f"**Price (datas de estadia):** {pp.date.min().date()} até {pp.date.max().date()} "
    f"| datas únicas: {pp.date.nunique()} | listings: {pp.airbnb_listing_id.nunique()}")
log(f"  Nº de datas distintas por listing (janela): min {pp.groupby('airbnb_listing_id').date.nunique().min()}, "
    f"média {pp.groupby('airbnb_listing_id').date.nunique().mean():.0f}, "
    f"máx {pp.groupby('airbnb_listing_id').date.nunique().max()}")

# ---------------------------------------------------------------------------
# 6. Cobertura de preço (bairro / tipo / quartos)
# ---------------------------------------------------------------------------
header("6. Cobertura de preço por bairro, tipo e quartos", 1)
base = mesh[["airbnb_listing_id", "suburb"]].merge(
    det[["airbnb_listing_id", "listing_type", "number_of_bedrooms"]],
    on="airbnb_listing_id", how="left")
base["has_price"] = base.airbnb_listing_id.isin(price_ids)
base["suburb"] = base.suburb.replace("none", np.nan)
log(f"Imóveis com preço: {int(base['has_price'].sum())} de {len(base)} "
    f"({round(base['has_price'].mean()*100,1)}%)")

def cov(g):
    out = base.groupby(g).agg(total=("airbnb_listing_id", "size"),
                              com_preco=("has_price", "sum"),
                              pct=("has_price", "mean")).sort_values("total", ascending=False)
    out["pct"] = (out["pct"] * 100).round(1)
    return out

header("6.1 Por bairro", 3)
table(cov("suburb"))
header("6.2 Por tipo de imóvel", 3)
table(cov("listing_type"))
header("6.3 Por nº de quartos", 3)
table(cov("number_of_bedrooms"))

# ---------------------------------------------------------------------------
# 7. Tratamento de múltiplas capturas (regra "última captura") + robustez
# ---------------------------------------------------------------------------
header("7. Regra de captura para Price_AV", 1)
log("Regra primária mantida para cada `(listing, date)`: captura mais recente "
    "(`aquisition_date` máxima). Abaixo, a comparação de robustez entre regras.")

def listing_mean(col, rule):
    if rule == "latest":
        pp_ = price.sort_values("aq").drop_duplicates(["airbnb_listing_id", "date"], keep="last")
    elif rule == "earliest":
        pp_ = price.sort_values("aq").drop_duplicates(["airbnb_listing_id", "date"], keep="first")
    elif rule == "mean":
        pp_ = price.groupby(["airbnb_listing_id", "date"], as_index=False)["price"].mean()
    else:
        pp_ = price.groupby(["airbnb_listing_id", "date"], as_index=False)["price"].median()
    return pp_.groupby("airbnb_listing_id", as_index=False)["price"].mean().rename(columns={"price": col})

m = (listing_mean("latest", "latest")
     .merge(listing_mean("earliest", "earliest"), on="airbnb_listing_id")
     .merge(listing_mean("mean", "mean"), on="airbnb_listing_id")
     .merge(listing_mean("median", "median"), on="airbnb_listing_id"))

def spearman(x, y):
    return x.rank().corr(y.rank())

log(f"n = {len(m)} imóveis com preço")
log(f"- Correlação de ranks: 'última' vs 'primeira' = {spearman(m['latest'], m['earliest']):.4f} | "
    f"'última' vs 'média' = {spearman(m['latest'], m['mean']):.4f} | "
    f"'primeira' vs 'média' = {spearman(m['earliest'], m['mean']):.4f}")
rel = ((m["latest"] - m["earliest"]).abs() / m["earliest"] * 100)
log(f"- Diferença % média ('última' vs 'primeira'): {rel.mean():.2f} | "
    f">5%: {round((rel>5).mean()*100,1)}% | >20%: {round((rel>20).mean()*100,1)}%")

# ---------------------------------------------------------------------------
# 8. Indício de sazonalidade + validação com painel balanceado
# ---------------------------------------------------------------------------
header("8. Indício de sazonalidade (a validar) e painel balanceado", 1)
pr = price.sort_values("aq").drop_duplicates(["airbnb_listing_id", "date"], keep="last")[["airbnb_listing_id", "date", "price"]]
pr["month"] = pr["date"].dt.month
mon_all = pr.groupby("month")["price"].mean().round(1)
log("Preço médio mensal (todos os imóveis observados):")
table(mon_all.reset_index().rename(columns={"month": "mês", "price": "preço médio"}))

# painel balanceado: imóveis presentes em todos os 4 meses
months = {1, 2, 3, 4}
present = pr.groupby("airbnb_listing_id")["month"].apply(lambda s: tuple(sorted(set(s))))
bal = [lid for lid, mm in present.items() if set(mm) == months]
log(f"Imóveis observados em TODOS os 4 meses (painel balanceado): {len(bal)}")
if bal:
    pbal = pr[pr.airbnb_listing_id.isin(bal)]
    log("Preço médio mensal RESTRITO ao painel balanceado:")
    table(pbal.groupby("month")["price"].mean().round(1).reset_index().rename(
        columns={"month": "mês", "price": "preço médio (painel balanceado)"}))
log("> Interpretação: se a queda persistir no painel balanceado, é mais provável sazonalidade; "
    "se sumir, era efeito de composição (troca de amostra entre meses).")

# ---------------------------------------------------------------------------
# 9. Distribuição dos grupos e limites de amostra
# ---------------------------------------------------------------------------
header("9. Distribuição dos grupos (bairro|tipo|quartos) e limites de amostra", 1)
base["grp"] = base["suburb"].fillna("(sem bairro)") + "|" + base.listing_type + "|" + base.number_of_bedrooms.astype("Int64").astype(str)
g = base.groupby("grp")["has_price"].sum().rename("n_price")
log(f"Grupos no Airbnb: {len(base['grp'].unique())} | imóveis com preço total: {int(g.sum())}")
rows = []
for t in [5, 10, 15, 20, 30]:
    rows.append({"corte >= n imóveis com preço": t,
                 "grupos": int((g >= t).sum()),
                 "imóveis nesses grupos": int(g[g >= t].sum())})
table(pd.DataFrame(rows))

vv2 = vv.drop_duplicates("listing_id")
vv2["grp"] = vv2["suburb"].fillna("(sem bairro)") + "|" + vv2["listing_type"] + "|" + vv2.bedrooms.astype("Int64").astype(str)
vg = vv2.groupby("grp").size().rename("n")
vrows = []
for t in [3, 5, 10, 20, 30]:
    vrows.append({"corte >= n anúncios": t, "grupos": int((vg >= t).sum()),
                  "anúncios": int(vg[vg >= t].sum())})
table(pd.DataFrame(vrows))
log(f"Grupos no VivaReal (dedup): {len(vg)}")

# ---------------------------------------------------------------------------
# 10. Qualidade após the latest-capture rule
# ---------------------------------------------------------------------------
header("10. Qualidade do Price após regra 'última captura'", 1)
pp2 = price.sort_values("aq").drop_duplicates(["airbnb_listing_id", "date"], keep="last")
pp2["price"] = pd.to_numeric(pp2.price, errors="coerce")
log(f"Linhas: {num(len(pp2))} | listings: {pp2.airbnb_listing_id.nunique()} | datas: {pp2.date.nunique()}")
log(f"Preço: min {pp2.price.min()} | p1 {pp2.price.quantile(.01):.0f} | mediana {pp2.price.median()} | "
    f"p99 {pp2.price.quantile(.99):.0f} | max {pp2.price.max()}")
log(f"Preço <=0: {int((pp2.price<=0).sum())} | >3000: {int((pp2.price>3000).sum())} | "
    f">5000: {int((pp2.price>5000).sum())}")
lst = pp2.sort_values("date")
lst["lmed"] = lst.groupby("airbnb_listing_id")["price"].transform("median")
lst["ratio"] = lst["price"] / lst["lmed"].replace(0, np.nan)
log(f"Preços >5x a mediana do próprio imóvel: {int((lst.ratio>5).sum())}")
nd = pp2.groupby("airbnb_listing_id").date.nunique()
log(f"Datas distintas por listing: min {nd.min()} | mediana {nd.median()} | max {nd.max()}")
log(f"Listings com <15 datas: {int((nd<15).sum())} | <30: {int((nd<30).sum())}")

# ---------------------------------------------------------------------------
# 11. Qualidade VivaReal
# ---------------------------------------------------------------------------
header("11. Qualidade do VivaReal", 1)
log(f"Linhas: {len(vv)} | duplicatas listing_id: {vv.duplicated('listing_id').sum()} | "
    f"suburb ausente: {int(vv.suburb.isna().sum())}")
log(f"sale_price ausente: {int(vv.sale_price.isna().sum())} | <=0: {int((vv.sale_price<=0).sum())}")
log(f"usable_area <=0: {int((vv.usable_area<=0).sum())}")
log("sale_price percentis:")
table(pd.DataFrame({"percentil": vv.sale_price.quantile([0, .01, .05, .5, .95, .99, 1]).index,
                    "sale_price": vv.sale_price.quantile([0, .01, .05, .5, .95, .99, 1]).round(0).values}))
log(f"listing_type: {sorted(vv.listing_type.dropna().unique())}")
log(f"property_type: {sorted(vv.property_type.dropna().unique())}")

# ---------------------------------------------------------------------------
# 12. Bairros: despadronização (lista para o mapa de normalização)
# ---------------------------------------------------------------------------
header("12. Bairros — divergências de grafia (para mapa de normalização)", 1)
log("Valores no Mesh (Airbnb):")
log(", ".join(sorted(mesh.suburb.replace("none", np.nan).dropna().unique())))
log("\nValores no VivaReal: ")
log(", ".join(sorted(vv.suburb.dropna().unique())))

# ---------------------------------------------------------------------------
# Escrita do relatório
# ---------------------------------------------------------------------------
report_md = "\n".join(REPORT)
with open(os.path.join(OUT, "audit_report.md"), "w", encoding="utf-8") as f:
    f.write("# Relatório de Auditoria — Etapa 1\n")
    f.write("**Gerado por:** `scripts/01_audit.py`\n**Data:** " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M") + "\n\n---\n")
    f.write(report_md + "\n")
print(f"Relatório escrito em output/audit_report.md ({len(REPORT)} linhas)")
print("RESUMO:")
print(f"  Linhas: Details {len(det)} | Hosts {len(host)} | Mesh {len(mesh)} | Price {num(len(price))} | VivaReal {num(len(vv))}")
print(f"  Com preço: {int(base['has_price'].sum())} / {len(base)}")
print(f"  Duplicatas: VivaReal {vv.duplicated('listing_id').sum()} | Hosts (owner) {num(h_dup)} | Price pares {num(dup_pairs)}")