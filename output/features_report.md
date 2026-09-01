# Características associadas a diárias e receitas maiores (associação, NÃO causalidade)

Base: 999 imóveis com preço. Diária = mediana das noites. Receita = estimada (cenário base). **Correlação de Spearman** (ordem, robusta a outliers).

     característica             diária receita_base
 number_of_bedrooms             +0.582       +0.596
number_of_bathrooms             +0.536       +0.552
   number_of_guests             +0.498       +0.515
  number_of_reviews             -0.166       -0.156
        star_rating             +0.059       +0.066
       cleaning_fee             +0.384       +0.393
         min_nights n/d (sem variação)          n/d


**Leitura:** valores positivos indicam que imóveis com mais daquela característica têm, em média, diária/receita maiores (associação). Não implica causalidade.


**Diária mediana por tipo de superhost (amostra: imóveis com preço):**
              n imóveis  diária mediana (R$)
is_superhost                                
False               565                575.0
True                434                518.0


**Diária mediana por tipo de imóvel:**
listing_type
apartamento    560.0
casa           500.0
hotel          330.0
outros         150.0


**Diária mediana por nº de quartos:**
number_of_bedrooms
0      435.0
1      385.0
2      450.0
3      650.0
4     1000.0
5     1500.0
6     2576.0
7     1325.0
12    2500.0
