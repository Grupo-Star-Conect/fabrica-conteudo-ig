# Fábrica de Conteúdo de @{{HANDLE}}

Esta pasta é a Fábrica de Conteúdo de Instagram de @{{HANDLE}}. Toda conversa aberta aqui já sabe quem é a pessoa: **nunca peça de novo nicho, público, objetivo ou voz**. Isso está nos arquivos abaixo, e você lê antes de qualquer pedido de conteúdo.

## Contexto fixo (ler sempre)

- `perfil/marca.md`: quem é, o que vende, pra quem, objetivo de cada formato
- `perfil/voz.md`: como fala, regras aprendidas, o que nunca diz
- `perfil/angulos.md`: ângulos e categorias que servem pra esse perfil
- `perfil/fontes.md`: de onde vêm as notícias do nicho
- `perfil/referencias.md`: perfis que servem de comparação
- `perfil/equipe.md`: pra quem vai cada post e como
- `config.json`: link do painel, se a Apify está ligada, horários

## Como pedir

Pedido curto basta: "faz um carrossel sobre X", "roteiriza a pauta 2", "por que meu último Reels foi bem?". Só mude objetivo, público ou tom quando a pessoa disser que quer fugir do padrão.

Os agentes da casa (já adaptados pra @{{HANDLE}}) estão em `meus-agentes/`:
- `/fabrica:radar` traz as pautas do dia com fonte
- `/fabrica:fabricar` transforma pauta, notícia ou ideia em post pronto
- `/fabrica:analista` lê o perfil e monta o comparativo
- `/fabrica:fila` muda status, entrega pro designer/social, publica
- `/fabrica:comecar` refaz uma parte do questionário (`/fabrica:comecar voz`)

## Regras

- Nunca inventar fato, número, pesquisa ou citação. Sem fonte, não entra.
- Texto que a pessoa traz é lei.
- Nada é publicado sem a pessoa dizer "pode publicar".
- Tudo que vira pauta ou post é gravado no painel (ferramenta ArtifactData, URL em `config.json`), pra aparecer lá.
- Quando a pessoa corrige um post de um jeito que parece preferência fixa, pergunte se vira regra e, se sim, acrescente em `perfil/voz.md` e no campo `regras` do documento `perfil/atual` do painel.
