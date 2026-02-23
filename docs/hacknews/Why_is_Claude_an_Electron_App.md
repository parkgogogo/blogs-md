URL: https://www.dbreunig.com/2026/02/21/why-is-claude-an-electron-app.html

## Why is Claude an Electron App?

为什么 Claude 是一个 Electron 应用？

### If code is free, why aren't all apps native?

如果代码是免费的，为什么不是所有应用都是原生的？

The state of coding agents can be summed up by [this fact](https://x.com/dbreunig/status/2024970389156495365?s=46)

编码智能体的现状可以用[这个事实](https://x.com/dbreunig/status/2024970389156495365?s=46)来总结：

Claude spent $20k on an agent swarm implementing (kinda) a C-compiler in Rust, but desktop Claude is an Electron app.

Claude 花费 2 万美元用智能体群实现了一个（某种意义上的）Rust 版 C 编译器，但桌面版 Claude 却是一个 Electron 应用。

If you're unfamiliar, Electron is a coding framework for building desktop applications using web tech, specifically HTML, CSS, and JS. What's great about Electron is it allows you to build one desktop app that supports Windows, Mac, and Linux. Plus it lets developers use existing web app code to get started. It's great for teams big and small. [Many apps you probably use every day are built with Electron](https://en.wikipedia.org/wiki/List_of_software_using_Electron?wprov=sfti1): Slack, Discord, VS Code, Teams, Notion, and more.

如果你不熟悉，Electron 是一个使用 Web 技术（特别是 HTML、CSS 和 JS）构建桌面应用的开发框架。Electron 的妙处在于它允许你构建一个支持 Windows、Mac 和 Linux 的桌面应用。此外，它让开发者可以使用现有的 Web 应用代码来开始开发。它对大小团队都很棒。[你可能每天使用的许多应用都是用 Electron 构建的](https://en.wikipedia.org/wiki/List_of_software_using_Electron?wprov=sfti1)：Slack、Discord、VS Code、Teams、Notion 等等。

There are downsides though. Electron apps are bloated; each runs its own Chromium engine. The minimum app size is usually a couple hundred megabytes. They are often laggy or unresponsive. They don't integrate well with OS features.

但也有缺点。Electron 应用臃肿；每个都运行自己的 Chromium 引擎。最小应用大小通常是几百兆字节。它们经常 laggy 或无响应。它们与操作系统功能集成不佳。

But now we have coding agents! [And one thing coding agents are proving to be pretty good at is cross-platform, cross-language implementations given a well-defined spec and test suite](https://www.dbreunig.com/2026/02/06/the-rise-of-spec-driven-development.html).

但现在我们有了编码智能体！[编码智能体被证明非常擅长的一件事是，给定一个定义良好的规范和测试套件，进行跨平台、跨语言的实现](https://www.dbreunig.com/2026/02/06/the-rise-of-spec-driven-development.html)。

On the surface, this ability should render Electron's benefits obsolete! Rather than write one web app and ship it to each platform, we should write one spec and test suite and use coding agents to ship native code to each platform. If this ability is real and adopted, users get snappy, performant, native apps from small, focused teams serving a broad market.

表面上看，这种能力应该使 Electron 的优势过时！与其编写一个 Web 应用并将其发布到每个平台，我们应该编写一个规范和测试套件，并使用编码智能体将原生代码发布到每个平台。如果这种能力是真实的并被采用，用户将从服务于广泛市场的小型专注团队那里获得快速、高性能的原生应用。

So why are we still using Electron and not embracing the agent-powered, spec driven development future?

那么为什么我们还停留在使用 Electron，而不是拥抱智能体驱动的、规范驱动的开发未来呢？

For one thing, coding agents are really good at the first 90% of dev. But that last bit – nailing down all the edge cases and continuing support once it meets the real world – remains hard, tedious, and requires plenty of agent hand-holding.

首先，编码智能体非常擅长开发的前 90%。但最后那一点——敲定所有边界情况并在接触现实世界后继续支持——仍然是困难、乏味的，并且需要大量的智能体 hand-holding。

Anthropic's [Rust-base C compiler](https://www.anthropic.com/engineering/building-c-compiler) slammed into this wall, after screaming through the bulk of the tests:

Anthropic 的[基于 Rust 的 C 编译器](https://www.anthropic.com/engineering/building-c-compiler)在快速通过大部分测试后撞上了这堵墙：

The resulting compiler has nearly reached the limits of Opus's abilities. I tried (hard!) to fix several of the above limitations but wasn't fully successful. New features and bugfixes frequently broke existing functionality.

生成的编译器几乎达到了 Opus 的能力极限。我（努力地！）尝试修复上述几个限制，但没有完全成功。新功能和错误修复经常破坏现有功能。

---

**批判性思考评论：**

这篇文章提出了一个尖锐的问题：如果 AI 编码智能体如此强大，为什么 Anthropic 自己的 Claude 桌面应用仍然使用 Electron 而非原生开发？

作者的诊断是：智能体擅长前 90% 的开发，但最后的 10%（边界情况处理、长期维护、现实世界适配）仍然困难。这个观察与软件开发中的"最后 10% 陷阱"相呼应——完成一个"能工作"的原型很容易，但要达到生产级别的健壮性则需要不成比例的努力。

关键洞察：
1. **规格驱动开发的局限**：即使有良好的规范和测试套件，跨平台原生开发仍然面临维护负担的三倍增长（Mac、Windows、Linux 各有一套代码库）。

2. **Electron 的持续优势**：虽然 Electron 应用臃肿且性能较差，但它提供了"一次编写，到处运行"的确定性，而这是智能体生成的原生代码目前无法匹敌的。

3. **组织现实**：Boris Cherny（Claude Code 团队成员）在 Hacker News 上的回应揭示了一个关键因素——许多 Claude Code 的工程师使用 Electron 是因为它适合快速原型，而他们优先考虑的是功能交付而非性能优化。

这篇文章提醒我们：技术选择往往由组织约束和业务优先级驱动，而不仅仅是技术能力。
