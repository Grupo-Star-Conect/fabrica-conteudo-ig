---
name: fila
description: Fila de produção da Fábrica de Conteúdo. Muda o status de uma pauta (escolhida, gravada, com designer/social, publicada, descartada), monta o pacote de entrega pro designer e pro social no formato que cada um usa, e publica carrossel ou imagem pela Publora quando ligado e com OK. Use com /fabrica:fila ou quando a pessoa disser "gravei a pauta X", "manda pro designer", "publica o carrossel", "o que tem na fila?".
---

# /fabrica:fila

Rode na pasta da Fábrica. Leia antes:
- `CLAUDE.md`;
- `perfil/equipe.md`;
- `config.json`.

Ache a pauta no painel (ArtifactData, `list` de `pautas`) pelo id ou pelo título que a pessoa disse. Se houver dúvida entre duas, pergunte qual.

## O que ela pode pedir

**"O que tem na fila?"**
Agrupe por status (`sugerida → escolhida → gravada → designer → publicada`), uma linha por pauta.

**Mudar status** ("gravei", "vou fazer", "descarta")
Faça `get` e depois `update` de `status` com `if_version`. Confirme em uma linha.

**Mandar pro designer ou pro social**
1. Monte `entregas/<data> - <titulo curto>.md` com:
   - o texto final pronto pra copiar (roteiro ou slides, legenda, hashtags);
   - o briefing de arte: formato (4:5 carrossel, 9:16 Reels), o que vai em cada slide, referência visual do perfil;
   - o prazo, se ela disse.
2. Adapte ao jeito de cada pessoa da equipe (`perfil/equipe.md`):
   - **WhatsApp:** gere também um bloco curto pronto pra colar;
   - **Drive:** diga o caminho do arquivo.
3. Mude o status pra `designer`.
4. Não envie mensagem a ninguém: entregue o texto pra ela mandar.

**Publicar** (só carrossel ou imagem, só com `config.json` → `publora: true`)
1. Mostre o cartão do que vai ao ar: imagens, legenda e horário.
2. Espere ela dizer "pode publicar".
3. Use o fluxo de publicação do `instagram-skills:ig-carousel-planner` ou `ig-caption-writer` (Publora), com as imagens que ela indicar.
4. Depois de publicado, mude o status pra `publicada` e grave a data.

**Sem Publora:** diga pra ela postar pelo app. Quando ela confirmar, marque `publicada`.

## Regras

- Nada vai ao ar sem "pode publicar" dito nesta conversa.
- Reels sempre é postado por ela. A Fábrica só entrega texto e marca status.
