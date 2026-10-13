# Fábrica de Conteúdo · Star Conect

Plugin do Claude Code que monta e opera uma Fábrica de Conteúdo de Instagram pra qualquer perfil:

- **`/fabrica:comecar`:** questionário que lê o seu perfil, confirma voz, público e objetivos, adapta os agentes a você, publica o seu painel e agenda as rotinas.
- **`/fabrica:radar`:** pautas do dia com link da fonte oficial e post já montado.
- **`/fabrica:fabricar`:** transforma pauta, notícia, ideia ou texto seu em post na sua voz.
- **`/fabrica:analista`:** lê o seu perfil e as referências, e monta o comparativo semanal.
- **`/fabrica:fila`:** status, entrega pro designer/social e publicação com OK.

Usa por baixo as skills do [instagram-skills](https://github.com/sergebulaev/instagram-skills) (MIT).

## Instalar

Pré-requisitos: Claude Pro e o app desktop do Claude (aba Code).

```
claude plugin marketplace add sergebulaev/instagram-skills
claude plugin install instagram-skills@instagram-skills
claude plugin marketplace add <origem-deste-repo>
claude plugin install fabrica@fabrica-star-conect
```

Depois:
1. Crie uma pasta vazia (ex.: `Fabrica de Conteudo`).
2. Abra o Claude nela.
3. Digite `/fabrica:comecar`.
