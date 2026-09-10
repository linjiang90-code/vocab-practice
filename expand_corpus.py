# -*- coding: utf-8 -*-
"""一次性迁移：把 9 个语料池的 900 句合并进 master.json（ids 101-1000）。
- 新句 introduced=False，进入 master.html 总览但不在每日轮换里
- 每日语料池由 meta.activeCount 控制：每 30 天 +50（run_daily 自动扩展）
- 可重复运行（幂等）：已存在的 id 会跳过，meta 只在首次设置 activeCount
用法：python expand_corpus.py
"""
import json, os, re, importlib

BASE = os.path.dirname(os.path.abspath(__file__))
MASTER = os.path.join(BASE, "master.json")

with open(MASTER, encoding="utf-8") as f:
    data = json.load(f)
S = data["sentences"]
meta = data["meta"]

existing_ids = {s["id"] for s in S}
existing_en = {s["en"].strip().lower().rstrip(".!?") for s in S}
POS = re.compile(r"^(n|v|adj|adv|phr|prep|pron|int|num|conj|det|aux|modal)\.\s*(.+)$")

new_records = []
skipped = 0
for i in range(1, 10):
    for ln in importlib.import_module("sentences_pool_%d" % i).RAW:
        en, zh, theme, cat, length, kw, kwipa, kwposzh = [x.strip() for x in ln.split("|")]
        key = en.lower().rstrip(".!?")
        if key in existing_en:
            skipped += 1
            continue
        m = POS.match(kwposzh)
        if not m:
            raise SystemExit("bad pos format: %r" % kwposzh)
        pos, zh_gloss = m.group(1) + ".", m.group(2)
        nid = max(existing_ids) + 1
        existing_ids.add(nid)
        existing_en.add(key)
        new_records.append({
            "id": nid, "en": en, "zh": zh, "theme": theme, "category": cat,
            "length": length if length in ("short", "long") else "short",
            "keyvocab": [{"term": kw, "ipa": kwipa, "pos": pos, "zh": zh_gloss}],
            "audio": meta["audioPattern"].format(id=nid),
            "learn": {"introduced": False, "introducedDay": None, "mastery": 0,
                      "reviewCount": 0, "lastReviewed": None, "dueDate": None,
                      "enh": {"fullIpa": "", "variants": [], "scenes": [], "grammar": "", "pron": ""}},
        })

S.extend(new_records)

# meta：活跃句库从当前 100 起，每 30 天 +50，直到 1000
if "activeCount" not in meta:
    meta["activeCount"] = 100
meta["totalTarget"] = 1000
meta["cumulativeTargetNote"] = "100 -> (每30天+50) -> 150 -> 200 -> ... -> 1000；每日 5 句随机推送"

with open(MASTER, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

intro = sum(1 for s in S if s["learn"]["introduced"])
print("MERGE DONE: total=%d added=%d skipped_dup=%d introduced=%d active=%d nextExpDay=%s"
      % (len(S), len(new_records), skipped, intro, meta["activeCount"], meta["nextExpansionDay"]))
