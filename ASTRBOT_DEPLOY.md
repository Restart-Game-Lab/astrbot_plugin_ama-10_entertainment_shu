# AstrBot 自动更新重载指南（GitHub Actions）

> 目标：**提交即生效**。每当 `main` 分支有新的 push（含 PR 合并），GitHub Actions 自动调用你部署的 AstrBot，让服务端 `git pull` 拉取最新插件代码并重载插件，无需手动进 WebUI。

## 工作流概述

`.github/workflows/astrbot-deploy.yml` 在 `push` 到 `main`（或手动触发）时执行：

1. 读取 `metadata.yaml` 的 `name` 得到 `plugin_id`
2. 调用 `POST /api/plugins/{plugin_id}/update` —— 让 AstrBot 重新拉取插件仓库（等价于 WebUI「更新插件」）
3. 调用 `POST /api/plugins/reload` —— 重载插件，使新代码生效

> 插件必须**以 git clone 方式安装**（`metadata.yaml` 的 `repo` 指向本仓库），`update` 才会真正执行 `git pull`。若插件是以 zip/upload 方式安装，则不支持该自动更新路径。

---

## 一、AstrBot 侧准备

1. **确认插件是 git 安装的**：AstrBot 的仓库中 `data/plugins/astrbot_plugin_ama_10_entertainment_shu` 应是 `git clone` 下来的目录（存在 `.git`）。
2. **创建 API Key**：
   - 打开 AstrBot WebUI → 设置（Settings）→ 找到「API Key」/「OpenAPI」部分；
   - 新建一个 API Key（形如 `abk_xxxxxxxx`）；
   - **权限 scope 必须包含 `plugin`**（否则调用会返回 403 `Insufficient API key scope`）。
   - 复制该 Key，稍后填入 GitHub Secrets。

3. **确认 WebUI 可被访问**：
   - 默认端口 `6185`，默认绑定 `0.0.0.0`；
   - 若 AstrBot 部署在局域网/服务器，需保证 GitHub Actions 的运行器能访问到该地址。
   - ⚠️ **如果服务器在内网且无公网 IP**，GitHub 托管的 Actions 无法直接访问内网地址。此时有两种可选方案：
     - **方案 A（推荐，无需公网）**：使用**自托管 runner**（self-hosted runner），让它在你的内网/服务器上运行，这样就能访问 `http://127.0.0.1:6185` 或内网地址。
     - **方案 B**：给服务器做公网暴露（反向代理 + 域名），并把公网地址填入 `ASTRBOT_URL`。**注意**：这样 API Key 会暴露在公网，务必用防火墙/HTTPS 保护好。

---

## 二、GitHub 侧配置 Secrets

在仓库 `Settings → Secrets and variables → Actions → New repository secret` 新建两个：

| Secret 名称 | 值 |
|-------------|----|
| `ASTRBOT_URL` | AstrBot WebUI 地址，例如 `http://127.0.0.1:6185`（自托管）或 `http://192.168.1.10:6185` |
| `ASTRBOT_API_KEY` | 上一步创建的 API Key（`abk_xx...`），需含 `plugin` 权限 |

> `plugin_id` 无需配置：工作流会从 `metadata.yaml` 的 `name` 字段自动读取。

---

## 三、触发方式

- **自动**：`push` 到 `main` 分支（含 PR 合并）会自动触发。
- **手动**：在 GitHub 仓库的 `Actions → AstrBot Deploy (Update + Reload) → Run workflow` 可手动触发，并可勾选 `dry_run` 只打印请求、不改动。

---

## 四、运行结果与排错

在 `Actions` 页面查看每次运行日志。关键输出：

```
==== AstrBot 自动部署 ====
>>> 1/2 更新插件代码（服务端 git pull）...
{...服务端返回的 JSON...}
>>> 2/2 重载插件（让新代码生效）...
{...}
==== 部署成功 ====
```

常见错误：

| 现象 | 原因 | 解决 |
|------|------|------|
| `401` | API Key 未传或错误 | 检查 `ASTRBOT_API_KEY` |
| `403 Insufficient API key scope` | Key 缺少 `plugin` 权限 | 在 WebUI 重新生成含 `plugin` scope 的 Key |
| `404` | 地址或 `plugin_id` 不对 | 检查 `ASTRBOT_URL`、`metadata.yaml` 的 `name` |
| 网络无法连接 | GitHub 托管 runner 无法访问内网 | 改用自托管 runner，或暴露公网地址 |

---

## 五、进阶：改为仅在发布时更新

如果不想每次 push 都重载，可修改工作流的 `on.push` 触发条件，例如只在版本号变化时触发：

```yaml
on:
  push:
    branches: [main]
    paths:
      - 'main.py'
      - 'metadata.yaml'
      - 'src/**'
```

或在 `push` 基础上，把发布 tag 也纳入：

```yaml
on:
  push:
    branches: [main]
  push:
    tags: ['v*'] # 注意：不能同时写两个 push，需合并或拆分
```

（GitHub Actions 不允许同一事件重复出现，若要同时监听分支与 tag，请分别拆分或使用 `workflow_dispatch` + 手动触发。）
