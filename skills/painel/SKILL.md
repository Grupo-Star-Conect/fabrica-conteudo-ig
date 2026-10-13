---
name: painel
description: Abre o app da Fábrica de Conteúdo no navegador do computador (servidor local, só nesta máquina). Use com /fabrica:painel ou quando a pessoa disser "abre a fábrica", "abre o painel", "quero ver minhas ideias".
---

# /fabrica:painel

1. **Pasta da Fábrica.** Confirme que a pasta atual é a da Fábrica: precisa existir `perfil/`. Se não existir, diga para rodar `/fabrica:comecar` aqui ou abrir o Claude na pasta certa.
2. **Já aberto?** Teste se `http://127.0.0.1:4787/` responde (`python3 -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:4787/',timeout=2);print('aberto')"`). Se responder, só diga o endereço.
3. **Abrir.** Se não responder, rode **em segundo plano** (sem esperar terminar):
   ```
   python3 "<diretório base desta skill>/../../app/server.py" --pasta "<caminho absoluto da pasta>" --abrir
   ```
4. **Responder:**
   - o endereço (`http://127.0.0.1:4787/`, ou a porta que o servidor imprimir);
   - o app fica aberto enquanto esta sessão ou o terminal estiver aberto;
   - pra fechar, é só fechar a sessão.
