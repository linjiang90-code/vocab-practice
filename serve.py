# -*- coding: utf-8 -*-
"""本地服务：托管 vocab-practice 目录，并提供掌握度回写 API。
用法：python serve.py  然后浏览器打开 http://127.0.0.1:3279/
- GET  /               -> index.html（一键预览入口）
- GET  /master.html    -> 100 句总览
- GET  /day*.html      -> 当日练习页
- GET  /api/status     -> 健康检查
- GET  /api/mastery    -> 返回全部句掌握度
- POST /api/mastery    -> 回写某句掌握度 {id, action: clear|fuzzy|unknown}
- GET  /cars-2026.html -> 2026 市售车型统计表（动态转发到车展项目源文件，始终最新）
- GET  /api/wecom/state-> 企业微信机器人长连接状态（是否已连、是否已拿到 chatid）
- POST /api/wecom/push -> 把某天的 5 句推送到企业微信 {date?, content?}
跨域（CORS）已放开，因此从 WorkBuddy 预览页(其他端口)打开也能回写。
（已取消 HTTP Basic Auth，访问无需账号密码。）

企业微信机器人（2026-11-09 接入）：
  本服务同时持有「智能机器人 · API 模式（长连接）」的 WebSocket。
  放在常驻服务里而不是单独进程，是因为该机器人同一时刻只允许 1 条长连接，
  且推送必须依赖连接存活——serve.py 已由任务计划开机自启 + 崩溃自重启，
  天然满足常驻要求，无需再建一个计划任务。
  前置条件：用户须先在企业微信里给机器人发过消息，chatid 才会被缓存。
"""
import json, os, threading, datetime
from http.server import HTTPServer, ThreadingHTTPServer, SimpleHTTPRequestHandler
import gen_views_html  # 自评回写后重建「已学回顾/学习日历」内嵌数据页
import wecom_push       # 组装每日 5 句 markdown 卡片

try:
    import wecom_bot
except Exception:        # 未装 aiohttp / 缺依赖时不影响站点其它功能
    wecom_bot = None

BASE = os.path.dirname(os.path.abspath(__file__))
MASTER = os.path.join(BASE, "master.json")
PORT = 3279
lock = threading.Lock()
WECOM_BOT = None        # 由 __main__ 启动后赋值；HTTP 线程只读


def _wecom_reply(body, bot):
    """收到用户消息时的自动回复：发「今日/明天」回对应卡片，其它给一句提示。"""
    text = ((body.get("text") or {}).get("content") or "").strip().lower()
    today = datetime.date.today()
    try:
        if any(k in text for k in ("今日", "今天", "today", "学", "句子", "推送")):
            return wecom_push.build_card(today.isoformat())
        if any(k in text for k in ("明日", "明天", "tomorrow", "预览")):
            return wecom_push.build_card((today + datetime.timedelta(days=1)).isoformat())
    except SystemExit as e:
        return "⚠️ %s" % e
    except Exception as e:
        return "⚠️ 生成失败：%r" % e
    return ("👋 我是「词力」口语教练的推送机器人。\n"
            "发 **今日** → 今天的 5 句\n发 **明天** → 明天的预习句\n"
            "每天 09:00 也会自动推一次。")

# 构建版本号：每次页面有大改或修复乱码后递增，serve.py 会对所有 *.html 请求
# 302 跳转到带 ?v=BUILD 的 URL，强制浏览器 / 省流量代理重新拉取最新内容，
# 彻底破除「8-20~8-22 期间缓存的坏副本」导致的整页中文乱码假象。
BUILD = "20261010a"

# 2026 市售车型统计表：由「2026 成都车展」项目持续维护的活文档（在外部工作区）。
# /cars-2026.html 动态读取该源文件返回 —— 源文件更新即站点同步最新，无需复制副本。
# vocab-practice/cars-2026.html 仅是接入前的快照兜底；本路由优先级高于静态文件。
CARS_SRC = r"C:\Users\Win10\WorkBuddy\2026-08-21-13-30-20\2026市售车型统计表.html"

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
        if p == "/api/wecom/state":
            if WECOM_BOT is None:
                return self._send(200, json.dumps(
                    {"enabled": False, "reason": "未配置 wecom_config.json 或缺少 aiohttp"}))
            return self._send(200, json.dumps(WECOM_BOT.state(), ensure_ascii=False))
        # 2026 市售车型统计表：动态读车展项目源文件（每次请求现读，始终最新）
        if p == "/cars-2026.html":
            try:
                with open(CARS_SRC, "rb") as f:
                    body = f.read()
                # 站点侧注入「返回首页」浮动按钮（右下角，避开 sticky 表头）。
                # 只改转发内容、不碰源文件——车展项目继续维护原文件，按钮永不丢失。
                inject = ('<div style="position:fixed;bottom:16px;right:14px;z-index:99999;">'
                          '<a href="/index.html" style="display:block;text-decoration:none;'
                          'background:#2f6fed;color:#fff;font-size:14px;font-weight:700;'
                          'padding:11px 18px;border-radius:999px;box-shadow:0 3px 10px rgba(0,0,0,.25);'
                          'font-family:-apple-system,PingFang SC,Microsoft YaHei,sans-serif;">'
                          '🏠 返回首页</a></div>').encode("utf-8")
                i = body.find(b"<body")
                if i != -1:
                    j = body.find(b">", i)
                    if j != -1:
                        body = body[:j + 1] + inject + body[j + 1:]
                return self._send(200, body, "text/html; charset=utf-8")
            except Exception as e:
                return self._send(500, json.dumps(
                    {"error": "cars source unreadable: %r" % e}))
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
        if self.path == "/api/wecom/push":
            # 每日推送入口：自动化/命令行只需 POST 一个日期，内容由服务端组装
            try:
                ln = int(self.headers.get("Content-Length", 0) or 0)
                raw = self.rfile.read(ln) if ln else b"{}"
                data = json.loads(raw or b"{}")
                date = data.get("date") or datetime.date.today().isoformat()
                content = data.get("content") or wecom_push.build_card(date)
                if WECOM_BOT is None:
                    # 未常驻长连接（默认按需模式）：直接用短连接发一次，避免与桌面端抢连接
                    res = wecom_push._push_direct(content)
                    res["date"] = date
                    res["mode"] = "direct"
                    return self._send(200 if res.get("ok") else 502,
                                      json.dumps(res, ensure_ascii=False))
                res = WECOM_BOT.send_markdown(content, data.get("chatid"), data.get("chat_type"))
                # 长连接可能正在重连（该机器人同时只允许 1 条连接，可能被其它客户端顶掉，
                # 表现为 not_connected 或回执超时），短暂等待后重试，避免每日推送整体失败。
                tries = 0
                while (not res.get("ok")) and tries < 3:
                    tries += 1
                    import time as _t
                    _t.sleep(5)
                    res = WECOM_BOT.send_markdown(content, data.get("chatid"), data.get("chat_type"))
                if tries:
                    res["retries"] = tries
                res["date"] = date
                return self._send(200 if res.get("ok") else 502,
                                  json.dumps(res, ensure_ascii=False))
            except SystemExit as e:
                return self._send(404, json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
            except Exception as e:
                return self._send(500, json.dumps({"ok": False, "error": repr(e)}, ensure_ascii=False))
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
    # 企业微信机器人长连接：由本常驻服务持有（同一机器人只允许 1 条长连接）
    if wecom_bot is not None:
        try:
            WECOM_BOT = wecom_bot.start_from_config(_wecom_reply)
            print("wecom bot: %s" % ("long link starting…" if WECOM_BOT else
                                     "not configured (缺 wecom_config.json)"), flush=True)
        except Exception as e:
            print("wecom bot start failed: %r" % (e,), flush=True)
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
