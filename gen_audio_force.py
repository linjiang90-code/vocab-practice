import json, os, asyncio, edge_tts

VOICE = "en-US-AndrewNeural"
RATE = "-10%"   # 略放慢，便于跟读
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("master.json", "r", encoding="utf-8") as f:
    data = json.load(f)
os.makedirs("audio", exist_ok=True)

async def gen_one(sid, text):
    for attempt in range(1, 4):
        try:
            comm = edge_tts.Communicate(text, VOICE, rate=RATE)
            await comm.save(f"audio/s{sid}.mp3")
            return True
        except Exception as e:
            print(f"  retry {attempt} for s{sid}: {e}")
            await asyncio.sleep(1.5)
    return False

async def main():
    total = len(data["sentences"])
    n_ok = 0
    n_fail = 0
    for s in data["sentences"]:
        sid = s["id"]
        text = s.get("en", "")
        if not text:
            print(f"skip s{sid} (no en)")
            continue
        ok = await gen_one(sid, text)
        if ok:
            n_ok += 1
        else:
            n_fail += 1
        print(f"[{sid:>3}] {'OK' if ok else 'FAIL'}  ({n_ok}/{n_ok + n_fail})  {text[:42]}")
    print(f"DONE ok={n_ok} fail={n_fail} total={total}")

asyncio.run(main())
