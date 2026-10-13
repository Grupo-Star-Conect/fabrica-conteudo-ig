---
name: analista
description: Lê o perfil da pessoa e das referências (Apify ou print), atualiza os números dos posts, fecha a análise de 7 dias de cada post publicado, cruza o que a Fábrica produziu com o resultado e grava na memória o que funciona (só com número). Uso - /fabrica:analista (semanal), /fabrica:analista vencidos (análise de 7 dias), /fabrica:analista print <id> <arquivos> (lê os prints dos insights). Também responde "por que esse post foi bem/mal?".
---

# /fabrica:analista

**Camadas:** o método é do SISTEMA (este arquivo). Os números e as conclusões são da pessoa e vão pra pasta dela (`dados/`, `memoria/`).

`FAB` = `python3 "<diretório base desta skill>/../../scripts/fab.py"`. `LER` = `python3 "<base>/../../scripts/ler_perfil.py" --env .env`.

## Modo `vencidos`: análise de 7 dias (rotina diária e botão do app)

Todo post marcado como publicado ganha `analisar_em` = 7 dias depois. Neste modo:

1. `FAB vencidos` lista os que já venceram. Se não houver nenhum, diga isso em uma linha e pare.
2. Para cada um:
   - **Achar o post.** Use `link_post`. Sem link, procure em `dados/posts-perfil.json` pela data (`publicado_em`, ±2 dias) e pela legenda. Se não achar, rode antes `LER <handle>` para atualizar.
   - **Números pela Apify:** `LER --posts <link>`. Grave em `ideia.resultado`: `{views, plays, curtidas, comentarios, compartilhamentos (se vier), duracao, lido_em}`.
   - **Comparar** com a média dela no mesmo formato (`dados/posts-perfil.json`): "1,4× a média de Reels", "abaixo da média".
   - **Trilha:** `FAB trilha <id> "Análise 7 dias" "Apify" --arquivo .tmp-trilha.md`, com os números, a comparação e uma leitura de 2-3 linhas (o que deu certo, o que repetir). Nunca chute o porquê sem base.
   - **Antes do print, o Chrome.** Se esta sessão tiver o Claude in Chrome (ferramentas `mcp__claude-in-chrome__*`) e `config.json` → `"chrome_dados": true`: abra o Meta Business Suite (business.facebook.com → Insights → Conteúdo) ou o post no instagram.com, logado como a pessoa, e leia alcance, salvamentos, compartilhamentos e retenção. Só leitura: nunca clique em publicar, impulsionar ou editar. Se ler, grave em `resultado.insights` e pule o pedido de print.
   - **Pedido de print.** A Apify não pega alcance, salvamentos, visitas ao perfil, seguidores pelo post, retenção, taxa de pulo nem tempo médio. Grave na ideia `FAB alterar <id> '{"pedido_print": "<texto>"}'` com o passo a passo:
     - **Post ou Reels:** "Abra o post no Instagram → toque em **Ver insights** (logo acima da legenda; se não aparecer, toque em ⋯ → Ver insights) → tire print da aba **Visão geral** e da aba **Engajamento**."
     - **Só Reels:** "Na mesma tela, desça até o **gráfico de retenção** e tire print também."
     - O app mostra esse pedido com um botão para enviar os prints.
   - **Status:** `FAB status <id> analisada`.
3. `FAB historico "Análise 7 dias: <N> posts"`.

## Modo `print <id> <arquivos>`: ler os prints dos insights

1. Abra cada imagem com Read e leia **só o que aparece**: visualizações, contas alcançadas, curtidas, comentários, salvamentos, compartilhamentos, visitas ao perfil, seguidores, taxa de pulo, tempo médio, e o ponto em que a curva de retenção cai.
2. Mescle em `ideia.resultado.insights` (`FAB alterar`), apague `pedido_print` (`"pedido_print": null`) e registre `FAB trilha <id> "Insights do Instagram" "print" --arquivo .tmp-trilha.md` com os números lidos e uma leitura curta.
3. **Retenção:** se houver gráfico e existir `memoria/videos/<shortcode>.md`, cruze o segundo da queda com a análise dos cortes ("caiu aos 6s, quando entra o segundo plano").
4. **Não** apague as imagens: o app apaga sozinho no fim. Nunca copie imagem pra outra pasta.

## 1. Números

- **Com Apify** (`config.json` → `"apify": true`): rode `LER <handle> <referências de perfil/referencias.md>`.
- **Sem Apify ou com erro:**
  - em conversa, peça o print do perfil e dos posts da semana;
  - na rotina, anote no histórico "faltou número: mandar print" e siga só com a fila.

Grave os posts dela em `dados/posts-perfil.json`: lista de `{id, url, formato, legenda, curtidas, comentarios, views, plays, duracao, slides, fixado, audio, hashtags, comentarios_recentes, data, tema}`. Mescle com o que já existe pelo `id`, sem duplicar e sem perder campos que já estavam lá.
- **`tema`** é seu: uma linha de 4 a 8 palavras dizendo do que o post fala (pela legenda e, se houver, pela análise em `memoria/videos/`). É o nome que o app mostra. Nunca deixe vazio.
- **`comentarios_recentes`:** se tiver pergunta de seguidor, ela é pauta. Mencione na leitura da semana.

Grave a semana em `dados/semanas.json`: lista. Atualize ou acrescente `{semana: "AAAA-Www", seguidores, engajamento, posts, referencias: [{handle, engajamento}], leitura}`.
- **Engajamento:** média de (curtidas+comentários)/seguidores×100 dos posts dos últimos 7 dias, 1 casa. Sem post na semana, use os últimos 6.

## 2. Cruzar Fábrica × resultado

1. Para cada ideia `publicada` (`FAB ideias --status publicada`), ache o post pela data e pela legenda.
2. Grave o resultado na ideia: `FAB alterar <id> '{"resultado":{…}}'`.
3. Agrupe por formato, categoria/ângulo e tipo de gancho, juntando também as análises de `memoria/videos/`. Compare cada grupo com a média dela.

## 3. Memória (o que deixa o sistema inteligente)

- **Provado:** grupo com 3 ou mais posts e média ≥ 1,3× a dela.
  `FAB salvar-direto o-que-funciona.md "- <data> · <padrão> · <N> posts · <X>× a média"` (número medido é fato e grava direto; preferência da pessoa nunca vai por aqui)
- **Repetição sem resultado:** 3 ou mais seguidos no mesmo formato, gancho ou tema, abaixo da média. Anote também no `o-que-funciona.md`, como "evitar".
- **Faltando teste:** formatos ainda sem dado entram na `leitura`, pro `produzir` variar.
- **Leitura da semana** (3 a 6 linhas, português simples, campo `leitura`):
  - o que rendeu e o que tem em comum;
  - o que ficou abaixo;
  - uma linha sobre as referências;
  - **Repetir:** …
  - **Parar:** …
- **Histórico:** `FAB historico "Análise semanal: <1 linha>"`.

## Pergunta avulsa "por que esse post foi bem?"

Se houver análise em `memoria/videos/`, use-a. Se não, assista com `/fabrica:assistir <link>`. Depois aplique a Skill `instagram-skills:ig-hook-extractor`: fórmula, por que funcionou, molde pra repetir.

## Regras

- Número só de fonte. Sem número, escreva "sem dado".
- Curtida não é alcance. Alcance, salvamento e retenção só por print dos insights (o pedido de print explica qual tela).
