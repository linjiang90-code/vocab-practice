# -*- coding: utf-8 -*-
"""把 enh_batch_101_125.py / enh_batch_126_150.py 的详细标注合并进 master.json learn.enh。
幂等：仅当该句 enh.fullIpa 为空时写入，已有标注不覆盖。"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import enh_batch_101_125, enh_batch_126_150

BASE = os.path.dirname(os.path.abspath(__file__))
MASTER = os.path.join(BASE, "master.json")

with open(MASTER, encoding="utf-8") as f:
    data = json.load(f)
S = {s["id"]: s for s in data["sentences"]}

filled = skipped = missing = 0
for mod in (enh_batch_101_125, enh_batch_126_150):
    for sid, enh in mod.ENH.items():
        if sid not in S:
            print("MISSING id", sid); missing += 1; continue
        cur = S[sid]["learn"]["enh"]
        if cur.get("fullIpa"):
            skipped += 1; continue
        # 结构校验
        assert enh.get("fullIpa") and isinstance(enh.get("variants"), list) \
            and isinstance(enh.get("scenes"), list) and enh.get("grammar") and enh.get("pron"), sid
        cur.update(enh)
        filled += 1

with open(MASTER, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

total_enh = sum(1 for s in data["sentences"] if s["learn"]["enh"].get("fullIpa"))
print("ENH MERGE: filled=%d skipped=%d missing=%d total_enh=%d/1000"
      % (filled, skipped, missing, total_enh))
