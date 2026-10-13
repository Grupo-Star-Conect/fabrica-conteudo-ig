# Fábrica de Conteúdo de @{{HANDLE}}

Esta pasta é a Fábrica de Conteúdo de Instagram de @{{HANDLE}}. Toda conversa aberta aqui já sabe quem é a pessoa: **nunca peça de novo nicho, público, objetivo ou voz**.

## Duas camadas

- **Sistema:** o plugin `fabrica`. Método, etapas, app. Atualiza com `claude plugin update fabrica@fabrica-star-conect`. Não se edita daqui.
- **Esta pessoa:** tudo nesta pasta. Nenhuma atualização apaga.

| Pasta | O que guarda |
|---|---|
| `perfil/` | Quem é, voz, ângulos, fontes, referências, equipe |
| `meus-agentes/` | O jeito dela de cada agente (radar, produzir, analista) |
| `memoria/` | O que deixa a Fábrica mais inteligente. **Ler antes de criar qualquer coisa** |
| `dados/` | Ideias (com a trilha de produção de cada post), posts do perfil, semanas |

O que fica em `memoria/`:
- `aprendizado.md`: o que ela ensinou (notícia boa ou ruim, ângulo ruim, tom errado, regras de ajuste);
- `o-que-funciona.md`: o que foi provado com número;
- `videos/`: análise de cada vídeo dela, assistido de verdade;
- `historico/AAAA-MM.md`: o que aconteceu em cada dia.

## Como trabalhar

- **App:** `/fabrica:painel` abre a tela no navegador. É o lugar do dia a dia.
- **Pedido em conversa:** pedido curto basta. Ex.: "traz isso: <link>", "produz a ideia X como carrossel", "por que meu último Reels foi bem?".
- **Agentes:**
  - `/fabrica:radar`: ideias;
  - `/fabrica:trazer`: assunto ou link vira ideia;
  - `/fabrica:produzir`: post com trilha;
  - `/fabrica:assistir`: vídeos;
  - `/fabrica:analista`: números e o que funciona;
  - `/fabrica:fila`: status, entrega, publicação.
- **Refazer parte do questionário:** `/fabrica:comecar <bloco>`.

## Regras

- Ler `memoria/` antes de sugerir ou produzir.
- Gravar o que importa no fim (com `fab.py`): sem memória, o sistema não aprende.
- Nunca inventar fato, número, pesquisa ou citação.
- Texto que a pessoa traz é lei.
- Nada é publicado sem a pessoa dizer "pode publicar".
- Se ela corrigir algo de um jeito que parece preferência fixa, guarde em `memoria/aprendizado.md`.
