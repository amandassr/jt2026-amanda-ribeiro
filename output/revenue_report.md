# Relatório — Etapa 2: Estimativa de receita potencial


**Gerado por:** `scripts/03_revenue.py`

---


## 1. Premissas dos cenários (SUPOSIÇÕES, não fatos)


**As taxas de ocupação e os fatores de sazonalidade (mai–dez) são CENÁRIOS ILUSTRATIVOS** escolhidos para testar possibilidades e a sensibilidade da análise. Eles **não representam uma ocupação comprovada** do mercado de Itapema — a base não fornece noites reservadas. Qualquer conclusão que dependa desses números é uma suposição, não um fato.


**Ocupação mensal (fração dos dias do mês ocupados)**

          conservador base otimista
Jan (31d)         55%  65%      75%
Feb (28d)         50%  60%      70%
Mar (31d)         45%  55%      65%
Apr (30d)         40%  50%      60%
May (31d)         25%  35%      45%
Jun (30d)         20%  28%      38%
Jul (31d)         25%  35%      45%
Aug (31d)         30%  40%      50%
Sep (30d)         25%  35%      45%
Oct (31d)         30%  40%      50%
Nov (30d)         35%  45%      55%
Dec (31d)         45%  55%      65%


**Fator de sazonalidade p/ meses não observados (mai–dez):** conservador 0.55, base 0.7, otimista 0.85

- jan–abr: usa a **mediana real** do preço de cada mês (dado observado).

- mai–dez: diária representativa × fator de sazonalidade (**suposição declarada**, edite em `scripts/config.py`).

- Estes valores foram escolhidos como referências e **serão testados por sensibilidade** (o resultado por imóvel pode mudar; o ranking comparativo de grupos tende a ser mais estável).


## 2. Diária representativa por imóvel (mediana das noites observadas)


- Imóveis com preço **e presentes no Details (base de análise)**: 999

  (removidos 6 imóveis sem bairro/tipo/quartos por não constarem no Details)

- Diária mediana (imóvel): p25 400 | p50 550 | p75 752

- Noites observadas por imóvel: min 2, mediana 62, máx 105


## 3. Receita anual estimada por cenário (distribuição por imóvel)


                              média      p25  p50 (mediana)       p75        máx
receita_anual_conservador   65248.0  40298.0        54532.0   73240.0   966275.0
receita_anual_base          91554.0  56306.0        76554.0  102965.0  1361650.0
receita_anual_otimista     122922.0  75412.0       102820.0  138769.0  1833825.0


## 4. Receita por grupo (bairro | tipo | quartos) — cenário BASE


(Apenas descrição da distribuição; **sem ranking**.)

Grupos com n>=10 imóveis com preço: 12

                                         n  rec_base_p50  rec_base_p75  diaria_p50
Meia Praia|apartamento|3               327       92038.0      113727.0       655.0
Meia Praia|apartamento|2               187       64025.0       80260.0       450.0
Centro|apartamento|1                    78       62007.0       73463.0       445.0
Centro|apartamento|2                    65       78289.0       96249.0       580.0
Meia Praia|apartamento|4                60      137943.0      218636.0      1012.0
Morretes|apartamento|2                  51       62675.0       76888.0       464.0
Centro|apartamento|3                    45      107365.0      116322.0       790.0
Meia Praia|apartamento|1                20       66086.0       75562.0       441.0
Tabuleiro dos Oliveiras|apartamento|2   12       60113.0       81692.0       425.0
Casa Branca|apartamento|2               11       49369.0       52566.0       350.0
Meia Praia|outros|1                     11       22703.0       28317.0       160.0
Morretes|apartamento|3                  10       86123.0      120478.0       611.0



## 5. Sanity check (diária)


- Imóveis com diária mediana acima do p99: 10 — mantidos para análise; são relevantes avaliar seu impacto.

- Imóveis com <15 noites observadas: 42 — receita menos confiável; serão identificados nas comparações.