#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Etapa 2c — Visuais executivos (16:9, PNG + SVG)
Hackathon Jovens Talentos AI Builder 2026 (Seazone) — Itapema (SC)

Reformulação completa do visual: estilo de relatório de decisão de investimento.
- Formato horizontal 16:9, alta resolução, fundo claro.
- Paleta azul-marinho + verde-água; dourado somente para destaques; cinza p/ baixa confiança.
- Nomes curtos ("Morretes | 2 quartos"), sem textos inclinados, valores direto nos gráficos.
- Candidatos preliminares destacados (principal / alternativa / compacto no Centro).
- Painel executivo de 1 página com 3 cartões + comparação + riscos/prós + nota de estimativa.

Os candidatos são PRELIMINARES (baseados na ordenação + confiança de amostra), sujeitos
à recomendação final. Qualquer grupo com n_airbnb < 30 é marcado como baixa confiança.
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import FuncFormatter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "output")
CH = os.path.join(OUT, "charts")
os.makedirs(CH, exist_ok=True)

# ---------------------------------------------------------------------------
# Estilo (paleta executiva)
# ---------------------------------------------------------------------------
NAVY   = "#00143D"
NAVY_H = "#5E7EA8"      # azul-marinho claro (conservador)
SEA    = "#17A398"      # verde-água (otimista)
SEA_D  = "#0E7C6D"
GOLD   = "#C9A227"      # dourado — só destaques
GRAY   = "#C6CFDB"      # baixa confiança
GRAY_D = "#8A97A8"
INK    = "#0E1B33"
MUTE   = "#5A6B85"
BG     = "#F7F9FC"
LIGHT  = "#EEF2F8"      # cartões
WHITE  = "#FFFFFF"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "text.color": INK,
    "axes.edgecolor": "#D6DDE8",
    "axes.labelcolor": INK,
    "xtick.color": MUTE,
    "ytick.color": MUTE,
    "axes.grid": True,
    "grid.color": "#E4E9F1",
    "grid.linewidth": 0.8,
    "grid.alpha": 1,
    "figure.facecolor": BG,
    "axes.facecolor": WHITE,
    "svg.fonttype": "none",
})

def short_name(row):
    b = {"Tabuleiro dos Oliveiras": "Tabuleiro"}.get(row["bairro"], row["bairro"])
    return f"{b} | {row['quartos']} quartos"

def name_n(row):
    return f"{short_name(row)}  ·  n={int(row['n_airbnb(preço)'])}"

def save(fig, base, tight=True, dpi=180):
    kw = dict(facecolor=fig.get_facecolor())
    if tight:
        kw["bbox_inches"] = "tight"
    fig.savefig(os.path.join(CH, base + ".png"), dpi=dpi, **kw)
    fig.savefig(os.path.join(CH, base + ".svg"), **kw)

def clean_ax(ax, xlabel=None, ylabel=None):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color("#D6DDE8")
    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)

def fmt_real(x, _):
    return f"R$ {x/1e3:,.0f}k" if x < 1e6 else f"R$ {x/1e6:.1f}M"

# ---------------------------------------------------------------------------
# Dados
# ---------------------------------------------------------------------------
dec = pd.read_csv(os.path.join(OUT, "decision_table.csv"))
dec["grupo"] = dec["bairro"] + " | " + dec["tipo"] + " | " + dec["quartos"].astype(int).astype(str)
dec["quartos"] = dec["quartos"].astype(int)
dec = dec.dropna(subset=["preco_compra_est"]).copy()
dec["lo_conf"] = dec["n_airbnb(preço)"] < 30
dec["nome"] = dec.apply(short_name, axis=1)
dec["nome_n"] = dec.apply(name_n, axis=1)

# Candidatos preliminares (documentado acima)
FOCAL = {
    "principal":   {"bairro": "Morretes",  "quartos": 2, "label": "Principal"},
    "alternativa": {"bairro": "Meia Praia", "quartos": 2, "label": "Alternativa"},
    "compacto":    {"bairro": "Centro",     "quartos": 1, "label": "Compacto Centro"},
}
def focal_of(row):
    for k, f in FOCAL.items():
        if row["bairro"] == f["bairro"] and row["quartos"] == f["quartos"]:
            return k
    return None

dec["focal"] = dec.apply(focal_of, axis=1)

bar_c = {"conservador": NAVY_H, "base": NAVY, "otimista": SEA}
def bar_color(row, cen):
    if row["lo_conf"]:
        return GRAY
    return bar_c[cen]

# ---------------------------------------------------------------------------
# Figura 1 — Cobertura das amostras
# ---------------------------------------------------------------------------
d = dec.sort_values("n_airbnb(preço)").copy()
y = np.arange(len(d))
fig, ax = plt.subplots(figsize=(16, 9))
h = 0.36
for i, (_, r) in enumerate(d.iterrows()):
    c_air = GRAY if r["lo_conf"] else NAVY
    c_viv = GRAY if r["lo_conf"] else SEA
    ax.barh(y[i] + h/2, r["n_airbnb(preço)"], height=h, color=c_air, label="Airbnb com preço" if i == 0 else None)
    ax.barh(y[i] - h/2, r["n_vivareal"], height=h, color=c_viv, label="VivaReal (anúncios)" if i == 0 else None)
    ax.text(r["n_airbnb(preço)"], y[i] + h/2, f" {int(r['n_airbnb(preço)'])}", va="center", fontsize=10)
    ax.text(r["n_vivareal"], y[i] - h/2, f" {int(r['n_vivareal'])}", va="center", fontsize=10)
ax.set_yticks(y, d["nome"].tolist())
ax.set_xlabel("Nº de imóveis / anúncios")
ax.set_title("Mais dados em Meia Praia e Centro; os bairros de maior retorno têm amostra menor",
             fontsize=14, fontweight="bold", color=NAVY, loc="left", pad=14)
ax.legend(loc="lower right", frameon=False)
ax.margins(x=0.18)
ax.set_axisbelow(True)
save(fig, "1_cobertura_amostras")
plt.close(fig)

# ---------------------------------------------------------------------------
# Figura 2 — Preço de compra x diária típica (relação que define o retorno)
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(16, 9))
markers = {"principal": "P", "alternativa": "A", "compacto": "C"}
rows = []
for _, r in dec.iterrows():
    c = GRAY if r["lo_conf"] else ("gold" if False else (GOLD if r["focal"] == "principal" else SEA if r["focal"] else NAVY))
    s = 90 if r["focal"] else 55
    ax.scatter(r["preco_compra_est"], r["diaria_tipica"], s=s, color=c,
               edgecolor=WHITE, linewidth=1.5, zorder=3)
    rows.append((r, c))
for i, (r, c) in enumerate(rows):
    dx = 8 if i % 2 == 0 else -8
    dy = 8 if i % 3 == 0 else -10
    ax.annotate(f"{r['nome_n']}\n{r['preco_compra_est']/1e3:.0f}.000 · {r['diaria_tipica']:.0f} · ret {r['retorno_base(%)']:.1f}%",
                (r["preco_compra_est"], r["diaria_tipica"]),
                xytext=(dx, dy), textcoords="offset points", fontsize=9, color=INK,
                arrowprops=dict(arrowstyle="-", color="#C9D2E0", lw=0.8) if r["lo_conf"] else None)
# legenda manual (sem sobrepor dados)
from matplotlib.lines import Line2D
leg = [
    Line2D([0], [0], marker="o", color="w", markerfacecolor=GOLD, markersize=9, label="Principal (destacado)"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor=SEA, markersize=9, label="Alternativa / Compacto Centro"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor=NAVY, markersize=9, label="Demais grupos"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor=GRAY, markersize=9, label="Baixa confiança (n<30)"),
]
ax.legend(handles=leg, loc="upper left", frameon=False, fontsize=10)
ax.xaxis.set_major_formatter(FuncFormatter(fmt_real))
ax.set_xlabel("Preço de compra estimado (R$) — mediana VivaReal")
ax.set_ylabel("Diária típica (R$) — mediana Airbnb")
ax.set_title("Diária e preço sobem juntos; o retorno vem da relação entre eles",
             fontsize=14, fontweight="bold", color=NAVY, loc="left", pad=14)
clean_ax(ax)
save(fig, "2_preco_x_diaria")
plt.close(fig)

# ---------------------------------------------------------------------------
# Figura 3 — Retorno bruto nos 3 cenários
# ---------------------------------------------------------------------------
d = dec.sort_values("retorno_base(%)", ascending=False).copy()
y = np.arange(len(d))
fig, ax = plt.subplots(figsize=(16, 9))
w = 0.55
for i, (_, r) in enumerate(d.iterrows()):
    vals = [r["retorno_cons(%)"], r["retorno_base(%)"], r["retorno_otim(%)"]]
    offs = [-w, 0, w]
    for v, o, cen in zip(vals, offs, ["conservador", "base", "otimista"]):
        c = GRAY if r["lo_conf"] else (GOLD if (r["focal"] and cen == "base") else bar_c[cen])
        ax.barh(y[i] + o, v, height=w*0.8, left=0, color=c, edgecolor="none")
        ax.text(v, y[i] + o, f" {v:.1f}%", va="center", ha="left", fontsize=8.5,
                color=GRAY_D if r["lo_conf"] else INK)
    if r["focal"]:
        ax.plot([-0.1, -0.1], [y[i] - 0.3, y[i] + 0.3], color=GOLD, lw=2.5)
ax.set_yticks(y, d["nome_n"].tolist())
ax.set_xlabel("Retorno bruto estimado (% ao ano)  ·  receita estimada ÷ preço de compra estimado")
ax.set_title("Morretes lidera o retorno, mas com amostra fina; Centro e Meia Praia são os mais testados",
             fontsize=14, fontweight="bold", color=NAVY, loc="left", pad=14)
lg = [Line2D([0], [0], color=NAVY_H, lw=6, label="Conservador"),
      Line2D([0], [0], color=NAVY, lw=6, label="Base"),
      Line2D([0], [0], color=SEA, lw=6, label="Otimista"),
      Line2D([0], [0], color=GRAY, lw=6, label="Baixa confiança (n<30)")]
ax.legend(handles=lg, loc="lower right", frameon=False, fontsize=10)
ax.margins(x=0.28)
ax.set_axisbelow(True)
save(fig, "3_retorno_3_cenarios")
plt.close(fig)

# ---------------------------------------------------------------------------
# PAINEL EXECUTIVO — 1 página (16:9)
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(16, 9))
fig.patch.set_facecolor(BG)
# layout em coordenadas normalizadas
CX1, CX2, CX3 = 0.035, 0.3575, 0.68
CW = 0.285
card_w, card_h = CW, 0.215
TXT_BOX = {"facecolor": WHITE, "edgecolor": "#DDE3EC", "linewidth": 1}

def card(ax, accent, title, value, sub, n_lbl):
    ax.add_patch(FancyBboxPatch((0.02, 0.04), 0.96, 0.92,
                 boxstyle="round,pad=0.012,rounding_size=0.03",
                 fc=WHITE, ec="#DDE3EC", lw=1.2))
    ax.add_patch(FancyBboxPatch((0.02, 0.04), 0.92, 0.92,
                 boxstyle="round,pad=0.012,rounding_size=0.03",
                 fc="none", ec="none"))
    ax.plot([0.05, 0.05], [0.10, 0.90], color=accent, lw=5, transform=ax.transAxes)
    ax.text(0.10, 0.88, title, transform=ax.transAxes, fontsize=13, fontweight="bold", color=accent)
    ax.text(0.10, 0.66, value, transform=ax.transAxes, fontsize=26, fontweight="bold", color=NAVY)
    ax.text(0.10, 0.50, sub, transform=ax.transAxes, fontsize=11, color=MUTE)
    ax.text(0.10, 0.34, n_lbl, transform=ax.transAxes, fontsize=10.5, color=MUTE)
    ax.axis("off")

def get_focal(name):
    f = FOCAL[name]
    m = (dec["bairro"] == f["bairro"]) & (dec["quartos"] == f["quartos"])
    return dec[m].iloc[0]

p = get_focal("principal"); a = get_focal("alternativa"); c = get_focal("compacto")

# Cartões
for ax, key, r, accent, ttl in [
    (fig.add_axes([CX1, 0.755, CW, card_h]), "principal", p, GOLD, "CANDIDATO PRINCIPAL"),
    (fig.add_axes([CX2, 0.755, CW, card_h]), "alternativa", a, SEA, "ALTERNATIVA (MAIS LÍQUIDA)"),
    (fig.add_axes([CX3, 0.755, CW, card_h]), "compacto", c, NAVY, "COMPACTO NO CENTRO (TESE)"),
]:
    sub = f"{r['nome']}  ·  retorno base {r['retorno_base(%)']:.1f}% a.a."
    card(ax, accent=accent, title=ttl,
         value=f"{r['retorno_base(%)']:.1f}% a.a.",
         sub=sub,
         n_lbl=f"preço R$ {r['preco_compra_est']/1e3:,.0f}k  ·  n Airbnb {int(r['n_airbnb(preço)'])}  ·  n VivaReal {int(r['n_vivareal'])}")

# Título do painel
fig.text(0.035, 0.955, "Recomendação preliminar de investimento — Itapema/SC",
         fontsize=17, fontweight="bold", color=NAVY)
fig.text(0.035, 0.925, "Comparação entre o candidato principal, a alternativa e o compacto no Centro "
         "(números preliminares — sujeitos à recomendação final)",
         fontsize=11, color=MUTE)

# Comparação visual — 3 minipainéis (preço / retorno base / amostra)
def mini(ax, rows, accent, n_major, xlabel, title, fmt):
    rows = rows.copy()
    yy = np.arange(len(rows))
    for i, (_, r) in enumerate(rows.iterrows()):
        ax.barh(yy[i], r[n_major], height=0.6, color=accent, edgecolor="none")
        ax.text(r[n_major], yy[i], f"  {fmt(r[n_major])}", va="center", fontsize=11,
                color=INK, fontweight="bold")
    ax.set_yticks(yy, rows["nome"].tolist())
    ax.invert_yaxis()
    ax.set_xlabel(xlabel)
    ax.set_title(title, fontsize=11.5, fontweight="bold", color=NAVY, loc="left")
    clean_ax(ax)
    ax.margins(x=0.25)

comp_rows = pd.concat([p.to_frame().T, a.to_frame().T, c.to_frame().T])
fmt_real1 = lambda v: fmt_real(v, None)
mini(fig.add_axes([0.035, 0.495, 0.285, 0.21]), comp_rows, GOLD,
     "preco_compra_est", "Preço compra estimado (R$)", "Preço de compra", fmt_real1)
mini(fig.add_axes([0.3575, 0.495, 0.285, 0.21]), comp_rows, SEA,
     "retorno_base(%)", "Retorno base (% a.a.)", "Retorno base", lambda v: f"{v:.1f}%")
mini(fig.add_axes([0.68, 0.495, 0.285, 0.21]), comp_rows, NAVY,
     "n_airbnb(preço)", "Amostra (n Airbnb com preço)", "Amostra", lambda v: f"{int(v)}")

# Por que considerar / principal risco
def text_block(ax, r, accent, why, risk):
    ax.add_patch(FancyBboxPatch((0.02, 0.03), 0.96, 0.97,
                 boxstyle="round,pad=0.012,rounding_size=0.02",
                 fc=LIGHT, ec="#DDE3EC", lw=1))
    ax.plot([0.055, 0.055], [0.12, 0.90], color=accent, lw=4, transform=ax.transAxes)
    ax.text(0.10, 0.90, "POR QUE CONSIDERAR", transform=ax.transAxes, fontsize=10,
            fontweight="bold", color=NAVY)
    ax.text(0.10, 0.72, why, transform=ax.transAxes, fontsize=11, color=INK, va="top",
            wrap=True)
    ax.text(0.10, 0.42, "PRINCIPAL RISCO", transform=ax.transAxes, fontsize=10,
            fontweight="bold", color=NAVY)
    ax.text(0.10, 0.16, risk, transform=ax.transAxes, fontsize=10.5, color=MUTE, va="top",
            wrap=True)
    ax.axis("off")

tb = [
    ("principal", p, GOLD,
     "Maior retorno base entre grupos com amostra razoável (7,9% a.a.). " \
     "Preço de entrada médio e mercado de venda profundo (1.037 anúncios).",
     "Amostra Airbnb moderada (51 imóveis); retorno depende dos cenários de ocupação " \
     "e de aluguel constante em Morretes."),
    ("alternativa", a, SEA,
     "Amostra mais ampla e líquida (187 Airbnb, 243 venda). Menor surpresa esperada; " \
     "base para escalar operação em Meia Praia.",
     "Retorno mais baixo (5,9% a.a.) e preço de compra maior (R$ 1,08 mi) — menos " \
     "alavancagem por real investido."),
    ("compacto", c, NAVY,
     "Melhor retorno dentro do Centro (6,97% a.a.) e menor preço de entrada (R$ 890 mil). " \
     "A tese dos compactos se sustenta no Centro, não na cidade.",
     "Poucos anúncios de venda no Centro (22) e concentração da oferta — amostra " \
     "de compra fina; ocupação é suposição."),
]
for key, r, accent, why, risk in tb:
    x = {"principal": 0.035, "alternativa": 0.3575, "compacto": 0.68}[key]
    text_block(fig.add_axes([x, 0.06, CW, 0.40]), r, accent, why, risk)

# Nota de estimativa (rodapé)
note_ax = fig.add_axes([0.035, 0.028, 0.93, 0.035], frameon=False)
note_ax.add_patch(FancyBboxPatch((0.0, 0.0), 1.0, 1.0,
                 boxstyle="round,pad=0.02,rounding_size=0.03",
                 fc="#FBF3E0", ec="#E6CF80", lw=1))
note_ax.text(0.5, 0.5,
             "Nota de estimativa · retorno e receita são ESTIMATIVAS baseadas em cenários "
             "de ocupação (conservador / base / otimista), ver scripts/config.py — não "
             "representam ocupação comprovada do mercado de Itapema.",
             transform=note_ax.transAxes, ha="center", va="center",
             fontsize=10.5, color="#8A6D1F", style="italic", fontweight="bold")
note_ax.axis("off")

save(fig, "0_dashboard_executivo", tight=False)
plt.close(fig)

print("Visuais regenerados (PNG + SVG) em output/charts/:")
for f in sorted(os.listdir(CH)):
    print(f"  - {f}")