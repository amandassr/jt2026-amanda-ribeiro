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

def save(fig, base, dpi=180):
    """Salva em PNG+SVG num canvas 16:9 FIXO (sem bbox_inches='tight', que corta textos)."""
    fig.set_size_inches(16, 9)
    fig.savefig(os.path.join(CH, base + ".png"), dpi=dpi, facecolor=fig.get_facecolor())
    fig.savefig(os.path.join(CH, base + ".svg"), facecolor=fig.get_facecolor())

def validate_fig(fig, label, dpi=180, tol=3):
    """Valida que NENHUM texto sai da área da imagem (canvas) nem do próprio cartão."""
    fig.canvas.draw()
    ren = fig.canvas.get_renderer()
    w, h = fig.canvas.get_width_height()
    bad = []
    # 1) todos os textos vs canvas (ignora textos invisíveis e ticks de eixos desligados)
    for t in fig.texts + [tt for ax in fig.axes if ax.axison for tt in
                          list(ax.texts) + ax.get_xticklabels() + ax.get_yticklabels()]:
        if not t.get_visible():
            continue
        tb = t.get_window_extent(renderer=ren).extents
        if (tb[0] < -tol or tb[1] < -tol or tb[2] > w + tol or tb[3] > h + tol):
            bad.append(("canvas", t.get_text()[:40], tuple(int(v) for v in tb)))
    # 2) textos dentro de cartões (axes com axis off)
    for ax in fig.axes:
        if ax.axison:
            continue
        box = ax.get_window_extent(renderer=ren).extents
        for t in ax.texts:
            if not t.get_visible():
                continue
            tb = t.get_window_extent(renderer=ren).extents
            if (tb[0] < box[0] - 1 or tb[1] < box[1] - 1 or
                    tb[2] > box[2] + 1 or tb[3] > box[3] + 1):
                bad.append(("cartão", t.get_text()[:40], tuple(int(v) for v in tb)))
    if bad:
        print(f"[{label}] ALERTA: {len(bad)} texto(s) ultrapassam limites:")
        for b in bad:
            print("   ", b)
    else:
        print(f"[{label}] OK: nenhum texto cortado (canvas {w}x{h} @ {dpi}dpi).")
    return bad

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
fig.subplots_adjust(left=0.20, right=0.985, top=0.90, bottom=0.12)
h = 0.36
for i, (_, r) in enumerate(d.iterrows()):
    c_air = GRAY if r["lo_conf"] else NAVY
    c_viv = GRAY if r["lo_conf"] else SEA
    ax.barh(y[i] + h/2, r["n_airbnb(preço)"], height=h, color=c_air, label="Airbnb com preço" if i == 0 else None)
    ax.barh(y[i] - h/2, r["n_vivareal"], height=h, color=c_viv, label="VivaReal (anúncios)" if i == 0 else None)
    ax.text(r["n_airbnb(preço)"], y[i] + h/2, f" {int(r['n_airbnb(preço)'])}", va="center",
            fontsize=10, clip_on=False)
    ax.text(r["n_vivareal"], y[i] - h/2, f" {int(r['n_vivareal'])}", va="center",
            fontsize=10, clip_on=False)
ax.set_yticks(y, d["nome"].tolist())
ax.set_xlabel("Nº de imóveis / anúncios")
ax.set_title("Mais dados em Meia Praia e Centro; os bairros de maior retorno têm amostra menor",
             fontsize=14, fontweight="bold", color=NAVY, loc="left", pad=14)
ax.legend(loc="lower right", frameon=False)
ax.margins(x=0.22)
ax.set_axisbelow(True)
ax.set_xlim(0, 2000)
validate_fig(fig, "1_cobertura_amostras")
save(fig, "1_cobertura_amostras")
plt.close(fig)

# ---------------------------------------------------------------------------
# Figura 2 — Preço de compra x diária típica (relação que define o retorno)
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(16, 9))
fig.subplots_adjust(left=0.16, right=0.955, top=0.90, bottom=0.11)
markers = {"principal": "P", "alternativa": "A", "compacto": "C"}
rows = []
for _, r in dec.iterrows():
    c = GRAY if r["lo_conf"] else ("gold" if False else (GOLD if r["focal"] == "principal" else SEA if r["focal"] else NAVY))
    s = 90 if r["focal"] else 55
    ax.scatter(r["preco_compra_est"], r["diaria_tipica"], s=s, color=c,
               edgecolor=WHITE, linewidth=1.5, zorder=3)
    rows.append((r, c))
# anota apenas os candidatos focais (menos poluição e sem textos na borda)
for i, (r, c) in enumerate(rows):
    if pd.isna(r["focal"]):
        continue
    dx = 8 if i % 2 == 0 else -8
    dy = 10 if i % 3 == 0 else -12
    ax.annotate(f"{r['nome_n']}\n{r['preco_compra_est']/1e3:.0f}.000 · {r['diaria_tipica']:.0f} · ret {r['retorno_base(%)']:.1f}%",
                (r["preco_compra_est"], r["diaria_tipica"]),
                xytext=(dx, dy), textcoords="offset points", fontsize=9, color=INK,
                clip_on=False)
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
ax.xaxis.set_major_formatter(FuncFormatter(fmt_real))
ax.set_xticks([0, 1_000_000, 2_000_000, 3_000_000, 4_000_000])
ax.set_xlim(0, 4_000_000)
ax.set_ylim(0, dec["diaria_tipica"].max() * 1.30)
validate_fig(fig, "2_preco_x_diaria")
save(fig, "2_preco_x_diaria")
plt.close(fig)

# ---------------------------------------------------------------------------
# Figura 3 — Retorno bruto nos 3 cenários
# ---------------------------------------------------------------------------
d = dec.sort_values("retorno_base(%)", ascending=False).copy()
y = np.arange(len(d))
fig, ax = plt.subplots(figsize=(16, 9))
fig.subplots_adjust(left=0.24, right=0.985, top=0.90, bottom=0.12)
w = 0.55
for i, (_, r) in enumerate(d.iterrows()):
    vals = [r["retorno_cons(%)"], r["retorno_base(%)"], r["retorno_otim(%)"]]
    offs = [-w, 0, w]
    for v, o, cen in zip(vals, offs, ["conservador", "base", "otimista"]):
        c = GRAY if r["lo_conf"] else (GOLD if (r["focal"] and cen == "base") else bar_c[cen])
        ax.barh(y[i] + o, v, height=w*0.8, left=0, color=c, edgecolor="none")
        ax.text(v, y[i] + o, f" {v:.1f}%", va="center", ha="left", fontsize=8.5,
                color=GRAY_D if r["lo_conf"] else INK, clip_on=False)
    if r["focal"]:
        ax.plot([-0.1, -0.1], [y[i] - 0.3, y[i] + 0.3], color=GOLD, lw=2.5)
ax.set_yticks(y, d["nome_n"].tolist(), fontsize=9.5)
ax.set_xlabel("Retorno bruto estimado (% ao ano)  ·  receita estimada ÷ preço de compra estimado")
ax.set_title("Morretes lidera o retorno, mas com amostra fina; Centro e Meia Praia são os mais testados",
             fontsize=14, fontweight="bold", color=NAVY, loc="left", pad=14)
lg = [Line2D([0], [0], color=NAVY_H, lw=6, label="Conservador"),
      Line2D([0], [0], color=NAVY, lw=6, label="Base"),
      Line2D([0], [0], color=SEA, lw=6, label="Otimista"),
      Line2D([0], [0], color=GRAY, lw=6, label="Baixa confiança (n<30)")]
ax.legend(handles=lg, loc="lower right", frameon=False, fontsize=10)
ax.set_axisbelow(True)
ax.set_xticks([0, 2, 4, 6, 8, 10, 12, 14])
ax.set_xlim(0, 14)
validate_fig(fig, "3_retorno_3_cenarios")
save(fig, "3_retorno_3_cenarios")
plt.close(fig)

# ---------------------------------------------------------------------------
# Helpers de layout: medição de texto, quebra automática e validação de limites
# ---------------------------------------------------------------------------
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties as _FP

def _txt_w(text, fontsize, family="DejaVu Sans"):
    """Largura do texto em polegadas, usando a métrica real da fonte."""
    fp = _FP(family=family, size=fontsize)
    path = TextPath((0, 0), text, size=fontsize, prop=fp)
    return path.get_extents().width / 72.0

def wrap_inches(text, max_w_in, fontsize, family="DejaVu Sans"):
    """Quebra em linhas para caber em max_w_in, sem cortar palavras."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip() if cur else w
        if _txt_w(trial, fontsize, family) <= max_w_in or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def line_h_in(fontsize, spacing=1.16):
    return fontsize / 72.0 * spacing

def ax_inches(ax, fig):
    pos = ax.get_position()
    fw, fh = fig.get_size_inches()
    return pos.width * fw, pos.height * fh

def fit_block(ax, fig, x_frac, y_top_frac, text, max_w_frac, fontsize0, max_h_frac,
              color=INK, ha="left", weight="normal", style="normal", spacing=1.16,
              min_fs=6.0):
    """Place text wrapped to width AND height, shrinking font until it fits."""
    axw, axh = ax_inches(ax, fig)
    max_w_in, max_h_in = max_w_frac * axw, max_h_frac * axh
    fs = fontsize0
    while fs >= min_fs:
        lines = wrap_inches(text, max_w_in, fs)
        if len(lines) * line_h_in(fs, spacing) <= max_h_in:
            return ax.text(x_frac, y_top_frac, "\n".join(lines),
                           transform=ax.transAxes, va="top", ha=ha, fontsize=fs,
                           color=color, fontweight=weight, style=style, linespacing=1.2)
        fs -= 0.5
    lines = wrap_inches(text, max_w_in, min_fs)
    return ax.text(x_frac, y_top_frac, "\n".join(lines), transform=ax.transAxes,
                   va="top", ha=ha, fontsize=min_fs, color=color,
                   fontweight=weight, style=style)

def rounded_box(ax, x, y, w, h, fc, ec="#DDE3EC", radius=0.02, lw=1.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle=f"round,pad=0.01,rounding_size={radius}",
                 fc=fc, ec=ec, lw=lw))

def get_focal(name):
    f = FOCAL[name]
    m = (dec["bairro"] == f["bairro"]) & (dec["quartos"] == f["quartos"])
    return dec[m].iloc[0]

p = get_focal("principal"); a = get_focal("alternativa"); c = get_focal("compacto")
CAND = [("principal", p, GOLD, "CANDIDATO PRINCIPAL"),
        ("alternativa", a, SEA, "ALTERNATIVA (MAIS LÍQUIDA)"),
        ("compacto", c, NAVY, "COMPACTO NO CENTRO (TESE)")]

CAND_WHY = {
    "principal": "Maior retorno base entre grupos com amostra razoável (7,9% a.a.). "
                 "Mercado de venda profundo (1.037 anúncios).",
    "alternativa": "Amostra ampla e líquida (187 Airbnb, 243 venda). Menor surpresa "
                   "esperada; base para escalar a operação.",
    "compacto": "Melhor retorno dentro do Centro (6,97%) e menor preço de entrada. "
                "A tese dos compactos se sustenta no Centro, não na cidade.",
}
CAND_RISK = {
    "principal": "Amostra Airbnb moderada (51); retorno depende de ocupação constante "
                 "e dos cenários de aluguel.",
    "alternativa": "Retorno menor (5,9%) e preço de entrada maior (R$ 1,08 mi).",
    "compacto": "Poucos anúncios de venda no Centro (22) e concentração da oferta; "
                "ocupação é suposição.",
}
FOOT_NOTE = ("Retornos e receitas são estimativas baseadas em cenários de ocupação "
             "(conservador / base / otimista) — ver scripts/config.py. Não representam "
             "ocupação comprovada do mercado de Itapema.")

# ---------------------------------------------------------------------------
# VISUAL 4 — Resumo da decisão (3 cartões) — 16:9
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(16, 9))
fig.patch.set_facecolor(BG)

fig.text(0.035, 0.955, "Resumo da decisão — candidatos de investimento em Itapema/SC",
         fontsize=17, fontweight="bold", color=NAVY, va="top")
fig.text(0.035, 0.918, "Números preliminares, sujeitos à revisão. Percentuais = retorno bruto "
         "estimado (% ao ano), receita estimada ÷ preço de compra estimado.",
         fontsize=11, color=MUTE, va="top")

CXS = [0.03, 0.356, 0.682]
CWS = 0.288
CARD_Y0, CARD_H = 0.045, 0.85

for (key, r, accent, ttl), x in zip(CAND, CXS):
    ax = fig.add_axes([x, CARD_Y0, CWS, CARD_H])
    rounded_box(ax, 0.02, 0.02, 0.96, 0.95, WHITE, radius=0.022)
    ax.plot([0.05, 0.05], [0.08, 0.92], color=accent, lw=5, transform=ax.transAxes)
    # Título do cartão
    ax.text(0.105, 0.945, ttl, transform=ax.transAxes, fontsize=13, fontweight="bold",
            color=accent, va="top", ha="left")
    # Nome do imóvel
    ax.text(0.105, 0.86, r["nome"], transform=ax.transAxes, fontsize=21, fontweight="bold",
            color=NAVY, va="top", ha="left")
    # Valor principal
    ax.text(0.105, 0.72, f"{r['retorno_base(%)']:.1f}% a.a.", transform=ax.transAxes,
            fontsize=34, fontweight="bold", color=NAVY, va="top", ha="left")
    # Linhas de informação (preço / amostras)
    info = [
        f"Preço estimado: R$ {r['preco_compra_est']/1e3:,.0f} mil",
        f"Amostra Airbnb (com preço): {int(r['n_airbnb(preço)'])} imóveis",
        f"Amostra VivaReal: {int(r['n_vivareal'])} anúncios",
    ]
    iy = 0.60
    for line in info:
        ax.text(0.105, iy, line, transform=ax.transAxes, fontsize=12.5, color=MUTE,
                va="top", ha="left")
        iy -= 0.052
    # divisor
    ax.plot([0.08, 0.94], [0.445, 0.445], transform=ax.transAxes, color="#E4E9F1", lw=1.2)
    # Por que considerar
    ax.text(0.105, 0.415, "POR QUE CONSIDERAR", transform=ax.transAxes, fontsize=11,
            fontweight="bold", color=NAVY, va="top", ha="left")
    fit_block(ax, fig, 0.105, 0.330, CAND_WHY[key], 0.80, 13.0, 0.155, color=INK)
    # Principal risco
    ax.text(0.105, 0.222, "PRINCIPAL RISCO", transform=ax.transAxes, fontsize=11,
            fontweight="bold", color=NAVY, va="top", ha="left")
    fit_block(ax, fig, 0.105, 0.148, CAND_RISK[key], 0.80, 12.5, 0.105, color=MUTE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

note_ax = fig.add_axes([0.02, 0.006, 0.96, 0.036], frameon=False)
rounded_box(note_ax, 0.0, 0.0, 1.0, 1.0, "#FBF3E0", ec="#E6CF80", radius=0.05, lw=1)
note_ax.text(0.5, 0.5, FOOT_NOTE, transform=note_ax.transAxes, ha="center", va="center",
             fontsize=9.5, color="#8A6D1F", style="italic", fontweight="bold")
note_ax.axis("off")

validate_fig(fig, "4_resumo_decisao", dpi=200)
save(fig, "4_resumo_decisao", dpi=200)
plt.close(fig)

# ---------------------------------------------------------------------------
# VISUAL 5 — Comparação dos candidatos (3 gráficos simples) — 16:9
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(16, 9))
fig.patch.set_facecolor(BG)

fig.text(0.05, 0.955, "Comparação dos candidatos — Itapema/SC",
         fontsize=17, fontweight="bold", color=NAVY, va="top")
fig.text(0.05, 0.907, "Preço de compra estimado (mediana VivaReal) · retorno base (cenário "
         "médio) · tamanho das amostras.",
         fontsize=11, color=MUTE, va="top")

colors = {"principal": GOLD, "alternativa": SEA, "compacto": NAVY}
comp_rows = pd.concat([p.to_frame().T, a.to_frame().T, c.to_frame().T])
comp_rows = comp_rows.reset_index(drop=True)

PANELS = [
    # (x, n_major, title, xlabel, fmt)
    (0.05,  "preco_compra_est", "Preço de compra estimado", "R$ (mediana VivaReal)", lambda v: fmt_real(v, None)),
    (0.365, "retorno_base(%)", "Retorno base", "% ao ano", lambda v: f"{v:.2f}%".replace(".", ",")),
    (0.68,  "n_airbnb(preço)", "Tamanho da amostra (Airbnb)", "n imóveis com preço", lambda v: f"{int(v)}"),
]

def panel(ax, n_major, title, xlabel, fmt, show_viva=False):
    yy = np.arange(len(comp_rows))[::-1]
    for i, (_, r) in enumerate(comp_rows.iterrows()):
        y = yy[i]
        color = colors[r["focal"]]
        ax.barh(y, r[n_major], height=0.5, color=color, edgecolor="none", zorder=3)
        ax.text(r[n_major], y, f"  {fmt(r[n_major])}", va="center", ha="left",
                fontsize=14, fontweight="bold", color=INK, zorder=4, clip_on=False)
        # nome do candidato ACIMA da barra (horizontal, dentro do painel, sem corte)
        ax.text(0.0, y + 0.42, r["nome"], va="bottom", ha="left",
                fontsize=11, fontweight="bold", color=MUTE, zorder=4, clip_on=False)
    # sem rótulos no eixo y (nomes vão acima das barras, evitando corte à esquerda)
    ax.set_yticks([])
    ax.set_xlabel(xlabel, fontsize=11, color=MUTE)
    ax.set_title(title, fontsize=14, fontweight="bold", color=NAVY, loc="left", pad=14)
    ax.set_axisbelow(True)
    clean_ax(ax)
    ax.set_xlim(0, comp_rows[n_major].max() * 1.42)
    ax.tick_params(axis="x", colors=MUTE)
    ax.set_yticks([])

# painéis de preço e retorno
for x, n_major, title, xlabel, fmt in PANELS[:2]:
    panel(fig.add_axes([x, 0.16, 0.30, 0.70]), n_major, title, xlabel, fmt, show_viva=False)

# painel de amostras: também mostra VivaReal
axs = fig.add_axes([0.68, 0.16, 0.30, 0.70])
yy = np.arange(len(comp_rows))[::-1]
for i, (_, r) in enumerate(comp_rows.iterrows()):
    y = yy[i]
    axs.barh(y + 0.185, r["n_vivareal"], height=0.30, color="#C6CFDB", edgecolor="none",
             label="VivaReal" if i == 0 else None, zorder=2)
    axs.barh(y - 0.185, r["n_airbnb(preço)"], height=0.30, color=colors[r["focal"]],
             edgecolor="none", label="Airbnb com preço" if i == 0 else None, zorder=3)
    axs.text(r["n_vivareal"], y + 0.185, f"  {int(r['n_vivareal'])}", va="center", ha="left",
             fontsize=12.5, color=MUTE, zorder=4, clip_on=False)
    axs.text(r["n_airbnb(preço)"], y - 0.185, f"  {int(r['n_airbnb(preço)'])}", va="center",
             ha="left", fontsize=12.5, fontweight="bold", color=INK, zorder=4, clip_on=False)
    axs.text(0.0, y + 0.42, r["nome"], va="bottom", ha="left",
             fontsize=11, fontweight="bold", color=MUTE, zorder=4, clip_on=False)
axs.set_yticks([])
axs.set_ylabel("Airbnb (verde/azul/dourado = candidato) · VivaReal (cinza)", fontsize=10, color=MUTE)
axs.set_xlabel("n imóveis / anúncios", fontsize=11, color=MUTE)
axs.set_title("Tamanho da amostra", fontsize=14, fontweight="bold", color=NAVY, loc="left", pad=14)
axs.set_axisbelow(True)
axs.set_xticks([0, 200, 400, 600, 800, 1000, 1200])
axs.set_xlim(0, 1200)
axs.legend(loc="lower right", frameon=False, fontsize=10)
clean_ax(axs)
axs.tick_params(axis="x", colors=MUTE)

note_ax2 = fig.add_axes([0.02, 0.006, 0.96, 0.036], frameon=False)
rounded_box(note_ax2, 0.0, 0.0, 1.0, 1.0, "#FBF3E0", ec="#E6CF80", radius=0.05, lw=1)
note_ax2.text(0.5, 0.5, FOOT_NOTE, transform=note_ax2.transAxes, ha="center", va="center",
              fontsize=9.5, color="#8A6D1F", style="italic", fontweight="bold")
note_ax2.axis("off")

validate_fig(fig, "5_comparacao_candidatos", dpi=200)
save(fig, "5_comparacao_candidatos", dpi=200)
plt.close(fig)

print("Visuais regenerados (PNG + SVG) em output/charts/:")
for f in sorted(os.listdir(CH)):
    print(f"  - {f}")