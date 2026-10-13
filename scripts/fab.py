#!/usr/bin/env python3
"""CLI da Fábrica: o jeito único de as skills gravarem dados na pasta do cliente.

Rode sempre de dentro da pasta da Fábrica (ou passe --pasta).

  fab.py ideia-nova '<json>'                cria ideia; imprime o id
  fab.py ideia <id>                         imprime a ideia (JSON)
  fab.py ideias [--status ideia,pronto]     lista id | status | título
  fab.py alterar <id> '<json>'              mescla campos (post, briefing, angulo, tipo...)
  fab.py trilha <id> <etapa> <skill> (--texto "..." | --arquivo saida.md)
  fab.py status <id> <status>
  fab.py publicar <id> [--link URL]         marca publicado e liga o timer de 7 dias
  fab.py vencidos                           publicados com a análise de 7 dias vencida
  fab.py historico "<texto>"                anota em memoria/historico/AAAA-MM.md
  fab.py memoria <arquivo.md> "<texto>"     PROPÕE guardar em memoria/<arquivo.md> (a pessoa confirma no app)
  fab.py perfil <arquivo.md> --arquivo novo.md   PROPÕE trocar perfil/<arquivo.md> (a pessoa confirma)
  fab.py salvar-direto <arquivo.md> "<texto>"    grava em memoria/ SEM confirmar: só número medido
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "app"))
from dados import Pasta, STATUS, MIGRA  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pasta", default=".")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("ideia-nova"); s.add_argument("json")
    s = sub.add_parser("ideia"); s.add_argument("id")
    s = sub.add_parser("ideias"); s.add_argument("--status", default="")
    s = sub.add_parser("alterar"); s.add_argument("id"); s.add_argument("json")
    s = sub.add_parser("trilha"); s.add_argument("id"); s.add_argument("etapa"); s.add_argument("skill")
    g = s.add_mutually_exclusive_group(required=True); g.add_argument("--texto"); g.add_argument("--arquivo")
    s = sub.add_parser("status"); s.add_argument("id"); s.add_argument("status", choices=STATUS + list(MIGRA))
    s = sub.add_parser("publicar"); s.add_argument("id"); s.add_argument("--link", default="")
    sub.add_parser("vencidos")
    s = sub.add_parser("historico"); s.add_argument("texto")
    s = sub.add_parser("memoria"); s.add_argument("arquivo"); s.add_argument("texto"); s.add_argument("--origem", default="")
    s = sub.add_parser("perfil"); s.add_argument("arquivo"); s.add_argument("--arquivo-novo", "--arquivo", dest="novo", required=True); s.add_argument("--origem", default="")
    s = sub.add_parser("salvar-direto"); s.add_argument("arquivo"); s.add_argument("texto")
    a = ap.parse_args()
    P = Pasta(a.pasta)

    if a.cmd == "ideia-nova":
        print(P.nova_ideia(json.loads(a.json))["id"])
    elif a.cmd == "ideia":
        print(json.dumps(P.ideia(a.id), ensure_ascii=False, indent=1))
    elif a.cmd == "ideias":
        filtro = [x for x in a.status.split(",") if x]
        for d in P.listar_ideias():
            if not filtro or d.get("status") in filtro:
                print(f"{d['id']} | {d.get('status')} | {d.get('titulo')}")
    elif a.cmd == "alterar":
        P.alterar(a.id, json.loads(a.json)); print("ok")
    elif a.cmd == "trilha":
        saida = a.texto if a.texto is not None else open(a.arquivo, encoding="utf-8").read()
        P.trilha(a.id, a.etapa, a.skill, saida); print("ok")
    elif a.cmd == "status":
        P.status(a.id, a.status); print("ok")
    elif a.cmd == "publicar":
        P.publicar(a.id, a.link or None); print("ok")
    elif a.cmd == "vencidos":
        for d in P.vencidos():
            print(f"{d['id']} | publicado {d.get('publicado_em')} | {d.get('link_post') or 'sem link'} | {d.get('titulo')}")
    elif a.cmd == "historico":
        P.historico(a.texto); print("ok")
    elif a.cmd in ("memoria", "salvar-direto"):
        nome = os.path.basename(a.arquivo)
        if not nome.endswith(".md"):
            sys.exit("use um arquivo .md")
        if a.cmd == "salvar-direto":
            P.anexar(f"memoria/{nome}", a.texto); print("ok")
        else:
            P.pendente_novo(f"memoria/{nome}", a.texto, a.origem)
            print("proposto: aparece no app pra pessoa confirmar (Salvar / Não guardar)")
    elif a.cmd == "perfil":
        nome = os.path.basename(a.arquivo)
        texto = open(a.novo, encoding="utf-8").read()
        P.pendente_novo(f"perfil/{nome}", texto, a.origem, modo="substituir")
        print("proposto: aparece no app com o antes e o depois pra pessoa confirmar")


if __name__ == "__main__":
    main()
