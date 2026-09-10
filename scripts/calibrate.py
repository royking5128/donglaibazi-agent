# -*- coding: utf-8 -*-
"""Phase 2 动态校准引擎 — 用真实经历反推用神/喜神/忌神。

算法按规划 2.1 节实现：
  1. 以排盘初判（扶抑取用）给出五行初始权重
  2. 用户提供的「顺/不顺年份」落到对应流年干支五行上修正权重（地支为主、天干为辅）
  3. 输出校准后的用神/喜神/忌神 + 置信度 + 验证轨迹
"""
from paipan import GAN, ZHI, WUXING_OF_GAN, WUXING_OF_ZHI

GAN_W = {g: WUXING_OF_GAN[g] for g in GAN}
ZHI_W = {z: WUXING_OF_ZHI[z] for z in ZHI}

# 生克方向表：sheng[X] = X 所生；ke[X] = X 所克
SHENG = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
KE = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}
# 反向：逆生[X] = 生 X 者；逆克[X] = 克 X 者
NI_SHENG = {v: k for k, v in SHENG.items()}
NI_KE = {v: k for k, v in KE.items()}

# 规划 2.1 节的固定修正量：地支为主，天干为辅
EVENT_ADJUST = {"好": {"主": 1.0, "辅": 0.5}, "差": {"主": -1.0, "辅": -0.8}}


def year_ganzhi(year: int) -> str:
    off = (year - 4) % 60
    return GAN[off % 10] + ZHI[off % 12]


def initial_weights(paipan_result: dict) -> dict:
    """基于命盘的扶抑取用初始权重（身弱扶、身强泄）。"""
    wuxing = paipan_result["wu_xing"]
    day_gan = paipan_result["bazi"]["day_master"][0]
    dm = WUXING_OF_GAN[day_gan]
    strength = paipan_result["day_master_strength"]

    # 基础分：各五行旺衰差异（越旺分越高）
    weights = {e: (wuxing[e] - min(wuxing.values())) * 0.2 for e in wuxing}

    if strength == "身弱":
        # 喜：印(生我)+1.0、比劫(同我)+0.8
        # 忌：官杀(克我)-0.8、食伤(我生)-0.5、财(我克)-0.3
        weights[NI_SHENG[dm]] += 1.0
        weights[dm] += 0.8
        weights[NI_KE[dm]] -= 0.8
        weights[SHENG[dm]] -= 0.5
        weights[KE[dm]] -= 0.3
    elif strength == "身强":
        # 喜：食伤(我生)+0.8、财(我克)+0.8、官杀(克我)+0.5
        # 忌：印(生我)-0.9、比劫(同我)-0.8
        weights[SHENG[dm]] += 0.8
        weights[KE[dm]] += 0.8
        weights[NI_KE[dm]] += 0.5
        weights[NI_SHENG[dm]] -= 0.9
        weights[dm] -= 0.8
    else:  # 中和：顺势微调
        weights[SHENG[dm]] += 0.5
        weights[KE[dm]] += 0.5
        weights[dm] += 0.3
    return weights


def calibrate(paipan_result: dict, events: list) -> dict:
    """events: [{"year": 2020, "outcome": "好"|"差", "note": "事业很好"}, ...]"""
    weights = initial_weights(paipan_result)
    traces = []

    for ev in events:
        year = int(ev["year"])
        outcome = ev.get("outcome", "好")
        gz = year_ganzhi(year)
        zhi_el, gan_el = ZHI_W[gz[1]], GAN_W[gz[0]]
        adj = EVENT_ADJUST[outcome]
        weights[zhi_el] += adj["主"]
        weights[gan_el] += adj["辅"]
        traces.append({
            "year": year, "ganzhi": gz, "outcome": outcome,
            "note": ev.get("note", ""),
            "地支五行": zhi_el, f"地支权重{adj['主']:+.1f}": True,
            "天干五行": gan_el, f"天干权重{adj['辅']:+.1f}": True,
        })

    ranked = sorted(weights.items(), key=lambda kv: kv[1], reverse=True)
    yongshen = ranked[0][0]
    xishen = [e for e, _ in ranked[1:3]]
    jishen = [e for e, _ in ranked[-2:]]

    # 置信度：事件数量 + 好年份五行集中度
    n = len(events)
    if n == 0:
        confidence, level = 0.3, "低（未提供经历，仅为排盘初判）"
    else:
        good_els = [ZHI_W[year_ganzhi(int(ev["year"]))[1]]
                    for ev in events if ev.get("outcome") == "好"]
        consistent = bool(good_els) and len(set(good_els)) <= max(1, len(good_els) // 2)
        base = min(0.5 + n * 0.1, 0.85)
        confidence = min(base + (0.1 if consistent else 0), 0.95)
        level = "高" if confidence >= 0.75 else ("中" if confidence >= 0.55 else "低")

    return {
        "yongshen": yongshen,
        "xishen": xishen,
        "jishen": jishen,
        "weights": {k: round(v, 2) for k, v in ranked},
        "event_traces": traces,
        "confidence": round(confidence, 2),
        "confidence_level": level,
    }
