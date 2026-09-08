"""
shuyo 命令执行文件

负责 /shuyo 指令的全部逻辑: 发送 ShuYo 校园软件说明, 并附带最新 APK 安装包。

为保证 APK 必然可发, 采用"后台定时预下载 + 命令时读取本地缓存"策略:
  - 定时任务每 10 分钟从 download.shuyo.work 下载最新 APK 到插件专属数据目录;
  - /shuyo 命令从缓存目录读取 APK 快速发出, 不受瞬间网络故障影响;
  - 下载超时 5 分钟, 失败仅记日志, 不影响命令与上一次缓存。
"""

import asyncio
import shutil
import urllib.request
from pathlib import Path

from astrbot.api import logger
from astrbot.api.message_components import File
from astrbot.core.utils.astrbot_path import get_astrbot_plugin_data_path

SHUYO_TEXT = """ShuYo是一款上大专属校园软件，登入校园统一认证系统即可自动获取课表，使用查找空教室、查阅选课小本本、校内论坛等功能。

安卓端：
APK安装包访问 https://download.shuyo.work/latest.apk 下载

iOS端：
计划9月TestFlight测试
10月上架App Store（可能跳票）"""

# 最新 APK 下载地址与附件文件名
SHUYO_APK_URL = "https://download.shuyo.work/latest.apk"
SHUYO_APK_NAME = "ShuYo-latest.apk"

# 下载超时时间(秒): 拉大到 5 分钟, 避免网络瞬间故障导致偶发失败
DOWNLOAD_TIMEOUT = 5 * 60

# 插件 id(metadata.yaml 中的 name), 用于定位插件专属数据目录
_PLUGIN_ID = "astrbot_plugin_ama_10_entertainment_shu"

# 缓存目录与下载中的临时目录
_CACHE_SUBDIR = "shuyo"
_DOWNLOADING_SUBDIR = "shuyo_downloading"

# 定时任务注册标记: 防止插件重载时重复注册同名 cron job
_cron_registered = False


def _plugin_data_dir() -> Path:
    """返回插件专属数据目录: <plugin_data>/<插件id>/shuyo/。"""
    root = Path(get_astrbot_plugin_data_path()) / _PLUGIN_ID / _CACHE_SUBDIR
    root.mkdir(parents=True, exist_ok=True)
    return root


def _download_apk_sync(dest: Path) -> None:
    """同步下载最新 ShuYo APK 到 dest 路径(在线程池中执行, 不阻塞事件循环)。"""
    request = urllib.request.Request(SHUYO_APK_URL, method="GET")
    with urllib.request.urlopen(request, timeout=DOWNLOAD_TIMEOUT) as response, open(dest, "wb") as f:
        f.write(response.read())


async def _refresh_apk_cache() -> None:
    """定时任务: 每 10 分钟下载最新 APK 到插件数据目录, 失败只记日志。

    先写入独立的临时目录, 成功后原子替换缓存文件, 避免半成品被 /shuyo 读到。
    """
    cache_dir = _plugin_data_dir()
    downloading_dir = cache_dir.parent / _DOWNLOADING_SUBDIR
    try:
        downloading_dir.mkdir(parents=True, exist_ok=True)
        tmp_path = downloading_dir / SHUYO_APK_NAME
        await asyncio.to_thread(_download_apk_sync, tmp_path)
        # 下载成功, 原子替换缓存
        final_path = cache_dir / SHUYO_APK_NAME
        shutil.move(str(tmp_path), str(final_path))
        logger.info(
            f"AMA-10 Entertainment Shu: ShuYo APK 已更新到 {final_path} "
            f"({final_path.stat().st_size} bytes)"
        )
    except Exception as e:
        logger.error(f"AMA-10 Entertainment Shu: ShuYo APK 定时下载失败(不影响命令, 沿用旧缓存): {e}")
    finally:
        # 清理下载临时目录
        try:
            if downloading_dir.exists():
                shutil.rmtree(downloading_dir)
        except OSError:
            pass


def _get_cached_apk() -> Path | None:
    """返回缓存目录中已下载好的 APK 路径; 没有缓存时返回 None。"""
    apk_path = _plugin_data_dir() / SHUYO_APK_NAME
    if apk_path.is_file():
        return apk_path
    return None


async def handle(event):
    """发送 ShuYo 校园软件说明, 并附带本地缓存的最新 APK(由定时任务预下载)。"""
    yield f"\u200b{SHUYO_TEXT}\n\n[2026/9/5]\n@Lilin-1024"

    cached = _get_cached_apk()
    if cached is not None:
        # 用本地缓存路径发送, 协议端(NapCat)与 AstrBot 共享文件系统
        yield File(name=SHUYO_APK_NAME, file=str(cached))
    else:
        # 尚未缓存(首次运行/下载失败): 退回按 URL 发送, 并尝试触发一次同步下载
        logger.warning(
            "AMA-10 Entertainment Shu: ShuYo APK 无本地缓存, 退回按 URL 发送并触发远程下载"
        )
        yield File(name=SHUYO_APK_NAME, url=SHUYO_APK_URL)
        # 触发一次后台下载, 优先填充缓存(不 await, 避免阻塞命令)
        try:
            asyncio.get_running_loop().create_task(_refresh_apk_cache())
        except RuntimeError:
            logger.debug("AMA-10 Entertainment Shu: 无运行中的事件循环, 跳过即时 APK 缓存刷新")


async def setup_cron(context) -> None:
    """注册定时任务: 每 10 分钟刷新一次 APK 缓存。

    在 Main.initialize() 中被 await 调用; add_basic_job 为异步方法。
    通过全局标记避免插件重载时重复注册同名任务。
    """
    global _cron_registered
    if _cron_registered:
        return
    _cron_registered = True

    cron_manager = getattr(context, "cron_manager", None)
    if cron_manager is None:
        logger.warning("AMA-10 Entertainment Shu: 未初始化 cron_manager, 跳过注册 APK 定时下载任务")
        return

    # 幂等: 若已存在同名任务则先删除, 防止重载后重复
    try:
        existing = await cron_manager.list_jobs()
        for job in existing:
            if job.name == "shuyo_apk_refresh":
                await cron_manager.delete_job(job.job_id)
    except Exception:
        pass

    async def _job() -> None:
        await _refresh_apk_cache()

    try:
        await cron_manager.add_basic_job(
            name="shuyo_apk_refresh",
            cron_expression="*/10 * * * *",
            handler=_job,
            description="每 10 分钟从 download.shuyo.work 下载最新 ShuYo APK 到插件数据目录",
            enabled=True,
            persistent=False,
        )
        logger.info("AMA-10 Entertainment Shu: ShuYo APK 定时下载任务已注册(每 10 分钟)")
    except Exception as e:
        logger.error(f"AMA-10 Entertainment Shu: 注册 ShuYo APK 定时下载任务失败: {e}")
