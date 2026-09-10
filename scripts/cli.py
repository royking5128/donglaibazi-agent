# -*- coding: utf-8 -*-
"""八字深度分析 Skill — CLI 统一入口。

子命令：
  paipan    排盘：四柱/十神/五行/藏干/大运/流年/神煞/刑冲合害 → JSON
  calibrate 校准：用顺/不顺年份经历反推用神 → JSON
  save      存档命盘到 data/profiles/
  list      列出存档
  load      加载存档

用法示例：
  python cli.py paipan --year 1990 --month 5 --day 15 --hour 12 --minute 0 --gender 男 --city "上海"
  python cli.py calibrate --chart chart.json --events "[{\"year\":2019,\"outcome\":\"好\"}]"
  python cli.py save --name "张三" --chart chart.json --calib calib.json
  python cli.py list
  python cli.py load --slug "张三"
"""
import argparse
import json
import sys
from pathlib import Path

from paipan import paipan
from shensha import compute_shen_sha
from xingchong import compute_xing_chong_he_hai
from calibrate import calibrate
from storage import save_profile, load_profile, list_profiles

SKILL_DIR = Path(__file__).resolve().parent


def cmd_paipan(a):
    r = paipan(a.year, a.month, a.day, a.hour, a.minute, a.gender,
               a.city or "", a.calendar, a.leap)
    r["shen_sha"] = compute_shen_sha(r)
    r["xing_chong_he_hai"] = compute_xing_chong_he_hai(r)
    return r


def _read_json(path):
    if path == "-":
        return json.loads(sys.stdin.read())
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    p = argparse.ArgumentParser(description="八字深度分析 CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("paipan")
    sp.add_argument("--year", type=int, required=True)
    sp.add_argument("--month", type=int, required=True)
    sp.add_argument("--day", type=int, required=True)
    sp.add_argument("--hour", type=int, required=True)
    sp.add_argument("--minute", type=int, required=True)
    sp.add_argument("--gender", required=True, help="男/女")
    sp.add_argument("--city", default="", help="出生地，用于真太阳时校正")
    sp.add_argument("--calendar", default="gregorian", choices=["gregorian", "lunar"])
    sp.add_argument("--leap", action="store_true", help="农历闰月")

    sp = sub.add_parser("calibrate")
    sp.add_argument("--chart", required=True, help="paipan 输出的 JSON 文件路径（或 - 读 stdin）")
    sp.add_argument("--events", required=True,
                    help='经历 JSON 数组：[{"year":2019,"outcome":"好","note":"事业好"}]')

    sp = sub.add_parser("save")
    sp.add_argument("--name", required=True)
    sp.add_argument("--chart", required=True)
    sp.add_argument("--calib", default="")
    sp.add_argument("--events", default="[]")

    sp = sub.add_parser("list")

    sp = sub.add_parser("load")
    sp.add_argument("--slug", required=True)

    a = p.parse_args()

    if a.cmd == "paipan":
        out = cmd_paipan(a)
    elif a.cmd == "calibrate":
        chart = _read_json(a.chart)
        events = json.loads(a.events) if a.events.strip().startswith("[") else None
        if events is None:
            # 兼容 "2019:好,2018:差" 简写
            events = []
            for part in a.events.split(","):
                y, o = part.strip().split(":")
                events.append({"year": int(y), "outcome": o.strip()})
        out = calibrate(chart, events)
    elif a.cmd == "save":
        from datetime import datetime
        data = {
            "name": a.name,
            "paipan": _read_json(a.chart),
            "calibration": _read_json(a.calib) if a.calib else None,
            "events": json.loads(a.events) if a.events else [],
            "updated_at": datetime.now().isoformat(timespec="seconds"),
        }
        out = save_profile(a.name, data)
    elif a.cmd == "list":
        out = {"profiles": list_profiles()}
    elif a.cmd == "load":
        out = load_profile(a.slug)
    else:
        p.error("未知子命令")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
