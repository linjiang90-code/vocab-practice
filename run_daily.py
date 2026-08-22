# -*- coding: utf-8 -*-
"""每日英语口语推送 驱动脚本（词力词汇教练）。
用法：python run_daily.py
自动：计算 dayIndex -> 阶段扩展(每30天) -> 选句(5) -> 注入增强内容 -> 生成音频 -> 生成当日页 -> 更新 learn -> 重生成 master.html
"""
import json, os, sys, subprocess, datetime, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
MASTER = os.path.join(BASE, "master.json")
VENV_PY = r"C:\Users\Win10\.workbuddy\binaries\python\envs\default\Scripts\python.exe"

# ============ 本日增强内容覆盖（由词汇教练手工撰写，注入 learn.enh）============
# 仅在选中句 enh 为空时写入。结构：fullIpa / variants / scenes / grammar / pron
ENH = {
    6: {
        "fullIpa": "/wʌt du ju ˈjuːʒuəli du ɑːn ˈwiːkendz/",
        "variants": [
            ["What do you do on weekends?", "省掉 usually，依然自然"],
            ["Any plans for the weekend?", "更偏闲聊，直接问有没有安排"],
            ["How do you usually spend your weekends?", "稍正式，spend 表『度过』"],
        ],
        "scenes": [
            ["破冰闲聊", "What do you usually do on weekends?", "对方答 I usually… / Not much.(没啥特别的)"],
            ["约人出去", "Do you wanna hang out this weekend?", "wanna = want to，问要不要一起玩"],
            ["不同回答", "I just chill at home. / I go hiking. / Work, unfortunately.", "宅家 / 去徒步 / 无奈要加班"],
        ],
        "grammar": "一般现在时表习惯性动作；usually 放在主语和实义动词之间（do you usually do）。weekend 英式常用 at weekends，美式用 on weekends。",
        "pron": "同化：do you→/dʒu/（d+j 同化为 dʒ，关键！）。连读：What do→/wʌ dʊ/（t 与 d 连读）；do on→/dʊ wɑn/（元音间加 w 滑音）；on weekends→/ɑːn ˈwiːkendz/（n 与 w 连读）。浊化：What do 快读 /wʌ dʊ/（t→d，极典型）；usually do 顺接 /ˈjuːʒuəli dʊ/。弱读：you 弱读 /jə/（亦可保留 /ju/）；do 作助动词弱读 /də/；on→/ən/。缩读：场景里 wanna = want to（口语缩读）。失去爆破/闪音：本句无典型（参考：better→/bɛɾɚ/、city→/sɪɾi/ 元音间 /t/ 标闪音；good boy→/ɡʊ bɔɪ/ 相邻爆破音标失去爆破）。",
    },
    7: {
        "fullIpa": "/ɪz ˈbrekfəst ɪnˈkluːdɪd ɪn ðə praɪs/",
        "variants": [
            ["Does the price include breakfast?", "更顺口，主动语态"],
            ["Is breakfast free?", "最简，但 free 不如 included 准确表达『含在房费里』"],
        ],
        "scenes": [
            ["订酒店问含早", "Is breakfast included?", "对方回 Yes, it's a buffet. / No, it's extra.(另收费) / Continental breakfast only.(仅欧式简早)"],
            ["顺带问是否含税/服务费", "Does it include tax and service?", "延展问法"],
            ["顺带问 wifi", "Is Wi-Fi included?", "一并确认网络"],
        ],
        "grammar": "be included in + 名词 是被动结构，表『被包含在…里』；price 单数用 is。included /ɪnˈkluːdɪd/ 是 include 的过去分词作形容词。",
        "pron": "连读：Is breakfast→/ɪz ˈbrekfəst/（z 与 b 连读）；breakfast included→/ˈbrekfəst ɪnˈkluːdɪd/（t 与 ɪ 连读）；included in→/ɪnˈkluːdɪd ɪn/（d 与 ɪ）；in the→/ɪn ðə/（n 与 ð）。失去爆破：breakfast 词尾 /t/ 在 /ɪ/ 前为不完全爆破 /ˈbrekfəs(t) ɪn/；included 词尾 /d/ 在 /ɪn/ 前 /ɪnˈkluːdɪ(d) ɪn/。浊化：breakfast 词尾 t 在 ɪ 前快读可浊化为 d：/ˈbrekfəsd ɪn/。弱读：the→/ðə/；in→/ɪn/。同化/滑音/缩读：无典型。",
    },
    8: {
        "fullIpa": "/kʊd ju ˌrekəˈmend ə ɡʊd ˈloʊkəl ˈrestərənt ðæts nɑːt tuː ɪkˈspensɪv ənd ˈwɪðɪn ˈwɔːkɪŋ ˈdɪstəns/",
        "variants": [
            ["Any good local spots around here?", "spots = 地点，极口语"],
            ["Where do locals eat?", "问本地人去哪吃，更地道"],
            ["Do you know a place that won't break the bank?", "break the bank 俚语『花太多钱』"],
        ],
        "scenes": [
            ["问酒店前台", "Can you recommend a good restaurant nearby?", "对方直接给名字"],
            ["问路人", "Where's a nice place to eat around here?", "对方指路"],
            ["不同回答", "Try the place on 5th St. / It's a bit touristy.(偏游客) / Book ahead, it's popular.(要预定)", ],
        ],
        "grammar": "recommend 后接名词或动名词：recommend a restaurant / recommend going there。within walking distance 是固定搭配『步行范围内』；that's = that is 引导定语从句修饰 restaurant。",
        "pron": "同化：Could you→/kʊdʒu/（d+j 同化为 dʒ，关键！）；that's not→/ðæts nɑt/（s 与 n 相邻）。连读：good local→/ɡʊ wˈloʊkəl/（d 后加 w 滑音）；not too→/nɑ tʊ/（两个 t 只读一次，后接元音）；too expensive 顺接 /tuː ɪkˈspensɪv/；and within→/ənd ˈwɪðɪn/（d 与 w）。浊化：not too 快读 /nɑ dʊ/（t→d）。失去爆破：good local /ɡʊ(d) ˈloʊkəl/（d 在 l 前不完全爆破）。弱读：a→/ə/；and→/ən/；that's→/ðæts/。缩读：that's = that is（口语缩读）。闪音：无典型。",
    },
    9: {
        "fullIpa": "/aɪ wʌz ˈwʌndərɪŋ ɪf juːd laɪk tə ɡræb ə ˈkɔːfi wɪð miː ˈsʌmtaɪm ðɪs wiːk/",
        "variants": [
            ["Want to get a coffee sometime?", "最口语，直接用 want"],
            ["Let's grab a coffee.", "已默认能成，更熟"],
            ["How about a coffee later?", "更轻的提议"],
        ],
        "scenes": [
            ["委婉邀约(不太熟)", "I was wondering if you'd like to…", "最礼貌，给对方余地"],
            ["熟人间", "Wanna grab a drink?", "drink 可含咖啡/酒，看语境"],
            ["不同回答", "Sure, Tuesday works. / I'd love to but I'm swamped.(想去但忙) / Rain check?(改天呗)"],
        ],
        "grammar": "I was wondering if… 用过去进行时表委婉，比 Do you want 客气得多，是邀约神句。would like to = 想（礼貌）；grab 本义抓，口语常指『快速喝/吃一杯』。",
        "pron": "连读：was wondering→/wʌz ˈwʌndərɪŋ/（z 与 w）；grab a→/ɡræb ə/（b 与 a）；coffee with→/ˈkɔfi wɪð/（i 与 w 滑音）；sometime this→/ˈsʌmtaɪm ðɪs/（m 与 ð）。浊化：like to→/laɪ də/（t→d，同 wanna 规律）；grab a 中 b 保持浊。弱读：to→/tə/；a→/ə/；me→/mi/(可弱读 /mə/)；if→/ɪf/。缩读：you'd = you would（口语缩读）；场景中 wanna = want to。失去爆破：grab a /ɡræ(b) ə/（b 在 a 前轻微不完全爆破）。闪音：无典型。",
    },
    10: {
        "fullIpa": "/aɪ siːm tə hæv lɔst maɪ weɪ kʊd ju tel miː haʊ tə ɡet tə ðə ˈsɪti ˈsentər frəm hɪr/",
        "variants": [
            ["I'm lost.", "最简，最常用"],
            ["I think I'm lost.", "更柔和"],
            ["Can you help me find my way?", "直接请帮忙指路"],
        ],
        "scenes": [
            ["问路人", "Excuse me, I seem to have lost my way.", "对方指路或 Follow me.(跟我来)"],
            ["用手机", "Can you help me find this on Maps?", "请对方帮忙查地图"],
            ["不同回答", "Go back to the main road. / I'll walk you there. / You're going the wrong way.(你走反了)"],
        ],
        "grammar": "I seem to have + 过去分词 表『我好像（已经）…了』，比 I'm lost 委婉。lost my way 固定搭配『迷路』；city center（英）/ downtown（美）都表市中心。",
        "pron": "同化：Could you→/kʊdʒu/（d+j 同化为 dʒ，关键！）。连读：seem to→/siːm p tə/（m 后加 p 滑音）；lost my→/lɔs maɪ/（t 与 m 连读）；my way→/maɪ weɪ/（aɪ 与 w 滑音）；from here→/frəm hɪr/（m 与 h）；tell me→/tɛl mi/（l 与 m）。浊化：lost my 快读 /lɔz maɪ/ 或 /lɔd maɪ/（t→d，典型）；have 的 v 保持浊。失去爆破：lost my /lɔ(s)t maɪ/（s-t，/t/ 在 m 前不完全爆破）；get to /ɡe(t) tə/；center /ˈsɛn(t)ər/（t 在 ər 前不完全爆破）。闪音：city→/ˈsɪɾi/（美式，元音间 /t/ 标闪音 /ɾ/，关键！）。弱读：to→/tə/；the→/ðə/。缩读：无典型。",
    },
}

# 阶段扩展用的新句（仅在 dayIndex == nextExpansionDay 且未覆盖时提供；今日不触发，留作模板）
NEW_SENTENCES = []

# ============ 逻辑 ============
with open(MASTER, encoding="utf-8") as f:
    data = json.load(f)
meta = data["meta"]
S = data["sentences"]
by_id = {s["id"]: s for s in S}

today = datetime.date.today()
start = datetime.date.fromisoformat(meta["startDate"])
dayIndex = (today - start).days + 1
today_str = today.isoformat()

expanded = 0
# 阶段扩展
if dayIndex == meta.get("nextExpansionDay") and dayIndex not in (meta.get("_expanded_days") or []):
    if NEW_SENTENCES:
        max_id = max(s["id"] for s in S)
        existing_en = {s["en"].strip().lower() for s in S}
        new_ids = []
        for i, ns in enumerate(NEW_SENTENCES):
            nid = max_id + 1 + i
            if ns["en"].strip().lower() in existing_en:
                continue
            rec = {
                "id": nid,
                "en": ns["en"], "zh": ns["zh"], "theme": ns["theme"],
                "category": ns["category"], "length": ns["length"],
                "keyvocab": ns["keyvocab"],
                "audio": meta["audioPattern"].format(id=nid),
                "learn": {"introduced": False, "introducedDay": None, "mastery": 0,
                          "reviewCount": 0, "lastReviewed": None, "dueDate": None,
                          "enh": {"fullIpa": "", "variants": [], "scenes": [], "grammar": "", "pron": ""}},
            }
            S.append(rec)
            by_id[nid] = rec
            new_ids.append(nid)
        expanded = len(new_ids)
        meta["expansionsDone"] = meta.get("expansionsDone", 0) + 1
        meta["nextExpansionDay"] = meta["nextExpansionDay"] + meta.get("expandIntervalDays", 30)
        ed = meta.get("_expanded_days") or []
        ed.append(dayIndex)
        meta["_expanded_days"] = ed

# 选句
dailyCount = int(meta["dailyCount"])
introDays = int(meta["introDays"])
if dayIndex <= introDays:
    pool = [s for s in S if not s["learn"]["introduced"]]
    pool.sort(key=lambda s: s["id"])
    selected = pool[:dailyCount]
    mode = "new"
else:
    pool = [s for s in S if s["learn"]["introduced"]]
    pool.sort(key=lambda s: (s["learn"]["mastery"], -(int(s["learn"]["reviewCount"] or 0))))
    selected = pool[:dailyCount]
    mode = "review"

selected_ids = [s["id"] for s in selected]

# 注入增强内容 + 生成音频
for s in selected:
    enh = s["learn"]["enh"]
    if not enh.get("fullIpa") and s["id"] in ENH:
        enh.update(ENH[s["id"]])
    # 音频
    apath = os.path.join(BASE, s["audio"])
    if not os.path.exists(apath):
        try:
            subprocess.run([VENV_PY, "gen_one.py", str(s["id"]), s["en"]],
                           cwd=BASE, check=True, capture_output=True, text=True)
        except Exception as e:
            print("AUDIO_FAIL", s["id"], e)

# 更新 learn
for s in selected:
    L = s["learn"]
    if not L["introduced"]:
        L["introduced"] = True
        L["introducedDay"] = dayIndex
    L["lastReviewed"] = today_str
    L["reviewCount"] = (L["reviewCount"] or 0) + 1
    L["mastery"] = min(5, (int(L["mastery"] or 0)) + 1)

# 写回 master.json
with open(MASTER, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# ============ 生成当日练习页 ============
# 预计算汇总数据（模板需要）
total = len(S)
learned = sum(1 for s in S if s["learn"]["introduced"])

def esc(x):
    return str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

data_list = []
for s in selected:
    enh = s["learn"]["enh"]
    data_list.append({
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
DATA_JSON = json.dumps(data_list, ensure_ascii=False)

shorts = [d for d in data_list if d["type"] == "short"]
longs = [d for d in data_list if d["type"] == "long"]

PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>英语口语 Day __DAY__ · 增强版</title>
<style>
  :root{
    --bg:#f5f7fa; --card:#ffffff; --text:#1f2329; --sub:#6b7280;
    --line:#e5e7eb; --accent:#2f6fed; --accent2:#0e9f6e; --warn:#b45309; --pron:#0369a1;
    --travel:#eef4ff; --daily:#eafaf3; --chip:#fff4e5;
    --var:#f3f0ff; --scene:#eafaf3; --gram:#fff7ed; --pr:#eaf4ff;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:-apple-system,"PingFang SC","Microsoft YaHei",Segoe UI,Roboto,sans-serif;
    background:var(--bg);color:var(--text);line-height:1.65;padding:24px 16px 60px}
  .wrap{max-width:820px;margin:0 auto}
  header{text-align:center;margin-bottom:14px}
  header h1{font-size:22px;font-weight:700}
  header p{color:var(--sub);font-size:13.5px;margin-top:6px}
  .summary{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin:14px 0 4px}
  .summary .box{background:#fff;border:1px solid var(--line);border-radius:10px;padding:8px 14px;text-align:center;min-width:96px}
  .summary .box b{display:block;font-size:18px;color:var(--accent)}
  .summary .box span{font-size:12px;color:var(--sub)}
  .legend{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;font-size:12px;color:var(--sub);margin:14px 0 18px}
  .legend b{color:var(--text)}
  .toolbar{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin:0 0 22px}
  .btn{border:1px solid var(--line);background:#fff;color:var(--text);border-radius:999px;
    padding:7px 16px;font-size:14px;cursor:pointer;transition:.15s}
  .btn:hover{border-color:var(--accent);color:var(--accent)}
  .btn.primary{background:var(--accent);color:#fff;border-color:var(--accent)}
  .sec-title{font-size:15px;font-weight:700;color:var(--sub);margin:24px 4px 12px;display:flex;align-items:center;gap:8px}
  .sec-title .tag{background:var(--accent);color:#fff;font-size:12px;padding:2px 9px;border-radius:6px}
  .card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;margin-bottom:14px;box-shadow:0 1px 3px rgba(0,0,0,.04)}
  .card .top{display:flex;align-items:center;gap:10px;margin-bottom:8px}
  .num{width:26px;height:26px;border-radius:50%;background:var(--accent);color:#fff;font-size:13px;font-weight:700;display:flex;align-items:center;justify-content:center;flex:none}
  .pill{font-size:12px;padding:2px 10px;border-radius:999px;font-weight:600}
  .pill.travel{background:var(--travel);color:#2f6fed}
  .pill.daily{background:var(--daily);color:#0e9f6e}
  .play{margin-left:auto;display:flex;gap:6px}
  .ic{border:1px solid var(--line);background:#fff;border-radius:8px;width:34px;height:30px;cursor:pointer;font-size:15px;display:flex;align-items:center;justify-content:center}
  .ic:hover{border-color:var(--accent);background:#f0f6ff}
  .en{font-size:19px;font-weight:600;letter-spacing:.2px}
  .ipa{color:var(--sub);font-size:13px;margin:4px 0 6px;font-style:italic}
  .zh{font-size:15px;color:#374151}
  .block{margin-top:12px;border-radius:10px;padding:10px 12px;font-size:13.5px}
  .block .h{font-weight:700;font-size:13px;margin-bottom:6px;display:flex;align-items:center;gap:6px}
  .var{background:var(--var)} .scene{background:var(--scene)} .gram{background:var(--gram)} .pr{background:var(--pr)}
  .var .h{color:#6d28d9} .scene .h{color:#0e9f6e} .gram .h{color:var(--warn)} .pr .h{color:var(--pron)}
  .kw{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
  .kw .chip{background:var(--chip);border-radius:8px;padding:5px 10px;font-size:13px}
  .kw .chip b{color:#b45309} .kw .chip .p{color:#9a3412;font-style:italic;margin-left:4px}
  .block ul{margin:0;padding:left:18px} .block li{margin:3px 0}
  .block li .ex{font-weight:600} .block li .nt{color:#6b7280}
  .scene li .occ{color:#0e9f6e;font-weight:600} .scene li .resp{color:#6b7280}
  footer{text-align:center;color:var(--sub);font-size:12px;margin-top:24px}
  .assess{display:flex;align-items:center;gap:8px;margin-top:12px;flex-wrap:wrap;border-top:1px dashed var(--line);padding-top:10px}
  .assess .lbl{font-size:13px;color:var(--sub)}
  .assess button{border:1px solid var(--line);background:#fff;border-radius:8px;padding:5px 12px;font-size:13px;cursor:pointer}
  .assess button:hover{filter:brightness(.97)}
  .assess .c{color:#16a34a}.assess .f{color:#d97706}.assess .u{color:#dc2626}
  .astat{font-size:12px;color:var(--sub);margin-left:auto}
  .mbadge{font-size:12px;font-weight:600;padding:2px 8px;border-radius:6px;background:#f1f5f9;color:#475569}
  .spd{font-size:14px;color:var(--sub);display:flex;align-items:center;gap:6px}
  .spd select{padding:6px 8px;border:1px solid var(--line);border-radius:8px;background:#fff;font-size:13px;color:var(--text);cursor:pointer}
  .readwrap{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:12px 0 2px;font-size:13px;color:var(--sub)}
  .readwrap audio{width:100%;height:32px;margin-bottom:2px}
  .readwrap select{padding:5px 8px;border:1px solid var(--line);border-radius:8px;background:#fff;font-size:13px;color:var(--text);cursor:pointer}
  .readwrap .rlbl{font-weight:600;color:#475569}
  .readwrap .spdlbl{color:var(--sub)}
  .readBtn{border:1px solid var(--accent2);background:var(--accent2);color:#fff;border-radius:8px;padding:5px 14px;font-size:13px;cursor:pointer}
  .readBtn:hover{filter:brightness(1.05)}
  .readBtn.run{background:#dc2626;border-color:#dc2626}
  .detailsBtn{width:100%;text-align:left;border:1px solid var(--line);background:#f8fafc;color:var(--sub);border-radius:10px;padding:8px 12px;font-size:13px;font-weight:600;cursor:pointer;margin-top:12px}
  .detailsBtn:hover{border-color:var(--accent);color:var(--accent)}
  .details.collapsed>.block{display:none}
  .mbar{width:96px;height:9px;border-radius:5px;background:#e5e7eb;overflow:hidden;flex:none}
  .mbar .mfill{height:100%;border-radius:5px;transition:width .25s,background .25s}
  .pagenav{display:flex;gap:8px;justify-content:flex-end;flex-wrap:wrap;margin-bottom:6px}
  .pagenav a{text-decoration:none;font-size:13px;color:#475569;border:1px solid var(--line);border-radius:999px;padding:6px 14px;font-weight:600;transition:.15s}
  .pagenav a:hover{border-color:var(--accent);color:var(--accent);background:#f0f6ff}
</style>
</head>
<body>
<div class="wrap">
<nav class="pagenav">
  <a href="index.html">\U0001f3e0 首页</a>
  <a href="review.html">\U0001f4da 已学回顾</a>
  <a href="calendar.html">\U0001f4c5 日历</a>
</nav>
  <header>
    <h1>\U0001f5a3 英语口语 · Day __DAY__（增强版）</h1>
    <p>旅游 + 日常混合 · __N__ 句/天 · 中英对照 + 生词音标 + 原声伴读 + 变体 + 场景俗语 + 语法 + 发音提示</p>
  </header>
  <div class="summary">
    <div class="box"><b>第 __DAY__ 天</b><span>连续学习</span></div>
    <div class="box"><b>__INTRO__ 句</b><span>今日新学</span></div>
    <div class="box"><b>__TOTAL__/__POOL__</b><span>累计已学</span></div>
    <div class="box"><b>__POOL__ 句</b><span>当前总池</span></div>
  </div>
  <div class="legend">
    <span>\U0001f53b <b>简化/口语变体</b></span>
    <span>\U0001f3ad <b>场景化表达 + 不同回答</b></span>
    <span>\U0001f4dd <b>语法提示</b></span>
    <span>\U0001f524 <b>发音提示(连读/同化/滑音/浊化/失去爆破/闪音/弱读/缩读)</b></span>
  </div>
  <div class="toolbar">
    <button class="btn primary" onclick="playAll()">▶ 全部伴读</button>
    <label class="spd">语速(批量预设)
      <select id="speedSel" onchange="setSpeed(this.value)" title="设为统一语速应用到全部句子">
        <option value="1">1倍</option>
        <option value="0.8">0.8倍</option>
        <option value="0.7">0.7倍</option>
        <option value="0.6">0.6倍</option>
      </select>
    </label>
    <button class="btn" onclick="stopAll()">⏹ 停止</button>
    <button class="btn" id="allDetBtn" onclick="toggleAllDetails()">\U0001f4c2 展开全部详情</button>
  </div>
  <div id="short"></div>
  <div id="long"></div>
  <footer>每天 9:00 自动推送新一批（同款增强版） · 进度本地保存，不外传</footer>
</div>
<script src="audio-engine.js"></script>
<script>
(function(){ const d=new Date().toISOString().slice(0,10); document.querySelectorAll('.today-nav').forEach(a=>a.href='day'+d+'.html'); })();
const DATA = __DATA_JSON__;
let speed = 1;
let cardSpeed = {};
try { DATA.forEach(d => { const sv = localStorage.getItem('vocab_speed_'+String(d.id).replace('s','')); if(sv) cardSpeed[d.id]=parseFloat(sv); }); } catch(e){}
const API_PORT = 3279;
try { const sv = localStorage.getItem('vocab_speed'); if (sv) { speed = parseFloat(sv); document.getElementById('speedSel').value = sv; } } catch(e){}
async function apiFetch(path, opts){
  for(const b of ['', 'http://127.0.0.1:'+API_PORT]){
    try{ const r = await fetch(b+path, opts); if(r && r.ok) return r; }catch(e){}
  }
  return null;
}
async function assess(sid, action, btn){
  const id = parseInt(String(sid).replace('s',''),10);
  const r = await apiFetch('/api/mastery', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({id, action})});
  const el = document.getElementById('mb-'+sid);
  const st = document.getElementById('as-'+sid);
  const cur = parseInt((el?el.textContent:'0/5').replace('/5',''),10)||0;
  let nv = cur;
  if(r){
    const j = await r.json(); nv = j.mastery;
    if(st) st.textContent = (action==='clear'?'已 +1':action==='unknown'?'已 -1':'已记录')+' · 已回写 ✓';
  } else {
    nv = action==='clear'?Math.min(5,cur+1):action==='unknown'?Math.max(0,cur-1):cur;
    if(st) st.textContent = '已本地记录（启动本地服务后可回写）';
  }
  setMbar(sid, nv);
  try{ localStorage.setItem('vocab_mastery_'+id, String(nv)); }catch(e){}
  if(btn) btn.blur();
}
function setSpeed(v){ speed=parseFloat(v); try{ localStorage.setItem('vocab_speed', String(speed)); }catch(e){}
  document.querySelectorAll('.spdSel').forEach(s=>s.value=v);
  DATA.forEach(d=>{ const sid=String(d.id).replace('s',''); cardSpeed[d.id]=speed; try{ localStorage.setItem('vocab_speed_'+sid, v); }catch(e){} }); }
function cardHTML(d){
  const kw=d.kw.map(k=>`<span class="chip"><b>${k[0]}</b><span class="p">${k[1]}</span> ${k[2]}</span>`).join('');
  const v=d.variants.map(x=>`<li><span class="ex">${x[0]}</span> <span class="nt">— ${x[1]}</span></li>`).join('');
  const sc=d.scenes.map(x=>`<li><span class="occ">【${x[0]}】</span> ${x[1]} <span class="resp">→ ${x[2]}</span></li>`).join('');
  return `<div class="card">
    <div class="top">
      <span class="num">${d.id.replace('s','')}</span>
      <span class="pill ${d.topic}">${d.topic==='travel'?'旅游':'日常'}</span>
      <span class="play">
        <span class="ic" title="原声伴读" onclick="playAudio('${d.id}')">\U0001f50a</span>
        <span class="ic" title="慢速朗读" onclick="playAudio('${d.id}', 0.7)">\U0001f422</span>
      </span>
    </div>
    <div class="en">${d.en}</div>
    <div class="ipa">${d.ipa}</div>
    <div class="zh">${d.zh}</div>
    <div class="kw">${kw}</div>
    <button class="detailsBtn" id="db-${d.id}" onclick="toggleDetails('${d.id}')">\U0001f4c2 展开详情（变体 / 场景 / 语法 / 发音）</button>
    <div class="details collapsed" id="dt-${d.id}">
      <div class="block var"><div class="h">\U0001f53b 简化 / 口语变体</div><ul>${v}</ul></div>
      <div class="block scene"><div class="h">\U0001f3ad 场景化表达 + 不同回答</div><ul>${sc}</ul></div>
      <div class="block gram"><div class="h">\U0001f4dd 语法提示</div><div>${d.grammar}</div></div>
      <div class="block pr"><div class="h">\U0001f524 发音提示（连读/同化/滑音/浊化/失去爆破/闪音/弱读/缩读）</div><div>${d.pron}</div></div>
    </div>
    <audio id="au-${d.id}" preload="none" src="audio/${d.id}.mp3"></audio>
    <div class="readwrap">
      <span class="rlbl">\U0001f501 朗读</span>
      <select id="rp-${d.id}" class="repsSel">
        <option value="2">2 遍</option>
        <option value="3" selected>3 遍</option>
        <option value="5">5 遍</option>
        <option value="8">8 遍</option>
      </select>
      <button id="rb-${d.id}" class="readBtn" onclick="loopSpeak('${d.id}')">▶ 开始</button>
      <span class="spdlbl">语速</span>
      <select class="spdSel" onchange="setCardSpeed('${d.id}',this.value)">
        <option value="1">1倍</option>
        <option value="0.8">0.8倍</option>
        <option value="0.7">0.7倍</option>
        <option value="0.6">0.6倍</option>
      </select>
    </div>
    <div class="assess">
      <span class="lbl">自评掌握度：</span>
      <div class="mbar" id="mbar-${d.id}"><div class="mfill" style="width:${d.mastery*20}%;background:${d.mastery<=2?'#dc2626':d.mastery<=4?'#d97706':'#16a34a'}"></div></div>
      <span class="mbadge" id="mb-${d.id}">${d.mastery}/5</span>
      <button class="c" onclick="assess('${d.id}','clear',this)">✅ 认识 +1</button>
      <button class="f" onclick="assess('${d.id}','fuzzy',this)">\U0001f7e1 模糊</button>
      <button class="u" onclick="assess('${d.id}','unknown',this)">\U0001f534 不认识 -1</button>
      <span class="astat" id="as-${d.id}"></span>
    </div>
  </div>`;
}
if(DATA.some(d=>d.type==='short')){
  const n=DATA.filter(d=>d.type==='short').length;
  const st=document.createElement('div'); st.className='sec-title';
  st.innerHTML=`<span class="tag">短句</span> Short sentences（${n}）`; document.querySelector('.wrap').insertBefore(st, document.getElementById('short'));
  document.getElementById('short').innerHTML=DATA.filter(d=>d.type==='short').map(cardHTML).join('');
}
if(DATA.some(d=>d.type==='long')){
  const n=DATA.filter(d=>d.type==='long').length;
  const st=document.createElement('div'); st.className='sec-title';
  st.innerHTML=`<span class="tag">长句</span> Long sentences（${n}）`; document.querySelector('.wrap').insertBefore(st, document.getElementById('long'));
  document.getElementById('long').innerHTML=DATA.filter(d=>d.type==='long').map(cardHTML).join('');
}
applyStoredDetails();
function setCardDetails(id, show){ const el=document.getElementById('dt-'+id); if(!el) return; el.classList.toggle('collapsed', !show);
  const btn=document.getElementById('db-'+id); if(btn) btn.textContent = show ? '\U0001f4c1 收起详情（变体 / 场景 / 语法 / 发音）' : '\U0001f4c2 展开详情（变体 / 场景 / 语法 / 发音）';
  try{ localStorage.setItem('vocab_details_'+id, show?'open':'closed'); }catch(e){} }
function toggleDetails(id){ const el=document.getElementById('dt-'+id); if(el) setCardDetails(id, el.classList.contains('collapsed')); }
function toggleAllDetails(){ const anyCollapsed = !!document.querySelector('.details.collapsed'); const show = anyCollapsed;
  document.querySelectorAll('.details').forEach(el=>setCardDetails(el.id.replace('dt-',''), show));
  const gb=document.getElementById('allDetBtn'); if(gb) gb.textContent = show ? '\U0001f4c1 收走全部详情' : '\U0001f4c2 展开全部详情'; }
function applyStoredDetails(){ DATA.forEach(d=>{ let st=null; try{ st=localStorage.getItem('vocab_details_'+d.id); }catch(e){}
  if(st==='open') setCardDetails(d.id, true); });
  const gb=document.getElementById('allDetBtn'); if(gb) gb.textContent = document.querySelector('.details.collapsed') ? '\U0001f4c2 展开全部详情' : '\U0001f4c1 收走全部详情'; }
function mColor(v){ return v<=2?'#dc2626':(v<=4?'#d97706':'#16a34a'); }
function setMbar(sid,v){ const bar=document.getElementById('mbar-'+sid);
  if(bar){ const f=bar.querySelector('.mfill'); f.style.width=(v*20)+'%'; f.style.background=mColor(v); }
  const b=document.getElementById('mb-'+sid); if(b) b.textContent=v+'/5'; }
function playAudio(id, rate){ if(window.VocabAudio){ VocabAudio.play(id, rate || cardSpeed[id] || speed); } }
function loopSpeak(id){ const btn=document.getElementById('rb-'+id); if(!btn) return;
  if(btn.classList.contains('run')){ if(window.VocabAudio) VocabAudio.stopId(id); btn.classList.remove('run'); btn.textContent='▶ 开始'; return; }
  const reps=parseInt(document.getElementById('rp-'+id).value,10)||3;
  btn.classList.add('run'); btn.textContent='⏹ 停止';
  if(window.VocabAudio){ VocabAudio.loop(id, cardSpeed[id]||speed, reps, { onEnd: ()=>{ btn.classList.remove('run'); btn.textContent='▶ 开始'; } }); }
  else { btn.classList.remove('run'); btn.textContent='▶ 开始'; } }
function setCardSpeed(id,v){ cardSpeed[id]=parseFloat(v);
  try{ localStorage.setItem('vocab_speed_'+String(id).replace('s',''), v); }catch(e){} }
function speak(t){ /* deprecated: 所有播放统一走服务器音频 VocabAudio */ }
let queue=[]; function playAll(){ stopAll(); queue=DATA.map(d=>d.id); next(); }
function next(){ if(!queue.length){ stopAll(); return; }
  const id=queue.shift();
  if(window.VocabAudio){ VocabAudio.play(id, cardSpeed[id]||speed, ()=>{ next(); }); }
  else { stopAll(); return; } }
function stopAll(){ queue=[]; if(window.VocabAudio) VocabAudio.stopAll();
  document.querySelectorAll('.readBtn.run').forEach(b=>{ b.classList.remove('run'); b.textContent='▶ 开始'; }); }
</script>
</body>
</html>"""

PAGE = (PAGE
        .replace("__DAY__", str(dayIndex))
        .replace("__N__", str(dailyCount))
        .replace("__INTRO__", str(sum(1 for s in selected if s["learn"].get("introducedDay") == dayIndex)))
        .replace("__DATA_JSON__", DATA_JSON)
        .replace("__TOTAL__", str(learned))
        .replace("__POOL__", str(total)))

day_file = os.path.join(BASE, "day%s.html" % today_str)
with open(day_file, "w", encoding="utf-8") as f:
    f.write(PAGE)

# 重生成 master.html
try:
    subprocess.run([VENV_PY, "gen_master_html.py"], cwd=BASE, check=True, capture_output=True, text=True)
except Exception as e:
    print("MASTER_HTML_FAIL", e)

# ============ 汇总 ============
streak_note = "连续天数≈%d（自 %s 起）" % (dayIndex, meta["startDate"])
print("==== DAILY SUMMARY ====")
print("today:", today_str, "dayIndex:", dayIndex, "mode:", mode)
print("selected:", selected_ids)
print("expanded_new:", expanded)
print("learned_total:", learned, "/", total)
print("today_new:", sum(1 for s in selected if s["learn"]["introducedDay"] == dayIndex))
print("day_file:", day_file)
