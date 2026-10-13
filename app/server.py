#!/usr/bin/env python3
"""App local da Fábrica de Conteúdo.

    python3 server.py --pasta "/caminho/da/Fabrica" [--porta 4787] [--abrir]

Serve a tela (ui/index.html) só em 127.0.0.1 e expõe uma API pequena:
leitura/gravação dos arquivos da pasta e execução do Claude Code (`claude -p`)
na pasta, com o plano da própria pessoa. Toda chamada exige o token da sessão,
que só a tela servida aqui conhece — outro site aberto no navegador não
consegue disparar nada.
"""
import argparse
import base64
import json
import os
import secrets
import shutil
import subprocess
import sys
import threading
import time
import uuid
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from dados import Pasta, agora, nova_sessao  # noqa: E402

PLUGIN = os.path.dirname(AQUI)
FAB = f'python3 "{os.path.join(PLUGIN, "scripts", "fab.py")}"'

TOKEN = secrets.token_urlsafe(24)
JOBS = {}
LOCK = threading.Lock()
FERRAMENTAS = [
    "Read", "Write", "Edit", "Glob", "Grep", "WebSearch", "WebFetch", "Skill", "TodoWrite",
    "Bash(python3:*)", "Bash(python:*)", "Bash(yt-dlp:*)", "Bash(ffmpeg:*)", "Bash(ffprobe:*)",
    "Bash(ls:*)", "Bash(mkdir:*)",
]


REGRAS_APP = ("Você está rodando por trás do app da Fábrica de Conteúdo, sem ninguém pra responder perguntas. "
              "Responda e escreva SEMPRE em português do Brasil. Não pergunte: decida pelo perfil e pela memória "
              "da pessoa, registre o que fez e explique no fim em poucas linhas.")


REGRAS_CONVERSA = (
    "Você é a Fábrica de Conteúdo conversando com a dona desta pasta pelo app. Responda SEMPRE em português do Brasil, "
    "curto e direto, como num chat. Você conhece o perfil dela (CLAUDE.md, perfil/, memoria/): nunca peça nicho, público "
    "ou voz de novo. Pode perguntar quando faltar algo que só ela sabe. Use as skills da Fábrica quando o pedido for "
    "delas (fabrica:radar, fabrica:trazer, fabrica:produzir, fabrica:assistir, fabrica:analista, fabrica:fila). "
    "REGRA DURA: você NUNCA grava direto em perfil/ nem em memoria/aprendizado.md ou memoria/o-que-funciona.md. "
    f"Para guardar uma regra ou preferência, PROPONHA com: {FAB} memoria aprendizado.md \"- <data> · <regra>\" --origem conversa. "
    f"Para mudar um arquivo de perfil, escreva a versão nova inteira em .tmp-perfil.md e rode: {FAB} perfil <arquivo.md> --arquivo .tmp-perfil.md --origem conversa. "
    "Ela confirma no app num cartão 'Salvar / Não guardar'. Diga em uma linha que deixou pra ela confirmar. "
    "Para dados de ideias e posts, use o fab.py (ideia, ideias, alterar, status, publicar). Nunca invente fato ou número."
)


def achar_claude():
    import glob
    candidatos = [shutil.which("claude"), os.path.expanduser("~/.local/bin/claude"),
                  os.path.expanduser("~/.claude/local/claude"), "/opt/homebrew/bin/claude", "/usr/local/bin/claude",
                  os.environ.get("CLAUDE_CODE_EXECPATH")]
    # Claude Code que vem dentro do app desktop (Mac), versão mais nova primeiro
    candidatos += sorted(glob.glob(os.path.expanduser(
        "~/Library/Application Support/Claude/claude-code/*/*/claude.app/Contents/MacOS/claude")), reverse=True)
    for c in candidatos:
        if c and os.path.exists(c):
            return c
    return None


def ambiente_limpo():
    """Ambiente sem as variáveis de uma sessão do Claude em andamento.

    Se o app foi aberto de dentro de uma conversa do Claude, o processo herda
    variáveis que fazem o Claude Code filho esperar a autenticação do pai e
    falhar com 'OAuth session expired'."""
    return {k: v for k, v in os.environ.items()
            if not (k.startswith("CLAUDE_CODE_") or k.startswith("CLAUDE_AGENT_SDK") or k in
                    ("CLAUDECODE", "CLAUDE_PID", "CLAUDE_EFFORT", "ANTHROPIC_BASE_URL"))}


NOMES_SKILL = {"instagram-skills:ig-hook-extractor": "gancho", "instagram-skills:ig-carousel-planner": "planejador de carrossel",
               "instagram-skills:ig-caption-writer": "legenda", "instagram-skills:ig-hashtag-strategist": "hashtags",
               "instagram-skills:ig-humanizer": "revisão anti-IA", "watch:watch": "assistir vídeo",
               "fabrica:analista": "analista", "fabrica:radar": "radar de ideias", "fabrica:produzir": "produção",
               "fabrica:trazer": "trazer assunto", "fabrica:assistir": "assistir vídeos", "fabrica:fila": "fila"}


def resumo_evento(ev):
    """Transforma uma linha do stream-json numa frase curta pra tela."""
    t = ev.get("type")
    out = []
    if t == "assistant":
        for c in (ev.get("message") or {}).get("content") or []:
            if c.get("type") == "tool_use":
                n, i = c.get("name"), c.get("input") or {}
                if n == "Skill":
                    out.append(("skill", "Usando: " + NOMES_SKILL.get(i.get('skill') or '', (i.get('skill') or '').split(':')[-1])))
                elif n == "WebSearch":
                    out.append(("busca", f"Pesquisando: {i.get('query', '')}"))
                elif n == "WebFetch":
                    out.append(("leitura", f"Lendo: {i.get('url', '')}"))
                elif n == "Bash":
                    cmd = i.get("command", "")
                    legivel = [("fab.py trilha", "Registrando a etapa"), ("fab.py memoria", "Propondo algo pra guardar"),
                               ("fab.py ideia-nova", "Criando a ideia"), ("fab.py alterar", "Salvando o post"),
                               ("fab.py publicar", "Marcando como publicado"), ("fab.py status", "Mudando o status"),
                               ("fab.py", "Lendo as ideias"), ("ler_perfil.py", "Lendo o Instagram pela Apify"),
                               ("yt-dlp", "Baixando o vídeo"), ("ffmpeg", "Separando os quadros do vídeo"),
                               ("whisper", "Transcrevendo o áudio")]
                    out.append(("comando", next((t for k, t in legivel if k in cmd), "Rodando uma etapa")))
                elif n in ("Write", "Edit"):
                    out.append(("arquivo", "Escrevendo"))
                elif n == "Read":
                    out.append(("arquivo", "Lendo o que já sei de você" if "/memoria/" in i.get("file_path", "") or "/perfil/" in i.get("file_path", "") else "Lendo"))
            elif c.get("type") == "text" and c.get("text", "").strip():
                out.append(("texto", c["text"].strip()[:400]))
    elif t == "result":
        out.append(("fim", (ev.get("result") or "").strip()[:1500]))
    return out


class Job:
    def __init__(self, acao, iid, prompt, pasta, sessao=None, retomar=False, conversa=None):
        self.id = uuid.uuid4().hex[:10]
        self.acao, self.iid, self.prompt = acao, iid, prompt
        self.eventos, self.status, self.inicio, self.fim = [], "rodando", time.time(), None
        self.erro = None
        self.pasta = pasta
        self.conversa = conversa      # id da conversa do app, quando é chat
        self.parcial = ""             # texto da resposta chegando aos pedaços
        self.resposta = ""
        claude = achar_claude()
        if not claude:
            self.status, self.erro = "erro", "Não achei o Claude Code instalado neste computador."
            return
        cmd = [claude, "-p", prompt, "--output-format", "stream-json", "--verbose",
               "--permission-mode", "acceptEdits",
               "--append-system-prompt", REGRAS_CONVERSA if conversa else REGRAS_APP,
               "--allowedTools", *FERRAMENTAS]
        if conversa:
            cmd += ["--include-partial-messages"]
        if sessao:
            cmd += (["--resume", sessao] if retomar else ["--session-id", sessao])
        self.proc = subprocess.Popen(cmd, cwd=pasta.raiz, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     stdin=subprocess.DEVNULL, text=True, bufsize=1, env=ambiente_limpo())
        threading.Thread(target=self._ler, daemon=True).start()

    def _ler(self):
        for linha in self.proc.stdout:
            linha = linha.strip()
            if not linha:
                continue
            try:
                ev = json.loads(linha)
            except json.JSONDecodeError:
                continue
            if ev.get("type") == "stream_event":
                d = (ev.get("event") or {}).get("delta") or {}
                if d.get("type") == "text_delta":
                    self.parcial += d.get("text", "")
                elif (ev.get("event") or {}).get("type") == "message_start" and self.parcial:
                    self.parcial += "\n\n"
                continue
            if ev.get("type") == "result":
                self.resposta = (ev.get("result") or "").strip()
            for tipo, txt in resumo_evento(ev):
                if self.conversa and tipo in ("texto", "fim"):
                    continue
                self.eventos.append({"tipo": tipo, "texto": txt, "t": round(time.time() - self.inicio)})
            if ev.get("type") == "result" and ev.get("is_error"):
                self.erro = (ev.get("result") or "erro")[:500]
        self.proc.wait()
        # rede de segurança: mídia de vídeo nunca fica na pasta da pessoa
        shutil.rmtree(self.pasta.p(".tmp-videos"), ignore_errors=True)
        if self.acao == "print":
            shutil.rmtree(self.pasta.p(".tmp-prints"), ignore_errors=True)
        try:
            os.remove(self.pasta.p(".tmp-perfil.md"))
        except OSError:
            pass
        try:
            os.remove(self.pasta.p(".tmp-trilha.md"))
        except OSError:
            pass
        if self.proc.returncode != 0 and not self.erro:
            self.erro = (self.proc.stderr.read() or "").strip()[-600:] or f"saiu com código {self.proc.returncode}"
        if self.erro and ("authenticat" in self.erro.lower() or "login" in self.erro.lower()):
            self.erro = ("O Claude Code deste computador está deslogado. Abra o Terminal, digite claude, "
                         "depois /login, entre com a sua conta e tente de novo.")
        self.status = "erro" if self.erro else "ok"
        self.fim = time.time()
        if self.conversa:
            self._fechar_conversa()

    def _fechar_conversa(self):
        c = self.pasta.conversa(self.conversa)
        if not c:
            return
        texto = self.resposta or self.parcial.strip() or (f"Deu erro: {self.erro}" if self.erro else "")
        etapas = [e["texto"] for e in self.eventos if e["tipo"] not in ("texto", "fim")]
        c.setdefault("mensagens", []).append({"role": "assistant", "texto": texto, "etapas": etapas,
                                              "erro": bool(self.erro), "quando": agora()})
        self.pasta.gravar_conversa(c)

    def json(self, desde=0):
        return {"id": self.id, "acao": self.acao, "ideia": self.iid, "status": self.status,
                "conversa": self.conversa, "parcial": self.parcial,
                "erro": self.erro, "eventos": self.eventos[desde:], "total": len(self.eventos),
                "segundos": round((self.fim or time.time()) - self.inicio)}


def montar_prompt(acao, corpo, P):
    iid = corpo.get("id")
    texto = (corpo.get("texto") or "").strip()
    if acao == "radar":
        return "/fabrica:radar" + (f" {texto}" if texto else ""), None, False
    if acao == "trazer":
        if not texto:
            raise ValueError("Escreva o assunto, o link da notícia ou o link do post.")
        return f"/fabrica:trazer {texto}", None, False
    if acao == "analista":
        return "/fabrica:analista", None, False
    if acao == "vencidos":
        return "/fabrica:analista vencidos", None, False
    if acao == "assistir":
        return "/fabrica:assistir" + (f" {texto}" if texto else ""), None, False
    d = P.ideia(iid) if iid else None
    if not d:
        raise ValueError("Ideia não encontrada.")
    if acao == "produzir":
        formato = corpo.get("formato") or "decida"
        sessao = d.get("sessao") or nova_sessao()
        retomar = bool(d.get("sessao"))
        P.alterar(iid, {"sessao": sessao, "status": "produzindo"})
        return f"/fabrica:produzir {iid} {formato}", sessao, retomar
    if acao == "print":
        arqs = corpo.get("arquivos") or []
        return f"/fabrica:analista print {iid} {' '.join(arqs)}", None, False
    if acao == "entregar":
        return f"/fabrica:fila entregar {iid}", None, False
    raise ValueError("Ação desconhecida.")


def abrir_conversa(P, corpo):
    """Acrescenta a mensagem da pessoa na conversa (cria se for nova) e devolve (conversa, prompt, sessao, retomar)."""
    texto = (corpo.get("texto") or "").strip()
    if not texto:
        raise ValueError("Escreva a mensagem.")
    cid, iid = corpo.get("conversa_id"), corpo.get("ideia_id")
    if iid and not cid:
        cid = "post-" + iid
    c = P.conversa(cid) if cid else None
    if not c:
        d = P.ideia(iid) if iid else None
        if iid and not d:
            raise ValueError("Ideia não encontrada.")
        cid = cid or time.strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:4]
        c = {"id": cid, "titulo": (d or {}).get("titulo") or texto.split("\n")[0][:70], "criado": agora(),
             "ideia_id": iid, "sessao": (d or {}).get("sessao"), "mensagens": []}
        # conversa antiga do "ajustar" (v0.2) vira o começo desta
        for m in (d or {}).get("conversa") or []:
            c["mensagens"].append({"role": m.get("role"), "texto": m.get("content", ""), "quando": m.get("quando")})
    retomar = bool(c.get("sessao"))
    if not retomar:
        c["sessao"] = nova_sessao()
        if iid:
            P.alterar(iid, {"sessao": c["sessao"]})
    c["mensagens"].append({"role": "user", "texto": texto, "quando": agora()})
    P.gravar_conversa(c)
    prompt = texto
    if iid:
        d = P.ideia(iid)
        prompt = (f"[Conversa sobre a ideia {iid}: \"{d.get('titulo')}\" (status {d.get('status')}). "
                  f"Se o pedido mudar o post, rode a skill fabrica:produzir com \"{iid} ajuste: <pedido>\".]\n\n{texto}")
    return c, prompt, c["sessao"], retomar


def handler(P, ui_path):
    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _env(self, code, obj, tipo="application/json"):
            body = obj if isinstance(obj, (bytes, bytearray)) else json.dumps(obj, ensure_ascii=False).encode()
            self.send_response(code)
            self.send_header("Content-Type", tipo + ("; charset=utf-8" if "json" in tipo or "html" in tipo else ""))
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _autorizado(self):
            return secrets.compare_digest(self.headers.get("X-Fabrica", ""), TOKEN)

        def do_GET(self):
            if self.path in ("/", "/index.html"):
                with open(ui_path, encoding="utf-8") as f:
                    html = f.read().replace("__TOKEN__", TOKEN)
                return self._env(200, html.encode(), "text/html")
            if not self._autorizado():
                return self._env(403, {"erro": "sem permissão"})
            if self.path == "/api/estado":
                e = P.estado()
                with LOCK:
                    e["jobs"] = [j.json(len(j.eventos)) for j in JOBS.values() if j.status == "rodando"]
                return self._env(200, e)
            if self.path.startswith("/api/conversa/"):
                c = P.conversa(self.path.split("/")[3])
                return self._env(200, c) if c else self._env(404, {"erro": "não achei"})
            if self.path.startswith("/api/job/"):
                partes = self.path.split("/")
                jid = partes[3]
                desde = int(partes[4]) if len(partes) > 4 and partes[4].isdigit() else 0
                j = JOBS.get(jid)
                return self._env(200, j.json(desde)) if j else self._env(404, {"erro": "não achei"})
            self._env(404, {"erro": "não achei"})

        def do_POST(self):
            if not self._autorizado():
                return self._env(403, {"erro": "sem permissão"})
            n = int(self.headers.get("Content-Length") or 0)
            if n > 30_000_000:
                return self._env(413, {"erro": "arquivo grande demais"})
            try:
                corpo = json.loads(self.rfile.read(n) or b"{}")
            except json.JSONDecodeError:
                return self._env(400, {"erro": "corpo inválido"})
            try:
                if self.path == "/api/feedback":
                    return self._env(200, P.feedback(corpo["id"], corpo["tipo"], (corpo.get("texto") or "")[:500]))
                if self.path == "/api/status":
                    return self._env(200, P.status(corpo["id"], corpo["status"]))
                if self.path == "/api/publicar":
                    return self._env(200, P.publicar(corpo["id"], corpo.get("link")))
                if self.path == "/api/salvar":
                    return self._env(200, P.pendente_salvar(corpo["id"], corpo.get("texto")))
                if self.path == "/api/descartar-salvar":
                    return self._env(200, P.pendente_descartar(corpo["id"]))
                if self.path == "/api/conversa":
                    with LOCK:
                        for j in JOBS.values():
                            if j.status == "rodando" and j.conversa and j.conversa in (
                                    corpo.get("conversa_id"), "post-" + (corpo.get("ideia_id") or "")):
                                return self._env(409, {"erro": "Espere a resposta anterior terminar."})
                    c, prompt, sessao, retomar = abrir_conversa(P, corpo)
                    j = Job("conversa", c.get("ideia_id"), prompt, P, sessao, retomar, conversa=c["id"])
                    with LOCK:
                        JOBS[j.id] = j
                    return self._env(200, {"conversa": c, "job": j.json()})
                if self.path == "/api/print":
                    iid = corpo["id"]
                    P.ideia(iid) or (_ for _ in ()).throw(ValueError("Ideia não encontrada."))
                    os.makedirs(P.p(".tmp-prints"), exist_ok=True)
                    arqs = []
                    for k, img in enumerate(corpo.get("imagens") or []):
                        dado = img.split(",", 1)[-1]
                        ext = "png" if "png" in img[:30] else "jpg"
                        rel = f".tmp-prints/{iid}-{k + 1}.{ext}"
                        with open(P.p(rel), "wb") as f:
                            f.write(base64.b64decode(dado))
                        arqs.append(rel)
                    if not arqs:
                        raise ValueError("Mande pelo menos um print.")
                    prompt, sessao, retomar = montar_prompt("print", {"id": iid, "arquivos": arqs}, P)
                    j = Job("print", iid, prompt, P)
                    with LOCK:
                        JOBS[j.id] = j
                    return self._env(200, j.json())
                if self.path == "/api/rodar":
                    acao = corpo.get("acao")
                    with LOCK:
                        for j in JOBS.values():
                            if j.status == "rodando" and j.acao == acao and j.iid == corpo.get("id"):
                                return self._env(200, j.json())
                    prompt, sessao, retomar = montar_prompt(acao, corpo, P)
                    j = Job(acao, corpo.get("id"), prompt, P, sessao, retomar)
                    with LOCK:
                        JOBS[j.id] = j
                    return self._env(200, j.json())
            except (KeyError, ValueError) as e:
                return self._env(400, {"erro": str(e).strip("'")})
            self._env(404, {"erro": "não achei"})

    return H


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pasta", required=True)
    ap.add_argument("--porta", type=int, default=4787)
    ap.add_argument("--abrir", action="store_true")
    a = ap.parse_args()
    P = Pasta(a.pasta)
    if not os.path.isdir(P.p("perfil")):
        print("Esta pasta ainda não tem a Fábrica. Rode /fabrica:comecar nela primeiro.")
        sys.exit(2)
    srv = None
    for porta in range(a.porta, a.porta + 20):
        try:
            srv = ThreadingHTTPServer(("127.0.0.1", porta), handler(P, os.path.join(AQUI, "ui", "index.html")))
            break
        except OSError:
            continue
    if not srv:
        sys.exit("Nenhuma porta livre entre %d e %d." % (a.porta, a.porta + 19))
    url = f"http://127.0.0.1:{srv.server_port}/"
    print(f"Fábrica aberta em {url}  (Ctrl+C pra fechar)", flush=True)
    if a.abrir:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
