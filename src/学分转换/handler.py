"""
学分转换 命令执行文件

负责 /学分转换 指令的全部逻辑。
"""

import os
from pathlib import Path

# 本命令文件夹
IMG_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# 固定图片路径
IMG_PATH = IMG_DIR / "学分转换.jpg"


async def handle(event):
    """发送标题文本 + 图片"""
    yield "📚 上海大学学分转换说明"
    yield IMG_PATH.read_bytes()