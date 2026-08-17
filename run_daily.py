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
    --bg:#f5f7fa; --card:#ffffff; --text:#1f2329; --sub:#6b7280; --line:#e5e7eb;
    --accent:#2f6fed; --accent2:#0e9f6e; --warn:#b45309; --pron:#0369a1;
    --travel:#eef4ff; --daily:#eafaf3; --chip:#fff4e5; --var:#f3f0ff; --scene:#eafaf3; --gram:#fff7ed; --pr:#eaf4ff;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:-apple-system,"PingFang SC","Microsoft YaHei",Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.65;padding:24px 16px 60px}
  .wrap{max-width:820px;margin:0 auto}
  header{text-align:center;margin-bottom:14px}
  header h1{font-size:22px;font-weight:700}
  header p{color:var(--sub);font-size:13.5px;margin-top:6px}
  .legend{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;font-size:12px;color:var(--sub);margin:6px 0 18px}
  .legend b{color:var(--text)}
  .toolbar{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin:0 0 22px}
  .btn{border:1px solid var(--line);background:#fff;color:var(--text);border-radius:999px;padding:7px 16px;font-size:14px;cursor:pointer;transition:.15s}
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
  .block ul{margin:0;padding-left:18px} .block li{margin:3px 0}
  .scene li .occ{color:#0e9f6e;font-weight:600} .scene li .resp{color:#6b7280}
  .rate{margin-top:14px;border-top:1px dashed var(--line);padding-top:12px;display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-size:13px}
  .rate .rlbl{color:var(--sub);font-weight:600}
  .rbtn{border:1px solid var(--line);background:#fff;border-radius:8px;padding:6px 12px;font-size:13px;cursor:pointer}
  .rbtn.up{border-color:#16a34a;color:#16a34a} .rbtn.up:hover{background:#f0fdf4}
  .rbtn.fz{border-color:#d97706;color:#d97706} .rbtn.fz:hover{background:#fffbeb}
  .rbtn.dn{border-color:#dc2626;color:#dc2626} .rbtn.dn:hover{background:#fef2f2}
  .rstat{font-size:12px;color:var(--sub);margin-left:4px}
  .rstat.ok{color:#16a34a;font-weight:600}
  footer{text-align:center;color:var(--sub);font-size:12px;padding:18px}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>🗣 英语口语 · Day __DAY__（增强版）</h1>
    <p>选句模式：__MODE__ · 中英对照 + 生词音标 + 原声伴读 + 变体 + 场景俚语 + 语法 + 发音提示（覆盖：连读/同化/滑音/浊化/失去爆破/闪音/弱读/缩读）</p>
  </header>
  <div class="legend">
    <span>🔹 <b>简化/口语变体</b></span>
    <span>🎭 <b>场景化表达 + 不同回答</b></span>
    <span>📝 <b>语法提示</b></span>
    <span>🔤 <b>发音提示</b></span>
  </div>
  <div class="toolbar">
    <button class="btn primary" onclick="playAll()">▶ 全部伴读</button>
    <button class="btn" id="slowBtn" onclick="toggleSlow()">🐢 慢速：关</button>
    <button class="btn" onclick="stopAll()">⏹ 停止</button>
  </div>
  <div class="sec-title"><span class="tag">短句</span> Short sentences（__NSHORT__）</div>
  <div id="short"></div>
  <div class="sec-title"><span class="tag">长句</span> Long sentences（__NLONG__）</div>
  <div id="long"></div>
  <footer>每天 10:00 自动推送新一批（同款增强版）· 底部自评按钮实时回写掌握度 · 进度本地保存，不外传</footer>
</div>
<script>
const DATA = __DATA_JSON__;
let slow=false;
function toggleSlow(){ slow=!slow; document.getElementById('slowBtn').textContent='🐢 慢速：'+(slow?'开':'关'); }
function cardHTML(d){
  const kw=d.kw.map(k=>`<span class="chip"><b>${k[0]}</b><span class="p">${k[1]}</span> ${k[2]}</span>`).join('');
  const v=d.variants.map(x=>`<li><span class="ex">${x[0]}</span> <span class="nt">— ${x[1]}</span></li>`).join('');
  const sc=d.scenes.map(x=>`<li><span class="occ">【${x[0]}】</span> ${x[1]} <span class="resp">→ ${x[2]}</span></li>`).join('');
  return `<div class="card">
    <div class="top">
      <span class="num">${d.id.replace('s','')}</span>
      <span class="pill ${d.topic}">${d.topic==='travel'?'旅游':'日常'}</span>
      <span class="play">
        <span class="ic" title="原声伴读" onclick="playAudio('${d.id}')">🔊</span>
        <span class="ic" title="慢速朗读" onclick="speak('${encodeURIComponent(d.en)}',true)">🐢</span>
      </span>
    </div>
    <div class="en">${d.en}</div>
    <div class="ipa">${d.ipa}</div>
    <div class="zh">${d.zh}</div>
    <div class="kw">${kw}</div>
    <div class="block var"><div class="h">🔹 简化 / 口语变体</div><ul>${v}</ul></div>
    <div class="block scene"><div class="h">🎭 场景化表达 + 不同回答</div><ul>${sc}</ul></div>
    <div class="block gram"><div class="h">📝 语法提示</div><div>${d.grammar}</div></div>
    <div class="block pr"><div class="h">🔤 发音提示（连读 / 同化 / 滑音 / 浊化 / 失去爆破 / 闪音 / 弱读 / 缩读）</div><div>${d.pron}</div></div>
    <div class="rate" data-nid="${d.nid}">
      <span class="rlbl">自评掌握度：</span>
      <button class="rbtn up" onclick="rate(${d.nid},'clear')">认识 +1</button>
      <button class="rbtn fz" onclick="rate(${d.nid},'fuzzy')">模糊</button>
      <button class="rbtn dn" onclick="rate(${d.nid},'unknown')">不认识 -1</button>
      <span class="rstat" id="rstat-${d.nid}"></span>
    </div>
  </div>`;
}
document.getElementById('short').innerHTML=DATA.filter(d=>d.type==='short').map(cardHTML).join('');
document.getElementById('long').innerHTML=DATA.filter(d=>d.type==='long').map(cardHTML).join('');
function playAudio(id){ const a=new Audio('audio/'+id+'.mp3');
  a.onerror=()=>speak(encodeURIComponent(DATA.find(d=>d.id===id).en),slow);
  a.play().catch(()=>speak(encodeURIComponent(DATA.find(d=>d.id===id).en),slow)); }
function speak(t,sl){ const u=new SpeechSynthesisUtterance(decodeURIComponent(t));
  u.lang='en-US'; u.rate=sl?0.55:0.95;
  const v=speechSynthesis.getVoices().find(x=>x.lang&&x.lang.startsWith('en')); if(v)u.voice=v;
  speechSynthesis.cancel(); speechSynthesis.speak(u); }
let queue=[]; function playAll(){ stopAll(); queue=DATA.map(d=>d.en); next(); }
function next(){ if(!queue.length)return; const u=new SpeechSynthesisUtterance(queue.shift());
  u.lang='en-US'; u.rate=slow?0.55:0.95;
  const v=speechSynthesis.getVoices().find(x=>x.lang&&x.lang.startsWith('en')); if(v)u.voice=v;
  u.onend=next; speechSynthesis.speak(u); }
function stopAll(){ speechSynthesis.cancel(); queue=[]; }
const PORT=8765;
async function apiPost(path,body){ try{ const r=await fetch('http://127.0.0.1:'+PORT+path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}); return await r.json(); }catch(e){ return null; } }
async function rate(nid,action){
  const el=document.getElementById('rstat-'+nid);
  const r=await apiPost('/api/mastery',{id:nid,action:action});
  if(r && r.ok){ el.className='rstat ok'; el.textContent='已记录 ✓ 掌握度 '+r.mastery+'/5'; }
  else { el.className='rstat'; el.textContent='服务未连接（数据已本地显示）'; }
}
</script>
</body>
</html>"""

PAGE = (PAGE
        .replace("__DAY__", str(dayIndex))
        .replace("__MODE__", "新学" if mode == "new" else "复习")
        .replace("__DATA_JSON__", DATA_JSON)
        .replace("__NSHORT__", str(len(shorts)))
        .replace("__NLONG__", str(len(longs))))

day_file = os.path.join(BASE, "day%d.html" % dayIndex)
with open(day_file, "w", encoding="utf-8") as f:
    f.write(PAGE)

# 重生成 master.html
try:
    subprocess.run([VENV_PY, "gen_master_html.py"], cwd=BASE, check=True, capture_output=True, text=True)
except Exception as e:
    print("MASTER_HTML_FAIL", e)

# ============ 汇总 ============
total = len(S)
learned = sum(1 for s in S if s["learn"]["introduced"])
streak_note = "连续天数≈%d（自 %s 起）" % (dayIndex, meta["startDate"])
print("==== DAILY SUMMARY ====")
print("today:", today_str, "dayIndex:", dayIndex, "mode:", mode)
print("selected:", selected_ids)
print("expanded_new:", expanded)
print("learned_total:", learned, "/", total)
print("today_new:", sum(1 for s in selected if s["learn"]["introducedDay"] == dayIndex))
print("day_file:", day_file)
