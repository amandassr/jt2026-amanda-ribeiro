# Final Checklist — itens obrigatórios da entrega

Marque cada item antes de enviar. Prazo: até as 9h (Brasília) do dia seguinte ao hackathon.
O formulário de entrega aceita um único envio.

---

## 1. Repositório

- [ ] Repositório **público** no GitHub com o nome `jt2026-primeiro-ultimo-nome`
- [ ] Contém análise, relatórios, tabela de decisão, gráficos e scripts

## 2. README.md

- [ ] **Primeira linha = link do vídeo** (Google Drive, "qualquer pessoa com o link")
  - atualmente `[PREENCHER ANTES DO ENVIO]` — substituir pelo link real antes de enviar
- [ ] Resumo executivo com a recomendação no início
- [ ] As **quatro perguntas** respondidas diretamente
- [ ] **Posição explícita** sobre a tese dos compactos (1 quarto no Centro)
- [ ] Comparativo entre Morretes 2q, Meia Praia 2q e Centro 1q
- [ ] Metodologia + cuidados com qualidade dos dados
- [ ] Cenários de receita/retorno com premissas visíveis
- [ ] Robustez, limitações e dados adicionais para compra real
- [ ] Como reproduzir a análise
- [ ] Estrutura do repositório + como a IA foi usada
- [ ] Recomendação **sem "liquidez"** (sem dado de velocidade de venda) e sem metragem inventada

## 3. Artefatos de análise

- [ ] `BRIEF.md`
- [ ] `scripts/01_audit.py` a `scripts/06_features.py` + `scripts/config.py`
- [ ] `output/audit_report.md`, `clean_log.md`, `revenue_report.md`, `return_report.md`, `features_report.md`
- [ ] `output/decision_table.csv`
- [ ] `output/charts/` — PNG e SVG (figuras 1 a 5, sem cortes nem sobreposições)
- [ ] Recomendação e receita/retorno sempre apresentados como **estimativas por cenários**

## 4. ai-log/

- [ ] Pasta `ai-log/` com conversas com a IA em **texto** (.md/.txt/.json)
- [ ] Sessão **inteira** exportada (não apenas um trecho)
- [ ] **Sem prints** como substituto — precisa ser texto legível

## 5. Vídeo (até 3 minutos)

- [ ] Subido no Google Drive com compartilhamento **"qualquer pessoa com o link"**
- [ ] Link na primeira linha do README
- [ ] Conta a recomendação, como usei a IA e o que faria com mais uma semana
- [ ] Duração <= 3min; roteiro em `VIDEO_SCRIPT.md`

## 6. Segurança

- [ ] `opencode.json` (e qualquer chave/secreto) **fora** do repositório
- [ ] Confirmar com `git check-ignore opencode.json`
- [ ] `output/processed/` fora do git (dados limpos reproduzíveis pelos scripts)

## 7. Conferência final

- [ ] Rodar todos os scripts do zero: `python3 scripts/01_audit.py` ... `python3 scripts/06_features.py`
- [ ] Abrir links em **aba anônima**: repositório abre? vídeo toca?
- [ ] `git status` sem arquivos indevidos; commits refletem o trabalho
- [ ] Preencher formulário de entrega só depois de conferir os links