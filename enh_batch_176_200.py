# -*- coding: utf-8 -*-
"""ENH 标注批次 176-200（Day61=10-12 解锁的 151-200 后半段）。
结构：fullIpa / variants / scenes / grammar / pron，与 101-150 同格式。
由 enh_merge.py 幂等合并进 master.json（仅 enh.fullIpa 为空时写入）。
"""
ENH = {
    176: {
        "fullIpa": "/ɪz ðə mjuːˈziːəm wɪˈðɪn ðɪs ˈdɪstrɪkt/",
        "variants": [
            ["Is the museum within this district?", "标准"],
            ["Is the museum in this area?", "area 比 district 更口语"],
            ["Where's the museum from here?", "直接问方位"],
        ],
        "scenes": [
            ["问前台/路人", "Is the museum within this district?", "对方回 It's across the river, actually."],
            ["确认范围", "Which district is it in?", "问属哪个区"],
            ["步行", "It's a long walk, take the metro.", "建议坐地铁"],
        ],
        "grammar": "within + 范围『在…之内』；this district『这个区』。museum 博物馆；district 行政区/区域。within 强调『在边界内』。",
        "pron": "连读：Is the→/ɪz ðə/（z 与 ð）；the museum→/ðə mjuːˈziːəm/（ð 与 m）；museum within→/mjuːˈziːəm wɪˈðɪn/（m 与 w）；within this→/wɪˈðɪn ðɪs/（n 与 ð）；this district→/ðɪs ˈdɪstrɪkt/（s 与 d）。弱读：the→/ðə/、is→/ɪz/（重读）、within→/wɪˈðɪn/、this→/ðɪs/。失去爆破：museum /mjuːˈziː(ə)m/（m 鼻音）；district /ˈdɪ(s)trɪkt/。浊化/同化/缩读：无典型。",
    },
    177: {
        "fullIpa": "/wɪtʃ ˈɛɡzɪt ʃʊd aɪ teɪk fɔr ðə ˈʃɑpɪŋ mɔl/",
        "variants": [
            ["Which exit should I take for the shopping mall?", "标准"],
            ["What exit is the mall?", "更简"],
            ["Which way out for the mall?", "way out 出口"],
        ],
        "scenes": [
            ["高速/地下车库问", "Which exit should I take for the shopping mall?", "对方回 Exit 12, follow the signs."],
            ["看标牌", "The mall is right at Exit C.", "确认出口编号"],
            ["走错", "You want the next one.", "提醒下一出口"],
        ],
        "grammar": "which exit『哪个出口』；should I take『我该走』（should 比 must/can 更礼貌）。for + 目的地 表『去…（的出口）』。shopping mall 购物中心。",
        "pron": "连读：Which exit→/wɪtʃ ˈɛɡzɪt/（tʃ 与 ɛ）；exit should→/ˈɛɡzɪt ʃʊd/（t 与 ʃ，t 不完全爆破为 /tʃ/ 音）；should I→/ʃʊd aɪ/（d 与 aɪ）；I take→/aɪ teɪk/（aɪ 与 t）；take for→/teɪk fɔr/（k 与 f）；for the→/fɔr ðə/（r 与 ð）；the shopping→/ðə ˈʃɑpɪŋ/（ð 与 ʃ）；shopping mall→/ˈʃɑpɪŋ mɔl/（ŋ 与 m）。弱读：the→/ðə/、should→/ʃʊd/、I→/aɪ/（重读）、for→/fər/。失去爆破：exit /ˈɛɡ(z)ɪt/（z 在 t 前）；should I /ʃʊ(d) aɪ/（d 在 aɪ 前）。浊化/同化/缩读：无典型。",
    },
    178: {
        "fullIpa": "/ɑr ðɛr ɛni ˈlændmɑːrks aɪ ʃʊd lʊk aʊt fɔr/",
        "variants": [
            ["Are there any landmarks I should look out for?", "标准"],
            ["What should I watch for?", "watch for 更口语"],
            ["Any signs I can't miss?", "miss 表『不会错过』"],
        ],
        "scenes": [
            ["问指路的人", "Are there any landmarks I should look out for?", "对方回 The big clock tower."],
            ["导航提示", "Turn when you see the cathedral.", "看见大教堂就转"],
            ["确认", "Is that the one with the blue dome?", "确认特征"],
        ],
        "grammar": "landmark『地标』；look out for『留意/提防』（此处指『注意看』）。any 用于疑问/否定；I should look out for 定语从句修饰 landmarks。",
        "pron": "连读：Are there→/ɑr ðɛr/（r 与 ð）；there any→/ðɛr ˈɛni/（r 与 ɛ）；any landmarks→/ˈɛni ˈlændmɑːrks/（i 与 l）；landmarks I→/ˈlændmɑːrks aɪ/（s 与 aɪ）；I should→/aɪ ʃʊd/（aɪ 与 ʃ）；should look→/ʃʊd lʊk/（d 与 l）；look out→/lʊk aʊt/（k 与 aʊ）；out for→/aʊt fɔr/（t 与 f）。弱读：there→/ðɛr/、any→/ˈɛni/、for→/fər/、are→/ɑr/（重读）。失去爆破：look out /lʊ(k) aʊt/（k 在 aʊ 前）；out for /aʊ(t) fɔr/。同化：无典型。缩读：无典型。",
    },
    179: {
        "fullIpa": "/kæn aɪ wɔk ðɛr bɪˈfɔr dɑrk/",
        "variants": [
            ["Can I walk there before dark?", "标准"],
            ["Can I make it before dark?", "make it 表『赶得及』"],
            ["Is it walkable before sunset?", "walkable 可步行"],
        ],
        "scenes": [
            ["问距离/时间", "Can I walk there before dark?", "对方回 Sure, it's 15 minutes."],
            ["赶时间", "Hurry, the light's going fast.", "天黑得快"],
            ["不行", "Take a bus, it's too far.", "太远建议车"],
        ],
        "grammar": "before dark『天黑前』；dark 此处名词『天黑/夜色』。Can I walk there『我能走到那儿吗』。before + 名词 表『在…之前』。",
        "pron": "连读：Can I→/kæn aɪ/（n 与 aɪ）；I walk→/aɪ wɔk/（aɪ 与 w 滑音）；walk there→/wɔk ðɛr/（k 与 ð）；there before→/ðɛr bɪˈfɔr/（r 与 b）；before dark→/bɪˈfɔr dɑrk/（r 与 d）。弱读：I→/aɪ/（重读）、there→/ðɛr/、before→/bɪˈfɔr/、can→/kən/。失去爆破：walk /wɔ(k)/；before /bɪˈfɔ(r)/。浊化/同化/缩读：无典型。",
    },
    180: {
        "fullIpa": "/aɪd laɪk tə bʊk ə ˈdʌbəl ruːm fɔr tu naɪts/",
        "variants": [
            ["I'd like to book a double room for two nights.", "标准"],
            ["A double for two nights, please.", "极简"],
            ["Can I reserve a double room for two nights?", "reserve 更正式"],
        ],
        "scenes": [
            ["酒店前台", "I'd like to book a double room for two nights.", "对方回 Let me check availability."],
            ["说明床型", "One big bed, not twins.", "大床而非双单床"],
            ["询价", "What's the rate per night?", "问房价"],
        ],
        "grammar": "I'd like to book… = I would like to book… 订房万能句。double room 双人房（一张大床）；for + 时间段『住…』。two nights 两晚。",
        "pron": "同化/缩读：I'd = I would（/aɪd/）。连读：like to→/laɪk tə/（k 与 t）；to book→/tə bʊk/（t 与 b）；book a→/bʊk ə/（k 与 ə）；a double→/ə ˈdʌbəl/；double room→/ˈdʌbəl ruːm/（l 与 r）；room for→/ruːm fɔr/（m 与 f）；for two→/fɔr tu/（r 与 t）；two nights→/tu naɪts/（w 与 n）。浊化：like to 快读 /laɪ də/（t→d）。弱读：to→/tə/、a→/ə/、for→/fər/。失去爆破：double /ˈdʌ(b)əl/；room /ruː(m)/。",
    },
    181: {
        "fullIpa": "/du ju hæv ˈɛniθɪŋ əˈveɪləbəl fɔr təˈnaɪt/",
        "variants": [
            ["Do you have anything available for tonight?", "标准"],
            ["Any rooms left for tonight?", "更简"],
            ["Do you have a room for tonight?", "直接问有没有房"],
        ],
        "scenes": [
            ["无预订直接问", "Do you have anything available for tonight?", "对方回 We have one queen left."],
            ["旺季", "It's fully booked, sorry.", "客满"],
            ["降价", "Last room, slightly discounted.", "最后一间有折扣"],
        ],
        "grammar": "anything available『任何可用的（房）』；for tonight『今晚』。have 实义动词，疑问句借 do。available『可用的/有空的』。",
        "pron": "连读：Do you→/du ju/（可同化 /dʒu/）；you have→/ju hæv/（j 与 h）；have anything→/hæv ˈɛniθɪŋ/（v 与 ɛ）；anything available→/ˈɛniθɪŋ əˈveɪləbəl/（ŋ 与 ə）；available for→/əˈveɪləbəl fɔr/（l 与 f）；for tonight→/fɔr təˈnaɪt/（r 与 t）。同化：Do you→/dʒu/（可选）。弱读：you→/ju/、do→/də/、for→/fər/。失去爆破：anything /ˈɛni(t)θɪŋ/（t 在 θ 前）；available /əˈveɪ(l)əbəl/。缩读：无典型。",
    },
    182: {
        "fullIpa": "/wʌts ðə reɪt fɔr ə ˈsɪŋɡəl ruːm pər naɪt/",
        "variants": [
            ["What's the rate for a single room per night?", "标准"],
            ["How much for a single room?", "最简"],
            ["What's the price per night?", "问每晚价"],
        ],
        "scenes": [
            ["问房价", "What's the rate for a single room per night?", "对方回 $80, tax included."],
            ["含早", "Is breakfast included?", "问含早"],
            ["对比", "Double is only $20 more.", "双人房贵20"],
        ],
        "grammar": "What's = What is 缩读；rate 此处『价格/费率』（= price）。for a single room『单人房』；per night『每晚』（per + 单位）。single room 单人间。",
        "pron": "同化/缩读：What's = What is（/wʌts/）。连读：the rate→/ðə reɪt/（ð 与 r）；rate for→/reɪt fɔr/（t 与 f）；for a→/fɔr ə/（r 与 ə）；a single→/ə ˈsɪŋɡəl/；single room→/ˈsɪŋɡəl ruːm/（l 与 r）；room per→/ruːm pər/（m 与 p）；per night→/pər naɪt/（r 与 n）。弱读：the→/ðə/、for→/fər/、a→/ə/、per→/pər/。失去爆破：rate /reɪ(t)/；single /ˈsɪŋ(ɡ)əl/（ŋ 鼻音）。浊化/同化：无典型。",
    },
    183: {
        "fullIpa": "/ɪz ðɛr ə ˈdɪskaʊnt fɔr ˈsteɪɪŋ ə hoʊl wiːk/",
        "variants": [
            ["Is there a discount for staying a whole week?", "标准"],
            ["Any weekly rate?", "weekly rate 周价"],
            ["Do you offer a long-stay discount?", "long-stay 长住"],
        ],
        "scenes": [
            ["谈长住价", "Is there a discount for staying a whole week?", "对方回 Yes, 10% off for 7 nights."],
            ["按周算", "The weekly rate is cheaper.", "周价更划算"],
            ["会员", "Sign up for free and save.", "注册免费省"],
        ],
        "grammar": "discount 折扣；for + 动名词 staying『对于住…』（for 后接名词/动名词）。a whole week『一整周』。there is 存在句。",
        "pron": "连读：Is there→/ɪz ðɛr/（z 与 ð）；there a→/ðɛr ə/；a discount→/ə ˈdɪskaʊnt/；discount for→/ˈdɪskaʊnt fɔr/（t 与 f）；for staying→/fɔr ˈsteɪɪŋ/（r 与 s）；staying a→/ˈsteɪɪŋ ə/（ŋ 与 ə）；a whole→/ə hoʊl/；whole week→/hoʊl wiːk/（l 与 w）。弱读：there→/ðɛr/、a→/ə/、for→/fər/、is→/ɪz/（重读）。失去爆破：discount /ˈdɪ(s)kaʊnt/；whole /hoʊ(l)/。浊化/同化/缩读：无典型。",
    },
    184: {
        "fullIpa": "/aɪ hæv ə ˌrɛzərˈveɪʃən ˈʌndər ðə neɪm wɑŋ/",
        "variants": [
            ["I have a reservation under the name Wang.", "标准"],
            ["I booked it under Wang.", "更简"],
            ["Reservation for Wang, please.", "前台常用报姓"],
        ],
        "scenes": [
            ["入住报预订", "I have a reservation under the name Wang.", "对方回 Let me pull that up."],
            ["拼错", "That's W-A-N-G, yes.", "确认拼写"],
            ["查找", "Found it, two nights, double.", "调出订单"],
        ],
        "grammar": "reservation 预订；under the name (of)…『以…的名字（登记）』。have a reservation『我有预订』。name 后接具体姓氏。",
        "pron": "连读：have a→/hæv ə/（v 与 ə）；a reservation→/ə ˌrɛzərˈveɪʃən/；reservation under→/ˌrɛzərˈveɪʃən ˈʌndər/（n 与 ʌ）；under the→/ˈʌndər ðə/（r 与 ð）；the name→/ðə neɪm/（ð 与 n）；name Wang→/neɪm wɑŋ/（m 与 w）。弱读：a→/ə/、the→/ðə/、have→/hæv/（重读）。失去爆破：reservation /ˌrɛzərˈveɪʃə(n)/（n 鼻音）；name /neɪ(m)/。浊化/同化/缩读：无典型。",
    },
    185: {
        "fullIpa": "/kʊdʒu ɡɪv mi ə ˈpæspɔːrt fɔr ə ˈmoʊmənt pliːz/",
        "variants": [
            ["Could you show me your passport, please?", "show 比 give 更自然（出示）"],
            ["May I see your passport?", "may 更正式礼貌"],
            ["Passport, please.", "极简"],
        ],
        "scenes": [
            ["入住查证件", "Could you give me a passport for a moment, please?", "对方回 Here you go."],
            ["返还", "Thanks, here's your passport back.", "用完归还"],
            ["替代", "A photo on your phone works too.", "手机照片也可"],
        ],
        "grammar": "give me a passport for a moment『借我看下护照』（for a moment『一下』）。Could you… 礼貌；更地道用 show your passport。passport 护照。",
        "pron": "同化：Could you→/kʊdʒu/（d+j 同化，关键！）。连读：give me→/ɡɪv mi/（v 与 m）；me a→/mi ə/；a passport→/ə ˈpæspɔːrt/；passport for→/ˈpæspɔːrt fɔr/（t 与 f）；for a→/fɔr ə/；a moment→/ə ˈmoʊmənt/；moment please→/ˈmoʊmənt pliːz/。弱读：me→/mi/、a→/ə/、for→/fər/。失去爆破：passport /ˈpæ(s)pɔːrt/；moment /ˈmoʊ(m)ənt/。缩读：无典型。",
    },
    186: {
        "fullIpa": "/wʌt taɪm ɪz ˈtʃɛk ɪn ˈjuːʒuəli/",
        "variants": [
            ["What time is check-in usually?", "标准"],
            ["When can I check in?", "问最早几点"],
            ["What's the earliest check-in?", "问最早"],
        ],
        "scenes": [
            ["问入住时间", "What time is check-in usually?", "对方回 From 3 PM."],
            ["早到", "Can I drop my bags early?", "早到先寄包"],
            ["提前", "Your room's ready now.", "房已好"],
        ],
        "grammar": "check-in 名词『入住/办理入住的时间』（动词短语 check in）。What time 问具体时刻；usually『通常』。is 提前到疑问词后。",
        "pron": "连读：What time→/wʌt taɪm/（t 与 t 只读一次）；time is→/taɪm ɪz/（m 与 ɪ）；is check→/ɪz tʃɛk/（z 与 tʃ）；check in→/tʃɛk ɪn/（k 与 ɪ）；in usually→/ɪn ˈjuːʒuəli/（n 与 j）。弱读：is→/ɪz/（重读）、in→/ɪn/。失去爆破：check /tʃɛ(k)/；time /taɪ(m)/。同化/滑音：in usually 加 j 滑音。浊化/缩读：无典型。",
    },
    187: {
        "fullIpa": "/kʊdʒu liːv maɪ ˈlʌɡɪdʒ hɪr ənˈtɪl ðə ruːm ɪz ˈrɛdi/",
        "variants": [
            ["Could you leave my luggage here until the room is ready?", "标准"],
            ["Can I store my bags here?", "store 寄存"],
            ["Keep my luggage till check-in?", "更简"],
        ],
        "scenes": [
            ["早到寄行李", "Could you leave my luggage here until the room is ready?", "对方回 Sure, we'll tag it."],
            ["拿回", "I'll come back at three.", "三点来取"],
            ["贵重", "Is it safe?", "问安全"],
        ],
        "grammar": "leave my luggage here『把行李留这儿』；until + 从句『直到…』。the room is ready『房间准备好』。Could you… 礼貌请求寄存。",
        "pron": "同化：Could you→/kʊdʒu/（d+j 同化，关键！）。连读：leave my→/liːv maɪ/（v 与 m）；my luggage→/maɪ ˈlʌɡɪdʒ/（aɪ 与 l）；luggage here→/ˈlʌɡɪdʒ hɪr/（dʒ 与 h）；here until→/hɪr ənˈtɪl/（r 与 ə）；until the→/ənˈtɪl ðə/（l 与 ð）；the room→/ðə ruːm/；room is→/ruːm ɪz/（m 与 ɪ）；is ready→/ɪz ˈrɛdi/。弱读：my→/maɪ/、the→/ðə/、is→/ɪz/、until→/ənˈtɪl/。失去爆破：luggage /ˈlʌɡɪ(d)ʒ/；room /ruː(m)/。缩读：无典型。",
    },
    188: {
        "fullIpa": "/aɪm ˈtʃɛkɪŋ aʊt təˈdeɪ ənd ˈwʊd laɪk tə ˈsɛtəl maɪ bɪl/",
        "variants": [
            ["I'm checking out today and would like to settle my bill.", "标准"],
            ["I'd like to check out and pay my bill.", "pay my bill 更口语"],
            ["Can I settle the bill now?", "问现在结账"],
        ],
        "scenes": [
            ["退房结账", "I'm checking out today and would like to settle my bill.", "对方回 Sure, let me print it."],
            ["对账", "Did I get charged for minibar?", "问迷你吧"],
            ["付款", "Card or cash?", "问支付方式"],
        ],
        "grammar": "check out 短语『退房』；would like to settle my bill『想结账/结清账单』。I'm = I am 缩读（现在进行时表当前动作）。and 连接并列。",
        "pron": "同化/缩读：I'm = I am（/aɪm/）；would→/wʊd/。连读：checking out→/ˈtʃɛkɪŋ aʊt/（ŋ 与 aʊ）；out today→/aʊt təˈdeɪ/（t 与 t）；today and→/təˈdeɪ ənd/（d 与 ə）；and would→/ənd wʊd/（d 与 w）；would like→/wʊd laɪk/（d 与 l）；like to→/laɪk tə/；to settle→/tə ˈsɛtəl/；settle my→/ˈsɛtəl maɪ/；my bill→/maɪ bɪl/。弱读：to→/tə/、and→/ənd/、my→/maɪ/。失去爆破：checking /ˈtʃɛ(k)ɪŋ/；settle /ˈsɛ(t)əl/。浊化：like to 快读 /laɪ də/（t→d）。",
    },
    189: {
        "fullIpa": "/wʌt taɪm du wi hæv tə ˈtʃɛk aʊt baɪ/",
        "variants": [
            ["What time do we have to check out by?", "标准"],
            ["When's checkout?", "最简"],
            ["Is late checkout okay?", "问可否晚退"],
        ],
        "scenes": [
            ["问最晚退房", "What time do we have to check out by?", "对方回 By noon, please."],
            ["申请晚退", "Can we stay till 2?", "问延到两点"],
            ["续住", "We'd like to extend one night.", "想多住一晚"],
        ],
        "grammar": "have to『必须』；by + 时间『在…之前（截止）』。check out by『最晚几点前退房』。do we have to… 疑问借助 do。",
        "pron": "连读：What time→/wʌt taɪm/（t 与 t）；time do→/taɪm du/（m 与 d）；do we→/du wi/（w 顺接）；we have→/wi hæv/（w 与 h）；have to→/hæf tə/（v 与 t，have 此处弱读 /hæf/ 或 /həv/）；to check→/tə tʃɛk/；check out→/tʃɛk aʊt/；out by→/aʊt baɪ/（t 与 b）。同化/浊化：have to→/hæftə/（v+t 连读，常见弱化）。弱读：do→/də/、we→/wi/、to→/tə/、by→/baɪ/（重读）。失去爆破：check /tʃɛ(k)/；out /aʊ(t)/。缩读：无典型。",
    },
    190: {
        "fullIpa": "/kʊdʒu ɡɪv mi ə rɪˈsiːt fɔr ðə ˈpeɪmənt/",
        "variants": [
            ["Could you give me a receipt for the payment?", "标准"],
            ["Can I get a receipt?", "最简"],
            ["I need a receipt, please.", "直接要"],
        ],
        "scenes": [
            ["付款后索要", "Could you give me a receipt for the payment?", "对方回 Sure, emailed or printed?"],
            ["报销", "I need it for expenses.", "说明用途"],
            ["电子", "Send it to my email.", "发邮件"],
        ],
        "grammar": "receipt 收据（注意 c 不发音，读 /rɪˈsiːt/）；for the payment『针对这笔付款』。Could you give me… 礼貌索取。",
        "pron": "同化：Could you→/kʊdʒu/（d+j 同化，关键！）。连读：give me→/ɡɪv mi/（v 与 m）；me a→/mi ə/；a receipt→/ə rɪˈsiːt/；receipt for→/rɪˈsiːt fɔr/（t 与 f）；for the→/fɔr ðə/；the payment→/ðə ˈpeɪmənt/（ð 与 p）。弱读：me→/mi/、a→/ə/、for→/fər/、the→/ðə/。失去爆破：receipt /rɪˈsiː(t)/；payment /ˈpeɪmənt/（m 鼻音）。缩读：无典型。",
    },
    191: {
        "fullIpa": "/ɪz ðɛr ə leɪt ˈtʃɛk aʊt ˈɑpʃən əˈveɪləbəl/",
        "variants": [
            ["Is there a late check-out option available?", "标准"],
            ["Can I check out late?", "最简"],
            ["Do you offer late checkout?", "问是否提供"],
        ],
        "scenes": [
            ["申请晚退", "Is there a late check-out option available?", "对方回 Until 2 PM, no charge."],
            ["收费", "It's $20 for late checkout.", "晚退收费"],
            ["会员免", "Free for members.", "会员免费"],
        ],
        "grammar": "late check-out『延迟退房』；option『选项/服务』；available『可用的』。there is 存在句。check-out 复合名词作定语。",
        "pron": "连读：Is there→/ɪz ðɛr/（z 与 ð）；there a→/ðɛr ə/；a late→/ə leɪt/（l 与 l 不连读，a 弱读）；late check→/leɪt tʃɛk/（t 与 tʃ）；check out→/tʃɛk aʊt/；out option→/aʊt ˈɑpʃən/（t 与 ɑ）；option available→/ˈɑpʃən əˈveɪləbəl/（n 与 ə）。弱读：there→/ðɛr/、a→/ə/、is→/ɪz/（重读）。失去爆破：late /leɪ(t)/；check /tʃɛ(k)/；out /aʊ(t)/。浊化/同化/缩读：无典型。",
    },
    192: {
        "fullIpa": "/kʊdʒu hæv ə ˈweɪk ʌp kɔːl æt sɪks təˈmɑroʊ/",
        "variants": [
            ["Could you give me a wake-up call at six tomorrow?", "give me 比 have 更直接"],
            ["Wake-up call at six, please.", "极简"],
            ["Can I get a morning call at 6?", "morning call 同义"],
        ],
        "scenes": [
            ["前台要叫醒", "Could you have a wake-up call at six tomorrow?", "对方回 Sure, six AM."],
            ["确认", "Six in the morning, right?", "确认上午六点"],
            ["手机替代", "I'll just set an alarm.", "自己设闹钟"],
        ],
        "grammar": "wake-up call『叫醒电话/服务』；at + 时刻 six；tomorrow『明天』。Could you have… 表请求安排。have a call『安排一个电话』。",
        "pron": "同化：Could you→/kʊdʒu/（d+j 同化，关键！）。连读：have a→/hæv ə/（v 与 ə）；a wake→/ə weɪk/（w 顺接）；wake up→/weɪk ʌp/（k 与 ʌ）；up call→/ʌp kɔːl/（p 与 k）；call at→/kɔːl æt/（l 与 æ）；at six→/æt sɪks/（t 与 s，t 不完全爆破）；six tomorrow→/sɪks təˈmɑroʊ/（s 与 t）。弱读：a→/ə/、have→/hæv/（重读）、at→/æt/。失去爆破：wake /weɪ(k)/；up /ʌ(p)/；six /sɪ(k)s/。浊化/缩读：无典型。",
    },
    193: {
        "fullIpa": "/ðə ɛr kənˈdɪʃənər ɪn maɪ ruːm ˈɪznt ˈwɜːrkɪŋ/",
        "variants": [
            ["The air conditioner in my room isn't working.", "标准"],
            ["My AC is broken.", "AC = air conditioner 口语"],
            ["The A/C doesn't work.", "doesn't work 更口语"],
        ],
        "scenes": [
            ["报修", "The air conditioner in my room isn't working.", "对方回 I'll send someone up."],
            ["换房", "Can we switch rooms?", "问换房"],
            ["临时", "A fan for now?", "先给风扇"],
        ],
        "grammar": "air conditioner 空调（口语 AC /ˌeɪˈsiː/ 或 A/C）。isn't working『不工作/坏了』（现在进行时表当前状态）；my room『我房间』。in my room 介词短语作定语。",
        "pron": "连读：The air→/ðə ɛr/（ð 与 ɛ）；air conditioner→/ɛr kənˈdɪʃənər/（r 与 k）；conditioner in→/kənˈdɪʃənər ɪn/（r 与 ɪ）；in my→/ɪn maɪ/（n 与 aɪ）；my room→/maɪ ruːm/；room isn't→/ruːm ˈɪznt/（m 与 ɪ）；isn't working→/ˈɪznt ˈwɜːrkɪŋ/（t 与 w）。弱读：the→/ðə/、in→/ɪn/、my→/maɪ/。失去爆破：conditioner /kənˈdɪʃə(n)ər/；room /ruː(m)/。同化/浊化/缩读：无典型。",
    },
    194: {
        "fullIpa": "/ðɛr z noʊ hɑt ˈwɔːtər ðɪs ˈmɔrnɪŋ/",
        "variants": [
            ["There's no hot water this morning.", "标准"],
            ["We have no hot water.", "更直白"],
            ["The water isn't hot.", "问法不同"],
        ],
        "scenes": [
            ["向前台反映", "There's no hot water this morning.", "对方回 Sorry, we'll check the boiler."],
            ["临时", "Cold shower for now.", "先用冷水"],
            ["解决", "It's fixed, try again.", "已修好"],
        ],
        "grammar": "There's = There is 缩读；no hot water『没有热水』。this morning『今早』。there be 存在句表『有/没有』。",
        "pron": "同化/缩读：There's = There is（/ðɛrz/）。连读：no hot→/noʊ hɑt/（w 与 h）；hot water→/hɑt ˈwɔːtər/（t 与 w）；water this→/ˈwɔːtər ðɪs/（r 与 ð）；this morning→/ðɪs ˈmɔrnɪŋ/（s 与 m）。弱读：no→/noʊ/、this→/ðɪs/、morning→/ˈmɔrnɪŋ/。失去爆破：hot /hɑ(t)/（t 在 w 前不完全爆破 /hɑwɔːtər/）；water /ˈwɔː(t)ər/。浊化：hot water 快读 /hɑ dɔːtər/（t→d）。",
    },
    195: {
        "fullIpa": "/kʊd ˈsʌmwʌn teɪk ə lʊk æt ðə ˈʃaʊər/",
        "variants": [
            ["Could someone take a look at the shower?", "标准"],
            ["Can you check the shower?", "更直白"],
            ["The shower's acting up.", "acting up 表『出毛病』"],
        ],
        "scenes": [
            ["报修淋浴", "Could someone take a look at the shower?", "对方回 Maintenance is on the way."],
            ["堵了", "It's clogged.", "堵住"],
            ["水温", "No hot water from it.", "没热水"],
        ],
        "grammar": "someone『某人』；take a look at…『看一下…』；the shower 淋浴。Could someone… 礼貌请求派人查看。",
        "pron": "连读：Could someone→/kʊd ˈsʌmwʌn/（d 与 s）；someone take→/ˈsʌmwʌn teɪk/（n 与 t）；take a→/teɪk ə/；a look→/ə lʊk/；look at→/lʊk æt/（k 与 æ）；at the→/æt ðə/（t 与 ð）；the shower→/ðə ˈʃaʊər/（ð 与 ʃ）。弱读：a→/ə/、at→/æt/、the→/ðə/、could→/kʊd/（重读）。失去爆破：look /lʊ(k)/；at /æ(t)/。浊化/同化/缩读：无典型。",
    },
    196: {
        "fullIpa": "/kʊdʒu brɪŋ ən ˈɛkstrə ˈblæŋkɪt tə ruːm θri oʊ faɪv/",
        "variants": [
            ["Could you bring an extra blanket to room three oh five?", "标准"],
            ["Can I get an extra blanket?", "最简"],
            ["We need another blanket, please.", "another 也行"],
        ],
        "scenes": [
            ["要毯子", "Could you bring an extra blanket to room three oh five?", "对方回 Sure, right away."],
            ["多要", "Two blankets, actually.", "要两条"],
            ["确认房号", "That's 305, yes.", "确认305"],
        ],
        "grammar": "extra blanket『额外毯子』；bring…to + 房号。three oh five = 305（英文房号读法 3-0-5）。Could you bring… 礼貌请求送物。",
        "pron": "同化：Could you→/kʊdʒu/（d+j 同化，关键！）。连读：bring an→/brɪŋ ən/（ŋ 与 ə）；an extra→/ən ˈɛkstrə/（n 与 ɛ）；extra blanket→/ˈɛkstrə ˈblæŋkɪt/（ə 与 b）；blanket to→/ˈblæŋkɪt tə/（t 与 t）；to room→/tə ruːm/（t 与 r）；room three→/ruːm θri/（m 与 θ）；three oh→/θri oʊ/（r 与 oʊ）；oh five→/oʊ faɪv/。弱读：an→/ən/、to→/tə/。失去爆破：blanket /ˈblæŋ(k)ɪt/；room /ruː(m)/。缩读：无典型。",
    },
    197: {
        "fullIpa": "/ɪz ruːm ˈsɜːrvɪs əˈveɪləbəl əˈraʊnd ðə ˈklɑk/",
        "variants": [
            ["Is room service available around the clock?", "标准"],
            ["Do you do 24-hour room service?", "24-hour 更口语"],
            ["Can I order food to the room?", "问送餐到房"],
        ],
        "scenes": [
            ["问客房送餐", "Is room service available around the clock?", "对方回 Yes, till midnight."],
            ["深夜", "I'd like a late-night snack.", "深夜小吃"],
            ["菜单", "What's on the menu?", "问有啥"],
        ],
        "grammar": "room service『客房送餐/服务』；around the clock『全天候/24小时』；available『可用的』。there is / is 系表结构。",
        "pron": "连读：Is room→/ɪz ruːm/（z 与 r）；room service→/ruːm ˈsɜːrvɪs/（m 与 s）；service available→/ˈsɜːrvɪs əˈveɪləbəl/（s 与 ə）；available around→/əˈveɪləbəl əˈraʊnd/（l 与 ə）；around the→/əˈraʊnd ðə/（d 与 ð）；the clock→/ðə klɑk/（ð 与 k）。弱读：is→/ɪz/（重读）、the→/ðə/、around→/əˈraʊnd/。失去爆破：service /ˈsɜːr(v)ɪs/；clock /klɑ(k)/。浊化/同化/缩读：无典型。",
    },
    198: {
        "fullIpa": "/kʊdʒu hæv maɪ suːt draɪ kliːnd baɪ təˈmɑroʊ/",
        "variants": [
            ["Could you have my suit dry-cleaned by tomorrow?", "标准"],
            ["Can you dry-clean this suit?", "更直白"],
            ["I need this suit cleaned by tomorrow.", "cleaned 也可"],
        ],
        "scenes": [
            ["送洗西装", "Could you have my suit dry-cleaned by tomorrow?", "对方回 Sure, before noon."],
            ["急件", "It's urgent, for a meeting.", "开会急用"],
            ["取回", "Deliver it to my room.", "送回房间"],
        ],
        "grammar": "have + 宾语 + 过去分词『让（别人）把…做好』（使役结构）；dry-cleaned 过去分词『干洗』。by tomorrow『明早前』。suit 西装。",
        "pron": "同化：Could you→/kʊdʒu/（d+j 同化，关键！）。连读：have my→/hæv maɪ/（v 与 aɪ）；my suit→/maɪ suːt/（aɪ 与 s）；suit dry→/suːt draɪ/（t 与 d）；dry cleaned→/draɪ kliːnd/（w 与 k，加 w 滑音）；cleaned by→/kliːnd baɪ/（d 与 b）；by tomorrow→/baɪ təˈmɑroʊ/（b 与 t）。弱读：my→/maɪ/、by→/baɪ/（重读）、have→/hæv/。失去爆破：suit /suː(t)/；cleaned /kliːn(d)/。浊化：suit dry /suː ddraɪ/（t→d）。",
    },
    199: {
        "fullIpa": "/ðə ruːm nɛkst dɔr ɪz tuː ˈnɔɪzi æt naɪt/",
        "variants": [
            ["The room next door is too noisy at night.", "标准"],
            ["My neighbors are loud.", "neighbors 更口语"],
            ["It's noisy next door.", "最简"],
        ],
        "scenes": [
            ["投诉噪音", "The room next door is too noisy at night.", "对方回 Sorry, I'll talk to them."],
            ["换房", "Can we move rooms?", "问换房"],
            ["缓解", "A pair of earplugs?", "给耳塞"],
        ],
        "grammar": "next door『隔壁』作后置定语修饰 room；too noisy『太吵』；at night『在夜里』。the room (that is) next door 省略关系从句。",
        "pron": "连读：The room→/ðə ruːm/（ð 与 r）；room next→/ruːm nɛkst/（m 与 n）；next door→/nɛkst dɔr/（t 与 d，不完全爆破）；door is→/dɔr ɪz/（r 与 ɪ）；is too→/ɪz tuː/（z 与 t）；too noisy→/tuː ˈnɔɪzi/（w 与 n）；noisy at→/ˈnɔɪzi æt/（i 与 æ）；at night→/æt naɪt/（t 与 n）。弱读：the→/ðə/、is→/ɪz/、at→/æt/。失去爆破：next /nɛ(k)st/；door /dɔ(r)/；night /naɪ(t)/。浊化：next door 快读 /nɛk dɔr/（t→d）。",
    },
    200: {
        "fullIpa": "/wʊd ɪt bi pəˈsɪbəl tə muːv tə ə ˈkwaɪətər ruːm/",
        "variants": [
            ["Would it be possible to move to a quieter room?", "标准，很礼貌"],
            ["Can I change to a quieter room?", "change 更口语"],
            ["Is a quiet room available?", "直接问安静房"],
        ],
        "scenes": [
            ["请求换房", "Would it be possible to move to a quieter room?", "对方回 Of course, we have one."],
            ["说明原因", "The one next door is loud.", "隔壁吵"],
            ["确认", "Same rate, right?", "问同价"],
        ],
        "grammar": "Would it be possible to…『能否…』极礼貌请求；move to…『搬/换到…』。a quieter room『更安静的房间』（quiet 比较级 quieter，双写 t + er）。",
        "pron": "连读：Would it→/wʊd ɪt/（d 与 ɪ，可同化 /wʊ dɪt/）；it be→/ɪt bi/（t 与 b）；be possible→/bi pəˈsɪbəl/（b 与 p）；possible to→/pəˈsɪbəl tə/（l 与 t）；to move→/tə muːv/；move to→/muːv tə/（v 与 t）；to a→/tə ə/；a quieter→/ə ˈkwaɪətər/；quieter room→/ˈkwaɪətər ruːm/（r 与 r）。同化：Would it→/wʊdʒɪt/（d+j 同化，可选）。弱读：it→/ɪt/、to→/tə/、a→/ə/、be→/bi/。失去爆破：possible /pəˈsɪ(b)əl/；move /muː(v)/；quieter /ˈkwaɪə(t)ər/。浊化/缩读：无典型。",
    },
}
