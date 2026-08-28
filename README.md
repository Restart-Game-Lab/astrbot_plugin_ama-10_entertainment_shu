# AMA-10 Entertainment SHU

<div align="center">

<img src="https://count.getloli.com/@preca-hoshino?name=ama-10_entertainment_shu&theme=rule34&padding=7&offset=0&align=top&scale=1&pixelated=1&darkmode=auto" alt="Moe Counter">

**上海大学（SHU）信息展示插件** — 把常用校园信息、导航与图片做成一句指令，随叫随发。

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)
![AstrBot](https://img.shields.io/badge/AstrBot-%E2%89%A54.16-green)
![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey)
[![Repo](https://img.shields.io/badge/repo-Restart--Game--Lab-blue)](https://github.com/Restart-Game-Lab/astrbot_plugin_ama-10_entertainment_shu)

[中文](README.md) | [English](README_EN.md) | [日本語](README_JA.md)

</div>

---

## 简介

`astrbot_plugin_ama-10_entertainment_shu` 是一个基于 [AstrBot](https://github.com/AstrBotDevs/AstrBot) 的 SHU 群聊信息插件。每个指令对应 `src/` 下的一个子文件夹，内含该指令的 `handler.py` 与资源图片，逻辑互相独立——替换图片即可更新内容，无需改代码。

## 特性

- 一个指令对应一个功能，随叫随发
- 每个指令独立存放在自己的子文件夹，换图即更新，无需改代码
- 指令逻辑与资源解耦
- 支持多张图片，按文件名顺序发送

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

本项目源代码基于 [GNU AGPL-3.0](LICENSE) 许可证开源。

> **版权声明**：本项目内所涉及的图片及 MEME（模因）资源，其版权均归 **上海大学**、**上海大学学盟社**、**上海大学学生会**、**西门情报站** 等相关组织机构所有。

> **致谢**：感谢 **[鼠鼠导航](https://shunav.iafenvoy.com/)**、**[选课小本本](https://course-rate.icu/)** 等开源项目提供的开放生态支持。
