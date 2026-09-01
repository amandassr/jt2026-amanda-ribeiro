# Log de Limpeza — Etapa 1
**Gerado por:** `scripts/02_clean.py`
**Data:** 2026-09-01 04:11

---

## T1. Price_AV — captura mais recente por (listing, date)


---

- Linhas antes: 118.839 | depois: 59.040 (removidas: 59.799)

---

- Listings únicos: 1005 | datas de estadia: 105

---

- Nenhum preço nulo após a limpeza: True


---

## T2. Hosts — uma linha por owner_id (captura mais recente)


---

- Linhas antes: 4.440 | depois: 3.057 (removidas: 1.383)

---

- Donos únicos: 3057


---

## T3. VivaReal — dedup de `listing_id` + bairro ausente marcado


---

- Linhas antes: 8.329 | depois: 8.293 (removidas: 36)

---

- `suburb` faltantes marcados como 'Desconhecido': 98


---

## T4. Normalização de bairros


---

Mapa de normalização (valor bruto -> canônico):

---

                      bruto                 canônico
0            alto sao bento           Alto Sao Bento
1                    centro                   Centro
2                meia praia               Meia Praia
3   meia praia - frente mar               Meia Praia
4        sertao do trombudo       Sertao do Trombudo
5               sertaozinho              Sertaozinho
6          jardim praia mar          Jardim Praiamar
7                 taboleiro  Tabuleiro dos Oliveiras
8                 tabuleiro  Tabuleiro dos Oliveiras
9              desconhecido             Desconhecido
10                andorinha                Andorinha
11           castelo branco           Castelo Branco
12                 estreito                 Estreito
13                  itapema                  Itapema
14              ocean tower              Ocean Tower


---

Aplicado em `Mesh` (Airbnb) e `VivaReal`. Valores do VivaReal que não existem no Mesh (`Andorinha`, `Castelo Branco`, `Estreito`, `Itapema`, `Ocean Tower`) ficam só como contexto do mercado de compra, sem correspondência com listings.


---

Distribuição dos bairros canônicos no Mesh:

---

                     suburb     n
0                Meia Praia  2860
1                    Centro   657
2                  Morretes   441
3   Tabuleiro dos Oliveiras   129
4               Casa Branca    88
5            Alto Sao Bento    62
6                    Ilhota    56
7                    Varzea    43
8            Canto da Praia    28
9        Sertao do Trombudo    22
10              Sertaozinho    21
11         Leopoldo Zarling    18
12                    Areal     5
13          Jardim Praiamar     5
14             Desconhecido     5
15                  Lameiro     1


---

Distribuição dos bairros canônicos no VivaReal:

---

                     suburb     n
0                Meia Praia  3455
1                  Morretes  1768
2                    Centro  1007
3                 Andorinha   779
4            Castelo Branco   506
5   Tabuleiro dos Oliveiras   134
6            Canto da Praia   131
7           Jardim Praiamar   104
8              Desconhecido    98
9               Casa Branca    95
10           Alto Sao Bento    66
11                   Ilhota    55
12                   Varzea    45
13       Sertao do Trombudo    41
14                 Estreito     5
15                  Itapema     2
16              Sertaozinho     1
17              Ocean Tower     1


---


- `vivareal_clean.csv` gravado com bairro normalizado (8293 linhas).


---

- `suburb` do Mesh marcados como 'Desconhecido' ('none'): 5


---

## T5. Verificação de integridade das junções


---

- Details + Mesh: 4441 -> 4441 linhas (1:1 OK)

---

- + Hosts (dedup por dono): 4441 -> 4441 linhas (OK, não multiplicou)

---

- 100% dos listings têm host na tabela de hosts (após dedup): 1

---

- Listings da `price_clean` presentes no Details: 999 / 1005

---

  (removidos da análise por não existirem no Details: 6)

---


- Base consolidada `base_airbnb.csv` gravada: 4441 linhas x 22 colunas.
