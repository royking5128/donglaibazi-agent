# 人生风向标 Agent · 安装指南

这不是「八字排盘工具」，是一张**你的人生使用说明书**：算准你的命盘后，用你的真实经历校准，给出「这个命怎么用」的行动建议。

---

## 一、安装（在 WorkBuddy 里粘贴这句话）

打开 WorkBuddy，把下面这句话**原样粘贴**发给它：

```
请帮我安装 GitHub 上的 skill「donglaibazi-agent」：
访问 https://github.com/royking5128/donglaibazi-agent
把整个仓库下载到本地，放入 ~/.workbuddy/skills/donglaibazi-agent 目录
然后确认这个 skill 已启用。
```

WorkBuddy 会自动完成下载、放置、启用。装好后它会回你一句「已启用」。

> 也可以手动：下载仓库 zip → 解压 → 把 `donglaibazi-agent` 文件夹放到 `~/.workbuddy/skills/` 下。

## 二、使用

装好后，对 WorkBuddy 说：

```
帮我做一次人生风向标分析
```

然后按提示提供：出生日期（阳历/农历）、出生时分、出生地、性别，以及「过去 20 年哪几年最顺/最不顺」。

它会先排盘 → 用你的经历校准 → 输出十板块全息报告 + 给你的具体行动建议。

## 三、依赖（首次使用自动提示）

排盘脚本依赖 `lunar-python`，首次用会提示安装：

```
pip install lunar-python
```

---

> 隐私：你的生辰只在本机分析，不上传任何云端。存档只在你自己的 `data/profiles/`。
> 免责：分析基于传统命理文化视角，供自我探索参考；人生重大决策请结合实际情况，必要时咨询专业人士。
