# -*- coding: utf-8 -*-
"""ENH 标注批次 226-250（Day91=2026-11-12 解锁的 201-250 后半段，收银/购物/支付/退税）。
结构：fullIpa / variants / scenes / grammar / pron，与 151-200 同格式。
由 enh_merge.py 幂等合并进 master.json（仅 enh.fullIpa 为空时写入）。
"""
ENH = {
    226: {
        "fullIpa": "/ðɪs ˈɪzənt wʌt aɪ ˈɔrdərd aɪm əˈfrɛd/",
        "variants": [
            ["This isn't what I ordered, I'm afraid.", "标准"],
            ["I didn't order this.", "更直接"],
            ["I think there's a mistake with my order.", "委婉指错"],
        ],
        "scenes": [
            ["上错菜", "This isn't what I ordered, I'm afraid.", "对方回 I'm so sorry, I'll fix it right away."],
            ["指认订单", "I ordered the chicken, not the beef.", "说清点的是什么"],
            ["外卖错单", "My delivery is missing an item.", "外卖少件"],
        ],
        "grammar": "This isn't what I ordered 中 what I ordered 是表语从句（我点的东西）。I'm afraid 句尾缓和语气（礼貌指出问题）。",
        "pron": "缩读：isn't = is not（/ˈɪzənt/）；I'm = I am（/aɪm/）。连读：This isn't→/ðɪ sɪzənt/（s 与 ɪ）；isn't what→/ˈɪzən(t) wʌt/；what I→/wʌ təɪ/（t 与 aɪ）；I ordered→/aɪ ˈɔrdərd/；ordered I'm→/ˈɔrdər d aɪm/；I'm afraid→/aɪ məˈfrɛd/（m 与 ə 连读）。弱读：what→/wət/。失去爆破：isn't /ˈɪzən(t)/。闪音：ordered 美式 /ˈɔrdɚd/。同化/浊化：无典型。",
    },
    227: {
        "fullIpa": "/ðə fuːd wʌz ˈɛksələnt θæŋk juː/",
        "variants": [
            ["The food was excellent, thank you.", "标准"],
            ["The food was great, thanks.", "更口语"],
            ["Everything was delicious.", "泛指全部菜"],
        ],
        "scenes": [
            ["结账夸赞", "The food was excellent, thank you.", "对方回 Thank you, hope to see you again."],
            ["当面夸厨师", "Compliments to the chef!", "向厨师致意，地道表达"],
            ["写好评", "I'll leave a good review.", "说要给好评"],
        ],
        "grammar": "was 过去时（用餐已结束）。excellent 极好的（比 good 强一档）。compliments to the chef 是夸厨师固定用语。",
        "pron": "连读：The food→/ðə fuːd/；food was→/fuː d wʌz/（d 与 w）；was excellent→/wʌ zˈɛksələnt/（z 与 ɛ）；excellent thank→/ˈɛksələn(t) θæŋk/（t 与 θ）；thank you→/θæŋk ju/。弱读：The→/ðə/、was→/wəz/。失去爆破：excellent /ˈɛksələn(t)/。θ 音：thank 咬舌 /θ/，勿读成 /s/。同化/缩读：无典型。",
    },
    228: {
        "fullIpa": "/kʊd wiː hæv ðə bɪl pliːz/",
        "variants": [
            ["Could we have the bill, please?", "标准（英式用 bill）"],
            ["Check, please.", "美式用 check"],
            ["Could we get the bill?", "更随意"],
        ],
        "scenes": [
            ["招手结账", "Could we have the bill, please?", "对方回 Right away."],
            ["分开付", "Could we get separate bills?", "分单"],
            ["一起付", "One bill, please.", "合单"],
        ],
        "grammar": "the bill 账单（英式）；美式说 the check。Could we have…? 索要万能句。",
        "pron": "连读：Could we→/kʊd wi/；we have→/wi hæv/；have the→/hæv ðə/；the bill→/ðə bɪl/；bill please→/bɪl pliːz/。弱读：the→/ðə/。失去爆破：Could /kʊ(d)/。同化/浊化/缩读：无典型。",
    },
    229: {
        "fullIpa": "/kʊd wiː splɪt ðə bɪl θriː weɪz/",
        "variants": [
            ["Could we split the bill three ways?", "标准"],
            ["Can we split it three ways?", "split it 更简"],
            ["Let's split the bill evenly.", "均摊说法"],
        ],
        "scenes": [
            ["朋友聚餐分摊", "Could we split the bill three ways?", "对方回 Sure, that's 68 each."],
            ["各付各的", "We'd like to pay separately.", "separately 各自付"],
            ["请客抢付", "It's on me tonight.", "我请客"],
        ],
        "grammar": "split the bill 分摊账单；three ways『按三份』（way 表份额）。split 过去式/过去分词同为 split。pay separately 各自付。",
        "pron": "连读：Could we→/kʊd wi/；we split→/wi splɪt/；split the→/splɪ(t) ðə/（t 失去爆破）；the bill→/ðə bɪl/；bill three→/bɪl θriː/；three ways→/θriː weɪz/。弱读：the→/ðə/。失去爆破：split /splɪ(t)/。θ 音：three /θriː/ 咬舌。同化/浊化/缩读：无典型。",
    },
    230: {
        "fullIpa": "/ɪz ˈsɜrvɪs tʃɑrdʒ ɪnˈkluːdɪd ɪn ðə bɪl/",
        "variants": [
            ["Is service charge included in the bill?", "标准"],
            ["Is the tip included?", "美式问法"],
            ["Is there a service fee?", "问有无服务费"],
        ],
        "scenes": [
            ["结账看单", "Is service charge included in the bill?", "对方回 Yes, 10% is added automatically."],
            ["要不要另给", "Should I leave any extra tip?", "问是否另给小费"],
            ["多收了", "I think we've been overcharged.", "发现多收费"],
        ],
        "grammar": "service charge 服务费（英式餐厅常自动加 10-12.5%）。included in… 含在…里。overcharge 多收费（over- 前缀表过度）。",
        "pron": "连读：Is service→/ɪz ˈsɜrvɪs/；service charge→/ˈsɜrvɪs tʃɑrdʒ/；charge included→/tʃɑrdʒ ɪnˈkluːdɪd/（dʒ 与 ɪ）；included in→/ɪnˈkluː dɪdɪn/；in the→/ɪn ðə/；the bill→/ðə bɪl/。弱读：in the→/ɪn ðə/。失去爆破：included /ɪnˈkluː(d)ɪd/。同化/浊化/缩读：无典型。",
    },
    231: {
        "fullIpa": "/kiːp ðə rɛst æz jʊr tɪp/",
        "variants": [
            ["Keep the rest as your tip.", "标准"],
            ["Keep the change.", "最常用简版！"],
            ["The rest is for you.", "更随意"],
        ],
        "scenes": [
            ["付现不找零", "Keep the change.", "出租车/餐馆通用"],
            ["指定小费", "Here's 100 — keep the rest as your tip.", "给整额当小费"],
            ["不给小费地区", "在中国/日本无需小费，直接付清即可", "文化提示"],
        ],
        "grammar": "Keep the change 是最高频变体（留着零钱别找了）。as your tip『作为你的小费』。rest 此处名词『剩余的钱』。",
        "pron": "连读：Keep the→/kiːp ðə/；the rest→/ðə rɛst/；rest as→/rɛs təz/（t 与 ə）；as your→/əz jər/；your tip→/jər tɪp/。弱读：the→/ðə/、as→/əz/、your→/jər/。失去爆破：rest /rɛs(t)/。同化：rest as→/rɛs təz/（t 与 ə 连读）。浊化：rest as 快读 t→d /rɛs dəz/。缩读：无典型。",
    },
    232: {
        "fullIpa": "/aɪd laɪk ðɪs tə teɪk əˈweɪ pliːz/",
        "variants": [
            ["I'd like this to take away, please.", "标准（英式 take away）"],
            ["To go, please.", "美式最简"],
            ["Could I get this to go?", "美式常用"],
        ],
        "scenes": [
            ["打包外带", "I'd like this to take away, please.", "对方回 Sure, just a moment."],
            ["剩菜打包", "Could you pack this up for me?", "堂食剩菜打包"],
            ["自带杯", "I have my own cup — can you use it?", "环保自带容器"],
        ],
        "grammar": "take away 外带（英式）；to go（美式）。pack up 打包剩菜。I'd like + 名词 + to take away 结构表意图。",
        "pron": "同化/缩读：I'd = I would（/aɪd/）。连读：like this→/laɪk ðɪs/；this to→/ðɪs tə/；to take→/tə teɪk/；take away→/teɪ kəˈweɪ/（k 与 ə 连读）；away please→/əˈweɪ pliːz/。弱读：to→/tə/。失去爆破：like /laɪ(k)/；take /teɪ(k)/。同化/浊化：无典型。",
    },
    233: {
        "fullIpa": "/duː juː duː dɪˈlɪvəri tuː ˈnɪrbaɪ hoʊˈtɛlz/",
        "variants": [
            ["Do you do delivery to nearby hotels?", "标准"],
            ["Do you deliver to hotels around here?", "deliver 动词更简"],
            ["Can you deliver to my hotel?", "指明目的地"],
        ],
        "scenes": [
            ["电话叫外卖", "Do you do delivery to nearby hotels?", "对方回 Yes, what's the room number?"],
            ["问配送费", "Is there a delivery fee?", "问配送费"],
            ["问时间", "How long will it take to arrive?", "问送达时间"],
        ],
        "grammar": "Do you do…? 第一个 do 助动词、第二个 do 实义动词『做/提供』。delivery 配送（名词）；deliver 配送（动词）。nearby 邻近的（形容词，不需 of）。",
        "pron": "缩读：Do you→/dʒə/（两处，缩读关键）。连读：do delivery→/də dɪˈlɪvəri/；delivery to→/dɪˈlɪvəri tə/；to nearby→/tə ˈnɪrbaɪ/；nearby hotels→/ˈnɪrbaɪ hoʊˈtɛlz/。弱读：to→/tə/。同化：Do you→/dʒu/→/dʒə/。失去爆破/浊化：无典型。",
    },
    234: {
        "fullIpa": "/aɪl hæv ə ˈbɜrɡər wɪð fraɪz tə ɡoʊ/",
        "variants": [
            ["I'll have a burger with fries to go.", "标准"],
            ["One burger and fries to go, please.", "更简"],
            ["Burger meal to go, please.", "点套餐带走"],
        ],
        "scenes": [
            ["快餐点单", "I'll have a burger with fries to go.", "对方回 For here or to go?"],
            ["加购", "Could you make it a combo?", "升级套餐"],
            ["饮料确认", "What drink would you like with that?", "问配饮"],
        ],
        "grammar": "I'll have… 点餐万能句。with fries『配薯条』；to go 带走（美式固定说法，作状语）。combo 套餐。",
        "pron": "缩读：I'll = I will（/aɪl/）。连读：have a→/hæ və/；a burger→/ə ˈbɜrɡər/；burger with→/ˈbɜrɡər wɪð/；with fries→/wɪð fraɪz/；fries to→/fraɪz tə/；to go→/tə ɡoʊ/。弱读：with→/wɪð/、to→/tə/、a→/ə/。失去爆破/同化/浊化：无典型。闪音：burger 美式 /ˈbɜɾɚ/（r 元音间闪音趋势）。",
    },
    235: {
        "fullIpa": "/fɔr hɪr ɔr tə ɡoʊ/",
        "variants": [
            ["For here or to go?", "标准（美式服务员问句）"],
            ["Is that for here or to go?", "完整版"],
            ["Are you eating in or taking out?", "英式说法"],
        ],
        "scenes": [
            ["服务员问", "For here or to go?", "客人答 To go, please."],
            ["堂食答", "For here, please.", "堂食"],
            ["犹豫", "Actually, to go — I'm in a hurry.", "改带走"],
        ],
        "grammar": "For here 在店吃；to go 带走（美式）。英式对应：eat in or take away。这是收银员必问句，听懂关键词即可。",
        "pron": "连读：For here→/fər hɪr/（h 音轻）；here or→/hɪ rər/（r 与 ə 连读）；or to→/ər tə/；to go→/tə ɡoʊ/。弱读：For→/fər/、to→/tə/、or→/ər/。失去爆破/同化/浊化/缩读：无典型。",
    },
    236: {
        "fullIpa": "/kʊd aɪ ɡɛt ˈɛkstrə ˈkɛtʃəp ˈpækɪts/",
        "variants": [
            ["Could I get extra ketchup packets?", "标准"],
            ["Can I have some more ketchup?", "更简"],
            ["A few more ketchup packets, please?", "a few 更口语"],
        ],
        "scenes": [
            ["要酱包", "Could I get extra ketchup packets?", "对方回 Sure, how many?"],
            ["要纸巾", "Could I get some napkins, please?", "同理要纸巾"],
            ["自取台", "Where's the condiment station?", "问调料自取台"],
        ],
        "grammar": "extra 额外的（= more）。packet 小包装袋；ketchup packets 番茄酱包。condiment 调味品。",
        "pron": "连读：Could I→/kʊ d aɪ/；I get→/aɪ ɡɛt/；get extra→/ɡɛ tɛkstrə/（t 与 ɛ）；extra ketchup→/ˈɛkstrə ˈkɛtʃəp/；ketchup packets→/ˈkɛtʃəp ˈpækɪts/。弱读：a→/ə/。失去爆破：get /ɡɛ(t)/。同化/浊化/缩读：无典型。",
    },
    237: {
        "fullIpa": "/haʊ mʌtʃ dʌz ðɪs kɔst ɪn ˈtoʊtəl/",
        "variants": [
            ["How much does this cost in total?", "标准"],
            ["What's the total?", "结账时最常用"],
            ["How much all together?", "口语化"],
        ],
        "scenes": [
            ["结账问总价", "How much does this cost in total?", "对方回 That comes to 260 yuan."],
            ["逐项核对", "Could you itemize the bill?", "要求列明细"],
            ["觉得贵", "That seems higher than I expected.", "委婉说贵"],
        ],
        "grammar": "How much does + 主语 + cost…? cost 动词花费。in total 总共（= altogether）。come to『合计为』（结账高频）。",
        "pron": "连读：How much→/haʊ mʌtʃ/；much does→/mʌtʃ dʌz/；does this→/dʌz ðɪs/；this cost→/ðɪs kɔst/（s 与 k）；cost in→/kɔs tɪn/（t 与 ɪ）；in total→/ɪn ˈtoʊtəl/。弱读：does→/dəz/、in→/ɪn/。失去爆破：cost /kɔs(t)/。同化/浊化/缩读：无典型。",
    },
    238: {
        "fullIpa": "/ɪz ðɪs ɑn seɪl æt ðə ˈmoʊmənt/",
        "variants": [
            ["Is this on sale at the moment?", "标准"],
            ["Is this on discount?", "discount 更直白"],
            ["Any deals on this right now?", "deals 更口语"],
        ],
        "scenes": [
            ["问折扣", "Is this on sale at the moment?", "对方回 Yes, 20% off this week."],
            ["问活动截止", "When does the sale end?", "问活动截止"],
            ["要会员价", "Do you have a member price?", "问会员价"],
        ],
        "grammar": "on sale 两义：①打折中（英式/美式通用）②在售（美式）。at the moment『目前』（= right now）。20% off 打八折（off 表减掉的百分比）。",
        "pron": "连读：Is this→/ɪz ðɪs/；this on→/ðɪ sɑn/（s 与 ɑ）；on sale→/ɑn seɪl/；sale at→/seɪ lət/（l 与 ə）；at the→/ət ðə/；the moment→/ðə ˈmoʊmənt/。弱读：at→/ət/、the→/ðə/、is→/ɪz/。失去爆破：at /ə(t)/；moment /ˈmoʊmən(t)/。同化/浊化：无典型。缩读：无典型。",
    },
    239: {
        "fullIpa": "/duː juː hæv ðɪs ʃɜrt ɪn ə ˈmiːdiəm/",
        "variants": [
            ["Do you have this shirt in a medium?", "标准"],
            ["Do you have a medium in this?", "换语序更简"],
            ["Got this in a medium?", "美式极简"],
        ],
        "scenes": [
            ["要尺码", "Do you have this shirt in a medium?", "对方回 Let me check the back."],
            ["尺码表", "What size is this one? / I usually wear L.", "报自己尺码"],
            ["断码", "Sorry, we're out of mediums — only S and XL left.", "缺货说法"],
        ],
        "grammar": "in a medium『有中号的』（in + 尺码/颜色 表『有…款的』）。尺码：S 小 / M 中 / L 大 / XL 特大。out of stock 缺货。",
        "pron": "缩读：Do you→/dʒə/。连读：have this→/hæv ðɪs/；this shirt→/ðɪs ʃɜrt/；shirt in→/ʃɜr tɪn/（t 与 ɪ）；in a→/ɪnə/（连读）；a medium→/ə ˈmiːdiəm/。弱读：in→/ɪn/、a→/ə/。同化：Do you→/dʒu/。失去爆破：shirt /ʃɜr(t)/。浊化/缩读其他：无典型。",
    },
    240: {
        "fullIpa": "/kʊd aɪ traɪ ðiːz ʃuːz ɑn ɪn ə naɪn/",
        "variants": [
            ["Could I try these shoes on in a nine?", "标准"],
            ["Can I try these in a size nine?", "size nine 更清楚"],
            ["Nine in these, please?", "极简"],
        ],
        "scenes": [
            ["要试穿", "Could I try these shoes on in a nine?", "对方回 Of course, have a seat."],
            ["偏小换码", "They're a bit small — do you have a half size up?", "要大半码"],
            ["试穿评价", "They pinch a little at the toe.", "挤脚说法"],
        ],
        "grammar": "try on 试穿（动词短语，代词放中间：try them on）。in a nine『有九码的』（in + 尺码）。half size up 大半码。",
        "pron": "连读：Could I→/kʊ d aɪ/；I try→/aɪ traɪ/；try these→/traɪ ðiːz/；these shoes→/ðiːz ʃuːz/；shoes on→/ʃuː zɑn/（z 与 ɑ）；on in→/ɑ nɪn/；in a→/ɪnə/；a nine→/ə naɪn/。弱读：a→/ə/、in→/ɪn/。失去爆破：Could /kʊ(d)/。同化/浊化/缩读：无典型。",
    },
    241: {
        "fullIpa": "/wɛr ɑr ðə ˈfɪtɪŋ ruːmz pliːz/",
        "variants": [
            ["Where are the fitting rooms, please?", "标准（英式 fitting room）"],
            ["Where's the dressing room?", "美式 dressing room"],
            ["Can I try these on somewhere?", "更随意"],
        ],
        "scenes": [
            ["问试衣间", "Where are the fitting rooms, please?", "对方回 Over there, on your left."],
            ["问能试几件", "How many items can I take in?", "问限带件数"],
            ["排队", "Is there a line for the fitting room?", "试衣间排队"],
        ],
        "grammar": "fitting room 试衣间（英式）；dressing room / changing room（美式/通用）。Where are + 复数名词…? 问位置。",
        "pron": "连读：Where are→/wɛr ər/（r 与 ə 连读）；are the→/ər ðə/；the fitting→/ðə ˈfɪtɪŋ/；fitting rooms→/ˈfɪtɪŋ ruːmz/（ŋ 与 r）；rooms please→/ruːmz pliːz/。弱读：are→/ər/、the→/ðə/。失去爆破/同化/浊化/缩读：无典型。",
    },
    242: {
        "fullIpa": "/ɪts ə bɪt taɪt əˈraʊnd ðə ˈʃoʊldərz/",
        "variants": [
            ["It's a bit tight around the shoulders.", "标准"],
            ["It's a little tight here.", "指位置更简"],
            ["The shoulders are too narrow.", "直接说问题"],
        ],
        "scenes": [
            ["试衣反馈", "It's a bit tight around the shoulders.", "对方回 Let me get you a larger size."],
            ["要大一号", "Could I try one size up?", "要大一号"],
            ["其他问题", "The sleeves are too long.", "袖子太长"],
        ],
        "grammar": "a bit + 形容词『有点…』（比 very 委婉）。tight 紧的 ↔ loose 松的。around the shoulders『肩部周围』。size up 大一号 / size down 小一号。",
        "pron": "缩读：It's = It is（/ɪts/）。连读：a bit→/ə bɪt/；bit tight→/bɪ(t) taɪt/（t 与 t 重叠只读一次）；tight around→/taɪ təˈraʊnd/（t 与 ə）；around the→/əˈraʊn(d) ðə/；the shoulders→/ðə ˈʃoʊldərz/。弱读：a→/ə/、the→/ðə/。失去爆破：It's /ɪts/；around /əˈraʊn(d)/。同化/浊化：无典型。缩读：无典型。",
    },
    243: {
        "fullIpa": "/duː juː hæv ɪt ɪn ˈɛni ˈʌðər ˈkʌlərz/",
        "variants": [
            ["Do you have it in any other colors?", "标准"],
            ["What other colors does it come in?", "come in 问款式更地道"],
            ["Got this in black?", "直接点名颜色"],
        ],
        "scenes": [
            ["问色号", "Do you have it in any other colors?", "对方回 We have black and navy."],
            ["指名要色", "I'd like it in white, please.", "要白色"],
            ["看实物", "Could you show me the navy one?", "请拿来看"],
        ],
        "grammar": "in + 颜色『有…色的』。come in + 颜色『有…色款』。any other + 复数名词『其他任何…』。",
        "pron": "缩读：Do you→/dʒə/。连读：have it→/hæ vɪt/（v 与 ɪ）；it in→/ɪ tɪn/（t 与 ɪ）；in any→/ɪ nɛni/（n 与 ɛ）；any other→/ˈɛni ˈʌðər/；other colors→/ˈʌðər ˈkʌlərz/。弱读：it→/ɪt/、in→/ɪn/、any→/ˈɛni/。同化：Do you→/dʒu/。闪音：other 美式 /ˈʌðɚ/（轻闪趋势）。失去爆破/浊化：无典型。",
    },
    244: {
        "fullIpa": "/ðɪs wʌn suːts juː ˈrɪli wɛl/",
        "variants": [
            ["This one suits you really well.", "标准"],
            ["That looks great on you.", "look good on sb 更常用"],
            ["It's very flattering.", "flattering 显气质，高级说法"],
        ],
        "scenes": [
            ["陪同购物夸赞", "This one suits you really well.", "对方回 You think so? I'll take it."],
            ["试衣间外评价", "That color really matches your skin tone.", "夸颜色衬肤色"],
            ["劝别买", "Honestly, the other one looks better on you.", "委婉劝选另一件"],
        ],
        "grammar": "suit(v.) 适合（衣服合身/风格衬）；注意与 suit(n.) 西装区分。look + adj. + on somebody『穿在某人身上显得…』。match 配衬。",
        "pron": "连读：This one→/ðɪs wʌn/；one suits→/wʌn suːts/（n 与 s）；suits you→/suːtʃu/（t+j 同化为 tʃ，关键！）；you really→/ju ˈrɪli/；really well→/ˈrɪli wɛl/。弱读：you→/jə/。同化：suits you→/suːtʃu/（t+j→tʃ）。浊化/失去爆破/缩读：无典型。",
    },
    245: {
        "fullIpa": "/kʊd juː ɡɪv miː ə ˈbɛtər praɪs ɪf aɪ baɪ tuː/",
        "variants": [
            ["Could you give me a better price if I buy two?", "标准"],
            ["Any discount if I buy two?", "更简"],
            ["Is there a deal for buying two?", "deal 口语"],
        ],
        "scenes": [
            ["讲价", "Could you give me a better price if I buy two?", "对方回 I can do 10% off for two."],
            ["市场砍价", "What's your best price?", "问最低价"],
            ["批发价", "Do you give a bulk discount?", "问批量折扣"],
        ],
        "grammar": "give me a better price『给个更优惠的价』；better price = discount。if I buy two 条件句（主句 could 表委婉请求）。bulk discount 批量折扣。",
        "pron": "连读：Could you→/kʊ dʒu/（同化）；give me→/ɡɪv mi/；me a→/miə/（连读）；a better→/ə ˈbɛtər/；better price→/ˈbɛtər praɪs/；price if→/praɪ sɪf/（s 与 ɪ）；if I→/ɪ faɪ/；I buy→/aɪ baɪ/；buy two→/baɪ tu/（aɪ 与 t）。弱读：a→/ə/、if→/ɪf/、me→/mɪ/。同化：Could you→/kʊdʒu/（关键）。闪音：better 美式 /ˈbɛɾɚ/（t 闪音化，关键！）。失去爆破/缩读：无典型。",
    },
    246: {
        "fullIpa": "/ðæts ə bɪt ˈoʊvər maɪ ˈbʌdʒɪt ˈɑnɪstli/",
        "variants": [
            ["That's a bit over my budget, honestly.", "标准"],
            ["That's more than I wanted to spend.", "更委婉"],
            ["It's a little pricey for me.", "pricey 口语『贵』"],
        ],
        "scenes": [
            ["委婉拒绝", "That's a bit over my budget, honestly.", "对方回 I have something in a lower range."],
            ["请推荐平价", "Could you show me something cheaper?", "请推荐便宜的"],
            ["砍价铺垫", "If you can bring it down a bit, I'll take it.", "降价就买"],
        ],
        "grammar": "over my budget『超出我的预算』（over=超过）。honestly 句尾副词，表坦诚（软化拒绝）。pricey = expensive 的口语版。",
        "pron": "缩读：That's = That is（/ðæts/）。连读：That's a→/ðæ(t) sə/；a bit→/ə bɪt/；bit over→/bɪ tˈoʊvər/（t 与 ə）；over my→/ˈoʊvər maɪ/；my budget→/maɪ ˈbʌdʒɪt/；budget honestly→/ˈbʌdʒɪ təˈɑnɪstli/（t 与 ə）。弱读：a→/ə/。失去爆破：That's /ðæ(t)s/；budget /ˈbʌdʒɪ(t)/。同化/浊化：无典型。",
    },
    247: {
        "fullIpa": "/kæn aɪ peɪ baɪ kɑːrd ɔr ɪz ɪt kæʃ ˈoʊnli/",
        "variants": [
            ["Can I pay by card or is it cash only?", "标准"],
            ["Do you take credit cards?", "更简"],
            ["Card or cash only?", "极简问法"],
        ],
        "scenes": [
            ["问支付方式", "Can I pay by card or is it cash only?", "对方回 Both work."],
            ["国外刷 Visa", "Do you accept Visa or Mastercard?", "问卡组织"],
            ["找零确认", "Could I get a receipt?", "要收据"],
        ],
        "grammar": "pay by card『刷卡支付』（by + 方式，不加 the）。cash only『只收现金』（only 后置修饰 cash）。accept = take 收（支付方式）。",
        "pron": "连读：Can I→/kæn aɪ/；I pay→/aɪ peɪ/；pay by→/peɪ baɪ/；by card→/baɪ kɑːrd/；card or→/kɑːr dər/（r 与 ə）；or is→/ər ɪz/；is it→/ɪ zɪt/（z 与 ɪ）；it cash→/ɪ(t) kæʃ/；cash only→/kæʃ ˈoʊnli/。弱读：or→/ər/、is→/ɪz/、it→/ɪt/。失去爆破：it /ɪ(t)/。同化/浊化/缩读：无典型。",
    },
    248: {
        "fullIpa": "/duː juː teɪk ˈmoʊbəl ˈpeɪmənt laɪk ˈæləpeɪ/",
        "variants": [
            ["Do you take mobile payment like Alipay?", "标准"],
            ["Can I pay with Alipay or WeChat Pay?", "具体点名更实用"],
            ["Do you accept QR code payment?", "扫码支付"],
        ],
        "scenes": [
            ["问扫码支付", "Do you take mobile payment like Alipay?", "对方回 Sure, scan the QR code here."],
            ["境外使用", "Does Alipay work here?", "问境外能否用"],
            ["刷脸支付", "Can I pay with face recognition?", "刷脸"],
        ],
        "grammar": "take/accept + 支付方式『收…』。mobile payment 移动支付。like Alipay『像支付宝这类』（like 表举例）。pay with + 工具（with 接具体工具，by 接方式）。",
        "pron": "缩读：Do you→/dʒə/。连读：take mobile→/teɪk ˈmoʊbəl/（k 与 m）；mobile payment→/ˈmoʊbəl ˈpeɪmənt/；payment like→/ˈpeɪmən(t) laɪk/；like Alipay→/laɪk ˈæləpeɪ/。弱读：无典型。同化：Do you→/dʒu/。失去爆破：payment /ˈpeɪmən(t)/；take /teɪ(k)/。浊化/缩读其他：无典型。",
    },
    249: {
        "fullIpa": "/kʊd aɪ ɡɛt ə tæks ˈrifʌnd fɔrm fɔr ðɪs/",
        "variants": [
            ["Could I get a tax refund form for this?", "标准"],
            ["Can I claim a tax refund on this?", "claim 申领"],
            ["Do you do tax-free shopping?", "问有无退税服务"],
        ],
        "scenes": [
            ["要退税单", "Could I get a tax refund form for this?", "对方回 Sure, may I see your passport?"],
            ["机场退税", "Where's the tax refund counter at the airport?", "问退税柜台"],
            ["退税条件", "What's the minimum amount for a refund?", "问起退金额"],
        ],
        "grammar": "tax refund 退税；refund form 退税单。claim a refund 申领退款。tax-free shopping 免税购物。minimum amount 起退金额。",
        "pron": "连读：Could I→/kʊ d aɪ/；I get→/aɪ ɡɛt/；get a→/ɡɛ tə/；a tax→/ə tæks/；tax refund→/tæks ˈrifʌnd/（s 与 r）；refund form→/ˈrifʌnd fɔrm/（d 与 f）；form for→/fɔrm fər/；for this→/fər ðɪs/。弱读：a→/ə/、for→/fər/。同化：无典型。失去爆破：get /ɡɛ(t)/。浊化/缩读：无典型。",
    },
    250: {
        "fullIpa": "/aɪd laɪk tə rɪˈtɜrn ðɪs ˈdʒækɪt wɪð ðə rɪˈsiːt/",
        "variants": [
            ["I'd like to return this jacket with the receipt.", "标准"],
            ["I want to return this — here's the receipt.", "更直接"],
            ["Can I get a refund for this jacket?", "直接要退款"],
        ],
        "scenes": [
            ["退货", "I'd like to return this jacket with the receipt.", "对方回 Any problem with it?"],
            ["换货", "Could I exchange it for a larger size?", "换大一号"],
            ["只退款不换", "I'd just like a refund, please.", "只要退款"],
        ],
        "grammar": "return 退回；exchange 换货；refund 退款（三个动词必分清）。with the receipt『凭收据』（凭凭证用 with）。get a refund 拿到退款。",
        "pron": "同化/缩读：I'd = I would（/aɪd/）。连读：like to→/laɪk tə/；to return→/tə rɪˈtɜrn/；return this→/rɪˈtɜrn ðɪs/（n 与 ð）；this jacket→/ðɪs ˈdʒækɪt/；jacket with→/ˈdʒækɪ(t) wɪð/；with the→/wɪð ðə/；the receipt→/ðə rɪˈsiːt/。弱读：to→/tə/、the→/ðə/。浊化：like to 快读 t→d /laɪ də/。失去爆破：like /laɪ(k)/；jacket /ˈdʒækɪ(t)/。注意：receipt 的 p 不发音 /rɪˈsiːt/（关键！）。",
    },
}
