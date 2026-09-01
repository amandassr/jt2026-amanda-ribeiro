# ai-log — Registro das conversas com IA

Este diretório contém o registro completo das conversas entre o usuário e a IA (OpenCode)
durante o desenvolvimento desta análise.

| Arquivo | O que é |
|---|---|
| `opencode-session.json` | **Exportação oficial da sessão**, feita com `opencode export <id> --sanitize` (proteção de dados sensíveis). É a fonte canônica do processo. |
| `opencode-session.md` | **Versão para leitura** da mesma sessão, em Markdown, em ordem cronológica (mensagens do usuário, respostas da IA e registros das ferramentas), gerada a partir do JSON — sem resumir nem reescrever o conteúdo. |

- O **JSON** é o artefato oficial do OpenCode.
- O **Markdown** existe para facilitar a leitura/avaliação humana do processo.

> Valores sensíveis (caminhos, credenciais, conteúdos protegidos) estão marcados como
> `[redacted:...]` pela própria exportação.