# -*- coding: utf-8 -*-
"""音频版本目录同步：为当前 BUILD 生成一个真实存在的 audio/b<BUILD>/ 目录。

为什么需要它（2026-11-12）：
    企业微信内置浏览器（X5/CEF）的媒体缓存按 URL「路径」建键，会无视
    Cache-Control: no-store，也不认 ?v= query。换音色（男声 -> Ava 女声）后，
    内嵌浏览器里仍反复放旧声，外部浏览器却正常。
    前端引擎把版本段写进路径 audio/b<BUILD>/s123.mp3 —— 路径与旧版完全不同，
    任何缓存实现都无法命中。
    但这个新路径要在磁盘上真实存在（否则需要服务端路由，而服务端可能要重启才生效）。
    本脚本用**硬链接**生成同名目录：不额外占磁盘、与 audio/*.mp3 指向同一份数据。

用法：
    python sync_audio_version.py            # 版本号取自 serve.py 的 BUILD
    python sync_audio_version.py 20261112b  # 显式指定
换音色 / 换语速后：先 bump serve.py 的 BUILD 与页面上的 audio-engine.js?v=20261112c，
再跑本脚本（regen_voice.py 也会自动调用）。
"""
import os
import re
import sys
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.join(BASE, "audio")


def current_build():
    with open(os.path.join(BASE, "serve.py"), encoding="utf-8") as f:
        m = re.search(r'^BUILD\s*=\s*"([0-9A-Za-z]+)"', f.read(), re.M)
    if not m:
        raise SystemExit("serve.py 里找不到 BUILD")
    return m.group(1)


def main():
    ver = (sys.argv[1] if len(sys.argv) > 1 else current_build()).strip()
    if not re.fullmatch(r"[0-9A-Za-z]+", ver):
        raise SystemExit("版本号只允许字母数字：%r" % ver)
    dst = os.path.join(AUDIO, "b" + ver)
    srcs = sorted(n for n in os.listdir(AUDIO)
                  if n.endswith(".mp3") and os.path.isfile(os.path.join(AUDIO, n)))
    if not srcs:
        raise SystemExit("audio/ 下没有 mp3")
    os.makedirs(dst, exist_ok=True)

    linked = copied = skipped = 0
    for n in srcs:
        s = os.path.join(AUDIO, n)
        d = os.path.join(dst, n)
        # 目标已存在且大小一致：视为已同步（硬链接无法跨卷，故比较大小作兜底判断）
        if os.path.exists(d) and os.path.getsize(d) == os.path.getsize(s):
            skipped += 1
            continue
        if os.path.exists(d):
            os.remove(d)
        try:
            os.link(s, d)          # 硬链接：同一份数据，不额外占空间
            linked += 1
        except OSError:
            shutil.copy2(s, d)     # 跨卷/不支持硬链接时退化为复制
            copied += 1

    print("audio/b%s/ 同步完成：新增硬链 %d，复制 %d，早已同步 %d，总计 %d"
          % (ver, linked, copied, skipped, len(srcs)))
    # 目录里多余的文件（被删掉的句子）顺手清理，避免长期堆积
    extra = [n for n in os.listdir(dst) if n.endswith(".mp3") and n not in srcs]
    for n in extra:
        os.remove(os.path.join(dst, n))
    if extra:
        print("清理多余 %d 个：%s" % (len(extra), ", ".join(extra[:5])))


if __name__ == "__main__":
    main()
