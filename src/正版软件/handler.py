"""
正版软件 命令执行文件

负责 /正版软件 指令的全部逻辑: 发送上海大学已购正版软件订阅说明(保留换行的纯文本)。

约定:
  - async def handle(event) 中 yield bytes(作为图片发送) 或 str(纯文本)
  - 修改本文件即可调整 /正版软件 的行为, 不影响其他命令
"""

# 上海大学已购正版软件订阅说明(原文, 保留全部换行)
GENUINE_SOFTWARE_TEXT = """上海大学已购买软件订阅如下
1. Adobe 系列软件和Adobe Creative Cloud
2. MATLAB
下载和使用说明：
https://software.shu.edu.cn (校内访问)
https://https-software-shu-edu-cn-443.webvpn.shu.edu.cn (WebVPN直接访问)"""


async def handle(event):
    """发送正版软件订阅说明, 保留换行, 格式与其他命令一致(内容 + 日期行)。"""
    yield f"\u200b{GENUINE_SOFTWARE_TEXT}\n\n[2026/8/26]"
