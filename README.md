# AMA-10 Entertainment Shu

上海大学信息展示插件: 每个命令对应 `src/` 下的一个子文件夹, 内含该命令的 `handler.py` 与图片资源, 命令逻辑互不影响。

## 指令

| 指令 | 说明 |
| ---- | ---- |
| `/群号大全` | 群号汇总图片 |
| `/校历` | 学年校历图片 |
| `/落姬坡` | 落姬坡图片 |
| `/醉萌亭记` | 醉萌亭记图片 |
| `/空教室查询` | 空教室查询地址 |
| `/VPN` | 上海大学 VPN 接入说明 |
| `/正版软件` | 正版软件订阅说明 |
| `/选课小本本` | 选课评价网站 |
| `/教务系统` | 教务系统地址 |
| `/网上教学` | 网上教学平台地址 |
| `/专业分流` | 大类分流与专业简介 |
| `/鼠鼠导航` | 鼠鼠导航地址 |
| `/校园地图` | 校园地图图片 |
| `/学盟圣经` | 学盟圣经内容 |
| `/群萝莉` | 群萝莉图片 |

## 目录结构

```
astrbot_plugin_ama-10_entertainment_shu/
├── main.py               # 插件入口: 注册命令 + 动态加载各命令 handler
├── metadata.yaml         # 插件元数据
└── src/                  # 命令目录(每个子文件夹 = 一个命令)
    └── <命令名>/          # 如 群号大全/ 校历/ 鼠鼠导航/
        ├── handler.py    # 命令执行逻辑
        └── 图片(可选)     # 按文件名顺序发送
```

## 命令执行文件约定

`src/<命令名>/handler.py` 定义 `handle(event)`, 通过 `yield` 输出内容:

```python
async def handle(event):
    yield b"..."      # bytes → 作为图片发送(与文本同一条消息)
    yield "文本..."   # str → 作为纯文本发送
```

- 也支持 `def handle(event)` 返回可迭代列表(元素同为 `bytes` / `str`)
- 可通过 `event.message_str` 读取指令参数

## 新增命令

1. 创建 `src/<命令名>/handler.py`(定义 `handle(event)`);
2. 在 `main.py` 的 `COMMAND_DIRS` 中注册映射;
3. 添加 `@filter.command("指令名")` handler 调用 `_dispatch(event, "<命令名>")`。

## 更新图片

将图片放入对应命令文件夹(支持 `png` / `jpg` / `jpeg` / `webp` / `gif` / `bmp`, 可放多张, 按文件名顺序发送), 然后在 WebUI 重载插件即可。
