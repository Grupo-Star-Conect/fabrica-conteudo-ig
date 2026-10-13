---
name: fabricar
description: Agente Fabricar da Fábrica de Conteúdo. Transforma uma pauta do painel, uma notícia, um link, uma ideia solta ou um texto da própria pessoa em post pronto (roteiro de Reels ou carrossel, legenda e hashtags) na voz dela e com o ângulo que funciona no perfil dela, usando as skills do instagram-skills por baixo. Use com /fabrica:fabricar [pauta|tema|link|texto] ou quando a pessoa pedir "faz um carrossel sobre", "roteiriza", "monta o post", "transforma isso em post".
---

# /fabrica:fabricar

Rode na pasta da Fábrica. Leia antes:
- `CLAUDE.md`;
- `perfil/*.md`;
- `meus-agentes/fabricar.md`.

O contexto da pessoa já está ali. **Não pergunte nicho, público, objetivo nem tom.** Só mude se ela pedir no próprio pedido.

## 1. Entender a entrada

| Entrada | O que fazer |
|---|---|
| Pauta do painel (id, título ou "a pauta 2") | `get` em `pautas/<id>` pelo ArtifactData |
| Link de notícia | Abra e leia. O fato vem dali |
| Ideia ou tema solto | Se o tema afirma fato, ache a fonte antes de escrever. Se é opinião, bastidor ou educação, siga |
| Texto da própria pessoa (roteiro, rascunho, áudio transcrito) | **É lei.** Use o texto dela, só arrume formato, gancho e legenda. Não reescreva o miolo |

**Formato:** se ela não disse, decida pelo `perfil/angulos.md` e pelo que funcionou no perfil. Pra ver o que funcionou, leia `posts` no painel, os de mais views ou curtidas.

## 2. Decidir antes de escrever (em silêncio)

- **Categoria:** análise de notícia, bastidor, história, educação, lista ou oferta. A oferta só existe se ela confirmou.
- **Virada:** qual das cinco, quando a categoria pede (ver `${CLAUDE_PLUGIN_ROOT}/referencias/angulos-e-formatos.md`).
- **Gancho:** escolha a fórmula pelo método do `instagram-skills:ig-hook-extractor` (as 10 fórmulas). Prefira a fórmula dos posts dela que mais performaram.
- **Frase mestra:** a ideia que o seguidor leva.

## 2b. Formato de vídeo (decisão sua, nunca pergunta pra pessoa)

Formatos de Reels:

| Formato | Quando usar |
|---|---|
| Falado pra câmera | Opinião, bastidor, história. O padrão quando não há imagem que prove |
| Tela dividida | A pessoa reage a algo visual: print de notícia, vídeo de outro perfil, antes/depois, comparação lado a lado. Só quando existe esse algo |
| Texto na tela + imagem de apoio (b-roll) | Lista curta, frase-tese, dado forte; ou quando a pessoa não pode gravar falando |
| Narração sobre tela | Tutorial, passo a passo no celular ou computador, mostrar um produto |

1. **Faça sentido primeiro.** O conteúdo decide: se não existe imagem pra reagir, não é tela dividida.
2. **Fase de teste.** Enquanto `meus-agentes/fabricar.md` não tiver "o que já está provado", alterne (se o arquivo não listar formatos em teste, alterne entre os quatro da tabela) entre os formatos em teste. Assim, em 2 a 3 semanas existe comparação. Não repita o mesmo formato mais de 2 vezes seguidas sem motivo.
3. **Com dado.** Quando houver o provado, use ele como padrão. Deixe 1 em cada 4 posts pra testar algo novo.
4. **Registro.** Grave a escolha em `formato_video` (ou `formato_carrossel`: lista, tese, passo a passo, antes/depois) e o motivo em uma linha. É isso que o analista cruza com o resultado.

## 3. Escrever

- **Reels:** roteiro **falado**.
  - Gancho nos primeiros 3 segundos.
  - Frases curtas, do jeito que ela fala (`perfil/voz.md`).
  - Duração do `meus-agentes/fabricar.md`.
  - Indique o que aparece na tela só quando ajuda (`[na tela: ...]`).
- **Carrossel:** use o método do `instagram-skills:ig-carousel-planner`.
  - Slide 1 = gancho.
  - Cada slide uma ideia.
  - Último slide fecha com a frase mestra ou uma pergunta.
  - Tamanho do `meus-agentes/fabricar.md`.
- **Legenda:** método do `instagram-skills:ig-caption-writer`.
  - Gancho nos primeiros 125 caracteres.
  - Corpo escaneável.
  - Um CTA só, ligado ao objetivo do formato.
- **Hashtags:** método do `instagram-skills:ig-hashtag-strategist`, na quantidade e no tamanho do perfil.
- **Passada final:** aplique o `instagram-skills:ig-humanizer` (modo auditoria) em tudo. Sem travessão, sem lista de emojis, sem frase de efeito vazia.

## 4. Mostrar e gravar

1. **Mostrar:** o post em blocos limpos, prontos pra copiar (roteiro ou slides, legenda, hashtags), mais uma linha dizendo o ângulo escolhido e por quê.
2. **Gravar no painel:**
   - **Pauta que já existia:** `update` em `post`, `titulo`, `gancho`, `categoria`, `angulo`, `formato_video` ou `formato_carrossel` e `motivo_formato`, com `if_version` da leitura.
   - **Pauta nova:** crie `pautas/<AAAAMMDD-x>` com `status: sugerida`, `origem: conversa` e os campos acima.
3. **Ajustes:** se ela pedir ajuste, refaça só o que ela pediu e grave de novo.
4. **Preferência fixa:** se o ajuste parece preferência fixa ("sempre mais curto", "nunca usa gíria"), pergunte se vira regra. Se ela disser que sim:
   - acrescente em `perfil/voz.md`;
   - acrescente em `regras` do documento `perfil/atual` do painel (`get` → `update` com `if_version`).

## Regras

- Nunca invente fato, número, nome, pesquisa ou citação.
- Rótulo de trabalho (categoria, "virada", "gancho") nunca aparece no texto do post.
- Nunca publique daqui. Publicar é com `/fabrica:fila`, depois do OK.
