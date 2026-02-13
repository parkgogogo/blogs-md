> 一句话摘要：如果目标是“让一个 agent 常驻在线、能按时跑任务、能把结果落到文件并送回 Telegram”，OpenClaw 属于那种把脏活累活做完的运行时；这篇文档用一个可复制的主线任务把 Gateway / Session / Tool / Cron / Workspace 的边界讲清楚，并顺手对比 Claude Code、Codex。

### 主线任务：每天 07:30 自动发一条日报，并且能追溯它到底跑没跑

先别背概念。先把一个任务跑通：

- 每天 07:30 生成一条摘要（可以是 RSS 摘要、项目进展、或者“今天要做啥”）
- 写入 workspace 的一个文件（可 diff）
- 把摘要发回 Telegram
- 你能查到它的 run history：成功了还是报错了

你会发现：一旦这个任务跑通，OpenClaw 的绝大多数设计都变得顺理成章。

### 5 分钟体检：确认“运行时”在工作，而不是只会聊天

先看网关与渠道是否在线：

```bash
openclaw status
openclaw channels status
openclaw gateway status
```

再看调度器是否真的在跑：

```bash
openclaw cron status
openclaw cron list
```

如果这两步都过不去，先别谈“agent 能力”，那是另一层问题。

### 为什么 OpenClaw 不是“另一个更聪明的 agent”

很多所谓 agent 的瓶颈不是推理，而是运行时：

- 能不能稳定接住 Telegram/WhatsApp 的消息（连接、重试、速率限制）
- 能不能按时触发（准点、可追溯、可重跑）
- 能不能做外部动作（写文件、跑命令、抓网页）并且留下证据

OpenClaw 把这部分工程化地做成了一层：消息进来 → 一轮执行 → 外部动作 → 消息出去。

### Gateway / Session / Tool：把边界切清楚，系统才会稳定

先给一句最实用的版本：

- **Gateway** 负责“收发与调度”——它得常驻在线，保证渠道连着、cron 能触发。
- **Session** 负责“一次消息触发的一轮执行”——该轮执行可以包含多次工具调用。
- **Tool** 负责“可验证的外部动作”——写到哪个路径、执行了什么命令、抓了哪个 URL，都能复查。

这三者分层的意义不玄学：它把故障域拆开了。I/O 抖动、工具超时、模型输出质量，属于不同层的问题。

你平时用得到的入口就这几个：

```bash
openclaw gateway status
openclaw gateway restart
openclaw status --all
```

### Workspace：为什么它几乎是 OpenClaw 的“默认数据库”

如果输出只存在聊天窗口里，那它天然不可复用：

- 没法 diff
- 没法回滚
- 没法被其它工具二次加工

所以 OpenClaw 更适合把结果落到 workspace 文件里，再决定要不要发回 Telegram。

一个很实用的习惯：把“可交付”的东西都当文件管理，而不是当对话管理。

### Cron：让任务变成“可以查账”的东西

cron 的关键不是“能定时”，而是“能追溯”。你需要的是：

- 任务有没有触发
- 触发了有没有成功
- 失败原因是什么

入口基本就三条：

```bash
openclaw cron status
openclaw cron list
openclaw cron runs --id <jobId> --limit 20
```

背后的落盘位置也值得记一下：cron jobs 默认持久化在 `~/.openclaw/cron/jobs.json`（这样 Gateway 重启不会丢）。

### Recipes：围绕主线任务，把 OpenClaw 用起来

#### Recipe：每天 07:30 产出文件 + 发一条消息

目标：你能在 `cron runs` 里看到每次执行的结果；你能在 workspace 里看到每天的输出文件。

最短步骤（先以“能跑”为准，内容简单点）：

1) 先建一个 cron job（命令行或 dashboard 都行）。
2) job 的动作固定成三件事：
   - 把摘要写入某个路径（例如 `blog.md/docs/clawbot/daily.md`）
   - 提交 git（可选，但强烈建议）
   - 发回 Telegram

成功标志：

- `openclaw cron runs --id <jobId>` 能看到 ok
- 目标文件有更新，并且内容可追溯到某次 run

常见坑（只写一个最常见的）：Gateway 没常驻，cron 根本没机会触发。

#### Recipe：把“阅读 RSS → 总结 → 落盘”变成流水线

目标：阅读不是“刷过去”，而是沉淀成可搜索的笔记。

做法：

- scan 出新增文章（例如用 RSS 工具）
- 抽样抓取正文
- 只写三件事：这篇文章在解决什么问题、它用了什么证据、它在结构上有什么可抄的写法
- 写入 workspace 的一份笔记文件（按日期归档）

这条流水线跑一周，你会明显感觉写作风格在变。

### OpenClaw、Claude Code、Codex：别用“谁更聪明”来对比

有个简单拆法：看你工作的主战场在哪里。

- 你的主战场在 **repo 内**（改代码、跑测试、迭代反馈）：Claude Code 更顺手。
- 你的主战场在 **聊天与日程**（长期在线、按时触发、跨工具编排、交付物落盘）：OpenClaw 更顺手。

Codex 更像发动机（模型能力）；OpenClaw/Claude Code 更像“把发动机装进不同车型的整车系统”。

### non-goals（别拿它干它不擅长的事）

- OpenClaw 不替代你的网络/代理基础设施；出站不稳时，工具链会超时或失败。
- OpenClaw 不是自治体；tool 能力越强，越要最小权限与审批边界。

### 收尾：用 OpenClaw 的正确姿势

- 先选一个主线任务跑通闭环（cron + workspace + delivery）。
- 再回头理解概念边界（Gateway/Session/Tool）。
- 最后把输出变成文件与提交：能查账、能复用、能迭代。
