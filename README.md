**[LINK DO VÍDEO — preencher antes do envio]** (Google Drive, "qualquer pessoa com o link", até 3 min): `[PREENCHER ANTES DO ENVIO]`

---

# Hackathon Jovens Talentos AI Builder 2026 — Seazone

# Recomendação de investimento imobiliário — Itapema (SC)

## 1. Resumo executivo

**Recomendação: apartamento de 2 quartos em Morretes.**

É o grupo que combina o **maior retorno-base entre os grupos com amostra confiável**:
~**7,9% ao ano** (cenário base; receita anual estimada ≈ R$ 62,7 mil sobre preço de compra
estimado ≈ R$ 790 mil), apoiado por **ampla amostra de anúncios de venda** (1.037 anúncios),
que torna o preço estimado mais sólido, e por amostra Airbnb razoável (51 imóveis com preço).

> Importante: retorno e receita são **estimativas** baseadas em cenários de ocupação
> (seção 7). Não são valores comprovados nem líquidos — não incluem custos de gestão,
> manutenção, IPTU, condomínio ou impostos.

![Resumo da decisão — candidatos](output/charts/4_resumo_decisao.png)
*Figura 1 — Resumo da decisão: cartões dos três candidatos avaliados.*

## 2. As quatro perguntas do desafio

### P1 — Qual o melhor perfil de imóvel?

Perfis maiores e com mais banheiros/hóspedes estão **associados** a diárias e receitas maiores
(quartos: +0,58; banheiros: +0,54; hóspedes: +0,50 — correlação de Spearman, ver
`output/features_report.md`). Entre os grupos com amostra confiável, o perfil mais eficiente por
real investido é o **apartamento de 2 quartos**, com destaque para Morretes.

### P2 — Qual a melhor localização em termos de receita?

Em **receita potencial estimada**, a localização de maior receita é a **Meia Praia**:
o perfil **apartamento de 4 quartos** tem receita-base estimada de **≈ R$ 137,9 mil/ano**
(com **60 imóveis com preço** na amostra; diária típica ≈ R$ 1.012).

**Receita ≠ retorno:** receita alta não significa melhor investimento. O **retorno**
(receita ÷ preço de compra) da Meia Praia 4q é baixo (**≈ 3,8% a.a.**) por causa do
preço de compra elevado. A melhor combinação **receita ÷ preço de compra** aparece em
**Morretes** (7,9% a.a.), seguida por grupos de Centro e Meia Praia de 2 quartos
(ver `output/decision_table.csv`).

### P3 — Quais características explicam as melhores receitas?

Associação (não causalidade), com diária mediana e receita-base por imóvel:

| Característica | Correlação com diária | Correlação com receita-base |
|---|---|---|
| Nº de quartos | +0,58 | +0,60 |
| Nº de banheiros | +0,54 | +0,55 |
| Nº de hóspedes | +0,50 | +0,52 |
| Taxa de limpeza (cleaning_fee) | +0,38 | +0,39 |
| Nº de reviews | −0,17 | −0,16 |
| Nota (star_rating) | +0,06 | +0,07 |

![Características associadas a diária e receita](output/charts/6_caracteristicas.png)
*Figura 2 — Correlação (Spearman) entre características e diária/receita. Associação, não causa.*

- **Tamanho (quartos/banheiros/capacidade)** é o fator mais fortemente associado a receita maior.
- **Superhost** não diferencia a diária, em média: **R$ 575** para não-superhosts (565 imóveis)
  vs **R$ 518** para superhosts (434 imóveis), na amostra de imóveis com preço (n=999).
- `min_nights` não varia na base (n/d) — não há como avaliar.
- Imóveis com diária no p99 têm estrutura maior e estão em Meia Praia/Centro.

### P4 — O que a Seazone compraria hoje e por quê?

**Compraria apartamentos de 2 quartos em Morretes.** Retorno bruto estimado de ~7,9% a.a.
(base), ~5,6% (conservador) e ~10,7% (otimista); receita anual estimada ≈ R$ 62,7 mil (base,
seção 7). Preço estimado ≈ R$ 790 mil, sustentado por 1.037 anúncios de venda do mesmo perfil.
É a decisão mais defensável: retorno líder entre grupos de amostra razoável, com menor preço
de entrada que as alternativas comparadas.

## 3. Posição sobre a tese dos compactos (1 quarto) no Centro

**A tese NÃO vence na comparação da cidade — mas é a melhor opção dentro do Centro.**

- O grupo **1 quarto no Centro** tem retorno-base de **~7,0% a.a.**: superior às opções do
  próprio bairro, porém **inferior a Morretes 2q (7,9%)** entre os grupos de amostra confiável.
- Sua amostra de compra é **fina** (apenas **22 anúncios de venda**) — o preço estimado é menos sólido.
- Conclusão: a tese **se sustenta apenas como aposta local de bairro**, não como recomendação geral.
  Para presença no Centro, o 1q seria o melhor perfil lá; na comparação da cidade, Morretes 2q vence.

## 4. Comparação dos três candidatos

| Métrica | Morretes 2q | Meia Praia 2q | Centro 1q |
|---|---|---|---|
| Retorno base (% a.a.) | **7,9%** | 5,9% | 7,0% |
| Retorno conservador (% a.a.) | 5,6% | 4,2% | 5,0% |
| Retorno otimista (% a.a.) | 10,7% | 8,0% | 9,4% |
| Receita anual estimada (base, R$) | ≈62,7 mil | ≈64,0 mil | ≈62,0 mil |
| Preço de compra estimado (R$) | ≈790 mil | ≈1,08 milhão | ≈890 mil |
| Amostra Airbnb com preço | 51 | 187 | 78 |
| Amostra VivaReal (anúncios) | 1.037 | 243 | 22 |
| Confiança da amostra | Média/razoável | Alta | Compra fina |

![Comparação dos candidatos](output/charts/5_comparacao_candidatos.png)
*Figura 3 — Comparação de preço, retorno e amostra entre os três candidatos.*

**Por que Morretes 3 quartos não foi escolhido (retorno maior, 10,2% a.a.)?**
A amostra é pequena — **apenas 10 imóveis com preço** — abaixo do mínimo de confiança
(n≥30 para afirmações sólidas). Retorno alto com amostra fina pode ser efeito de acaso, e o
grupo aparece apenas quando o corte amostral é baixo. Morretes 2q tem base mais sólida.

**Por que a tese dos compactos no Centro não vence?**
Porque, na cidade, Morretes 2q tem retorno maior (7,9% vs 7,0%) e preço menor (R$ 790 mil vs
R$ 890 mil), com amostra de compra muito mais ampla (1.037 vs 22). O compacto só é superior
dentro do próprio Centro.

## 5. Metodologia e cuidados com os dados

- **Receita estimada por imóvel:** diária mediana das noites observadas (jan–abr/2025, o
  período com preço) → sazonalidade por mês → ocupação por cenário. Ver `scripts/03_revenue.py`
  e `scripts/config.py`.
- **Preço de compra:** mediana do `sale_price` do VivaReal por grupo (bairro normalizado +
  tipo + nº de quartos). Sem chave direta Airbnb↔VivaReal, o preço é **estatístico, não exato**.
- **Auditoria/limpeza:** 4.441 listings; preço para **999 (22,5%)**; capturas repetidas tratadas
  (mais recente por noite); hosts deduplicados por dono; VivaReal deduplicado, 98 sem bairro
  marcados. Ver `output/audit_report.md` e `output/clean_log.md`.
- **Cuidados-chave:** ausência de preço NÃO = ocupado; diária ≠ receita; sem metragem no Airbnb
  (sem R$/m²); **sem "liquidez"** — temos quantidade de anúncios, não velocidade de venda/fechamento.

## 6. Cenários de receita e retorno (premissas visíveis)

Premissas **ilustrativas** (ocupação mensal + fator de sazonalidade mai–dez) centralizadas em
`scripts/config.py`:

| Cenário | Ocupação jan–abr | Ocupação mai–dez | Fator de diária mai–dez |
|---|---|---|---|
| Conservador | 55–40% | 45–20% | ×0,55 |
| Base | 65–50% | 55–28% | ×0,70 |
| Otimista | 75–60% | 65–38% | ×0,85 |

(valores mensais exatos em `output/revenue_report.md`). **Essas taxas não representam ocupação
comprovada** — são cenários para testar sensibilidade. Retorno = receita estimada ÷ preço de
compra estimado (bruto, sem custos).

## 7. Robustez, limitações e dados necessários para uma compra real

**Testes de robustez** (ver `output/return_report.md`):
- **Corte amostral (5/10/15/20/30):** o top-5 muda entre cortes — por isso a tabela usa n≥10 e
  sinaliza confiança (≥30 = razoável). Morretes 3q só lidera em cortes baixos.
- **Regra de captura:** última vs média das capturas → correlação de ranks 0,994 (a ordenação quase não muda).
- **Outliers (10 imóveis ≈ 1%):** sinalizar/remover não muda o top-5 dos grupos elegíveis.

**Limitações:**
- Preço disponível só para 22,5%; 77% dos imóveis ficam sem análise de receita.
- Janela de preços **curta** (jan–abr/2025), que **inclui o pico de janeiro e a queda observada
  até abril** — **não representa o ano completo**; a projeção anual é sensível à sazonalidade (suposição).
- Sem ocupação real; sem custos (gestão, manutenção, IPTU, condomínio, impostos) → retorno é bruto.

**Para uma compra real, seriam necessários:**
- Histórico de ocupação/noites reservadas por imóvel;
- custos operacionais e impostos (IPTU, condomínio, gestão, manutenção);
- verificação de titularidade/área e visita técnica;
- tendências de demanda por bairro **ao longo do ano**.

## 8. Como reproduzir

Opção rápida — roda toda a análise na ordem correta:

```bash
pip install -r requirements.txt
python3 scripts/run_all.py
```

Ou, passo a passo (mesmas etapas do comando único):

```bash
pip install -r requirements.txt
python3 scripts/01_audit.py      # auditoria -> output/audit_report.md
python3 scripts/02_clean.py      # limpeza -> output/clean_log.md e output/processed/
python3 scripts/03_revenue.py    # receita por cenário -> output/revenue_report.md
python3 scripts/04_return.py     # retorno + tabela de decisão -> output/decision_table.csv
python3 scripts/06_features.py   # associação de características -> output/features_report.md
python3 scripts/05_charts.py     # visuais -> output/charts/*.png e *.svg
```

## 9. Estrutura do repositório e uso de IA

| Pasta / arquivo | Conteúdo |
|---|---|
| `BRIEF.md` | Planejamento da análise (objetivo, critérios, tratamento, limitações) |
| `scripts/` | Código reproduzível (01–06) + `config.py` (premissas dos cenários) |
| `output/*.md` / `.csv` | Relatórios e tabela de decisão |
| `output/charts/` | Visuais em PNG+SVG |
| `output/processed/` | Dados limpos (reproduzíveis, não versionados) |
| `ai-log/` | **Conversas com a IA em texto (sessão inteira) — já incluído** ([JSON](ai-log/opencode-session.json) · [Markdown](ai-log/opencode-session.md)) |
| `VIDEO_SCRIPT.md` | Roteiro do vídeo (~2min40) |
| `FINAL_CHECKLIST.md` | Itens obrigatórios da entrega |
| `data/` | Dados brutos do desafio |

**Gráficos (`output/charts/`):**
- `1_cobertura_amostras` — cobertura das amostras (Airbnb × VivaReal) por grupo.
- `2_preco_x_diaria` — relação entre preço de compra estimado e diária típica.
- `3_retorno_3_cenarios` — retorno bruto nos três cenários por grupo.
- `4_resumo_decisao` — cartões dos 3 candidatos (recomendação, alternativa, tese).
- `5_comparacao_candidatos` — comparação de preço, retorno e amostra.
- `6_caracteristicas` — características associadas a diária/receita (correlação).

**Como a IA foi utilizada:** as conversas completas estão em `ai-log/` (texto) —
[exportação oficial (JSON)](ai-log/opencode-session.json) e
[versão para leitura (Markdown)](ai-log/opencode-session.md) — com a iteração de análise,
decisões de metodologia, revisões críticas das escolhas e correções de qualidade dos dados,
documentadas para avaliação do processo.

## 10. Decisões tomadas com apoio da IA

De forma transparente, estas foram as decisões de metodologia nas quais a IA ajudou e que,
após revisão crítica, foram mantidas:

- **Taxa fixa de ocupação rejeitada e substituída por cenários**: em vez de chutar um
  percentual único (ex.: 50%), a receita usa três cenários (conservador/base/otimista) com
  premissas visíveis em `scripts/config.py`.
- **Ausência de preço mantida como desconhecida**: não foi tratada como "ocupado", "zero"
  ou "vendido" — imóvel sem preço fica fora da estimativa de receita, sem inferência.
- **Duplicidade de anfitriões corrigida antes da junção**: `Hosts_ids` tinha 4.440 linhas
  para 3.057 donos; foi deduplicado por `owner_id` para que a junção não multiplicasse linhas.
- **Grupos pequenos separados dos candidatos confiáveis**: apenas grupos com n≥10 entram na
  tabela de decisão; n<30 é marcado como baixa confiança, e a sensibilidade ao corte é
  reportada (Morretes 3q, por exemplo, só lidera com amostra fina).
- **Afirmações de sazonalidade e "liquidez" revisadas para não ultrapassar os dados**:
  a queda jan→abr é tratada como indício sujeito a validação (não como conclusão), e o termo
  "liquidez" foi evitado porque não há dado de velocidade de venda — usamos apenas tamanho de
  amostra de anúncios.

---

*Seazone — Jovens Talentos AI Builder 2026*