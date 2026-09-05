"""
shuyo 命令执行文件

负责 /shuyo 指令的全部逻辑: 发送 ShuYo 校园软件说明。
"""

SHUYO_TEXT = """ShuYo是一款上大专属校园软件，登入校园统一认证系统即可自动获取课表，使用查找空教室、查阅选课小本本、校内论坛等功能。

安卓端：
安装包可在群文件中获取，或访问https://download.shuyo.work/latest.apk下载

iOS端：
计划9月TestFlight测试
10月上架App Store（可能跳票）"""


async def handle(event):
    """发送 ShuYo 校园软件说明。"""
    yield f"\u200b{SHUYO_TEXT}\n\n[2026/9/5]"
