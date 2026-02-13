> 一句话摘要：如果你想要的不是“会聊天的模型”，而是一个能在 Telegram 里常驻、能准点跑任务、能调用工具、还能把结果落到文件并可追溯的助手——你需要的是运行时（runtime）。OpenClaw 就是这层。

### 主线任务：做一个每天 07:30 准点跑、跑完你能查账的日报

先别背 Gateway/Session 这些词。先把一个任务做出来：

- 每天 **07:30** 生成一段摘要（RSS、项目状态、或者“今天要做啥”都行）
- 写到 workspace 里一个文件（能 diff）
- 发回 Telegram
- 你能用 run history 证明它到底跑没跑

这条链路跑通，你对 OpenClaw 的理解就够用了。

### 5 分钟验活：别先改 prompt，先确认运行时在线

```bash
openclaw status
openclaw channels status
openclaw gateway status

openclaw cron status
openclaw cron list
```

什么叫“在线”：

- Gateway reachable
- Telegram 这种 channel adapter 状态 OK
- cron enabled，能列出 job

这一步都过不去，先别讨论“模型聪不聪明”，你还在 runtime 这一层。

### OpenClaw 不是“更聪明的 agent”，它把无聊的部分做成产品

多数 agent demo 挂掉的原因很无聊：

- 没有稳定的聊天 I/O
- 没有调度器
- 没有边界清晰的外部动作
- 没有交付物（对话结束就蒸发）

OpenClaw 反过来做：把“无聊但决定能不能每天用”的东西做成一等公民：

- **Gateway**：常驻进程，负责 I/O + 路由 + 调度
- **Session**：一次消息触发的一轮执行
- **Tool**：可验证的外部动作
- **Workspace**：文件式交付物（可 review、可提交、可回滚）

### Gateway：I/O + 调度的控制平面

Gateway 存在的意义很简单：模型不运行的时候，系统也要活着。

你日常需要记住的入口就两个：

```bash
openclaw gateway status
openclaw gateway restart
```

边界也简单：Gateway 越无聊越好。把重活塞进 I/O 循环，任何一次工具超时都可能变成“消息不回”。

### Session：一条消息触发的一轮工作

Session 是 OpenClaw 把“收到一条消息”变成“做完一轮事情”的容器。它可以在一次回合里串起多个 tool 调用。

一个很实用的心智模型：

- “不回”经常不是“模型不行”，而是“某个外部动作在等/在超时”。

### Tools：外部动作要能复查，不靠感觉

Tools 是 OpenClaw 能当助手的原因。

一个 tool 跑完应该留下你能指着看的证据：

- 写了哪个路径
- 跑了什么命令、退出码是多少
- 抓了哪个 URL
- cron jobId 是什么

有一个边界值得记住：

- `web_fetch` 是 HTTP + 可读性提取，它 **不执行 JS**。
- JS-heavy 或要登录的网站就别硬扛，换 browser 工具。

### Cron：让任务变成“能查账”的东西

cron 的关键不是“能定时”，而是“能追溯”。你关心的是：

- 到点有没有触发
- 触发了有没有成功
- 失败原因是什么

最常用的三个入口：

```bash
openclaw cron status
openclaw cron list
openclaw cron runs --id <jobId> --limit 20
```

另外一个“钉子”：cron 的 job 默认持久化在这里：

- `~/.openclaw/cron/jobs.json`

所以 Gateway 重启不会把你的计划清空。

### Workspace：交付物比聊天记录值钱

如果输出只在聊天窗口里，你没法：

- diff
- review
- 复用
- 集成到别的流程

把结果写到 workspace 文件里就行了：能提交、能回滚、能迭代。

官方默认路径是：

- `~/.openclaw/workspace`

### Recipes（照抄就能用）

#### Recipe 1：每天 07:30 产出文件 + 发 Telegram

目标：证明这条链路是闭环的（schedule → artifact → delivery → audit）。

做法（不写花活，只写最短路径）：

- 建一个每天 07:30 触发的 cron job
- job 做三件事：
  1) 写摘要到 workspace 某个路径
  2)（可选但推荐）commit
  3) 发一条摘要到 Telegram

成功标志：

- `openclaw cron runs --id <jobId>` 里能看到 `ok`
- 文件每天在变
- Telegram 能收到

常见坑：Gateway 不常驻，cron 就等于没电。

#### Recipe 2：把“看网页”变成可搜索笔记

目标：阅读不蒸发。

- 用 `web_fetch` 抓正文
- 总结
- 写进 workspace 的按日期归档 markdown

成功标志：过一周你还能在 workspace 里搜到这条笔记。

### 对比：别问“谁更聪明”，问“你的主战场在哪”

- **Claude Code** 更像 repo 内循环：读代码、改文件、跑命令、迭代。
- **OpenClaw** 更像长期在线的 ops 循环：聊天 I/O、调度、跨工具编排、交付物落盘。

一个粗暴但实用的规则：

- 产品在 repo 里 → Claude Code
- 工作流在 Telegram 里，还要准点跑 → OpenClaw

Codex 这种更像发动机（模型能力）。OpenClaw/Claude Code 是把发动机装进不同车型的“整车系统”。

### non-goals

- OpenClaw 不替代网络/代理基础设施；出站不稳会直接表现为工具失败。
- OpenClaw 不是自治体；tool 越强越需要最小权限和审批。

### 今天就复制的 3 件事

- 跑一次 runtime 检查：`openclaw status`、`openclaw channels status`、`openclaw cron status`
- 做一个 07:30 的 cron job，并强制它写一个 workspace 文件
- 把 `cron runs` 当账本：它要么跑了，要么没跑，不接受“感觉应该跑了”
