# Fábrica de Conteúdo · Star Conect

Plugin do Claude Code que monta e opera uma Fábrica de Conteúdo de Instagram pra qualquer perfil:

- **`/fabrica:comecar`:** questionário que lê o seu perfil, assiste aos seus vídeos, confirma voz, público e objetivos, adapta os agentes a você, cria a memória e agenda as rotinas.
- **`/fabrica:painel`:** abre o app no navegador do computador. É ali que se trabalha no dia a dia.
- **`/fabrica:radar`:** ideias do dia, com link da fonte e o porquê de cada uma.
- **`/fabrica:trazer`:** transforma tema, link de notícia ou link de post de outra pessoa em ideia.
- **`/fabrica:produzir`:** produz o post passando por cada etapa, com trilha visível: fonte, formato e ângulo, gancho, texto, legenda, hashtags, revisão anti-IA e briefing.
- **`/fabrica:assistir`:** assiste aos seus vídeos (frames + transcrição) e guarda só a análise em texto.
- **`/fabrica:analista`:** números, cruzamento com o que foi publicado e o que funciona.
- **`/fabrica:fila`:** status, entrega pro designer/social e publicação com OK.

**Camadas.** O plugin é o sistema e atualiza sozinho. A sua pasta (`perfil/`, `meus-agentes/`, `memoria/`, `dados/`) é sua, e nenhuma atualização mexe nela.

Usa por baixo dois plugins abertos: [instagram-skills](https://github.com/sergebulaev/instagram-skills) e [claude-video / watch](https://github.com/bradautomates/claude-video), ambos MIT.

## Instalar

Pré-requisitos: Claude Pro, Claude Code logado no Terminal (`claude` → `/login`), Python 3 e ffmpeg.

```
claude plugin marketplace add sergebulaev/instagram-skills
claude plugin install instagram-skills@instagram-skills
claude plugin marketplace add bradautomates/claude-video
claude plugin install watch@claude-video
claude plugin marketplace add <origem-deste-repo>
claude plugin install fabrica@fabrica-star-conect
```

Depois:
1. Crie uma pasta vazia.
2. Abra o Claude nela.
3. Digite `/fabrica:comecar`.

## Atualizar

```
claude plugin marketplace update fabrica-star-conect
claude plugin update fabrica@fabrica-star-conect
```
