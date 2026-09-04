"""
main.py - AMA-10 Entertainment Shu 插件主文件

解耦架构:
  每个命令对应 src/ 下的一个子文件夹(以中文命令命名), 子文件夹内放置该命令的执行文件
  handler.py 和资源文件(图片等)。main.py 只负责: 注册命令 -> 动态加载对应子文件夹的
  handler.py -> 将 handler 产出的文本+图片合并为同一条消息链发送。

当前命令:
  /群号大全  → src/群号大全/handler.py
  /校历      → src/校历/handler.py
  /落姬坡    → src/落姬坡/handler.py
  /醉萌亭记  → src/醉萌亭记/handler.py
  /空教室查询 → src/空教室查询/handler.py
  /VPN       → src/VPN/handler.py
  /正版软件  → src/正版软件/handler.py
  /选课小本本 → src/选课小本本/handler.py
  /教务系统  → src/教务系统/handler.py
  /网上教学  → src/网上教学/handler.py
  /专业分流  → src/专业分流/handler.py
  /鼠鼠导航  → src/鼠鼠导航/handler.py
  /校园地图  → src/校园地图/handler.py
  /校园网    → src/校园网/handler.py
  /学盟圣经  → src/学盟圣经/handler.py
  /学盟攻略  → src/学盟攻略/handler.py
  /群萝莉    → src/群萝莉/handler.py
  /LGTM      → src/LGTM/handler.py

命令文件夹约定:
  src/<命令文件夹>/handler.py
    - 必须定义 handle(event) 函数
    - 推荐写法: async def handle(event), 内部 yield bytes(作为图片发送) 或 str(纯文本)
    - 也可以用 def handle(event) 返回可迭代列表, 元素同样支持 bytes / str
    - 可通过 event.message_str / event.get_message_args() 读取指令参数
"""

import base64
import importlib.util
import os
from pathlib import Path
from typing import AsyncIterator

from astrbot.api import logger
from astrbot.api.event import filter, AstrMessageEvent, MessageChain
from astrbot.api.star import Context, Star, register

# 插件自身目录(子文件夹所在位置)
PLUGIN_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# 业务代码目录(命令模块收存在 src/ 下)
SRC_DIR = PLUGIN_DIR / "src"

# 命令 -> src/ 下的命令文件夹 映射:新增命令时在此注册新文件夹即可
COMMAND_DIRS: dict[str, str] = {
    "group_list": "群号大全",  # /群号大全
    "school_calendar": "校历",  # /校历
    "luo_ji_po": "落姬坡",  # /落姬坡
    "zui_meng_ting_ji": "醉萌亭记",  # /醉萌亭记
    "empty_classroom": "空教室查询",  # /空教室查询
    "vpn": "VPN",  # /VPN
    "genuine_software": "正版软件",  # /正版软件
    "course_rate": "选课小本本",  # /选课小本本
    "jwxt": "教务系统",  # /教务系统
    "online_learning": "网上教学",  # /网上教学
    "major_division": "专业分流",  # /专业分流
    "shu_nav": "鼠鼠导航",  # /鼠鼠导航
    "campus_map": "校园地图",  # /校园地图
    "campus_network": "校园网",  # /校园网
    "bible": "学盟圣经",  # /学盟圣经
    "guide": "学盟攻略",  # /学盟攻略
    "group_loli": "群萝莉",  # /群萝莉
    "credit_transfer": "学分转换",  # /学分转换
    "lgtm": "LGTM",  # /LGTM
}

# 命令文件夹内执行文件的固定名称
HANDLER_FILE = "handler.py"

# 动态加载模块时使用的唯一前缀, 避免多次加载/重载时模块缓存冲突
_MODULE_PREFIX = "ama10_entertainment_shu"


def _load_handler(folder: str):
    """动态加载指定命令文件夹(src/<folder>/handler.py), 失败返回 None。"""
    handler_path = SRC_DIR / folder / HANDLER_FILE
    if not handler_path.is_file():
        logger.warning(f"AMA-10 Entertainment Shu: 命令文件夹 src/{folder}/ 缺少 {HANDLER_FILE}")
        return None
    # 模块名按文件夹唯一化, 保证重载插件时能加载到最新代码
    module_name = f"{_MODULE_PREFIX}_{folder}_handler"
    spec = importlib.util.spec_from_file_location(module_name, handler_path)
    if spec is None or spec.loader is None:
        logger.error(f"AMA-10 Entertainment Shu: 无法为 {folder}/{HANDLER_FILE} 创建模块 spec")
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        logger.error(f"AMA-10 Entertainment Shu: 加载 {folder}/{HANDLER_FILE} 失败: {e}")
        return None
    return module


async def _iter_results(result) -> AsyncIterator:
    """将 handle() 的返回值统一规整为异步迭代器: 兼容 async 生成器 / 可迭代对象。"""
    if hasattr(result, "__aiter__"):
        async for item in result:
            yield item
        return
    if hasattr(result, "__iter__") and not hasattr(result, "__await__"):
        for item in result:
            yield item
        return
    # 普通 async 函数(coroutine): await 后再迭代
    awaited = await result
    if hasattr(awaited, "__aiter__"):
        async for item in awaited:
            yield item
    elif hasattr(awaited, "__iter__"):
        for item in awaited:
            yield item


@register(
    "astrbot_plugin_ama_10_entertainment_shu",
    "Restart-Game-Lab",
    "上海大学学盟社等群聊相关命令插件: 每个命令对应 src/ 下的一个子文件夹, 子文件夹内放置执行文件与资源",
    "v1.11.0",
    "https://github.com/Restart-Game-Lab/astrbot_plugin_ama-10_entertainment_shu",
)
class Main(Star):
    """AMA-10 Entertainment Shu 插件主类: 只负责命令注册与调度, 不含具体业务逻辑"""

    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("群号大全")
    async def group_list(self, event: AstrMessageEvent):
        """发送群号大全"""
        async for item in self._dispatch(event, COMMAND_DIRS["group_list"]):
            yield item

    @filter.command("校历")
    async def school_calendar(self, event: AstrMessageEvent):
        """发送校历"""
        async for item in self._dispatch(event, COMMAND_DIRS["school_calendar"]):
            yield item

    @filter.command("落姬坡")
    async def luo_ji_po(self, event: AstrMessageEvent):
        """发送落姬坡图片"""
        async for item in self._dispatch(event, COMMAND_DIRS["luo_ji_po"]):
            yield item

    @filter.command("醉萌亭记")
    async def zui_meng_ting_ji(self, event: AstrMessageEvent):
        """发送醉萌亭记图片"""
        async for item in self._dispatch(event, COMMAND_DIRS["zui_meng_ting_ji"]):
            yield item

    @filter.command("空教室查询")
    async def empty_classroom(self, event: AstrMessageEvent):
        """发送空教室查询地址"""
        async for item in self._dispatch(event, COMMAND_DIRS["empty_classroom"]):
            yield item

    @filter.command("VPN")
    async def vpn(self, event: AstrMessageEvent):
        """发送上海大学 VPN 接入说明"""
        async for item in self._dispatch(event, COMMAND_DIRS["vpn"]):
            yield item

    @filter.command("正版软件")
    async def genuine_software(self, event: AstrMessageEvent):
        """发送上海大学正版软件订阅说明"""
        async for item in self._dispatch(event, COMMAND_DIRS["genuine_software"]):
            yield item

    @filter.command("选课小本本")
    async def course_rate(self, event: AstrMessageEvent):
        """发送选课小本本地址"""
        async for item in self._dispatch(event, COMMAND_DIRS["course_rate"]):
            yield item

    @filter.command("教务系统")
    async def jwxt(self, event: AstrMessageEvent):
        """发送上海大学教务系统地址"""
        async for item in self._dispatch(event, COMMAND_DIRS["jwxt"]):
            yield item

    @filter.command("网上教学")
    async def online_learning(self, event: AstrMessageEvent):
        """发送上海大学网上教学辅助平台地址"""
        async for item in self._dispatch(event, COMMAND_DIRS["online_learning"]):
            yield item

    @filter.command("专业分流")
    async def major_division(self, event: AstrMessageEvent):
        """发送上海大学大类分流和各专业简介地址"""
        async for item in self._dispatch(event, COMMAND_DIRS["major_division"]):
            yield item

    @filter.command("鼠鼠导航")
    async def shu_nav(self, event: AstrMessageEvent):
        """发送鼠鼠导航地址"""
        async for item in self._dispatch(event, COMMAND_DIRS["shu_nav"]):
            yield item

    @filter.command("校园地图")
    async def campus_map(self, event: AstrMessageEvent):
        """发送校园地图图片"""
        async for item in self._dispatch(event, COMMAND_DIRS["campus_map"]):
            yield item

    @filter.command("校园网")
    async def campus_network(self, event: AstrMessageEvent):
        """发送上海大学校园网接入说明"""
        async for item in self._dispatch(event, COMMAND_DIRS["campus_network"]):
            yield item

    @filter.command("学盟圣经")
    async def bible(self, event: AstrMessageEvent):
        """发送学盟圣经内容"""
        async for item in self._dispatch(event, COMMAND_DIRS["bible"]):
            yield item

    @filter.command("学盟攻略")
    async def guide(self, event: AstrMessageEvent):
        """发送学盟攻略功能集合(纯文本)"""
        async for item in self._dispatch(event, COMMAND_DIRS["guide"]):
            yield item

    @filter.command("群萝莉")
    async def group_loli(self, event: AstrMessageEvent):
        """发送群萝莉图片"""
        async for item in self._dispatch(event, COMMAND_DIRS["group_loli"]):
            yield item

    @filter.command("学分转换")
    async def credit_transfer(self, event: AstrMessageEvent):
        """发送学分转换图片"""
        async for item in self._dispatch(event, COMMAND_DIRS["credit_transfer"]):
            yield item

    @filter.command("LGTM")
    async def lgtm(self, event: AstrMessageEvent):
        """发送 LGTM 图片(所属学盟圣经)"""
        async for item in self._dispatch(event, COMMAND_DIRS["lgtm"]):
            yield item

    async def _dispatch(self, event: AstrMessageEvent, folder: str):
        """加载命令文件夹的执行文件, 将其产出的文本+图片合并为同一条消息链发送。"""
        module = _load_handler(folder)
        if module is None:
            yield event.plain_result(
                f"指令执行文件缺失: 请管理员在插件 {folder}/ 目录下放置 {HANDLER_FILE} 后重载插件。"
            )
            return
        handler = getattr(module, "handle", None)
        if handler is None:
            yield event.plain_result(
                f"指令执行文件格式错误: {folder}/{HANDLER_FILE} 缺少 handle(event) 函数。"
            )
            return
        try:
            # 收集 handler 产出的全部内容(文本 + 图片 bytes), 合并进同一条消息链
            chain = MessageChain()
            has_content = False
            result = handler(event)
            async for item in _iter_results(result):
                if isinstance(item, bytes):
                    # base64 内嵌图片, 不依赖 AstrBot 与协议端(NapCat)共享文件系统
                    chain.base64_image(base64.b64encode(item).decode("utf-8"))
                    has_content = True
                elif isinstance(item, str):
                    chain.message(item)
                    has_content = True
                else:
                    logger.warning(
                        f"AMA-10 Entertainment Shu: {folder}/handler.py 返回了不支持的类型 {type(item).__name__}, 已跳过"
                    )
            if has_content:
                yield event.chain_result(chain.chain)
            else:
                yield event.plain_result(
                    f"指令未产出任何内容: 请检查插件 {folder}/ 目录下的 {HANDLER_FILE}。"
                )
        except Exception as e:
            logger.error(f"AMA-10 Entertainment Shu: 执行 {folder}/{HANDLER_FILE} 出错: {e}")
            yield event.plain_result("指令执行出错, 请查看插件日志。")
