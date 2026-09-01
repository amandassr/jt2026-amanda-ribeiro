#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Etapa 2b — Preço de compra estimado e retorno bruto por grupo
Hackathon Jovens Talentos AI Builder 2026 (Seazone) — Itapema (SC)

Método (conforme BRIEF.md):
- Preço de compra estimado por grupo = MEDIANA do sale_price do VivaReal
  (bairro + tipo + nº de quartos, após normalização). Sempre mostra n do VivaReal.
  Grupo sem correspondência suficiente -> marcado "NÃO COMPARÁVEL" (sem aproximação silenciosa).
- Retorno bruto estimado = receita_anual_<cenário> / preço_compra_estimado, por cenário.
- Sensibilidade: cortes amostrais (5/15/20/30), regra de captura (última vs média),
  outliers (sinalizar vs remover, sempre registrados).
- Tabela de decisão + ORDENAÇÃO PRELIMINAR (não é a recomendação final).
- Testa separadamente a tese dos compactos (1 quarto) no Centro.
"""
import os
import pandas as pd
import numpy as np

from config import OCCUPANCY, SEASON_OUT, OBSERVED_MONTHS, DAYS, PREMSA_MOTIVACAO

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
PROC = os.path.join(ROOT, "output", "processed")
OUT = os.path.join(ROOT, "output")
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
# Parâmetros de amostra (definidos no BRIEF.md, seção 7)
# ---------------------------------------------------------------------------
MIN_AIRBNB = 10          # mínimo de imóveis Airbnb COM PREÇO por grupo (decisão)
MIN_VIVA = 5            # mínimo de anúncios VivaReal para estimar compra
N_AIRBNB_RAZOAVEL = 30  # >= 30 => confiança razoável (Airbnb)
N_VIVA_RAZOAVEL = 10    # >= 10 => confiança razoável (VivaReal)

# ---------------------------------------------------------------------------
# Carrega dados
# ---------------------------------------------------------------------------
rev = pd.read_csv(os.path.join(PROC, "revenue_per_imovel.csv"))
vv = pd.read_csv(os.path.join(PROC, "vivareal_clean.csv"))
price_raw = pd.read_csv(os.path.join(DATA, "Price_AV_Itapema.csv"))
price_raw["price"] = pd.to_numeric(price_raw.price, errors="coerce")
price_raw["date"] = pd.to_datetime(price_raw.date, errors="coerce")
price_raw["aq"] = pd.to_datetime(price_raw.aquisition_date, errors="coerce")

rev["number_of_bedrooms"] = rev["number_of_bedrooms"].fillna(0).astype(int)
vv["bedrooms"] = vv["bedrooms"].fillna(0).astype(int)

def grp_key(suburb, ltype, beds):
    return f"{suburb}|{ltype}|{int(beds)}"
def grp_key_series(suburb_s, ltype_s, beds_s):
    return suburb_s.astype(str) + "|" + ltype_s.astype(str) + "|" + beds_s.astype(int).astype(str)

rev["grp"] = grp_key_series(rev["suburb"], rev["listing_type"], rev["number_of_bedrooms"])
vv["grp"] = grp_key_series(vv["suburb"], vv["listing_type"], vv["bedrooms"])

# ---------------------------------------------------------------------------
# 1. Preço de compra por grupo (mediana VivaReal)
# ---------------------------------------------------------------------------
vvp = vv.groupby("grp")["sale_price"].agg(preco_compra="median", n_viva="size")

# ---------------------------------------------------------------------------
# 2. Receita e diária por grupo (Airbnb)
# ---------------------------------------------------------------------------
g = rev.groupby("grp").agg(
    n_airbnb=("airbnb_listing_id", "size"),
    diaria_p50=("diaria_mediana", "median"),
    n_datas_p50=("ndatas", "median"),
    rec_cons_p50=("receita_anual_conservador", "median"),
    rec_base_p50=("receita_anual_base", "median"),
    rec_otim_p50=("receita_anual_otimista", "median"),
)

groups = g.join(vvp, how="left")
groups = groups.reset_index().merge(
    rev[["grp", "suburb", "listing_type", "number_of_bedrooms"]].drop_duplicates(),
    on="grp", how="left")

# ---------------------------------------------------------------------------
# 3. Retorno bruto por cenário
# ---------------------------------------------------------------------------
def retorno(rec, preco):
    return np.where(pd.notna(preco) & (preco > 0), rec / preco, np.nan)

for c in ["cons", "base", "otim"]:
    col = f"rec_{c}_p50"
    groups[f"retorno_{c}"] = retorno(groups[col], groups["preco_compra"])

# marcação de comparabilidade
def status_compra(row):
    if pd.isna(row["preco_compra"]) or row["n_viva"] < MIN_VIVA:
        return "NAO_COMPARAVEL"
    if row["n_viva"] >= N_VIVA_RAZOAVEL:
        return "COMPRA_RAZOAVEL"
    return "COMPRA_BAIXA"

def status_airbnb(row):
    if row["n_airbnb"] >= N_AIRBNB_RAZOAVEL:
        return "AIRBNB_RAZOAVEL"
    if row["n_airbnb"] >= MIN_AIRBNB:
        return "AIRBNB_BAIXA"
    return "AIRBNB_AQUEM_MIMIMO"

groups["status_compra"] = groups.apply(status_compra, axis=1)
groups["status_airbnb"] = groups.apply(status_airbnb, axis=1)
groups["status_amostra"] = groups["status_airbnb"] + " / " + groups["status_compra"]

# ---------------------------------------------------------------------------
# Relatório
# ---------------------------------------------------------------------------
log("# Relatório — Etapa 2b: preço de compra e retorno bruto\n")
log("**Gerado por:** `scripts/04_return.py`\n\n---\n")
log(PREMSA_MOTIVACAO + "\n")

log("## 1. Preço de compra estimado (mediana do VivaReal por grupo)\n")
log("- Grupo = **bairro normalizado + tipo de imóvel + nº de quartos**.")
log("- Preço = mediana do `sale_price` dos anúncios de venda do mesmo grupo.")
log(f"- Amostra mínima VivaReal para estimar: **{MIN_VIVA}** anúncios. "
    f"Abaixo disso → marcado como **NÃO COMPARÁVEL** (sem aproximação silenciosa).")
log(f"- Confiança: VivaReal {MIN_VIVA}–{N_VIVA_RAZOAVEL-1} = **baixa**; ≥{N_VIVA_RAZOAVEL} = **razoável**; "
    f"Airbnb <{MIN_AIRBNB} = fora do corte de decisão; ≥{N_AIRBNB_RAZOAVEL} = razoável.\n")
log("Dimensões de cada lado (antes do join, após limpeza):")
log(f"- Grupos no Airbnb com preço: {rev['grp'].nunique()} | imóveis: {len(rev)}")
log(f"- Grupos no VivaReal: {len(vvp)} | anúncios: {len(vv)}\n")

n_nc = (groups["status_compra"] == "NAO_COMPARAVEL").sum()
log(f"Grupos no TOTAL: {len(groups)} | não comparáveis (sem VivaReal suficiente): {n_nc}\n")

# ---------------------------------------------------------------------------
# 4. Tabela de decisão (grupos elegíveis)
# ---------------------------------------------------------------------------
dec = groups[groups["n_airbnb"] >= MIN_AIRBNB].copy()
dec = dec.sort_values("retorno_base", ascending=False).reset_index(drop=True)

dec_out = dec[["suburb", "listing_type", "number_of_bedrooms",
               "n_airbnb", "n_viva", "diaria_p50", "preco_compra",
               "rec_cons_p50", "rec_base_p50", "rec_otim_p50",
               "retorno_cons", "retorno_base", "retorno_otim", "status_amostra"]].copy()
for c in ["diaria_p50", "preco_compra", "rec_cons_p50", "rec_base_p50", "rec_otim_p50"]:
    dec_out[c] = dec_out[c].round(0)
for c in ["retorno_cons", "retorno_base", "retorno_otim"]:
    dec_out[c] = (dec_out[c] * 100).round(2)

dec_out = dec_out.rename(columns={
    "suburb": "bairro", "listing_type": "tipo", "number_of_bedrooms": "quartos",
    "n_airbnb": "n_airbnb(preço)", "n_viva": "n_vivareal",
    "diaria_p50": "diaria_tipica", "preco_compra": "preco_compra_est",
    "rec_cons_p50": "receita_cons", "rec_base_p50": "receita_base", "rec_otim_p50": "receita_otim",
    "retorno_cons": "retorno_cons(%)", "retorno_base": "retorno_base(%)", "retorno_otim": "retorno_otim(%)",
    "status_amostra": "confianca"})

log("## 2. Tabela de decisão — ORDENAÇÃO PRELIMINAR (NÃO é a recomendação final)\n")
log(f"Grupos elegíveis (n_airbnb ≥ {MIN_AIRBNB} com preço): {len(dec_out)}\n")
log("Leitura: **retorno_<cenario>(%)** = receita anual estimada ÷ preço de compra estimado, por ano.")
log("Preços/receitas em R$.")
table(dec_out)

dec_out.to_csv(os.path.join(OUT, "decision_table.csv"), index=False)
groups.to_csv(os.path.join(OUT, "processed", "groups_return.csv"), index=False)
log("\n`s:output/decision_table.csv` e `output/processed/groups_return.csv` gravados.`\n")

# ---------------------------------------------------------------------------
# 5. Sensibilidade — cortes amostrais
# ---------------------------------------------------------------------------
log("## 3. Sensibilidade ao corte amostral\n")
log("Top-10 por retorno base para diferentes cortes mínimos de n_airbnb com preço "
    "(só grupos comparáveis no VivaReal). Verifica se o topo é estável ao corte.\n")

def topk(corte, k=10):
    gg = groups[(groups["n_airbnb"] >= corte) &
                (groups["status_compra"] != "NAO_COMPARAVEL")].copy()
    gg = gg.sort_values("retorno_base", ascending=False)
    return gg[["suburb", "listing_type", "number_of_bedrooms"]].head(k).apply(
        lambda r: f"{r['suburb']} {r['listing_type']} {r['number_of_bedrooms']}q", axis=1).tolist()

tops = {c: topk(c) for c in [5, 10, 15, 20, 30]}
base10 = set(tops[10][:5])
for c in [5, 15, 20, 30]:
    ol = [g for g in tops[c][:5] if g in base10]
    log(f"- Corte n≥{c}: top-5 preserva {len(ol)} dos {len(base10)} do corte 10 "
        f"({', '.join(tops[c][:5])})")

log(f"\nDetalhe (corte 10): top-5 = {tops[10][:5]}")
log(f"Detalhe (corte 30): top-5 = {tops[30][:5]}\n")

# ---------------------------------------------------------------------------
# 6. Sensibilidade — regra de captura (última vs média)
# ---------------------------------------------------------------------------
log("## 4. Sensibilidade à regra de captura (última vs média das capturas)\n")
log("Recomputa a diária representativa por imóvel usando **média das capturas** por "
    "(listing,date) e a receita por grupo; compara com a regra padrão (última captura).\n")

def median_diaria_rule(rule):
    if rule == "latest":
        pp = price_raw.sort_values("aq").drop_duplicates(["airbnb_listing_id", "date"], keep="last")
    elif rule == "earliest":
        pp = price_raw.sort_values("aq").drop_duplicates(["airbnb_listing_id", "date"], keep="first")
    elif rule == "mean":
        pp = price_raw.groupby(["airbnb_listing_id", "date"], as_index=False)["price"].mean()
    else:
        pp = price_raw.groupby(["airbnb_listing_id", "date"], as_index=False)["price"].median()
    return pp.groupby("airbnb_listing_id")["price"].median()

d_latest = median_diaria_rule("latest")
d_mean = median_diaria_rule("mean")

# reconstroi receita base sob a regra "média das capturas" (formulação idêntica à 03)
price_mean = price_raw.groupby(["airbnb_listing_id", "date"], as_index=False)["price"].mean()
price_mean["month"] = price_mean["date"].dt.month
rep_m = price_mean.groupby("airbnb_listing_id")["price"].median().rename("diaria_mediana")
month_m = price_mean.groupby(["airbnb_listing_id", "month"])["price"].median().unstack(fill_value=np.nan)
base_m = rev[["airbnb_listing_id", "listing_type", "number_of_bedrooms", "suburb"]].drop_duplicates()

def annual_revenue(mean_diaria, monthly_matrix, cen, obs=OBSERVED_MONTHS):
    ann = []
    for lid in monthly_matrix.index:
        a = 0.0
        for m in range(1, 13):
            occ = OCCUPANCY[cen][m]
            if m in obs:
                d = monthly_matrix.loc[lid, m]
                if pd.isna(d):
                    d = mean_diaria.loc[lid]
            else:
                d = mean_diaria.loc[lid] * SEASON_OUT[cen]
            a += d * occ * DAYS[m]
        ann.append(a)
    return pd.Series(ann, index=monthly_matrix.index)

ids = set(rev["airbnb_listing_id"])
monthly_latest = rev.set_index("airbnb_listing_id")[["diaria_m1", "diaria_m2", "diaria_m3", "diaria_m4"]]
monthly_latest.columns = [1, 2, 3, 4]
monthly_latest = monthly_latest.loc[list(ids)]
daily_latest = rev.set_index("airbnb_listing_id")["diaria_mediana"].loc[list(ids)]

rev_base_latest = annual_revenue(daily_latest, monthly_latest, "base")
rev_base_mean = annual_revenue(rep_m, month_m, "base").loc[list(ids)]

cmp = pd.DataFrame({"rev_latest": rev_base_latest, "rev_mean": rev_base_mean})
cmp["ratio"] = cmp["rev_mean"] / cmp["rev_latest"]
log(f"- Correlação de ranks (receita base por imóvel, última vs média): "
    f"{cmp['rev_latest'].rank().corr(cmp['rev_mean'].rank()):.4f}")
log(f"- Imóveis com receita base variando >5% entre as regras: "
    f"{int((cmp['ratio'] > 1.05).sum() + (cmp['ratio'] < 0.95).sum())} / {len(cmp)}")
log("- Ranks muito correlacionados → a regra de captura **não altera materialmente** a ordenação. "
    "Grupos instáveis serão apontados individualmente se necessário.\n")

# ---------------------------------------------------------------------------
# 7. Sensibilidade — outliers (sinalizar vs remover)
# ---------------------------------------------------------------------------
log("## 5. Sensibilidade a outliers da diária\n")
q99 = rev["diaria_mediana"].quantile(0.99)
q1, q3 = rev["diaria_mediana"].quantile(0.25), rev["diaria_mediana"].quantile(0.75)
iqr = q3 - q1
out_rule = (rev["diaria_mediana"] > q99) | (rev["diaria_mediana"] < q1 - 3 * iqr)
out_ids = set(rev.loc[out_rule, "airbnb_listing_id"])
log(f"- Critério outlier: diária > p99 ({q99:.0f}) ou < q1−3×IQR ({q1 - 3*iqr:.0f}).")
log(f"- Imóveis sinalizados como outlier: {len(out_ids)} ({out_rule.mean()*100:.1f}%). "
    f"**Nenhum é excluído definitivamente**; aqui a comparação mostra como mudaria se SO_SINALIZAR "
    f"ou se REMOVER (registro abaixo).\n")

rev_flag = rev.copy()
rev_flag["outlier_flag"] = rev_flag["diaria_mediana"].isin(out_ids).astype(int)

# receita/retorno por grupo sem os outliers (só para COMPARAR; nenhum imóvel é excluído em definitivo)
rev_noout = rev[~rev["airbnb_listing_id"].isin(out_ids)]
g_noout = rev_noout.groupby("grp").agg(
    n_airbnb=("airbnb_listing_id", "size"),
    rec_base_p50=("receita_anual_base", "median"),
    diaria_p50=("diaria_mediana", "median")).reset_index()
g_wo = g_noout.merge(vvp, on="grp", how="left")
g_wo["retorno_base"] = retorno(g_wo["rec_base_p50"], g_wo["preco_compra"])
g_wo = g_wo[g_wo["n_airbnb"] >= MIN_AIRBNB].copy()
g_wo = g_wo.sort_values("retorno_base", ascending=False)

top_main = groups[(groups["n_airbnb"] >= MIN_AIRBNB) &
                  (groups["status_compra"] != "NAO_COMPARAVEL")]
top_main = top_main.sort_values("retorno_base", ascending=False)["grp"].head(5).tolist()
top_noout = g_wo.dropna(subset=["retorno_base"])["grp"].head(5).tolist()

name_map = rev[["grp", "suburb", "listing_type", "number_of_bedrooms"]].drop_duplicates().set_index("grp")
def grpname(g):
    r = name_map.loc[g]
    return f"{r['suburb']} {r['listing_type']} {r['number_of_bedrooms']}q"

top_main_n = [grpname(g) for g in top_main]
top_noout_n = [grpname(g) for g in top_noout]
log(f"- Top-5 (COM todos os imóveis): {top_main_n}")
log(f"- Top-5 (SEM outliers sinalizados, removidos só para esta comparação): {top_noout_n}")
keep = len(set(top_main[:3]) & set(top_noout[:3]))
log(f"- Top-3 preservados ao remover outliers: {keep} de 3 → "
    f"{'resultado estável' if keep >= 2 else 'sinal de instabilidade a investigar'}\n")
log(f"- Detalhe dos imóveis sinalizados como outlier (todos registrados): "
    f"{sorted(out_ids)[:20]}{' ...' if len(out_ids) > 20 else ''}\n")

# ---------------------------------------------------------------------------
# 8. Teste da tese: compactos (1 quarto) no Centro
# ---------------------------------------------------------------------------
log("## 6. Tese dos compactos (1 quarto) no Centro\n")
log("A tese preliminar interna sugeria que apartamentos compactos (studio/1q) no Centro "
    "seriam a aposta mais eficiente. O teste abaixo compara perfis DENTRO do Centro e "
    "o 1q-Centro contra os demais grupos comparáveis (não é a decisão final).\n")

centro = groups[(groups["suburb"] == "Centro") &
                (groups["status_compra"] != "NAO_COMPARAVEL")].copy()
centro = centro.sort_values("retorno_base", ascending=False)
if len(centro):
    cc = centro[["listing_type", "number_of_bedrooms", "n_airbnb", "n_viva",
                 "diaria_p50", "preco_compra", "retorno_cons", "retorno_base", "retorno_otim"]].copy()
    cc[["diaria_p50", "preco_compra"]] = cc[["diaria_p50", "preco_compra"]].round(0)
    cc[["retorno_cons", "retorno_base", "retorno_otim"]] = (cc[["retorno_cons", "retorno_base", "retorno_otim"]] * 100).round(2)
    log("**Perfis no Centro (retorno base ordenado, % ao ano):**")
    table(cc.reset_index(drop=True))

    tese = groups[(groups["suburb"] == "Centro") & (groups["listing_type"] == "apartamento") &
                  (groups["number_of_bedrooms"] == 1)]
    if len(tese):
        r = tese.iloc[0]
        log(f"\n**O grupo 1q-Centro:** retorno base {r['retorno_base']*100:.2f}% | "
            f"n_airbnb(preço)={int(r['n_airbnb'])} | n_viva={int(r['n_viva'])} | "
            f"diária {r['diaria_p50']:.0f} | preço {r['preco_compra']:.0f}")
        top_any = groups.sort_values("retorno_base", ascending=False)
        top_any = top_any[top_any["status_compra"] != "NAO_COMPARAVEL"]
        rank = (top_any["grp"] == tese["grp"].iloc[0]).values.argmax()
        log(f"Posição do grupo no ranking geral de retorno base: {rank + 1}º\n")
else:
    log("Sem grupos comparáveis no Centro.\n")

# ---------------------------------------------------------------------------
# Escrita
# ---------------------------------------------------------------------------
content = "\n\n".join(REPORT)
with open(os.path.join(OUT, "return_report.md"), "w", encoding="utf-8") as f:
    f.write(content + "\n")
print("return_report.md e decision_table.csv gravados.")
print(f"  Grupos elegíveis (n_airbnb≥{MIN_AIRBNB}): {len(dec_out)}")
print("  Top-5 retorno base:", " | ".join(
    f"{r['bairro']} {r['tipo']} {r['quartos']}q" for _, r in dec_out.head(5).iterrows()))