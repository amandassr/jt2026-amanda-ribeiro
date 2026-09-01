# Relatório — Etapa 2b: preço de compra e retorno bruto


**Gerado por:** `scripts/04_return.py`

---


**As taxas de ocupação e os fatores de sazonalidade (mai–dez) são CENÁRIOS ILUSTRATIVOS** escolhidos para testar possibilidades e a sensibilidade da análise. Eles **não representam uma ocupação comprovada** do mercado de Itapema — a base não fornece noites reservadas. Qualquer conclusão que dependa desses números é uma suposição, não um fato.


## 1. Preço de compra estimado (mediana do VivaReal por grupo)


- Grupo = **bairro normalizado + tipo de imóvel + nº de quartos**.

- Preço = mediana do `sale_price` dos anúncios de venda do mesmo grupo.

- Amostra mínima VivaReal para estimar: **5** anúncios. Abaixo disso → marcado como **NÃO COMPARÁVEL** (sem aproximação silenciosa).

- Confiança: VivaReal 5–9 = **baixa**; ≥10 = **razoável**; Airbnb <10 = fora do corte de decisão; ≥30 = razoável.


Dimensões de cada lado (antes do join, após limpeza):

- Grupos no Airbnb com preço: 70 | imóveis: 999

- Grupos no VivaReal: 151 | anúncios: 8293


Grupos no TOTAL: 70 | não comparáveis (sem VivaReal suficiente): 38


## 2. Tabela de decisão — ORDENAÇÃO PRELIMINAR (NÃO é a recomendação final)


Grupos elegíveis (n_airbnb ≥ 10 com preço): 12


Leitura: **retorno_<cenario>(%)** = receita anual estimada ÷ preço de compra estimado, por ano.

Preços/receitas em R$.

                     bairro         tipo  quartos  n_airbnb(preço)  n_vivareal  diaria_tipica  preco_compra_est  receita_cons  receita_base  receita_otim  retorno_cons(%)  retorno_base(%)  retorno_otim(%)                          confianca
0                  Morretes  apartamento        3               10       155.0          611.0          845000.0       62068.0       86123.0      114919.0             7.35            10.19            13.60     AIRBNB_BAIXA / COMPRA_RAZOAVEL
1                  Morretes  apartamento        2               51      1037.0          464.0          790000.0       44322.0       62675.0       84780.0             5.61             7.93            10.73  AIRBNB_RAZOAVEL / COMPRA_RAZOAVEL
2   Tabuleiro dos Oliveiras  apartamento        2               12       110.0          425.0          780470.0       42969.0       60113.0       80516.0             5.51             7.70            10.32     AIRBNB_BAIXA / COMPRA_RAZOAVEL
3               Casa Branca  apartamento        2               11        20.0          350.0          655000.0       35275.0       49369.0       66143.0             5.39             7.54            10.10     AIRBNB_BAIXA / COMPRA_RAZOAVEL
4                Meia Praia  apartamento        1               20        58.0          441.0          877500.0       47405.0       66086.0       88936.0             5.40             7.53            10.14     AIRBNB_BAIXA / COMPRA_RAZOAVEL
5                    Centro  apartamento        1               78        22.0          445.0          890000.0       44371.0       62007.0       83387.0             4.99             6.97             9.37  AIRBNB_RAZOAVEL / COMPRA_RAZOAVEL
6                    Centro  apartamento        2               65        89.0          580.0         1150000.0       55186.0       78289.0      106000.0             4.80             6.81             9.22  AIRBNB_RAZOAVEL / COMPRA_RAZOAVEL
7                Meia Praia  apartamento        2              187       243.0          450.0         1080000.0       45806.0       64025.0       85827.0             4.24             5.93             7.95  AIRBNB_RAZOAVEL / COMPRA_RAZOAVEL
8                    Centro  apartamento        3               45       437.0          790.0         2100000.0       76286.0      107365.0      143683.0             3.63             5.11             6.84  AIRBNB_RAZOAVEL / COMPRA_RAZOAVEL
9                Meia Praia  apartamento        3              327      1697.0          655.0         1885000.0       65340.0       92038.0      123392.0             3.47             4.88             6.55  AIRBNB_RAZOAVEL / COMPRA_RAZOAVEL
10               Meia Praia  apartamento        4               60      1323.0         1012.0         3600000.0       98122.0      137943.0      185715.0             2.73             3.83             5.16  AIRBNB_RAZOAVEL / COMPRA_RAZOAVEL
11               Meia Praia       outros        1               11         NaN          160.0               NaN       16142.0       22703.0       30613.0              NaN              NaN              NaN      AIRBNB_BAIXA / NAO_COMPARAVEL



`s:output/decision_table.csv` e `output/processed/groups_return.csv` gravados.`


## 3. Sensibilidade ao corte amostral


Top-10 por retorno base para diferentes cortes mínimos de n_airbnb com preço (só grupos comparáveis no VivaReal). Verifica se o topo é estável ao corte.


- Corte n≥5: top-5 preserva 4 dos 5 do corte 10 (Morretes apartamento 3q, Morretes casa 2q, Morretes apartamento 2q, Tabuleiro dos Oliveiras apartamento 2q, Casa Branca apartamento 2q)

- Corte n≥15: top-5 preserva 2 dos 5 do corte 10 (Morretes apartamento 2q, Meia Praia apartamento 1q, Centro apartamento 1q, Centro apartamento 2q, Meia Praia apartamento 2q)

- Corte n≥20: top-5 preserva 2 dos 5 do corte 10 (Morretes apartamento 2q, Meia Praia apartamento 1q, Centro apartamento 1q, Centro apartamento 2q, Meia Praia apartamento 2q)

- Corte n≥30: top-5 preserva 1 dos 5 do corte 10 (Morretes apartamento 2q, Centro apartamento 1q, Centro apartamento 2q, Meia Praia apartamento 2q, Centro apartamento 3q)


Detalhe (corte 10): top-5 = ['Morretes apartamento 3q', 'Morretes apartamento 2q', 'Tabuleiro dos Oliveiras apartamento 2q', 'Casa Branca apartamento 2q', 'Meia Praia apartamento 1q']

Detalhe (corte 30): top-5 = ['Morretes apartamento 2q', 'Centro apartamento 1q', 'Centro apartamento 2q', 'Meia Praia apartamento 2q', 'Centro apartamento 3q']


## 4. Sensibilidade à regra de captura (última vs média das capturas)


Recomputa a diária representativa por imóvel usando **média das capturas** por (listing,date) e a receita por grupo; compara com a regra padrão (última captura).


- Correlação de ranks (receita base por imóvel, última vs média): 0.9940

- Imóveis com receita base variando >5% entre as regras: 131 / 999

- Ranks muito correlacionados → a regra de captura **não altera materialmente** a ordenação. Grupos instáveis serão apontados individualmente se necessário.


## 5. Sensibilidade a outliers da diária


- Critério outlier: diária > p99 (2304) ou < q1−3×IQR (-654).

- Imóveis sinalizados como outlier: 10 (1.0%). **Nenhum é excluído definitivamente**; aqui a comparação mostra como mudaria se SO_SINALIZAR ou se REMOVER (registro abaixo).


- Top-5 (COM todos os imóveis): ['Morretes apartamento 3q', 'Morretes apartamento 2q', 'Tabuleiro dos Oliveiras apartamento 2q', 'Casa Branca apartamento 2q', 'Meia Praia apartamento 1q']

- Top-5 (SEM outliers sinalizados, removidos só para esta comparação): ['Morretes apartamento 3q', 'Morretes apartamento 2q', 'Tabuleiro dos Oliveiras apartamento 2q', 'Casa Branca apartamento 2q', 'Meia Praia apartamento 1q']

- Top-3 preservados ao remover outliers: 3 de 3 → resultado estável


- Detalhe dos imóveis sinalizados como outlier (todos registrados): [30519162, 31167122, 40191152, 40289385, 40391575, 43300431, 44075219, 52758042, 995680028058206783, 1242002119123644781]


## 6. Tese dos compactos (1 quarto) no Centro


A tese preliminar interna sugeria que apartamentos compactos (studio/1q) no Centro seriam a aposta mais eficiente. O teste abaixo compara perfis DENTRO do Centro e o 1q-Centro contra os demais grupos comparáveis (não é a decisão final).


**Perfis no Centro (retorno base ordenado, % ao ano):**

  listing_type  number_of_bedrooms  n_airbnb  n_viva  diaria_p50  preco_compra  retorno_cons  retorno_base  retorno_otim
0  apartamento                   1        78    22.0       445.0      890000.0          4.99          6.97          9.37
1  apartamento                   2        65    89.0       580.0     1150000.0          4.80          6.81          9.22
2         casa                   3         2     5.0       675.0     1580000.0          4.18          5.88          7.90
3  apartamento                   3        45   437.0       790.0     2100000.0          3.63          5.11          6.84
4         casa                   4         4     7.0      1350.0     5198800.0          2.63          3.67          4.92
5  apartamento                   4         4   400.0       745.0     3700000.0          1.90          2.68          3.61
6  apartamento                   5         1    28.0       850.0     8665000.0          0.80          1.15          1.58



**O grupo 1q-Centro:** retorno base 6.97% | n_airbnb(preço)=78 | n_viva=22 | diária 445 | preço 890000

Posição do grupo no ranking geral de retorno base: 14º

