---
name: analista
description: Lê o perfil da pessoa e das referências (Apify ou print), atualiza os números dos posts, cruza o que a Fábrica produziu e foi publicado com o resultado, e grava na memória o que funciona (só com número). Roda pela rotina semanal, pelo botão do app ou /fabrica:analista. Também responde "por que esse post foi bem/mal?".
---

# /fabrica:analista

**Camadas:** o método é do SISTEMA (este arquivo). Os números e as conclusões são da pessoa e vão pra pasta dela (`dados/`, `memoria/`).

`FAB` = `python3 "<diretório base desta skill>/../../scripts/fab.py"`. `LER` = `python3 "<base>/../../scripts/ler_perfil.py" --env .env`.

## 1. Números

- **Com Apify** (`config.json` → `"apify": true`): rode `LER <handle> <referências de perfil/referencias.md>`.
- **Sem Apify ou com erro:**
  - em conversa, peça o print do perfil e dos posts da semana;
  - na rotina, anote no histórico "faltou número: mandar print" e siga só com a fila.

Grave os posts dela em `dados/posts-perfil.json`: lista de `{id, url, formato, legenda, curtidas, comentarios, views, data}`. Mescle com o que já existe pelo `id`, sem duplicar.

Grave a semana em `dados/semanas.json`: lista. Atualize ou acrescente `{semana: "AAAA-Www", seguidores, engajamento, posts, referencias: [{handle, engajamento}], leitura}`.
- **Engajamento:** média de (curtidas+comentários)/seguidores×100 dos posts dos últimos 7 dias, 1 casa. Sem post na semana, use os últimos 6.

## 2. Cruzar Fábrica × resultado

1. Para cada ideia `publicada` (`FAB ideias --status publicada`), ache o post pela data e pela legenda.
2. Grave o resultado na ideia: `FAB alterar <id> '{"resultado":{…}}'`.
3. Agrupe por formato, categoria/ângulo e tipo de gancho, juntando também as análises de `memoria/videos/`. Compare cada grupo com a média dela.

## 3. Memória (o que deixa o sistema inteligente)

- **Provado:** grupo com 3 ou mais posts e média ≥ 1,3× a dela.
  `FAB memoria o-que-funciona.md "- <data> · <padrão> · <N> posts · <X>× a média"`
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
- Curtida não é alcance. Alcance e retenção só por print ou pelo painel profissional (versão futura).
