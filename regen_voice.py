"""按 voice_config.py 的音色批量重录音频。

用法：
    venv 解释器 regen_voice.py            # 重录 1..(activeCount+50)，即当前激活区+下一批
    venv 解释器 regen_voice.py 1 250      # 指定 id 区间
    venv 解释器 regen_voice.py --missing  # 只补缺失文件，不覆盖已有

并发 3 + 失败重试 3 次；edge-tts 音色与语速全部取自 voice_config.py。
"""
import asyncio
import json
import os
import sys

import edge_tts
import voice_config

BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE)
AUDIO = "audio"
CONCURRENCY = 3
RETRIES = 3


def load_sentences():
    with open("master.json", encoding="utf-8") as f:
        m = json.load(f)
    return m, {s["id"]: s.get("en", "") for s in m["sentences"]}


async def synth(sid, text, sem, stats):
    out = os.path.join(AUDIO, "s%d.mp3" % sid)
    tmp = out + ".tmp"
    async with sem:
        for attempt in range(1, RETRIES + 1):
            try:
                await edge_tts.Communicate(text, voice_config.VOICE, **voice_config.kwargs()).save(tmp)
                size = os.path.getsize(tmp)
                if size < 2000:
                    raise RuntimeError("文件过小(%d B)" % size)
                os.replace(tmp, out)          # 原子替换：播放中的请求不会读到半个文件
                stats["ok"] += 1
                print("[%3d] OK   %5d B  %s" % (sid, size, text[:40]))
                return
            except Exception as e:
                if attempt == RETRIES:
                    stats["fail"] += 1
                    stats["errors"].append((sid, repr(e)[:120]))
                    print("[%3d] FAIL %s" % (sid, repr(e)[:100]))
                    if os.path.exists(tmp):
                        os.remove(tmp)
                else:
                    await asyncio.sleep(1.5 * attempt)


async def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    only_missing = "--missing" in sys.argv

    m, texts = load_sentences()
    meta = m.get("meta", {})
    default_hi = int(meta.get("activeCount", 200)) + int(meta.get("expandCount", 50))
    lo = int(args[0]) if len(args) > 0 else 1
    hi = int(args[1]) if len(args) > 1 else default_hi

    ids = [i for i in sorted(texts) if lo <= i <= hi and texts[i].strip()]
    if only_missing:
        ids = [i for i in ids if not os.path.exists(os.path.join(AUDIO, "s%d.mp3" % i))]

    os.makedirs(AUDIO, exist_ok=True)
    print("VOICE=%s RATE=%s  ids %d..%d  共 %d 条" % (voice_config.VOICE, voice_config.RATE, lo, hi, len(ids)))

    sem = asyncio.Semaphore(CONCURRENCY)
    stats = {"ok": 0, "fail": 0, "errors": []}
    await asyncio.gather(*(synth(i, texts[i], sem, stats) for i in ids))

    print("\nDONE ok=%d fail=%d" % (stats["ok"], stats["fail"]))
    for sid, err in stats["errors"][:10]:
        print("  s%d: %s" % (sid, err))


asyncio.run(main())

# 换音色/换语速后的自动化收尾（2026-11-12）：必须同步「① serve.py 的 BUILD
# ② 所有页面的 audio-engine.js?v= ③ 磁盘 audio/b<版本>/ 目录」，否则企业微信
# 内置浏览器（X5/CEF）按路径缓存 mp3，你录了新声用户仍听到旧声。详见 bump_build.py
if "--no-bump" not in sys.argv:
    try:
        import subprocess as _sp
        _sp.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "bump_build.py")],
                check=False)
    except Exception as _e:
        print("bump_build 未执行（请手动跑一次 bump_build.py）：%r" % (_e,))
