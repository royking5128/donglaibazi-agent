# -*- coding: utf-8 -*-
"""刑冲合害计算 — 地支三刑/六冲/六合/三合/六害，天干五合。"""

CHONG = [("子", "午"), ("丑", "未"), ("寅", "申"), ("卯", "酉"),
         ("辰", "戌"), ("巳", "亥")]

LIU_HE = [("子", "丑"), ("寅", "亥"), ("卯", "戌"), ("辰", "酉"),
          ("巳", "申"), ("午", "未")]

LIU_HAI = [("子", "未"), ("丑", "午"), ("寅", "巳"), ("卯", "辰"),
           ("申", "亥"), ("酉", "戌")]

SAN_HE = [("申", "子", "辰", "水"), ("寅", "午", "戌", "火"),
          ("巳", "酉", "丑", "金"), ("亥", "卯", "未", "木")]

SAN_XING = [
    ("寅", "巳", "申"),   # 无恩之刑
    ("丑", "戌", "未"),   # 恃势之刑
]
ZI_XING = ["辰", "午", "酉", "亥"]  # 自刑

GAN_HE = [("甲", "己", "土"), ("乙", "庚", "金"), ("丙", "辛", "水"),
          ("丁", "壬", "木"), ("戊", "癸", "火")]


def compute_xing_chong_he_hai(paipan_result: dict) -> dict:
    bazi = paipan_result["bazi"]
    y, m, d, h = (bazi["year_pillar"], bazi["month_pillar"],
                  bazi["day_pillar"], bazi["hour_pillar"])
    branches = [y[1], m[1], d[1], h[1]]
    stems = [y[0], m[0], d[0], h[0]]
    pos_names = ["年支", "月支", "日支", "时支"]
    result = {"刑": [], "冲": [], "合": [], "害": []}

    def label(i, j):
        return f"{pos_names[i]}{branches[i]}与{pos_names[j]}{branches[j]}"

    # 六冲
    for i in range(4):
        for j in range(i + 1, 4):
            if (branches[i], branches[j]) in CHONG or (branches[j], branches[i]) in CHONG:
                result["冲"].append(label(i, j))

    # 六合
    for i in range(4):
        for j in range(i + 1, 4):
            if (branches[i], branches[j]) in LIU_HE or (branches[j], branches[i]) in LIU_HE:
                result["合"].append(label(i, j) + "六合")

    # 六害
    for i in range(4):
        for j in range(i + 1, 4):
            if (branches[i], branches[j]) in LIU_HAI or (branches[j], branches[i]) in LIU_HAI:
                result["害"].append(label(i, j) + "相害")

    # 三合局（三支全）
    bset = set(branches)
    for a, b, c, elem in SAN_HE:
        if {a, b, c} <= bset:
            result["合"].append(f"{a}{b}{c}三合{elem}局")

    # 三刑（三支全）与两两刑
    for a, b, c in SAN_XING:
        pair_cnt = sum(1 for p in [(a, b), (b, c), (a, c)]
                       if p[0] in bset and p[1] in bset)
        if {a, b, c} <= bset:
            result["刑"].append(f"{a}{b}{c}三刑")
        elif pair_cnt >= 1:
            for p in [(a, b), (b, c), (a, c)]:
                if p[0] in bset and p[1] in bset:
                    result["刑"].append(f"{p[0]}{p[1]}相刑")

    # 自刑（同支两现及以上）
    for z in ZI_XING:
        if branches.count(z) >= 2:
            result["刑"].append(f"{z}自刑")

    # 天干五合（相邻才算）
    for i in range(3):
        for ga, gb, elem in GAN_HE:
            if (stems[i], stems[i + 1]) in [(ga, gb), (gb, ga)]:
                result["合"].append(f"{pos_names[i]}干{stems[i]}与{pos_names[i+1]}干{stems[i+1]}五合化{elem}")

    return {k: v for k, v in result.items() if v}
