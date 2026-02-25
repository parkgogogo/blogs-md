# Stevens: 一个可破解的 AI 助手

**原文标题:** Stevens: a hackable AI assistant using a single SQLite table and a handful of cron jobs  
**原文作者:** Geoffrey Litt  
**原文链接:** https://geoffreylitt.com/2025/04/12/how-i-made-a-useful-ai-assistant-with-one-sqlite-table-and-a-handful-of-cron-jobs.html  
**翻译日期:** 2025-02-25

---

> There's a lot of hype these days around patterns for building with AI. Agents, memory, RAG, assistants—so many buzzwords! But the reality is, **you don't need fancy techniques or libraries to build useful personal tools with LLMs.**

如今，关于使用 AI 构建应用的模式有很多炒作。智能体、记忆、RAG、助手——这么多流行词！但现实是，**你不需要花哨的技术或库就能用 LLM 构建有用的个人工具。**

> In this short post, I'll show you how I built a useful AI assistant for my family using a dead simple architecture: a single SQLite table of memories, and a handful of cron jobs for ingesting memories and sending updates, all hosted on [Val.town](https://www.val.town). The whole thing is so simple that you can easily copy and extend it yourself.

在这篇短文中，我将向你展示我是如何为家人构建一个有用的 AI 助手的，使用极其简单的架构：一个 SQLite 记忆表，以及几个用于摄取记忆和发送更新的定时任务，全部托管在 [Val.town](https://www.val.town) 上。整个系统如此简单，你可以轻松复制并扩展它。

---

## Meet Stevens | 认识 Stevens

> The assistant is called Stevens, named after the butler in the great Ishiguro novel [Remains of the Day](https://en.wikipedia.org/wiki/The_Remains_of_the_Day). Every morning it sends a brief to me and my wife via Telegram, including our calendar schedules for the day, a preview of the weather forecast, any postal mail or packages we're expected to receive, and any reminders we've asked it to keep track of. All written up nice and formally, just like you'd expect from a proper butler.

这个助手叫 Stevens，名字来源于石黑一雄的伟大小说[《长日留痕》](https://en.wikipedia.org/wiki/The_Remains_of_the_Day)中的管家。每天早上，它会通过 Telegram 给我和妻子发送简报，包括当天的日程安排、天气预报预览、我们可能收到的邮件或包裹，以及我们让它记录的任何提醒。所有内容都写得正式得体，就像你期望从一位真正的管家那里得到的那样。

> Here's an example. (I'll use fake data throughout this post, beacuse our actual updates contain private information.)

这里有一个例子。（我在本文中将使用假数据，因为我们的实际更新包含私人信息。）

> Beyond the daily brief, we can communicate with Stevens on-demand—we can forward an email with some important info, or just leave a reminder or ask a question via Telegram chat.

除了每日简报，我们可以随时与 Stevens 交流——我们可以转发包含重要信息的邮件，或者通过 Telegram 聊天留下提醒或提问。

> That's Stevens. It's rudimentary, but already more useful to me than Siri!

这就是 Stevens。它很简陋，但对我来说已经比 Siri 更有用了！

---

## Behind the scenes | 幕后架构

> Let's break down the simple architecture behind Stevens. The whole thing is hosted on [Val.town](https://www.val.town), a lovely platform that offers SQLite storage, HTTP request handling, scheduled cron jobs, and inbound/outbound email: a perfect set of capabilities for this project.

让我们来剖析 Stevens 背后的简单架构。整个系统托管在 [Val.town](https://www.val.town) 上，这是一个很棒的平��，提供 SQLite 存储、HTTP 请求处理、定时 cron 任务和收发邮件功能：这是一套完美适合这个项目的能力组合。

> First, how does Stevens know what goes in the morning brief? The key is the butler's notebook, a log of everything that Stevens knows. There's an admin view where we can see the notebook contents—let's peek and see what's in there:

首先，Stevens 怎么知道每日简报里应该放什么？关键是管家的笔记本，一本记录 Stevens 所知道的一切的日志。有一个管理视图，我们可以在那里看到笔记本的内容——让我们偷偷看看里面有什么：

> You can see some of the entries that fed into the morning brief above—for example, the parent-teacher conference has a log entry.

你可以看到构成上述每日简报的一些条目——例如，家长会有一条日志记录。

> In addition to some text, entries can have a *date* when they are expected to be relevant. There are also entries with no date that serve as general background info, and are always included. You can see these particular background memories came from a Telegram chat, because Stevens does an intake interview via Telegram when you first get started:

除了一些文本外，条目可以有一个*日期*，表示它们预计何时相关。还有一些没有日期的条目作为一般背景信息，总是被包含在内。你可以看到这些特定的背景记忆来自 Telegram 聊天，因为 Stevens 在你刚开始使用时通过 Telegram 进行入职访谈：

> **With this notebook in hand, sending the morning brief is easy**: just run a cron job which makes a call to the Claude API to write the update, and then sends the text to a Telegram thread. As context for the model, we include any log entries dated for the coming week,以及 undated background entries.

**有了这个笔记本，发送每日简报就很容易了**：只需运行一个 cron 任务，调用 Claude API 来编写更新，然后将文本发送到 Telegram 线程。作为模型的上下文，我们包含任何日期为下一周的日志条目，以及没有日期的背景条目。

> Under the hood, the "notebook" is just a single SQLite table with a few columns. Here's a more boring view of things:

在底层，"笔记本"只是一个有几列的 SQLite 表。这是一个更无聊的视图：

> But wait: how did the various log entries get there in the first place? In the admin view, we can watch Stevens buzzing around entering things into the log from various sources:

但是等等：这些日志条目最初是怎么进入系统的呢？在管理视图中，我们可以看到 Stevens 从各种来源忙碌地将内容输入日志：

> This is just some data importers populating the table:

这只是一些数据导入器在填充表格：

> - An hourly data pull from the Google Calendar API
> - An hourly check of the local weather forecast using a weather API
> - I forward [USPS Informed Delivery](https://www.usps.com/manage/informed-delivery.htm) containing scans of our postal mail, and Stevens OCRs them using Claude
> - Inbound Telegram and email messages can also result in log entries
> - Every week, some "fun facts" get added into the log, as a way of adding some color to future daily updates.

- 每小时从 Google Calendar API 拉取数据
- 每小时使用天气 API 检查本地天气预报
- 我转发 [USPS Informed Delivery](https://www.usps.com/manage/informed-delivery.htm) 包含我们邮件扫描的邮件，Stevens 使用 Claude 进行 OCR 识别
- 收到的 Telegram 和邮件消息也可以生成日志条目
- 每周，一些"有趣的事实"会被添加到日志中，为未来的每日更新增添一些色彩

> **This system is easily extensible with new importers.** An importer is just any process that adds/edits memories in the log. The memory contents can be any arbitrary text, since they'll just be fed back into an LLM later anyways.

**这个系统可以轻松地通过新的导入器进行扩展。**导入器只是任何在日志中添加/编辑记忆的过程。记忆内容可以是任意文本，因为它们稍后反正会被反馈给 LLM。

---

## Reflections | 反思

> A few quick reflections on this project:

对这个项目的一些快速反思：

> **It's very useful for personal AI tools to have access to broader context from other information sources.** Awareness of things like my calendar and the weather forecast turns a dumb chatbot into a useful assistant. ChatGPT recently added memory of past conversations, but there's lots of information not stored within that silo. I've [written before](https://x.com/geoffreylitt/status/1810442615264796864) about how the endgame for AI-driven personal software isn't more app silos, it's small tools operating on a shared pool of context about our lives.

**对于个人 AI 工具来说，能够访问来自其他信息来源的更广泛上下文非常有用。**了解我的日历和天气预报等内容，将一个愚蠢的聊天机器人变成了一个有用的助手。ChatGPT 最近增加了对过去对话的记忆，但有很多信息并不存储在那个孤立系统中。我以前[写过](https://x.com/geoffreylitt/status/1810442615264796864)，AI 驱动的个人软件的终局不是更多的应用孤岛，而是基于我们生活共享上下文池运行的小型工具。

> **"Memory" can start simple.** In this case, the use cases of the assistant are limited, and its information is inherently time-bounded, so it's fairly easy to query for the relevant context to give to the LLM. It also helps that some modern models have long context windows. As the available information grows in size, RAG and [fancier](https://x.com/sjwhitmore/status/1910439061615239520) [approaches](https://arxiv.org/abs/2304.03442) to memory may be needed, but you can start simple.

**"记忆"可以从简单开始。**在这种情况下，助手的用例是有限的，它的信息本质上是有时限的，所以查询相关上下文提供给 LLM 是相当容易的。一些现代模型具有长上下文窗口也有帮助。随着可用信息规模的增长，可能需要 RAG 和[更复杂的](https://x.com/sjwhitmore/status/1910439061615239520)[记忆方法](https://arxiv.org/abs/2304.03442)，但你可以从简单开始。

> **Vibe coding enables sillier projects.** Initially, Stevens spoke with a dry tone, like you might expect from a generic Apple or Google product. But it turned out it was just more *fun* to have the assistant speak like a formal butler. This was trivial to do, just a couple lines in a prompt. Similarly, I decided to make the admin dashboard views feel like a video game, because why not? I generated the image assets in ChatGPT, and vibe coded the whole UI in Cursor + Claude 3.7 Sonnet; it took a tiny bit of extra effort in exchange for a lot more fun.

**氛围编码（Vibe coding）支持更有趣的项目。**最初，Stevens 以一种枯燥的语气说话，就像你可能期望的通用苹果或谷歌产品一样。但结果发现，让助手像一个正式管家那样说话更有趣。这很容易做到，只需要在提示中写几行。同样，我决定让管理仪表板视图感觉像电子游戏，因为为什么不呢？我在 ChatGPT 中生成了图像素材，并在 Cursor + Claude 3.7 Sonnet 中进行氛围编码完成整个 UI；这只需要一点点额外的努力，但换来的是更多的乐趣。

---

## Try it yourself | 自己动手试试

> Stevens isn't a product you can run out of the box, it's just a personal project I made for myself.

Stevens 不是一个开箱即用的产品，它只是我为我自己做的一个个人项目。

> But if you're curious, you can check out the code and fork the project [here](https://www.val.town/x/geoffreylitt/stevensDemo). You should be able to apply this basic pattern—a single memories table and an extensible constellation of cron jobs—to do lots of other useful things.

但如果你好奇，你可以在[这里](https://www.val.town/x/geoffreylitt/stevensDemo)查看代码并 fork 项目。你应该能够应用这个基本模式——一个记忆表和一个可扩展的 cron 任务群——来做很多其他有用的事情。

> I recommend editing the code using your AI editor of choice with the [Val Town CLI](https://github.com/val-town/vt) to sync to local filesystem.

我建议使用你选择的 AI 编辑器配合 [Val Town CLI](https://github.com/val-town/vt) 将代码同步到本地文件系统来编辑代码。

---

## 批判性思考与评论

### 1. 极简架构的哲学价值

作者展示了一种"足够好"的工程哲学。在技术世界充斥着复杂架构和过度设计的今天，Stevens 项目证明了一个核心观点：**解决实际问题的工具不需要追逐每一个技术潮流**。单个 SQLite 表 + 几个定时任务，这种"复古"的组合却能创造出比 Siri 更个性化的体验。这提醒我们，技术选型应该以问题为导向，而非以 hype 为导向。

### 2. 关于"个人上下文池"的洞察

作者提到 AI 驱动的个人软件的终局不是更多应用孤岛，而是基于共享上下文池的小型工具。这是一个深刻的洞察。目前的大型 AI 产品（如 ChatGPT、Claude）都在构建自己的记忆系统，但真正的个人 AI 应该是跨平台的、以用户为中心的。Stevens 的架构——从多个数据源（日历、邮件、天气）汇聚信息到一个统一的记忆表——预示了这种未来。

### 3. "氛围编码"的意义

"Vibe coding"（氛围编码）这个词精准地描述了当前 AI 辅助开发的新范式。当技术门槛降低到只需要"写几行提示"就能改变产品性格时，创造的乐趣和实验精神被重新点燃。Stevens 的管家人设不是功能性的必需品，但它让技术产品有了温度和个性。这提示我们：AI 时代的产品差异化可能不再来自核心功能，而是来自**用户体验的细微差别**。

### 4. 局限性与潜在风险

尽管这个项目令人耳目一新，但我们也应该看到其局限性：

- **隐私和安全**: 所有个人数据集中在一个 SQLite 表中，虽然方便但也成为单一故障点
- **可扩展性**: 作者自己也承认，当信息规模增长时，简单的查询可能不够，需要 RAG 等更复杂的方案
- **维护负担**: 个人项目的 cron 任务、API 集成需要持续维护，当依赖的服务（USPS、Google Calendar）改变 API 时，谁来维护？

### 5. 对开发者的启示

Stevens 项目最大的价值在于它提供了一个**可复制的最小可行 AI 助手（MVA - Minimum Viable Assistant）模板**。它展示了一个清晰的模式：
1. 统一的数据存储（记忆表）
2. 可插拔的数据源（导入器）
3. 基于 LLM 的生成层
4. 多渠道的输出（Telegram、邮件）

这个模式可以应用到无数场景：个人知识管理、家庭事务协调、小型团队的智能助手等。它降低了构建 AI 应用的认知门槛，让更多人可以从"用 AI"走向"造 AI"。

---

*🦞 由小龙虾翻译整理*
