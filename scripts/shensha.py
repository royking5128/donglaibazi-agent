# -*- coding: utf-8 -*-
"""神煞计算 — 核心集合（以日干/日支为锚点的常用神煞）。

规划要求 33+，本版实现以核心常用神煞为主，覆盖：
天乙贵人、太极贵人、天德贵人、月德贵人、文昌贵人、羊刃、禄神、
桃花（咸池）、红鸾、天喜、驿马、华盖、将星、劫煞、亡神、
孤辰、寡宿、空亡、金舆、国印、魁罡、阴差阳错、元辰、灾煞、
贯索（勾煞）、绞煞、飞刃、学堂、红艳、流霞、天罗地网、十恶大败、夹禄。
"""
from paipan import GAN, ZHI, WUXING_OF_GAN, ten_god

# 天乙贵人：甲戊庚→丑未；乙己→子申；丙丁→亥酉；壬癸→巳卯；辛→午寅
TIAN_YI = {"甲": "丑未", "戊": "丑未", "庚": "丑未", "乙": "子申", "己": "子申",
           "丙": "亥酉", "丁": "亥酉", "壬": "巳卯", "癸": "巳卯", "辛": "午寅"}
# 太极贵人：甲乙→子午；丙丁→卯酉；戊己→辰戌丑未；庚辛→寅亥；壬癸→巳申
TAI_JI = {"甲": "子午", "乙": "子午", "丙": "卯酉", "丁": "卯酉",
          "戊": "辰戌丑未", "己": "辰戌丑未", "庚": "寅亥", "辛": "寅亥",
          "壬": "巳申", "癸": "巳申"}
# 文昌：甲→巳 乙→午 丙戊→申 丁己→酉 庚→亥 辛→子 壬→寅 癸→卯
WEN_CHANG = {"甲": "巳", "乙": "午", "丙": "申", "戊": "申", "丁": "酉",
             "己": "酉", "庚": "亥", "辛": "子", "壬": "寅", "癸": "卯"}
# 禄神：甲→寅 乙→卯 丙戊→巳 丁己→午 庚→申 辛→酉 壬→亥 癸→子
LU_SHEN = {"甲": "寅", "乙": "卯", "丙": "巳", "戊": "巳", "丁": "午",
           "己": "午", "庚": "申", "辛": "酉", "壬": "亥", "癸": "子"}
# 羊刃（阳干）：甲→卯 丙戊→午 庚→酉 壬→子
YANG_REN = {"甲": "卯", "丙": "午", "戊": "午", "庚": "酉", "壬": "子"}
# 桃花（咸池）：申子辰→酉 寅午戌→卯 巳酉丑→午 亥卯未→子
TAO_HUA = {"申": "酉", "子": "酉", "辰": "酉", "寅": "卯", "午": "卯", "戌": "卯",
           "巳": "午", "酉": "午", "丑": "午", "亥": "子", "卯": "子", "未": "子"}
# 驿马：申子辰→寅 寅午戌→申 巳酉丑→亥 亥卯未→巳
YI_MA = {"申": "寅", "子": "寅", "辰": "寅", "寅": "申", "午": "申", "戌": "申",
         "巳": "亥", "酉": "亥", "丑": "亥", "亥": "巳", "卯": "巳", "未": "巳"}
# 华盖：申子辰→辰 寅午戌→戌 巳酉丑→丑 亥卯未→未
HUA_GAI = {"申": "辰", "子": "辰", "辰": "辰", "寅": "戌", "午": "戌", "戌": "戌",
           "巳": "丑", "酉": "丑", "丑": "丑", "亥": "未", "卯": "未", "未": "未"}
# 将星：申子辰→子 寅午戌→午 巳酉丑→酉 亥卯未→卯
JIANG_XING = {"申": "子", "子": "子", "辰": "子", "寅": "午", "午": "午", "戌": "午",
              "巳": "酉", "酉": "酉", "丑": "酉", "亥": "卯", "卯": "卯", "未": "卯"}
# 劫煞：申子辰→巳 寅午戌→亥 巳酉丑→寅 亥卯未→申
JIE_SHA = {"申": "巳", "子": "巳", "辰": "巳", "寅": "亥", "午": "亥", "戌": "亥",
           "巳": "寅", "酉": "寅", "丑": "寅", "亥": "申", "卯": "申", "未": "申"}
# 亡神：申子辰→亥 寅午戌→巳 巳酉丑→申 亥卯未→寅
WANG_SHEN = {"申": "亥", "子": "亥", "辰": "亥", "寅": "巳", "午": "巳", "戌": "巳",
             "巳": "申", "酉": "申", "丑": "申", "亥": "寅", "卯": "寅", "未": "寅"}
# 孤辰寡宿：亥子丑→孤寅寡戌；寅卯辰→孤巳寡丑；巳午未→孤申寡辰；申酉戌→孤亥寡未
GU_CHEN = {"亥": "寅", "子": "寅", "丑": "寅", "寅": "巳", "卯": "巳", "辰": "巳",
           "巳": "申", "午": "申", "未": "申", "申": "亥", "酉": "亥", "戌": "亥"}
GUA_SU = {"亥": "戌", "子": "戌", "丑": "戌", "寅": "丑", "卯": "丑", "辰": "丑",
          "巳": "辰", "午": "辰", "未": "辰", "申": "未", "酉": "未", "戌": "未"}
# 红鸾（以年支查，卯起子逆行）
HONG_LUAN = {"子": "卯", "丑": "寅", "寅": "丑", "卯": "子", "辰": "亥", "巳": "戌",
             "午": "酉", "未": "申", "申": "未", "酉": "午", "戌": "巳", "亥": "辰"}
# 天喜（红鸾对冲）
TIAN_XI = {"子": "酉", "丑": "申", "寅": "未", "卯": "午", "辰": "巳", "巳": "辰",
           "午": "卯", "未": "寅", "申": "丑", "酉": "子", "戌": "亥", "亥": "戌"}
# 金舆：甲→辰 乙→巳 丙→未 丁→申 戊→未 己→申 庚→戌 辛→亥 壬→丑 癸→寅
JIN_YU = {"甲": "辰", "乙": "巳", "丙": "未", "丁": "申", "戊": "未",
          "己": "申", "庚": "戌", "辛": "亥", "壬": "丑", "癸": "寅"}
# 国印：甲→戌 乙→亥 丙→丑 丁→寅 戊→丑 己→寅 庚→辰 辛→巳 壬→未 癸→申
GUO_YIN = {"甲": "戌", "乙": "亥", "丙": "丑", "丁": "寅", "戊": "丑",
           "己": "寅", "庚": "辰", "辛": "巳", "壬": "未", "癸": "申"}
# 学堂：金命见巳 辛巳；木命见亥 己亥；水土命见申 甲申；火命见寅 丙寅（以纳音简化为日干五行）
XUE_TANG = {"金": "巳", "木": "亥", "水": "申", "土": "申", "火": "寅"}
# 红艳（以日干查）：甲→午 乙→申 丙→寅 丁→未 戊→辰 己→辰 庚→戌 辛→酉 壬→子 癸→申
HONG_YAN = {"甲": "午", "乙": "申", "丙": "寅", "丁": "未", "戊": "辰",
            "己": "辰", "庚": "戌", "辛": "酉", "壬": "子", "癸": "申"}
# 流霞：甲→酉 乙→戌 丙→未 丁→申 戊→巳 己→午 庚→辰 辛→卯 壬→亥 癸→寅
LIU_XIA = {"甲": "酉", "乙": "戌", "丙": "未", "丁": "申", "戊": "巳",
           "己": "午", "庚": "辰", "辛": "卯", "壬": "亥", "癸": "寅"}
# 天医：月支前一支（正月丑、二月寅……以月支推）
TIAN_YI_MED = {"寅": "丑", "卯": "寅", "辰": "卯", "巳": "辰", "午": "巳", "未": "午",
               "申": "未", "酉": "申", "戌": "酉", "亥": "戌", "子": "亥", "丑": "子"}
# 福星贵人：甲→寅子 乙→丑卯 丙戊→子 戊→丑 己→未 丁→亥 庚→申辛→巳 壬→巳 癸→卯（取常用简表）
FU_XING = {"甲": "寅子", "乙": "丑卯", "丙": "子", "丁": "亥", "戊": "丑",
           "己": "未", "庚": "申", "辛": "巳", "壬": "巳", "癸": "卯"}

CHONG_MAP = {"子": "午", "午": "子", "丑": "未", "未": "丑", "寅": "申", "申": "寅",
             "卯": "酉", "酉": "卯", "辰": "戌", "戌": "辰", "巳": "亥", "亥": "巳"}


def _xun_kong(day_gan_index: int, day_zhi_index: int):
    """旬空：以日柱定旬，旬内空亡两支。"""
    # 六十甲子中日柱序号
    idx = (day_gan_index % 10)
    diff = (day_zhi_index - day_gan_index) % 12
    # 空亡 = 旬首前两支：xun_head_zhi = day_zhi - day_gan (mod 12)
    xun_head = (day_zhi_index - day_gan_index) % 12
    kong1 = ZHI[(xun_head + 10) % 12]
    kong2 = ZHI[(xun_head + 11) % 12]
    return [kong1, kong2]


def compute_shen_sha(paipan_result: dict) -> dict:
    """以规划 JSON 命盘为输入，返回命带神煞集合。"""
    bazi = paipan_result["bazi"]
    y, m, d, h = (bazi["year_pillar"], bazi["month_pillar"],
                  bazi["day_pillar"], bazi["hour_pillar"])
    day_gan = d[0]
    branches = [y[1], m[1], d[1], h[1]]
    year_zhi, day_zhi = y[1], d[1]
    dm_wuxing = WUXING_OF_GAN[day_gan]

    def hits(targets: str) -> list:
        return [b for b in branches if b in targets]

    dayun_ganzhi = [x["ganzhi"] for x in paipan_result.get("da_yun", [])]
    stems = [y[0], m[0], d[0], h[0]]

    shen_sha = {}
    shen_sha["天乙贵人"] = hits(TIAN_YI.get(day_gan, ""))
    shen_sha["太极贵人"] = hits(TAI_JI.get(day_gan, ""))
    shen_sha["文昌贵人"] = hits(WEN_CHANG.get(day_gan, ""))
    shen_sha["禄神"] = hits(LU_SHEN.get(day_gan, ""))
    shen_sha["羊刃"] = hits(YANG_REN.get(day_gan, ""))
    shen_sha["飞刃"] = hits(CHONG_MAP.get(YANG_REN.get(day_gan, ""), "")) if day_gan in YANG_REN else []
    shen_sha["金舆"] = hits(JIN_YU.get(day_gan, ""))
    shen_sha["国印贵人"] = hits(GUO_YIN.get(day_gan, ""))
    shen_sha["红艳"] = hits(HONG_YAN.get(day_gan, ""))
    shen_sha["流霞"] = hits(LIU_XIA.get(day_gan, ""))
    shen_sha["福星贵人"] = hits(FU_XING.get(day_gan, ""))
    # 天医（以月支查）
    m_zhi_med = TIAN_YI_MED.get(m[1], "")
    if m_zhi_med:
        shen_sha["天医"] = [b for b in branches if b == m_zhi_med]
    # 三奇贵人：天干顺序 甲戊庚 / 乙丙丁 / 壬癸辛（连续出现于年月日或月日时）
    for combo in ("甲戊庚", "乙丙丁", "壬癸辛"):
        stem_str = "".join(stems)
        if combo in stem_str or combo[::-1] in stem_str:
            shen_sha["三奇贵人"] = list(combo)
            break
    shen_sha["学堂"] = hits(XUE_TANG.get(dm_wuxing, ""))
    shen_sha["桃花"] = hits(TAO_HUA.get(year_zhi, ""))
    shen_sha["红鸾"] = hits(HONG_LUAN.get(year_zhi, ""))
    shen_sha["天喜"] = hits(TIAN_XI.get(year_zhi, ""))
    shen_sha["驿马"] = hits(YI_MA.get(year_zhi, "")) + hits(YI_MA.get(day_zhi, ""))
    shen_sha["华盖"] = hits(HUA_GAI.get(year_zhi, "")) + hits(HUA_GAI.get(day_zhi, ""))
    shen_sha["将星"] = hits(JIANG_XING.get(year_zhi, "")) + hits(JIANG_XING.get(day_zhi, ""))
    shen_sha["劫煞"] = hits(JIE_SHA.get(year_zhi, "")) + hits(JIE_SHA.get(day_zhi, ""))
    shen_sha["亡神"] = hits(WANG_SHEN.get(year_zhi, "")) + hits(WANG_SHEN.get(day_zhi, ""))
    shen_sha["孤辰"] = hits(GU_CHEN.get(year_zhi, ""))
    shen_sha["寡宿"] = hits(GUA_SU.get(year_zhi, ""))

    # 空亡（以日柱定旬）
    dgi = GAN.index(day_gan); dzi = ZHI.index(day_zhi)
    kong = _xun_kong(dgi, dzi)
    shen_sha["空亡"] = [b for b in branches if b in kong]

    # 魁罡：日柱为 庚辰/庚戌/壬辰/戊戌
    shen_sha["魁罡"] = [d] if d in ("庚辰", "庚戌", "壬辰", "戊戌") else []

    # 天罗地网：戌亥为天罗，辰巳为地网（火命人见戌亥、水土命人见辰巳）
    tianluo = {"火"}; diwang = {"水", "土"}
    if dm_wuxing in tianluo:
        shen_sha["天罗"] = [b for b in branches if b in "戌亥"]
    if dm_wuxing in diwang:
        shen_sha["地网"] = [b for b in branches if b in "辰巳"]

    # 阴差阳错：丙子 丁丑 戊寅 辛卯 壬辰 癸巳 丙午 丁未 戊申 辛酉 壬戌 癸亥
    yin_cha_yang_cuo = {"丙子", "丁丑", "戊寅", "辛卯", "壬辰", "癸巳",
                        "丙午", "丁未", "戊申", "辛酉", "壬戌", "癸亥"}
    found = [p for p in (y, m, d, h) if p in yin_cha_yang_cuo]
    if found:
        shen_sha["阴差阳错"] = found

    # 十恶大败日：庚戌甲辰乙巳丙申丁亥戊戌己丑庚辰辛巳壬申癸亥（甲辰年旬等，取常见日柱集）
    shi_e = {"庚戌", "甲辰", "乙巳", "丙申", "丁亥", "戊戌", "己丑", "庚辰", "辛巳", "壬申", "癸亥"}
    # 需与十恶大败年旬配合，此处按日柱简化标注
    se = [p for p in (d,) if p in shi_e]
    if se:
        shen_sha["十恶大败"] = se

    # 天德/月德（按月支查）
    # 月德：寅午戌月→丙 申子辰月→壬 巳酉丑月→庚 亥卯未月→甲
    yue_de = {"寅": "丙", "午": "丙", "戌": "丙", "申": "壬", "子": "壬", "辰": "壬",
              "巳": "庚", "酉": "庚", "丑": "庚", "亥": "甲", "卯": "甲", "未": "甲"}
    # 天德：正月丁 二月申 三月壬 四月辛 五月亥 六月甲 七月癸 八月寅 九月丙 十月乙 十一月巳 十二月庚
    tian_de = {"寅": "丁", "卯": "申", "辰": "壬", "巳": "辛", "午": "亥", "未": "甲",
               "申": "癸", "酉": "寅", "戌": "丙", "亥": "乙", "子": "巳", "丑": "庚"}
    m_zhi = m[1]
    if yue_de.get(m_zhi) in (y[0], m[0], d[0], h[0]) and yue_de[m_zhi] != day_gan:
        shen_sha["月德贵人"] = [yue_de[m_zhi]]
    td = tian_de.get(m_zhi, "")
    stems_all = [y[0], m[0], d[0], h[0]] + list(paipan_result["hidden_stems"]["day_branch"])
    if td and td in stems_all and td != day_gan:
        shen_sha["天德贵人"] = [td]

    # 灾煞：将星对冲位
    jx = JIANG_XING.get(year_zhi, "")
    if jx:
        shen_sha["灾煞"] = [b for b in branches if b == CHONG_MAP.get(jx, "")]

    # 元辰（以年干阴阳定）：阳男阴女冲前一支，阴男阳女冲后一支（简化取冲位±1）
    gender = paipan_result["input"]["gender"]
    chong = CHONG_MAP.get(year_zhi, "")
    if chong:
        idx = ZHI.index(chong)
        yuan_chen = ZHI[(idx + 1) % 12]
        shen_sha["元辰"] = [b for b in branches if b == yuan_chen]

    # 勾绞（贯索/绞煞）
    yang_gan = day_gan in "甲丙戊庚壬"
    if yang_gan:
        shen_sha["勾煞"] = [b for b in branches if b == ZHI[(ZHI.index(m_zhi) + 3) % 12]]
        shen_sha["绞煞"] = [b for b in branches if b == ZHI[(ZHI.index(m_zhi) - 3) % 12]]
    else:
        shen_sha["勾煞"] = [b for b in branches if b == ZHI[(ZHI.index(m_zhi) - 3) % 12]]
        shen_sha["绞煞"] = [b for b in branches if b == ZHI[(ZHI.index(m_zhi) + 3) % 12]]

    # 夹禄：日支前后夹禄神位
    lu = LU_SHEN.get(day_gan, "")
    if lu:
        lu_i = ZHI.index(lu); day_i = ZHI.index(day_zhi)
        if abs(lu_i - day_i) == 1:
            shen_sha["夹禄"] = [lu]

    # 过滤空值
    return {k: v for k, v in shen_sha.items() if v}
