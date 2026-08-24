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
（已取消 HTTP Basic Auth，访问无需账号密码。）
"""
import json, os, threading, datetime
from http.server import HTTPServer, ThreadingHTTPServer, SimpleHTTPRequestHandler
import gen_views_html  # 自评回写后重建「已学回顾/学习日历」内嵌数据页

BASE = os.path.dirname(os.path.abspath(__file__))
MASTER = os.path.join(BASE, "master.json")
PORT = 3279
lock = threading.Lock()

# 构建版本号：每次页面有大改或修复乱码后递增，serve.py 会对所有 *.html 请求
# 302 跳转到带 ?v=BUILD 的 URL，强制浏览器 / 省流量代理重新拉取最新内容，
# 彻底破除「8-20~8-22 期间缓存的坏副本」导致的整页中文乱码假象。
BUILD = "20260824b"

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
    def guess_type(self, path):
        # 强制为 text/* 资源声明 UTF-8 编码，避免浏览器把 UTF-8 中文误当 GBK 解析成乱码
        # （曾出现「较早打开的页面正常、之后新页面整页中文乱码」的边界现象，
        #   根因即响应头未声明 charset 时浏览器对新文件猜测编码出错）
        t = super().guess_type(path)
        if t.startswith("text/") and "charset" not in t.lower():
            return t + "; charset=utf-8"
        return t

    def setup(self):
        super().setup()
        # 防止客户端半开/慢速连接永久阻塞线程、拖垮整个服务（曾出现占端口却不响应）
        self.connection.settimeout(60)

    def end_headers(self):
        # 禁用静态资源缓存：前端(cards.js 等)频繁改动，避免远程浏览器长期使用旧缓存
        # 导致「改了却像没生效 / 朗读无声」等缓存假象。API 不受影响（仍走 _send）。
        self.send_header("Cache-Control", "no-store, max-age=0")
        self.send_header("Pragma", "no-cache")
        super().end_headers()

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

    def do_HEAD(self):
        return super().do_HEAD()

    def do_GET(self):
        # 缓存击穿：所有静态 HTML 请求强制带版本号，杜绝旧缓存副本（含代理缓存）
        p = self.path.split("?", 1)[0]
        if p.endswith(".html") and "v=" not in self.path:
            sep = "&" if "?" in self.path else "?"
            self.send_response(302)
            self.send_header("Location", self.path + sep + "v=" + BUILD)
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            return
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
                    try:
                        # 重新加载生成器模块，避免使用服务启动时锁进内存的旧版代码
                        # （曾因旧版 gen_views_html 在每次回写时重建 review/calendar，
                        #  把新增的 mastery.js 引用覆盖掉，导致多页自评失效）
                        import importlib
                        importlib.reload(gen_views_html)
                        gen_views_html.main()
                    except Exception:
                        pass
                return self._send(200, json.dumps({"ok": True, "id": sid, "mastery": m}))
            except Exception as e:
                return self._send(500, json.dumps({"error": str(e)}))
        return self._send(404, json.dumps({"error": "not found"}))

if __name__ == "__main__":
    os.chdir(BASE)
    import signal
    # 忽略客户端断开导致的 BrokenPipe，避免 handler 线程异常冒泡
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_IGN)
    except Exception:
        pass
    # 崩溃自重启：serve_forever 若异常退出，等待后自动拉起，避免长时间假死无服务
    while True:
        try:
            srv = ThreadingHTTPServer(("0.0.0.0", PORT), H)
        except OSError as e:
            # 端口被占用（已有实例在跑）→ 不要自重启空转，直接退出，避免多实例抢端口
            print("vocab serve: port %d already in use (%r) — another instance is running, exit." % (PORT, e), flush=True)
            break
        try:
            srv.daemon_threads = True
            print("vocab serve on http://127.0.0.1:%d (threading, self-healing)" % PORT, flush=True)
            srv.serve_forever()
        except KeyboardInterrupt:
            print("vocab serve stopped by user", flush=True)
            break
        except Exception as e:
            print("vocab serve crashed: %r — restarting in 3s" % e, flush=True)
            try:
                srv.server_close()
            except Exception:
                pass
            import time
            time.sleep(3)
