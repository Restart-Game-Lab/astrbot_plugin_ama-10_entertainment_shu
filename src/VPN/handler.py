"""
VPN 命令执行文件

负责 /VPN 指令的全部逻辑: 发送上海大学校内 VPN 接入说明(保留换行的纯文本)。

约定:
  - async def handle(event) 中 yield bytes(作为图片发送) 或 str(纯文本)
  - 修改本文件即可调整 /VPN 的行为, 不影响其他命令
"""

# 上海大学校内 VPN 接入说明(原文, 保留全部换行)
VPN_TEXT = """上海大学校内VPN支持下列方式接入
1. aTrust Web/客户端
2. OpenVPN 客户端
3. EasyConnect 客户端
4. WebVPN Web
下载和使用说明：https://vpn.shu.edu.cn

*OpenVPN,EasyConnect登录方式需要TOTP二次验证令牌，推荐企业微信 "信息服务->OTP令牌" 或 https://otp.shu.edu.cn 方式获取"""


async def handle(event):
    """发送 VPN 接入说明, 保留换行, 格式与其他命令一致(内容 + 日期行)。"""
    yield f"\u200b{VPN_TEXT}\n\n[2026/8/26]"
