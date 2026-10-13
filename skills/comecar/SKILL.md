---
name: comecar
description: Questionário de instalação da Fábrica de Conteúdo. Entende quem é a pessoa, lê o perfil do Instagram, assiste aos vídeos dela, confirma voz, público, objetivos, fontes e referências, ADAPTA os agentes ao perfil, cria a memória, abre o app local e agenda as rotinas. Rode com /fabrica:comecar na pasta onde a Fábrica vai morar. Com argumento refaz só um bloco - /fabrica:comecar voz | angulos | fontes | referencias | volume | equipe | publicar | migrar.
---

# /fabrica:comecar

Você vai configurar a Fábrica de Conteúdo de Instagram de uma pessoa. No fim, ela tem:
- a pasta pronta;
- os agentes reescritos pro perfil dela;
- a memória dela começada (vídeos assistidos, o que funciona);
- o app da Fábrica aberto no computador;
- as primeiras ideias;
- as rotinas agendadas.

A pessoa nunca mais vai precisar explicar nicho, público ou objetivo.

**Tom:** conversa de gente, em português do Brasil, frases curtas. Uma pergunta por vez, sempre aberta, com uma linha de subtexto dizendo o que você quer saber. Nunca ofereça opção pronta pra resposta que só ela sabe. Quando você já tem a resposta (da bio, dos posts), mostre o que entendeu e pergunte "é isso? muda algo?".

**Pergunte só o que só a pessoa sabe.** Fato da vida dela pode ser perguntado: o que vende, pra quem, quanto consegue produzir, quem é a equipe, como fala. Decisão de criação **nunca** vira pergunta: quando usar tela dividida, texto na tela ou narração, qual gancho, qual ângulo, que dia postar. Essas decisões são trabalho da Fábrica. Ela testa variações enquanto não tem dado e repete o que funcionou quando passa a ter. Se a pessoa disser "não sei" ou "decide você", isso é a resposta certa: registre que a Fábrica decide e siga.

**Pasta de trabalho:** a pasta atual. `PLUGIN` = `<diretório base desta skill>/../..`. `FAB` = `python3 "PLUGIN/scripts/fab.py"`.

**Camadas:** o plugin é o SISTEMA (método, etapas, app) e atualiza sozinho. A pasta é da PESSOA (perfil, agentes adaptados, memória, dados) e nenhuma atualização mexe nela. Tudo que você descobre sobre ela vai pra pasta.

## Passo 0. Conferir a casa

1. **Refazer um bloco.** Se veio argumento (`voz`, `angulos`, `fontes`, `referencias`, `formatos`, `equipe`, `publicar`, `painel`) e `perfil/` já existe:
   - leia os arquivos atuais;
   - refaça só aquele bloco;
   - mostre antes/depois;
   - grave nos arquivos;
   - termine. Pule o resto deste roteiro.
1b. **Migrar da versão antiga.** Se `config.json` tem `painel_url` (versão com painel no Claude) ou veio o argumento `migrar`:
   - crie `memoria/` e `dados/`;
   - traga as pautas do painel antigo como ideias (ArtifactData `list` em `pautas` com o `painel_url`; pra cada uma, `FAB ideia-nova` com título, fonte e `por_que` = ângulo). Essa ferramenta só existe na conversa do app do Claude, não nos botões do app da Fábrica. Se não estiver disponível, peça pra pessoa colar o título de cada pauta antiga (ou siga sem elas) e diga isso em uma linha;
   - renomeie `meus-agentes/fabricar.md` pra `meus-agentes/produzir.md`;
   - troque o `CLAUDE.md` pelo modelo novo;
   - tire `painel_url` do `config.json`;
   - crie `memoria/aprendizado.md` com o que o `perfil/voz.md` já diz que ela nunca faz;
   - siga pro Passo 5b (assistir aos vídeos) e depois os itens 8 a 11 do Passo 10 (ideias, rotinas, app, fechamento). Não refaça as perguntas. Se já existirem tarefas agendadas da versão antiga, troque o prompt delas pelos novos.
2. **Já instalado.** Se `perfil/` existe e não veio argumento, pergunte se é pra refazer tudo ou só um bloco.
3. **Dependências.** A Fábrica usa dois plugins abertos do GitHub:
   - `instagram-skills`: legenda, carrossel, gancho, hashtag, anti-IA;
   - `watch` (claude-video): assistir a vídeo com frames e transcrição.

   Confira se `instagram-skills:ig-humanizer` e `watch:watch` estão disponíveis. Se faltar algum, pare e mostre o que falta:
   ```
   claude plugin marketplace add sergebulaev/instagram-skills
   claude plugin install instagram-skills@instagram-skills
   claude plugin marketplace add bradautomates/claude-video
   claude plugin install watch@claude-video
   ```
   Depois de instalar, a pessoa abre uma conversa nova e roda `/fabrica:comecar` de novo.
4. **Abertura.** Diga em 3 linhas o que vai acontecer: umas 10 perguntas (cerca de 15 minutos). Depois a Fábrica assiste a alguns vídeos dela e abre o app com as primeiras ideias.

## Passo 1. Perfil

Pergunte o @ do Instagram.

Depois pergunte como ela quer que você leia o perfil e as referências. Explique as duas opções em uma linha cada:
- **Mandar print ou colar os posts:** grátis, mas você mesma manda quando eu pedir.
- **Conectar a Apify:** grátis até US$5 por mês, e eu leio sozinho toda semana. Leva uns 3 minutos pra conectar.

**Se escolher Apify:**
1. Passo a passo:
   - criar conta em https://console.apify.com/sign-up (dá pra entrar com Google);
   - abrir https://console.apify.com/settings/integrations;
   - copiar o "Personal API token";
   - colar aqui.
2. Grave o token em `.env` na pasta (`APIFY_TOKEN=...`). Avise que ele fica só nesse arquivo, no computador dela.
3. Garanta que `.env` não seja publicado. Crie `.gitignore` com `.env` se a pasta for virar repositório.
4. Rode e grave os posts em `dados/posts-perfil.json` (lista `{id,url,formato,legenda,curtidas,comentarios,views,data}`):
   ```
   python3 "PLUGIN/scripts/ler_perfil.py" --env .env <handle>
   ```
5. Se der `sem_token` ou `token inválido`, ajude a corrigir. Se der erro de rede ou crédito, siga pelo caminho do print.

**Se escolher print:** peça um print do topo do perfil (bio e números). Peça também os 6 a 10 últimos posts: print da grade, ou link + legenda colada + curtidas e comentários de cada um.

Com o que leu, escreva **o que entendeu** e peça confirmação:
- nicho;
- o que vende ou oferece;
- pra quem;
- objetivo do Instagram (vender, autoridade, crescer, atrair cliente);
- o que mais funcionou entre os posts, e por quê, em uma frase.

Pergunte o que ajustar.

## Passo 1a. Buscar contexto antes de perguntar

Antes de qualquer pergunta nova, junte sozinho o que já está público:
- **Bio e link da bio:** abra o site ou a página do link (WebFetch). Anote o que vende, para quem, preço se houver, depoimentos e casos.
- **Busca na web** pelo nome do negócio ou da pessoa: reportagens, Google Meu Negócio, avaliações (o que os clientes elogiam e reclamam, com as palavras deles).
- **Comentários dos posts** (`comentarios_recentes` da Apify): perguntas de seguidor e palavras que o público usa.
- **Legendas e vídeos** já lidos no Passo 1.

Monte um rascunho curto de **cliente, oferta e prova** e mostre: "Isso eu já descobri sozinho: … Confere?". Cada item que você achou é uma pergunta a menos no Passo 1c.

## Passo 1b. O que você já fez

Pergunte se ela já tem roteiros, legendas, posts planejados, textos ou materiais que já usa. Ela pode:
- colar aqui;
- dizer o caminho de uma pasta no computador;
- mandar o link de uma pasta do Drive ou de um documento.

Leia tudo. Copie em texto pra `memoria/roteiros/` (um `.md` por material, com a origem no topo). Não copie mídia.

Isso serve a três coisas:
- a voz real dela (Passo 2);
- ideias que ela já teve, que viram ideias na Fábrica (`FAB ideia-nova` com `"origem":"já feito"` e `"texto_proprio": true` quando for roteiro pronto);
- o que **não** repetir.

Se ela não tiver nada, siga.

## Passo 1c. O que só você sabe

Perguntas que mais melhoram o conteúdo, tiradas de briefings de social media. **Pule as que o Passo 1a ou 1b já respondeu**: nesse caso, mostre o que achou e peça só um "é isso?". Uma por vez, aberta, com a linha de subtexto entre parênteses, exatamente nessa linguagem simples:

**Cliente**
1. "O que seu cliente fala pra não comprar?" (cada desculpa dele vira um post que quebra essa crença)
2. "Quais perguntas mais chegam no direct e nos comentários?" (é a lista de pautas que o seu público já pediu; mostre as que você achou nos comentários)
3. "Como o cliente descreve o problema, com as palavras dele? Pode colar mensagens reais, sem nome." (pro texto soar como ele fala, não como propaganda)
4. "Seu cliente já sabe que tem esse problema, ou você precisa mostrar pra ele?" (muda o jeito de começar o post)

**Oferta**
5. "Como fica a vida do cliente depois de comprar de você?" (é a promessa que o post entrega)
6. "Por que comprar de você e não de outro?" (o que só você tem)
7. "Que resultados, números ou depoimentos você pode mostrar?" (prova de verdade; sem isso eu não cito número nenhum)
8. "O que você quer vender ou divulgar mais nos próximos 3 meses? Tem alguma data importante?" (pra puxar o conteúdo pra onde está o dinheiro)

**Limites**
9. "Sobre o que você não fala de jeito nenhum? E com quem você não quer parecer?" (tema proibido e o tipo de perfil que você não quer imitar)

**Ação**
10. "Depois de ver o post, pra onde a pessoa deve ir? Direct, WhatsApp, link da bio, comentar uma palavra?" (o convite do fim do post)
11. "O que precisa acontecer pra você dizer que o Instagram está dando certo?" (é o número que eu vou acompanhar toda semana)

**Onde gravar:**
- 1 a 4 em `perfil/publico.md` (crie se não existir), em seções curtas: Objeções, Perguntas do público, Palavras do cliente, Quanto ele já sabe;
- 5 a 8 em `perfil/marca.md`, seções Promessa, Diferencial, Provas que posso citar, Prioridade dos próximos meses;
- 9 em `memoria/aprendizado.md`, na seção "Do questionário";
- 10 e 11 em `perfil/marca.md` (seções Para onde o post leva, Sucesso é) e em `config.json` (`"cta_destino"`, `"meta_sucesso"`).

**Teto:** somando este passo com voz, volume, equipe, fontes e referências, a pessoa responde **no máximo 12 perguntas abertas**. Se passar disso, você está perguntando o que devia ter buscado. Perguntas de sim/não (Apify, Chrome, publicação) não contam.

## Passo 2. Voz

A voz sai do que ela já escreveu, não de adjetivo.

- **Legendas:** use as legendas dos posts dela (Apify ou coladas). Se tiver menos de 3, peça mais, ou peça pra ela escrever como explicaria o produto pra um cliente no WhatsApp.
- **Reels:** pergunte como ela fala nos Reels (Reels não tem texto pra ler). Peça pra ela descrever, ou colar a transcrição de um.
- **Modelo do perfil de voz:** aplique o método de perfil de voz do `instagram-skills` (`references/voice-profile.md` e `voice-rules.md` do plugin dele, ou a skill `instagram-skills:ig-humanizer` em modo perfil). Monte:
  - como abre e como fecha;
  - tamanho de frase;
  - palavras e gírias que usa;
  - emojis (quais e quanto);
  - pessoa verbal (eu, a gente);
  - o que NUNCA diz.
- **Confirmação:** mostre o resultado em até 10 linhas, com um exemplo de legenda nova escrita nessa voz, e pergunte se soa como ela.
- **Exemplo bom e ruim:** pergunte "Qual post seu você mais gostou, e qual odiou?" (o que gostou é o molde; o que odiou entra no "nunca"). Pule se ela já disse.

## Passo 3. Público e objetivos por formato

Confirme, com o que já sabe:
- quem é o seguidor que interessa (não "todo mundo");
- o que o Reels deve buscar (alcance, seguidor novo, mensagem no direct);
- o que o carrossel deve buscar (salvamento, autoridade, venda).

Explique que esse vai ser o padrão de todo pedido, e que ela só precisa dizer quando quiser fugir dele.

## Passo 4. Fontes de assunto

1. Pesquise na web as fontes **oficiais** e confiáveis do nicho dela:
   - site oficial de marcas e órgãos;
   - portais especializados;
   - calendário de eventos;
   - blogs de fabricante.
2. Proponha de 5 a 8 fontes, com link e uma linha dizendo o que cada uma traz.
3. Pergunte quais risca e quais acrescenta. Ela pode acrescentar perfil, canal do YouTube ou site que acompanha.

## Passo 5. Referências

1. Peça de 2 a 5 perfis que ela admira ou que concorrem com ela, e o que admira em cada um.
2. Se a Apify estiver ligada, leia os perfis pelo mesmo script. Diga em uma linha o que cada um faz que funciona.

## Passo 5b. Assistir aos vídeos dela

Peça autorização em uma frase: "Posso usar o login do Instagram que está no seu Chrome pra baixar seus Reels e assistir? Eu guardo só a análise em texto e apago o vídeo."
- Se sim, grave `"chrome_autorizado": true` no `config.json`.
- Se não, só vídeos públicos.

Rode o agente `/fabrica:assistir` com:
- **os vídeos dela que deram certo:** os Reels de `dados/posts-perfil.json`, ordenados por views (ou curtidas). Pegue os 8 melhores, mais os 2 piores pra comparar;
- **os perfis de referência:** os 3 Reels de maior resultado de cada perfil de `perfil/referencias.md`. Leia com `ler_perfil.py` e grave a análise em `memoria/referencias/<handle>.md`.

Sem Apify, use os links que ela der. Avise que isso leva alguns minutos e que ela pode seguir respondendo as próximas perguntas enquanto isso. Antes de usar a primeira vez, rode o setup do `watch` com motor local e transcrição local (`--engine local`, `--backend whisperx`). Avise que a primeira vez baixa o modelo de transcrição e demora uns minutos.

Use o que viu pra **confirmar a voz** (Passo 2) com base no que ela fala de verdade, e pra começar `memoria/o-que-funciona.md`, só com o que tiver número.

## Passo 6. Volume

Pergunte uma coisa só: quantos posts por semana ela consegue manter de verdade. Ofereça faixas pra facilitar a resposta: 2 a 3, 4 a 5, 6 ou mais.

Pergunte também se tem alguma limitação de produção. Ex.: "nem sempre consigo gravar" muda a mistura pra mais carrossel.

Sugira começar menor do que ela acha. Consistência vale mais que volume.

**Não pergunte:**
- dia;
- formato de vídeo (falado, tela dividida, texto na tela, narração);
- mistura Reels/carrossel além do que ela disser espontaneamente.

Explique em uma frase: "nas primeiras semanas eu vario o formato de propósito e, com o resultado, fico com o que funciona no seu perfil".

## Passo 7. Equipe

Pergunte quem faz o quê depois do texto pronto:
- ela mesma;
- um designer;
- uma social media.

Pergunte também como cada pessoa recebe hoje (WhatsApp, pasta do Drive, Canva). A Fábrica vai entregar o pacote do post no formato que cada um usa.

## Passo 8. Publicação automática

Pergunte se ela quer que carrossel e post de imagem possam ser publicados direto daqui, sempre depois do OK dela.

**Se sim**, explique que isso pede três coisas:
- conta comercial ou de criador no Instagram;
- conta na Publora (https://app.publora.com/signup, paga);
- o `PUBLORA_API_KEY` e o `INSTAGRAM_PLATFORM_ID` no `.env`.

Pode deixar pra depois: `/fabrica:comecar publicar`.

Reels continua sendo gravado e postado por ela.

## Passo 9. Ângulos

1. Leia `PLUGIN/referencias/angulos-e-formatos.md`.
2. Com tudo que já sabe (nicho, objetivo, o que funcionou nos posts dela), escolha:
   - as 3 ou 4 categorias principais;
   - as viradas que mais servem.
3. Mostre a escolha com o porquê de cada uma, como informação, não como pergunta. Ela corrige se quiser. Diga que isso é o ponto de partida e que o analista ajusta com o resultado.

## Passo 10. Montar a Fábrica dela

Crie tudo de uma vez.

1. **`perfil/`**: `marca.md`, `voz.md`, `angulos.md`, `fontes.md`, `referencias.md`, `equipe.md`. Cada arquivo é curto, com o que foi confirmado. Nada inventado.
2. **`meus-agentes/`**: um arquivo por agente, só com o que é DELA, por cima do método do sistema.
   - `radar.md`:
     - fontes em ordem;
     - quantas ideias por dia (padrão 4);
     - temas a evitar;
     - o tipo de assunto que mais serve ao público.
   - `produzir.md`:
     - voz resumida;
     - categorias e viradas prioritárias;
     - como ela fala nos Reels;
     - formatos em teste (alternar nas primeiras semanas);
     - tamanho de carrossel;
     - CTA por objetivo;
     - hashtags.
   - `analista.md`:
     - referências;
     - Apify ou print;
     - o que medir pelo objetivo dela;
     - dia da leitura.
3. **`memoria/`**:
   - `aprendizado.md`: começa com o cabeçalho "# O que você ensinou à Fábrica" e o que ela disse no questionário que é preferência ("nunca X", "gosto de Y");
   - `o-que-funciona.md`: "# O que funciona (medido)" e o que saiu dos vídeos com número;
   - `historico/` e `videos/`.
4. **`dados/`**: `ideias/`, `posts-perfil.json` e `semanas.json`, este com o ponto zero da semana atual (seguidores, engajamento, referências, leitura de 2-3 linhas).
5. **`CLAUDE.md`**: copie `PLUGIN/modelos/CLAUDE.md`, trocando `{{HANDLE}}`.
6. **`config.json`**: `{"handle","apify":true|false,"publora":true|false,"chrome_autorizado":true|false,"radar_horario":"07:00","analista_dia":"segunda","criado":"AAAA-MM-DD"}`.
7. **`.gitignore`** com `.env` e `.tmp-videos/`.
8. **Primeiras ideias.** Rode `/fabrica:radar`.
9. **Rotinas.** Se a ferramenta de tarefas agendadas do app desktop estiver disponível (`scheduled-tasks`), crie:
   - **"Fábrica - ideias do dia"**, todo dia no `radar_horario`. Prompt: `Na pasta <caminho absoluto>, rode /fabrica:radar.`
   - **"Fábrica - leitura semanal"**, no `analista_dia` às 08:00. Prompt: `Na pasta <caminho>, rode /fabrica:analista e depois /fabrica:assistir.`

   Avise que rodam com o computador ligado e o app do Claude aberto. Se o computador estiver desligado na hora, rodam quando ele ligar.
10. **Abrir o app:** rode `/fabrica:painel`.
11. **Fechamento** (curto):
    - o endereço do app;
    - como abrir de novo: no Claude, nesta pasta, `/fabrica:painel`;
    - o uso diário em 3 passos:
      1. abre o app e ensina a Fábrica nas ideias (boa, ruim, ângulo ruim);
      2. clica em Produzir e acompanha cada etapa;
      3. ajusta conversando e marca o status;
    - tudo que ela ensinar fica guardado na memória e muda as próximas ideias.

## Regras

- Nunca invente dado do perfil. O que não leu, pergunte.
- Token só em `.env`. Nunca em `perfil/`, `memoria/`, `CLAUDE.md` ou no app.
- Se alguma etapa falhar, diga o que falhou, siga com o resto e anote em `config.json` (`pendente`).
