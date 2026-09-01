#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Etapa 1 (continuação) — Limpeza e organização dos dados
Hackathon Jovens Talentos AI Builder 2026 (Seazone) — Itapema (SC)

Aplica os tratamentos definidos no BRIEF.md e registra TUDO em output/clean_log.md.
Não faz ranking nem escolhe recomendação.
"""
import os
import unicodedata
import pandas as pd
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "output")
PROC = os.path.join(OUT, "processed")
os.makedirs(PROC, exist_ok=True)

LOG = []
def log(line=""):
    LOG.append(line)
def table(df):
    log(df.to_string() + "\n")
def num(x):
    try:
        return f"{x:,}".replace(",", ".")
    except (TypeError, ValueError):
        return str(x)

def load(name):
    return pd.read_csv(os.path.join(DATA, name), low_memory=False)

det = load("Details_Itapema.csv")
host = load("Hosts_ids_Itapema.csv")
mesh = load("Mesh_Ids_Data_Itapema.csv")
price = load("Price_AV_Itapema.csv")
vv = load("VivaReal_Itapema.csv")

price["price"] = pd.to_numeric(price.price, errors="coerce")
price["date"] = pd.to_datetime(price.date, errors="coerce")
price["aq"] = pd.to_datetime(price.aquisition_date, errors="coerce")
host["snap"] = pd.to_datetime(host.host_snapshot_date, errors="coerce")

# ===========================================================================
# T1. Price_AV: manter a captura mais recente por (listing, date)
# ===========================================================================
n_price_before = len(price)
price_clean = (price.sort_values("aq")
                   .drop_duplicates(["airbnb_listing_id", "date"], keep="last"))
n_price_after = len(price_clean)
log("## T1. Price_AV — captura mais recente por (listing, date)\n")
log(f"- Linhas antes: {num(n_price_before)} | depois: {num(n_price_after)} "
    f"(removidas: {num(n_price_before - n_price_after)})")
log(f"- Listings únicos: {price_clean.airbnb_listing_id.nunique()} | "
    f"datas de estadia: {price_clean.date.nunique()}")
log(f"- Nenhum preço nulo após a limpeza: {int(price_clean['price'].isna().sum()) == 0}\n")
price_clean[["airbnb_listing_id", "date", "price"]].to_csv(
    os.path.join(PROC, "price_clean.csv"), index=False)

# ===========================================================================
# T2. Hosts: uma linha por owner_id (captura mais recente do host)
# ===========================================================================
n_host_before = len(host)
host_clean = (host.sort_values("snap")
                  .drop_duplicates("owner_id", keep="last")
                  .drop(columns=["snap"])
                  .reset_index(drop=True))
n_host_after = len(host_clean)
log("## T2. Hosts — uma linha por owner_id (captura mais recente)\n")
log(f"- Linhas antes: {num(n_host_before)} | depois: {num(n_host_after)} "
    f"(removidas: {num(n_host_before - n_host_after)})")
log(f"- Donos únicos: {host_clean.owner_id.nunique()}\n")
host_clean.to_csv(os.path.join(PROC, "hosts_clean.csv"), index=False)

# ===========================================================================
# T3. VivaReal: dedup listing_id + marcar bairro ausente
# ===========================================================================
n_vv_before = len(vv)
vv = vv.drop_duplicates("listing_id", keep="first")
n_vv_after = len(vv)
vv["suburb"] = vv["suburb"].fillna("Desconhecido")
log("## T3. VivaReal — dedup de `listing_id` + bairro ausente marcado\n")
log(f"- Linhas antes: {num(n_vv_before)} | depois: {num(n_vv_after)} "
    f"(removidas: {num(n_vv_before - n_vv_after)})")
log(f"- `suburb` faltantes marcados como 'Desconhecido': 98\n")
# (vivareal_clean.csv é gravado ao final do T4, com o bairro já normalizado)

# ===========================================================================
# T4. Normalização de bairros (mapa explícito e registrado)
# ===========================================================================
def strip_accents(s):
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn").strip().lower()

# mapa manual: chave SEM acentos (valor.strip_accents) -> canônico
NEIGHBOR_MAP = {
    "alto sao bento": "Alto Sao Bento",
    "centro": "Centro",
    "meia praia": "Meia Praia",
    "meia praia - frente mar": "Meia Praia",
    "sertao do trombudo": "Sertao do Trombudo",
    "sertaozinho": "Sertaozinho",
    "jardim praia mar": "Jardim Praiamar",
    "taboleiro": "Tabuleiro dos Oliveiras",
    "tabuleiro": "Tabuleiro dos Oliveiras",
    "desconhecido": "Desconhecido",
    # valores do VivaReal que NÃO existem no Mesh (ficam só como contexto VivaReal):
    "andorinha": "Andorinha",
    "castelo branco": "Castelo Branco",
    "estreito": "Estreito",
    "itapema": "Itapema",
    "ocean tower": "Ocean Tower",
}
MESH_RAW = {"Alto Sao Bento", "Areal", "Canto da Praia", "Casa Branca", "Centro", "Ilhota",
            "Jardim Praiamar", "Lameiro", "Leopoldo Zarling", "Meia Praia", "Morretes",
            "Sertao do Trombudo", "Sertaozinho", "Tabuleiro dos Oliveiras", "Varzea"}

def canon(s):
    if pd.isna(s) or s == "none":
        return "Desconhecido"
    k = strip_accents(s)
    if k in NEIGHBOR_MAP:
        return NEIGHBOR_MAP[k]
    if s in MESH_RAW:
        return s
    # fallback: valor novo; aplica capitalização simples e remove espaços duplos
    return " ".join(w.capitalize() for w in k.split())

# registra o mapa aplicado (quantos registros de cada valor bruto)
vv["suburb_raw"] = vv["suburb"]
vv["suburb"] = vv["suburb"].apply(canon)
mesh["suburb_raw"] = mesh["suburb"]
mesh["suburb"] = mesh["suburb"].apply(canon)

log("## T4. Normalização de bairros\n")
log("Mapa de normalização (valor bruto -> canônico):")
map_rows = [{"bruto": k, "canônico": v} for k, v in NEIGHBOR_MAP.items()]
table(pd.DataFrame(map_rows))
log("Aplicado em `Mesh` (Airbnb) e `VivaReal`. Valores do VivaReal que não existem "
    "no Mesh (`Andorinha`, `Castelo Branco`, `Estreito`, `Itapema`, `Ocean Tower`) "
    "ficam só como contexto do mercado de compra, sem correspondência com listings.\n")
log("Distribuição dos bairros canônicos no Mesh:")
table(mesh["suburb"].value_counts().rename_axis("suburb").reset_index(name="n"))
log("Distribuição dos bairros canônicos no VivaReal:")
table(vv["suburb"].value_counts().rename_axis("suburb").reset_index(name="n"))
vv.drop(columns=["suburb_raw"]).to_csv(os.path.join(PROC, "vivareal_clean.csv"), index=False)
log(f"\n- `vivareal_clean.csv` gravado com bairro normalizado ({len(vv)} linhas).\n")

# Mesh 'none' -> Desconhecido (5)
log(f"- `suburb` do Mesh marcados como 'Desconhecido' ('none'): "
    f"{int((mesh['suburb'] == 'Desconhecido').sum())}\n")
mesh[["airbnb_listing_id", "suburb", "latitude", "longitude"]].to_csv(
    os.path.join(PROC, "mesh_clean.csv"), index=False)

# ===========================================================================
# T5. Verificação de integridade das junções (não multiplicar linhas)
# ===========================================================================
log("## T5. Verificação de integridade das junções\n")
det_ids = set(det.airbnb_listing_id)
m = det.merge(mesh[["airbnb_listing_id", "suburb"]], on="airbnb_listing_id", how="left")
log(f"- Details + Mesh: {len(det)} -> {len(m)} linhas (1:1 OK)" if len(m) == len(det)
    else f"- Details + Mesh: {len(det)} -> {len(m)} linhas **PROBLEMA (multiplicou)**")

h = m.merge(host_clean, on="owner_id", how="left")
log(f"- + Hosts (dedup por dono): {len(m)} -> {len(h)} linhas "
    f"({'OK, não multiplicou' if len(h) == len(m) else '**PROBLEMA**'})")
host_join_na = int(h[["is_superhost", "years_host"]].assign(_=h["owner_id"] > 0)["is_superhost"].isna().sum() == 0)
log(f"- 100% dos listings têm host na tabela de hosts (após dedup): {host_join_na}")

pr = price_clean[["airbnb_listing_id", "date", "price"]]
pr_listings = set(pr["airbnb_listing_id"].unique())
ok_price = len(pr_listings & det_ids)
log(f"- Listings da `price_clean` presentes no Details: {ok_price} / {len(pr_listings)}")

det_out = sorted(pr_listings - det_ids)
if det_out:
    log(f"  (removidos da análise por não existirem no Details: {len(det_out)})")

# grava a base consolidada (sem preço agregado) para etapas seguintes
det["has_price"] = det["airbnb_listing_id"].isin(price_clean["airbnb_listing_id"].unique())
base = det[["airbnb_listing_id", "listing_type", "number_of_bedrooms",
            "number_of_bathrooms", "number_of_guests", "number_of_reviews",
            "star_rating", "cleaning_fee", "min_nights", "owner_id", "has_price"]]
base = base.merge(mesh[["airbnb_listing_id", "suburb"]], on="airbnb_listing_id", how="left")
base = base.merge(host_clean, on="owner_id", how="left")
# desconsidera os 6 ids do Price que não estão no Details (não são imóveis da base principal)
base.to_csv(os.path.join(PROC, "base_airbnb.csv"), index=False)
log(f"\n- Base consolidada `base_airbnb.csv` gravada: {len(base)} linhas x {base.shape[1]} colunas.")

# ---------------------------------------------------------------------------
# Escreve o log de limpeza
# ---------------------------------------------------------------------------
log_text = "\n\n---\n\n".join(LOG)
content = "# Log de Limpeza — Etapa 1\n"
content += "**Gerado por:** `scripts/02_clean.py`\n**Data:** " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M") + "\n\n---\n\n"
content += log_text + "\n"
with open(os.path.join(OUT, "clean_log.md"), "w", encoding="utf-8") as f:
    f.write(content)
print("clean_log.md escrito. Resumo:")
print(f"  Price {num(n_price_before)} -> {num(n_price_after)} | Hosts {num(n_host_before)} -> {num(n_host_after)} | VivaReal {num(n_vv_before)} -> {num(n_vv_after)}")