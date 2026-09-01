#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
config.py — PREMISSAS CENTRAIS da análise de receita.

IMPORTANTE: as taxas de ocupação e os fatores de sazonalidade abaixo são
CENÁRIOS ILUSTRATIVOS escolhidos para TESTAR possibilidades e a sensibilidade
da análise. Eles NÃO representam uma ocupação comprovada do mercado de Itapema.
Não há dado de ocupação real na base.

Se quiser ajustar qualquer premissa, edite APENAS este arquivo.
Todos os scripts (03, 04, 05) leem daqui.
"""
import calendar

# ---------------------------------------------------------------------------
# Ocupação mensal (fração dos dias do mês em que o imóvel estaria ocupado)
# por cenário. Janeiro-abril são meses OBSERVADOS na base; mas a ocupação em si
# (quantas noites reservadas) nunca fornecida — logo estes números são suposições.
# ---------------------------------------------------------------------------
OCCUPANCY = {
    "conservador": {1:.55, 2:.50, 3:.45, 4:.40, 5:.25, 6:.20, 7:.25, 8:.30, 9:.25, 10:.30, 11:.35, 12:.45},
    "base":        {1:.65, 2:.60, 3:.55, 4:.50, 5:.35, 6:.28, 7:.35, 8:.40, 9:.35, 10:.40, 11:.45, 12:.55},
    "otimista":    {1:.75, 2:.70, 3:.65, 4:.60, 5:.45, 6:.38, 7:.45, 8:.50, 9:.45, 10:.50, 11:.55, 12:.65},
}

# ---------------------------------------------------------------------------
# Fator de sazonalidade aplicado à diária representativa do imóvel nos meses
# NÃO observados (mai–dez). Também é suposição ilustrativa.
# ---------------------------------------------------------------------------
SEASON_OUT = {
    "conservador": 0.55,
    "base":        0.70,
    "otimista":    0.85,
}

# Meses com preços observados na base (jan–abr/2025)
OBSERVED_MONTHS = [1, 2, 3, 4]

# Número de dias de cada mês (ano 2025)
DAYS = {m: calendar.monthrange(2025, m)[1] for m in range(1, 13)}

# Linguagem para o relatório
PREMSA_MOTIVACAO = (
    "**As taxas de ocupação e os fatores de sazonalidade (mai–dez) são CENÁRIOS "
    "ILUSTRATIVOS** escolhidos para testar possibilidades e a sensibilidade da análise. "
    "Eles **não representam uma ocupação comprovada** do mercado de Itapema — a base não "
    "fornece noites reservadas. Qualquer conclusão que dependa desses números é uma "
    "suposição, não um fato."
)