import json, os, subprocess, sys

VENV = r"C:/Users/Win10/.workbuddy/binaries/python/envs/default/Scripts/python.exe"
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("master.json", "r", encoding="utf-8") as f:
    data = json.load(f)

os.makedirs("audio", exist_ok=True)
missing = [s for s in data["sentences"] if not os.path.exists(s["audio"])]
print(f"TOTAL={len(data['sentences'])} MISSING_AUDIO={len(missing)}")

for s in missing:
    print(f"[{s['id']:>3}] gen: {s['en']}")
    subprocess.run([VENV, "gen_one.py", str(s["id"]), s["en"]], check=True)

print("AUDIO_GEN_DONE", len(missing))
