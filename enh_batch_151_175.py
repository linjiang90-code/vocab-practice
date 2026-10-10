# -*- coding: utf-8 -*-
"""ENH 标注批次 151-175（Day61=10-12 解锁的 151-200 前半段）。
结构：fullIpa / variants / scenes / grammar / pron，与 101-150 同格式。
由 enh_merge.py 幂等合并进 master.json（仅 enh.fullIpa 为空时写入）。
"""
ENH = {
    151: {
        "fullIpa": "/wɪtʃ ˈplætfɔːrm dʌz ðə ɪkˈsprɛs liːv frəm/",
        "variants": [
            ["What platform does it leave from?", "it 指代车次，更口语"],
            ["Which platform for the express?", "极简，车站常用"],
            ["What platform is the express on?", "另一种地道说法"],
        ],
        "scenes": [
            ["火车站问讯处", "Which platform does the express leave from?", "对方回 Platform 4, on your right."],
            ["看大屏确认", "It's leaving from Platform 2.", "自己核对站台号"],
            ["换乘赶车", "Hurry, it leaves in five minutes.", "提醒发车在即"],
        ],
        "grammar": "platform 站台；express 此处作名词『快车』。leave from + 地点 表『从…发车』。which 引导特殊疑问句，助动词 does 提前到主语 the express 前。",
        "pron": "连读：Which platform→/wɪtʃ ˈplætfɔːrm/（tʃ 与 p 相邻）；does the→/dʌz ðə/（z 与 ð）；the express→/ðə ɪkˈsprɛs/（ð 与 ɪ）；leave from→/liːv frəm/（v 与 f，可加 v 滑音）。弱读：the→/ðə/、does→/dəz/、from→/frəm/。失去爆破：express 词尾 /s/ 在 /l/ 前不完全爆破 /ɪkˈsprɛ(s) liːv/。同化/滑音/浊化/缩读：无典型。",
    },
    152: {
        "fullIpa": "/wɛr du aɪ ɡɛt ɔːf fɔr ðə oʊld taʊn/",
        "variants": [
            ["Where should I get off for the old town?", "should 更礼貌，问『该在哪下』"],
            ["What stop is the old town?", "更简，直接问站点"],
            ["Can you tell me where to get off?", "请对方提醒下车点"],
        ],
        "scenes": [
            ["公交/地铁上问同车人", "Where do I get off for the old town?", "对方回 Two stops after this one."],
            ["看站牌", "Is this the stop for the old town?", "确认是否到站"],
            ["用地铁", "Which station is closest to the old town?", "问最近站点"],
        ],
        "grammar": "get off 固定短语『下车』（公交/地铁/火车通用，下船用 get off 也可）。for + 目的地 表『去…（该在哪下）』。old town 老城区/老城。",
        "pron": "连读：Where do→/wɛr du/（r 与 d）；do I→/du aɪ/（双元音顺接）；get off→/ɡɛt ɔːf/（t 与 ɔ）；for the→/fɔr ðə/（r 与 ð）。浊化：get off 快读 /ɡɛ dɔːf/（t→d，典型）。弱读：do→/də/、I→/aɪ/（此处重读）、the→/ðə/、for→/fər/。失去爆破：get off /ɡɛ(t) ɔːf/（t 在 ɔ 前不完全爆破）。缩读：无典型。",
    },
    153: {
        "fullIpa": "/kʊdʒu lɛt mi noʊ wɛn wi əˈraɪv/",
        "variants": [
            ["Can you tell me when we arrive?", "tell me 比 let me know 更直白"],
            ["Please let me know when we get there.", "get there 更口语"],
            ["Wake me up when we arrive?", "若想睡觉，用 wake me up"],
        ],
        "scenes": [
            ["长途巴士上请司机提醒", "Could you let me know when we arrive?", "司机回 Sure, I'll call it out."],
            ["火车上问乘务员", "Which stop is mine?", "对方帮你看站"],
            ["自己设闹钟", "I'll set an alarm just in case.", "以防错过"],
        ],
        "grammar": "Could you + 动词原形 表委婉请求（比 Can you 客气）。let me know 『告诉我』；when we arrive 是时间状语从句。arrive 为不及物，不加宾语。",
        "pron": "同化：Could you→/kʊdʒu/（d+j 同化为 dʒ，关键！）。连读：let me→/lɛ mi/（t 与 m，t 轻化/失去爆破）；me know→/mi noʊ/；know when→/noʊ wɛn/（w 滑音）；when we→/wɛn wi/（n 与 w）；we arrive→/wi əˈraɪv/（w 顺接）。弱读：me→/mi/、we→/wi/。失去爆破：let me /lɛ(t) mi/（t 在 m 前不完全爆破）。缩读：无典型。",
    },
    154: {
        "fullIpa": "/haʊ ˈɔfən du ðə ˈbʌsɪz rʌn ɑn ðɪs ruːt/",
        "variants": [
            ["How frequent are the buses on this route?", "frequent 更正式，表『班次密』"],
            ["How often does this bus come?", "问单辆车也行"],
            ["What's the bus schedule here?", "直接问时刻表"],
        ],
        "scenes": [
            ["站台问调度", "How often do the buses run on this route?", "对方回 Every ten minutes."],
            ["查站牌", "It says one every 15 minutes.", "自己看频次"],
            ["末班车", "When's the last bus?", "问收车时间"],
        ],
        "grammar": "How often 问频率『多久一次』；do the buses run 用复数 buses 因泛指该线路所有车。on this route 『在这条线路上』。route 美式常读 /ruːt/，英式 /raʊt/。",
        "pron": "连读：How often→/haʊ ˈɔfən/（w 与 ɔ）；often do→/ˈɔfən du/（n 与 d）；do the→/du ðə/（ð）；the buses→/ðə ˈbʌsɪz/（ð 与 b）；buses run→/ˈbʌsɪz rʌn/（z 与 r）；on this→/ɑn ðɪs/（n 与 ð）；this route→/ðɪs ruːt/（s 与 r）。弱读：the→/ðə/、do→/də/、on→/ən/。失去爆破：often /ˈɔf(t)ən/（t 在 n 前不完全爆破，常直接不发音）。浊化/同化/滑音/缩读：无典型。",
    },
    155: {
        "fullIpa": "/dʌz ðɪs bʌs ɡoʊ ɔl ðə weɪ tə ðə biːtʃ/",
        "variants": [
            ["Does this bus go to the beach?", "最简，直接问终点"],
            ["Is the beach on this route?", "问是否在该线路上"],
            ["Where does this bus end up?", "问终点站"],
        ],
        "scenes": [
            ["上车前问司机", "Does this bus go all the way to the beach?", "司机回 Yep, final stop."],
            ["看车头牌", "Beach is the last stop.", "自己确认"],
            ["换乘", "You'll need to transfer at the square.", "需换乘"],
        ],
        "grammar": "all the way to + 地点 『一路到…/直达…』。go 此处表『开往/行驶到』。the beach 海滩（度假地常用 the）。",
        "pron": "连读：Does this→/dʌz ðɪs/（z 与 ð）；this bus→/ðɪs bʌs/（s 与 b）；bus go→/bʌs ɡoʊ/（s 与 ɡ）；go all→/ɡoʊ ɔl/（w 与 ɔ）；all the→/ɔl ðə/（l 与 ð）；the way→/ðə weɪ/（ð 与 w 滑音）；way to→/weɪ tə/（w 与 t）；to the→/tə ðə/（t 与 ð）；the beach→/ðə biːtʃ/（ð 与 b）。弱读：the→/ðə/、to→/tə/、this→/ðɪs/（重读）。失去爆破：beach 词尾 tʃ 保留。浊化/同化/缩读：无典型。",
    },
    156: {
        "fullIpa": "/wɛrz ðə ˈnɪrɪst bʌs stɑp/",
        "variants": [
            ["Where's the closest bus stop?", "closest 与 nearest 同义"],
            ["Is there a bus stop near here?", "问附近有没有"],
            ["Which bus stop is nearest?", "问哪一个最近"],
        ],
        "scenes": [
            ["街头问路人", "Where's the nearest bus stop?", "对方回 Just around the corner."],
            ["用地图", "The stop is 200 meters ahead.", "导航提示"],
            ["确认方向", "Am I walking the right way?", "确认没走反"],
        ],
        "grammar": "nearest 是 near 最高级『最近的』；bus stop 公交站（英式也用 bus stop，美式同）。Where's = Where is 缩读。",
        "pron": "连读：Where's the→/wɛrz ðə/（z 与 ð）；the nearest→/ðə ˈnɪrɪst/（ð 与 n）；nearest bus→/ˈnɪrɪst bʌs/（t 与 b）；bus stop→/bʌs stɑp/（s 与 s 相邻，只读一次送气）。弱读：the→/ðə/。失去爆破：nearest /ˈnɪrɪ(s)t/（s 在 t 前）；bus stop /bʌ(s) stɑp/。浊化/同化/缩读：无典型。",
    },
    157: {
        "fullIpa": "/aɪd laɪk tə rɛnt ə ˈkɑmpækt kɑr fɔr θri daɪz/",
        "variants": [
            ["I'd like to rent a small car for three days.", "small 比 compact 更口语"],
            ["Can I rent a compact for three days?", "用 can 更直白"],
            ["I want to hire a compact car.", "hire 英式常用（租）"],
        ],
        "scenes": [
            ["租车柜台", "I'd like to rent a compact car for three days.", "对方回 Sure, let me see what's available."],
            ["说明车型", "Something fuel-efficient, please.", "补充要省油"],
            ["谈自动挡", "Automatic or manual?", "问自动还是手动"],
        ],
        "grammar": "I'd like to… = I would like to… 比 I want 礼貌，租车的万能开头。rent（美）/ hire（英）都表『租』。compact car 紧凑型车；for + 时间段 表租期。",
        "pron": "同化/缩读：I'd = I would（/aɪd/）。连读：like to→/laɪk tə/（k 与 t，可连成 /laɪktə/）；to rent→/tə rɛnt/（t 与 r）；rent a→/rɛn də/（t 与 ə，t 轻化）；a compact→/ə ˈkɑmpækt/；compact car→/ˈkɑmpækt kɑr/（t 与 k）；car for→/kɑr fɔr/（r 与 f，加 r 滑音）；for three→/fɔr θri/（r 与 θ）；three days→/θri daɪz/（θ 与 d）。浊化：like to 快读 /laɪ də/（t→d）。弱读：to→/tə/、a→/ə/、for→/fər/。失去爆破：compact /ˈkɑm(p)ækt/（p 在 æ 前不完全爆破）。",
    },
    158: {
        "fullIpa": "/dʌz ðə praɪs ɪnˈkluːd fʊl ɪnˈʃʊrəns/",
        "variants": [
            ["Does the price include insurance?", "insurance 不带 full 也行"],
            ["Is insurance included?", "更简，被动"],
            ["What does full insurance cover?", "追问保哪些"],
        ],
        "scenes": [
            ["租车谈价", "Does the price include full insurance?", "对方回 It's an extra $12 a day.（另收）"],
            ["确认免赔", "Is there a deductible?", "问自付额"],
            ["信用卡已含", "My credit card covers it.", "自家卡已带险"],
        ],
        "grammar": "include 及物『包含』；full insurance 全险（碰撞+盗抢等全包）。price 单数用 does。be included 被动形式亦可。",
        "pron": "连读：Does the→/dʌz ðə/（z 与 ð）；the price→/ðə praɪs/（ð 与 p）；price include→/praɪs ɪnˈkluːd/（s 与 ɪ）；include full→/ɪnˈkluːd fʊl/（d 与 f）；full insurance→/fʊl ɪnˈʃʊrəns/（l 与 ɪ）。弱读：the→/ðə/、does→/dəz/。失去爆破：full /fʊ(l) ɪnˈʃʊrəns/（l 在 ɪ 前）。浊化/同化/缩读：无典型。",
    },
    159: {
        "fullIpa": "/du aɪ niːd ən ˌɪntərˈnæʃənəl ˈdraɪvɪŋ ˈpɜːrmɪt/",
        "variants": [
            ["Do I need an international license?", "license 与 permit 同义"],
            ["Is my home license valid here?", "问本国驾照是否有效"],
            ["Do you accept a foreign license?", "问是否认外国证"],
        ],
        "scenes": [
            ["租车被要求证件", "Do I need an international driving permit?", "对方回 Yes, we need to see it."],
            ["免押", "A passport is enough.", "有时护照即可"],
            ["当地交规", "In some countries IDP is mandatory.", "部分国家强制"],
        ],
        "grammar": "international driving permit（IDP）国际驾驶许可，常配合本国驾照使用。need 实义动词，疑问句借 do。an 用于元音开头的 international 前。",
        "pron": "连读：Do I→/du aɪ/；I need→/aɪ niːd/（aɪ 与 n）；need an→/niːd ən/（d 与 ə）；an international→/ən ˌɪntərˈnæʃənəl/（n 与 ɪ）；international driving→/ˌɪntərˈnæʃənəl ˈdraɪvɪŋ/（l 与 d）；driving permit→/ˈdraɪvɪŋ ˈpɜːrmɪt/（ŋ 与 p）。浊化：need an 快读 /niː dən/（d→d 本就浊）；driving /ˈdraɪvɪŋ/ 词尾 ŋ。弱读：a→/ə/、an→/ən/。失去爆破：international /ˌɪntərˈnæʃə(n)əl/（n 在 ə 前鼻音）。缩读：无典型。",
    },
    160: {
        "fullIpa": "/ɪz ðə ˈfjuːəl ˈpɑləsi fʊl tə fʊl/",
        "variants": [
            ["Is it full-to-full?", "极简，租车行通用说法"],
            ["Do I return it with a full tank?", "full tank 满油箱"],
            ["What's the fuel policy?", "直接问政策"],
        ],
        "scenes": [
            ["取车确认油量", "Is the fuel policy full-to-full?", "对方回 Yes, bring it back full."],
            ["忘了加", "There's a refueling charge if not full.", "不满要收费"],
            ["预购油", "Pre-purchase a full tank?", "问要不要先买满箱"],
        ],
        "grammar": "fuel policy 油量/燃油政策；full-to-full 『满油取、满油还』是租车行标准条款。policy 此处指『规定/政策』。",
        "pron": "连读：Is the→/ɪz ðə/（z 与 ð）；the fuel→/ðə ˈfjuːəl/（ð 与 f）；fuel policy→/ˈfjuːəl ˈpɑləsi/（l 与 p）；policy full→/ˈpɑləsi fʊl/（i 与 f）；full to→/fʊl tə/（l 与 t）；to full→/tə fʊl/（t 与 f）。弱读：the→/ðə/、to→/tə/。失去爆破：fuel /ˈfjuː(ə)l/（l 鼻音）；policy /ˈpɑlə(s)i/。浊化/同化/缩读：无典型。",
    },
    161: {
        "fullIpa": "/wɛr kæn aɪ rɪˈtɜːrn ðə kɑr ˈæftər ˈaʊərz/",
        "variants": [
            ["Where do I return the car after hours?", "do I 比 can I 更自然"],
            ["Is there a drop box after hours?", "drop box 投钥匙箱"],
            ["Can I return it late tonight?", "问当晚晚些还"],
        ],
        "scenes": [
            ["柜台下班前问", "Where can I return the car after hours?", "对方回 Use the key drop by the gate."],
            ["夜间还车", "Just leave the keys in the box.", "投钥匙箱即可"],
            ["确认收费", "No extra charge for late return?", "问是否加收"],
        ],
        "grammar": "after hours 固定短语『下班后/营业时间外』。return the car 还车；where can I… 问地点。",
        "pron": "连读：Where can→/wɛr kæn/（r 与 k）；can I→/kæn aɪ/（n 与 aɪ）；I return→/aɪ rɪˈtɜːrn/（aɪ 与 r）；return the→/rɪˈtɜːrn ðə/（n 与 ð）；the car→/ðə kɑr/（ð 与 k）；car after→/kɑr ˈæftər/（r 与 æ，加 r 滑音）；after hours→/ˈæftər ˈaʊərz/（r 与 aʊ）。弱读：the→/ðə/、can→/kən/、I→/aɪ/（重读）。失去爆破：after /ˈæf(t)ər/（t 在 ə 前不完全爆破）。缩读：无典型。",
    },
    162: {
        "fullIpa": "/ɪz ðɛr ə ɡæs ˈsteɪʃən ɑn ðə weɪ tə ðə ˈhaɪweɪ/",
        "variants": [
            ["Is there a gas station on the way to the highway?", "highway 美式高速"],
            ["Where's the nearest gas station?", "问最近也行"],
            ["Can I get fuel before the highway?", "fuel 更正式"],
        ],
        "scenes": [
            ["开车问导航/同车人", "Is there a gas station on the way to the highway?", "对方回 There's one at the next exit."],
            ["高速入口前", "Fill up before you get on.", "提醒先加满"],
            ["确认营业", "It's open 24 hours.", "全天候"],
        ],
        "grammar": "on the way to + 地点『在去…的路上』；gas station 加油站（英式 petrol station）。highway 美式高速公路（英式 motorway）。there is 存在句。",
        "pron": "连读：Is there→/ɪz ðɛr/（z 与 ð）；there a→/ðɛr ə/（r 与 ə）；a gas→/ə ɡæs/；gas station→/ɡæs ˈsteɪʃən/（s 与 s）；station on→/ˈsteɪʃən ɑn/（n 与 ɑ）；on the→/ɑn ðə/（n 与 ð）；the way→/ðə weɪ/（ð 与 w 滑音）；way to→/weɪ tə/（w 与 t）；to the→/tə ðə/；the highway→/ðə ˈhaɪweɪ/。弱读：there→/ðɛr/、a→/ə/、the→/ðə/、to→/tə/、on→/ən/。失去爆破：gas /ɡæ(s)/。浊化/同化/缩读：无典型。",
    },
    163: {
        "fullIpa": "/kʊdʒu fɪl ɪt ʌp wɪð ˈrɛɡjələr pliːz/",
        "variants": [
            ["Fill it up with regular, please.", "直接说，最常用"],
            ["Regular, fill her up.", "fill her up 俚语指加满（车拟人）"],
            ["Unleaded, please.", "unleaded 无铅，美式常指普通汽油"],
        ],
        "scenes": [
            ["加油站对店员", "Could you fill it up with regular, please?", "店员回 Sure, and wash the windows?"],
            ["只加部分", "Just ten dollars, please.", "不加满"],
            ["高级油", "Premium instead?", "问是否加高标"],
        ],
        "grammar": "fill up 短语『加满』；with + 油号 regular（普通汽油）。Could you… 礼貌请求。it 指代油箱/车。",
        "pron": "同化：Could you→/kʊdʒu/（d+j 同化为 dʒ，关键！）。连读：fill it→/fɪl ɪt/（l 与 ɪ，t 轻化）；it up→/ɪ tʌp/；up with→/ʌp wɪð/（p 与 w 滑音）；with regular→/wɪð ˈrɛɡjələr/（ð 与 r）；regular please→/ˈrɛɡjələr pliːz/。弱读：it→/ɪt/、up→/ʌp/、with→/wɪð/。失去爆破：fill it /fɪ(l) ɪt/（l 鼻音）；up with /ʌ(p) wɪð/（p 在 w 前不完全爆破）。缩读：无典型。",
    },
    164: {
        "fullIpa": "/ɪz ˈpɑrkɪŋ friː əˈraʊnd hɪr ɑn ˈwiːkɛndz/",
        "variants": [
            ["Is parking free here on weekends?", "here 比 around here 更简"],
            ["Do we have to pay for parking?", "问要不要付费"],
            ["Where's the nearest parking lot?", "问最近停车场"],
        ],
        "scenes": [
            ["街头问路人", "Is parking free around here on weekends?", "对方回 Metered, but free after six."],
            ["看咪表", "You still need to pay till 8 PM.", "仍要付费到晚8"],
            ["酒店住客", "Guests park free.", "住客免费"],
        ],
        "grammar": "parking 动名词作主语『停车（费）』；free 此处『免费』。around here 『这一带』。on weekends 美式（英式 at weekends）。",
        "pron": "连读：Is parking→/ɪz ˈpɑrkɪŋ/（z 与 p）；parking free→/ˈpɑrkɪŋ friː/（ŋ 与 f）；free around→/friː əˈraʊnd/（i 与 ə）；around here→/əˈraʊnd hɪr/（d 与 h）；here on→/hɪr ɑn/（r 与 ɑ）；on weekends→/ɑn ˈwiːkɛndz/（n 与 w）。弱读：is→/ɪz/（重读）、around→/əˈraʊnd/、here→/hɪr/、on→/ən/。失去爆破：weekends 词尾 /dz/ 保留。浊化/同化/缩读：无典型。",
    },
    165: {
        "fullIpa": "/du ju ˈvælɪdeɪt ˈpɑrkɪŋ fɔr ˈkʌstəmərz/",
        "variants": [
            ["Do you validate parking for customers?", "validate 指『盖章免停车费』"],
            ["Can you stamp my ticket?", "stamp 盖章，更口语"],
            ["Is parking validated with a purchase?", "问消费是否免停"],
        ],
        "scenes": [
            ["商场/餐厅结账", "Do you validate parking for customers?", "对方回 Yes, show me the receipt."],
            ["自助机", "Use the machine at the entrance.", "门口机器自盖"],
            ["限额", "Two hours free after validation.", "盖章后免2小时"],
        ],
        "grammar": "validate parking（美）『为停车券盖章/核销，免停车费』，零售/餐饮常用。for customers 『为顾客』。validate 及物，parking 作宾语。",
        "pron": "连读：Do you→/du ju/（可同化 /dʒu/）；you validate→/ju ˈvælɪdeɪt/（j 与 v）；validate parking→/ˈvælɪdeɪt ˈpɑrkɪŋ/（t 与 p）；parking for→/ˈpɑrkɪŋ fɔr/（ŋ 与 f）；for customers→/fɔr ˈkʌstəmərz/（r 与 k）。同化：Do you→/dʒu/（d+j 同化，可选）。弱读：you→/ju/、do→/də/、for→/fər/。失去爆破：validate /ˈvælɪdeɪ(t)/（t 词尾）。缩读：无典型。",
    },
    166: {
        "fullIpa": "/ɪkˈskjuːz mi wɪtʃ weɪ ɪz ðə treɪn ˈsteɪʃən/",
        "variants": [
            ["Excuse me, where's the train station?", "更简，略掉 which way"],
            ["Which way to the train station?", "极简，省 excuse me 也可"],
            ["How do I get to the train station?", "问『怎么去』也常见"],
        ],
        "scenes": [
            ["街头问路人", "Excuse me, which way is the train station?", "对方回 Go straight, it's on your left."],
            ["地铁里", "Follow the signs to the platforms.", "看指示牌"],
            ["确认距离", "Is it far from here?", "问远不远"],
        ],
        "grammar": "Excuse me 礼貌开场『打扰一下』。which way 『哪边/哪个方向』。train station 火车站（英式也用 railway station）。",
        "pron": "连读：Excuse me→/ɪkˈskjuːz mi/（z 与 m，z 轻化）；me which→/mi wɪtʃ/（m 与 w 滑音）；which way→/wɪtʃ weɪ/（tʃ 与 w）；way is→/weɪ ɪz/（w 与 ɪ）；is the→/ɪz ðə/（ð）；the train→/ðə treɪn/（ð 与 t）；train station→/treɪn ˈsteɪʃən/（n 与 s）。弱读：me→/mi/、the→/ðə/、is→/ɪz/。失去爆破：excuse /ɪkˈskjuː(z)/；train /treɪ(n)/。同化/滑音：me which 加 w 滑音。缩读：无典型。",
    },
    167: {
        "fullIpa": "/ɡoʊ streɪt fɔr tu blɑks ðɛn tɜːrn lɛft/",
        "variants": [
            ["Go straight for two blocks, then turn left.", "标准指路"],
            ["Straight on, two blocks, then left.", "更口语省略"],
            ["Keep going straight, then left at the second block.", "keep going 更自然"],
        ],
        "scenes": [
            ["路人指路", "Go straight for two blocks, then turn left.", "对方可能补 You'll see a red door."],
            ["确认", "Left at the corner?", "确认左转点"],
            ["走过了", "You went too far.", "提醒走过了"],
        ],
        "grammar": "go straight 『直走』；for + 距离 two blocks『两个街区』。then 『然后』；turn left/right『左/右转』。block 城市街区。",
        "pron": "连读：Go straight→/ɡoʊ streɪt/（w 与 s，加 w 滑音）；straight for→/streɪt fɔr/（t 与 f）；for two→/fɔr tu/（r 与 t）；two blocks→/tu blɑks/（w 与 b）；blocks then→/blɑks ðɛn/（s 与 ð）；then turn→/ðɛn tɜːrn/（n 与 t）；turn left→/tɜːrn lɛft/（n 与 l）。弱读：for→/fər/、then→/ðɛn/（重读）。失去爆破：straight /streɪ(t)/（t 词尾）；blocks /blɑ(k)s/（k 在 s 前）。浊化：for two 快读 /fɔr du/（t→d）。同化/缩读：无典型。",
    },
    168: {
        "fullIpa": "/ɪts dʒʌst əˈraʊnd ðə ˈkɔːrnər ɑn jʊr raɪt/",
        "variants": [
            ["It's just around the corner on your right.", "标准"],
            ["It's right around the corner.", "更简，强调很近"],
            ["Just around the bend on the right.", "bend 弯路/拐弯"],
        ],
        "scenes": [
            ["指路收尾", "It's just around the corner on your right.", "对方回 Oh, that's close."],
            ["确认", "On the right, past the bakery?", "确认参照物"],
            ["很近", "Two-minute walk.", "强调步行近"],
        ],
        "grammar": "around the corner 『在拐角处/很近』；on your right/left『在你右/左边』。It's = It is 缩读；just 『就/只』表近。",
        "pron": "同化/缩读：It's = It is（/ɪts/）。连读：just around→/dʒʌst əˈraʊnd/（t 与 ə）；around the→/əˈraʊnd ðə/（d 与 ð）；the corner→/ðə ˈkɔːrnər/（ð 与 k）；corner on→/ˈkɔːrnər ɑn/（r 与 ɑ）；on your→/ɑn jʊr/（n 与 j 滑音）；your right→/jʊr raɪt/（r 与 r）。弱读：the→/ðə/、around→/əˈraʊnd/、on→/ən/、your→/jʊr/。失去爆破：just /dʒʌ(s)t/（s 在 t 前）；corner /ˈkɔː(r)nər/。浊化/同化：无典型。",
    },
    169: {
        "fullIpa": "/ɪz ɪt wɪˈðɪn ˈwɔːkɪŋ ˈdɪstəns frəm hɪr/",
        "variants": [
            ["Is it within walking distance from here?", "标准"],
            ["Can I walk there?", "更简，直接问能走吗"],
            ["Is it a short walk?", "问步行近不近"],
        ],
        "scenes": [
            ["问能否步行", "Is it within walking distance from here?", "对方回 Yeah, about ten minutes."],
            ["太远", "Better take a cab.", "建议打车"],
            ["导航", "It's a 15-minute walk.", "给出时间"],
        ],
        "grammar": "within walking distance 『步行可达范围内』固定搭配；from here『从这儿』。within + 名词 表『在…之内』。",
        "pron": "连读：Is it→/ɪz ɪt/（z 与 ɪ）；it within→/ɪt wɪˈðɪn/（t 与 w 滑音）；within walking→/wɪˈðɪn ˈwɔːkɪŋ/（n 与 w）；walking distance→/ˈwɔːkɪŋ ˈdɪstəns/（ŋ 与 d）；distance from→/ˈdɪstəns frəm/（s 与 f）；from here→/frəm hɪr/（m 与 h）。弱读：it→/ɪt/、is→/ɪz/（重读）、from→/frəm/、here→/hɪr/。失去爆破：distance /ˈdɪs(t)əns/（t 在 ə 前）；walking /ˈwɔː(k)ɪŋ/。浊化/同化/缩读：无典型。",
    },
    170: {
        "fullIpa": "/haʊ fɑr ɪz ðə ˈɛrport frəm ˈdaʊntaʊn/",
        "variants": [
            ["How far is the airport from downtown?", "标准"],
            ["How long to the airport?", "问耗时也行"],
            ["Is the airport far from the city center?", "city center 英式同义"],
        ],
        "scenes": [
            ["问司机/前台", "How far is the airport from downtown?", "对方回 About 40 minutes by car."],
            ["查交通", "Traffic can be heavy at rush hour.", "提醒高峰堵"],
            ["预算", "A taxi runs $50 or so.", "给出车费"],
        ],
        "grammar": "How far 问距离『多远』；from downtown『离市中心』。airport 机场；downtown 市中心（美式常用，英式 city centre）。",
        "pron": "连读：How far→/haʊ fɑr/（w 与 f）；far is→/fɑr ɪz/（r 与 ɪ）；is the→/ɪz ðə/（ð）；the airport→/ðə ˈɛrport/（ð 与 ɛ）；airport from→/ˈɛrport frəm/（t 与 f）；from downtown→/frəm ˈdaʊntaʊn/（m 与 d）。弱读：the→/ðə/、is→/ɪz/（重读）、from→/frəm/。失去爆破：airport /ˈɛr(p)ort/（p 在 ɔ 前不完全爆破）。浊化/同化/缩读：无典型。",
    },
    171: {
        "fullIpa": "/æm aɪ ˈhɛdɪŋ ɪn ðə raɪt dəˈrɛkʃən fɔr ðə pɑrk/",
        "variants": [
            ["Am I heading in the right direction for the park?", "标准"],
            ["Am I going the right way to the park?", "going the right way 更口语"],
            ["Is this the way to the park?", "最简，问这条路对不对"],
        ],
        "scenes": [
            ["走路怕走反", "Am I heading in the right direction for the park?", "对方回 Yes, keep going straight."],
            ["被纠正", "Actually, it's the other way.", "其实反了"],
            ["用地图", "You're on the right track.", "方向没错"],
        ],
        "grammar": "heading (in) + direction『朝…方向走』；in the right direction『方向正确』。for the park 表目的/去向。Am I… 现在进行时表当前在做的动作。",
        "pron": "连读：Am I→/æm aɪ/（m 与 aɪ）；I heading→/aɪ ˈhɛdɪŋ/（aɪ 与 h）；heading in→/ˈhɛdɪŋ ɪn/（ŋ 与 ɪ）；in the→/ɪn ðə/（n 与 Ë）；the right→/ðə raɪt/（ð 与 r）；right direction→/raɪt dəˈrɛkʃən/（t 与 d）；direction for→/dəˈrɛkʃən fɔr/（n 与 f）；for the→/fɔr ðə/；the park→/ðə pɑrk/。弱读：the→/ðə/、in→/ɪn/、for→/fər/、am→/æm/（重读）。失去爆破：right /raɪ(t)/。同化/滑音/浊化/缩读：无典型。",
    },
    172: {
        "fullIpa": "/kʊdʒu ʃoʊ mi ɑn ðə mæp wɛr wi ɑr/",
        "variants": [
            ["Could you show me on the map where we are?", "标准"],
            ["Can you point to where we are?", "point to 更直白"],
            ["Where are we on this map?", "自己看也可"],
        ],
        "scenes": [
            ["拿地图问同伴", "Could you show me on the map where we are?", "对方回 Right here, by the river."],
            ["用手机", "Let me drop a pin.", "手机定位"],
            ["确认方位", "We're heading north.", "在北边"],
        ],
        "grammar": "show me on the map『在地图上指给我』；where we are 是宾语从句（我们所在位置）。Could you… 礼貌请求。",
        "pron": "同化：Could you→/kʊdʒu/（d+j 同化，关键！）。连读：show me→/ʃoʊ mi/（w 与 m）；me on→/mi ɑn/（m 与 ɑ）；on the→/ɑn ðə/（n 与 ð）；the map→/ðə mæp/（ð 与 m）；map where→/mæp wɛr/（p 与 w 滑音）；where we→/wɛr wi/（r 与 w）；we are→/wi ɑr/（w 与 ɑ）。弱读：me→/mi/、the→/ðə/、on→/ən/、we→/wi/、are→/ɑr/。失去爆破：map /mæ(p)/。缩读：无典型。",
    },
    173: {
        "fullIpa": "/ɪz ðɛr ə ˈʃɔːrtkʌt tə əˈvɔɪd ðə ˈtræfɪk/",
        "variants": [
            ["Is there a shortcut to avoid the traffic?", "标准"],
            ["Any way to skip the jam?", "jam 俚语『堵车』"],
            ["Can we take a back road?", "back road 小路/后路"],
        ],
        "scenes": [
            ["导航堵车问同伴", "Is there a shortcut to avoid the traffic?", "对方回 There's a side street ahead."],
            ["用导航", "Reroute to avoid congestion.", "让导航改道"],
            ["接受堵", "Just sit tight, it'll clear.", "只能等"],
        ],
        "grammar": "shortcut 『近路/捷径』；to avoid『为了避开』不定式表目的。traffic 不可数『车流/交通』，the traffic 指当前这段拥堵。",
        "pron": "连读：Is there→/ɪz ðɛr/（z 与 ð）；there a→/ðɛr ə/；a shortcut→/ə ˈʃɔːrtkʌt/；shortcut to→/ˈʃɔːrtkʌt tə/（t 与 t 只读一次）；to avoid→/tə əˈvɔɪd/（t 与 ə）；avoid the→/əˈvɔɪd ðə/（d 与 ð）；the traffic→/ðə ˈtræfɪk/（ð 与 t）。弱读：there→/ðɛr/、a→/ə/、to→/tə/、the→/ðə/。失去爆破：shortcut /ˈʃɔː(r)tkʌt/（t 在 k 前）；avoid /əˈvɔɪ(d)/。浊化/同化/缩读：无典型。",
    },
    174: {
        "fullIpa": "/krɔs ðə brɪdʒ ənd kiːp ˈɡoʊɪŋ ənˈtɪl ju si ðə taʊər/",
        "variants": [
            ["Cross the bridge and keep going until you see the tower.", "标准指路"],
            ["Go over the bridge, then straight on to the tower.", "over the bridge 同义"],
            ["Past the bridge, keep walking till the tower.", "past 表『过了』"],
        ],
        "scenes": [
            ["路人指路", "Cross the bridge and keep going until you see the tower.", "对方回 You can't miss it."],
            ["确认", "The red tower?", "确认地标颜色"],
            ["走过了", "Turn back, you passed it.", "提醒往回"],
        ],
        "grammar": "cross the bridge『过桥』（cross 及物，不用 go across 也可）；keep going『继续走』；until you see…『直到你看见…』。and 连接两个祈使句。",
        "pron": "连读：Cross the→/krɔs ðə/（s 与 ð）；the bridge→/ðə brɪdʒ/（ð 与 b）；bridge and→/brɪdʒ ənd/（dʒ 与 ə）；and keep→/ənd kiːp/（d 与 k）；keep going→/kiːp ˈɡoʊɪŋ/（p 与 ɡ）；going until→/ˈɡoʊɪŋ ənˈtɪl/（ŋ 与 ə）；until you→/ənˈtɪl ju/（l 与 j，可同化 /ənˈtʃu/）；you see→/ju si/（j 与 s）；see the→/si ðə/（s 与 ð）；the tower→/ðə ˈtaʊər/（ð 与 t）。弱读：the→/ðə/、and→/ənd/、you→/ju/、until→/ənˈtɪl/。同化：until you→/ənˈtʃu/（t+j 同化 /tʃ/，可选）。失去爆破：bridge /brɪ(d)ʒ/；keep /kiː(p)/。浊化/缩读：无典型。",
    },
    175: {
        "fullIpa": "/wɛr ɪz ðə ˈtʊrɪst ɪnˈfɔːrməʃən ˈsɛntər/",
        "variants": [
            ["Where is the tourist information center?", "标准"],
            ["Where's the info center?", "info 口语缩写"],
            ["Is there a visitor center nearby?", "visitor center 同义"],
        ],
        "scenes": [
            ["问路人/车站", "Where is the tourist information center?", "对方回 Next to the station exit."],
            ["找地图", "They have free city maps inside.", "里面免费地图"],
            ["问开放", "Open till seven, I think.", "确认时间"],
        ],
        "grammar": "tourist information center『旅游咨询中心』（常简称 info center）；information 不可数，无复数。Where's = Where is 缩读。center 美式（英式 centre）。",
        "pron": "连读：Where is→/wɛr ɪz/（r 与 ɪ）；is the→/ɪz ðə/（ð）；the tourist→/ðə ˈtʊrɪst/（ð 与 t）；tourist information→/ˈtʊrɪst ɪnˈfɔːrməʃən/（t 与 ɪ）；information center→/ɪnˈfɔːrməʃən ˈsɛntər/（n 与 s）。弱读：the→/ðə/、is→/ɪz/（重读）。失去爆破：tourist /ˈtʊrɪ(s)t/（s 在 t 前）；information /ɪnˈfɔːr(m)əʃən/（m 鼻音）。浊化/同化/缩读：无典型。",
    },
}
