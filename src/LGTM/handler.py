"""
LGTM 命令执行文件

负责 /LGTM 指令的全部逻辑: 发送本文件夹内的图片。

所属: 学盟圣经。

约定:
  - async def handle(event) 中 yield bytes(作为图片发送) 或 str(纯文本)
  - 修改本文件即可调整 /LGTM 的行为, 不影响其他命令
"""

import os
from pathlib import Path

# 本命令文件夹(handler.py 与图片同目录)
IMG_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# 固定图片路径(写死, 不探测文件夹内图片数量)
IMG_PATH = IMG_DIR / "LGTM.jpg"


async def handle(event):
    """发送图片, 合并进同一条消息。"""
    yield IMG_PATH.read_bytes()