# -*- coding: utf-8 -*-
"""生成「已学回顾 review.html」与「学习日历 calendar.html」。
关键：把数据直接内嵌进页面（不再运行时 fetch master.json / days.json / day*.json），
因此无论是通过服务地址、WorkBuddy 预览面板，还是直接双击本地文件打开，都能正常显示。
数据取自 master.json / days.json / day<日期>.json 侧车。
用法：python gen_views_html.py
"""
import json, os, glob, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
MASTER = os.path.join(BASE, "master.json")
DAYS = os.path.join(BASE, "days.json")


def load_master():
    with open(MASTER, encoding="utf-8") as f:
        return json.load(f)


def load_days():
    if os.path.exists(DAYS):
        try:
            with open(DAYS, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def load_day_ids():
    """读取所有 day<YYYY-MM-DD>.json 侧车，返回 {日期: [ids]}。"""
    out = {}
    for p in glob.glob(os.path.join(BASE, "day????-??-??.json")):
        try:
            with open(p, encoding="utf-8") as f:
                j = json.load(f)
            d = j.get("date") or os.path.basename(p)[3:-5]
            ids = j.get("ids") or []
            out[d] = ids
        except Exception:
            pass
    return out


def slim(s):
    """抽取渲染卡片所需的字段。"""
    learn = s.get("learn", {}) or {}
    return {
        "id": s["id"],
        "en": s.get("en"),
        "zh": s.get("zh"),
        "category": s.get("category"),
        "theme": s.get("theme"),
        "mastery": int(learn.get("mastery") or 0),
        "introducedDay": learn.get("introducedDay") or 0,
        "keyvocab": s.get("keyvocab") or [],
        "enh": learn.get("enh") or {},
    }


def safe_json(obj):
    """JSON 字符串，转义 </ 以防提前闭合 <script>。"""
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


# ---------- 已学回顾 ----------
REVIEW_TMPL = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>已学回顾 · 英语口语学习</title>
<link rel="stylesheet" href="cards.css">
<style>
  .pagenav a.cur{background:var(--travel);border-color:var(--travel);color:#fff}
</style>
</head>
<body>
<div class="wrap">
  <nav class="pagenav">
    <a href="index.html">🏠 首页</a>
    <a class="cur" href="review.html">📚 已学回顾</a>
  </nav>
  <div class="phead">
    <h1>📚 已学回顾</h1>
    <p>所有已引入学习的句式范式总览 · 点击任意一句可跳转到总览页查看完整发音详情</p>
  </div>
  <div class="pstat" id="stat"><b id="nLearned">0</b><span>已学句式（按引入日期排列）</span></div>
  <div class="grid" id="grid"></div>
</div>
<script src="audio-engine.js"></script>
<script src="mastery.js"></script>
<script src="cards.js"></script>
<script>
const REVIEW_DATA = /*REVIEW_DATA*/;
(function(){
  const grid = document.getElementById('grid');
  const learned = REVIEW_DATA || [];
  document.getElementById('nLearned').textContent = learned.length;
  if (!learned.length){
    grid.innerHTML = '<div class="empty">还没有已学的句式。返回首页开始今日练习吧。</div>';
    return;
  }
  grid.innerHTML = learned.map(s => renderSentenceCard({
    id:s.id, en:s.en, zh:s.zh, category:s.category, theme:s.theme,
    mastery:s.mastery||0, keyvocab:s.keyvocab||[], enh:s.enh||{}
  })).join('');
  if(window.VocabMastery) VocabMastery.refreshAll();
})();
</script>
</body>
</html>"""


# ---------- 学习日历 ----------
CAL_TMPL = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>学习日历 · 英语口语学习</title>
<link rel="stylesheet" href="cards.css">
<style>
  .pagenav a.cur{background:var(--travel);border-color:var(--travel);color:#fff}
  .recent{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:14px;font-size:13px;color:var(--sub)}
  .recent .rlbl{font-weight:600;color:#475569}
  .recent .rchip{border:1px solid var(--daily);background:#eafaf3;color:var(--daily);
    border-radius:999px;padding:5px 14px;font-size:13px;font-weight:600;cursor:pointer;transition:.15s}
  .recent .rchip:hover{background:#d7f5ea}
  .recent .rchip.rprev{background:#fff7ed;color:#b45309;border-color:#fed7aa}
  .recent .rchip.rprev:hover{background:#fde9d3}
</style>
</head>
<body>
<div class="wrap">
  <nav class="pagenav">
    <a href="index.html">🏠 首页</a>
    <a href="review.html">📚 已学回顾</a>
    <a class="cur" href="calendar.html">📅 学习日历</a>
  </nav>
  <div class="phead">
    <h1>📅 学习日历</h1>
    <p>🟢 绿色=已练习 · 🟠 橙色=可提前预习（点开即学）· 点「最近练习 / 可预习」或日历高亮日期查看当日句式，点句子可跳转总览详情</p>
  </div>
  <div class="recent" id="recent"></div>
  <div class="cal">
    <div class="chead">
      <div>
        <button class="navbtn" id="prevBtn">‹ 上个月</button>
        <button class="navbtn" id="nextBtn">下个月 ›</button>
      </div>
      <div>
        <h2 id="calTitle">—</h2>
        <a class="today-chip" id="todayChip" href="#">今天</a>
      </div>
    </div>
    <div class="calgrid" id="calgrid"></div>
  </div>
  <div class="daypanel" id="daypanel"></div>
</div>
<script src="audio-engine.js"></script>
<script src="mastery.js"></script>
<script src="cards.js"></script>
<script>
const CAL_DATA = /*CAL_DATA*/;
const DOW = ['日','一','二','三','四','五','六'];
let practiced = new Set(CAL_DATA.days || []);
let preview = new Set(CAL_DATA.previewDays || []);
let recovered = new Set(CAL_DATA.recoveredDays || []);
let sMap = CAL_DATA.smap || {};
let dayIds = CAL_DATA.dayIds || {};
let viewY = 0, viewM = 0;

function pad(n){ return n<10 ? '0'+n : ''+n; }
function ymd(y,m,d){ return y + '-' + pad(m+1) + '-' + pad(d); }
function todayStr(){ const t = new Date(); return ymd(t.getFullYear(), t.getMonth(), t.getDate()); }

function renderRecent(){
  const box = document.getElementById('recent');
  const dsP = (CAL_DATA.days||[]).slice().sort().reverse().slice(0,3); // 最近 3 次
  const dsU = (CAL_DATA.previewDays||[]).slice().sort().slice(0,5);   // 可预习（最早 5 天）
  let html = '';
  if (dsP.length) html += '<span class="rlbl">最近练习：</span>' +
    dsP.map(d => '<button class="rchip" onclick="showDay(\'' + d + '\')">' + d + '</button>').join('');
  if (dsU.length) html += '<span class="rlbl" style="margin-left:10px">可预习：</span>' +
    dsU.map(d => '<button class="rchip rprev" onclick="showDay(\'' + d + '\')">🔓 ' + d + '</button>').join('');
  if (!html){ box.style.display='none'; return; }
  box.innerHTML = html;
}

function renderCalendar(){
  const grid = document.getElementById('calgrid');
  const title = document.getElementById('calTitle');
  title.textContent = viewY + ' 年 ' + (viewM+1) + ' 月';
  grid.innerHTML = '';
  DOW.forEach(d => { const c=document.createElement('div'); c.className='dow'; c.textContent=d; grid.appendChild(c); });
  const first = new Date(viewY, viewM, 1);
  const startDow = first.getDay();
  const daysInMonth = new Date(viewY, viewM+1, 0).getDate();
  const tStr = todayStr();
  for (let i=0;i<startDow;i++){ const e=document.createElement('div'); e.className='calcell empty'; grid.appendChild(e); }
  for (let d=1; d<=daysInMonth; d++){
    const ds = ymd(viewY, viewM, d);
    const c=document.createElement('div'); c.className='calcell';
    const isPrac = practiced.has(ds);
    const isPrev = preview.has(ds);
    const isRec = recovered.has(ds);
    if (isPrac) c.className += ' prac';
    if (isPrev) c.className += ' preview';
    if (isRec) c.className += ' prac';
    if (ds === tStr) c.className += ' today';
    c.textContent = d;
    if (isPrac || isPrev || isRec){
      const dot=document.createElement('span'); dot.className='dot'; c.appendChild(dot);
      c.onclick=()=>showDay(ds);
    }
    grid.appendChild(c);
  }
}

function showDay(ds){
  const panel = document.getElementById('daypanel');
  let ids = dayIds[ds] || [];
  if (!ids.length){
    panel.innerHTML = '<div class="empty">该日（'+ds+'）没有可用的练习数据。</div>';
    return;
  }
  const tag = preview.has(ds) ? ' 🔓预习' : '';
  const cards = ids.map(id => {
    const s = sMap[id]; if(!s) return '';
    return renderSentenceCard({ id:s.id, en:s.en, zh:s.zh, category:s.category, theme:s.theme,
      mastery:s.mastery||0, keyvocab:s.keyvocab||[], enh:s.enh||{} });
  }).join('');
  panel.innerHTML = '<div class="dph">📅 ' + ds + ' 练习句式' + tag + ' <span>（共 ' + ids.length + ' 句，点击句子可跳转总览）</span></div>' +
    '<div class="grid">' + (cards || '<div class="empty">该日无可用句子数据。</div>') + '</div>';
  panel.scrollIntoView({behavior:'smooth', block:'start'});
  if(window.VocabMastery) VocabMastery.refreshAll();
}

document.getElementById('prevBtn').onclick = ()=>{ viewM--; if(viewM<0){viewM=11;viewY--;} renderCalendar(); };
document.getElementById('nextBtn').onclick = ()=>{ viewM++; if(viewM>11){viewM=0;viewY++;} renderCalendar(); };
document.getElementById('todayChip').onclick = (e)=>{
  e.preventDefault();
  const t=new Date(); viewY=t.getFullYear(); viewM=t.getMonth(); renderCalendar();
  const ts=todayStr();
  if(practiced.has(ts)) showDay(ts);
  else document.getElementById('daypanel').innerHTML='<div class="empty">今天（'+ts+'）还没有生成练习页。每日 9:00 自动推送后会显示在这里。</div>';
};

(function(){
  const t=new Date(); viewY=t.getFullYear(); viewM=t.getMonth();
  renderRecent(); renderCalendar();
  if(window.VocabMastery) VocabMastery.refreshAll();
})();
</script>
</body>
</html>"""


def main():
    master = load_master()
    S = master.get("sentences", [])
    days = load_days()
    day_ids = load_day_ids()

    # 已学回顾：所有已引入的句式
    learned = [slim(s) for s in S if s.get("learn") and s["learn"].get("introduced")]
    learned.sort(key=lambda s: (s["introducedDay"], s["id"]))

    # 学习日历：句子映射 + 每日 ids
    smap = {s["id"]: slim(s) for s in S}

    # 预习日：有 day<日期>.json 侧车、日期晚于今天、且尚未登记为「已练习」的日期
    today_str = datetime.date.today().isoformat()
    practiced_set = set(days)
    preview_days = sorted(d for d in day_ids if d > today_str and d not in practiced_set)
    # 容错：有侧车内容、日期已过、但当日自动化漏登记进 days.json 的「孤儿日」，
    # 也作为可点击的已练习日显示（绿色、无 🔓 横幅），避免日历出现点不了/无数据的死格
    recovered_days = sorted(d for d in day_ids if d <= today_str and d not in practiced_set)

    review_html = REVIEW_TMPL.replace("/*REVIEW_DATA*/", safe_json(learned))
    cal_data = {"days": days, "smap": smap, "dayIds": day_ids,
                "previewDays": preview_days, "recoveredDays": recovered_days, "todayStr": today_str}
    cal_html = CAL_TMPL.replace("/*CAL_DATA*/", safe_json(cal_data))

    with open(os.path.join(BASE, "review.html"), "w", encoding="utf-8") as f:
        f.write(review_html)
    with open(os.path.join(BASE, "calendar.html"), "w", encoding="utf-8") as f:
        f.write(cal_html)

    print("GEN_VIEWS: review=%d learned, calendar days=%d, preview=%d, smap=%d, dayIds=%d"
          % (len(learned), len(days), len(preview_days), len(smap), len(day_ids)))


if __name__ == "__main__":
    main()
