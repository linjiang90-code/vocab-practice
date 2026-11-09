# -*- coding: utf-8 -*-
"""把每日 5 句做成企业微信 markdown 卡片并推送。

两种传输方式（按 wecom_config.json 的配置自动选择）：
  1) 智能机器人长连接（默认）：POST 到本机常驻服务的 /api/wecom/push
     —— 由 serve.py 持有 WebSocket 长连接，本脚本只负责组装内容。
  2) 群机器人 Webhook（可选兜底）：config 里填 webhook_url 即可，纯 HTTPS POST，无需常驻进程。

用法：
  python wecom_push.py                 # 推送今天
  python wecom_push.py 2026-11-09      # 推送指定日期
  python wecom_push.py 2026-11-09 --dry# 只打印卡片，不发送
"""
import datetime
import json
import os
import re
import sys
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
MASTER = os.path.join(BASE, "master.json")
DAYS = os.path.join(BASE, "days.json")
CONFIG_PATH = os.path.join(BASE, "wecom_config.json")
LOCAL_API = "http://127.0.0.1:3279/api/wecom/push"
DEFAULT_SITE = "http://125.71.210.3:3279"

WEEK = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

# 企业微信「智能机器人（API 模式）」的 markdown 只支持标准语法，
# 不支持 <font color="..."> 这类 HTML（那是群机器人 Webhook 才有的扩展），
# 传进去会被原样显示成乱码般的标签文本，所以这里统一清洗掉。
_TAG_RE = re.compile(r"</?[a-zA-Z][^>]{0,80}>")


def _sanitize_md(text):
    """去掉 markdown 正文里不被支持的 HTML 标签。"""
    return _TAG_RE.sub("", text)


def _load(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def _site():
    cfg = _load(CONFIG_PATH, {})
    return (cfg.get("site") or DEFAULT_SITE).rstrip("/")


def build_card(date=None, master=None):
    """组装 markdown 卡片文本。date 为 None 时取今天。"""
    if date is None:
        date = datetime.date.today().isoformat()
    d = datetime.date.fromisoformat(date)

    m = master or _load(MASTER, {})
    if not m.get("sentences"):
        raise SystemExit("master.json 读取失败")
    side = _load(os.path.join(BASE, "day%s.json" % date), {})
    ids = side.get("ids") or []
    if not ids:
        raise SystemExit("没有 %s 的选句记录（day%s.json），可能当天还没生成" % (date, date))

    by_id = {s["id"]: s for s in m["sentences"]}
    meta = m.get("meta") or {}
    start = datetime.date.fromisoformat(meta.get("startDate") or date)
    day_index = (d - start).days + 1

    days = _load(DAYS, [])
    practiced = len(set(days)) if isinstance(days, list) else 0
    introduced = sum(1 for s in m["sentences"] if s.get("learn", {}).get("introduced"))

    lines = []
    lines.append("# 📅 今日英语口语 · Day %d" % day_index)
    lines.append("**%s %s** ｜ %d 句 ｜ 点开练习页可点读跟读" % (date, WEEK[d.weekday()], len(ids)))
    lines.append("")
    for i, sid in enumerate(ids, 1):
        s = by_id.get(sid)
        if not s:
            continue
        tag = "🆕 " if not s.get("learn", {}).get("introduced") else ""
        lines.append("**%d.** %s%s" % (i, tag, s.get("en", "")))
        lines.append("　%s" % (s.get("zh") or ""))
        kv = s.get("keyvocab") or []
        if kv:
            terms = " · ".join("%s %s" % (k.get("term", ""), k.get("ipa", "")) for k in kv[:4])
            lines.append("　🔈 %s" % terms.strip())
        lines.append("")
    lines.append("[👉 打开今日练习页（点读 / 跟读 / 自评掌握度）](%s/day%s.html)" % (_site(), date))
    lines.append("")
    lines.append("> 累计已学 %d 句 ｜ 已练习 %d 天 ｜ 词库 %d 句" % (
        introduced, practiced, len(m["sentences"])))
    return _sanitize_md("\n".join(lines))


def push_via_local_api(card, date):
    """交给常驻服务（持有长连接）发出去。"""
    body = json.dumps({"date": date, "content": card}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(LOCAL_API, data=body,
                                headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.loads(r.read().decode("utf-8") or "{}")
    except Exception as e:
        return {"ok": False, "error": "local_api_unreachable: %r" % e}


def push_via_webhook(card, webhook_url):
    body = json.dumps({"msgtype": "markdown", "markdown": {"content": card}},
                      ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(webhook_url, data=body,
                                headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode("utf-8") or "{}")
    except Exception as e:
        return {"ok": False, "error": "webhook_failed: %r" % e}


def push(date=None, content=None, dry=False):
    date = date or datetime.date.today().isoformat()
    card = content or build_card(date)
    if dry:
        return {"ok": True, "dry": True, "content": card}
    cfg = _load(CONFIG_PATH, {})
    hook = (cfg.get("webhook_url") or "").strip()
    if hook:
        return push_via_webhook(card, hook)
    res = push_via_local_api(card, date)
    if res.get("ok"):
        return res
    # 兜底：常驻服务还没重启到新版（或没在跑）时，直接自己连一次长连接发完就断开。
    # 该机器人同时只允许 1 条长连接，因此这只是短时占用，serve.py 的客户端会自动重连。
    fallback = _push_direct(card)
    fallback["local_api_error"] = res.get("error") or res.get("detail")
    return fallback


def _push_direct(card, wait=15, attempts=3):
    """直连发送（短时占用长连接）。该机器人同一时刻只允许 1 条连接，
    而桌面端也可能连着同一个机器人，会偶发把连接顶掉导致回执超时，
    所以这里必须重建连接重试，而不是一次失败就放弃。"""
    try:
        import time
        import wecom_bot
    except Exception as e:
        return {"ok": False, "error": "direct_unavailable: %r" % e}
    cfg = _load(CONFIG_PATH, {})
    if not (cfg.get("bot_id") and cfg.get("secret")):
        return {"ok": False, "error": "no_credentials"}
    last = {"ok": False, "error": "not_started"}
    for i in range(attempts):
        bot = wecom_bot.WeComBot(cfg["bot_id"], cfg["secret"])
        bot.start()
        t0 = time.time()
        while time.time() - t0 < wait and not bot.connected:
            time.sleep(0.3)
        if not bot.connected:
            last = {"ok": False, "error": "direct_not_connected: %s" % bot.last_error}
        else:
            last = bot.send_markdown(card)
            if last.get("ok"):
                last["attempt"] = i + 1
                return last
        time.sleep(3)
    last["attempts"] = attempts
    return last


def main(argv):
    dry = "--dry" in argv
    args = [a for a in argv[1:] if not a.startswith("--")]
    date = args[0] if args else None
    res = push(date=date, dry=dry)
    if dry:
        print(res.get("content", ""))
        return 0
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0 if res.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
