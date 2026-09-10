# -*- coding: utf-8 -*-
"""契约界面后端 — 表单提交 → 自动排盘 + 校准。

POST /api/contract  接收契约表单，返回命盘 + 校准结果
GET  /              契约界面（左右分栏）
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path
from datetime import datetime

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))

from paipan import paipan
from shensha import compute_shen_sha
from xingchong import compute_xing_chong_he_hai
from calibrate import calibrate

app = FastAPI(title="八字契约界面", version="1.0.0")
WEB_DIR = Path(__file__).resolve().parent


class ContractForm(BaseModel):
    calendar_type: str = "gregorian"       # gregorian | lunar
    is_leap_month: bool = False
    year: int
    month: int
    day: int
    hour: int
    minute: int
    hour_unknown: bool = False             # 时辰不详兜底：按 12:00 中点排，结果标注
    gender: str                            # 男 | 女
    city: str = ""
    good_years: List[int] = []
    bad_years: List[int] = []
    normal_years: List[int] = []
    good_months: List[int] = []              # 月份契约：过去10年顺的阳历月份
    bad_months: List[int] = []                # 月份契约：不顺的阳历月份


@app.get("/api/meta")
def meta():
    """前端初始化信息：当前年份（用于右侧年份选择器的右边界）。"""
    return {"current_year": datetime.now().year}


@app.get("/")
def welcome():
    """启动首屏：说明页（人生使用说明书介绍），点确认进入契约界面。"""
    return FileResponse(WEB_DIR / "welcome.html")


@app.get("/contract")
def contract_page():
    """契约界面（从说明页点「开始分析我的八字」进入）。"""
    return FileResponse(WEB_DIR / "index.html")


@app.post("/api/contract")
def contract(req: ContractForm):
    try:
        hour, minute = (12, 0) if req.hour_unknown else (req.hour, req.minute)
        chart = paipan(req.year, req.month, req.day, hour, minute,
                       req.gender, req.city, req.calendar_type, req.is_leap_month)
        chart["shen_sha"] = compute_shen_sha(chart)
        chart["xing_chong_he_hai"] = compute_xing_chong_he_hai(chart)
        if req.hour_unknown:
            chart["true_solar_time"]["note"] += "｜⚠️ 时辰不详，按正午中点排盘，时柱仅供参考"
        events = ([{"year": y, "outcome": "好"} for y in req.good_years]
                  + [{"year": y, "outcome": "差"} for y in req.bad_years])
        calib = calibrate(chart, events) if events else None
        # 月份契约：透传给 agent 做月令节奏解读（附月支对应）
        ZHI_OF_MONTH = {1: "丑", 2: "寅", 3: "卯", 4: "辰", 5: "巳", 6: "午",
                        7: "未", 8: "申", 9: "酉", 10: "戌", 11: "亥", 12: "子"}
        months_contract = None
        if req.good_months or req.bad_months:
            months_contract = {
                "good_months": [{"month": m, "月支": ZHI_OF_MONTH[m]} for m in req.good_months],
                "bad_months": [{"month": m, "月支": ZHI_OF_MONTH[m]} for m in req.bad_months],
                "note": "用户自述过去10年的顺/不顺阳历月份，供解读月令节奏（节气月以立春起寅月推算）",
            }
        return {"chart": chart, "calibration": calib,
                "months_contract": months_contract,
                "form": req.model_dump()}
    except Exception as e:
        raise HTTPException(400, f"排盘失败: {e}")


@app.get("/contract")
def index_legacy():
    return FileResponse(WEB_DIR / "index.html")
