# -*- coding: utf-8 -*-
"""确定性排盘引擎 — 四柱、十神、五行、藏干、大运、流年。

核心原则（来自规划）：所有历法转换与干支推算由代码完成，模型绝不手算四柱。
输出 JSON 结构对齐规划的 1.2 节契约。
"""
from datetime import datetime
from lunar_python import Solar, Lunar, EightChar

from geo import true_solar_time

GAN = "甲乙丙丁戊己庚辛壬癸"
ZHI = "子丑寅卯辰巳午未申酉戌亥"
WUXING_OF_GAN = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
                 "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"}
WUXING_OF_ZHI = {"子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火",
                 "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水"}
YINYANG_OF_GAN = {"甲": "阳", "乙": "阴", "丙": "阳", "丁": "阴", "戊": "阳",
                  "己": "阴", "庚": "阳", "辛": "阴", "壬": "阳", "癸": "阴"}

TEN_GODS_MAP = {}  # (day_gan, other_gan) -> 十神


def _build_ten_gods():
    """按五行生克+阴阳构建十神表。"""
    sheng = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}   # 我生
    ke = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}     # 我克
    for d in GAN:
        for o in GAN:
            dw, ow = WUXING_OF_GAN[d], WUXING_OF_GAN[o]
            same_polarity = YINYANG_OF_GAN[d] == YINYANG_OF_GAN[o]
            if dw == ow:
                god = "比肩" if same_polarity else "劫财"
            elif sheng[dw] == ow:
                god = "食神" if same_polarity else "伤官"
            elif ke[dw] == ow:
                god = "偏财" if same_polarity else "正财"
            elif ke[ow] == dw:
                god = "七杀" if same_polarity else "正官"
            elif sheng[ow] == dw:
                god = "偏印" if same_polarity else "正印"
            TEN_GODS_MAP[(d, o)] = god


_build_ten_gods()


def ten_god(day_gan: str, other_gan: str) -> str:
    return TEN_GODS_MAP[(day_gan, other_gan)]


def _zhi_zhu(zhi: str) -> str:
    """支中人元十神 → '正官' 形式（对日干）。"""
    return ten_god


def lunar_from_input(year, month, day, hour, minute, calendar_type="gregorian",
                     is_leap_month=False):
    if calendar_type == "lunar":
        lunar = Lunar.fromYmdHms(year, month, day, hour, minute, 0)
        if is_leap_month:
            # lunar-python 通过负数月表达闰月
            lunar = Lunar.fromYmdHms(year, -month, day, hour, minute, 0)
        solar = lunar.getSolar()
    else:
        solar = Solar.fromYmdHms(year, month, day, hour, minute, 0)
        lunar = solar.getLunar()
    return solar, lunar


def paipan(year: int, month: int, day: int, hour: int, minute: int,
           gender: str, city: str = "", calendar_type: str = "gregorian",
           is_leap_month: bool = False) -> dict:
    """主入口：输出规划 1.2 节契约的 JSON 命盘。

    gender: "男"/"M"/"male" 或 "女"/"F"/"female"
    """
    g = str(gender).strip()
    male = g in ("男", "M", "m", "male", "Male", "1")

    dt = datetime(year, month, day, hour, minute)
    adj_dt, tst_note, tst_applied = true_solar_time(dt, city)

    solar, lunar = lunar_from_input(
        adj_dt.year, adj_dt.month, adj_dt.day, adj_dt.hour, adj_dt.minute,
        calendar_type, is_leap_month)
    ec = lunar.getEightChar()
    ec.setSect(2)  # 晚子时日柱算当天（规划固定流派约定）

    y = ec.getYear(); m = ec.getMonth(); d = ec.getDay(); h = ec.getTime()
    day_gan = d[0]

    # ----- 四柱与十神 -----
    pillars = {
        "year_pillar": y, "month_pillar": m, "day_pillar": d, "hour_pillar": h,
        "day_master": day_gan + WUXING_OF_GAN[day_gan],
    }

    # 日主旺衰：得令/得地/得助 三项速判（说明性结论，供校准层修正）
    month_zhi = m[1]
    dm_wuxing = WUXING_OF_GAN[day_gan]
    # 生我者（月支为印星：当令且生身，算得令）
    SHENG_BY = {"木": "水", "火": "木", "土": "火", "金": "土", "水": "金"}
    season_support = WUXING_OF_ZHI[month_zhi] in (dm_wuxing, SHENG_BY[dm_wuxing])
    branch_gens = [ec.getYearHideGan(), ec.getMonthHideGan(),
                   ec.getDayHideGan(), ec.getTimeHideGan()]
    has_root = any(day_gan in hg for hg in branch_gens)
    helper = [GAN[i] for i in range(10)
              if WUXING_OF_GAN[GAN[i]] == dm_wuxing and GAN[i] != day_gan]
    stems = [y[0], m[0], h[0]]
    has_helper = any(s in helper for s in stems)
    score = sum([season_support, has_root, has_helper])
    strength = "身强" if score >= 2 else ("身弱" if score <= 1 else "中和")

    shi_shen = {
        "year_stem": ten_god(day_gan, y[0]),
        "month_stem": ten_god(day_gan, m[0]),
        "day_stem": "日主",
        "hour_stem": ten_god(day_gan, h[0]),
        "year_branch": ten_god(day_gan, ec.getYearHideGan()[0]),
        "month_branch": ten_god(day_gan, ec.getMonthHideGan()[0]),
        "day_branch": ten_god(day_gan, ec.getDayHideGan()[0]),
        "hour_branch": ten_god(day_gan, ec.getTimeHideGan()[0]),
    }

    # ----- 五行统计（含藏干加权：本气1.0 中气0.6 余气0.3）-----
    wuxing = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
    for zhi in [y[1], m[1], d[1], h[1]]:
        wuxing[WUXING_OF_ZHI[zhi]] += 1.0
    for hg, w in [(ec.getYearHideGan(), (1.0, 0.6, 0.3)),
                  (ec.getMonthHideGan(), (1.0, 0.6, 0.3)),
                  (ec.getDayHideGan(), (1.0, 0.6, 0.3)),
                  (ec.getTimeHideGan(), (1.0, 0.6, 0.3))]:
        for gan, wt in zip(hg, w):
            wuxing[WUXING_OF_GAN[gan]] += wt
    wuxing = {k: round(v, 1) for k, v in wuxing.items()}

    hidden_stems = {
        "year_branch": "".join(ec.getYearHideGan()),
        "month_branch": "".join(ec.getMonthHideGan()),
        "day_branch": "".join(ec.getDayHideGan()),
        "hour_branch": "".join(ec.getTimeHideGan()),
    }

    # ----- 大运（男阳/女阴顺排，男阴/女阳逆排）-----
    yun = ec.getYun(1 if male else 0)
    start_year_offset = yun.getStartYear()
    start_month_offset = yun.getStartMonth()
    dayun_list = yun.getDaYun()
    da_yun = []
    for i, dy in enumerate(dayun_list[:10]):
        if i == 0:
            continue  # 起运前的幼年段
        da_yun.append({
            "index": i,
            "age_start": dy.getStartYear() - (solar.getYear() - yun.getBirthYear()) if False else dy.getStartYear() - solar.getYear(),
            "start_year": dy.getStartYear(),
            "end_year": dy.getEndYear() - 1,
            "ganzhi": dy.getGanZhi(),
        })

    # ----- 流年（当前大运前后 20 年）-----
    now_year = datetime.now().year
    liu_nian = []
    for yy in range(now_year - 10, now_year + 11):
        offset = (yy - 4) % 60
        liu_nian.append({"year": yy, "ganzhi": GAN[offset % 10] + ZHI[offset % 12]})

    result = {
        "input": {
            "birth": f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}",
            "calendar_type": calendar_type,
            "is_leap_month": is_leap_month,
            "gender": "男" if male else "女",
            "city": city,
        },
        "true_solar_time": {
            "applied": tst_applied,
            "note": tst_note,
            "adjusted_time": f"{adj_dt:%Y-%m-%d %H:%M}",
        },
        "bazi": pillars,
        "day_master_strength": strength,
        "strength_basis": {
            "得令": season_support, "得地": has_root, "得助": has_helper,
        },
        "shi_shen": shi_shen,
        "wu_xing": wuxing,
        "hidden_stems": hidden_stems,
        "da_yun": da_yun,
        "liu_nian": liu_nian,
        "start_yun": {
            "years": start_year_offset, "months": start_month_offset,
            "note": f"出生后约 {start_year_offset} 年 {start_month_offset} 个月起运",
        },
    }
    return result
