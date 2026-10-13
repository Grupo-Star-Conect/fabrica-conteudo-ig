---
name: radar
description: Busca ideias de post pro perfil da pessoa - notícias e assuntos do nicho nas fontes aprovadas, filtrados pelo que ela já ensinou (memória). Entrega SÓ IDEIAS (assunto, fonte, por que serve), sem produzir o post; a produção acontece quando ela clica em Produzir. Roda pela rotina diária, pelo botão "Buscar ideias agora" do app ou com /fabrica:radar [assunto].
---

# /fabrica:radar

**Camadas:** este arquivo é o SISTEMA (como buscar). As fontes, os temas e o que a pessoa gosta ou não gosta moram na pasta dela (`perfil/fontes.md`, `meus-agentes/radar.md`, `memoria/`).

`FAB` = `python3 "<diretório base desta skill>/../../scripts/fab.py"`, rodado na pasta da Fábrica.

## 1. Contexto

Leia:
- `perfil/marca.md`, `perfil/publico.md` (se existir), `perfil/fontes.md`;
- `meus-agentes/radar.md`;
- `memoria/aprendizado.md`, `memoria/o-que-funciona.md`.

Rode `FAB ideias` pra ver o que já existe e não repetir (inclui as `arquivada` e `descartada`: não traga de novo).

**Dúvidas reais primeiro:** `dados/posts-perfil.json` traz `comentarios_recentes`. Pergunta de seguidor que ainda não virou ideia é a melhor pauta que existe.

**Aprendizado manda.**
- "Notícia ruim" de um tipo de assunto: pare de trazer esse tipo.
- "Notícia boa": traga mais do mesmo tipo.
- "Ângulo ruim": o assunto serve, então traga, mas no `por_que` proponha outro jeito de olhar.

## 2. Buscar

- Fontes de `perfil/fontes.md`: o que saiu nas últimas 72h (WebSearch + WebFetch na página de notícias).
- 2 ou 3 buscas amplas do nicho com as palavras que o público dela usa.
- Se veio um assunto como argumento, busque só ele.
- Abra cada link: precisa existir, ter data e dizer o que você vai dizer. Boato, notícia velha e tema bloqueado na memória saem.

## 3. Escolher e gravar ideias

Escolha a quantidade de `meus-agentes/radar.md` (padrão: 4). Critério: o que mais serve **ao público e ao objetivo dela**, não o que é maior na mídia.

Uma ideia pode ser sem notícia (bastidor, educação, história) quando o dia estiver fraco.

Para cada ideia:
```
FAB ideia-nova '{"titulo":"…","por_que":"2-3 linhas: por que isso interessa ao público dela e que ângulo dá","fonte":{"nome":"…","url":"…"} ou null,"resumo_fonte":"3-5 linhas do que a fonte diz, com data","tipo_sugerido":"reels|carrossel|post","origem":"radar"}'
```
Título curto e concreto, do jeito que ela falaria.

## 4. Memória

`FAB historico "Radar: N ideias (<títulos curtos>)"`.

Se você ignorou algo por causa da memória, anote numa linha. Ex.: "pulei 2 notícias de imposto, marcado como ruim".

## Regras

- Não produza post aqui. Só ideia.
- Nunca invente notícia, data ou número. Sem link que abre, não entra.
