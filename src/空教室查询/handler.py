"""
空教室查询 命令执行文件

负责 /空教室查询 指令的全部逻辑: 发送空教室查询网站地址。

约定:
  - async def handle(event) 中 yield bytes(作为图片发送) 或 str(纯文本)
  - 修改本文件即可调整 /空教室查询 的行为, 不影响其他命令
"""

# 空教室查询地址
EMPTY_CLASSROOM_TEXT = "classroom.cc.shu.edu.cn"


async def handle(event):
    """发送空教室查询地址, 格式与其他命令一致(内容 + 日期行)。"""
    yield f"\u200b{EMPTY_CLASSROOM_TEXT}\n\n[2026/8/26]"
