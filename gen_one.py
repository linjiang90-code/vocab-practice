import sys, asyncio, edge_tts, os
import voice_config

# Usage: python gen_one.py <id> "<english text>"
sid = sys.argv[1]
text = sys.argv[2]
os.makedirs("audio", exist_ok=True)
out = f"audio/s{sid}.mp3"
tmp = out + ".tmp"

async def main():
    communicate = edge_tts.Communicate(text, voice_config.VOICE, **voice_config.kwargs())
    await communicate.save(tmp)
    os.replace(tmp, out)     # 原子替换，避免页面读到写了一半的文件

asyncio.run(main())
print("OK", out)
