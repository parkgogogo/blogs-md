URL: https://pi.dev

# Pi – a minimal terminal coding harness
# Pi – 一个极简的终端编程工具

---

There are many coding agents, but this one is mine.

编码助手有很多，但这个是属于我的。

---

## About / 关于

### Why pi? / 为什么选择 Pi？

Pi is a minimal terminal coding harness. Adapt pi to your workflows, not the other way around. Extend it with TypeScript [extensions](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#extensions), [skills](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#skills), [prompt templates](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#prompt-templates), and [themes](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#themes). Bundle them as [pi packages](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#pi-packages) and share via npm or git.

Pi 是一个极简的终端编程工具。让 Pi 适应你的工作流程，而不是反过来。你可以用 TypeScript [扩展](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#extensions)、[技能](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#skills)、[提示模板](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#prompt-templates)和[主题](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#themes)来扩展它。将它们打包成 [Pi 包](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#pi-packages)，通过 npm 或 git 分享。

Pi ships with powerful defaults but skips features like sub-agents and plan mode. Ask pi to build what you want, or install a package that does it your way.

Pi 自带强大的默认配置，但跳过了子代理和计划模式等功能。让 Pi 帮你构建你想要的东西，或者安装一个按你方式工作的包。

Four modes: interactive, print/JSON, [RPC, and SDK](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#programmatic-usage). See [clawdbot](https://github.com/clawdbot/clawdbot) for a real-world integration.

四种模式：交互式、打印/JSON、[RPC 和 SDK](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#programmatic-usage)。查看 [clawdbot](https://github.com/clawdbot/clawdbot) 了解真实世界的集成案例。

---

## Providers & Models / 提供商与模型

### 15+ providers, hundreds of models / 15+ 提供商，数百个模型

Anthropic, OpenAI, Google, Azure, Bedrock, Mistral, Groq, Cerebras, xAI, Hugging Face, Kimi For Coding, MiniMax, OpenRouter, Ollama, and more. Authenticate via API keys or OAuth.

Anthropic、OpenAI、Google、Azure、Bedrock、Mistral、Groq、Cerebras、xAI、Hugging Face、Kimi For Coding、MiniMax、OpenRouter、Ollama 等。通过 API 密钥或 OAuth 进行认证。

Switch models mid-session with `/model` or `Ctrl+L`. Cycle through your favorites with `Ctrl+P`.

在会话中途使用 `/model` 或 `Ctrl+L` 切换模型。使用 `Ctrl+P` 循环切换你收藏的模型。

Add custom providers and models via [models.json](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/docs/models.md) or [extensions](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/docs/custom-provider.md).

通过 [models.json](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/docs/models.md) 或[扩展](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/docs/custom-provider.md)添加自定义提供商和模型。

---

## Sessions / 会话

### Tree-structured, shareable history / 树状结构，可分享的历史

Sessions are stored as trees. Use `/tree` to navigate to any previous point and continue from there. All branches live in a single file. Filter by message type, label entries as bookmarks.

会话以树状结构存储。使用 `/tree` 导航到任何之前的节点并从那里继续。所有分支都保存在一个文件中。按消息类型过滤，将条目标记为书签。

Export to HTML with `/export`, or upload to a GitHub gist with `/share` and get a shareable URL that renders it.

使用 `/export` 导出为 HTML，或使用 `/share` 上传到 GitHub gist 并获得一个可分享的渲染链接。

---

## Context / 上下文

### Context engineering / 上下文工程

Pi's [minimal system prompt](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/src/core/system-prompt.ts) and extensibility let you do actual context engineering. Control what goes into the context窗口 and how it's managed.

Pi 的[极简系统提示](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/src/core/system-prompt.ts)和可扩展性让你能够进行真正的上下文工程。控制什么内容进入上下文窗口以及如何管理它。

**AGENTS.md:** Project instructions loaded at startup from `~/.pi/agent/`, parent directories, and the current directory.

**AGENTS.md:** 项目指令在启动时从 `~/.pi/agent/`、父目录和当前目录加载。

**SYSTEM.md:** Replace or append to the default system prompt per-project.

**SYSTEM.md:** 按项目替换或追加到默认系统提示。

**Compaction:** Auto-summarizes older messages when approaching the context limit. Fully customizable via [extensions](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/examples/extensions/custom-compaction.ts): implement topic-based compaction, code-aware summaries, or use different summarization models.

**压缩：** 当接近上下文限制时自动总结较旧的消息。通过[扩展](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/examples/extensions/custom-compaction.ts)完全可自定义：实现基于主题的压缩、代码感知摘要，或使用不同的摘要模型。

**Skills:** Capability packages with instructions and tools, loaded on-demand. Progressive disclosure without busting the prompt cache. See [skills](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#skills).

**技能：** 带有指令和工具的能力包，按需加载。渐进式披露而不会破坏提示缓存。查看[技能](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#skills)。

**Prompt templates:** Reusable prompts as Markdown files. Type `/name` to expand. See [prompt templates](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#prompt-templates).

**提示模板：** 可重用的 Markdown 文件形式的提示。输入 `/name` 展开。查看[提示模板](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#prompt-templates)。

**Dynamic context:** [Extensions](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#extensions) can inject messages before each turn, filter the message history, implement RAG, or build long-term memory.

**动态上下文：** [扩展](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#extensions)可以在每次回合前注入消息、过滤消息历史、实现 RAG 或构建长期记忆。

---

## Queuing / 队列

### Steer or follow up / 引导或跟进

Submit messages while the agent works. `Enter` sends a steering message (delivered after current tool, interrupts remaining tools). `Alt+Enter` sends a follow-up (waits until the agent finishes).

在代理工作时提交消息。`Enter` 发送引导消息（在当前工具后传递，中断剩余工具）。`Alt+Enter` 发送跟进消息（等待代理完成）。

---

## Extensions / 扩展

### Primitives, not features / 原语，而非功能

Features that other agents bake in, you can build yourself. Extensions are TypeScript modules with access to tools, commands, keyboard shortcuts, events, and the full TUI.

其他代理内置的功能，你可以自己构建。扩展是具有工具、命令、键盘快捷键、事件和完整 TUI 访问权限的 TypeScript 模块。

[Sub-agents](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/examples/extensions/subagent/), [plan mode](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/examples/extensions/plan-mode/), [permission gates](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/examples/extensions/permission-gate.ts), [path protection](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/examples/extensions/protected-paths.ts), [SSH execution](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/examples/extensions/ssh.ts), [sandboxing](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/examples/extensions/sandbox/), MCP integration, custom editors, status bars, overlays. [Yes, Doom runs.](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/examples/extensions/doom-overlay/)

[子代理](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/examples/extensions/subagent/)、[计划模式](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/examples/extensions/plan-mode/)、[权限门](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/examples/extensions/permission-gate.ts)、[路径保护](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/examples/extensions/protected-paths.ts)、[SSH 执行](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/examples/extensions/ssh.ts)、[沙箱](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/examples/extensions/sandbox/)、MCP 集成、自定义编辑器、状态栏、覆盖层。[是的，能运行 Doom。](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/examples/extensions/doom-overlay/)

Don't want to build it? Ask pi to build it for you. Or install a [package](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#pi-packages) that does it your way. See the [50+ examples](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/examples/extensions/).

不想自己构建？让 Pi 帮你构建。或者安装一个按你方式工作的[包](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#pi-packages)。查看[50+ 示例](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/examples/extensions/)。

---

## Packages / 包

### Install and share / 安装与分享

Bundle extensions, skills, prompts, and themes as packages. Install from npm or git:

将扩展、技能、提示和主题打包成包。从 npm 或 git 安装：

```
$ pi install npm:@foo/pi-tools
$ pi install git:github.com/badlogic/pi-doom
```

Pin versions with `@1.2.3` or `@tag`. Update all with `pi update`, list with `pi list`, configure with `pi config`.

使用 `@1.2.3` 或 `@tag` 固定版本。使用 `pi update` 更新全部，使用 `pi list` 列出，使用 `pi config` 配置。

Test without installing using `pi -e git:github.com/user/repo`.

使用 `pi -e git:github.com/user/repo` 在不安装的情况下测试。

Find packages on [npm](https://www.npmjs.com/search?q=keywords%3Api-package) or [Discord](https://discord.com/channels/1456806362351669492/1457744485428629628). Share yours with the `pi-package` keyword.

在 [npm](https://www.npmjs.com/search?q=keywords%3Api-package) 或 [Discord](https://discord.com/channels/1456806362351669492/1457744485428629628) 上查找包。使用 `pi-package` 关键词分享你的包。

---

## Integration / 集成

### Four modes / 四种模式

**Interactive:** The full TUI experience.

**交互式：** 完整的 TUI 体验。

**Print/JSON:** `pi -p "query"` for scripts, `--mode json` for event streams.

**打印/JSON：** 脚本使用 `pi -p "query"`，事件流使用 `--mode json`。

**RPC:** JSON protocol over stdin/stdout for non-Node integrations. See [docs/rpc.md](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/docs/rpc.md).

**RPC：** 通过 stdin/stdout 的 JSON 协议，用于非 Node 集成。查看 [docs/rpc.md](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/docs/rpc.md)。

**SDK:** Embed pi in your apps. See [clawdbot](https://github.com/clawdbot/clawdbot) for a real-world example.

**SDK：** 在你的应用中嵌入 Pi。查看 [clawdbot](https://github.com/clawdbot/clawdbot) 了解真实案例。

---

## Philosophy / 理念

### What we didn't build / 我们没有构建什么

Pi is aggressively extensible so it doesn't have to dictate your workflow. Features that other tools bake in can be built with [extensions](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#extensions), [skills](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#skills), or installed from third-party [pi packages](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#pi-packages). This keeps the core minimal while letting you shape pi to fit how you work.

Pi 被设计为高度可扩展，因此它不必规定你的工作流程。其他工具内置的功能可以通过[扩展](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#extensions)、[技能](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#skills)构建，或从第三方 [Pi 包](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#pi-packages)安装。这使得核心保持精简，同时让你可以塑造 Pi 以适应你的工作方式。

**No MCP.** Build CLI tools with READMEs (see [Skills](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#skills)), or build an extension that adds MCP support. [Why?](https://mariozechner.at/posts/2025-11-02-what-if-you-dont-need-mcp/)

**没有 MCP。** 用 README 构建 CLI 工具（查看[技能](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#skills)），或构建添加 MCP 支持的扩展。[为什么？](https://mariozechner.at/posts/2025-11-02-what-if-you-dont-need-mcp/)

**No sub-agents.** There's many ways to do this. Spawn pi instances via tmux, or build your own with [extensions](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#extensions), or install a package that does it your way.

**没有子代理。** 有很多方法可以实现这一点。通过 tmux 生成 Pi 实例，或用[扩展](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#extensions)构建你自己的，或安装一个按你方式工作的包。

**No permission popups.** Run in a container, or build your own confirmation flow with [extensions](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#extensions) inline with your environment and security requirements.

**没有权限弹窗。** 在容器中运行，或用[扩展](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#extensions)构建符合你的环境和安全要求的确认流程。

**No plan mode.** Write plans to files, or build it with [extensions](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#extensions), or install a package.

**没有计划模式。** 将计划写入文件，或用[扩展](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#extensions)构建，或安装一个包。

**No built-in to-dos.** Use a TODO.md file, or build your own with [extensions](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#extensions).

**没有内置待办事项。** 使用 TODO.md 文件，或用[扩展](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#extensions)构建你自己的。

**No background bash.** Use tmux. Full observability, direct interaction.

**没有后台 bash。** 使用 tmux。完全可观察性，直接交互。

Read the [blog post](https://mariozechner.at/posts/2025-11-30-pi-coding-agent/) for the full rationale.

阅读[博客文章](https://mariozechner.at/posts/2025-11-30-pi-coding-agent/)了解完整的理念。

---

## Community / 社区

### Get involved / 参与其中

**Issues:** [GitHub](https://github.com/badlogic/pi-mono/issues) for bugs and features.

**Issues：** [GitHub](https://github.com/badlogic/pi-mono/issues) 用于报告 bug 和功能请求。

**Discord:** [Community server](https://discord.com/invite/nKXTsAcmbT) for discussion and sharing.

**Discord：** [社区服务器](https://discord.com/invite/nKXTsAcmbT) 用于讨论和分享。

**Docs:** [README](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#readme) and [docs/](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/docs) for everything else.

**文档：** [README](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#readme) 和 [docs/](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/docs) 用于其他所有内容。

---

MIT License • [Mario Zechner](https://mariozechner.at) & [contributors](https://github.com/badlogic/pi-mono/graphs/contributors)

pi.dev domain graciously donated by [exe.dev](https://exe.dev) ❤️

---

## 批判性思考与评论

Pi 代表了一种与当前 AI 编码助手趋势截然不同的设计理念。以下是一些值得思考的要点：

### 1. "Unix 哲学" 的回归

Pi 的核心理念是"做一件事，并做好它"。与 Cursor、Windsurf 等一体化 IDE 不同，Pi 选择保持核心极简，将高级功能交给扩展生态系统。这种设计哲学让人想起 Unix 工具链——小而美、可组合、专注于单一职责。

### 2. 对 MCP 的质疑

作者明确反对 MCP（Model Context Protocol），认为简单的 CLI 工具配合 README 文档足以实现类似功能。这一观点颇具争议性，因为 MCP 正被 Anthropic 等公司大力推广。Pi 的立场是：与其为每个工具学习新的协议，不如直接调用已经熟悉的命令行工具。

### 3. 用户自主权的权衡

Pi 将许多"应该内置"的功能（如子代理、计划模式、权限弹窗）交给用户自行实现。这种设计带来了灵活性，但也提高了入门门槛。对于追求开箱即用的用户，Pi 可能显得过于"裸机"；但对于喜欢定制化的开发者，这正是其魅力所在。

### 4. 终端优先的策略

在 GUI 主导的 AI 助手市场中，Pi 选择深耕终端。这一决策既是优势也是局限：它天然适合已经习惯命令行的开发者，但可能难以吸引更广泛的非技术用户群体。

### 5. 生态系统的可持续性

Pi 的成功很大程度上取决于其扩展生态的繁荣。虽然 npm 和 git 提供了便利的分发渠道，但如何激励开发者持续维护高质量的扩展包，仍是任何开源项目面临的长期挑战。

总体而言，Pi 是一款面向"黑客"的工具——它不迎合所有人，但对那些愿意投入时间构建自己理想工作流的开发者来说，它提供了近乎无限的定制空间。这种"宁可给用户能力，也不替用户做决定"的态度，在当前 AI 工具趋于同质化的背景下，显得尤为珍贵。
