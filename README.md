<div align="center">

**上海大学（SHU）信息展示插件** — 把常用校园信息、导航与图片做成一句指令，随叫随发。

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)
![AstrBot](https://img.shields.io/badge/AstrBot-%E2%89%A54.16-green)
![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey)
[![Repo](https://img.shields.io/badge/repo-Restart--Game--Lab-blue)](https://github.com/Restart-Game-Lab/astrbot_plugin_ama-10_entertainment_shu)

</div>

---

## 简介

`astrbot_plugin_ama-10_entertainment_shu` 是一个基于 [AstrBot](https://github.com/AstrBotDevs/AstrBot) 的 SHU 群聊信息插件。每个指令对应 `src/` 下的一个子文件夹，内含该指令的 `handler.py` 与资源图片，逻辑互相独立——替换图片即可更新内容，无需改代码。

## 指令

| 指令 | 说明 |
|:---|:---|
| `/群号大全` | 群号汇总图片 |
| `/校历` | 学年校历图片 |
| `/落姬坡` | 落姬坡图片 |
| `/醉萌亭记` | 醉萌亭记图片 |
| `/空教室查询` | 空教室查询地址 |
| `/VPN` | 上海大学 VPN 接入说明 |
| `/正版软件` | 正版软件订阅说明 |
| `/选课小本本` | 选课评价网站 |
| `/教务系统` | 教务系统地址 |
| `/网上教学` | 网上教学平台地址 |
| `/专业分流` | 大类分流与专业简介 |
| `/鼠鼠导航` | 鼠鼠导航地址 |
| `/校园地图` | 校园地图图片 |
| `/学盟圣经` | 学盟圣经内容 |
| `/群萝莉` | 群萝莉图片 |

## 目录结构

```
astrbot_plugin_ama-10_entertainment_shu/
├── main.py          # 插件入口: 注册命令 + 动态加载各命令 handler
├── metadata.yaml    # 插件元数据
└── src/             # 命令目录(每个子文件夹 = 一个命令)
    └── <命令名>/     # 如 群号大全/ 校历/ 鼠鼠导航/
        ├── handler.py   # 命令执行逻辑
        └── 图片(可选)    # 按文件名顺序发送
```

## 更新内容

将图片放入对应命令文件夹（支持 `png` / `jpg` / `jpeg` / `webp` / `gif` / `bmp`，可放多张，按文件名顺序发送），然后在 WebUI 对本插件执行「重载插件」即可生效。

## 新增命令

1. 创建 `src/<命令名>/handler.py`（定义 `handle(event)`）；
2. 在 `main.py` 的 `COMMAND_DIRS` 中注册映射；
3. 添加 `@filter.command("指令名")` handler 调用 `_dispatch(event, "<命令名>")`。

## 许可证

本项目基于 [GNU AGPL-3.0](LICENSE) 许可证开源。
