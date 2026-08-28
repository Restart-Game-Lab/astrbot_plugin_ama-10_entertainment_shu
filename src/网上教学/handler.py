"""
网上教学 命令执行文件

负责 /网上教学 指令的全部逻辑: 发送上海大学网上教学辅助平台地址(保留换行的纯文本)。

约定:
  - async def handle(event) 中 yield bytes(作为图片发送) 或 str(纯文本)
  - 修改本文件即可调整 /网上教学 的行为, 不影响其他命令
"""

# 上海大学网上教学辅助平台地址(原文, 保留全部换行)
ONLINE_LEARNING_TEXT = """上海大学网上教学辅助平台/学习通网页端
https://learning.shu.edu.cn"""


async def handle(event):
    """发送网上教学平台地址, 保留换行, 格式与其他命令一致(内容 + 日期行)。"""
    yield f"\u200b{ONLINE_LEARNING_TEXT}\n\n[2026/8/26]"
