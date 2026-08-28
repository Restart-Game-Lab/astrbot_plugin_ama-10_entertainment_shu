# AMA-10 Entertainment SHU

<div align="center">

<img src="https://count.getloli.com/@preca-hoshino?name=ama-10_entertainment_shu&theme=rule34&padding=7&offset=0&align=top&scale=1&pixelated=1&darkmode=auto" alt="Moe Counter">

**上海大学（SHU）情報表示プラグイン** — キャンパス情報やナビ、画像をひとつのコマンドで呼び出せます。

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)
![AstrBot](https://img.shields.io/badge/AstrBot-%E2%89%A54.16-green)
![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey)
[![Repo](https://img.shields.io/badge/repo-Restart--Game--Lab-blue)](https://github.com/Restart-Game-Lab/astrbot_plugin_ama-10_entertainment_shu)

[中文](README.md) | [English](README_EN.md) | [日本語](README_JA.md)

</div>

---

## 概要

`astrbot_plugin_ama-10_entertainment_shu` は [AstrBot](https://github.com/AstrBotDevs/AstrBot) ベースの SHU グルチャ情報プラグインです。各コマンドは `src/` 以下のサブフォルダに対応し、そのコマンドの `handler.py` とリソース画像を含みます。ロジックはコマンドごとに独立しています — 画像を差し替えるだけで内容を更新でき、コード変更は不要です。

## 特徴

- ひとつのコマンドでひとつの機能を呼び出せる
- 各コマンドが独立したサブフォルダにあり、画像を差し替えるだけで更新可能
- コマンドロジックとリソースが分離されている
- 複数画像をファイル名順に送信可能

## ディレクトリ構成

```
astrbot_plugin_ama-10_entertainment_shu/
├── main.py          # プラグインエントリ: コマンド登録 + 各ハンドラの動的読み込み
├── metadata.yaml    # プラグインメタデータ
└── src/             # コマンドディレクトリ（各サブフォルダ = ひとつのコマンド）
    └── <コマンド名>/ # 例: 群号大全/ 校历/ 鼠鼠导航/
        ├── handler.py   # コマンド実行ロジック
        └── 画像(任意)    # ファイル名順に送信
```

## コンテンツの更新

対応コマンドフォルダに画像を置くだけでOK（`png` / `jpg` / `jpeg` / `webp` / `gif` / `bmp` 対応、複数可、ファイル名順に送信）。その後 WebUI でこのプラグインの「プラグインを再読み込み」を実行すれば反映されます。

## コマンドの追加

1. `src/<コマンド名>/handler.py` を作成（`handle(event)` を定義）;
2. `main.py` の `COMMAND_DIRS` にマッピングを登録;
3. `_dispatch(event, "<コマンド名>")` を呼ぶ `@filter.command("<コマンド名>")` ハンドラを追加。

## ライセンス

このプロジェクトは [GNU AGPL-3.0](LICENSE) の下でライセンスされています。

> **著作権表示**: 本プロジェクトに含まれる画像および MEME（ミーム）リソースの著作権は、**上海大学**、**上海大学学盟社**、**上海大学学生会**、**西门情报站** などの関連機関に帰属します。

> **謝辞**: **[ShuNav](https://shunav.iafenvoy.com/)**、**[Course Rate](https://course-rate.icu/)** などのオープンソースプロジェクトが提供するオープンエコシステムに感謝します。
