import sys, asyncio, edge_tts, os

# Usage: python gen_one.py <id> "<english text>"
sid = sys.argv[1]
text = sys.argv[2]
os.makedirs("audio", exist_ok=True)
out = f"audio/s{sid}.mp3"

async def main():
    communicate = edge_tts.Communicate(text, "en-US-AndrewNeural", rate="-10%")
    await communicate.save(out)

asyncio.run(main())
print("OK", out)
