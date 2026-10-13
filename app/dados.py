"""Camada de dados da Fábrica: tudo mora em arquivos na pasta do cliente.

Usado pelo servidor do app e pelo CLI `scripts/fab.py` (que as skills chamam).
Nada aqui fala com a internet.
"""
import datetime as _dt
import json
import os
import re
import uuid

STATUS = ["nova", "vou_usar", "guardada", "descartada", "arquivada", "produzindo", "pronto", "gravada",
          "com_equipe", "publicada", "analisada"]
# status da v0.2 -> v0.3
MIGRA = {"ideia": "nova", "escolhida": "vou_usar", "designer": "com_equipe"}
VENCE_DIAS = 7       # ideia nova sem decisão vai pro Arquivo
ANALISA_DIAS = 7     # post publicado é analisado depois disso
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


def em_dias(n):
    return (_dt.date.today() + _dt.timedelta(days=n)).isoformat()


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
        return _norm(self.ler_json(self.caminho_ideia(iid)))

    def listar_ideias(self):
        if not os.path.isdir(self.ideias):
            return []
        out = []
        for nome in os.listdir(self.ideias):
            if nome.endswith(".json"):
                d = _norm(self.ler_json(os.path.join(self.ideias, nome)))
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
            "id": iid, "data": hoje(), "criado": agora(), "status": "nova",
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
        status = MIGRA.get(status, status)
        if status not in STATUS:
            raise ValueError("status inválido")
        if status == "publicada":
            return self.publicar(iid)
        campos = {"status": status}
        if status in ("vou_usar", "guardada", "descartada"):
            campos["decidido_em"] = hoje()
        d = self.alterar(iid, campos)
        self.historico(f"Status → {status}: {d['titulo']}")
        return d

    def publicar(self, iid, link=None):
        campos = {"status": "publicada", "publicado_em": hoje(), "analisar_em": em_dias(ANALISA_DIAS)}
        if link:
            campos["link_post"] = link.strip()
        d = self.alterar(iid, campos)
        self.historico(f"Publicado (análise em {campos['analisar_em']}): {d['titulo']}")
        return d

    def varrer(self):
        """Ideia nova sem decisão há mais de VENCE_DIAS vai pro Arquivo. Nada é apagado."""
        limite = (_dt.date.today() - _dt.timedelta(days=VENCE_DIAS)).isoformat()
        n = 0
        for d in self.listar_ideias():
            if d.get("status") == "nova" and (d.get("data") or hoje()) < limite:
                self.alterar(d["id"], {"status": "arquivada", "arquivada_em": hoje()})
                n += 1
        if n:
            self.historico(f"Arquivo: {n} ideia(s) sem decisão há mais de {VENCE_DIAS} dias")
        return n

    def vencidos(self):
        """Posts publicados cuja análise de 7 dias já venceu."""
        return [d for d in self.listar_ideias()
                if d.get("status") == "publicada" and (d.get("analisar_em") or "9999") <= hoje()]

    # ---------- confirmar antes de salvar ----------
    def _pend_path(self):
        return self.p("dados", "pendente-salvar.json")

    def pendentes(self):
        return self.ler_json(self._pend_path(), []) or []

    def pendente_novo(self, arquivo, texto, origem="", modo="anexar"):
        arquivo = arquivo.strip().lstrip("./")
        if not re.fullmatch(r"(memoria|perfil)/[a-z0-9-]+\.md", arquivo):
            raise ValueError("só dá pra guardar em memoria/*.md ou perfil/*.md")
        L = self.pendentes()
        item = {"id": uuid.uuid4().hex[:8], "arquivo": arquivo, "texto": texto.strip(), "origem": origem,
                "modo": modo, "quando": agora()}
        if modo == "substituir":
            item["antes"] = self.ler(arquivo)
        L.append(item)
        self.gravar_json(self._pend_path(), L)
        return item

    def pendente_salvar(self, pid, texto=None):
        L = self.pendentes()
        it = next((x for x in L if x["id"] == pid), None)
        if not it:
            raise KeyError(pid)
        txt = (texto if texto is not None else it["texto"]).strip()
        if it.get("modo") == "substituir":
            with open(self.p(it["arquivo"]), "w", encoding="utf-8") as f:
                f.write(txt + "\n")
        else:
            self.anexar(it["arquivo"], txt)
        self.gravar_json(self._pend_path(), [x for x in L if x["id"] != pid])
        self.historico(f"Guardado em {it['arquivo']} (confirmado por você)")
        return it

    def pendente_descartar(self, pid):
        L = self.pendentes()
        self.gravar_json(self._pend_path(), [x for x in L if x["id"] != pid])
        return {"ok": True}

    # ---------- conversas do app ----------
    def caminho_conversa(self, cid):
        if not re.fullmatch(r"[a-z0-9-]{1,90}", cid or ""):
            raise ValueError("conversa inválida")
        return self.p("dados", "conversas", cid + ".json")

    def conversa(self, cid):
        return self.ler_json(self.caminho_conversa(cid))

    def gravar_conversa(self, c):
        c["atualizado"] = agora()
        self.gravar_json(self.caminho_conversa(c["id"]), c)
        return c

    def conversas(self):
        d = self.p("dados", "conversas")
        if not os.path.isdir(d):
            return []
        out = []
        for nome in os.listdir(d):
            if nome.endswith(".json"):
                c = self.ler_json(os.path.join(d, nome))
                if c:
                    out.append({k: c.get(k) for k in ("id", "titulo", "criado", "atualizado", "ideia_id")}
                               | {"n": len(c.get("mensagens") or [])})
        out.sort(key=lambda c: c.get("atualizado") or "", reverse=True)
        return out

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
        self.varrer()
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
                    videos.append(_video(nome, self.ler("memoria", "videos", nome), posts))
        refs = []
        rdir = self.p("memoria", "referencias")
        if os.path.isdir(rdir):
            for nome in sorted(os.listdir(rdir)):
                if nome.endswith(".md"):
                    refs.append({"handle": nome[:-3], "texto": self.ler("memoria", "referencias", nome)})
        mes = hoje()[:7]
        return {
            "referencias": refs,
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
            "pendentes": self.pendentes(),
            "conversas": self.conversas(),
            "vencidos": [d["id"] for d in self.vencidos()],
            "publico": self.ler("perfil", "publico.md"),
            "angulos": self.ler("perfil", "angulos.md"),
            "fontes": self.ler("perfil", "fontes.md"),
            "hoje": hoje(),
            "vence_dias": VENCE_DIAS,
        }


def _norm(d):
    if d and d.get("status") in MIGRA:
        d["status"] = MIGRA[d["status"]]
    return d


def _video(nome, texto, posts):
    """Análise de vídeo com nome legível: o tema (H1), a data, o link e os números do post."""
    vid = nome[:-3]
    h1 = next((l[2:].strip() for l in texto.splitlines() if l.startswith("# ")), vid)
    titulo, _, data = h1.rpartition(" · ")
    if not titulo:
        titulo, data = h1, ""
    m = re.search(r"Link:\s*(\S+)", texto)
    post = next((p for p in posts if p.get("id") == vid), {}) if isinstance(posts, list) else {}
    return {"id": vid, "titulo": titulo.strip().strip('"“”'), "data": data.strip() or post.get("data", ""),
            "link": m.group(1) if m else post.get("url"), "tema": post.get("tema"),
            "numeros": {k: post.get(k) for k in ("views", "curtidas", "comentarios") if post.get(k) is not None},
            "texto": texto}


def nova_sessao():
    return str(uuid.uuid4())
