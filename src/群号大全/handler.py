"""
group_list 命令执行文件

负责 /群号大全 指令的全部逻辑: 收集本文件夹内的图片并按文件名顺序发送。

约定:
  - async def handle(event) 中 yield bytes(作为图片发送) 或 str(纯文本)
  - 修改本文件即可调整 /群号大全 的行为, 不影响其他命令
"""

import os
from pathlib import Path

# 本命令文件夹(handler.py 与图片同目录)
IMG_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# 固定图片路径(写死, 不探测文件夹内图片数量)
IMG_PATH = IMG_DIR / "群号大全.webp"


async def handle(event):
    """发送标题文本 + 图片, 合并进同一条消息。"""
    yield "\u200b上海大学学生组织/社团/迎新QQ群号汇总\n\n本图可能包含过时信息，请去 https://docs.qq.com/sheet/DYk9nbXR6UU52R01T 查看\n\n[2026/8/26]"
    yield IMG_PATH.read_bytes()
