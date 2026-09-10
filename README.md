# donglaibazi-agent

**八字深度分析 Agent — 不是算命，是一张「你的人生使用说明书」**

> 计算与解读解耦：Python 确定性排盘（0 幻觉）+ 真实经历校准用神 + Agent 深度解读。

## 这是什么

一个基于 **Agent Skill 架构** 的八字深度分析系统。核心理念：

- **计算层（Python）**：历法转换、真太阳时校正、四柱十神、五行大运、35 项神煞、刑冲合害——全部由确定性代码完成，**模型绝不手算四柱**，从根本上消灭排盘幻觉
- **校准层**：用用户真实的顺/不顺年份经历反推用神/喜神/忌神——因为同样的八字，不同的人会走出不同的人生轨迹
- **解读层（Agent）**：贴着用户皮肤长的深度解读，不说"你命里缺火"，说"你适合在被需要时专注，不适合硬逼自己早起"

## 项目结构

```
donglaibazi-agent/
├── SKILL.md              # Agent 工作流规范（十板块全息首报 + 追问环节 + PDF 收口）
├── scripts/              # 确定性计算层
│   ├── cli.py            # 统一入口：paipan / calibrate / save / list / load
│   ├── paipan.py         # 排盘：真太阳时/四柱/十神/五行加权/大运/流年/旺衰
│   ├── geo.py            # 城市经度库 + 均时差校正
│   ├── shensha.py        # 神煞 35 项
│   ├── xingchong.py      # 刑冲合害
│   ├── calibrate.py      # 经历校准引擎（扶抑取用 + 事件权重 + 置信度）
│   └── storage.py        # 本地存档 CRUD
├── contract/             # 契约界面（Web）
│   ├── run_contract.py   # 启动入口（http://127.0.0.1:8401）
│   └── web/
│       ├── welcome.html  # 启动说明首屏（人生使用说明书介绍）
│       ├── index.html    # 契约界面（左：生辰表单；右：年份勾选 + 月份契约）
│       └── web_server.py # FastAPI：表单 → 自动排盘 + 校准 → JSON
└── data/profiles/         # 本地存档（自动创建，不上传）
```

## 使用方式

### 方式一：作为 Agent Skill（推荐）

放进任何支持 SKILL.md 规范的 Agent（如 Box-Agent / Hermes / Claude Code 等）的 skills 目录：

```bash
git clone https://github.com/donglai/donglaibazi-agent.git ~/.box-agent/skills/donglaibazi-agent
# 或
git clone https://github.com/donglai/donglaibazi-agent.git ~/.hermes/skills/donglaibazi-agent
```

安装依赖（一次性）：

```bash
python -m pip install lunar-python
```

然后对 Agent 说「帮我算八字」即可。Agent 会按 SKILL.md 的流程工作：

```
契约界面（可选）或对话收集生辰
→ Python 确定性排盘（JSON）
→ 用户真实经历校准用神（顺/不顺年份 + 月份）
→ 十板块全息首报
→ 追问三问（妻财子禄寿 / 当下困惑 / 具体深读）
→ 深度应答（每轮带确认）
→ 「转PDF」收口
```

### 方式二：契约界面（Web 表单）

```bash
pip install fastapi uvicorn lunar-python
python contract/run_contract.py
# 浏览器打开 http://127.0.0.1:8401
```

- **首屏**：启动说明（这工具是什么、你会得到什么、真实案例、隐私与免责）
- **左栏**：生辰契约（阳/农历、时分、性别、出生地，含时辰不详兜底）
- **右栏**：人生节律契约——年份勾选（以出生年为终点往前约 20 年，先选顺/不顺档位再点选，档位栏滚动时冻结）+ 月份契约（过去 10 年几月顺/几月不顺）
- **提交**：自动排盘 + 校准，输出三段 JSON，交给 Agent 直接深度解读

### CLI 直用（不经 Agent）

```bash
python scripts/cli.py paipan --year 1990 --month 5 --day 15 --hour 12 --minute 0 --gender 男 --city 上海
python scripts/cli.py calibrate --chart chart.json --events '[{"year":2019,"outcome":"好"},{"year":2018,"outcome":"差"}]'
python scripts/cli.py save --name 张三 --chart chart.json --calib calib.json
python scripts/cli.py list
python scripts/cli.py load --slug 张三
```

## 十板块全息首报

1. 定盘总论（含格局专论 + 五行能量叙事）
2. 四柱拆解（每柱五段 + 十神专论 + 神煞专论）
3. 行为密码（用/养/防五层展开 + 身体专章）
4. 金句辑录（十节 + 随身卡，按用户校准体系贴盘生成）
5. 月令作战日历（12 个月逐月宜忌）
6. 流年预警地图（未来 5-10 年逐年 + 最凶年标警）
7. 大运十年战略（蓄力/开渠/洪峰/收网分段）
8. 关系模式论（择偶倾向/夫妻宫/相处雷区与解药）
9. 财富机制论（财星/财库开启年份/变现路径）
10. 追问三问收尾（每轮应答带确认句，「转PDF」收口）

三条全局深度增强：**验证锚**（论断必须挂用户真实年份证据）、**时间窗**（建议必须挂流年坐标）、**破解法**（风险必须给提前卸力操作）。

## 排盘口径

- 晚子时 23:00-23:59 日柱算当天
- 真太阳时按出生地经度 + 均时差自动校正
- 大运：男阳/女阴顺排，男阴/女阳逆排
- 五行统计含藏干加权（本气 1.0 / 中气 0.6 / 余气 0.3）
- 校准权重：扶抑取用初始 + 经历修正（顺年地支 +1.0/天干 +0.5；差年 -1.0/-0.8）

## 隐私

- 生辰信息仅用于本地分析，**不上传任何云端**
- 存档仅存于本机 `data/profiles/`
- 不追踪、不画像、不推送广告

## 免责声明

本工具的分析基于中国传统命理文化视角，供参考与自我探索之用。人生重大决策（职业、婚姻、财务、健康）请结合自身实际情况，必要时咨询专业人士。

## License

MIT
