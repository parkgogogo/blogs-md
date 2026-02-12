> 一句话摘要：OpenClaw 不是“更聪明的模型”，而是一套让 agent **长期在线、能接入聊天渠道、能按时触发任务、能调用工具并留下证据** 的运行时；本文按“怎么用”讲清楚概念与边界，并用同一套维度对比 Claude Code、Codex 和传统 prompt+loop agent。

### 先把话说死：OpenClaw 解决的是“运行时问题”

很多 agent 项目写着写着就会变成两种东西：

- 一种是“我在 IDE 里跟它结对编程”（工作区内循环，文件/测试/代码是主角）。
- 另一种是“我想让它在 Telegram 里随叫随到，定时做事，还能把结果落到文件里”（长期在线，I/O 与调度是主角）。

Claude Code 明显属于前者；OpenClaw 明显属于后者。

把它理解成“消息网关 + 任务调度 + 工具编排 + 工作区落盘”，后面概念就不容易乱。

### 5 分钟：确认你真的在用一个“在线运行时”

先不谈架构。先确认它能稳定完成一个闭环。

```bash
openclaw status
openclaw channels status
openclaw gateway status
```

怎么看算 OK：

- `openclaw status` 里 Gateway reachable。
- `openclaw channels status` 里目标渠道（比如 Telegram）状态 OK。

需要更“可复制给别人看”的一次性诊断输出：

```bash
openclaw status --all
```

### 你会反复遇到的几个名词（以及它们的边界）

这里不做百科式解释，只解释到“用的时候不会误用”。

**Gateway**

- 是什么：常驻进程，负责渠道连接、消息收发、会话路由、cron/heartbeat 调度。
- 入口：`openclaw gateway status` / `openclaw gateway restart`
- non-goals：不负责“聪明”，只负责“可靠收发 + 可靠调度”。把复杂逻辑塞进 Gateway 会把故障域搞大。

**Session**

- 是什么：一次消息触发的一轮执行上下文；可以包含多次工具调用。
- 入口：日常用 `openclaw status` 观察会话活跃与异常提示即可。
- 边界：一旦引入 tools，Session 的失败通常来自“外部动作卡住/超时”，不是“不会写字”。

**Tool**

- 是什么：能产生可验证外部效果的能力（读写文件、执行命令、抓网页、发消息、建定时任务）。
- 入口：在 OpenClaw 里就是 tool call；在工程落地上你只需要记住：工具的输出应该能被复查（路径、命令、URL）。
- 取舍：工具越强，权限与审批就越重要；否则就是在主机上放了一个“可被 prompt 注入的 shell”。

**Skill**

- 是什么：SOP（作业指导书）。固定“质量门槛”，不是固定“写作套路”。
- 正确用法：把 checklist 固化（必须给入口、必须给 recipes、必须落盘提交），节奏与文风留给终稿编辑。

**Workspace / Memory**

- Workspace：把结果落盘的地方；如果不落盘，就很难复用、很难 diff。
- Memory：保存偏好与上下文，但不能替代“把关键事实写进文件”。

**Cron vs Heartbeat**

- Cron：准点闹钟（准时、可追踪 run history）。
- Heartbeat：周期巡检（可漂移、适合合并多个检查）。

常用入口（够用就行）：

```bash
openclaw cron status
openclaw cron list
openclaw cron runs --id <jobId> --limit 20
```

### 一个能长期跑的用法：把“任务”写成可追踪的交付物

OpenClaw 真正比“聊天式 agent demo”强的地方，是它鼓励把结果变成可追踪交付：

- 写到文件（workspace）
- 提交到 git（可回滚、可审阅）
- 按时触发（cron）
- 把结果送回渠道（delivery）

这套组合拳决定了它适合做“长期助手”，而不是只适合做一次性问答。

### Recipes（照抄就能用）

#### Recipe：定时产出一条内容并送回聊天

目标：每天固定时间产出一条结构化结果（哪怕只是“提醒 + 链接 + 3 行摘要”）。

入口（先把运行面确认清楚）：

```bash
openclaw cron status
openclaw cron list
```

成功标志：

- 有 jobId；`openclaw cron runs` 里能看到 ok/error 的历史。

常见坑：

- 以为 cron 跑在“模型里”。不是的：cron 跑在 Gateway 里，Gateway 不常驻就不会触发。

#### Recipe：把一次写作变成可复用交付（落盘 + commit）

目标：别让内容只存在于聊天窗口；把文章落到 `blog.md/docs/clawbot/` 并提交。

成功标志：

- 文件落盘 + 有 commit（能 diff、能回滚）。

常见坑：

- 只生成文本不落盘，后续就只能靠记忆碰运气。

### 为什么它最近火（一个工程视角的解释）

一句话：很多人终于意识到，agent 的瓶颈不在“会不会推理”，而在“能不能长期在线把事做完”。

OpenClaw 把最容易被忽略的那部分做成了产品化能力：

- 渠道 I/O（收发、状态、连接）
- 调度（cron/heartbeat）
- 工具边界（可验证的外部动作）
- 交付介质（workspace 文件 + git）

这类能力不性感，但决定了“能不能每天用”。

### 对比：OpenClaw vs Claude Code vs Codex vs 传统 agent

这里不搞玄学名词，按使用场景拆。

**OpenClaw vs Claude Code**

- Claude Code 更像“在 repo 里结对编程”：改代码、跑测试、迭代反馈是主线。
- OpenClaw 更像“在收件箱/Telegram 里长期在线”：能按时触发、能跨工具做事、能把结果落到文件。
- 直接结论：写代码时优先 Claude Code；“长期助手/自动化”优先 OpenClaw。两者不是替代关系。

**OpenClaw vs Codex**

- Codex 更像发动机（模型能力）。
- OpenClaw 更像整车（运行时 + I/O + 调度 + 工具 + 交付）。
- 所以对比 Codex 时，别纠结“谁更聪明”，先问：谁能让任务闭环可追踪。

**OpenClaw vs prompt+loop agent**

- prompt+loop 的问题不是“不能跑”，而是“跑久了状态不可控、结果不可追溯”。
- OpenClaw 的取舍是工程化：宁可引入 Gateway/cron/workspace，也要把故障域和交付边界切清楚。

### non-goals（避免误用）

- OpenClaw 不替代网络/代理基础设施；出站不稳定会直接影响工具链。
- OpenClaw 不是自治体；越强的 tool 越需要最小权限与审批边界。

### 总结

- OpenClaw 的主价值是“运行时”：在线、可调度、可工具化、可落盘。
- 用它时优先围绕“任务闭环”组织概念，而不是背概念。
- 与 Claude Code/Codex 的差异不在智商，而在“你要在什么场景把事做完”。
