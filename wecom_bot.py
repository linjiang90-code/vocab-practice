# -*- coding: utf-8 -*-
"""企业微信「智能机器人 · API 模式（长连接）」客户端。

用途：把每日 5 句推送到企业微信机器人会话（主动推送）。

官方协议（developer.work.weixin.qq.com  path/101837、document/60904）：
  1) WebSocket 连 wss://openws.work.weixin.qq.com
  2) 立刻发 aibot_subscribe {bot_id, secret}，等 {"errcode":0,"errmsg":"ok"}
  3) 每 30s 发一次 ping 保活（否则连接被回收）
  4) 收 aibot_msg_callback（消息）/ aibot_event_callback（事件）
  5) 主动推送用 aibot_send_msg（msgtype=markdown）

硬约束（踩坑点，别改）：
  - 同一机器人同一时间只能有 1 条长连接，新连接会「踢掉」旧连接。
    所以本机只应有一个实例在连：统一由 serve.py（常驻服务）持有连接。
  - 主动推送的前置条件：用户必须先在企业微信里给机器人发过消息，
    此后才能推给该会话 → 本模块在收到消息回调时缓存 chatid/chat_type。
  - 频率限制：单会话 30 条/分钟、1000 条/小时；markdown 内容 ≤ 20480 字节。
  - 凭证（Bot ID / Secret）只存本地 wecom_config.json，已被 .gitignore 排除。

用法：
  python wecom_bot.py test           # 连一次验证凭证，打印订阅结果与收到的回调
  python wecom_bot.py listen 60      # 长连接监听 60 秒，打印收到的消息
  python wecom_bot.py send "文本"     # 主动推送一条 markdown（需已有 chatid）
  python wecom_bot.py card [日期]     # 推送某天的「今日 5 句」卡片
本模块被 serve.py import 时只提供类与启动函数，不会自动连接。
"""
import asyncio
import json
import os
import threading
import time
import uuid

WSS = "wss://openws.work.weixin.qq.com"
BASE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE, "wecom_config.json")   # 凭证（gitignored）
STATE_PATH = os.path.join(BASE, "wecom_state.json")     # 运行时状态 chatid（gitignored）
HERE = BASE

HEARTBEAT = 30          # 官方建议 30s
MAX_BACKOFF = 60


def _read_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def _write_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def load_config():
    return _read_json(CONFIG_PATH, {})


def load_state():
    return _read_json(STATE_PATH, {})


def save_state(st):
    try:
        _write_json(STATE_PATH, st)
    except Exception:
        pass


def _rid():
    return uuid.uuid4().hex


def _log(msg):
    print("[wecom] %s %s" % (time.strftime("%H:%M:%S"), msg), flush=True)


class WeComBot:
    """长连接客户端。start() 后跑在独立线程的事件循环里，主线程可安全调用 send_*。"""

    def __init__(self, bot_id, secret, on_message=None):
        self.bot_id = bot_id
        self.secret = secret
        self.on_message = on_message      # callable(body, bot) -> 可选回复文本
        self.loop = None
        self.ws = None
        self.connected = False
        self.pending = {}
        self.last_error = ""
        self.thread = None
        self.stat = {"connects": 0, "recv": 0, "sent": 0,
                     "connected_at": None, "last_recv": None, "last_send": None,
                     "kicked": 0}

    # ---------------- lifecycle ----------------
    def start(self):
        if self.thread and self.thread.is_alive():
            return self.thread
        self.thread = threading.Thread(target=self._thread_main, name="wecom-bot", daemon=True)
        self.thread.start()
        return self.thread

    def _thread_main(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        try:
            self.loop.run_until_complete(self._run_forever())
        except Exception as e:
            _log("event loop exited: %r" % e)

    async def _run_forever(self):
        backoff = 1
        while True:
            try:
                reached = await self._session()
                # 能订阅成功过 → 重置退避；说明网络与凭证都正常
                if reached:
                    backoff = 1
                else:
                    backoff = min(backoff * 2, MAX_BACKOFF)
            except asyncio.CancelledError:
                raise
            except Exception as e:
                self.last_error = repr(e)
                _log("session error: %r (retry in %ss)" % (e, backoff))
                backoff = min(backoff * 2, MAX_BACKOFF)
            await asyncio.sleep(backoff)

    async def _session(self):
        import aiohttp
        async with aiohttp.ClientSession(trust_env=False) as sess:
            async with sess.ws_connect(WSS, heartbeat=None, max_msg_size=0) as ws:
                self.ws = ws
                # ⚠️ 必须先起读循环再发订阅：回执帧只有被读循环消费才能唤醒等待者，
                #    否则会误报 "ack timeout"（曾踩过：把订阅回执的真实错误码吃掉了）。
                reader = asyncio.create_task(self._read_loop(ws, aiohttp))
                ack = await self._request(ws, {
                    "cmd": "aibot_subscribe",
                    "headers": {"req_id": _rid()},
                    "body": {"bot_id": self.bot_id, "secret": self.secret},
                }, timeout=10)
                if ack.get("errcode") != 0:
                    self.last_error = "subscribe failed: %s" % json.dumps(ack, ensure_ascii=False)
                    _log(self.last_error)
                    reader.cancel()
                    return False
                self.connected = True
                self.last_error = ""
                self.stat["connects"] += 1
                self.stat["connected_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
                _log("subscribed ok (bot %s…)" % self.bot_id[:8])
                hb = asyncio.create_task(self._heartbeat(ws))
                try:
                    await reader
                finally:
                    hb.cancel()
                    self.connected = False
                    self.ws = None
                    # 未能解析的等待者全部放掉，避免 HTTP 线程永久阻塞
                    for fut in list(self.pending.values()):
                        if not fut.done():
                            fut.set_result({"errcode": -2, "errmsg": "connection closed"})
                    self.pending.clear()
                    if not self.last_error:
                        _log("disconnected, will reconnect")
                return True

    async def _read_loop(self, ws, aiohttp):
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                self._dispatch(msg.data)
            elif msg.type == aiohttp.WSMsgType.BINARY:
                self._dispatch(msg.data.decode("utf-8", "replace"))
            elif msg.type in (aiohttp.WSMsgType.CLOSED,
                              aiohttp.WSMsgType.CLOSING,
                              aiohttp.WSMsgType.ERROR):
                break

    async def _heartbeat(self, ws):
        while True:
            await asyncio.sleep(HEARTBEAT)
            try:
                await ws.send_str(json.dumps({"cmd": "ping", "headers": {"req_id": _rid()}}))
            except Exception:
                return

    async def _request(self, ws, payload, timeout=10):
        rid = payload["headers"]["req_id"]
        loop = asyncio.get_event_loop()
        fut = loop.create_future()
        self.pending[rid] = fut
        try:
            await ws.send_str(json.dumps(payload, ensure_ascii=False))
            return await asyncio.wait_for(fut, timeout=timeout)
        except asyncio.TimeoutError:
            return {"errcode": -1, "errmsg": "ack timeout"}
        finally:
            self.pending.pop(rid, None)

    # ---------------- inbound ----------------
    def _dispatch(self, raw):
        try:
            frame = json.loads(raw)
        except Exception:
            return
        if os.environ.get("WECOM_DEBUG"):
            _log("RAW %s" % (raw if isinstance(raw, str) else raw[:400]))
        cmd = frame.get("cmd")
        rid = (frame.get("headers") or {}).get("req_id")
        if not cmd:
            fut = self.pending.get(rid)
            if fut is not None and not fut.done():
                fut.set_result(frame)
            return
        self.stat["recv"] += 1
        self.stat["last_recv"] = time.strftime("%m-%d %H:%M:%S")
        if cmd == "aibot_msg_callback":
            self._on_msg(frame)
        elif cmd == "aibot_event_callback":
            self._on_event(frame)
        else:
            _log("frame: %s" % cmd)

    def _on_msg(self, frame):
        body = frame.get("body") or {}
        chattype = (body.get("chattype") or "single").lower()
        chat_type = 2 if chattype == "group" else 1
        userid = ((body.get("from") or {}).get("userid") or "")
        # 单聊回调不返回 chatid，此时的「会话 id」就是用户 userid
        chatid = body.get("chatid") or userid
        if chatid:
            st = load_state()
            st.update({"chatid": chatid, "chat_type": chat_type, "userid": userid,
                       "chattype": chattype,
                       "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")})
            save_state(st)
            _log("msg from %s (%s) chatid=%s…" % (userid, chattype, str(chatid)[:10]))
        if not self.on_message or not self.loop:
            return
        try:
            reply = self.on_message(body, self)
        except Exception as e:
            _log("on_message error: %r" % e)
            return
        if reply:
            asyncio.run_coroutine_threadsafe(
                self._send_markdown_async(reply, chatid, chat_type, 15), self.loop)

    def _on_event(self, frame):
        body = frame.get("body") or {}
        etype = body.get("eventtype") or body.get("event") or "?"
        _log("event: %s" % etype)
        if "disconnect" in str(etype).lower():
            self.stat["kicked"] += 1
            self.last_error = "被踢：同一机器人有新长连接接入"
        # 用户进入单聊会话时也可能带 chatid，顺手缓存
        chatid = body.get("chatid") or ((body.get("from") or {}).get("userid") or "")
        if chatid:
            st = load_state()
            st.setdefault("chatid", chatid)
            st["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            save_state(st)

    # ---------------- outbound ----------------
    def send_markdown(self, content, chatid=None, chat_type=None, timeout=15):
        """线程安全。返回 {"ok":bool, ...}，绝不抛异常（HTTP 层直接用）。"""
        if not self.loop:
            return {"ok": False, "error": "bot_not_started"}
        if not self.connected or self.ws is None:
            return {"ok": False, "error": "not_connected" + ((": " + self.last_error) if self.last_error else "")}
        st = load_state()
        chatid = chatid or st.get("chatid")
        if not chatid:
            return {"ok": False, "error": "no_chatid：请先在企业微信里给机器人发一条消息，再推送"}
        chat_type = int(chat_type or st.get("chat_type") or 1)
        try:
            fut = asyncio.run_coroutine_threadsafe(
                self._send_markdown_async(content, chatid, chat_type, timeout), self.loop)
            return fut.result(timeout=timeout + 5)
        except Exception as e:
            return {"ok": False, "error": repr(e)}

    async def _send_markdown_async(self, content, chatid, chat_type, timeout=15):
        ws = self.ws
        if ws is None:
            return {"ok": False, "error": "not_connected"}
        payload = {
            "cmd": "aibot_send_msg",
            "headers": {"req_id": _rid()},
            "body": {
                "chatid": chatid,
                "chat_type": int(chat_type),
                "msgtype": "markdown",
                "markdown": {"content": content[:20000]},
            },
        }
        ack = await self._request(ws, payload, timeout=timeout)
        ok = ack.get("errcode") == 0
        if ok:
            self.stat["sent"] += 1
            self.stat["last_send"] = time.strftime("%m-%d %H:%M:%S")
        else:
            _log("send failed: %s" % json.dumps(ack, ensure_ascii=False)[:300])
        return {"ok": ok, "ack": ack, "chatid": chatid, "chat_type": int(chat_type)}

    # ---------------- introspection ----------------
    def state(self):
        st = load_state()
        return {
            "enabled": True,
            "connected": bool(self.connected),
            "bot_id": (self.bot_id[:8] + "…") if self.bot_id else "",
            "last_error": self.last_error,
            "stat": self.stat,
            "chatid": st.get("chatid"),
            "chat_type": st.get("chat_type"),
            "userid": st.get("userid"),
        }


_DEFAULT_BOT = None


def start_from_config(on_message=None):
    """读取 wecom_config.json 并启动长连接。未配置/无 aiohttp 时返回 None（服务照常运行）。

    默认**不**在服务启动时抢占长连接：该机器人同一时刻只允许 1 条长连接，
    而桌面端 WorkBuddy 自身也可能连着同一个机器人，两边常驻会互相「踢」，
    表现为 disconnected_event + 偶发回执超时。因此默认按需直连（wecom_push 兜底），
    只有配置里显式 "persistent": true 时才常驻（用于「发今日」这类聊天交互）。
    """
    global _DEFAULT_BOT
    cfg = load_config()
    bot_id = (cfg.get("bot_id") or "").strip()
    secret = (cfg.get("secret") or "").strip()
    if not bot_id or not secret:
        return None
    if not cfg.get("persistent"):
        _log("persistent=false，按需直连模式（不常驻长连接）")
        return None
    try:
        import aiohttp  # noqa: F401
    except Exception as e:
        _log("aiohttp 不可用，跳过企业微信长连接: %r" % e)
        return None
    bot = WeComBot(bot_id, secret, on_message=on_message)
    bot.start()
    _DEFAULT_BOT = bot
    return bot


def get_bot():
    return _DEFAULT_BOT


# ---------------- 命令行自测 ----------------
def _cli():
    import sys
    cfg = load_config()
    if not cfg.get("bot_id") or not cfg.get("secret"):
        print("缺少 wecom_config.json（bot_id / secret）")
        return 2
    mode = sys.argv[1] if len(sys.argv) > 1 else "test"

    if mode == "test":
        bot = WeComBot(cfg["bot_id"], cfg["secret"])
        bot.start()
        t0 = time.time()
        while time.time() - t0 < 12:
            time.sleep(0.5)
            if bot.connected:
                break
        print("CONNECTED:", bot.connected)
        print("STATE:", json.dumps(bot.state(), ensure_ascii=False, indent=1))
        time.sleep(2)
        return 0 if bot.connected else 1

    if mode == "listen":
        secs = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        bot = WeComBot(cfg["bot_id"], cfg["secret"],
                       on_message=lambda body, b: "收到 👋 发「今日」我给你推今天的 5 句。")
        bot.start()
        print("listening %ss … 请在企业微信里给机器人发一条消息" % secs)
        time.sleep(secs)
        print("STATE:", json.dumps(bot.state(), ensure_ascii=False, indent=1))
        return 0

    if mode == "send":
        text = sys.argv[2] if len(sys.argv) > 2 else "测试消息"
        bot = WeComBot(cfg["bot_id"], cfg["secret"])
        bot.start()
        t0 = time.time()
        while time.time() - t0 < 12 and not bot.connected:
            time.sleep(0.3)
        print(json.dumps(bot.send_markdown(text), ensure_ascii=False, indent=1))
        time.sleep(1)
        return 0

    if mode == "card":
        import wecom_push
        date = sys.argv[2] if len(sys.argv) > 2 else None
        content = wecom_push.build_card(date)
        print(content)
        bot = WeComBot(cfg["bot_id"], cfg["secret"])
        bot.start()
        t0 = time.time()
        while time.time() - t0 < 12 and not bot.connected:
            time.sleep(0.3)
        print(json.dumps(bot.send_markdown(content), ensure_ascii=False, indent=1))
        time.sleep(1)
        return 0

    print("未知模式: %s" % mode)
    return 2


if __name__ == "__main__":
    raise SystemExit(_cli())
