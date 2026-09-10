# -*- coding: utf-8 -*-
"""本地命盘存档 — profiles CRUD（规划「本地存档」节）。

存档位置：./data/profiles/<slug>.json
内容：命盘 JSON + 校准结果 + 事件记录 + 用户修正记录。
"""
import json
import re
from pathlib import Path

PROFILES_DIR = Path(__file__).resolve().parent.parent / "data" / "profiles"


def _ensure_dir():
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)


def slugify(name: str) -> str:
    s = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", str(name)).strip("-")
    return s or "anonymous"


def save_profile(slug: str, data: dict) -> dict:
    _ensure_dir()
    slug = slugify(slug)
    data = dict(data)
    data["slug"] = slug
    path = PROFILES_DIR / f"{slug}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"slug": slug, "path": str(path)}


def load_profile(slug: str) -> dict:
    path = PROFILES_DIR / f"{slugify(slug)}.json"
    if not path.exists():
        raise FileNotFoundError(f"档案不存在: {slug}")
    return json.loads(path.read_text(encoding="utf-8"))


def list_profiles() -> list:
    _ensure_dir()
    out = []
    for p in sorted(PROFILES_DIR.glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            out.append({
                "slug": d.get("slug", p.stem),
                "name": d.get("name", p.stem),
                "birth": d.get("paipan", {}).get("input", {}).get("birth", ""),
                "gender": d.get("paipan", {}).get("input", {}).get("gender", ""),
                "updated_at": d.get("updated_at", ""),
            })
        except Exception:
            continue
    return out


def delete_profile(slug: str) -> bool:
    path = PROFILES_DIR / f"{slugify(slug)}.json"
    if path.exists():
        path.unlink()
        return True
    return False
