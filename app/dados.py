"""Camada de dados da Fábrica: tudo mora em arquivos na pasta do cliente.

Usado pelo servidor do app e pelo CLI `scripts/fab.py` (que as skills chamam).
Nada aqui fala com a internet.
"""
import datetime as _dt
import json
import os
import re
import uuid

STATUS = ["ideia", "produzindo", "pronto", "escolhida", "gravada", "designer", "publicada", "descartada"]
FEEDBACK = {
    "noticia_boa": "Notícia boa",
    "noticia_ruim": "Notícia ruim / não serve",
    "angulo_ruim": "Notícia boa, ângulo ruim",
    "tom_errado": "Tom errado",
    "gostei_post": "Gostei do post",
}


def hoje():
    return _dt.date.today().isoformat()


def agora():
    return _dt.datetime.now().isoformat(timespec="seconds")


def slug(txt, n=50):
    s = txt.lower()
    for a, b in (("áàâã", "a"), ("éê", "e"), ("í", "i"), ("óôõ", "o"), ("ú", "u"), ("ç", "c")):
        for ch in a:
            s = s.replace(ch, b)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:n].strip("-") or "ideia"


class Pasta:
    def __init__(self, raiz):
        self.raiz = os.path.abspath(raiz)
        self.ideias = os.path.join(self.raiz, "dados", "ideias")
        self.mem = os.path.join(self.raiz, "memoria")

    # ---------- util ----------
    def p(self, *partes):
        return os.path.join(self.raiz, *partes)

    def ler(self, *partes, padrao=""):
        try:
            with open(self.p(*partes), encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return padrao

    def ler_json(self, caminho, padrao=None):
        try:
            with open(caminho, encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return padrao

    def gravar_json(self, caminho, dado):
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        tmp = caminho + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(dado, f, ensure_ascii=False, indent=1)
        os.replace(tmp, caminho)

    def anexar(self, rel, texto):
        caminho = self.p(rel)
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        novo = not os.path.exists(caminho)
        with open(caminho, "a", encoding="utf-8") as f:
            if novo and rel.startswith("memoria/historico/"):
                f.write(f"# Histórico {os.path.basename(rel)[:-3]}\n\n")
            f.write(texto.rstrip() + "\n")

    def config(self):
        return self.ler_json(self.p("config.json"), {}) or {}

    # ---------- ideias ----------
    def caminho_ideia(self, iid):
        if not re.fullmatch(r"[a-z0-9-]{1,80}", iid or ""):
            raise ValueError("id inválido")
        return os.path.join(self.ideias, iid + ".json")

    def ideia(self, iid):
        return self.ler_json(self.caminho_ideia(iid))

    def listar_ideias(self):
        if not os.path.isdir(self.ideias):
            return []
        out = []
        for nome in os.listdir(self.ideias):
            if nome.endswith(".json"):
                d = self.ler_json(os.path.join(self.ideias, nome))
                if d:
                    out.append(d)
        out.sort(key=lambda d: (d.get("data", ""), d.get("criado", "")), reverse=True)
        return out

    def nova_ideia(self, dado):
        titulo = dado.get("titulo") or "ideia"
        base = f"{hoje().replace('-', '')}-{slug(titulo, 40)}"
        iid, n = base, 2
        while os.path.exists(self.caminho_ideia(iid)):
            iid, n = f"{base}-{n}", n + 1
        ideia = {
            "id": iid, "data": hoje(), "criado": agora(), "status": "ideia",
            "titulo": titulo, "por_que": "", "fonte": None, "tipo_sugerido": None,
            "origem": "radar", "feedback": [], "trilha": [], "post": None,
            "briefing": None, "conversa": [], "sessao": None,
        }
        ideia.update({k: v for k, v in dado.items() if k != "id"})
        self.gravar_json(self.caminho_ideia(iid), ideia)
        self.historico(f"Ideia nova ({ideia['origem']}): {titulo}")
        return ideia

    def alterar(self, iid, campos):
        d = self.ideia(iid)
        if d is None:
            raise KeyError(iid)
        d.update(campos)
        d["atualizado"] = agora()
        self.gravar_json(self.caminho_ideia(iid), d)
        return d

    def trilha(self, iid, etapa, skill, saida):
        d = self.ideia(iid)
        if d is None:
            raise KeyError(iid)
        d.setdefault("trilha", []).append({"etapa": etapa, "skill": skill or "", "saida": saida, "quando": agora()})
        d["atualizado"] = agora()
        self.gravar_json(self.caminho_ideia(iid), d)
        return d

    def status(self, iid, status):
        if status not in STATUS:
            raise ValueError("status inválido")
        d = self.alterar(iid, {"status": status})
        self.historico(f"Status → {status}: {d['titulo']}")
        return d

    def feedback(self, iid, tipo, texto=""):
        if tipo not in FEEDBACK:
            raise ValueError("feedback inválido")
        d = self.ideia(iid)
        if d is None:
            raise KeyError(iid)
        d.setdefault("feedback", []).append({"tipo": tipo, "texto": texto, "quando": agora()})
        if tipo == "noticia_ruim":
            d["status"] = "descartada"
        self.gravar_json(self.caminho_ideia(iid), d)
        fonte = (d.get("fonte") or {}).get("nome") or "sem fonte"
        linha = f"- {hoje()} · {FEEDBACK[tipo]} · \"{d['titulo']}\" ({fonte})"
        if d.get("angulo"):
            linha += f" · ângulo: {d['angulo']}"
        if texto:
            linha += f" · motivo: {texto}"
        self.anexar("memoria/aprendizado.md", linha)
        self.historico(f"Feedback {FEEDBACK[tipo]}: {d['titulo']}")
        return d

    def historico(self, texto):
        mes = hoje()[:7]
        self.anexar(f"memoria/historico/{mes}.md", f"- {agora()[:16].replace('T', ' ')} · {texto}")

    # ---------- leitura geral pro app ----------
    def estado(self):
        cfg = self.config()
        posts = []
        pp = self.p("dados", "posts-perfil.json")
        posts = self.ler_json(pp, []) or []
        semanas = self.ler_json(self.p("dados", "semanas.json"), []) or []
        videos = []
        vdir = self.p("memoria", "videos")
        if os.path.isdir(vdir):
            for nome in sorted(os.listdir(vdir), reverse=True):
                if nome.endswith(".md"):
                    videos.append({"arquivo": nome, "texto": self.ler("memoria", "videos", nome)})
        mes = hoje()[:7]
        return {
            "config": {k: v for k, v in cfg.items() if "token" not in k.lower() and "key" not in k.lower()},
            "marca": self.ler("perfil", "marca.md"),
            "voz": self.ler("perfil", "voz.md"),
            "ideias": self.listar_ideias(),
            "posts": posts,
            "semanas": semanas,
            "videos": videos,
            "memoria": {
                "aprendizado": self.ler("memoria", "aprendizado.md"),
                "o_que_funciona": self.ler("memoria", "o-que-funciona.md"),
                "historico": self.ler("memoria", "historico", f"{mes}.md"),
            },
            "feedback_tipos": FEEDBACK,
        }


def nova_sessao():
    return str(uuid.uuid4())
