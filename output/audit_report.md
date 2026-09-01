# Relatório de Auditoria — Etapa 1
**Gerado por:** `scripts/01_audit.py`
**Data:** 2026-09-01 04:11

---

# 1. Estrutura das bases

                     arquivo   linhas  colunas              chave
0        Details_Itapema.csv    4,441       35  airbnb_listing_id
1      Hosts_ids_Itapema.csv    4,440       11           owner_id
2  Mesh_Ids_Data_Itapema.csv    4,441        8  airbnb_listing_id
3       Price_AV_Itapema.csv  118,839        4  airbnb_listing_id
4       VivaReal_Itapema.csv    8,329       22         listing_id


# 2. Dados ausentes por coluna


## 2.1 Details_Itapema.csv

              coluna  ausentes     %
3     ad_description        54   1.2
4              space      2527  56.9
13          check_in       446  10.0
14         check_out       842  19.0
25  can_instant_book       355   8.0
26   is_professional       355   8.0
33    is_new_listing       874  19.7


## 2.2 Hosts_ids_Itapema.csv

                coluna  ausentes      %
8  response_rate_shown      4440  100.0
9  response_time_shown      4440  100.0


## 2.3 Mesh_Ids_Data_Itapema.csv

* Sem campos vazios.


## 2.4 Price_AV_Itapema.csv

* Sem campos vazios.


## 2.5 VivaReal_Itapema.csv

               coluna  ausentes      %
7        rental_price      8327  100.0
8       rental_period      8327  100.0
9         yearly_iptu      2714   32.6
10  monthly_condo_fee      2490   29.9
16              state         2    0.0
18             suburb        98    1.2


# 3. Duplicidades de chave

**Details:** duplicatas em `airbnb_listing_id`: 0 | ids únicos: 4441 / 4441
**Mesh:** duplicatas em `airbnb_listing_id`: 0 | ids únicos: 4441 / 4441
**Price:** linhas duplicadas `(listing,date)`: 93.387 | pares afetados: 33.588
  Nº de capturas distintas dentro de cada par duplicado: {2: 7377, 3: 26211}
  Listings únicos no Price: 1005
**Hosts:** duplicatas em `owner_id`: 1.383 linhas (repetições) | linhas em chaves repetidas: 1.892 | donos únicos: 3.057 / 4440
  Das 1.892 linhas com chave repetida: nº de `host_snapshot_date` distintas por dono: {2: 309, 3: 89, 4: 43, 5: 18, 6: 11, 7: 6, 8: 4, 9: 3, 10: 3, 11: 4, 12: 1, 13: 2, 14: 3, 16: 1, 17: 1, 20: 1, 21: 1, 22: 1, 23: 2, 24: 1, 25: 1, 29: 1, 34: 1, 58: 1, 112: 1}
  Linhas repetidas que são IDÊNTICAS em todas as outras colunas: 0 | que DIFEREM em ao menos uma coluna: 1.892
**VivaReal:** duplicatas em `listing_id`: 36 | ids únicos: 8293 / 8329

# 4. Chaves e relações entre bases

**Details ↔ Mesh:** todos os ids do Mesh existem no Details? True; todos do Details no Mesh? True | (Diferença: 0)
**Price ↔ Details:** listings do Price fora do Details: 6 -> [np.int64(31122806), np.int64(1250122800440869898), np.int64(1286394668026043637), np.int64(1314095834089788250), np.int64(1318376138623084691), np.int64(1333504785474035960)]
  Listings com pelo menos um preço: 999 | sem preço: 3442
**Details ↔ Hosts:** owner_ids do Details existentes no Hosts: 3057 / 3057
**VivaReal ↔ Airbnb:** colunas em comum: ['amenities', 'aquisition_date', 'listing_type'] | NÃO há coluna de id comum -> sem ligação direta confiável.

# 5. Períodos das datas

                        base              coluna                     min                     max  qtde distinta
0        Details_Itapema.csv     aquisition_date 2025-01-13 01:54:03.000 2025-01-13 03:01:31.000           2624
1      Hosts_ids_Itapema.csv  host_snapshot_date 2025-01-13 01:54:03.000 2025-01-13 03:01:31.000           2624
2  Mesh_Ids_Data_Itapema.csv     aquisition_date 2021-10-25 14:40:16.352 2026-05-04 19:18:49.603           2362
3       Price_AV_Itapema.csv     aquisition_date 2025-01-06 13:22:07.000 2025-01-20 15:07:47.000           4172
4       VivaReal_Itapema.csv     aquisition_date 2025-01-11 00:00:00.000 2025-01-11 00:00:00.000              1

**Price (datas de estadia):** 2025-01-06 até 2025-04-20 | datas únicas: 105 | listings: 1005
  Nº de datas distintas por listing (janela): min 2, média 59, máx 105

# 6. Cobertura de preço por bairro, tipo e quartos

Imóveis com preço: 999 de 4441 (22.5%)

### 6.1 Por bairro

                         total  com_preco   pct
suburb                                         
Meia Praia                2860        632  22.1
Centro                     657        205  31.2
Morretes                   441         83  18.8
Tabuleiro dos Oliveiras    129         20  15.5
Casa Branca                 88         15  17.0
Alto Sao Bento              62          5   8.1
Ilhota                      56         10  17.9
Varzea                      43          5  11.6
Canto da Praia              28          9  32.1
Sertao do Trombudo          22          3  13.6
Sertaozinho                 21          6  28.6
Leopoldo Zarling            18          1   5.6
Areal                        5          1  20.0
Jardim Praiamar              5          1  20.0
Lameiro                      1          0   0.0


### 6.2 Por tipo de imóvel

              total  com_preco   pct
listing_type                        
apartamento    3710        911  24.6
casa            443         70  15.8
outros          245         17   6.9
hotel            43          1   2.3


### 6.3 Por nº de quartos

                    total  com_preco   pct
number_of_bedrooms                        
3                    1922        404  21.0
2                    1482        351  23.7
1                     549        144  26.2
4                     371         80  21.6
0                      56          8  14.3
5                      41          7  17.1
6                       6          2  33.3
7                       5          2  40.0
12                      4          1  25.0
10                      2          0   0.0
8                       1          0   0.0
11                      1          0   0.0
16                      1          0   0.0


# 7. Regra de captura para Price_AV

Regra primária mantida para cada `(listing, date)`: captura mais recente (`aquisition_date` máxima). Abaixo, a comparação de robustez entre regras.
n = 1005 imóveis com preço
- Correlação de ranks: 'última' vs 'primeira' = 0.9906 | 'última' vs 'média' = 0.9960 | 'primeira' vs 'média' = 0.9986
- Diferença % média ('última' vs 'primeira'): 2.48 | >5%: 16.7% | >20%: 1.2%

# 8. Indício de sazonalidade (a validar) e painel balanceado

Preço médio mensal (todos os imóveis observados):
   mês  preço médio
0    1        952.2
1    2        784.2
2    3        672.0
3    4        579.0

Imóveis observados em TODOS os 4 meses (painel balanceado): 565
Preço médio mensal RESTRITO ao painel balanceado:
   mês  preço médio (painel balanceado)
0    1                            980.5
1    2                            813.8
2    3                            706.5
3    4                            604.3

> Interpretação: se a queda persistir no painel balanceado, é mais provável sazonalidade; se sumir, era efeito de composição (troca de amostra entre meses).

# 9. Distribuição dos grupos (bairro|tipo|quartos) e limites de amostra

Grupos no Airbnb: 156 | imóveis com preço total: 999
   corte >= n imóveis com preço  grupos  imóveis nesses grupos
0                             5      16                    904
1                            10      12                    877
2                            15       8                    833
3                            20       8                    833
4                            30       7                    813

   corte >= n anúncios  grupos  anúncios
0                    3      94      8208
1                    5      70      8123
2                   10      49      7993
3                   20      35      7804
4                   30      25      7551

Grupos no VivaReal (dedup): 162

# 10. Qualidade do Price após regra 'última captura'

Linhas: 59.040 | listings: 1005 | datas: 105
Preço: min 63.0 | p1 160 | mediana 591.0 | p99 2500 | max 29000.0
Preço <=0: 0 | >3000: 390 | >5000: 183
Preços >5x a mediana do próprio imóvel: 1
Datas distintas por listing: min 2 | mediana 62.0 | max 105
Listings com <15 datas: 42 | <30: 141

# 11. Qualidade do VivaReal

Linhas: 8329 | duplicatas listing_id: 36 | suburb ausente: 98
sale_price ausente: 0 | <=0: 0
usable_area <=0: 11
sale_price percentis:
   percentil  sale_price
0       0.00     10000.0
1       0.01    450000.0
2       0.05    590000.0
3       0.50   1750000.0
4       0.95   6999000.0
5       0.99  12990736.0
6       1.00  44000000.0

listing_type: ['apartamento', 'casa', 'comercial', 'outros', 'terreno']
property_type: ['UNIT']

# 12. Bairros — divergências de grafia (para mapa de normalização)

Valores no Mesh (Airbnb):
Alto Sao Bento, Areal, Canto da Praia, Casa Branca, Centro, Ilhota, Jardim Praiamar, Lameiro, Leopoldo Zarling, Meia Praia, Morretes, Sertao do Trombudo, Sertaozinho, Tabuleiro dos Oliveiras, Varzea

Valores no VivaReal: 
Alto São Bento, Andorinha, CENTRO, Canto da Praia, Casa Branca, Castelo Branco, Centro, Estreito, Ilhota, Itapema, Jardim Praia Mar, MEIA PRAIA, Meia Praia, Meia Praia - Frente Mar, Meia praia, Morretes, Ocean Tower, Sertão Do Trombudo, Sertão do Trombudo, Sertãozinho, Taboleiro, Tabuleiro, Tabuleiro dos Oliveiras, Varzea, meia praia
