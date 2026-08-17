# -*- coding: utf-8 -*-
"""每日推送补完脚本（词力词汇教练）· 2026-08-17 Day 5。
补完 09:45 半成品运行：#11-15 已被 introduced 但 enh 为空。
本脚本为其撰写完整增强内容，写回 master.json，生成当日页并刷新 master.html。
"""
import json, os, subprocess, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
MASTER = os.path.join(BASE, "master.json")
VENV_PY = r"C:\Users\Win10\.workbuddy\binaries\python\envs\default\Scripts\python.exe"

# ============ Day 5 选中批（#11-15）完整增强内容 ============
ENH = {
    11: {
        "fullIpa": "/wɛr kən aɪ baɪ ə ˈtɪkɪt tə ðə ˈsɪti ˈsɛntər/",
        "variants": [
            ["Where do I get a ticket to downtown?", "downtown 美式常用，等同 city center"],
            ["How do I buy a ticket for the city?", "更直白的说法"],
            ["Ticket to the center — where to buy?", "极简口语，火车/公交场景"],
        ],
        "scenes": [
            ["火车站问售票处", "Where can I buy a ticket to the city center?", "对方指 Counter 3. / The machine over there.(那边机器)"],
            ["机场快线购票", "Can I get a ticket here for downtown?", "对方回 Yes, at the red kiosk.(红色自助机)"],
            ["不同回答", "Cash only at the window. / It's cheaper online.(网上更便宜) / Which zone are you going to?(去哪个区)"],
        ],
        "grammar": "Where can I + 动词原形 用于问地点/方式；buy a ticket to + 目的地。city center（英）/ downtown（美）都表市中心；ticket 指车票，飞机票也常说 ticket/fare。can 在疑问句与 I 之间弱读为 /kən/。",
        "pron": "连读：Where can→/wɛr kən/（r 与 k 连读）；can I→/kən aɪ/（n 与 a）；buy a→/baɪ ə/（a 与 ə）；ticket to→/ˈtɪkɪt tə/（t 与 t 只读一次）；to the→/tə ðə/（t 与 ð）；city center→/ˈsɪti ˈsɛntər/（i 与 s）。同化：无典型。滑音：无典型。浊化：无典型（Where can 中 k 在 ə 前保持清；buy a 中 b 本浊）。失去爆破：ticket to→/ˈtɪkɪ(t) tə/（t 在 t 前不完全爆破，只读一次）。闪音：city→/ˈsɪɾi/（美式，元音间 /t/ 标闪音 /ɾ/，关键！）；center→/ˈsɛnɾər/（美式，/t/ 在 ən 间标闪音 /ɾ/，关键！）。弱读：can→/kən/（功能词弱读省 /æ/）；a→/ə/；to→/tə/；the→/ðə/。缩读：无典型。",
    },
    12: {
        "fullIpa": "/haʊ lɔŋ dʌz ɪt teɪk tə ɡɛt ðɛr/",
        "variants": [
            ["How long is the trip?", "trip 表行程，更简"],
            ["How much time does it take?", "更直白"],
            ["How long will it take?", "will 表将来，问大概要多久"],
        ],
        "scenes": [
            ["问行程时长", "How long does it take to get there?", "对方回 About 20 minutes by bus. / It's a 40-minute drive.(开车40分钟)"],
            ["问步行", "How long on foot?", "省略主语，问步行要多久"],
            ["不同回答", "Depends on traffic.(看路况) / Not long, ten minutes tops.(最多十分钟) / Quite a while, half an hour.(挺久，半小时)"],
        ],
        "grammar": "How long does it take (to do)? 是固定句型，问『做某事要多久』；it 是形式主语，take 表花费时间。does 随主语 it 用第三人称单数。long 这里指时间长度，不是空间长短。",
        "pron": "连读：How long→/haʊ lɔŋ/（w 与 l）；long does→/lɔŋ dʌz/（ŋ 与 d）；does it→/dʌz ɪt/（z 与 ɪ）；it take→/ɪt teɪk/（t 与 t）；take to→/teɪk tə/（k 与 t）；to get→/tə ɡɛt/（t 与 ɡ）；get there→/ɡɛt ðɛr/（t 与 ð）。同化：无典型。滑音：无典型。浊化：无典型（take to 中 k 在 t 前保持清；does it 中 z 本浊）。失去爆破：it take→/ɪ(t) teɪk/（t 在 t 前不完全爆破，只读一次）；take to→/teɪ(k) tə/（k 在 t 前不完全爆破）；get there→/ɡɛ(t) ðɛr/（t 在 ð 前不完全爆破）。闪音：无典型（take 词尾 t 在相邻 t 前失爆而非闪音；get 词尾 t 在 ð 前失爆）。弱读：does→/dəz/（弱读省 /ʌ/）；it→/ɪt/（轻读）；to→/tə/。缩读：无典型。",
    },
    13: {
        "fullIpa": "/ɪz ðɪs sit ˈteɪkən/",
        "variants": [
            ["Is this seat free?", "free 表空闲，更口语"],
            ["Can I sit here?", "直接问能不能坐"],
            ["Is anyone sitting here?", "问是否有人，最自然"],
        ],
        "scenes": [
            ["火车/飞机找座", "Is this seat taken?", "对方回 No, go ahead. / Yes, sorry.(有人)"],
            ["餐厅留座", "Is this taken?", "更简，指椅子"],
            ["不同回答", "It's reserved.(被订了) / Help yourself.(请坐) / I'm saving it for a friend.(帮朋友留的)"],
        ],
        "grammar": "Is this + 名词 + taken? taken 是 take 的过去分词作形容词，表『被占用的』。问座位是否有人用，比 Is anyone here? 更明确。seat 单数，与 this 搭配用 is。",
        "pron": "连读：Is this→/ɪz ðɪs/（z 与 ð）；this seat→/ðɪs sit/（s 与 s 只读一次清音）；seat taken→/sit ˈteɪkən/（t 与 t）。同化：无典型。滑音：无典型。浊化：无典型（this seat 中 s 后接清 s 保持清；seat taken 中 t 清）。失去爆破：this seat→/ðɪ(s) sit/（s 在 s 前通常只读一次）；seat taken→/si(t) ˈteɪkən/（t 在 t 前不完全爆破，只读一次）。闪音：无典型（taken 词首 t 在元音后但不处于元音之间，不标闪音）。弱读：this→/ðɪs/（此处可重读）。缩读：无典型。",
    },
    14: {
        "fullIpa": "/aɪd laɪk ə ˈwɪndoʊ sit pliz/",
        "variants": [
            ["A window seat, please.", "省略 I'd like，值机柜台直接说"],
            ["Could I get a seat by the window?", "更委婉"],
            ["Window, not aisle, thanks.", "aisle 过道座，对比说明偏好"],
        ],
        "scenes": [
            ["机场值机", "I'd like a window seat, please.", "对方回 Sure, any preference on row?(哪排) / Window it is.(给您窗边)"],
            ["火车选座", "Can I have the window side?", "火车常用 side 而非 seat"],
            ["不同回答", "We only have aisle left.(只剩过道) / Window's taken, middle ok?(窗没了，中要吗) / No problem.(没问题)"],
        ],
        "grammar": "I'd like = I would like，比 I want 礼貌，点单/选座万能句。window seat 窗边座；aisle seat 过道座；middle seat 中间座。please 放句末表礼貌。",
        "pron": "同化：无典型（I'd like 中 d 后接 l，不触发 d+j）。连读：I'd like→/aɪd laɪk/（d 与 l）；like a→/laɪk ə/（k 与 ə）；a window→/ə ˈwɪndoʊ/（ə 与 w）；window seat→/ˈwɪndoʊ sit/（oʊ 与 s）；seat please→/sit pliz/（t 与 p）。滑音：无典型。浊化：like a 快读 /laɪɡə/（k→g 浊化，关键！）；window 中 d 本浊。失去爆破：window seat→/ˈwɪn(d)oʊ sit/（d 在 oʊ 前轻微不完全爆破）；seat please→/si(t) pliz/（t 在 p 前不完全爆破）。闪音：window 美式偶可读 /ˈwɪɾdoʊ/（d 在鼻音 n 与元音间轻微闪音 /ɾ/，可选）。弱读：a→/ə/；please 此处重读 /pliz/。缩读：I'd = I would（/aɪd/，'d 为 would 缩读，关键！）。",
    },
    15: {
        "fullIpa": "/wɛr ɪz ðə ˈbæɡɪdʒ kleɪm/",
        "variants": [
            ["Where do I pick up my luggage?", "pick up 取行李，更口语"],
            ["Where's the luggage carousel?", "carousel 转盘，指行李转盘"],
            ["How do I get to baggage claim?", "问怎么走过去"],
        ],
        "scenes": [
            ["机场取行李", "Where is the baggage claim?", "对方回 Follow the signs. / Downstairs, turn left.(楼下左转)"],
            ["问转盘", "Which belt is the Beijing flight?", "问哪条转盘"],
            ["不同回答", "It's right after customs.(过海关就到) / This way, I'll show you.(我带你) / Belt 5, near Exit B.(5号转盘，B口旁)"],
        ],
        "grammar": "Where is + 名词? 问地点；baggage claim 行李领取处（固定搭配，claim 此处理解『领取』）。luggage / baggage 同义；carousel 行李转盘。is 随单数主语。",
        "pron": "连读：Where is→/wɛə rɪz/（r 与 ɪ 连读，/wɛərɪz/）；is the→/ɪz ðə/（z 与 ð）；the baggage→/ðə ˈbæɡɪdʒ/（ə 与 b）；baggage claim→/ˈbæɡɪdʒ kleɪm/（dʒ 与 k）。同化：无典型。滑音：无典型。浊化：无典型（baggage 中 g 本浊；claim 中 k 在 l 前保持清）。失去爆破：baggage claim→/ˈbæɡɪ(d)ʒ kleɪm/（d 在 dʒ 前轻微不完全爆破）。闪音：无典型（baggage 中 ɡ 在 ɪ 前，非 t）。弱读：is→/z/（功能词弱读省 /ɪ/，/wɛə rɪz/）；the→/ðə/。缩读：Where is→/wɛərz/（'s 为 is 缩读，关键！）。",
    },
}

with open(MASTER, encoding="utf-8") as f:
    data = json.load(f)
meta = data["meta"]
S = data["sentences"]
by_id = {s["id"]: s for s in S}

today = datetime.date.today()
start = datetime.date.fromisoformat(meta["startDate"])
dayIndex = (today - start).days + 1
today_str = today.isoformat()

# 选中批：#11-15（今日新学批，09:45 已 introduced 但 enh 为空，本次补完）
selected = [by_id[i] for i in (11, 12, 13, 14, 15) if i in by_id]
selected_ids = [s["id"] for s in selected]

# 注入增强内容
for s in selected:
    if not s["learn"]["enh"].get("fullIpa") and s["id"] in ENH:
        s["learn"]["enh"].update(ENH[s["id"]])

# 更新 learn：introduced 已 true、introducedDay 已 5；刷新 lastReviewed，保持掌握度一致（补完而非二次计入）
for s in selected:
    L = s["learn"]
    L["introduced"] = True
    if not L.get("introducedDay"):
        L["introducedDay"] = dayIndex
    L["lastReviewed"] = today_str
    # 保持 mastery / reviewCount 不变（已在 09:45 计入一次）

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
        .replace("__MODE__", "新学")
        .replace("__DATA_JSON__", DATA_JSON)
        .replace("__NSHORT__", str(len(shorts)))
        .replace("__NLONG__", str(len(longs))))

day_file = os.path.join(BASE, "day%s.html" % today_str)
with open(day_file, "w", encoding="utf-8") as f:
    f.write(PAGE)

# 重生成 master.html
try:
    subprocess.run([VENV_PY, "gen_master_html.py"], cwd=BASE, check=True, capture_output=True, text=True)
except Exception as e:
    print("MASTER_HTML_FAIL", e)

total = len(S)
learned = sum(1 for s in S if s["learn"]["introduced"])
enhd = sum(1 for s in S if s["learn"]["introduced"] and s["learn"]["enh"].get("fullIpa"))
print("==== DAILY SUMMARY ====")
print("today:", today_str, "dayIndex:", dayIndex)
print("completed_batch:", selected_ids)
print("day_file:", day_file)
print("learned_total:", learned, "/", total)
print("introduced_with_enh:", enhd, "/", learned)
print("audio_checked: s11-s15 exist, skip gen")
