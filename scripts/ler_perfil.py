#!/usr/bin/env python3
"""Lê perfis públicos do Instagram pela Apify e devolve JSON normalizado.

Uso:
    python3 ler_perfil.py --env /caminho/da/pasta/.env usuario1 usuario2 ...

Saída (stdout): {"perfis": [{"username", "seguidores", "seguindo", "posts_total",
"bio", "posts": [{"id","url","formato","legenda","curtidas","comentarios",
"views","data"}]}], "erros": [...]}

Sem dependências além da biblioteca padrão. O token vem de APIFY_TOKEN no
ambiente ou no arquivo .env indicado. Nunca imprime o token.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

ACTOR = "apify~instagram-profile-scraper"
URL = "https://api.apify.com/v2/acts/{a}/run-sync-get-dataset-items?token={t}"


def token_do_env(caminho):
    tok = os.environ.get("APIFY_TOKEN", "").strip()
    if tok:
        return tok
    if caminho and os.path.exists(caminho):
        with open(caminho, encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha.startswith("APIFY_TOKEN="):
                    return linha.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def formato(p):
    tipo = (p.get("type") or "").lower()
    prod = (p.get("productType") or "").lower()
    if prod == "clips" or tipo == "video":
        return "reels"
    if tipo == "sidecar":
        return "carrossel"
    return "foto"


def normaliza(item):
    posts = []
    for p in item.get("latestPosts") or []:
        views = p.get("videoViewCount") or p.get("videoPlayCount")
        posts.append({
            "id": p.get("shortCode") or p.get("id"),
            "url": p.get("url") or (f"https://www.instagram.com/p/{p.get('shortCode')}/" if p.get("shortCode") else None),
            "formato": formato(p),
            "legenda": (p.get("caption") or "")[:600],
            "curtidas": p.get("likesCount") if (p.get("likesCount") or 0) >= 0 else None,
            "comentarios": p.get("commentsCount"),
            "views": views,
            "data": (p.get("timestamp") or "")[:10],
        })
    return {
        "username": item.get("username"),
        "seguidores": item.get("followersCount"),
        "seguindo": item.get("followsCount"),
        "posts_total": item.get("postsCount"),
        "bio": item.get("biography"),
        "categoria": item.get("businessCategoryName"),
        "posts": posts,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", default=".env")
    ap.add_argument("usuarios", nargs="+")
    a = ap.parse_args()
    tok = token_do_env(a.env)
    if not tok:
        print(json.dumps({"erro": "sem_token", "mensagem": "APIFY_TOKEN não encontrado no .env da pasta."}, ensure_ascii=False))
        sys.exit(2)
    nomes = [u.lstrip("@").strip() for u in a.usuarios if u.strip()]
    corpo = json.dumps({"usernames": nomes}).encode()
    req = urllib.request.Request(URL.format(a=ACTOR, t=tok), data=corpo, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            itens = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        msg = {401: "token inválido", 402: "crédito da Apify acabou"}.get(e.code, f"erro HTTP {e.code}")
        print(json.dumps({"erro": "apify", "mensagem": msg}, ensure_ascii=False))
        sys.exit(3)
    except Exception as e:  # rede, timeout
        print(json.dumps({"erro": "rede", "mensagem": str(e)}, ensure_ascii=False))
        sys.exit(3)
    perfis, erros = [], []
    for it in itens:
        if it.get("error") or not it.get("username"):
            erros.append(it.get("error") or "perfil não encontrado")
        else:
            perfis.append(normaliza(it))
    print(json.dumps({"perfis": perfis, "erros": erros}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
