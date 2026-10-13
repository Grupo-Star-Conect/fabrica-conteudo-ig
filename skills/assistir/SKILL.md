---
name: assistir
description: Assiste de verdade aos vídeos do próprio perfil da pessoa (frames + transcrição, via skill watch do plugin claude-video) e grava só a análise em texto em memoria/videos/ - gancho, estrutura, cortes, formato, tese, resultado. A mídia é apagada. Roda no /fabrica:comecar, pelo botão "Assistir aos vídeos novos" do app ou com /fabrica:assistir [links].
---

# /fabrica:assistir

`FAB` = `python3 "<diretório base desta skill>/../../scripts/fab.py"`.

## Quais vídeos

- **Vieram links:** use eles.
- **Não vieram:** pegue os Reels de `dados/posts-perfil.json` (lidos pela Apify), do mais recente pro mais antigo, que ainda **não** tenham `memoria/videos/<id>.md`. Até 8 por rodada.
- **Sem `posts-perfil.json`:** peça os links (se for conversa). Na rotina automática, anote no histórico que faltam links e pare.

## Para cada vídeo

1. **Assistir.** Chame a Skill `watch:watch`:
   - motor local (`--engine local`), `--detail balanced`;
   - `--out-dir .tmp-videos`;
   - `--cookies-from-browser chrome` se `config.json` → `"chrome_autorizado": true`.

   Se o download falhar por login e não houver autorização, registre no histórico e siga pro próximo.
2. **Olhar de verdade.** Leia os frames, principalmente os dos 3 primeiros segundos, e a transcrição. Não classifique nada que você não viu ou ouviu.
3. **Gravar** `memoria/videos/<id>.md`:
   ```markdown
   # <primeira frase falada ou título> · <data>
   Link: <url> · Duração: <s> · Resultado: <views/curtidas/comentários de posts-perfil.json, se houver>

   ## Gancho (0-3s)
   Dito: "…" · Na tela: … · Fórmula: <qual das fórmulas do ig-hook-extractor>
   ## Formato
   falado pra câmera | tela dividida | texto na tela | narração · enquadramento · ritmo de cortes (N cortes em Xs)
   ## Estrutura
   <passo a passo do vídeo, 3-6 linhas>
   ## Tese / frase mestra
   ## Transcrição
   <texto corrido, enxuto>
   ## Leitura
   <por que foi bem ou mal comparado à média dela, 2-3 linhas, sem chute>
   ```
4. **Limpar.** Apague a pasta da execução do watch (`python3 -c "import shutil;shutil.rmtree('<pasta da execução>')"`). Se `.tmp-videos` ficar vazia, apague também.

## Depois de todos

1. **Padrão.** Se já existem 4 ou mais análises, procure o que se repete: gancho, formato e tese dos que renderam acima da média dela.
2. **Memória.** Grave em `memoria/o-que-funciona.md` só o que tem número por trás: `FAB memoria o-que-funciona.md "- <data> · <padrão> · base: N vídeos, X× a média"`.
3. **Histórico.** `FAB historico "Assistidos N vídeos"`.
