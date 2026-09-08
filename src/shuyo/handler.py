"""
shuyo 命令执行文件

负责 /shuyo 指令的全部逻辑: 发送 ShuYo 校园软件说明, 并附带最新 APK 安装包。
"""

from astrbot.api.message_components import File

SHUYO_TEXT = """ShuYo是一款上大专属校园软件，登入校园统一认证系统即可自动获取课表，使用查找空教室、查阅选课小本本、校内论坛等功能。

安卓端：
安装包可在群文件中获取，或访问https://download.shuyo.work/latest.apk下载

iOS端：
计划9月TestFlight测试
10月上架App Store（可能跳票）"""

# 最新 APK 下载地址与附件文件名
SHUYO_APK_URL = "https://download.shuyo.work/latest.apk"
SHUYO_APK_NAME = "ShuYo-latest.apk"


async def handle(event):
    """发送 ShuYo 校园软件说明, 并附带最新 APK(由 API 按 URL 下载发送)。"""
    yield f"\u200b{SHUYO_TEXT}\n\n[2026/9/5]\n@Lilin-1024"
    yield File(name=SHUYO_APK_NAME, url=SHUYO_APK_URL)
