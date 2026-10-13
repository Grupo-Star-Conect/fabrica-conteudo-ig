---
name: fila
description: Fila de produção da Fábrica - status das ideias e posts, pacote de entrega pro designer e pro social, e publicação de carrossel/imagem pela Publora quando ligada e com OK. Use com /fabrica:fila [entregar <id>] ou quando a pessoa disser "o que tem na fila?", "gravei o X", "manda pro designer", "publica o carrossel".
---

# /fabrica:fila

`FAB` = `python3 "<diretório base desta skill>/../../scripts/fab.py"`. Leia `perfil/equipe.md` e `config.json`.

## O que a pessoa pode pedir

**"O que tem na fila?"**
Rode `FAB ideias` e agrupe por status (`ideia → pronto → escolhida → gravada → designer → publicada`).

**Mudar status** ("gravei", "vou fazer", "publiquei")
Rode `FAB status <id> <status>`.

**`entregar <id>`**
1. Monte `entregas/<data> - <título curto>.md` com:
   - o texto final pronto pra copiar (slides, roteiro ou texto da arte, legenda, hashtags);
   - o briefing;
   - o prazo, se houver.
2. Pra cada pessoa de `perfil/equipe.md`, faça um bloco curto no formato que ela usa (ex.: WhatsApp). Ninguém recebe mensagem daqui: a pessoa copia e manda.
3. Rode `FAB status <id> designer` e `FAB historico "Entregue: <título>"`.

**Publicar** (só carrossel ou imagem, só com `config.json` → `"publora": true`)
1. Mostre o que vai ao ar.
2. Espere "pode publicar".
3. Use o fluxo de publicação do `instagram-skills` (Publora).
4. Rode `FAB status <id> publicada`.

Na rotina e no app, publicar nunca acontece: só em conversa, com OK.
