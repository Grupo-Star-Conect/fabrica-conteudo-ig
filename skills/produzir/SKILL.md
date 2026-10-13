---
name: produzir
description: Produz um post a partir de uma ideia da Fábrica, passando por TODAS as etapas e registrando cada uma na trilha (fonte, formato e ângulo, gancho, texto, legenda, hashtags, revisão anti-IA, briefing), chamando as skills do instagram-skills de verdade. Também faz ajuste de um post já produzido. Uso - /fabrica:produzir <id> [decida|reels|carrossel|post] ou /fabrica:produzir <id> ajuste: <pedido>. Chamado pelo botão Produzir e pelo Ajustar do app.
---

# /fabrica:produzir

**Camadas:** este arquivo é o SISTEMA (como a Fábrica produz). O que é da pessoa mora na pasta: `perfil/`, `meus-agentes/produzir.md` e `memoria/`. Nunca grave regra da pessoa aqui. Nunca troque o método por preferência dela: a preferência vai pra memória dela.

`FAB` = `python3 "<diretório base desta skill>/../../scripts/fab.py"`, rodado na pasta da Fábrica.

## 0. Carregar o contexto (sempre, antes de qualquer etapa)

Leia:
- `CLAUDE.md`;
- `perfil/marca.md`, `perfil/publico.md` (se existir), `perfil/voz.md`, `perfil/angulos.md`;
- `meus-agentes/produzir.md` (se existir);
- `memoria/aprendizado.md`;
- `memoria/o-que-funciona.md`;
- as análises em `memoria/videos/` (as 3 mais recentes, se existirem);
- a ideia: `FAB ideia <id>`.

A memória manda. Se `aprendizado.md` diz "ângulo X ruim" ou "não gosto de tom Y", isso vale aqui.

## Modo ajuste (`ajuste: <pedido>`)

1. Leia a trilha e o post atuais.
2. Refaça **só** as etapas que o pedido afeta. Ex.: "troca o gancho" mexe em gancho → texto → legenda → revisão. "Muda pra carrossel" refaz tudo a partir do formato.
3. Registre na trilha cada etapa refeita, com o nome "Ajuste · <etapa>".
4. Termine respondendo em 1-3 linhas o que mudou. A conversa do app guarda a resposta sozinha: não grave conversa na ideia.
5. Se o pedido soa como preferência fixa ("sempre", "nunca", "não gosto de", "prefiro"), **proponha** guardar: `FAB memoria aprendizado.md "- <data> · Regra pedida no ajuste: <regra>" --origem "ajuste <id>"`. Isso não grava: aparece no app pra ela confirmar. Diga na resposta "deixei a regra pra você confirmar".
6. Pule para o passo 9.

## Etapas (modo normal): cada uma termina com `FAB trilha`

Para registrar a saída, grave o texto num arquivo temporário (`.tmp-trilha.md` na pasta) e rode:
```
FAB trilha <id> "<Etapa>" "<skill ou ferramenta>" --arquivo .tmp-trilha.md
```
A saída registrada é o que a etapa produziu de fato: texto, decisão e motivo. Nunca escreva "feito".

1. **Fonte** (WebFetch). Abra o link da ideia. Anote os fatos que vão ser usados, cada um com o trecho que o sustenta. Se for link de post/vídeo de outra pessoa, use a análise já gravada pelo `trazer` (`resumo_fonte`). Sem link: escreva "sem fonte, conteúdo de opinião, bastidor ou educação", e nenhum número ou fato externo entra no post.
2. **Formato e ângulo** (decisão sua). Se veio `reels`, `carrossel` ou `post`, respeite. Se veio `decida`, escolha pelo que o conteúdo pede e pelo que `memoria/o-que-funciona.md` provou. Enquanto não houver prova, alterne formatos de propósito:
   - **falado pra câmera:** opinião, bastidor, história;
   - **tela dividida:** só quando existe algo visual pra reagir, como print de notícia, vídeo de outro perfil ou antes/depois;
   - **texto na tela + imagem de apoio:** lista, tese, dado forte;
   - **narração sobre tela:** tutorial;
   - **carrossel:** guia, passo a passo, lista salvável;
   - **post fixo:** uma frase-tese ou um dado só.

   Escolha categoria e virada em `perfil/angulos.md` e `<base>/../../referencias/angulos-e-formatos.md`. Registre formato, categoria, virada e **por quê**, em 2-3 linhas.
3. **Gancho** (Skill `instagram-skills:ig-hook-extractor`). **Chame a skill de verdade** com a ferramenta Skill e use as fórmulas dela. Gere 3 opções, escolha uma e diga por quê. Se as análises de vídeo mostram qual gancho segura o público dela, prefira esse.
4. **Texto** (o que vai na peça):
   - **Carrossel:** chame a Skill `instagram-skills:ig-carousel-planner` (só planejar, nunca publicar). Saída: o texto exato de cada slide, 5 a 8 slides, slide 1 = gancho, último fecha com frase mestra ou pergunta.
   - **Reels:** roteiro **falado** na voz dela.
     - Gancho palavra por palavra nos 3 primeiros segundos, depois pontos obrigatórios, depois fechamento.
     - Frases curtas.
     - Marque `[na tela: …]` só quando ajuda (tela dividida, print, texto).
     - Duração alvo.
   - **Post fixo:** texto da arte (título + no máximo 2 linhas de apoio).
5. **Legenda** (Skill `instagram-skills:ig-caption-writer`, **modo rascunho, nunca publicar**). Regras da legenda:
   - gancho nos primeiros 125 caracteres;
   - corpo escaneável;
   - um CTA, ligado ao objetivo do formato (`perfil/marca.md`).

   Se a ideia tem fonte, cite a fonte no fim.
6. **Hashtags** (Skill `instagram-skills:ig-hashtag-strategist`). Mistura de tamanhos, na quantidade do método.
7. **Revisão anti-IA** (Skill `instagram-skills:ig-humanizer`, modo auditoria e depois reescrita). Rode sobre slides/roteiro/texto da arte E legenda. A saída da trilha precisa listar **o que foi encontrado e o que mudou** (ex.: "travessão removido no slide 3", "'revolucionar' trocado por…"). Se nada mudou, diga que passou limpo e em quais critérios. Confira também `perfil/voz.md` (o que ela nunca diz).
8. **Briefing** (decisão sua):
   - **Carrossel e post fixo** (pro designer): formato 4:5 (1080×1350), o que vai visualmente em cada slide, onde entra print/imagem real (nunca inventada), destaque de texto.
   - **Reels** (pra quem grava e edita): enquadramento, se é tela dividida e com o quê, cortes, texto na tela, b-roll.

   Tudo curto e acionável.
9. **Salvar.** Um `FAB alterar` com:
   ```json
   {"tipo":"reels|carrossel|post","angulo":"…","categoria":"…",
    "post":{"formato_motivo":"…","roteiro":"…"|null,"slides":[…]|null,"texto_arte":"…"|null,"legenda":"…","hashtags":[…]},
    "briefing":"…","status":"pronto"}
   ```
   Depois `FAB historico "Produzido: <título> (<tipo>, <formato>)"`. Apague `.tmp-trilha.md`.

## Regras do sistema

- Toda etapa com skill **chama a skill** pela ferramenta Skill. Imitar de cabeça é falha.
- Nunca invente fato, número, nome, pesquisa ou citação.
- Texto que a pessoa trouxe (roteiro, rascunho) é lei: só formate, não reescreva o miolo.
- Rótulos de trabalho ("virada", "gancho", "categoria") nunca vão pro texto do post.
- Nunca publique daqui.
