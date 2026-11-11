"""朗读音色统一配置 —— 只改这里，全站所有生成脚本生效。

改动后必须重录已有音频，否则新旧音色混播：
    venv 解释器 regen_voice.py           # 重录 1..上限 全部
    venv 解释器 regen_voice.py 1 250     # 指定 id 区间

音色选型（2026-11-11 定）：
    en-US-AvaNeural  女声，温暖自然、吐词清楚不生硬，长句起伏自然
    语速 -15%：比自然语速慢一档，让连读/弱读有空间展开，跟读不吃力
"""

VOICE = "en-US-AvaNeural"
RATE = "-15%"
PITCH = "+0Hz"


def kwargs():
    """传给 edge_tts.Communicate 的语音参数。"""
    return {"rate": RATE, "pitch": PITCH}
