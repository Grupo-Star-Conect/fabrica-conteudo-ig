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
from dados import Pasta, nova_sessao  # noqa: E402

TOKEN = secrets.token_urlsafe(24)
JOBS = {}
LOCK = threading.Lock()
FERRAMENTAS = [
    "Read", "Write", "Edit", "Glob", "Grep", "WebSearch", "WebFetch", "Skill", "TodoWrite",
    "Bash(python3:*)", "Bash(python:*)", "Bash(yt-dlp:*)", "Bash(ffmpeg:*)", "Bash(ffprobe:*)",
    "Bash(ls:*)", "Bash(mkdir:*)",
]


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


def resumo_evento(ev):
    """Transforma uma linha do stream-json numa frase curta pra tela."""
    t = ev.get("type")
    out = []
    if t == "assistant":
        for c in (ev.get("message") or {}).get("content") or []:
            if c.get("type") == "tool_use":
                n, i = c.get("name"), c.get("input") or {}
                if n == "Skill":
                    out.append(("skill", f"Skill: {i.get('skill') or i.get('command') or ''}"))
                elif n == "WebSearch":
                    out.append(("busca", f"Pesquisando: {i.get('query', '')}"))
                elif n == "WebFetch":
                    out.append(("leitura", f"Lendo: {i.get('url', '')}"))
                elif n == "Bash":
                    cmd = i.get("command", "")
                    if "fab.py trilha" in cmd:
                        out.append(("etapa", "Etapa registrada na trilha"))
                    else:
                        out.append(("comando", f"Executando: {cmd[:110]}"))
                elif n in ("Write", "Edit"):
                    out.append(("arquivo", f"Gravando: {os.path.basename(i.get('file_path', ''))}"))
                elif n == "Read":
                    out.append(("arquivo", f"Lendo arquivo: {os.path.basename(i.get('file_path', ''))}"))
            elif c.get("type") == "text" and c.get("text", "").strip():
                out.append(("texto", c["text"].strip()[:400]))
    elif t == "result":
        out.append(("fim", (ev.get("result") or "").strip()[:1500]))
    return out


class Job:
    def __init__(self, acao, iid, prompt, pasta, sessao=None, retomar=False):
        self.id = uuid.uuid4().hex[:10]
        self.acao, self.iid, self.prompt = acao, iid, prompt
        self.eventos, self.status, self.inicio, self.fim = [], "rodando", time.time(), None
        self.erro = None
        claude = achar_claude()
        if not claude:
            self.status, self.erro = "erro", "Não achei o Claude Code instalado neste computador."
            return
        cmd = [claude, "-p", prompt, "--output-format", "stream-json", "--verbose",
               "--permission-mode", "acceptEdits", "--allowedTools", *FERRAMENTAS]
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
            for tipo, txt in resumo_evento(ev):
                self.eventos.append({"tipo": tipo, "texto": txt, "t": round(time.time() - self.inicio)})
            if ev.get("type") == "result" and ev.get("is_error"):
                self.erro = (ev.get("result") or "erro")[:500]
        self.proc.wait()
        if self.proc.returncode != 0 and not self.erro:
            self.erro = (self.proc.stderr.read() or "").strip()[-600:] or f"saiu com código {self.proc.returncode}"
        if self.erro and ("authenticat" in self.erro.lower() or "login" in self.erro.lower()):
            self.erro = ("O Claude Code deste computador está deslogado. Abra o Terminal, digite claude, "
                         "depois /login, entre com a sua conta e tente de novo.")
        self.status = "erro" if self.erro else "ok"
        self.fim = time.time()

    def json(self, desde=0):
        return {"id": self.id, "acao": self.acao, "ideia": self.iid, "status": self.status,
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
    if acao == "ajustar":
        if not texto:
            raise ValueError("Escreva o que ajustar.")
        conv = d.get("conversa") or []
        conv.append({"role": "user", "content": texto, "quando": time.strftime("%Y-%m-%dT%H:%M")})
        sessao = d.get("sessao") or nova_sessao()
        retomar = bool(d.get("sessao"))
        P.alterar(iid, {"conversa": conv, "sessao": sessao})
        return f"/fabrica:produzir {iid} ajuste: {texto}", sessao, retomar
    if acao == "entregar":
        return f"/fabrica:fila entregar {iid}", None, False
    raise ValueError("Ação desconhecida.")


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
            try:
                corpo = json.loads(self.rfile.read(n) or b"{}")
            except json.JSONDecodeError:
                return self._env(400, {"erro": "corpo inválido"})
            try:
                if self.path == "/api/feedback":
                    return self._env(200, P.feedback(corpo["id"], corpo["tipo"], (corpo.get("texto") or "")[:500]))
                if self.path == "/api/status":
                    return self._env(200, P.status(corpo["id"], corpo["status"]))
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
