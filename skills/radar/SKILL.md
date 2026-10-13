---
name: radar
description: Agente Radar da Fábrica de Conteúdo. Busca notícias e assuntos do nicho nas fontes aprovadas, guarda as notícias com link oficial e gera as pautas do dia (com o post já montado na voz da pessoa) direto no painel. Roda sozinho todo dia pela rotina agendada, ou à mão com /fabrica:radar. Com argumento busca um assunto específico - /fabrica:radar "lançamento X".
---

# /fabrica:radar

Rode na pasta da Fábrica. Antes de tudo, leia:
- `CLAUDE.md`;
- `perfil/marca.md`, `perfil/voz.md`, `perfil/angulos.md`, `perfil/fontes.md`;
- `meus-agentes/radar.md`;
- `config.json`.

Se `perfil/` não existir, diga para rodar `/fabrica:comecar` e pare.

## 1. O que já existe no painel

Com ArtifactData (`url` = `painel_url` do `config.json`), leia:
- `list` de `pautas` (limit 100): títulos e status;
- `list` de `noticias` (limit 100): urls.

Isso é pra não repetir pauta nem notícia.

## 2. Buscar

1. **Fontes:** para cada fonte de `perfil/fontes.md`, na ordem de `meus-agentes/radar.md`, busque o que saiu nas **últimas 48 horas** (WebSearch, WebFetch na página de notícias da fonte).
2. **Assunto em alta:** pesquise também 2 ou 3 buscas amplas do nicho ("<nicho> novidade hoje", termos que o público usa).
3. **Notícia que entra:** tem link oficial que abre, data clara e relação direta com o público da pessoa.
4. **Notícia que sai:** boato sem fonte, notícia velha requentada e tema da lista de evitar.
5. **Meta:** de 6 a 15 notícias. Abra o link de cada uma pra confirmar que existe e que diz o que você vai dizer.

Se veio argumento, busque só aquele assunto.

## 3. Montar as pautas

1. **Quantidade e mistura:** escolha as N melhores notícias, com N e a mistura Reels/carrossel definidos em `meus-agentes/radar.md`. **Melhor** = o que mais serve ao objetivo da pessoa e ao público dela, não o que é maior na mídia.
2. **Pauta sem notícia:** se a cadência pede e o dia está fraco, uma pauta pode vir de educação do nicho sem notícia. Nesse caso, `fonte` = null.
3. **Para cada pauta, decida:** categoria, ângulo e virada (de `perfil/angulos.md`), gancho e formato.
4. **Monte o post** seguindo o agente `/fabrica:fabricar` (as regras dele valem aqui):
   - **Reels:** roteiro falado + legenda + hashtags;
   - **Carrossel:** slides + legenda + hashtags.

## 4. Gravar no painel

Um `batch` só com ArtifactData:

- **`noticias/<id>`:** cada notícia nova. O id é slug curto do título, só letras, números e `-`, até 60 caracteres. Campos: `titulo, url, fonte, data, usada` (`true` se virou pauta hoje).
- **`pautas/<AAAAMMDD-n>`:** cada pauta. Campos:
  - `data` (hoje), `tipo` (`reels` | `carrossel`), `categoria`, `titulo`, `gancho`, `angulo`;
  - `fonte` (`{nome, url}` ou null);
  - `status`: `sugerida`;
  - `conversa`: `[]`;
  - `origem`: `radar`;
  - `post`: `{roteiro}` ou `{slides: [...]}`, mais `legenda` e `hashtags` (lista).

## 5. Fechar

1. **Pautas velhas:** pautas `sugerida` com mais de 7 dias passam pra `descartada` numa segunda escrita. Leia a versão de cada uma e use `if_version`.
2. **Na rotina automática:** termine com uma linha (quantas notícias, quantas pautas).
3. **Quando a pessoa rodou à mão:** liste as pautas em 1 linha cada e lembre o link do painel.

## Regras

- Nunca invente notícia, número, data ou citação. Sem link que abre, não entra.
- Uma pauta por notícia. Duas notícias do mesmo fato viram uma pauta só, com a fonte mais oficial.
- Hashtag pulse (Apify) **não** roda aqui: custa crédito. Só no analista semanal.
