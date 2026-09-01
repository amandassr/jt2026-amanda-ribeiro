# BRIEF — Hackathon Jovens Talentos AI Builder 2026 (Seazone)

> Documento de planejamento. Nenhuma análise, ranking ou recomendação foi feita ainda.
> Este brief é o contrato de trabalho: será usado como referência para todo o código e decisões a seguir.

---

## 1. Objetivo

Recomendar para a Seazone **onde e no que investir** no mercado imobiliário de Itapema (SC),
com base nos dados fornecidos (Airbnb + VivaReal), construindo a decisão de forma
defensável e registrando o processo de uso de IA.

## 2. Pergunta central

**Qual o imóvel (perfil + localização) que gera o melhor retorno sobre o valor de compra,
e por quê?**

Subperguntas do desafio:
1. Melhor perfil de imóvel (tipologia, nº de quartos, tipo de anúncio).
2. Melhor localização em termos de receita.
3. Quais características explicam as melhores receitas.
4. Se a Seazone fosse investir hoje, o que comprar e por quê (com estimativa de retorno).

## 3. Critérios da decisão

- **Critério principal: retorno bruto estimado** = receita potencial estimada ÷ preço de compra estimado.
  - É **bruto** (não temos custos: manutenção, gestão, impostos, vacância operacional).
  - É **estimativa** (não temos ocupação real confirmada, nem receita observada anual).
  - **Termo adotado: "retorno bruto estimado".** O nome "ROI" será evitado como rótulo principal,
    porque "ROI" costuma implicar resultado líquido de todos os custos, o que os dados não permitem.
    Quando o termo "ROI" for usado, será sempre qualificado como **"ROI bruto estimado"** (razão pura
    receita estimada ÷ preço estimado), nunca como retorno líquido.
- **Critérios de apoio:** preço de compra, nº de imóveis por grupo (nunca decidir com amostra pequena).
  - **Receita por área não será usada para comparar retorno**: o Airbnb não tem metragem, e não vamos inventá-la.
- **Transparência:** todo resultado reportado com o **nº de imóveis (n)** que o sustenta.

## 4. O que os dados comprovam, estimam e não permitem saber

| Item | Status |
|---|---|
| Perfil físico do anúncio Airbnb (tipo, quartos, banheiros, camas, hóspedes) | **Comprova** (Details) |
| Reviews, nota, nº de reviews por imóvel | **Comprova** (Details) |
| Perfil do anfitrião (superhost, anos, nº reviews) | **Comprova** (Hosts) |
| Bairro + lat/long de cada anúncio | **Comprova** (Mesh) |
| Preço de venda anunciado + área + quartos no VivaReal | **Comprova** (VivaReal, p/ anúncio de venda) |
| Diária anunciada por noite, jan–abr/2025, para 22,5% dos imóveis | **Comprova** (Price_AV) |
| Preço de compra de um imóvel Airbnb específico | **Estima** (via equivalência por grupo no VivaReal) |
| Receita potencial anual | **Estima** (só temos ~3,5 meses; usa cenários) |
| Retorno bruto estimado | **Estima** (resultado de duas estimativas) |
| Ocupação/estação "alta" do período | **Indício a validar** — há queda de preço jan→abr, mas a amostra muda mês a mês (ver seção 5.5) |
| **Ocupação real** (noites reservadas) | **Não permite saber** — ausência de preço NÃO = ocupado/zero/vendido |
| **Receita líquida** (descontando custos) | **Não permite saber** — não há custos na base |
| **Metragem do imóvel Airbnb** | **Não existe na base** — não será inventada |
| **Equivalência exata Airbnb ↔ VivaReal (mesmo imóvel)** | **Não permite saber com segurança** — não há chave comum |
| **Chave de anfitriões (`owner_id`) única** | **Não é única** — 3.057 donos em 4.440 linhas; 1.383 linhas repetem a chave (ver seção 5.9) |

## 5. Correções e nuances às primeiras escolhas

(fruto da inspeção estrutural; ajustam a abordagem para caber nos dados reais)

1. **Ligação direta Airbnb↔VivaReal: descartada como mecanismo.**
   Não existe coluna comum (o `listing_id` do VivaReal não corresponde ao `airbnb_listing_id`).
   Não há como garantir que um anúncio de venda represente o mesmo imóvel de um anúncio Airbnb.
   → Usamos **equivalência estatística por grupo** (bairro + tipo + nº de quartos), nunca match um-a-um.

2. **Sem área no Airbnb.** O Details não tem `usable_area`. Como não vamos inventar metragem:
   - Não faremos "R$/m²" no lado Airbnb.
   - Preço de compra estimado = **mediana do preço de venda** dos imóveis parecidos do VivaReal.
   - `R$/m²` pode aparecer **só dentro do VivaReal** como contexto, nunca para calcular o ROI.

3. **Nomes de bairro despadronizados entre as bases** (ex.: `Centro`/`CENTRO`, `Meia praia`/`MEIA PRAIA`,
   `Tabuleiro`/`Taboleiro`, e VivaReal com bairros que o Mesh nem tem, como `Castelo Branco`, `Andorinha`).
   → Será criado um **mapa de normalização** antes de qualquer cruzamento.

4. **Price_AV é "diária anunciada", não ocupação.** Cada linha = uma noite (`date`) de um imóvel,
   com o preço registrado numa captura (`aquisition_date`). Não há campo de reserva/ocupação.

5. **A queda jan–abr é um INDÍCIO, não uma conclusão sobre sazonalidade.** Checagem nos dados:
   preço médio mensal observado cai mês a mês (jan ≈ R$ 952 → fev ≈ 784 → mar ≈ 672 → abr ≈ 579),
   com pico no início de janeiro. Isso pode refletir (a) sazonalidade real OU (b) **efeito de composição**:
   os imóveis com preço em janeiro não são os mesmos de abril, então a queda pode ser só troca de amostra.
   → O tratamento será **validar** com um painel balanceado (imóveis observados em todos os meses) antes de
   atribuir a queda à sazonalidade. Enquanto isso, a sazonalidade entra na projeção apenas como
   **suposição declarada**, ajustada por mês.

6. **Regra da captura mais recente — defensável e checada.** Testamos a robustez comparando as regras
   "mais recente", "mais antiga", "média das capturas" e "mediana das capturas" para a média de diária
   por imóvel (n = 1.005):
   - Correlação de ranks: mais recente vs mais antiga = 0,99; mais recente vs média = 0,996.
   - Diferença média de valor ≈ 2,5%; apenas 1,2% dos imóveis muda >20% entre as regras.
   → **A escolha não altera materialmente a ordenação.** Regra mantida como primária ("última captura",
   = visão final do preço da noite), **com a regra "média das capturas" executada como checagem de
   robustez** (se um resultado mudar ao trocar a regra, ele é reportado como instável).

7. **Amostra pequena predomina.** A maioria dos 156 grupos (bairro×tipo×quartos) tem menos de 3
   imóveis com preço. Dados exatos que sustentam a regra:
   - Com mínimo de 10 imóveis com preço → só **12 grupos** entram (877 imóveis).
   - Com mínimo de 30 → **7 grupos** (813 imóveis).
   - VivaReal (dedup de anúncios): mínimo 10 → **49 grupos** (7.993 anúncios).
   → A regra de amostra mínima é obrigatória (seção 7), e os **limites serão testados por sensibilidade**.

8. **Qualidade dos dados (checada).**
   - Price_AV: sem preço vazio, sem zero/negativo; outliers altos existem (máx R$ 29.000; 400 registros
     > R$ 3.000; 1 preço >5× a mediana do próprio imóvel) → usar **mediana** (não média) como métrica-tipo.
   - VivaReal: 36 anúncios duplicados (`listing_id`) e 98 sem bairro → **deduplicar antes da mediana** e
     marcar "bairro desconhecido". `sale_price` sem vazios; some outliers (máx R$ 44M).
   - Details/Mesh: sem duplicatas de listing; 5 registros com `suburb = 'none'`.
   - **Junções não inflam linhas** (agregação a mediana por grupo); o risco é apenas dupla-contagem de
     anúncio duplicado — resolvido com o dedup.

9. **Verificação de chaves ANTES de qualquer junção (obrigatória e checada).** Unicidade por base:
   - `Details.airbnb_listing_id`: **única** (4.441/4.441).
   - `Mesh.airbnb_listing_id`: **única** (4.441/4.441), liga 1:1 com Details.
   - `Price.airbnb_listing_id`: **1.005 únicos**; 6 não existem no Details; logo 999 anúncios com preço.
   - `Hosts.owner_id`: **NÃO é única** — 3.057 donos em 4.440 linhas (1.383 linhas repetem a chave).
     These linhas repetidas têm snapshot diferente e serão deduplicadas para **uma linha por dono**
     (manter a captura mais recente do host), de modo que a junção Outline→Hosts **não multiplique linhas**.
   - `VivaReal.listing_id`: **36 duplicados** → dedup antes de qualquer uso.
   - Não existe chave comum entre VivaReal e Airbnb (ver seção 5.1).

## 6. Como cada base será tratada

### 6.1 Details_Itapema
- Base dos listings: tipo, quartos, banheiros, reviews, nota, cleaning_fee, min_nights, amenidades.
- Sem alterações de valor; apenas leitura e, se preciso, normalização de tipos.

### 6.2 Hosts_ids_Itapema
- `response_rate_shown` e `response_time_shown` estão **100% vazios** → desusados.
- **Antes de qualquer junção, deduplicar `owner_id` para uma linha por dono** (manter a captura mais
  recente do host). Sem isso, a junção com o Details multiplica linhas (ver seção 5.9).
- Usamos: superhost, anos/meses como host, nº de reviews do host, nota — como **contexto de demanda/reputação**, não como ocupação.

### 6.3 Mesh_Ids_Data_Itapema
- Fonte de **bairro** e localização; liga 1:1 com Details.
- `suburb = 'none'` (5 registros) será marcado como "bairro desconhecido" e tratado à parte.

### 6.4 Price_AV
- A principal base de receita. Cada registro = **preço de uma noite** (`date`) em uma captura (`aquisition_date`).
- **Tratamento de múltiplas capturas (linhas duplicadas):**
  - Causa: o mesmo `(listing, date)` foi capturado em momentos diferentes (a maioria com 3 capturas);
    o preço às vezes muda entre capturas (preço dinâmico).
  - **Regra primária (justificada):** manter apenas a **captura mais recente** (`aquisition_date` máxima)
    por `(listing, date)` — é a visão final do preço daquela noite; capturas antigas são intermediárias.
    Empate (mesma `aquisition_date`) resolvido de forma determinística.
  - **Robustez (obrigatória):** repetir a análise com a regra "média das capturas" e comparar
    (ver seção 5.6). Resultado que mudar ao trocar a regra é reportado como **instável**.
  - **Ausência de preço não significa reserva/ocupação/receita zero** — não será tratada como 0 nem inferida.
- **Diária ≠ receita, e sem pesar quem tem mais datas:**
  - Calculamos a **diária representativa por imóvel** (mediana das noites observadas daquele imóvel).
    Isso **não dá peso extra** a imóveis com mais datas: cada imóvel contribui com *um* valor,
    independente de quantas noites tem preço.
  - Agregação por grupo = mediana (ou distribuição) dessas diárias por imóvel — nunca soma de noites.
- **Comparação justa (mesmo período):**
  - As janelas de preço por imóvel variam. Comparamos métricas **normalizadas por noite coberta**
    (ex.: diária mediana, diária por mês), nunca totais brutos (que favoreceriam quem tem janela maior).
- **Projeção anual — sem multiplicação ingênua:**
  - Não multiplicar "média × 365 × ocupação" direto.
  - A sazonalidade é **mensal** (ver seção 5.5): jan é pico, depois cai. Ajuste por mês + ocupação
    = **suposições declaradas**, nunca fatos.
  - Projeção via **cenários** (seção 8). A diária observada é um **potencial de preço**, e a receita
    só existe quando multiplicamos por premissas de ocupação deixadas explícitas.

### 6.5 VivaReal
- Fonte do **preço de compra** (`sale_price`). `sale_price` e `usable_area` sempre preenchidos.
- **Limpeza antes do uso:** deduplicar `listing_id` (36 duplicados) e marcar bairro ausente (98 registros)
  como "bairro desconhecido" — nunca excluir sem registro.
- Preço de compra estimado de um grupo = **mediana do `sale_price`** dos anúncios de venda do mesmo
  (bairro normalizado + tipo + nº de quartos). Uso da mediana (robusta a outliers).
  Grupo sem anúncios suficientes no VivaReal → sem estimativa de compra → fica fora do comparativo de
  retorno (ou reportado como "preço não estimável").
- A junção agrega cada grupo a **um** valor (mediana) → não multiplica linhas; o risco era dupla-contagem
  de anúncio duplicado, já tratado no dedup.
- Bairro normalizado pelo mapa da seção 5.3.

## 7. Amostra mínima razoável

Distribuição real dos grupos (observada, sem ranking), que fundamenta a regra:

- Airbnb (156 grupos): com mínimo de 10 imóveis com preço entram **12 grupos** (877 imóveis);
  com mínimo de 30 entram **7 grupos** (813 imóveis).
- VivaReal (162 grupos, já deduplicado): com mínimo de 10 anúncios entram **49 grupos** (7.993 anúncios).

**Regra proposta (não fixa — será testada por sensibilidade):**
- **Corte primário: mínimo de 10 imóveis com preço** por grupo para comparar receita/retorno.
- Grupos com n entre 10 e 29 → reportar com a marca **"confiança baixa"**.
- Grupos com n ≥ 30 → **"confiança razoável"**.
- **Sensibilidade obrigatória:** repetir a análise com os cortes **5, 15, 20 e 30** e verificar se os
  grupos no topo se mantêm. Se a conclusão mudar conforme o corte, ela é **instável ao corte** e será
  reportada como tal (não apresentada como conclusão firme).
- **Todo resultado mostra o n.** Nenhuma exclusão de grupo/registro acontece sem ficar registrada.

## 8. Cenários (conservador / base / otimista)

Como a janela é curta e há um **indício de queda de preço entre jan e abr** (a validar, seção 5.5),
a receita anual será estimada por cenários, cada um com premissas explícitas e reportadas:

- **Conservador:** ocupação baixa + ajuste de sazonalidade forte (janeiro é pico e infla a janela).
- **Base:** ocupação de referência + sazonalidade mensal média (mais defensável).
- **Otimista:** ocupação alta + sazonalidade suave.

**IMPORTANTE: as taxas de ocupação e os fatores de sazonalidade (mai–dez) são CENÁRIOS
ILUSTRATIVOS escolhidos para TESTAR possibilidades e a sensibilidade da análise. Eles NÃO
representam uma ocupação comprovada do mercado de Itapema** — a base não fornece noites reservadas.
Qualquer conclusão que dependa desses números é suposição, não fato.

As premissas (ocupação % por mês × fator fora da janela) ficam reunidas e centralizadas em
`scripts/config.py`, num único lugar **fácil de alterar**. Todos os scripts de análise leem dali.
Premissas são declaradas em tabela, de forma explícita e separadas do que é **comprovado**.
Mostraremos **como o resultado muda entre cenários**.
Nenhum número será tratado como "o valor certo" — a diária observada é um **potencial de preço**,
não uma receita; receita só aparece multiplicada por premissas de ocupação deixadas claras.

## 9. Papel dos proxies (demanda, não ocupação)

- `number_of_reviews`, `star_rating`, `is_superhost`, `guest_satisfaction` etc.
  serão usados **somente como contexto de demanda/reputação** para qualificar os resultados.
- **Não** serão convertidos em ocupação, receita ou noites reservadas.
- **Receita por m² NÃO será usada para comparar retorno**: o Airbnb não tem metragem,
  e não vamos inventá-la. `R$/m²` só aparece internamente no VivaReal (como nomenclatura de mercado),
  nunca no cálculo do retorno.

## 10. Etapas da análise (sequência de trabalho)

1. Limpeza e normalização (bairros, capturas de preço, tipos, dedup de VivaReal **e de Hosts por dono**,
   marcação de bairro desconhecido — cada exclusão registrada), **após verificação de chaves** (seção 5.9).
2. Dicionário de grupos e checagem de distribuição → aplicar regra de amostra mínima (seção 7).
3. **Robustez da regra de captura:** comparar "última" vs "média das capturas" (seção 5.6).
4. Preço de compra estimado por grupo (mediana VivaReal, bairro+tipo+quartos, pós-dedup).
5. Diária representativa por imóvel (mediana, sem peso por nº de datas) e cenários de receita (seção 8).
6. Retorno bruto estimado por imóvel → agregação por grupo, sempre com n e cenários.
7. **Sensibilidade ao corte amostral (5/10/15/20/30)** — verificar se o topo se mantém (seção 7).
8. **Testar explicitamente a tese dos compactos (1q) no Centro** — sustentar OU contestar com números.
9. Sanity check final: outliers, grupos pequenos, janelas de captura, sazonalidade mensal.
10. Redigir recomendação final (README/relatorio.md) + posição sobre a tese + limitações honestas.
11. Registrar conversas com IA em texto na pasta `ai-log/` (sessão inteira).
12. Vídeo de até 3 min (Drive, link na 1ª linha do README) + checklist final.

## 11. Limitações (registradas desde o início)

- Sem ocupação real → receita é estimativa por cenário (suposição explícita).
- Sem custos → retorno é **bruto**, não líquido. Por isso o termo é "retorno bruto estimado".
- Sem metragem do Airbnb → preço de compra por equivalência de grupo, não por m²; **sem receita/m²**.
- Janela de preços de ~3,5 meses (jan–abr), com **indício de queda** (a validar) → projeção anual sensível
  à sazonalidade (suposição), tratada por mês e por cenários.
- Preço disponível para 22,5% dos imóveis → 77% ficam sem receita estimável (e sem comparar por retorno).
- Sem chave entre Airbnb e VivaReal → preço de compra é estatístico, não exato.
- Nomes de bairro e tipos divergem entre bases → exige normalização.
- Qualidade/outliers: duplicatas no VivaReal (36) e no Price (capturas repetidas), **duplicatas de dono no
  Hosts (1.383 linhas)**, outliers altos de preço, 98 anúncios sem bairro, 5 Mesh sem bairro → tratados com
  dedup + mediana + registro de cada exclusão.

## 12. Regras de trabalho

- **Não inventar dados** (metragem, ocupação, preços).
- **Não consultar entregas/trabalhos de outros participantes.**
- Distinguir sempre, em cada etapa: o que é **comprovado**, o que é **aproximação/estimativa**,
  o que é **suposição** e o que **não sabemos**.
- Questionar qualquer conclusão que dependa de amostra pequena ou de um único corte.
- IA é ferramenta e o processo fica registrado em texto.