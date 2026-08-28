# AstrBot 自动更新重载指南（GitHub Actions + SSH）

> 目标：**提交即生效**。每当 `main` 分支有新的 push（含 PR 合并），GitHub Actions 通过 **SSH 登录 AstrBot 所在服务器**，在服务器本地（`127.0.0.1:<端口>`）调用 AstrBot 的插件更新/重载 API，实现服务端 `git pull` + reload，无需手动进 WebUI。
>
> **适用场景**：AstrBot 端口不对外暴露（只监听 `127.0.0.1`），服务器在内网 / 无公网。通过 SSH 即可安全访问本机 AstrBot，无需公网暴露 API。

## 工作流概述

`.github/workflows/astrbot-deploy.yml` 在 `push` 到 `main`（或手动触发）时执行：

1. 读取 `metadata.yaml` 的 `name` 得到 `plugin_id`
2. **SSH 登录** AstrBot 所在服务器
3. 在服务器本地调用 `POST http://127.0.0.1:<port>/api/plugins/{plugin_id}/update` —— 让 AstrBot 重新拉取插件仓库（等价于 WebUI「更新插件」）
4. 调用 `POST http://127.0.0.1:<port>/api/plugins/reload` —— 重载插件，使新代码生效

> 插件必须**以 git clone 方式安装**（`metadata.yaml` 的 `repo` 指向本仓库），`update` 才会真正执行 `git pull`。若插件是以 zip/upload 方式安装，则不支持该自动更新路径。

---

## 一、服务器侧准备

1. **确认插件是 git 安装的**：AstrBot 仓库中 `data/plugins/astrbot_plugin_ama_10_entertainment_shu` 应是 `git clone` 下来的目录（存在 `.git`）。
2. **确认 SSH 可用**：服务器需运行 OpenSSH Server（Linux 默认），且存在一个可用于登录的账号。
3. **确认 AstrBot 端口监听在 127.0.0.1**：默认 `6185`。若已改为其它端口，在 GitHub Secret 中用 `ASTRBOT_PORT` 指定。
4. **创建 API Key**：
   - 打开 AstrBot WebUI → 设置（Settings）→ 找到「API Key」/「OpenAPI」部分；
   - 新建一个 API Key（形如 `abk_xxxxxxxx`）；
   - **权限 scope 必须包含 `plugin`**（否则调用会返回 403 `Insufficient API key scope`）；
   - 复制该 Key，稍后填入 GitHub Secrets。

---

## 二、生成 SSH 密钥对（推荐免密）

在**本地**生成一对 **ed25519** 密钥：

```bash
ssh-keygen -t ed25519 -C "astrbot-deploy" -f ~/.ssh/astrbot_deploy_ed25519
```

- 生成两个文件：`astrbot_deploy_ed25519`（**私钥**）和 `astrbot_deploy_ed25519.pub`（**公钥**）。
- 若设置了口令（passphrase），私钥填入 Secret 时还需配置 `SSH_PASSPHRASE`；建议**不设口令**，更省事。

将**公钥**追加到服务器的 `~/.ssh/authorized_keys`（以 `deploy` 用户为例）：

```bash
ssh-copy-id -i ~/.ssh/astrbot_deploy_ed25519.pub deploy@<服务器地址>
# 或手动
cat ~/.ssh/astrbot_deploy_ed25519.pub | ssh deploy@<服务器地址> \
  'mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys'
```

本地测试连接：

```bash
ssh -i ~/.ssh/astrbot_deploy_ed25519 deploy@<服务器地址> 'echo ok'
```

> 若服务器端禁用了密码登录、改过 SSH 端口、或限制来源 IP，记得相应调整 `SSH_PORT` 等配置。

---

## 三、GitHub 侧配置 Secrets（仓库机密）

在仓库 `Settings → Secrets and variables → Actions → New repository secret` 依次新建以下**必需**机密：

| Secret 名称 | 值 | 备注 |
|-------------|----|------|
| `SSH_HOST` | AstrBot 所在服务器地址（IP 或域名） | 必需 |
| `SSH_USER` | SSH 登录用户名 | 必需 |
| `SSH_PRIVATE_KEY` | **私钥全文**（`astrbot_deploy_ed25519` 内容） | 必需 |
| `ASTRBOT_API_KEY` | AstrBot API Key（`abk_xx...`），需含 `plugin` 权限 | 必需 |

**可选**机密：

| Secret 名称 | 值 | 默认 |
|-------------|----|------|
| `SSH_PORT` | SSH 端口 | `22` |
| `SSH_PASSPHRASE` | 私钥口令 | 无 |
| `SSH_FINGERPRINT` | 服务器 host key 指纹（启用主机校验） | 关闭 |
| `ASTRBOT_PORT` | AstrBot WebUI 端口 | `6185` |

> `plugin_id` 无需配置：工作流会从 `metadata.yaml` 的 `name` 字段自动读取。

### 关于 `SSH_FINGERPRINT`（推荐配置）

配置指纹可防止中间人攻击。获取方式：

```bash
ssh-keygen -F <服务器地址> -p   # 仅用于已知主机
# 或首次连接后查看
ssh-keyscan <服务器地址>
```

将返回的指纹填入 `SSH_FINGERPRINT`。工作流会自动启用 `host_key_check`。若不填，则关闭主机校验（仍可用，但安全性略低）。

---

## 四、触发方式

- **自动**：`push` 到 `main` 分支（含 PR 合并）会自动触发。
- **手动**：在 GitHub 仓库的 `Actions → AstrBot Deploy via SSH (Update + Reload) → Run workflow` 可手动触发。

---

## 五、运行结果与排错

在 `Actions` 页面查看每次运行日志。关键输出：

```
==== AstrBot 自动部署 (SSH -> localhost) ====
>>> 1/2 更新插件代码（服务端 git pull）...
{...服务端返回的 JSON...}
>>> 2/2 重载插件（让新代码生效）...
{...}
==== 部署成功 ====
```

常见错误：

| 现象 | 原因 | 解决 |
|------|------|------|
| SSH 连接失败 / `Host key verification failed` | 密钥未授权、端口/指纹不对 | 检查 `SSH_USER`、`SSH_PRIVATE_KEY`、`SSH_PORT`、`SSH_FINGERPRINT` |
| `Permission denied (publickey)` | 公钥未加入服务器 `authorized_keys` | 重新执行 `ssh-copy-id`，确认私钥对应公钥 |
| `401` | AstrBot API Key 未传或错误 | 检查 `ASTRBOT_API_KEY` |
| `403 Insufficient API key scope` | Key 缺少 `plugin` 权限 | 在 WebUI 重新生成含 `plugin` scope 的 Key |
| `404` | 端口或 `plugin_id` 不对 | 检查 `ASTRBOT_PORT`、`metadata.yaml` 的 `name` |
| 连接本机 `127.0.0.1` 被拒 | AstrBot 未运行或端口不对 | 在服务器确认 `ss -tlnp \| grep 6185` 或对应端口 |

---

## 六、进阶：改为仅在发布时更新

如果不想每次 push 都重载，可修改工作流的 `on.push` 触发条件，例如只在特定文件变化时触发：

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

---

## 七、安全建议

- **用最小权限账号**：为 CI 单独建一个 SSH 用户，只授予执行 `curl` 调用本机 AstrBot 所需权限，不要用 root。
- **私钥保密**：`SSH_PRIVATE_KEY` 属敏感机密，勿提交进仓库，只在 `Settings → Secrets` 保存。
- **关闭主机校验可选**：建议配置 `SSH_FINGERPRINT` 以启用主机校验，提升安全性。
- **不暴露 AstrBot 端口**：本方案全程在服务器本地 `127.0.0.1` 调用 AstrBot，公网无法访问该端口，API Key 不会暴露。
