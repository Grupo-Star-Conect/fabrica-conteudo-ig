---
name: trazer
description: Transforma o que a pessoa trouxe - um tema, um link de notícia, um link de post ou vídeo de outra pessoa, um texto ou roteiro dela - numa ideia da Fábrica adaptada ao perfil dela. Vídeo de outra pessoa é ASSISTIDO de verdade (skill watch). Usado pelo campo "Trazer assunto" do app ou /fabrica:trazer <tema|link|texto>.
---

# /fabrica:trazer

`FAB` = `python3 "<diretório base desta skill>/../../scripts/fab.py"`, rodado na pasta.

Leia antes:
- `perfil/marca.md`, `perfil/voz.md`;
- `memoria/aprendizado.md`.

## Identificar o que veio

**Link de notícia ou artigo.** Abra (WebFetch) e resuma o fato com data. A fonte é o próprio link.

**Link de post, Reels ou vídeo** (Instagram, TikTok, YouTube, X). **Assista** com a Skill `watch:watch` (plugin claude-video):
- motor local;
- `--detail balanced`;
- `--out-dir .tmp-videos`;
- com `--cookies-from-browser chrome` só se `config.json` tiver `"chrome_autorizado": true`.

Olhe os frames e a transcrição e anote:
- o gancho dito e mostrado nos 3 primeiros segundos;
- a estrutura;
- os cortes;
- o formato (falado, tela dividida, texto na tela…);
- a tese.

Depois apague a pasta da execução (`python3 -c "import shutil;shutil.rmtree('<pasta da execução>')"`). Nada de mídia fica.

O `por_que` diz **como adaptar pro perfil dela**: o que copiar da estrutura, o que trocar pra voz e o público dela. Nunca copiar o texto. A fonte é o post original.

**Tema solto.** Se o tema afirma fato, ache a fonte oficial (WebSearch). Se é opinião ou educação, siga sem fonte.

**Texto ou roteiro dela.** É lei. Guarde inteiro em `resumo_fonte` e marque `"texto_proprio": true`. O `produzir` não reescreve o miolo.

## Gravar

```
FAB ideia-nova '{"titulo":"…","por_que":"…","fonte":{…}|null,"resumo_fonte":"…","tipo_sugerido":"…","origem":"trazido","texto_proprio":false}'
```

Depois `FAB historico "Trazido por você: <título>"`.

Responda em 2 linhas: o que entendeu e o ângulo proposto. A produção é quando ela clicar em Produzir.
