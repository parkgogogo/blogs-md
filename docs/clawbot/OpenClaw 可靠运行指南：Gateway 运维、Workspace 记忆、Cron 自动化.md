```bash
openclaw gateway status --deep
openclaw logs --follow
# 本机控制台（默认）：http://127.0.0.1:18789
# WebSocket（默认）：ws://127.0.0.1:18789
```

主线任务：把 OpenClaw 部署成一个长期运行、可远程访问、可审计的 Gateway，并用 workspace + cron 交付可维护的日常自动化。

## 组件与端口：Gateway、Clients、Nodes、Canvas host

把 OpenClaw 跑“可靠”，第一件事是把它当成一个控制面服务，而不是一次性的 CLI。

- **Gateway**：常驻进程。负责收发渠道消息、维护连接、调度 cron、提供控制面 API/WS。
- **Clients**：你在终端里敲的 `openclaw ...`、浏览器控制台、以及任何连接到 Gateway 的控制面。
- **Nodes**：成对设备（手机/树莓派/另一台电脑）。节点连接到同一个 Gateway，暴露摄像头/屏幕/位置/远程命令等能力。
- **Canvas host**：把可视化 UI（HTML/A2UI）跑在单独的服务/端口上（实现细节由配置决定；镜像文档示例里常见 18793）。

默认网络边界很明确：**Gateway 默认只监听 loopback**。

- 典型默认：`127.0.0.1:18789`（本机控制面、WS、UI）。
- 远程使用优先 VPN/Tailscale；其次才是 SSH 隧道（见后面）。

控制面 WS 链路可以用一句“协议节奏”记住：先握手拿到 snapshot，再靠事件流推进一次 agent run。

- `connect → hello-ok(snapshot) → event:* → req:agent → event:agent(streaming) → res:agent(final)`

## 安装与首次上线：onboard、configure、agents add

目标是 10 分钟内得到一个“可复现”的闭环：Gateway 常驻 + 能接到一条消息 + 能把回复送回去。

### 1) 安装 CLI 与运行时

```bash
node -v   # 需要 >= 22
npm install -g openclaw@latest
openclaw --help
```

### 2) 用向导把最小可用配置跑通

```bash
openclaw onboard --install-daemon
# 或：只做配置，不装守护
openclaw configure
```

向导默认值通常足够当“安全起点”：loopback、18789、token 鉴权、默认 workspace（`~/.openclaw/workspace`）。

### 3) 多 agent：把“工作台/会话/记忆”物理隔离

需要把一个 Gateway 服务多个“人格/用途”（工作、生活、家里设备）时，不要靠提示词硬分流，直接建新 agent：

```bash
openclaw agents add work
openclaw agents add home
```

隔离的价值：不同 workspace、不同 session 历史、不同 skills/工具约束，排障和回滚都更可控。

## Gateway 服务化与日常运维：status、logs、doctor、remote access

把 Gateway 当服务运维，日常就靠 3 条命令：状态、日志、体检。

### 每天会用到的检查动作

```bash
openclaw gateway status --deep
openclaw logs --follow
openclaw doctor
```

- `status --deep`：把“看起来在线”拆成可验证的探针。
- `logs --follow`：第一时间看重连、鉴权失败、工具超时。
- `doctor`：把常见环境问题（配置/依赖/权限）变成结构化诊断。

### 守护进程：让 Gateway 不依赖你开着终端

如果向导没装 daemon，后续补上：

```bash
openclaw gateway install
openclaw gateway restart
openclaw gateway stop
```

Linux 上如果用 systemd 且希望“用户退出登录也常驻”，需要启用 lingering：

```bash
sudo loginctl enable-linger <user>
```

### 远程访问：不暴露 18789 的前提下拿到控制面

最保守的远程方式是 SSH 隧道，把远端 loopback 映射到本机：

```bash
ssh -N -L 18789:127.0.0.1:18789 user@host
# 然后在本机打开：
# http://127.0.0.1:18789
```

规则：**只转发到 127.0.0.1:18789**；不要为了省事把 Gateway 直接 bind 到 `0.0.0.0` 再裸露公网。

### 多 Gateway：端口 + 配置 + state + workspace 必须成套隔离

同一台机器上跑多个 Gateway，最常见的失败是“端口没换”或“状态目录共用了”。

一条可复制的隔离启动方式：

```bash
OPENCLAW_CONFIG_PATH=~/.openclaw/openclaw-work.json \
OPENCLAW_STATE_DIR=~/.openclaw-state-work \
openclaw gateway --port 19001 --verbose
```

端口优先级也要记住：`--port → OPENCLAW_GATEWAY_PORT → gateway.port → 18789`。

## Workspace 文件地图：bootstrap、memory、skills、canvas

`~/.openclaw/workspace/` 是“行为与记忆”的落点，不是临时目录。

### 目录里哪些文件最关键

常见骨架（按运维重要性排序）：

- `AGENTS.md`：工作方式/规则（相当于运行时约束）。
- `SOUL.md`、`USER.md`、`IDENTITY.md`：身份与协作边界。
- `TOOLS.md`：环境相关的本地备忘（摄像头名、SSH 别名、TTS 偏好）。
- `HEARTBEAT.md`：允许在心跳时做的巡检清单（不是定时系统本体）。
- `memory/YYYY-MM-DD.md`：当日流水日志（可审计的“发生过什么”）。
- `skills/`：把交付标准写成可复用 SOP。
- `canvas/`：可视化界面资产（如果使用）。

### 哪些东西不该放进 workspace（也不该被 git 备份）

workspace 之外的敏感/状态型文件，通常在 `~/.openclaw/`：

- 配置：`~/.openclaw/openclaw.json`
- 凭据：`~/.openclaw/credentials/`
- 会话与运行时状态：常见在 `~/.openclaw/agents/<agentId>/sessions/`（实现细节以版本为准）

底线：**只备份可公开的“规则/流程/记忆摘要”，不要把 token、渠道密钥、凭据目录提交进仓库**。

### 用私有仓库备份 workspace（最小集合）

```bash
cd ~/.openclaw/workspace
git init
git add AGENTS.md SOUL.md USER.md IDENTITY.md TOOLS.md HEARTBEAT.md memory/ skills/
git commit -m "backup: agent workspace"
```

## 配置编辑与热重载：openclaw.json、config get/set、reload mode

配置的“可控”来自两点：**路径固定** + **修改可验证**。

### 配置文件路径与最小编辑闭环

配置文件默认在：`~/.openclaw/openclaw.json`。

先读再改，避免“改错字段导致 Gateway 起不来”：

```bash
openclaw config get agents.defaults.workspace
openclaw config set agents.defaults.workspace "~/.openclaw/workspace"
openclaw config set agents.defaults.heartbeat.every "2h"
openclaw config unset tools.web.search.apiKey
```

如果想直接编辑 JSON，也建议先用 `config get` 确认字段路径真实存在，再落盘。

### 热重载模式：改完是热更新还是重启

Gateway 支持不同的 reload 策略（对运维影响巨大）：

- `gateway.reload.mode: hybrid`：默认思路，能热就热，必要时重启。
- `hot`：尽量不重启（但并非所有变更都能热更新）。
- `restart`：每次变更都重启（稳定但会有短暂不可用）。
- `off`：不自动 reload（适合严格的发布窗口）。

建议：生产化/长期运行时用 `hybrid`，并给一个小的 debounce，降低频繁写配置导致的抖动。

```json
{
  "gateway": {
    "reload": { "mode": "hybrid", "debounceMs": 300 }
  }
}
```

### 控制台入口

默认控制台：`http://127.0.0.1:18789`。远程访问时走 SSH 隧道/内网，不要直接公网暴露。

## Cron 自动化：任务模型、存储、常用配方

cron 的关键事实只有一个：**cron 跑在 Gateway 里**。Gateway 不常驻，cron 就等于不存在。

### 存储位置与审计方式

- 任务定义：`~/.openclaw/cron/jobs.json`
- 运行历史：`~/.openclaw/cron/runs/*.jsonl`

这两条路径是“可靠性抓手”：

- 想知道有没有创建成功，看 `jobs.json`。
- 想知道有没有触发/为什么失败，看 `runs/*.jsonl`。

### 两种执行风格：main 的 systemEvent / isolated 的 agentTurn

- **main / systemEvent**：把一个系统事件投递到主会话里（适合“提醒主助理处理一下”）。
- **isolated / agentTurn**：在隔离会话 `cron:<jobId>` 里执行一次完整回合（适合“自己跑完并把结果投递出去”）。

投递控制常用两件：

- `delivery.mode: announce|none`：要不要对外发一条消息。
- `delivery.channel` / `delivery.to`：发到哪。

另外，唤醒策略是显式字段：`wakeMode: now|next-heartbeat`。

### 立即可抄的 3 个配方

#### 配方 1：一次性提醒（到点就删）

```bash
openclaw cron add \
  --name "Pay rent" \
  --at "2026-03-01T01:00:00Z" \
  --session main \
  --system-event "提醒：交房租" \
  --wake now \
  --delete-after-run
```

#### 配方 2：每天固定时间做事（隔离执行 + 对外投递）

```bash
openclaw cron add \
  --name "Daily brief" \
  --cron "0 7 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "生成今日简报：日历 + 待办 + 天气；只发结论" \
  --announce \
  --channel telegram \
  --to "chat:<your_chat_id>"
```

#### 配方 3：把“会不会触发”变成可测试的事实

```bash
openclaw cron list
openclaw cron run <job-id>
openclaw cron runs --id <job-id> --limit 20
```

### 运维开关：快速禁用 cron

排查问题或临时降低噪声时，可以直接禁用 cron（注意：这是 Gateway 侧行为）：

```bash
OPENCLAW_SKIP_CRON=1 openclaw gateway restart
```

## 长任务与后台进程：exec、process、pty、超时与回收

可靠性不只在“有没有触发”，还在“长任务不会把整个回合拖死”。

### 什么时候该把 exec 后台化

- 拉依赖、构建、下载、抓取大量网页。
- 需要交互式 TTY（例如某些登录/确认界面）。

典型参数：

- `yieldMs`：前台等多久再返回。
- `background: true`：立刻后台跑。
- `pty: true`：需要 TTY 时打开。
- `timeout`：别让任务无限挂。

（工具层面语义）后台会话返回 `sessionId`，再用 `process` 跟踪：

- `process list`：列出会话
- `process poll/log`：看输出
- `process kill`：终止

关键限制要记住：**后台会话不落盘，进程重启会丢**。需要持久化审计的任务，用 cron + 文件输出。

### 可调默认值（配置侧）

长任务经常需要把默认超时/清理策略调得更贴合环境：

- `tools.exec.backgroundMs`
- `tools.exec.timeoutSec`
- `tools.exec.cleanupMs`

## 故障签名与定位顺序：端口冲突、未授权、配置校验失败、cron 不触发

这里不靠“感觉”，靠错误字符串分流。

### 1) 端口冲突 / Gateway 起不来：EADDRINUSE / GatewayLockError

特征：启动时报 `EADDRINUSE`，或提示 `GatewayLockError("another gateway instance ...")`。

处理顺序：

1) 先确认是不是已有实例在用 18789：
   - `openclaw gateway status`
2) 需要并行跑第二个实例：直接换端口并隔离 state/config：

```bash
openclaw gateway --port 19001
```

### 2) 未授权：能连上端口但所有操作都被拒

默认鉴权是“安全默认”。症状通常是控制台/CLI 报 auth/token 错误。

处理：

- 确认环境变量/配置里 token 一致（例如 `OPENCLAW_GATEWAY_TOKEN`）。
- 不要用“临时关鉴权”来图快；先把远程访问改成 VPN/SSH 隧道。

### 3) 配置校验失败：Gateway 不启动，只剩诊断命令可用

特征：改了 `~/.openclaw/openclaw.json` 后 Gateway 起不来。

处理顺序：

1) `openclaw doctor` 看校验错误位置
2) 回滚到上一次可用配置（提前把 openclaw.json 纳入备份/版本管理）
3) 再用 `openclaw config set` 小步修改，避免一次性大改

### 4) cron 不触发：job 在，但 run 记录为空

特征：`openclaw cron list` 看得到任务，但没有任何 run 历史。

处理顺序：

1) Gateway 必须常驻：`openclaw gateway status --deep`
2) 确认没被禁用：不要设置了 `OPENCLAW_SKIP_CRON=1`
3) 直接手工触发一次：`openclaw cron run <job-id>`
4) 去 `~/.openclaw/cron/runs/*.jsonl` 找 error/ok

## 运行到“随时可用”的最小检查清单（可复制到值班手册）

- Gateway 健康：`openclaw gateway status --deep`
- 日志无持续报错：`openclaw logs --follow`（重点看重连/鉴权失败/超时）
- 配置可读：`openclaw config get agents.defaults.workspace` → 指向 `~/.openclaw/workspace`
- cron 可审计：`ls ~/.openclaw/cron/jobs.json`，并能用 `openclaw cron runs --id <jobId>` 查到记录
- 远程可控但不暴露公网：`ssh -N -L 18789:127.0.0.1:18789 user@host`

## 参考资料

- OpenClaw — Personal AI Assistant (GitHub README) — https://github.com/openclaw/openclaw
- Agent Workspace — OpenClaw Docs — https://docs.openclaw.ai/concepts/agent-workspace
- Gateway Runbook — OpenClaw Docs — https://docs.openclaw.ai/gateway
- Cron Jobs (Gateway scheduler) — OpenClaw Docs — https://docs.openclaw.ai/automation/cron-jobs
- Configuration — OpenClaw Docs — https://docs.openclaw.ai/gateway/configuration
- Onboarding Wizard (CLI) — OpenClaw Docs — https://docs.openclaw.ai/start/wizard
- Gateway architecture — OpenClaw Docs (openclawcn mirror) — https://openclawcn.com/en/docs/concepts/architecture/
- Background Exec + Process Tool — OpenClaw Docs (openclawcn mirror) — https://openclawcn.com/en/docs/gateway/background-process/
- Gateway lock — OpenClaw Docs (openclawcn mirror) — https://openclawcn.com/en/docs/gateway/gateway-lock/
