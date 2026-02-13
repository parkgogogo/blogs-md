# 自建 AI 网关：把聊天软件变成你的智能助手

一个能在 72 小时内获得 60,000+ GitHub stars 的开源项目，背后站着 PSPDFKit 创始人 Peter Steinberger——OpenClaw 的爆火不是偶然。这是一款面向开发者的自托管 AI 网关，让你在自己机器上运行的 AI 助手，通过 Telegram、WhatsApp、Discord 等日常聊天软件与你对话。

**主线任务**：在本地运行 OpenClaw Gateway，连接 Telegram，发送第一条消息并获得 AI 回复。成功标志是在 Telegram 中收到 AI 助手的回复，且能在浏览器打开 Control UI 查看网关状态。

### 让它先跑起来

安装需要 Node.js 22 或更高版本。运行全局安装：

```bash
npm install -g openclaw@latest
```

安装完成后，执行 onboarding 向导：

```bash
openclaw onboard --install-daemon
```

这个向导会引导你完成 Gateway 初始化、API 密钥配置（推荐 Anthropic）、以及系统服务的安装。`--install-daemon` 参数会同时安装后台服务，让 Gateway 随系统启动。

现在启动 Gateway：

```bash
openclaw gateway --port 18789 --verbose
```

你会看到 Control UI 运行在 http://127.0.0.1:18789/。打开浏览器访问这个地址，能看到网关状态页——这证明 Gateway 已经正常工作。

如果之前没有使用 `--install-daemon`，也可以用以下命令让 Gateway 作为服务运行：

```bash
openclaw gateway install
```

Gateway 支持热重载配置，大多数配置变更无需重启。热重载模式默认是 `hybrid`：安全变更即时生效，关键变更自动重启。你也可以设置为 `hot`（只热应用安全变更）、`restart`（任何变更都重启）或 `off`（完全关闭）。

### 接入 Telegram：最简单的一步

在所有支持的聊天平台中，Telegram 配置最为简单——你不需要扫描二维码，不需要手机保持在线，只需一个 bot token。

找 @BotFather 创建新 bot，拿到 token（格式如 `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`）。然后在 Gateway 的 Control UI 配置页面，或直接用 CLI 添加：

```bash
openclaw config set channels.telegram.botToken "你的token"
openclaw config set channels.telegram.enabled true
```

Telegram 通道默认使用 `pairing` 模式：陌生用户首次发送消息时，会被要求等待配对批准，你不会收到未经同意的消息。配对码是 8 位大写字母，有效期 1 小时。

在 Telegram 向你的 bot 发送任意消息，然后查看 Gateway 日志：

```bash
openclaw logs --follow
```

你会看到一条配对请求，包含类似 `CODE: ABCD1234` 的配对码。批准它：

```bash
openclaw pairing approve telegram ABCD1234
```

现在发送测试消息：

```bash
openclaw message send --channel telegram --target @你的bot用户名 --message "你好"
```

或在 Telegram 中直接向 bot 发送消息。如果一切正常，AI 助手会在几秒内回复。这就是成功标志：消息发出，回复收到，Gateway 的 Control UI 显示活跃会话。

### 控制谁能发消息给你

自托管的核心是你掌控数据边界。OpenClaw 的安全模型基于白名单而非黑名单。

默认 `dmPolicy` 是 `pairing`，适合个人使用：每个新对话者都需要你显式批准。如果你只想让特定用户访问，可以改用 `allowlist` 模式：

```bash
openclaw config set channels.telegram.dmPolicy allowlist
openclaw config set channels.telegram.allowFrom '["你的telegram_id", "同事id"]'
```

Telegram ID 是数字格式。想安全获取自己的 ID，无需使用第三方 bot：直接向 bot 发消息，然后从 `openclaw logs --follow` 的 `from.id` 字段读取。

`allowFrom` 支持多种格式：纯数字 ID、带 `@` 的用户名、或带 `telegram:` / `tg:` 前缀的形式。OpenClaw 会自动归一化。

还有一个更开放但不推荐的模式 `open`：允许任何人发消息。这需要同时设置 `allowFrom` 包含 `"*"` 才会生效。

对于群聊，策略独立控制。`groupPolicy` 默认是 `allowlist`，只允许白名单内成员在群中触发 bot。`requireMention` 默认为 true，意味着 bot 只在被 `@` 时响应。

### 理解 Gateway 的决策边界

Gateway 不只是聊天机器人的中间层——它是 sessions、routing、channel connections 的单一真相源。这是你与 AI 助手之间的控制平面。

当消息从 Telegram 进入，Gateway 会：

1. 验证发送者身份（检查配对状态和白名单）
2. 创建或恢复 session（基于聊天 ID 隔离）
3. 将消息路由给 agent runtime
4. 收集 AI 回复并通过原通道返回

Session 数据存储在 `~/.openclaw/agents/<agent>/sessions/<session>.jsonl`，每行一条消息记录。这意味着你的对话历史完全保存在本地，不会上传到任何第三方——除非你使用远程模型 API。

配置存储在 `~/.openclaw/openclaw.json`。这是个可选文件；如果不存在，OpenClaw 使用安全默认值运行。配置支持环境变量替换，语法是 `${VAR_NAME}`：

```json
{
  "models": {
    "providers": {
      "anthropic": {
        "apiKey": "${ANTHROPIC_API_KEY}"
      }
    }
  }
}
```

缺失的环境变量会在加载时报错。如果需要字面量 `$`，用 `$${VAR}` 转义。

### 它能做什么：从发消息到控制浏览器

OpenClaw 内置的工具集覆盖常见自动化场景：

- **browser**：控制浏览器访问网页、截屏、执行页面操作
- **canvas**：可视化工作区，支持 agent 驱动的图形界面
- **nodes**：管理配对设备（iOS/Android/macOS 节点）
- **cron**：定时任务调度
- **fs/filesystem**：文件系统操作
- **exec**：执行 shell 命令（可配置沙箱）

工具权限通过 profiles 控制：`minimal`（仅 session 状态）、`coding`（文件+运行时+会话）、`messaging`（消息相关）、`full`（全部工具）。你也可以用工具组 shorthand，如 `group:runtime`、`group:fs`、`group:web`。

Agent 每次启动时会读取工作区中的 bootstrap 文件：`AGENTS.md`（代理规范）、`SOUL.md`（身份定义）、`TOOLS.md`（工具笔记）、`IDENTITY.md`（身份详情）、`USER.md`（用户偏好）。这些 Markdown 文件作为系统提示词的一部分注入，让 AI 助手了解上下文。

### 常见问题排查

如果 Gateway 启动失败，先运行诊断：

```bash
openclaw doctor
```

这个命令会检查配置合法性、OAuth token 有效期、目录权限、以及 Gateway 健康状态。添加 `--fix` 参数可以自动修复可修复的问题（如配置格式迁移、权限调整）。

如果配置验证失败，Gateway 不会启动，只有诊断命令可用。这是安全设计：错误的配置可能导致安全漏洞或数据丢失。

端口冲突是常见问题。Gateway 默认使用 18789。如果启动时报端口被占用，检查是否有其他 Gateway 实例在运行，或 SSH 隧道占用了该端口。`openclaw doctor` 会自动检测这种情况。

另一个常见问题是权限。如果运行 Gateway 的用户和安装时的用户不同，可能导致状态目录无法写入。检查 `~/.openclaw` 目录的所有权。

### 下一步

现在你已经有一个工作的 Gateway 和 Telegram 通道。接下来可以：

1. **连接更多平台**：WhatsApp（需 QR 配对）、Discord、Slack、Signal 等都支持。同时启用多个通道时，OpenClaw 会根据消息来源路由回复。

2. **配置定时任务**：使用 `openclaw cron add` 创建周期性任务。语法类似 cron，但触发的是 agent 而非 shell 命令。

3. **探索 Control UI**：http://127.0.0.1:18789/ 提供配置管理、会话查看、以及实时日志。你可以在这里调整配置而无需编辑 JSON 文件。

4. **备份工作区**：`~/.openclaw/workspace/` 包含你的自定义技能和代理配置。建议用 git 管理，方便迁移和版本控制。

5. **阅读安全建议**：执行 `openclaw doctor` 会提示潜在的安全风险配置，比如开放的 DM 策略或缺失的 Gateway 认证 token。

---

**参考与延伸阅读**

- OpenClaw 官方文档：https://docs.openclaw.ai/
- GitHub 仓库：https://github.com/openclaw/openclaw
- DigitalOcean 入门指南：https://www.digitalocean.com/resources/articles/what-is-openclaw
- 配置文件参考：https://docs.openclaw.ai/gateway/configuration
- 聊天通道文档：https://docs.openclaw.ai/channels
- Agent 运行时详解：https://docs.openclaw.ai/concepts/agent
