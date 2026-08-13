import asyncio, edge_tts, os

OUT = os.path.join(os.path.dirname(__file__), "audio")
os.makedirs(OUT, exist_ok=True)

VOICE = "en-US-AriaNeural"
RATE = "-10%"   # 略放慢，便于跟读

SENTENCES = [
    ("s1",  "Where is the nearest subway station?"),
    ("s2",  "Could you say that again, please?"),
    ("s3",  "I'd like to book a table for two."),
    ("s4",  "It's nice to meet you."),
    ("s5",  "How much does this cost?"),
    ("s6",  "What do you usually do on weekends?"),
    ("s7",  "Is breakfast included in the price?"),
    ("s8",  "Could you recommend a good local restaurant that's not too expensive and within walking distance?"),
    ("s9",  "I was wondering if you'd like to grab a coffee with me sometime this week."),
    ("s10", "I seem to have lost my way — could you tell me how to get to the city center from here?"),
]

async def amain():
    for sid, text in SENTENCES:
        comm = edge_tts.Communicate(text, VOICE, rate=RATE)
        path = os.path.join(OUT, f"{sid}.mp3")
        await comm.save(path)
        print("saved", path)

asyncio.run(amain())
print("ALL_DONE")
