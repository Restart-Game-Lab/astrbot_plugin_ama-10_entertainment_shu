# AMA-10 Entertainment SHU

<div align="center">

<img src="https://count.getloli.com/@preca-hoshino?name=ama-10_entertainment_shu&theme=rule34&padding=7&offset=0&align=top&scale=1&pixelated=1&darkmode=auto" alt="Moe Counter">

**A Shanghai University (SHU) info display plugin** — Turn everyday campus info, navigation, and images into a single command, on demand.

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)
![AstrBot](https://img.shields.io/badge/AstrBot-%E2%89%A54.16-green)
![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey)
[![Repo](https://img.shields.io/badge/repo-Restart--Game--Lab-blue)](https://github.com/Restart-Game-Lab/astrbot_plugin_ama-10_entertainment_shu)

[中文](README.md) | [English](README_EN.md) | [日本語](README_JA.md)

</div>

---

## Introduction

`astrbot_plugin_ama-10_entertainment_shu` is a SHU group-chat info plugin built on [AstrBot](https://github.com/AstrBotDevs/AstrBot). Each command corresponds to a subfolder under `src/`, containing that command's `handler.py` and assets. The logic is isolated per command — replace the images to update content, no code changes needed.

## Features

- One command per feature, on demand
- Each command lives in its own subfolder; swap images to update without touching code
- Command logic and resources are decoupled
- Supports multiple images sent in filename order

## Project Structure

```
astrbot_plugin_ama-10_entertainment_shu/
├── main.py          # Plugin entry: registers commands + dynamically loads each handler
├── metadata.yaml    # Plugin metadata
└── src/             # Command directory (each subfolder = one command)
    └── <command>/    # e.g. 群号大全/ 校历/ 鼠鼠导航/
        ├── handler.py   # Command execution logic
        └── images (optional) # Sent in filename order
```

## Updating Content

Place images in the corresponding command folder (supports `png` / `jpg` / `jpeg` / `webp` / `gif` / `bmp`, multiple allowed, sent in filename order), then select "Reload Plugin" for this plugin in the WebUI.

## Adding a Command

1. Create `src/<command>/handler.py` (define `handle(event)`);
2. Register the mapping in `COMMAND_DIRS` in `main.py`;
3. Add an `@filter.command("<command>")` handler that calls `_dispatch(event, "<command>")`.

## License

This project is licensed under [GNU AGPL-3.0](LICENSE).

> **Copyright Notice**: All images and MEME resources involved in this project are copyrighted by **Shanghai University**, **Shanghai University XueMeng Society**, **Shanghai University Student Union**, **西门情报站** and other relevant organizations.

> **Acknowledgements**: Thanks to the open ecosystem provided by **[ShuNav](https://shunav.iafenvoy.com/)**, **[Course Rate](https://course-rate.icu/)** and other open-source projects.
