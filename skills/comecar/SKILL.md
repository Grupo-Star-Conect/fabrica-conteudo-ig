---
name: comecar
description: Questionário de instalação da Fábrica de Conteúdo. Entende quem é a pessoa, lê o perfil do Instagram, confirma voz, público, objetivos, fontes e referências, ADAPTA os agentes (radar, fabricar, analista) a esse perfil, publica o painel na conta Claude dela e deixa as rotinas rodando. Rode com /fabrica:comecar na pasta onde a Fábrica vai morar. Com argumento refaz só um bloco - /fabrica:comecar voz | angulos | fontes | referencias | formatos | equipe | publicar | painel.
---

# /fabrica:comecar

Você vai configurar a Fábrica de Conteúdo de Instagram de uma pessoa. No fim, ela tem:
- a pasta pronta;
- os agentes reescritos pro perfil dela;
- o painel publicado na conta Claude dela;
- as primeiras pautas;
- as rotinas agendadas.

A pessoa nunca mais vai precisar explicar nicho, público ou objetivo.

**Tom:** conversa de gente, em português do Brasil, frases curtas. Uma pergunta por vez, sempre aberta, com uma linha de subtexto dizendo o que você quer saber. Nunca ofereça opção pronta pra resposta que só ela sabe. Quando você já tem a resposta (da bio, dos posts), mostre o que entendeu e pergunte "é isso? muda algo?".

**Pergunte só o que só a pessoa sabe.** Fato da vida dela pode ser perguntado: o que vende, pra quem, quanto consegue produzir, quem é a equipe, como fala. Decisão de criação **nunca** vira pergunta: quando usar tela dividida, texto na tela ou narração, qual gancho, qual ângulo, que dia postar. Essas decisões são trabalho da Fábrica. Ela testa variações enquanto não tem dado e repete o que funcionou quando passa a ter. Se a pessoa disser "não sei" ou "decide você", isso é a resposta certa: registre que a Fábrica decide e siga.

**Pasta de trabalho:** a pasta atual. Os arquivos do plugin ficam em `${CLAUDE_PLUGIN_ROOT}`.

## Passo 0. Conferir a casa

1. **Refazer um bloco.** Se veio argumento (`voz`, `angulos`, `fontes`, `referencias`, `formatos`, `equipe`, `publicar`, `painel`) e `perfil/` já existe:
   - leia os arquivos atuais;
   - refaça só aquele bloco;
   - mostre antes/depois;
   - grave nos arquivos e no painel;
   - termine. Pule o resto deste roteiro.
2. **Já instalado.** Se `perfil/` existe e não veio argumento, pergunte se é pra refazer tudo ou só um bloco.
3. **Dependência.** Confira se as skills do `instagram-skills` estão disponíveis (ex.: `instagram-skills:ig-humanizer`). Se não estiverem, pare e mostre:
   ```
   claude plugin marketplace add sergebulaev/instagram-skills
   claude plugin install instagram-skills@instagram-skills
   ```
   Depois de instalar, a pessoa abre uma conversa nova e roda `/fabrica:comecar` de novo.
4. **Abertura.** Diga em 3 linhas o que vai acontecer: umas 10 perguntas (cerca de 15 minutos), e no fim ela ganha o painel e as primeiras pautas.

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
2. Grave o token em `.env` na pasta (`APIFY_TOKEN=...`). Avise que ele fica só nesse arquivo, no computador dela, e nunca vai pro painel.
3. Garanta que `.env` não seja publicado. Crie `.gitignore` com `.env` se a pasta for virar repositório.
4. Rode:
   ```
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ler_perfil.py" --env .env <handle>
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

1. Leia `${CLAUDE_PLUGIN_ROOT}/referencias/angulos-e-formatos.md`.
2. Com tudo que já sabe (nicho, objetivo, o que funcionou nos posts dela), escolha:
   - as 3 ou 4 categorias principais;
   - as viradas que mais servem.
3. Mostre a escolha com o porquê de cada uma, como informação, não como pergunta. Ela corrige se quiser. Diga que isso é o ponto de partida e que o analista ajusta com o resultado.

## Passo 10. Montar a Fábrica dela

Crie tudo de uma vez.

1. **`perfil/`**: `marca.md`, `voz.md`, `angulos.md`, `fontes.md`, `referencias.md`, `equipe.md`. Cada arquivo é curto, direto, com o que foi confirmado. Nada inventado.
2. **`meus-agentes/`**: um arquivo por agente, com as instruções específicas dela por cima do agente da casa.
   - `radar.md`:
     - quais fontes ler e em que ordem;
     - quantas pautas por dia (cadência semanal dividida pelos dias, mínimo 2);
     - mistura Reels/carrossel;
     - temas a evitar.
   - `fabricar.md`:
     - voz resumida;
     - categorias e viradas prioritárias;
     - como ela fala nos Reels;
     - **formatos em teste**: a lista de formatos de vídeo e de carrossel que a Fábrica vai alternar nas primeiras semanas (ver `fabricar`, seção "Formato de vídeo"), começando pelos que as referências e os posts dela sugerem;
     - **o que já está provado**: começa vazio, e o analista preenche;
     - tamanho de carrossel;
     - CTA padrão por objetivo;
     - hashtags (tamanho e quantidade, pelo método do `ig-hashtag-strategist`).
   - `analista.md`:
     - referências;
     - Apify ou print;
     - o que medir (pelo objetivo dela);
     - dia da leitura semanal.
3. **`CLAUDE.md`**: copie `${CLAUDE_PLUGIN_ROOT}/modelos/CLAUDE.md`, trocando `{{HANDLE}}`.
4. **`config.json`**: `{"handle","apify":true|false,"publora":true|false,"painel_url":null,"radar_horario":"07:00","analista_dia":"segunda","criado":"AAAA-MM-DD"}`.
5. **Publicar o painel:**
   - copie `${CLAUDE_PLUGIN_ROOT}/painel/index.html` pra `painel/index.html` na pasta;
   - publique com a ferramenta Artifact: `file_path` = esse arquivo, `capabilities` = `{"db":{},"user":{},"sample":{}}`, `icon` = `calendar`, `description` = "Painel da Fábrica de Conteúdo de @handle";
   - grave a URL em `config.json` (`painel_url`).
6. **Carregar o painel com ArtifactData** (`url` = `painel_url`), num `batch` só:
   - documento `perfil/atual`, com os campos `handle, nicho, oferta, publico, objetivo_reels, objetivo_carrossel, voz` (resumo de 1-2 frases), `regras` (lista, vazia no começo), `nunca` (lista), `angulos` (lista curta), `referencias` (lista de @), `fontes` (lista de nomes), `cadencia` (frase), `formato_reels` (frase);
   - coleção `posts`: um documento por post lido, com o id do post como `doc_id` (só letras, números, `_` e `-`). Campos: `formato, views, curtidas, comentarios, legenda, data, url`;
   - coleção `semanas`: o ponto zero, com `doc_id` = semana ISO (ex.: `2026-W42`). Campos: `semana`, `seguidores`, `engajamento` (média de (curtidas+comentários)/seguidores×100 dos posts lidos, 1 casa), `posts` (quantos posts nos últimos 7 dias), `referencias` (`[{handle, engajamento}]` se leu as referências), `leitura` (2-3 linhas do que funciona e do que não funciona hoje).
7. **Primeiras pautas:** rode o agente `/fabrica:radar` agora, pra que o painel já abra com pautas.
8. **Rotinas.** Se a ferramenta de tarefas agendadas do app desktop estiver disponível (`scheduled-tasks`), crie duas:
   - **"Fábrica - radar diário"**, todo dia no `radar_horario`. Prompt: `Na pasta <caminho absoluto da pasta>, rode /fabrica:radar.`
   - **"Fábrica - leitura semanal"**, no `analista_dia` às 08:00. Prompt: `Na pasta <caminho>, rode /fabrica:analista.`

   Avise que elas rodam com o computador ligado e o app do Claude aberto, e que, se o computador estiver desligado, rodam quando ele ligar. Se a ferramenta não existir, explique como criar pelo app (menu de tarefas agendadas) com os mesmos dois prompts.
9. **Fechamento** (curto):
   - o link do painel;
   - "amanhã às 7h chegam as pautas novas";
   - o uso diário em 3 passos: abre o painel → escolhe a pauta → ajusta conversando e marca o status;
   - "pra pedir qualquer coisa fora do painel, abra o Claude nesta pasta e peça em uma linha".

## Regras

- Nunca invente dado do perfil. O que não leu, pergunte.
- Nunca grave token no painel, no `CLAUDE.md` ou em `perfil/`. Só em `.env`.
- Escritas no painel (ArtifactData): para documento que já existe, leia (`get`) e passe o `version` como `if_version`.
- Se alguma etapa falhar, diga o que falhou, siga com o resto e deixe anotado em `config.json` (`pendente`).
