"""
专业分流 命令执行文件

负责 /专业分流 指令的全部逻辑: 发送上海大学大类分流和各专业简介地址(保留换行的纯文本)。

约定:
  - async def handle(event) 中 yield bytes(作为图片发送) 或 str(纯文本)
  - 修改本文件即可调整 /专业分流 的行为, 不影响其他命令
"""

# 上海大学大类分流和各专业简介(原文, 保留全部换行)
ZYINFO_TEXT = """上海大学大类分流和各专业简介
https://zyinfo.shu.edu.cn (校内访问)
https://https-zyinfo-shu-edu-cn-443.webvpn.shu.edu.cn (WebVPN直接访问)"""


async def handle(event):
    """发送大类分流和各专业简介地址, 保留换行, 格式与其他命令一致(内容 + 日期行)。"""
    yield f"\u200b{ZYINFO_TEXT}\n\n[2026/8/26]"
