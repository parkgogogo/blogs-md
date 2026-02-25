URL: https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/#atom-everything

# Linear walkthroughs / 线性代码导览

Sometimes it's useful to have a coding agent give you a structured walkthrough of a codebase.

有时让编程助手为你提供结构化的代码库导览是非常有用的。

Maybe it's existing code you need to get up to speed on, maybe it's your own code that you've forgotten the details of, or maybe you vibe coded the whole thing and need to understand how it actually works.

可能是你需要快速上手的现有代码，可能是你自己写的但已忘记细节的代码，也可能是你通过氛围编程（vibe coding）整个写出来的东西，现在需要理解它实际是如何工作的。

Frontier models with the right agent harness can construct a detailed walkthrough to help you understand how code works.

配备了合适代理框架的前沿模型能够构建详细的导览，帮助你理解代码的工作原理。

## An example using Showboat and Present / 使用 Showboat 和 Present 的示例

I recently vibe coded a SwiftUI slide presentation app on my Mac using Claude Code and Opus 4.6.

我最近使用 Claude Code 和 Opus 4.6 在我的 Mac 上通过氛围编程写了一个 SwiftUI 幻灯片演示应用。

I was speaking about the advances in frontier models between November 2025 and February 2026, and I like to include at least one gimmick in my talks (a STAR moment - Something They'll Always Remember). In this case I decided the gimmick would be revealing at the end of the presentation that the slide mechanism itself was an example of what vibe coding could do.

我当时正在演讲，主题是 2025 年 11 月到 2026 年 2 月之间前沿模型的进展，我喜欢在我的演讲中至少包含一个小噱头（一个 STAR 时刻——让他们永远记住的东西）。在这个例子中，我决定这个噱头是在演讲结束时揭晓：幻灯片机制本身就是氛围编程能力的一个示例。

I released the code to GitHub and then realized I didn't know anything about how it actually worked - I had prompted the whole thing into existence (partial transcript here) without paying any attention to the code it was writing.

我将代码发布到了 GitHub，然后意识到我对它实际如何工作一无所知——我通过提示词让整个应用凭空出现（部分对话记录在这里），完全没有关注它写的代码。

So I fired up a new instance of Claude Code for web, pointed it at my repo and prompted:

于是我启动了一个全新的 Claude Code for Web 实例，指向我的代码库，并输入了提示词：

> Read the source and then plan a linear walkthrough of the code that explains how it all works in detail
> Then run "uvx showboat --help" to learn showboat - use showboat to create a walkthrough.md file in the repo and build the walkthrough in there, using showboat note for commentary and showboat exec plus sed or grep or cat or whatever you need to include snippets of code you are talking about

> 阅读源代码，然后规划一个线性的代码导览，详细解释整个代码是如何工作的
> 然后运行 "uvx showboat --help" 来了解 showboat —— 使用 showboat 在代码库中创建一个 walkthrough.md 文件，并在其中构建导览，使用 showboat note 来添加注释，使用 showboat exec 配合 sed、grep、cat 或任何你需要的工具来包含你正在讨论的代码片段

Showboat is a tool I built to help coding agents write documents that demonstrate their work. You can see the showboat --help output here, which is designed to give the model everything it needs to know in order to use the tool.

Showboat 是我构建的一个工具，用于帮助编程助手编写展示其工作的文档。你可以在这里看到 showboat --help 的输出，它的设计目的是为模型提供使用这个工具所需的全部信息。

The `showboat note` command adds Markdown to the document. The `showboat exec` command accepts a shell command, executes it and then adds both the command and its output to the document.

`showboat note` 命令向文档添加 Markdown 内容。`showboat exec` 命令接受一个 shell 命令，执行它，然后将命令及其输出都添加到文档中。

By telling it to use "sed or grep or cat or whatever you need to include snippets of code you are talking about" I ensured that Claude Code would not manually copy snippets of code into the document, since that could introduce a risk of hallucinations or mistakes.

通过告诉它使用 "sed 或 grep 或 cat 或任何你需要的东西来包含你正在讨论的代码片段"，我确保 Claude Code 不会手动复制代码片段到文档中，因为那样可能会引入幻觉或错误的风险。

This worked extremely well. Here's the document Claude Code created with Showboat, which talks through all six .swift files in detail and provides a clear and actionable explanation about how the code works.

这效果非常好。这是 Claude Code 使用 Showboat 创建的文档，它详细讲解了全部六个 .swift 文件，并提供了关于代码如何工作的清晰且可操作的解释。

I learned a great deal about how SwiftUI apps are structured and absorbed some solid details about the Swift language itself just from reading this document.

仅通过阅读这个文档，我就学到了大量关于 SwiftUI 应用结构的知识，并吸收了一些关于 Swift 语言本身的扎实细节。

If you are concerned that LLMs might reduce the speed at which you learn new skills I strongly recommend adopting patterns like this one. Even a ~40 minute vibe coded toy project can become an opportunity to explore new ecosystems and pick up some interesting new tricks.

如果你担心大语言模型可能会降低你学习新技能的速度，我强烈建议采用像这样的模式。即使是一个花了大约 40 分钟通过氛围编程完成的小玩具项目，也可以成为探索新生态系统和学到一些有趣新技巧的机会。

---

## 批判性思考评论 / Critical Thinking Commentary

### 关于"线性导览"模式的深层价值

Simon Willison 提出的"线性导览"模式揭示了一个重要但常被忽视的 AI 编程痛点：我们过于关注代码生成，却忽略了代码理解。当 AI 可以快速产出数百行代码时，人类开发者面临的核心问题不再是"如何写出代码"，而是"如何理解已经存在的代码"。

这一模式的核心洞察在于：将代码解释的任务委托给 AI 本身，形成一个人机协同的学习闭环。Showboat 工具的设计尤为精妙——它通过强制执行"命令执行+输出捕获"的工作流，从根本上消除了 AI 在手动复制代码时可能产生的幻觉问题。

### 对学习影响的再思考

Willison 在文末提到的一个观点值得深思：LLM 不会降低学习速度，反而可以通过这种方式加速学习。这一论断具有一定的合理性，但也需要辩证看待。

积极方面，线性导览确实将"阅读代码"这一原本枯燥且耗时的工作转化为结构化、可导航的学习材料。开发者可以在较短时间内掌握项目全貌，而不必在文件间来回跳转、自行梳理逻辑。

然而，潜在的风险在于：如果开发者过度依赖 AI 生成的导览，可能会形成一种"快餐式"的学习习惯——追求快速理解而跳过深度思考。真正的编程能力培养仍需要亲手调试、修改代码，在错误中学习。

### 对工具设计的启示

Showboat 的设计体现了面向 AI 的工具设计新范式：
1. **确定性输入输出**：使用 exec 命令而非自由文本，确保代码片段的准确性
2. **渐进式构建**：支持 note 和 exec 组合使用，让 AI 能够边分析边记录
3. **机器可读的帮助文档**：--help 输出专门针对模型优化，而非人类用户

这种"AI 优先"的工具设计理念可能会成为未来开发工具的重要方向。

### 实践建议

对于希望采用此模式的开发者：
1. **明确导览目标**：是用于新人上手、代码审查还是知识沉淀？
2. **迭代优化**：首次生成的导览可能不够理想，可以通过后续提示逐步完善
3. **结合人工审核**：AI 导览虽高效，但关键决策点仍需人工验证

总体而言，线性导览模式代表了 AI 辅助编程向更深层次演进的一个信号——从单纯的代码生成，转向知识管理与团队协作的智能化。
