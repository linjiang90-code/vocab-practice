# -*- coding: utf-8 -*-
"""换音色/换语速后的「三处同步」一键完成（2026-11-12）。

背景（血泪教训）：
    企业微信内置浏览器（X5/CEF）的媒体缓存按 URL 路径建键，无视 no-store，
    换音色后仍反复播放旧声。为此音频 URL 变成 audio/b<版本>/sNNN.mp3，
    需要三处同时对齐，漏一处就会退回旧声或 404：
        ① serve.py 的 BUILD（HTML 302 目标 + 正常日志）
        ② 所有页面/模板的 audio-engine.js?v=<版本>
        ③ 磁盘上的 audio/b<版本>/ 目录（硬链接，真实存在）

用法：
    python bump_build.py           # 版本自增并完成三处同步
    python bump_build.py --dry     # 只打印将要做什么
regen_voice.py 重录结束后会自动调用本脚本。
"""
import glob
import io
import os
import re
import subprocess
import sys
import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
SERVE = os.path.join(BASE, "serve.py")


def next_build(cur, today):
    """BUILD 形如 20261112b：同日则末位字母 +1，跨日则重开为 a。"""
    m = re.fullmatch(r"(\d{8})([a-z])", cur or "")
    if not m:
        return today + "a"
    day, ch = m.group(1), m.group(2)
    if day != today:
        return today + "a"
    return day + ("a" if ch == "z" else chr(ord(ch) + 1))


def main():
    dry = "--dry" in sys.argv
    today = datetime.date.today().strftime("%Y%m%d")

    s = io.open(SERVE, encoding="utf-8").read()
    m = re.search(r'^BUILD\s*=\s*"([0-9A-Za-z]+)"', s, re.M)
    if not m:
        raise SystemExit("serve.py 里找不到 BUILD")
    old = m.group(1)
    new = next_build(old, today)
    print("BUILD: %s -> %s" % (old, new))

    # ① serve.py
    if not dry:
        s2 = re.sub(r'^(BUILD\s*=\s*")[0-9A-Za-z]+(")', r"\g<1>" + new + r"\g<2>", s, count=1, flags=re.M)
        io.open(SERVE, "w", encoding="utf-8", newline="").write(s2)

    # ② 页面 + 生成器模板的引擎引用
    pat = re.compile(r"audio-engine\.js\?v=[0-9A-Za-z]+")
    changed = 0
    for f in glob.glob(os.path.join(BASE, "*.html")) + glob.glob(os.path.join(BASE, "*.py")):
        try:
            t = io.open(f, encoding="utf-8").read()
        except Exception:
            continue
        if not pat.search(t):
            continue
        changed += 1
        if not dry:
            io.open(f, "w", encoding="utf-8", newline="").write(
                pat.sub("audio-engine.js?v=" + new, t))
    print("引擎引用已更新：%d 个文件 -> ?v=%s" % (changed, new))

    # ③ 磁盘版本目录（硬链接，不额外占空间）
    if dry:
        print("[dry] 跳过 sync_audio_version.py")
    else:
        r = subprocess.run([sys.executable, os.path.join(BASE, "sync_audio_version.py"), new],
                           capture_output=True, text=True)
        print((r.stdout or r.stderr or "").strip())

    print("完成。注意：serve.py 的 BUILD 需**重启 vocab-serve** 才对 302 生效；")
    print("      但页面引用与音频目录已即时生效，浏览器重新打开页面即可听到新音色。")


if __name__ == "__main__":
    main()
