# Hackathon Jovens Talentos AI Builder 2026 — Seazone

## 👉 Leia o desafio aqui

### **[ABRIR O DESAFIO COMPLETO](https://seazone-tech.github.io/jovens-talentos-2026-hackathon-data/)**

Lá está tudo: a missão, os dados, **o que entregar**, as regras, o prazo e **como vamos avaliar**.
Leia antes de começar a mexer nos dados.

> Se o link acima não abrir, o mesmo conteúdo está no arquivo [`index.html`](index.html) deste repositório
> (baixe e abra no navegador).

---

## Primeiro passo

**Faça um _fork_ deste repositório.** É nele que você vai trabalhar e é ele que você entrega.

---

## Os dados (`data/`)

Snapshot estático do mercado imobiliário de **Itapema (SC)**, com anúncios de Airbnb e de venda (VivaReal).
É a mesma base para todos os candidatos, para garantir comparação justa.

| Arquivo | O que tem | Como conecta |
|---|---|---|
| `Details_Itapema.csv` | Cada anúncio de Airbnb: título, reviews, star rating, descrição, host_id, nº de quartos, tipo de imóvel | Base principal dos listings |
| `Hosts_ids_Itapema.csv` | Dados do anfitrião: nº de reviews, anos como host, superhost, taxa de resposta | Liga com Details pelo `owner_id` |
| `Mesh_Ids_Data_Itapema.csv` | Latitude/longitude + bairro de cada anúncio | Liga por listing |
| `Price_AV_Itapema.csv` | Preço por anúncio, por data de estadia e por data de captura | Liga por listing |
| `VivaReal_Itapema.csv` | Anúncios de venda: preço, condomínio, área, vendedor | Mercado de compra |

---

## Estrutura do projeto

| Pasta / arquivo | O que é |
|---|---|
| `BRIEF.md` | Planejamento da análise (objetivo, critérios, tratamento dos dados, limitações, etapas) |
| `scripts/` | Código Python reproduzível (auditoria, limpeza, receita, retorno e gráficos) |
| `scripts/config.py` | **Premissas centrais dos cenários (ocupação e sazonalidade)** — um único lugar para alterar |
| `output/audit_report.md` | Relatório de auditoria dos dados brutos (linhas, ausentes, duplicidades, chaves, períodos, cobertura) |
| `output/clean_log.md` | Log de limpeza: cada tratamento aplicado e quantos registros mudaram |
| `output/revenue_report.md` | Estimativa de receita potencial por imóvel e por grupo, nos 3 cenários |
| `output/decision_table.csv` | Tabela de decisão: perfil × localização, compra, receita e retorno bruto nos 3 cenários |
| `output/processed/` | Dados limpos gerados pelos scripts (reproduzíveis, não versionados) |
| `data/` | Dados brutos fornecidos pelo desafio |

## Como executar

Crie um ambiente com Python 3 e instale as dependências:

```bash
pip install pandas matplotlib
```

Auditoria dos dados brutos:

```bash
python3 scripts/01_audit.py    # gera output/audit_report.md
```

Limpeza e organização (geram `output/clean_log.md` e os arquivos em `output/processed/`):

```bash
python3 scripts/02_clean.py
```

Estimativa de receita (lê `scripts/config.py` para cenários):

```bash
python3 scripts/03_revenue.py  # gera output/revenue_report.md
```

Retorno bruto e tabela de decisão:

```bash
python3 scripts/04_return.py   # gera output/decision_table.csv + output/return_report.md
```

Gráficos combinados:

```bash
python3 scripts/05_charts.py   # gera output/charts/*.png
```

Os arquivos limpos podem ser recriados a qualquer momento; por isso não são versionados.

## Principais cuidados encontrados na auditoria

- **Preço disponível para ~22% dos anúncios** (999 de 4.441) — concentrados em Meia Praia e Centro,
  e em apartamentos. Isso restringe e orienta as comparações.
- **Price_AV tem capturas repetidas** da mesma noite (59.799 linhas) — na limpeza mantém-se **a captura
  mais recente** por `(listing, date)`, regra cuja robustez foi verificada.
- **`owner_id` em Hosts não é único** (4.440 linhas para 3.057 donos) — na limpeza fica **uma linha por dono**;
  isso evita multiplicar linhas nas junções.
- **VivaReal:** 36 anúncios duplicados e 98 sem bairro (marcados como "Desconhecido", nada excluído em silêncio).
- **Nomes de bairro divergem** entre as bases (acentos, caixa, variantes) — há um mapa de normalização registrado.
- **Sem ligação direta entre Airbnb e VivaReal** (não há id comum) — o preço de compra será estimado.
- **Sem metragem no Airbnb** — não se usa receita por m²; não inventamos área.
- **Ausência de preço NÃO significa ocupado/receita zero.**
- **Diária anunciada ≠ receita** (sem ocupação real). A sazonalidade jan→abr ainda é um indício a validar.
- **As premissas de ocupação e sazonalidade são cenários ilustrativos** (centralizadas em `scripts/config.py`),
  não uma ocupação comprovada do mercado de Itapema.

> Ainda **não** há ranking nem recomendação final: eles virão nas próximas etapas.

## Resumo do que você entrega

1. **Este repositório, forkado e público**, com a sua análise, o `README.md` explicando como rodar,
   a pasta `ai-log/` (conversas com a IA **em texto**) e a recomendação final escrita.
2. **Vídeo de até 3 minutos** no Google Drive, com o link na primeira linha do seu README.

O detalhe de cada item, o prazo e o formulário de entrega estão no
**[desafio completo](https://seazone-tech.github.io/jovens-talentos-2026-hackathon-data/)**.

---

*Seazone — Jovens Talentos AI Builder 2026*
