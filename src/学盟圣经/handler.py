"""
学盟圣经 命令执行文件

负责 /学盟圣经 指令的全部逻辑: 发送学盟圣经内容(保留换行的纯文本) + 本文件夹内的图片。

约定:
  - async def handle(event) 中 yield bytes(作为图片发送) 或 str(纯文本)
  - 修改本文件即可调整 /学盟圣经 的行为, 不影响其他命令
"""

import os
from pathlib import Path

# 本命令文件夹(handler.py 与图片同目录)
IMG_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# 固定图片路径(写死, 不探测文件夹内图片数量)
IMG_PATH = IMG_DIR / "Image_1787761317379_551.gif"

# 学盟圣经内容(原文, 保留全部换行)
BIBLE_TEXT = """《学盟圣经》
1. /落姬坡
2. /醉萌亭记
3. /群萝莉"""


async def handle(event):
    """发送文本说明 + 图片, 合并进同一条消息。"""
    yield f"\u200b{BIBLE_TEXT}\n\n[2026/8/26]"
    yield IMG_PATH.read_bytes()
