# -*- coding: utf-8 -*-
"""预生成未来 N 天练习页（用于「提前预习」）。

设计要点：
- 不修改 master.json 的 introduced / mastery（进度仍由每日自动化 run_daily.py 在真实日期接管）。
- 仅生成静态 day<date>.html + day<date>.json 侧车，便于日历提前展示、用户提前学习。
- 日练习页模板直接从 run_daily.py 提取（run_daily 是每日自动化的权威模板，提取可自动与之保持一致）。
- 选句逻辑与未来自动化行为一致：从「首个未引入句」起按 id 顺序每 5 句一批（dayIndex<=introDays 时为新句日；
  超出总句数或 dayIndex>introDays 时为复习日，取当前掌握度最低的 5 句作为预览）。

用法：
  python gen_future.py                 # 默认：起始=明天，天数=22
  python gen_future.py 2026-08-21 22   # 指定起始日期与天数
"""
import json
import os
import re
import sys
import datetime
import glob

BASE = os.path.dirname(os.path.abspath(__file__))
MASTER = os.path.join(BASE, "master.json")
DAYS = os.path.join(BASE, "days.json")

with open(MASTER, encoding="utf-8") as f:
    data = json.load(f)
meta = data["meta"]
S = data["sentences"]
by_id = {s["id"]: s for s in S}

today = datetime.date.today()
start = datetime.date.fromisoformat(meta["startDate"])
dailyCount = int(meta["dailyCount"])
introDays = int(meta["introDays"])
total = len(S)
introduced = sum(1 for s in S if s["learn"]["introduced"])
first_un = next(s["id"] for s in S if not s["learn"]["introduced"])
total_str = str(total)

# ---- 参数 ----
begin = (today + datetime.timedelta(days=1)) if len(sys.argv) < 2 else datetime.date.fromisoformat(sys.argv[1])
n_days = 22 if len(sys.argv) < 3 else int(sys.argv[2])

# ---- 提取权威模板（run_daily.py 的 PAGE 字符串）----
src = open(os.path.join(BASE, "run_daily.py"), encoding="utf-8").read()
mm = re.search(r'PAGE = """(.*?)"""', src, re.S)
if not mm:
    raise RuntimeError("无法从 run_daily.py 提取 PAGE 模板")
PAGE_TMPL = mm.group(1)
assert PAGE_TMPL.lstrip().startswith("<!DOCTYPE html>")
assert PAGE_TMPL.rstrip().endswith("</html>")
# 注入「预习横幅」占位 + 样式（仅 gen_future 预生成页使用；真实自动化页不含此横幅）
PAGE_TMPL = PAGE_TMPL.replace("</header>", "</header>\n  __PREVIEW_BANNER__", 1)
PAGE_TMPL = PAGE_TMPL.replace(
    "</style>",
    ".preview-banner{background:#fff7ed;border:1px solid #fed7aa;color:#b45309;"
    "border-radius:10px;padding:9px 12px;font-size:13px;margin:10px 0 4px;text-align:center;line-height:1.5}\n</style>",
    1,
)


def build_data_list(selected):
    out = []
    for s in selected:
        enh = s["learn"]["enh"]
        out.append({
            "id": "s%d" % s["id"], "nid": s["id"],
            "type": "long" if s["length"] == "long" else "short",
            "topic": s["theme"], "en": s["en"], "ipa": enh.get("fullIpa", ""),
            "zh": s["zh"],
            "kw": [[k["term"], k["ipa"], "%s%s" % (k.get("pos", ""), k.get("zh", ""))] for k in s["keyvocab"]],
            "variants": enh.get("variants", []) or [],
            "scenes": enh.get("scenes", []) or [],
            "grammar": enh.get("grammar", ""),
            "pron": enh.get("pron", ""),
            "mastery": s["learn"].get("mastery", 0) or 0,
        })
    return out


def select_for(D):
    """返回该日期应展示的句子与元信息，逻辑与未来自动化一致。"""
    k = (D - today).days  # >=1
    dayIndex = (D - start).days + 1
    base = first_un
    start_id = base + dailyCount * (k - 1)
    block = [start_id + i for i in range(dailyCount)]
    if dayIndex <= introDays and start_id + dailyCount - 1 <= total:
        selected = [by_id[i] for i in block if i in by_id]
        mode = "new"
        proj_total = introduced + dailyCount * k
        intro_n = len(selected)
    else:
        # 复习预览：按 id 顺序轮转取 5 句，使不同未来日展示不同句式（真实自动化当日会用掌握度重选并覆盖）
        all_ids = sorted(by_id.keys())
        off = (dayIndex * dailyCount) % total
        selected = [by_id[all_ids[(off + j) % total]] for j in range(dailyCount)]
        mode = "review"
        proj_total = total
        intro_n = 0
    return selected, mode, dayIndex, proj_total, intro_n


# ---- 预生成未来页 ----
generated = []
for i in range(n_days):
    D = begin + datetime.timedelta(days=i)
    selected, mode, dayIndex, proj_total, intro_n = select_for(D)
    if not selected:
        continue
    data_list = build_data_list(selected)
    DATA_JSON = json.dumps(data_list, ensure_ascii=False)
    is_future = D > today
    banner = ('<div class="preview-banner">🔓 预习模式 · 该日尚未到（%s），可提前学习；'
              '每日 9:00 自动推送后会与此页内容同步。</div>' % D.isoformat()) if is_future else ""
    html = (PAGE_TMPL
            .replace("__DAY__", str(dayIndex))
            .replace("__N__", str(dailyCount))
            .replace("__INTRO__", str(intro_n))
            .replace("__DATA_JSON__", DATA_JSON)
            .replace("__TOTAL__", str(proj_total))
            .replace("__POOL__", total_str)
            .replace("__PREVIEW_BANNER__", banner))
    with open(os.path.join(BASE, "day%s.html" % D.isoformat()), "w", encoding="utf-8") as f:
        f.write(html)
    dj = {"date": D.isoformat(), "ids": [s["id"] for s in selected], "preview": is_future}
    with open(os.path.join(BASE, "day%s.json" % D.isoformat()), "w", encoding="utf-8") as f:
        json.dump(dj, f, ensure_ascii=False, indent=2)
    generated.append((D.isoformat(), mode, [s["id"] for s in selected], proj_total))

# ---- 修复：已存在 day<date>.html 但缺侧车 / 未登记到 days.json 的真实练习日 ----
days_list = []
if os.path.exists(DAYS):
    try:
        days_list = json.load(open(DAYS, encoding="utf-8"))
    except Exception:
        days_list = []
days_set = set(days_list)
today_str = today.isoformat()
fixed = []
for p in sorted(glob.glob(os.path.join(BASE, "day????-??-??.html"))):
    d = os.path.basename(p)[3:-5]
    if os.path.exists(os.path.join(BASE, "day%s.json" % d)):
        continue
    txt = open(p, encoding="utf-8").read()
    ids = sorted(set(int(x) for x in re.findall(r'"id"\s*:\s*"s(\d+)"', txt)))
    if not ids:
        continue
    json.dump({"date": d, "ids": ids},
              open(os.path.join(BASE, "day%s.json" % d), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    if d <= today_str and d not in days_set:
        days_list.append(d)
        days_set.add(d)
        fixed.append(d)
if fixed:
    days_list = sorted(set(days_list))
    json.dump(days_list, open(DAYS, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

print("GEN_FUTURE: first_un=%d introduced=%d total=%d begin=%s n=%d"
      % (first_un, introduced, total, begin.isoformat(), n_days))
print("generated future pages: %d" % len(generated))
for g in generated:
    print("  %s mode=%s ids=%s proj_total=%d" % (g[0], g[1], g[2], g[3]))
if fixed:
    print("fixed missing sidecars / days.json: %s" % fixed)
