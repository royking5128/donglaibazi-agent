# -*- coding: utf-8 -*-
"""契约界面启动入口：python run_contract.py（默认 http://127.0.0.1:8401）"""
import sys
from pathlib import Path
import uvicorn

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent / "web"))
    uvicorn.run("web.web_server:app", host="127.0.0.1", port=8401, reload=False)
