# -*- coding: utf-8 -*-
"""把每日 5 句做成企业微信 markdown 卡片并推送。

两种传输方式（按 wecom_config.json 的配置自动选择）：
  1) 智能机器人长连接（默认）：POST 到本机常驻服务的 /api/wecom/push
     —— 由 serve.py 持有 WebSocket 长连接，本脚本只负责组装内容。
  2) 群机器人 Webhook（可选兜底）：config 里填 webhook_url 即可，纯 HTTPS POST，无需常驻进程。

卡片有 4 种形态，按小时自动轮换，避免一天 13 次推送全是同一张脸：
  0 全览     —— 5 句英文 + 中文 + 关键词音标
  1 精讲     —— 聚焦其中 1 句：整句音标 / 3 个变体 / 3 个场景 / 语法点
  2 中译英   —— 只给中文 + 关键词提示，末尾附答案（碎片时间自测）
  3 发音要点 —— 5 句的音标 + 连读弱读浊化提示

用法：
  python wecom_push.py                 # 推送今天，形态按当前小时自动轮换
  python wecom_push.py 2026-11-09      # 推送指定日期
  python wecom_push.py --mode 2        # 强制指定形态（0-3）
  python wecom_push.py --dry           # 只打印卡片，不发送
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
# 传进去会被原样显示成标签文本，所以这里统一清洗掉。
_TAG_RE = re.compile(r"</?[a-zA-Z][^>]{0,80}>")

MODE_NAME = {0: "全览", 1: "精讲", 2: "中译英自测", 3: "发音要点"}

# 每个整点 30 分推一次，09:30 起、21:30 收尾（22 点收工）
PUSH_HOURS = list(range(9, 22))


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


def _clip(text, limit=170):
    """截断过长的说明文字，保持单条推送轻量。"""
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    cut = text[:limit]
    # 尽量停在句号/分号处，避免半句截断
    for sep in ("。", "；", "，"):
        pos = cut.rfind(sep)
        if pos > limit * 0.55:
            return cut[:pos + 1] + "…"
    return cut + "…"


def auto_mode(hour=None):
    """整点轮换：09:30 全览 → 10:30 精讲 → 11:30 中译英 → 12:30 发音 → 循环。"""
    if hour is None:
        hour = datetime.datetime.now().hour
    if hour < 9:
        return 0
    return (hour - 9) % 4


def _focus_index(hour=None):
    """精讲轮换：一天 3 次精讲（10:30/14:30/18:30）依次覆盖第 1/2/3 句。"""
    if hour is None:
        hour = datetime.datetime.now().hour
    if hour < 10:
        return 0
    return ((hour - 10) // 4) % 5


def _resolve_day(date):
    """返回 (实际日期, ids)。当天页还没生成时，回退到最近一期，保证提醒不断档。"""
    side = _load(os.path.join(BASE, "day%s.json" % date), {})
    ids = side.get("ids") or []
    if ids:
        return date, ids
    # 回退：找 <= date 的最近一份侧车
    cands = []
    for name in os.listdir(BASE):
        m = re.fullmatch(r"day(\d{4}-\d{2}-\d{2})\.json", name)
        if m and m.group(1) <= date:
            cands.append(m.group(1))
    for d in sorted(cands, reverse=True):
        side = _load(os.path.join(BASE, "day%s.json" % d), {})
        ids = side.get("ids") or []
        if ids:
            return d, ids
    raise SystemExit("没有 %s 及之前的选句记录（dayYYYY-MM-DD.json）" % date)


def _header(day_index, date, suffix):
    d = datetime.date.fromisoformat(date)
    return [
        "# 📅 今日英语口语 · Day %d" % day_index,
        "**%s %s** ｜ %s" % (date, WEEK[d.weekday()], suffix),
        "",
    ]


def _mode_overview(ids, by_id, day_index, date):
    lines = _header(day_index, date, "%d 句全览 ｜ 点开练习页可点读跟读" % len(ids))
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
    return lines


def _mode_focus(ids, by_id, day_index, date, hour):
    # 一天 3 次精讲依次覆盖 3 句；叠加 day_index 让 5 句在几天内轮流被讲到
    idx = (_focus_index(hour) + day_index - 1) % max(1, len(ids))
    sid = ids[idx]
    s = by_id.get(sid) or {}
    enh = (s.get("learn") or {}).get("enh") or {}
    lines = _header(day_index, date, "精讲第 %d/%d 句 ｜ 一句吃透" % (idx + 1, len(ids)))
    lines.append("**%s**" % (s.get("en") or ""))
    lines.append("　%s" % (s.get("zh") or ""))
    if enh.get("fullIpa"):
        lines.append("　🔈 %s" % enh["fullIpa"])
    lines.append("")

    variants = enh.get("variants") or []
    if variants:
        lines.append("**换个说法**")
        for v in variants[:3]:
            if isinstance(v, (list, tuple)) and len(v) >= 2:
                lines.append("· %s — %s" % (v[0], v[1]))
        lines.append("")

    scenes = enh.get("scenes") or []
    if scenes:
        lines.append("**这样用**")
        for sc in scenes[:2]:
            if isinstance(sc, (list, tuple)) and len(sc) >= 2:
                note = sc[2] if len(sc) > 2 else ""
                lines.append("· %s：%s%s" % (sc[0], sc[1], (" — " + note) if note else ""))
        lines.append("")

    if enh.get("grammar"):
        lines.append("**语法点**")
        lines.append("　%s" % _clip(enh["grammar"], 120))
        lines.append("")
    lines.append("[👉 点开练习页听原声](%s/day%s.html)" % (_site(), date))
    return lines


def _mode_quiz(ids, by_id, day_index, date):
    lines = _header(day_index, date, "%d 句中译英自测 ｜ 先默说，再对答案" % len(ids))
    for i, sid in enumerate(ids, 1):
        s = by_id.get(sid) or {}
        lines.append("**%d.** %s" % (i, s.get("zh") or ""))
        kv = s.get("keyvocab") or []
        if kv:
            hint = " · ".join(k.get("term", "") for k in kv[:3])
            lines.append("　提示：%s" % hint)
        lines.append("")
    lines.append("---")
    lines.append("**答案**")
    for i, sid in enumerate(ids, 1):
        s = by_id.get(sid) or {}
        lines.append("%d. %s" % (i, s.get("en") or ""))
    lines.append("")
    lines.append("[👉 逐句点读纠音](%s/day%s.html)" % (_site(), date))
    return lines


def _mode_pron(ids, by_id, day_index, date):
    lines = _header(day_index, date, "发音要点 ｜ 连读 · 弱读 · 浊化")
    for i, sid in enumerate(ids, 1):
        s = by_id.get(sid) or {}
        enh = (s.get("learn") or {}).get("enh") or {}
        lines.append("**%d.** %s" % (i, s.get("en") or ""))
        if enh.get("fullIpa"):
            lines.append("　🔈 %s" % enh["fullIpa"])
        if enh.get("pron"):
            lines.append("　%s" % _clip(enh["pron"], 150))
        lines.append("")
    lines.append("[👉 跟着原声跟读](%s/day%s.html)" % (_site(), date))
    return lines


def build_card(date=None, master=None, mode=None, hour=None):
    """组装 markdown 卡片文本。date 为 None 时取今天；mode 为 None 时按当前小时轮换。"""
    if date is None:
        date = datetime.date.today().isoformat()
    d = datetime.date.fromisoformat(date)

    m = master or _load(MASTER, {})
    if not m.get("sentences"):
        raise SystemExit("master.json 读取失败")

    used_date, ids = _resolve_day(date)
    by_id = {s["id"]: s for s in m["sentences"]}
    meta = m.get("meta") or {}
    start = datetime.date.fromisoformat(meta.get("startDate") or used_date)
    day_index = (datetime.date.fromisoformat(used_date) - start).days + 1

    if mode is None:
        mode = auto_mode(hour)
    mode = int(mode) % 4

    if mode == 1:
        lines = _mode_focus(ids, by_id, day_index, used_date, hour)
    elif mode == 2:
        lines = _mode_quiz(ids, by_id, day_index, used_date)
    elif mode == 3:
        lines = _mode_pron(ids, by_id, day_index, used_date)
    else:
        lines = _mode_overview(ids, by_id, day_index, used_date)

    # 当天页缺失、回退到旧日期时，明确告知，避免误以为推送错了
    if used_date != date:
        lines.append("")
        lines.append("（%s 的练习页还没生成，这里展示最近一期 %s 的内容）" % (date, used_date))

    days = _load(DAYS, [])
    practiced = len(set(days)) if isinstance(days, list) else 0
    introduced = sum(1 for s in m["sentences"] if s.get("learn", {}).get("introduced"))
    lines.append("")
    lines.append("> 累计已学 %d 句 ｜ 已练习 %d 天 ｜ 词库 %d 句 ｜ %s · %s" % (
        introduced, practiced, len(m["sentences"]),
        datetime.datetime.now().strftime("%H:%M"), MODE_NAME[mode]))
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


def in_window(hour=None):
    """提醒窗口：09:30 – 22:00（用整点 9–21 表示，22 点收工）。"""
    if hour is None:
        hour = datetime.datetime.now().hour
    return hour in PUSH_HOURS


def push(date=None, content=None, dry=False, mode=None, window_only=False):
    if window_only and not in_window():
        return {"ok": True, "skipped": True, "reason": "outside_window",
                "hour": datetime.datetime.now().hour, "window": "09:30-22:00"}
    date = date or datetime.date.today().isoformat()
    card = content or build_card(date, mode=mode)
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
    mode = None
    rest = []
    i = 1
    while i < len(argv):
        a = argv[i]
        if a == "--mode" and i + 1 < len(argv):
            mode = int(argv[i + 1])
            i += 2
            continue
        if a.startswith("--mode="):
            mode = int(a.split("=", 1)[1])
            i += 1
            continue
        if not a.startswith("--"):
            rest.append(a)
        i += 1
    date = rest[0] if rest else None
    res = push(date=date, dry=dry, mode=mode, window_only=("--window" in argv))
    if dry:
        print(res.get("content", ""))
        return 0
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0 if res.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
