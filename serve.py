# -*- coding: utf-8 -*-
"""本地服务：托管 vocab-practice 目录，并提供掌握度回写 API。
用法：python serve.py  然后浏览器打开 http://127.0.0.1:3279/
- GET  /               -> index.html（一键预览入口）
- GET  /master.html    -> 100 句总览
- GET  /day*.html      -> 当日练习页
- GET  /api/status     -> 健康检查
- GET  /api/mastery    -> 返回全部句掌握度
- POST /api/mastery    -> 回写某句掌握度 {id, action: clear|fuzzy|unknown}
跨域（CORS）已放开，因此从 WorkBuddy 预览页(其他端口)打开也能回写。
所有请求需 HTTP Basic Auth（凭据在 gitignored 的 serve_auth.json 中，切勿提交到公开仓库）。
浏览器首次访问会弹出登录框，输入后同源请求自动带凭证。
"""
import json, os, threading, datetime, base64
from http.server import HTTPServer, ThreadingHTTPServer, SimpleHTTPRequestHandler

BASE = os.path.dirname(os.path.abspath(__file__))
MASTER = os.path.join(BASE, "master.json")
PORT = 3279
lock = threading.Lock()

AUTH_FILE = os.path.join(BASE, "serve_auth.json")

def load_creds():
    """从 gitignored 的 serve_auth.json 读取 (user, password)。文件缺失则锁定服务。"""
    try:
        with open(AUTH_FILE, encoding="utf-8") as f:
            d = json.load(f)
        return d.get("user", ""), d.get("password", "")
    except Exception:
        return "", ""

CORS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}

def load_master():
    with open(MASTER, encoding="utf-8") as f:
        return json.load(f)

def save_master(d):
    tmp = MASTER + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    os.replace(tmp, MASTER)

class H(SimpleHTTPRequestHandler):
    def setup(self):
        super().setup()
        # 防止客户端半开/慢速连接永久阻塞线程、拖垮整个服务（曾出现占端口却不响应）
        self.connection.settimeout(60)

    def _send(self, code, body=b"", ctype="application/json"):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        for k, v in CORS.items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def do_OPTIONS(self):
        self._send(204)

    def _auth_ok(self):
        user, pwd = load_creds()
        if not user or not pwd:
            return False  # 未配置凭据 -> 锁定服务
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Basic "):
            return False
        try:
            decoded = base64.b64decode(auth[6:]).decode("utf-8", "ignore")
            u, _, p = decoded.partition(":")
            return u == user and p == pwd
        except Exception:
            return False

    def _require_auth(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="vocab-practice"')
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"401 Authorization Required")

    def do_HEAD(self):
        if not self._auth_ok():
            return self._require_auth()
        return super().do_HEAD()

    def do_GET(self):
        if not self._auth_ok():
            return self._require_auth()
        if self.path == "/api/status":
            return self._send(200, json.dumps({"ok": True, "port": PORT}))
        if self.path == "/api/mastery":
            try:
                d = load_master()
                out = [{"id": s["id"],
                        "mastery": int(s["learn"]["mastery"] or 0),
                        "reviewCount": s["learn"]["reviewCount"],
                        "lastReviewed": s["learn"]["lastReviewed"],
                        "introduced": bool(s["learn"]["introduced"])}
                       for s in d["sentences"]]
                return self._send(200, json.dumps({"sentences": out}))
            except Exception as e:
                return self._send(500, json.dumps({"error": str(e)}))
        return super().do_GET()

    def do_POST(self):
        if not self._auth_ok():
            return self._require_auth()
        if self.path == "/api/mastery":
            try:
                ln = int(self.headers.get("Content-Length", 0) or 0)
                raw = self.rfile.read(ln) if ln else b"{}"
                data = json.loads(raw or b"{}")
                sid = int(data.get("id"))
                action = data.get("action")
                if action not in ("clear", "fuzzy", "unknown"):
                    return self._send(400, json.dumps({"error": "bad action"}))
                with lock:
                    d = load_master()
                    s = next((x for x in d["sentences"] if x["id"] == sid), None)
                    if not s:
                        return self._send(404, json.dumps({"error": "not found"}))
                    m = int(s["learn"]["mastery"] or 0)
                    today = datetime.date.today().isoformat()
                    if action == "clear":
                        m = min(5, m + 1)
                        s["learn"]["lastReviewed"] = today
                        s["learn"]["reviewCount"] = (s["learn"]["reviewCount"] or 0) + 1
                    elif action == "unknown":
                        m = max(0, m - 1)
                        s["learn"]["lastReviewed"] = today
                    elif action == "fuzzy":
                        s["learn"]["lastReviewed"] = today
                    s["learn"]["mastery"] = m
                    save_master(d)
                return self._send(200, json.dumps({"ok": True, "id": sid, "mastery": m}))
            except Exception as e:
                return self._send(500, json.dumps({"error": str(e)}))
        return self._send(404, json.dumps({"error": "not found"}))

if __name__ == "__main__":
    os.chdir(BASE)
    srv = ThreadingHTTPServer(("0.0.0.0", PORT), H)
    srv.daemon_threads = True
    print("vocab serve on http://127.0.0.1:%d (threading)" % PORT)
    srv.serve_forever()
