#!/usr/bin/env python3
"""Lê perfis públicos do Instagram pela Apify e devolve JSON normalizado.

Uso:
    python3 ler_perfil.py --env /caminho/da/pasta/.env usuario1 usuario2 ...
    python3 ler_perfil.py --env .env --posts <link do post> [<link> ...] [--pago]

--posts lê posts específicos (análise de 7 dias). --pago pede também os
compartilhamentos, que só existem no plano pago da Apify.

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
ACTOR_POST = "apify~instagram-scraper"
ACTOR_REEL = "apify~instagram-reel-scraper"
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


def post(p):
    """Um post da Apify no formato da Fábrica, com tudo que ela entrega."""
    musica = p.get("musicInfo") or {}
    sc = p.get("shortCode")
    curt = p.get("likesCount")
    out = {
        "id": sc or p.get("id"),
        "url": p.get("url") or (f"https://www.instagram.com/p/{sc}/" if sc else None),
        "formato": formato(p),
        "legenda": (p.get("caption") or "")[:600],
        "curtidas": curt if isinstance(curt, int) and curt >= 0 else None,   # -1 = curtidas ocultas
        "comentarios": p.get("commentsCount"),
        "views": p.get("videoViewCount") or p.get("videoPlayCount"),
        "plays": p.get("videoPlayCount"),
        "duracao": round(p["videoDuration"]) if p.get("videoDuration") else None,
        "slides": len(p.get("childPosts") or []) or None,
        "fixado": bool(p.get("isPinned")),
        "audio": ("original" if musica.get("uses_original_audio") else
                  " - ".join(x for x in (musica.get("artist_name"), musica.get("song_name")) if x) or None) if musica else None,
        "hashtags": p.get("hashtags") or [],
        "mencoes": p.get("mentions") or [],
        "comentarios_recentes": [c.get("text") for c in (p.get("latestComments") or [])[:5] if c.get("text")],
        "data": (p.get("timestamp") or "")[:10],
    }
    if p.get("sharesCount") is not None:
        out["compartilhamentos"] = p.get("sharesCount")
    return {k: v for k, v in out.items() if v not in (None, [], "")}


def normaliza(item):
    posts = [post(p) for p in item.get("latestPosts") or []]
    return {
        "username": item.get("username"),
        "seguidores": item.get("followersCount"),
        "seguindo": item.get("followsCount"),
        "posts_total": item.get("postsCount"),
        "bio": item.get("biography"),
        "categoria": item.get("businessCategoryName"),
        "posts": posts,
    }


def chamar(actor, tok, corpo):
    req = urllib.request.Request(URL.format(a=actor, t=tok), data=json.dumps(corpo).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read().decode())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", default=".env")
    ap.add_argument("--posts", action="store_true", help="os argumentos são links de posts")
    ap.add_argument("--pago", action="store_true", help="pede compartilhamentos (plano pago da Apify)")
    ap.add_argument("usuarios", nargs="+")
    a = ap.parse_args()
    tok = token_do_env(a.env)
    if not tok:
        print(json.dumps({"erro": "sem_token", "mensagem": "APIFY_TOKEN não encontrado no .env da pasta."}, ensure_ascii=False))
        sys.exit(2)
    nomes = [u.lstrip("@").strip() for u in a.usuarios if u.strip()]
    try:
        if a.posts:
            itens = chamar(ACTOR_POST, tok, {"directUrls": nomes, "resultsType": "details", "resultsLimit": len(nomes)})
            if a.pago:  # compartilhamentos vêm do reel-scraper
                extra = chamar(ACTOR_REEL, tok, {"username": nomes, "includeSharesCount": True, "resultsLimit": len(nomes)})
                share = {x.get("shortCode"): x.get("sharesCount") for x in extra if x.get("shortCode")}
                for it in itens:
                    if share.get(it.get("shortCode")) is not None:
                        it["sharesCount"] = share[it["shortCode"]]
            posts = [post(p) for p in itens if p.get("shortCode")]
            erros = [p.get("error") for p in itens if p.get("error")]
            print(json.dumps({"posts": posts, "erros": erros}, ensure_ascii=False, indent=1))
            return
        itens = chamar(ACTOR, tok, {"usernames": nomes})
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
