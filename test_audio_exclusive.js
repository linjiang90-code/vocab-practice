// 临时验证脚本：用打桩的 AudioContext 检验 audio-engine.js 的「互斥播放」
const fs = require('fs');
const vm = require('vm');
const path = require('path');

const src = fs.readFileSync(path.join(__dirname, 'audio-engine.js'), 'utf8');

function makeEnv(decodeDelay = 40, dur = 0.3) {
  const starts = [];   // 记录所有 start 的 source
  const stopped = [];
  class FakeCtx {
    constructor() { this.state = 'running'; this.destination = {}; }
    resume() {}
    createBufferSource() {
      const s = {
        buffer: null, playbackRate: { value: 1 }, onended: null, started: false, stopCalled: false,
        connect() {}, disconnect() {},
        start() { this.started = true; starts.push(this); },
        stop() { if (!this.started) return; this.stopCalled = true; stopped.push(this); if (this.onended) { const f = this.onended; this.onended = null; f(); } }
      };
      return s;
    }
    decodeAudioData(ab, ok) { setTimeout(() => ok({ duration: dur }), decodeDelay); return; }
  }
  const ctx = {
    window: {}, setTimeout, clearTimeout, Promise, console, Math, Date,
    fetch: () => Promise.resolve({ ok: true, status: 200, arrayBuffer: () => Promise.resolve(new ArrayBuffer(8)) }),
    AbortController: class { constructor() { this.signal = {}; } abort() {} },
    document: {
      querySelectorAll: () => [],
      getElementById: () => null,
      createElement: () => ({ style: {}, play() { return Promise.resolve(); }, pause() {} }),
      body: { appendChild() {} },
      documentElement: { appendChild() {} }
    }
  };
  ctx.window.AudioContext = FakeCtx;
  ctx.window.document = ctx.document;
  vm.createContext(ctx);
  vm.runInContext(src, ctx);
  return { V: ctx.window.VocabAudio, starts, stopped };
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  let fail = 0;

  // 场景 1：循环播放 A（3 遍）中途点 B —— B 应立刻独占，A 被停
  {
    const { V, starts, stopped } = makeEnv(30, 0.25);
    V.loop('1', 1, 3, {});
    await sleep(120);                       // A 已开始播
    const aStarted = starts.filter(s => s.started).length;
    V.play('2', 1);
    await sleep(300);
    const live = starts.filter(s => s.started && !s.stopCalled);
    const ok = V.isActive('2') && !V.isActive('1') && live.length === 1;
    console.log(`[场景1] A已起播=${aStarted>0} 存活音源=${live.length} A活动=${V.isActive('1')} B活动=${V.isActive('2')} => ${ok ? 'PASS' : 'FAIL'}`);
    if (!ok) fail++;
  }

  // 场景 2：解码竞态 —— 连点 A、B（间隔 10ms < 解码耗时），只应有 B 发声
  {
    const { V, starts } = makeEnv(80, 0.25);
    V.play('1', 1);
    await sleep(10);
    V.play('2', 1);
    await sleep(400);
    const live = starts.filter(s => s.started && !s.stopCalled);
    const only2 = live.length === 1 && V.isActive('2') && !V.isActive('1');
    console.log(`[场景2] 存活音源=${live.length} B活动=${V.isActive('2')} => ${only2 ? 'PASS' : 'FAIL'}`);
    if (!only2) fail++;
  }

  // 场景 3：循环 3 遍能正常跑完并自行结束（不因互斥逻辑卡住）
  {
    const { V, starts } = makeEnv(10, 0.12);
    let ended = false;
    V.loop('3', 1, 3, { onEnd: () => { ended = true; } });
    await sleep(2400);   // 打桩不触发 onended，每遍靠 400ms 兜底定时器推进
    console.log(`[场景3] 起播次数=${starts.length} 结束回调=${ended} 活动=${V.isActive('3')} => ${starts.length === 3 && ended ? 'PASS' : 'FAIL'}`);
    if (!(starts.length === 3 && ended)) fail++;
  }

  // 场景 4：点 B 后再点回 A（单次），A 应正常播，B 停止
  {
    const { V, starts } = makeEnv(20, 0.4);
    V.play('2', 1);
    await sleep(100);
    V.play('1', 1);
    await sleep(150);
    const live = starts.filter(s => s.started && !s.stopCalled);
    const ok = live.length === 1 && V.isActive('1') && !V.isActive('2');
    console.log(`[场景4] 存活音源=${live.length} A活动=${V.isActive('1')} => ${ok ? 'PASS' : 'FAIL'}`);
    if (!ok) fail++;
  }

  console.log(fail === 0 ? '\n全部通过' : `\n${fail} 项失败`);
  process.exit(fail === 0 ? 0 : 1);
})();
