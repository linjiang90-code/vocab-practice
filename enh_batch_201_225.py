# -*- coding: utf-8 -*-
"""ENH 标注批次 201-225（Day91=2026-11-12 解锁的 201-250 前半段，酒店延伸+餐厅点餐）。
结构：fullIpa / variants / scenes / grammar / pron，与 151-200 同格式。
由 enh_merge.py 幂等合并进 master.json（仅 enh.fullIpa 为空时写入）。
"""
ENH = {
    201: {
        "fullIpa": "/ðə vjuː frʌm ðɪs ruːm ɪz əˈmeɪzɪŋ/",
        "variants": [
            ["The view from this room is amazing.", "标准"],
            ["What a view!", "感叹式，更口语"],
            ["The view here is stunning.", "stunning 比 amazing 更书面"],
        ],
        "scenes": [
            ["入住后感叹", "The view from this room is amazing.", "对方回 Glad you like it."],
            ["拍照分享", "Check out this view!", "发照片给朋友"],
            ["请求换房", "Could I get a room with a better view?", "想换海景/城景房"],
        ],
        "grammar": "view 景色，from this room『从这个房间（看出去）』。amazing 令人惊叹；同类词：breathtaking / stunning / spectacular。",
        "pron": "连读：The view→/ðə vjuː/；view from→/vjuː frʌm/；from this→/frʌm ðɪs/；this room→/ðɪs ruːm/；room is→/ruː mɪz/（m 与 ɪ 连读）；is amazing→/ɪ zəˈmeɪzɪŋ/。弱读：The→/ðə/、from→/frʌm/、is→/ɪz/。失去爆破/同化/浊化/缩读：无典型。",
    },
    202: {
        "fullIpa": "/dʌz ðə ruːm kʌm wɪð ə seɪf fɔr ˈvæljuəbəlz/",
        "variants": [
            ["Does the room come with a safe for valuables?", "标准"],
            ["Is there a safe in the room?", "更简"],
            ["Can I get a safety deposit box?", "前台保管箱说法"],
        ],
        "scenes": [
            ["入住时问", "Does the room come with a safe for valuables?", "对方回 Yes, it's in the closet."],
            ["贵重物品寄存", "Can I leave my passport at the front desk?", "寄存前台"],
            ["保险箱打不开", "The safe won't open. Could someone help?", "叫人修"],
        ],
        "grammar": "come with…『自带/配有…』（房间设施万能句式）。safe 此处名词『保险箱』（形容词安全是 safe，重音不同语境区分）。valuables 贵重物品（形容词变名词，定冠词泛指一类）。",
        "pron": "连读：Does the→/dʌz ðə/；room come→/ruːm kʌm/；come with→/kʌm wɪð/；with a→/wɪð ə/；a safe→/ə seɪf/；safe for→/seɪ f fɔr/；for valuables→/fər ˈvæljuəbəlz/。弱读：the→/ðə/、a→/ə/、for→/fər/、does→/dʌz/。失去爆破：valuables /ˈvæljuə(b)əlz/。同化/浊化/缩读：无典型。",
    },
    203: {
        "fullIpa": "/ɪz ðə ˈmɪnibɑːr ɪnˈkluːdɪd ɪn ðə ruːm reɪt/",
        "variants": [
            ["Is the minibar included in the room rate?", "标准"],
            ["Is the minibar free?", "更直接"],
            ["Do I have to pay for the minibar?", "确认是否收费"],
        ],
        "scenes": [
            ["入住确认", "Is the minibar included in the room rate?", "对方回 No, items are charged separately."],
            ["退房争议", "I didn't touch the minibar.", "声明没动过迷你吧"],
            ["问计价", "How much is a bottle of water from the minibar?", "问单品价"],
        ],
        "grammar": "included in…『包含在…里』（be included in 固定搭配）。room rate 房价。minibar 迷你酒吧（复合名词，重音在前）。",
        "pron": "连读：Is the→/ɪz ðə/；minibar included→/ˈmɪnibɑː rɪnˈkluːdɪd/（r 与 ɪ 连读）；included in→/ɪnˈkluː dɪdɪn/（d 与 ɪ）；in the→/ɪn ðə/；the room→/ðə ruːm/；room rate→/ruːm reɪt/。弱读：the→/ðə/、in→/ɪn/。同化：included /ɪnˈkluːdɪd/ 中 n 在 k 前可为 ŋ 音。浊化/缩读：无典型。",
    },
    204: {
        "fullIpa": "/kʊd aɪ ɡɛt ə spɛr ki kɑːrd fɔr maɪ ˈpɑːrtnər/",
        "variants": [
            ["Could I get a spare key card for my partner?", "标准"],
            ["Can we have two key cards?", "直接要两张"],
            ["Could you make another key card for us?", "请再制作一张"],
        ],
        "scenes": [
            ["入住时", "Could I get a spare key card for my partner?", "对方回 Sure, how many cards?"],
            ["房卡消磁", "My key card stopped working.", "重新做卡"],
            ["同伴晚到", "My friend will arrive later — can he check in with this?", "问代取卡"],
        ],
        "grammar": "spare『备用的』（形容词）。key card 房卡。Could I get… 比 Can I have… 更委婉，要东西万能句。",
        "pron": "同化/缩读：无典型。连读：Could I→/kʊ d aɪ/（d 与 aɪ）；get a→/ɡɛ tə/；a spare→/ə spɛr/；spare key→/spɛr ki/；key card→/ki kɑːrd/；card for→/kɑːr d fɔr/；for my→/fər maɪ/；my partner→/maɪ ˈpɑːrtnər/。弱读：for→/fər/、a→/ə/。失去爆破：get /ɡɛ(t)/ 在 a 前；spare /spɛ(r)/。",
    },
    205: {
        "fullIpa": "/aɪd laɪk tʊ ɪkˈstɛnd maɪ steɪ fɔr tu mɔr naɪts/",
        "variants": [
            ["I'd like to extend my stay for two more nights.", "标准"],
            ["Can I extend my stay by two nights?", "by + 数量"],
            ["Is it possible to stay two extra nights?", "extra nights 更口语"],
        ],
        "scenes": [
            ["前台续住", "I'd like to extend my stay for two more nights.", "对方回 Let me check availability."],
            ["房间没空", "I'm sorry, we're fully booked. I can move you to a sister hotel.", "满房调店"],
            ["涨价确认", "Will the rate be the same?", "确认续房价"],
        ],
        "grammar": "extend my stay『延长住宿』固定搭配；extend v. 延长（续签合同也用它）。for + 数量 + more + 名词『再多…』= 多住两晚。",
        "pron": "同化/缩读：I'd = I would（/aɪd/）。连读：like to→/laɪk tə/；to extend→/tʊ ɪkˈstɛnd/；extend my→/ɪkˈstɛn(d) maɪ/；my stay→/maɪ steɪ/；stay for→/steɪ fər/；for two→/fər tu/；two more→/tu mɔr/；more nights→/mɔr naɪts/。弱读：to→/tə/、for→/fər/。失去爆破：extend /ɪkˈstɛn(d)/。",
    },
    206: {
        "fullIpa": "/ɪz ðə ruːm reɪt ðə seɪm ɪf aɪ steɪ ˈlɔːŋɡər/",
        "variants": [
            ["Is the room rate the same if I stay longer?", "标准"],
            ["Does the price change if I stay longer?", "价格变不变"],
            ["Any discount for a longer stay?", "长住有无折扣"],
        ],
        "scenes": [
            ["续住问价", "Is the room rate the same if I stay longer?", "对方回 Long stays get 10% off."],
            ["还价", "What's your best rate for a week?", "问周价"],
            ["确认含早", "Does that include breakfast?", "确认含早"],
        ],
        "grammar": "the same『一样的』；if 引导条件从句。rate 价格/费率；stay longer 待更久（stay 动词）。",
        "pron": "连读：Is the→/ɪz ðə/；room rate→/ruːm reɪt/；rate the→/reɪ(t) ðə/；the same→/ðə seɪm/；same if→/seɪ mɪf/（m 与 ɪ 连读）；if I→/ɪ faɪ/；I stay→/aɪ steɪ/；stay longer→/steɪ ˈlɔːŋɡər/。弱读：the→/ðə/、if→/ɪf/。失去爆破：rate /reɪ(t)/；same /seɪ(m)/。同化/浊化/缩读：无典型。",
    },
    207: {
        "fullIpa": "/duː juː ˈɔfər ˈɛrpɔːrt ˈpɪkʌp fɔr ɡɛsts/",
        "variants": [
            ["Do you offer airport pickup for guests?", "标准"],
            ["Is there an airport shuttle?", "shuttle 摆渡车，酒店常用"],
            ["Can you arrange a pickup from the airport?", "请酒店安排"],
        ],
        "scenes": [
            ["订房时问", "Do you offer airport pickup for guests?", "对方回 Yes, it's 200 yuan per trip."],
            ["免费班车", "Is the shuttle free? What's the schedule?", "问班车时刻"],
            ["报航班号", "My flight is CZ3456, landing at 14:30.", "预约接机"],
        ],
        "grammar": "offer + 名词『提供…』。pickup 接载（名词，重音在前 /ˈpɪkʌp/；动词 pick up 重音在后）。for guests 为住客提供。",
        "pron": "连读：Do you→/duː ju/（常缩读 /dʒə/）；offer airport→/ˈɔfər ˈɛrpɔːrt/；airport pickup→/ˈɛrpɔːrt ˈpɪkʌp/；pickup for→/ˈpɪkʌ p fər/；for guests→/fər ɡɛsts/。弱读：for→/fər/。缩读：Do you→/djə/（常见口语缩读）。失去爆破：airport /ˈɛrpɔː(r)t/。",
    },
    208: {
        "fullIpa": "/ɪz ˈbrɛkfəst sɜrvd ɪn ðə ˈlɑbi ɔr ɪn ðə ˈrɛstrɑnt/",
        "variants": [
            ["Is breakfast served in the lobby or in the restaurant?", "标准"],
            ["Where is breakfast served?", "更简"],
            ["Which floor is breakfast on?", "问楼层"],
        ],
        "scenes": [
            ["前台问", "Is breakfast served in the lobby or in the restaurant?", "对方回 In the restaurant, on the second floor."],
            ["找位置", "Could you show me where the restaurant is?", "请人指路"],
            ["打包", "Can I get breakfast to go?", "问能否外带"],
        ],
        "grammar": "is served 被动语态『被供应』（服务场景高频句式）。or 连接选择疑问。lobby 大堂；restaurant 餐厅。",
        "pron": "连读：Is breakfast→/ɪz ˈbrɛkfəst/；breakfast served→/ˈbrɛkfəs(t) sɜrvd/（t 与 s 相邻，前 t 失去爆破）；served in→/sɜrv dɪn/（d 与 ɪ）；in the→/ɪn ðə/；lobby or→/ˈlɑ bi ɔr/；or in→/ɔr ɪn/；in the restaurant→/ɪn ðə ˈrɛstrɑnt/。弱读：the→/ðə/、in→/ɪn/、or→/ər/。失去爆破：breakfast /ˈbrɛk(f)əst/。",
    },
    209: {
        "fullIpa": "/wʌt taɪm dʌz ˈbrɛkfəst stɑːrt ɪn ðə ˈmɔrnɪŋ/",
        "variants": [
            ["What time does breakfast start in the morning?", "标准"],
            ["When does breakfast start?", "when 更简"],
            ["What are your breakfast hours?", "问时段更地道"],
        ],
        "scenes": [
            ["前台问", "What time does breakfast start in the morning?", "对方回 From 6:30 to 10:00."],
            ["赶早班机", "Can I get breakfast earlier? My flight is at 7.", "问能否提前"],
            ["最后时间", "Until what time is it served?", "问截止"],
        ],
        "grammar": "What time does + 主语 + 动词原形…? 问具体时刻。start 开始（不及物）；in the morning 泛指早上。",
        "pron": "连读：What time→/wʌ(t) taɪm/（t 与 t 重叠，只读一次）；does breakfast→/dʌz ˈbrɛkfəst/；breakfast start→/ˈbrɛkfəs(t) stɑːrt/；start in→/stɑːr tɪn/；in the→/ɪn ðə/；the morning→/ðə ˈmɔrnɪŋ/。弱读：does→/dəz/、in the→/ɪn ðə/。失去爆破：What /wʌ(t)/；breakfast /ˈbrɛk(f)əst/。同化/浊化/缩读：无典型。",
    },
    210: {
        "fullIpa": "/kʊd juː ˌrɛkəˈmɛnd ə ˈloʊkəl dɪʃ wɜrθ ˈtraɪɪŋ/",
        "variants": [
            ["Could you recommend a local dish worth trying?", "标准"],
            ["What's a must-try local dish?", "must-try 更口语"],
            ["Any local food you'd suggest?", "更随意"],
        ],
        "scenes": [
            ["问前台/店员", "Could you recommend a local dish worth trying?", "对方回 Try the hotpot — it's famous here."],
            ["问店", "Where can I get authentic local food?", "问哪家店正宗"],
            ["怕辣确认", "Is it very spicy? I'm not good with spicy food.", "确认口味"],
        ],
        "grammar": "recommend + 名词『推荐…』。worth + doing『值得做…』（worth trying，固定用法，worth 后接动名词）。local dish 本地菜。",
        "pron": "连读：Could you→/kʊ dʒu/（d+j 同化为 dʒ）；recommend a→/ˌrɛkəˈmɛn də/；a local→/ə ˈloʊkəl/；local dish→/ˈloʊkəl dɪʃ/；dish worth→/dɪʃ wɜrθ/；worth trying→/wɜrθ ˈtraɪɪŋ/。弱读：a→/ə/、you→/ju/。同化：Could you→/kʊdʒu/（关键！d+j→dʒ）。失去爆破/浊化/缩读：无典型。",
    },
    211: {
        "fullIpa": "/duː juː hæv ˈɛni ˈteɪbəlz friː fɔr tuː təˈnaɪt/",
        "variants": [
            ["Do you have any tables free for two tonight?", "标准"],
            ["Is there a table for two available tonight?", "available 更正式"],
            ["Got a table for two tonight?", "美式口语极简"],
        ],
        "scenes": [
            ["进店问位", "Do you have any tables free for two tonight?", "对方回 Yes, right this way."],
            ["满座等位", "It's about a 20-minute wait.", "等位 20 分钟"],
            ["没订位", "Do you take walk-ins?", "问能否不预约直接吃"],
        ],
        "grammar": "tables free『空着的桌子』（形容词后置修饰）。for two『两位的』。any 用于疑问句表『有没有一些』。",
        "pron": "连读：Do you→/dʒə/（缩读）；have any→/hæ vəˈni/（v 与 ə）；any tables→/ˈɛni ˈteɪbəlz/；tables free→/ˈteɪbəlz friː/；free for→/friː fər/；for two→/fər tu/；two tonight→/tu təˈnaɪt/（t 与 t 重叠只读一次）。弱读：for→/fər/。同化/浊化/失去爆破：无典型。缩读：Do you→/dʒə/。",
    },
    212: {
        "fullIpa": "/aɪd laɪk tə meɪk ə ˌrɛzərˈveɪʃən fɔr sɪks æt ˈsɛvən piː ɛm/",
        "variants": [
            ["I'd like to make a reservation for six at seven p.m.", "标准"],
            ["A table for six at 7 tonight, please.", "极简"],
            ["Can I book a table for six at seven?", "book 比 make a reservation 随意"],
        ],
        "scenes": [
            ["电话订位", "I'd like to make a reservation for six at seven p.m.", "对方回 May I have your name?"],
            ["确认座位", "Is that inside or outside seating?", "问堂内还是户外"],
            ["改时间", "Can we push it to 7:30?", "改晚半小时"],
        ],
        "grammar": "make a reservation 预订（固定搭配）；book = reserve = make a reservation。for six『六个人的』（数字直接表人数）；at + 时刻『在…点』。p.m. 下午。",
        "pron": "同化/缩读：I'd = I would（/aɪd/）。连读：like to→/laɪk tə/；to make→/tə meɪk/；make a→/meɪ kə/；a reservation→/ə ˌrɛzərˈveɪʃən/；reservation for→/ˌrɛzərˈveɪʃən fər/；for six→/fər sɪks/；six at→/sɪk sæt/（s 与 æ 连读）；at seven→/æt ˈsɛvən/；seven p.m.→/ˈsɛvən piːɛm/。弱读：to→/tə/、a→/ə/、for→/fər/、at→/ət/。失去爆破：make /meɪ(k)/。",
    },
    213: {
        "fullIpa": "/wil teɪk ðə ˈteɪbəl baɪ ðə ˈwɪndoʊ ɪf ˈpɑsəbəl/",
        "variants": [
            ["We'll take the table by the window if possible.", "标准"],
            ["Can we sit by the window?", "直接问"],
            ["Window seat if you have one, please.", "更简"],
        ],
        "scenes": [
            ["选位", "We'll take the table by the window if possible.", "对方回 Of course, this way please."],
            ["被安排别处", "Could we move closer to the window?", "请求换位"],
            ["安静角落", "Somewhere quieter would be great.", "想坐安静处"],
        ],
        "grammar": "We'll take…『我们要…』（点单/选位万能开头）。by the window『靠窗』（by 表『在…旁边』）。if possible『如果可以的话』插入语。",
        "pron": "缩读：We'll = We will（/wil/）。连读：take the→/teɪk ðə/；the table→/ðə ˈteɪbəl/；table by→/ˈteɪbəl baɪ/；by the→/baɪ ðə/；the window→/ðə ˈwɪndoʊ/；window if→/ˈwɪndoʊ wɪf/（d 与 ɪ 连读；if 轻读）；if possible→/ɪf ˈpɑsəbəl/。弱读：the→/ðə/、if→/ɪf/。失去爆破：take /teɪ(k)/。同化/浊化：无典型。",
    },
    214: {
        "fullIpa": "/kʊd aɪ siː ðə ˈmɛnjuː pliːz/",
        "variants": [
            ["Could I see the menu, please?", "标准"],
            ["Can I get a menu, please?", "美式常用"],
            ["Menu, please.", "极简"],
        ],
        "scenes": [
            ["入座要菜单", "Could I see the menu, please?", "对方回 Here you are."],
            ["要看中文菜单", "Do you have a menu in English/Chinese?", "要外语菜单"],
            ["扫码点餐", "Can I scan a QR code to order?", "扫码点单"],
        ],
        "grammar": "Could I see…? 索要东西万能句（see 此处=拿到看）。please 放句尾更自然。",
        "pron": "连读：Could I→/kʊ d aɪ/（d 与 aɪ）；I see→/aɪ siː/；see the→/siː ðə/；the menu→/ðə ˈmɛnjuː/；menu please→/ˈmɛnju pliːz/。弱读：the→/ðə/。失去爆破：Could /kʊ(d)/。同化/浊化/缩读：无典型。",
    },
    215: {
        "fullIpa": "/wʌt duː juː ˌrɛkəˈmɛnd æz ə ˈstɑrtər/",
        "variants": [
            ["What do you recommend as a starter?", "标准"],
            ["Any good starters?", "更简"],
            ["What's popular for starters?", "问招牌前菜"],
        ],
        "scenes": [
            ["问服务员", "What do you recommend as a starter?", "对方回 The soup of the day is very popular."],
            ["跟进主菜", "And for the main course?", "接着问主菜"],
            ["犹豫时", "What do most people order?", "问大众选择"],
        ],
        "grammar": "recommend + 名词；as a starter『作为前菜』（as 表角色）。starter 前菜（英式）；美式常说 appetizer。",
        "pron": "连读：What do→/wʌ(t) du/；do you→/dʒə/（缩读）；recommend as→/ˌrɛkəˈmɛn dəz/（d 与 ə）；as a→/ə zə/（z 与 ə 连读）；a starter→/ə ˈstɑrtər/。弱读：do→/də/、as→/əz/、a→/ə/。失去爆破：What /wʌ(t)/；recommend /ˌrɛkəˈmɛn(d)/。同化/浊化：无典型。缩读：do you→/dʒə/。",
    },
    216: {
        "fullIpa": "/aɪl hæv ðə seɪm æz wʌt ʃiːz ˈhævɪŋ/",
        "variants": [
            ["I'll have the same as what she's having.", "标准"],
            ["Same for me, please.", "极简，最常用"],
            ["I'll have what she's having.", "更简（经典梗 When Harry Met Sally）"],
        ],
        "scenes": [
            ["跟点", "I'll have the same as what she's having.", "服务员直接记两份"],
            ["拼桌参考", "That looks good — I'll have one of those.", "指着别人菜点"],
            ["人多跟点", "Make it two.", "来两份一样的"],
        ],
        "grammar": "I'll have… 点餐万能句（have=吃/点）。the same as…『和…一样』。what she's having 名词性从句（她正在点的）。",
        "pron": "缩读：I'll = I will（/aɪl/）；she's = she is（/ʃiːz/）。连读：have the→/hæv ðə/；the same→/ðə seɪm/；same as→/seɪ məz/（m 与 ə 连读）；as what→/əz wʌt/；what she's→/wʌt ʃiːz/；she's having→/ʃiːz ˈhævɪŋ/。弱读：the→/ðə/、as→/əz/、what→/wət/。失去爆破：What /wʌ(t)/。同化：what she's→/wʌt ʃiːz/（t 与 ʃ 相邻，t 可塞擦成 /tʃ/）。",
    },
    217: {
        "fullIpa": "/kʊd aɪ ɡɛt ðɪs wɪˈðaʊt ˈʌnjənz/",
        "variants": [
            ["Could I get this without onions?", "标准"],
            ["No onions, please.", "极简"],
            ["Could you hold the onions?", "hold = 不加，美式餐馆黑话"],
        ],
        "scenes": [
            ["点餐忌口", "Could I get this without onions?", "对方回 Sure, no problem."],
            ["不吃香菜", "Could you hold the cilantro?", "香菜说法"],
            ["上错菜", "This has onions — I asked for no onions.", "礼貌指错"],
        ],
        "grammar": "without + 名词『不含…』。hold + 食材 = 不放该食材（餐馆用语）。get this『做这道（菜）』。",
        "pron": "连读：Could I→/kʊ d aɪ/；get this→/ɡɛ(t) ðɪs/；this without→/ðɪs wɪˈðaʊt/；without onions→/wɪˈðaʊ tˈʌnjənz/（t 与 ʌ 连读）。弱读：a→/ə/（a 未出现），this→/ðɪs/。失去爆破：get /ɡɛ(t)/。同化：无典型。浊化/缩读：无典型。",
    },
    218: {
        "fullIpa": "/ɪz ðɪs dɪʃ ˈvɛri ˈspaɪsi/",
        "variants": [
            ["Is this dish very spicy?", "标准"],
            ["How spicy is it?", "问辣度等级更实用"],
            ["Is it hot? I can't handle spicy food.", "hot 也指辣"],
        ],
        "scenes": [
            ["点餐确认", "Is this dish very spicy?", "对方回 Mild/Medium/Very spicy."],
            ["要求减辣", "Could you make it less spicy?", "要求微辣"],
            ["小朋友吃", "Is it kid-friendly? Not too spicy?", "给娃点菜"],
        ],
        "grammar": "spicy 辣的（口语也用 hot，但 hot 兼指温度，需语境）。How spicy…? 问程度（very / a little / not at all）。",
        "pron": "连读：Is this→/ɪz ðɪs/；this dish→/ðɪs dɪʃ/；dish very→/dɪʃ ˈvɛri/；very spicy→/ˈvɛri ˈspaɪsi/。弱读：is→/ɪz/、this→/ðɪs/。浊化：spicy /ˈspaɪsi/ 的 s 后 p 清辅音送气强（非浊化，标准送气）。失去爆破/同化/缩读：无典型。",
    },
    219: {
        "fullIpa": "/aɪm əˈlɜrdʒɪk tuː ˈpiːnʌts soʊ pliːz biː ˈkɛrfəl/",
        "variants": [
            ["I'm allergic to peanuts, so please be careful.", "标准"],
            ["I have a peanut allergy.", "名词说法，更正式"],
            ["No peanuts, please — severe allergy.", "强调严重性"],
        ],
        "scenes": [
            ["点餐声明", "I'm allergic to peanuts, so please be careful.", "对方回 Noted, I'll inform the chef."],
            ["强调严重", "Even a small amount could cause a reaction.", "微量也不行"],
            ["随身卡", "Here's my allergy card.", "出示过敏提示卡"],
        ],
        "grammar": "be allergic to + 食物『对…过敏』（介词 to，不是 with）。so 表因果承接。please be careful 礼貌叮嘱。",
        "pron": "缩读：I'm = I am（/aɪm/）。连读：allergic to→/əˈlɜrdʒɪk tu/；to peanuts→/tə ˈpiːnʌts/；peanuts so→/ˈpiːnʌ(t) soʊ/（ts 与 s 相邻）；so please→/soʊ pliːz/；please be→/pliːz bi/；be careful→/bi ˈkɛrfəl/。弱读：to→/tə/、so→/sə/。失去爆破：peanuts /ˈpiːnʌ(t)s/。同化/浊化：无典型。",
    },
    220: {
        "fullIpa": "/kʊd juː tɛl miː wʌts ɪn ðɪs sɔs/",
        "variants": [
            ["Could you tell me what's in this sauce?", "标准"],
            ["What's in the sauce?", "更简"],
            ["What does the sauce contain?", "正式问法"],
        ],
        "scenes": [
            ["过敏排查", "Could you tell me what's in this sauce?", "确认不含过敏原"],
            ["好奇配方", "This sauce is amazing — what's in it?", "好奇成分"],
            ["素食确认", "Is the sauce vegetarian?", "问是否素食"],
        ],
        "grammar": "tell me + what 引导宾语从句（what's in…）。sauce 酱汁；与 source（来源）同音异义。contain 含有（及物，不接 in）。",
        "pron": "连读：Could you→/kʊ dʒu/（d+j→dʒ 同化）；tell me→/tɛl mi/；me what's→/mi wʌts/；what's in→/wʌ(t) sɪn/（t 与 s 相邻，可连读 /wʌtsɪn/）；in this→/ɪn ðɪs/；this sauce→/ðɪs sɔs/。弱读：me→/mɪ/、this→/ðɪs/。同化：Could you→/kʊdʒu/（关键）。失去爆破：What's /wʌts/ 结尾。缩读：what's = what is。",
    },
    221: {
        "fullIpa": "/dʌz ɪt kənˈteɪn ˈɛni ˈsiːfuːd/",
        "variants": [
            ["Does it contain any seafood?", "标准"],
            ["Is there any seafood in it?", "更口语"],
            ["Any shellfish in this?", "问贝类更具体"],
        ],
        "scenes": [
            ["过敏排查", "Does it contain any seafood?", "对方回 No seafood, just chicken."],
            ["素食确认", "I'm vegetarian — does this have any meat?", "素食者泛问肉类的说法"],
            ["海鲜忌口", "I avoid shellfish. Is this safe for me?", "贝类过敏"],
        ],
        "grammar": "contain 及物动词直接接宾语（不接 in）。any 用于疑问句。seafood 海鲜（集合名词不可数）。",
        "pron": "连读：Does it→/dʌ zɪt/（z 与 ɪ）；it contain→/ɪ(t) kənˈteɪn/；contain any→/kənˈteɪ nəni/（n 与 ɛ）；any seafood→/ˈɛni ˈsiːfuːd/。弱读：it→/ɪt/、any→/ˈɛni/。失去爆破：it /ɪ(t)/。同化/浊化/缩读：无典型。",
    },
    222: {
        "fullIpa": "/aɪl ˈɔrdər ðə sɛt miːl fɔr tuː/",
        "variants": [
            ["I'll order the set meal for two.", "标准"],
            ["The set menu for two, please.", "set menu 英式说法"],
            ["Two set meals, please.", "更直接"],
        ],
        "scenes": [
            ["点套餐", "I'll order the set meal for two.", "对方回 Any drinks with that?"],
            ["问套餐内容", "What does the set meal include?", "问包含什么"],
            ["升级套餐", "Can we upgrade to the deluxe set?", "问升级"],
        ],
        "grammar": "I'll order… 点单万能句。set meal 套餐（英式）；美式说 combo / combo meal。for two『两人份』。",
        "pron": "缩读：I'll = I will（/aɪl/）。连读：order the→/ˈɔrdər ðə/；the set→/ðə sɛt/；set meal→/sɛ(t) miːl/（t 失去爆破后连读）；meal for→/miːl fər/；for two→/fər tu/。弱读：the→/ðə/、for→/fər/。失去爆破：set /sɛ(t)/。同化/浊化：无典型。",
    },
    223: {
        "fullIpa": "/haʊ wʊd juː laɪk jʊr steɪk dʌn/",
        "variants": [
            ["How would you like your steak done?", "标准（服务员问句）"],
            ["How do you want your steak?", "更直接"],
            ["How should it be cooked?", "问做法"],
        ],
        "scenes": [
            ["服务员问熟度", "How would you like your steak done?", "客人答 Medium, please."],
            ["客人反问", "What do you suggest?", "请服务员建议"],
            ["担心生熟", "Is rare safe to eat here?", "问几分熟安全性"],
        ],
        "grammar": "How would you like…? 服务业高频问句（=你想要…怎么样）。your steak done 中 done 是过去分词作宾补（做完的状态）。",
        "pron": "连读：How would→/haʊ wʊd/；would you→/wʊ dʒu/（d+j→dʒ 同化）；you like→/dʒu laɪk/；like your→/laɪk jʊr/（k 与 j 滑音过渡）；your steak→/jʊr steɪk/；steak done→/steɪk dʌn/。弱读：would→/wəd/、your→/jər/。同化：would you→/wʊdʒu/（关键！）。浊化：steak /steɪk/ 的 s 后 t 送气（标准）。缩读：无典型。",
    },
    224: {
        "fullIpa": "/ˈmiːdiəm wɛl fɔr miː pliːz/",
        "variants": [
            ["Medium well for me, please.", "标准"],
            ["Medium, please.", "更简"],
            ["I'll go with medium well.", "go with 表选择"],
        ],
        "scenes": [
            ["答熟度", "Medium well for me, please.", "服务员记下"],
            ["牛排偏生", "This is more rare than medium — could you cook it a bit more?", "回炉重烤"],
            ["熟度等级", "Rare → Medium rare → Medium → Medium well → Well done（生到全熟）", "点餐前记住等级"],
        ],
        "grammar": "熟度五档：rare（一分）/ medium rare（三分）/ medium（五分）/ medium well（七分）/ well done（全熟）。for me『我的那份』；please 放句尾。",
        "pron": "连读：Medium well→/ˈmiːdiəm wɛl/（m 与 w 滑音）；well for→/wɛl fər/；for me→/fər mi/；me please→/mi pliːz/。弱读：for→/fər/。浊化：无（medium m 清音起）。失去爆破/同化/缩读：无典型。",
    },
    225: {
        "fullIpa": "/kʊd wiː ɡɛt sʌm mɔr ˈwɔtər fɔr ðə ˈteɪbəl/",
        "variants": [
            ["Could we get some more water for the table?", "标准"],
            ["More water, please.", "极简"],
            ["Could we have a refill on the water?", "refill 续杯"],
        ],
        "scenes": [
            ["加水", "Could we get some more water for the table?", "对方回 Sure, still or sparkling?"],
            ["问水型", "Just tap water is fine.", "免费自来水"],
            ["续杯", "Can I get a refill?", "美式免费续杯场景"],
        ],
        "grammar": "some more + 不可数名词『再来一些…』。for the table『全桌的』（不是一个人的）。refill 续杯/续水。",
        "pron": "连读：Could we→/kʊd wi/；we get→/wi ɡɛt/；get some→/ɡɛ(t) sʌm/；some more→/sʌm mɔr/；more water→/mɔr ˈwɔtər/；water for→/ˈwɔtər fər/；for the→/fər ðə/；the table→/ðə ˈteɪbəl/。弱读：some→/səm/、for→/fər/、the→/ðə/。失去爆破：get /ɡɛ(t)/。闪音：water 美式 /ˈwɔɾər/（t 在两元音间闪音化，关键！）。同化/浊化：无典型。",
    },
}
