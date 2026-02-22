URL: https://boristane.com/blog/how-i-use-claude-code/

---

I've been using [Claude Code](https://docs.anthropic.com/en/docs/claude-code) as my primary development tool for about 9 months now, and the workflow I've developed looks nothing like how most people use AI coding tools. Most developers input a prompt, sometimes use planning mode, fix errors, and repeat. Those more hooked to the web cobble together ralph loops, mcp, gas town (remember those?), and so on. Both result in a mess that falls over for any non-trivial task.

我已经使用 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 作为我的主要开发工具大约 9 个月了，而我所形成的工作流程与大多数人使用 AI 编程工具的方式截然不同。大多数开发者输入一个提示词，有时使用规划模式，修复错误，然后重复。那些更沉迷于网络的人则在拼凑 ralph 循环、mcp、gas town（还记得那些吗？）等等。这两种情况的结果都是一团糟，对于任何非平凡的任务都完全崩溃。

The workflow I'm about to describe has one core principle: Never let Claude write code until you've reviewed and approved a written plan. This separation of planning from execution is the single most important thing I do. It prevents wasted effort, keeps me in control of architectural decisions, and produces dramatically better results than jumping straight to code, while minimizing token usage.

我要描述的这个工作流程有一个核心原则：在审阅并批准一份书面计划之前，绝不让 Claude 编写代码。这种将规划与执行分离的做法是我所做的最重要的事情。它能防止浪费精力，让我掌控架构决策，并且在最小化 token 使用量的同时，产生比直接跳到代码阶段好得多的结果。

```
flowchart LR
 R[Research] --> P[Plan]
 P --> A[Annotate]
 A -->|repeat 1-6x| A
 A --> T[Todo List]
 T --> I[Implement]
 I --> F[Feedback & Iterate]
```

## Phase 1: Research
## 第一阶段：研究

Every meaningful task begins with a deep read instruction. Before Claude does anything else, I ask it to thoroughly understand the relevant parts of the codebase. And I always ask for the research to be written into a persistent markdown file, never just a verbal summary in chat.

每一个有意义的任务都始于一个深度阅读指令。在 Claude 做其他任何事情之前，我要求它彻底理解代码库的相关部分。而且我总是要求将研究结果写入一个持久的 markdown 文件，而绝不仅仅是聊天中的口头总结。

```
Deep read this folder, deeply understand how it works, what it does, and all the intricacies. Once you're done, write a detailed report of your learning and findings in research.md
```

```
深度阅读这个文件夹，深入理解它是如何工作的、它做什么以及所有的细节。完成之后，在 research.md 中写下你的学习和发现的详细报告
```

```
Research deeply into the notification system, understand all the intricacies, and write a detailed research.md document with everything about how notifications work
```

```
深入研究通知系统，理解其所有复杂细节，并撰写一份详细的 research.md 文档，包含关于通知如何工作的所有信息
```

```
Carefully examine the task scheduling flow, deeply understand it and look for bugs. There is definitely a bug in the system because it sometimes runs tasks that should have been cancelled. Keep researching this flow until you find all the bugs, don't stop until you've found all the bugs. Once done, write a detailed report in research.md
```

```
仔细检查任务调度流程，深入理解它并寻找潜在的 bug。系统中肯定存在 bug，因为它有时会运行本应被取消的任务。继续研究这个流程直到找到所有 bug，不要停止，直到找到所有 bug。完成后，在 research.md 中撰写一份详细的报告
```

Note the phrasing: "deeply", "in detail", "intricacies", "carefully examine everything". This is not filler. Without these words, Claude skims. It reads a file, sees what a function does at the signature level, and moves on. You need to signal explicitly that surface-level reading is unacceptable.

注意措辞："深度地"、"详细地"、"复杂细节"、"仔细检查所有内容"。这不仅仅是空话。如果没有这些词，Claude 就会略读。它会读一个文件，看看函数在签名级别上做了什么，然后就继续。你需要明确表明，表面层次的阅读是不可接受的。

The written artifact (research.md) is crucial. This is not about making Claude do homework. It is my review surface. I can read it, verify that Claude actually understands the system, and correct misconceptions before any planning happens. If the research is wrong, the plan will be wrong, and the implementation will be wrong. Garbage in, garbage out.

书面成果（research.md）至关重要。这并不是让 Claude 做作业的问题。它是我的审阅面。我可以阅读它，验证 Claude 是否真正理解了系统，并在任何规划发生之前纠正误解。如果研究是错误的，计划就会错误，实现也会错误。垃圾进，垃圾出。

This is the most expensive failure mode in AI-assisted coding, and it is not wrong syntax or bad logic. It is implementations that work in isolation but break the surrounding system. A function that ignores an existing caching layer. A migration that doesn't account for ORM conventions. An API endpoint that duplicates logic that exists elsewhere. The research phase prevents all of these.

这是 AI 辅助编码中最昂贵的失败模式，它不是错误的语法或糟糕的逻辑。而是那些在孤立环境中工作正常但会破坏周围系统的实现。一个忽视现有缓存层的函数。一个未考虑 ORM 约定的迁移。一个重复了别处已有逻辑的 API 端点。研究阶段可以防止所有这些。

## Phase 2: Planning
## 第二阶段：规划

Once I've reviewed the research, I ask for a detailed implementation plan in a separate markdown file.

一旦我审阅完研究，我就会要求在一个单独的 markdown 文件中提供详细的实现计划。

```
I want to build a new feature <name and description> that extends the system to achieve <business outcome>. Write a detailed plan.md document outlining how to achieve this. Include code snippets
```

```
我想构建一个新功能 <名称和描述>，将系统扩展到实现 <业务成果>。撰写一份详细的 plan.md 文档，概述如何实现这一点。包含代码片段
```

```
The listing endpoint should support cursor-based pagination instead of offset pagination. Write a detailed plan.md on how to implement this. Read the source files before making recommendations, base the plan on the actual codebase
```

```
列表端点应该支持基于游标的分页，而不是偏移分页。撰写一份详细的 plan.md 说明如何实现这一点。在提出建议之前先阅读源文件，基于实际的代码库来制定计划
```

The generated plan always includes a detailed explanation of the approach, code snippets showing the actual changes, file paths that will be modified, and considerations and trade-offs.

生成的计划总是包括方法的详细解释、显示实际更改的代码片段、将要修改的文件路径，以及考虑和权衡。

I use my own .md plan files instead of Claude Code's built-in planning mode. The built-in planning mode is bad. My markdown files give me complete control. I can edit them in my editor, add inline comments, and they persist as real artifacts in the project.

我使用我自己的 .md 计划文件，而不是 Claude Code 内置的规划模式。内置的规划模式很糟糕。我的 markdown 文件给了我完全的控制权。我可以在我的编辑器中编辑它，添加内联注释，并且它作为项目中的真实成果持续存在。

One trick I use constantly: for well-contained features that I've seen good implementations of in open source repos, I share that code as a reference alongside the plan request. If I want to add sortable IDs, I'll paste code from a project that implements ID generation well and say "this is how they implement sortable IDs, write a plan.md explaining how we adopt a similar approach." Claude performs dramatically better when it has concrete reference implementations to work from than when designing from scratch.

我不断使用的一个技巧是：对于那些我已经在开源仓库中看到过良好实现的、封装良好的功能，我会分享那段代码作为参考，同时提出计划请求。如果我想添加可排序 ID，我会粘贴一个项目做得很好的 ID 生成代码，然后说"这就是他们如何实现可排序 ID 的，撰写一份 plan.md 解释我们如何采用类似的方法。"当 Claude 有具体的参考实现可以参照时，它的表现比从头设计要好得多。

But the plan document itself is not the interesting part. The interesting part is what happens next.

但计划文档本身并不是有趣的部分。有趣的是接下来发生的事。

## The Annotation Loop
## 注释循环

This is the most unique part of my workflow, and where I add the most value.

这是我工作流程中最独特的部分，也是我增加最多价值的地方。

```
flowchart TD
 W[Claude writes plan.md] --> R[I review in my editor]
 R --> N[I add inline comments]
 N --> S[Send Claude back to the document]
 S --> U[Claude updates the plan]
 U --> D{Satisfied?}
 D -->|No| R
 D -->|Yes| T[Ask for todo list]
```

After Claude writes a plan, I open it in my editor and add inline comments directly to the document. These comments correct assumptions, reject approaches, add constraints, or provide domain knowledge that Claude doesn't have.

在 Claude 撰写计划后，我在我的编辑器中打开它，直接在文档中添加内联注释。这些注释纠正假设、拒绝方法、添加约束，或提供 Claude 不具备的领域知识。

The comments vary dramatically in length. Sometimes a comment is just two words: "not optional" next to a parameter Claude marked as optional. Other times it is a paragraph explaining a business constraint or pasting a code snippet showing the data format I expect.

注释的长度差异很大。有时一个注释只有两个字：在 Claude 标记为可选的参数旁边写上"不是可选的"。其他时候则是一段解释业务约束或粘贴代码片段展示我期望的数据格式的段落。

Some real examples of comments I might add:

我可能会添加的一些真实注释示例：

- "Use drizzle:generate for migrations, not raw SQL" — domain knowledge Claude doesn't have

- "使用 drizzle:generate 进行迁移，而不是原始 SQL" —— Claude 不具备的领域知识

- "No — this should be PATCH, not PUT" — correcting a wrong assumption

- "不 —— 这应该是 PATCH，不是 PUT" —— 纠正错误的假设

- "Remove this section entirely, we don't need caching here" — rejecting a proposed approach

- "完全删除这一节，我们这里不需要缓存" —— 拒绝提议的方法

- "The queue consumer already handles retries, so this retry logic is redundant. Delete it and just let it fail" — explaining why something should change

- "队列消费者已经处理了重试，所以这个重试逻辑是多余的。删除它，直接让它失败" —— 解释为什么某事应该改变

- "This is wrong, the visibility field needs to be on the list itself, not on individual items. When the list is public, all items are public. Restructure the schema section accordingly" — redirecting an entire section of the plan

- "这是错的，可见性字段需要放在列表本身上，而不是单个项目上。当列表是公开时，所有项目都是公开的。相应地重新构建模式部分" —— 重定向计划的整个部分

Then I send Claude back to the document:

然后我让 Claude 回到文档：

```
I've added some comments to the document, address all the comments and update the document accordingly. Don't implement yet
```

```
我在文档中添加了一些注释，处理所有注释并相应地更新文档。暂时不要实现
```

This loop repeats between 1 and 6 times. The explicit "Don't implement yet" guard is crucial. Without it, Claude jumps to code the moment it thinks the plan is good enough. It is not good enough until I say it is.

这个循环重复 1 到 6 次。明确的"暂时不要实现"保护是至关重要的。没有它，Claude 一旦认为计划足够好就会跳到代码阶段。除非我说它足够好，否则它还不够好。

### Why this works so well
### 为什么这个方法如此有效

The markdown file acts as shared mutable state between me and Claude. I can think at my own pace, point precisely to where things are wrong, and re-engage without losing context. I don't have to explain everything in chat messages. I just point to the exact spot in the document where the problem is and write my correction right there.

markdown 文件充当我和 Claude 之间的共享可变状态。我可以按照自己的节奏思考，精确地指出哪里出了问题，并在不丢失上下文的情况下重新参与。我不需要在聊天消息中解释所有内容。我只需指向文档中问题所在的确切位置，就在那里写下我的更正。

This is fundamentally different from trying to steer an implementation through chat messages. The plan is a structured, complete specification that I can review comprehensively. Chat conversations are things I have to scroll through to reconstruct what was decided. The plan wins every time.

这与试图通过聊天消息来引导实现是根本不同的。计划是一个结构化的、完整的规范，我可以全面审阅。聊天对话是我必须滚动浏览才能重建决策的东西。计划每次都胜过聊天。

Three rounds of "I've added comments, update the plan" can transform a generic implementation plan into one that fits perfectly into the existing system. Claude excels at understanding code, proposing solutions, and writing implementations. But it doesn't know my product priorities, my users' pain points, or the engineering tradeoffs I'm willing to make. The annotation loop is how I inject that judgment.

三轮"我添加了注释，更新计划"可以将一个通用的实现计划转变为一个完美融入现有系统的计划。Claude 在理解代码、提出解决方案和编写实现方面表现出色。但它不知道我的产品优先级、我的用户的痛点，或者我愿意做出的工程权衡。注释循环就是我如何注入这些判断的方式。

### The Todo List
### 待办事项列表

Before starting implementation, I always ask for a granular task breakdown:

在开始实现之前，我总是要求一个细粒度的任务分解：

```
Add a detailed todo list to the plan with all the phases and individual tasks required to complete the plan — don't implement yet
```

```
在计划中添加一个详细的待办事项列表，包含完成计划所需的所有阶段和单个任务 —— 暂时不要实现
```

This creates a checklist that serves as a progress tracker during implementation. Claude marks items as complete as it finishes them, so I can check the plan at any point and know exactly where things stand. Especially valuable in sessions that run for hours.

这创建了一个清单，在实施过程中作为进度跟踪器。Claude 在完成时会将项目标记为已完成，所以我可以随时查看计划并准确了解进展。在运行数小时的会话中尤其有价值。

## Phase 3: Implementation
## 第三阶段：实现

When the plan is ready, I issue the implementation command. I've refined this into a standard prompt I can reuse across sessions:

当计划准备好后，我发出实现命令。我已经将其精炼成一个可以在各个会话中重复使用的标准提示：

```
Implement everything. When you complete a task or phase, mark it as done in the plan document. Don't stop until all tasks and phases are complete. Don't add unnecessary comments or JSDoc, don't use any or unknown types. Continuously run type checking to ensure you're not introducing new issues
```

```
全部实现。当你完成一个任务或阶段时，在计划文档中将其标记为已完成。不要停止，直到所有任务和阶段都完成。不要添加不必要的注释或 JSDoc，不要使用 any 或 unknown 类型。持续运行类型检查以确保你没有引入新问题
```

This single prompt encodes everything that matters:

这个单一的提示编码了所有重要的内容：

- "Implement everything": Complete everything in the plan, don't cherry-pick

- "全部实现"：完成计划中的所有内容，不要挑三拣四

- "mark it as done in the plan document": The plan is the source of truth for progress

- "在计划文档中将其标记为已完成"：计划是进度的真实来源

- "Don't stop until all tasks and phases are complete": Don't stop halfway waiting for confirmation

- "不要停止，直到所有任务和阶段都完成"：不要中途停下来等待确认

- "Don't add unnecessary comments or JSDoc": Keep the code clean

- "不要添加不必要的注释或 JSDoc"：保持代码整洁

- "don't use any or unknown types": Maintain strict typing

- "不要使用 any 或 unknown 类型"：保持严格类型

- "Continuously run type checking": Catch issues early, not at the end

- "持续运行类型检查"：尽早发现问题，而不是最后

I use this exact wording in almost every implementation session (with minor variations). When I say "Implement everything", every decision has already been made and verified. Implementation becomes mechanical rather than creative. This is deliberate. I want implementation to be boring. The creative work happens in the annotation loop. Once the plan is right, execution should be straightforward.

我在几乎每个实现会话中都使用这个确切的措辞（有轻微的变化）。当我说"全部实现"时，每个决定都已经做出并验证过了。实现变得机械而不是创造性。这是故意的。我希望实现是乏味的。创造性工作发生在注释循环中。一旦计划正确，执行就应该是直接的。

Without the planning phase, what usually happens is that Claude makes a reasonable but wrong assumption early on, builds on it for 15 minutes, and then I have to unwind a chain of changes. The "Don't implement yet" guard eliminates this entirely.

如果没有规划阶段，通常会发生的情况是 Claude 在早期就做出了一个合理但错误的假设，在此基础上构建了 15 分钟，然后我不得不解开一连串的更改。"暂时不要实现"的保护完全消除了这个问题。

## Feedback During Implementation
## 实现过程中的反馈

Once Claude is executing the plan, my role shifts from architect to supervisor. My prompts become much shorter.

一旦 Claude 在执行计划，我的角色就从架构师转变为监督者。我的提示变得简洁得多。

```
flowchart LR
 I[Claude implements] --> R[I review / test]
 R --> C{Correct?}
 C -->|No| F[Concise correction]
 F --> I
 C -->|Yes| N{More tasks?}
 N -->|Yes| I
 N -->|No| D[Done]
```

Planning comments might be a paragraph, but implementation corrections are often just a sentence:

规划注释可能是一段话，但实现更正往往只是一个句子：

- "You didn't implement the deduplicateByTitle function."
- "你没有实现 deduplicateByTitle 函数。"

- "You built the settings page in the main app, but it should be in the admin app, move it."

- "你把设置页面建在了主应用中，但它应该在管理应用中，移动它。"

Claude has the full context of the plan and the ongoing session, so concise corrections are sufficient.

Claude 拥有计划的完整上下文和正在进行的会话，所以简洁的更正就足够了。

Frontend work is the most iterative part. I test in the browser and fire off rapid corrections:

前端工作是最具迭代性的部分。我在浏览器中测试并快速发出更正：

- "wider"

- "更宽"

- "still truncated"

- "还是被截断了"

- "2px gap"

- "有 2px 的间隙"

For visual issues, I sometimes attach screenshots. A screenshot of a misaligned table communicates the problem faster than describing it.

对于视觉问题，我有时会附加截图。一张表格未对齐的截图比描述问题更快地传达问题。

I also frequently reference existing code:

我也经常引用现有代码：

- "This table should look exactly like the user table, same headers, same pagination, same row density."

- "这个表格应该看起来完全像用户表格，相同的表头、相同的分页、相同的行密度。"

This is more precise than describing the design from scratch. Most features in a mature codebase are variations on existing patterns. A new settings page should look like existing settings pages. Pointing to reference code conveys all the implicit requirements without listing them. Claude usually reads the reference file before making the correction.

这比从头描述设计要精确得多。成熟代码库中的大多数功能都是现有模式的变化。一个新的设置页面应该看起来像现有的设置页面。指向参考代码传达了所有隐含的要求，而无需一一说明。Claude 通常会在做出更正之前阅读参考文件。

When something goes in the wrong direction, I don't try to patch it. I revert and rescope by dropping the git changes:

当某事走向错误的方向时，我不会试图修补它。我通过放弃 git 更改来恢复和重新确定范围：

- "I reverted everything. Now all I want is for the list view to be cleaner — nothing else."

- "我恢复了所有内容。现在我想要的只是让列表视图更简洁 —— 其他什么都不做。"

Rescoping after a revert almost always produces better results than trying to fix a bad approach incrementally.

在恢复后缩小范围几乎总是比试图逐步修复一个糟糕的方法产生更好的结果。

## Maintaining Dominance
## 保持主导地位

Even when I delegate execution to Claude, I never let it fully autonomously decide what to build. I do the vast majority of proactive steering in the plan.md document.

即使我将执行委托给 Claude，我也从不让它完全自主决定构建什么。我在 plan.md 文档中完成绝大部分的主动引导。

This matters because Claude sometimes proposes solutions that are technically correct but wrong for the project. Maybe the approach is over-engineered, or it changes a public API signature that other parts of the system depend on, or it picks a more complex option when a simpler one exists. I have context about the broader system, product direction, and engineering culture that Claude does not.

这很重要，因为 Claude 有时会提议技术上正确但对项目来说是错误的解决方案。也许这种方法过于工程化，或者它改变了系统其他部分依赖的公共 API 签名，或者它在有更简单的选择时选择了更复杂的选项。我拥有关于更广泛的系统、产品方向和工程文化的上下文，而 Claude 没有。

```
flowchart TD
 P[Claude proposes changes] --> E[I evaluate each item]
 E --> A[Accept as-is]
 E --> M[Modify approach]
 E --> S[Skip / Delete]
 E --> O[Override technical choice]
 A & M & S & O --> R[Refined implementation scope]
```

Picking from proposals: When Claude identifies multiple issues, I go through them one by one: "For the first one, just use Promise.all, don't overcomplicate it; for the third, extract to a separate function for readability; ignore the fourth and fifth, they're not worth the complexity." I make project-level decisions based on what I know matters right now.

从提议中挑选：当 Claude 识别多个问题时，我逐一处理："对于第一个，直接使用 Promise.all，不要搞得太复杂；对于第三个，提取到一个单独的函数以提高可读性；忽略第四和第五个，它们不值得这么复杂。"我根据对当下什么是重要的了解，做出项目级别的决策。

Cutting scope: When the plan includes nice-to-have features, I proactively cut them. "Remove the download feature from the plan, I don't want to implement this now." This prevents scope creep.

削减范围：当计划包含锦上添花的功能时，我主动砍掉它们。"从计划中删除下载功能，我现在不想实现这个。"这防止了范围蔓延。

Protecting existing interfaces: When I know something shouldn't change, I set hard constraints: "The signatures of these three functions should not change, callers should adapt, not the library."

保护现有接口：当我知道某事不应该改变时，我设置硬约束："这三个函数的签名不应该改变，调用者应该适应，而不是库。"

Overriding technical choices: Sometimes I have specific preferences that Claude wouldn't know: "Use this model instead of that" or "Use this library's built-in method instead of writing a custom one." Quick, direct overrides.

覆盖技术选择：有时我有 Claude 不会知道的特定偏好："使用这个模型而不是那个"或"使用这个库的内置方法而不是写一个自定义的。"快速、直接的覆盖。

Claude handles the mechanical execution while I make the judgment calls. The plan captures the big decisions upfront, and selective guidance handles the smaller decisions that arise during implementation.

Claude 处理机械执行，而我做出判断调用。计划预先捕获了重大决策，选择性指导处理实施过程中出现的较小决策。

## Single Long Sessions
## 单次长时间会话

I do research, planning, and implementation in single long sessions rather than spreading them across separate sessions. A session might start with a deep read of a folder, go through three rounds of plan annotations, then run the full implementation, all in one continuous conversation.

我在单次长时间会话中进行研究、规划和实现，而不是将它们分散到单独的会话中。一个会话可能从深度阅读一个文件夹开始，经过三轮计划注释，然后运行完整的实现，全部在一个连续的对话中完成。

I don't see the performance degradation people talk about after 50% context window. In fact, when I say "Implement everything", Claude has built up understanding throughout the entire session: reading files during research, refining its mental model during annotation loops, absorbing my domain knowledge corrections.

我没有看到在 50% 上下文窗口后大家谈论的性能下降。实际上，当我说"全部实现"时，Claude 已经在整个会话中建立了理解：在研究期间阅读文件，在注释循环中精炼其心智模型，吸收我的领域知识更正。

When the context window fills, Claude's automatic compression keeps enough context to continue. And the plan document, that persistent artifact, survives compression with full fidelity. I can point to it at any time.

当上下文窗口填满时，Claude 的自动压缩保持足够的上下文以继续。而计划文档，这个持久的成果，在压缩后以完整的保真度存活下来。我可以随时指向它。

## One-Sentence Summary of the Workflow
## 一句话总结工作流程

Deep read, write a plan, annotate the plan until it's right, then let Claude execute all the way through while type-checking.

深度阅读，撰写计划，注释计划直到正确，然后让 Claude 一路执行到底，同时检查类型。

That's it. No magic prompts, no elaborate system instructions, no clever tricks. Just a disciplined process that separates thinking from typing. Research prevents Claude from making ignorant changes. Planning prevents it from making wrong changes. The annotation loop injects my judgment. The implementation command lets it run uninterrupted once every decision has been made.

就这样。没有神奇的提示，没有精心设计的系统指令，没有巧妙的技巧。只是一个有纪律的流程，将思考与打字分开。研究防止 Claude 做出无知的更改。计划防止它做出错误的更改。注释循环注入我的判断。实现命令让它在每个决定都已做出后可以不间断地运行。

Try my workflow and you'll wonder how you ever shipped anything with a coding assistant without an annotated plan document sitting between you and the code.

试试我的工作流程，你会好奇没有一份注释计划文档夹在您和代码之间，您是如何通过编码助手交付任何东西的。

---

## 批判性思考评论 / Critical Thinking Commentary

### 作者核心论点分析

这篇文章的核心论点是：**AI 辅助编程的关键不在于提示词工程，而在于建立一套"规划-审阅-执行"的分离式工作流程**。作者主张将"思考"（研究、规划、注释）与"打字"（代码实现）严格区分，通过 markdown 文档作为"共享可变状态"来实现人机协作。

作者的主要论点包括：
1. **深度研究是防止"垃圾进垃圾出"的关键** — 通过要求 Claude 撰写详细的研究文档，开发者可以在早期发现并纠正误解
2. **注释循环是注入人类判断的核心机制** — 通过在计划文档中添加内联注释，开发者可以将产品优先级、业务约束和工程权衡传递给 AI
3. **实现应该是"乏味的"** — 一旦计划正确，执行就应该是机械的，而非创造性的
4. **单次长会话优于多次短会话** — 持续对话可以保持上下文连贯性

### 优点与亮点

1. **实践导向的方法论**：作者提供的不是理论框架，而是经过 9 个月实战验证的具体流程。每个阶段都有明确的提示词模板和流程图，具有很强的可操作性。

2. **对失败模式的深刻洞察**：作者指出 AI 编程最昂贵的失败不是语法错误，而是"在孤立环境中工作正常但破坏周围系统的实现"。这种系统性风险的认知比技术细节更有价值。

3. **人机协作的重新定位**：作者没有将 Claude 视为"自动编程工具"，而是将其定位为"执行者"，人类保留"架构师"和"审阅者"的角色。这种角色分工体现了对 AI 能力的清醒认知。

4. **文档即代码的理念**：将研究、计划、待办事项写入持久化的 markdown 文件，既作为审阅面，又作为项目资产。这比依赖聊天历史更具工程纪律性。

### 局限性与盲点

1. **对上下文窗口压缩的乐观假设**：作者声称没有看到 50% 上下文窗口后的性能下降，但这可能与特定类型的代码库有关。对于极其复杂的系统，自动压缩可能会丢失关键细节。

2. **注释循环的次数不确定性**：1-6 轮的注释循环听起来合理，但在实际项目中，如果需要 10 轮以上才能达到满意状态，这种工作流程的效率就会受到质疑。作者没有讨论如何界定"足够好"的标准。

3. **对团队协作的忽视**：这篇文章描述的是一种个人开发者的工作流程。在多人协作环境中，如何处理多个开发者对同一份 plan.md 的并发编辑？如何解决不同开发者之间的判断冲突？这些问题未被涉及。

4. **假设开发者具备足够的判断能力**：这个流程的有效性高度依赖开发者能够"正确"地审阅研究文档、添加有价值的注释、做出合理的技术决策。对于初级开发者，他们可能无法识别 Claude 的研究是否真正"深入"。

5. **对维护成本的低估**：研究文档、计划文档、待办清单需要持续维护。在快速迭代的项目中，这些文档可能迅速过时，成为技术债务的一部分。

### 我的批判性视角

作者的工作流程本质上是一种**"瀑布式"的人机协作模型**：研究 → 规划 → 注释 → 实现。这种方法在需求相对明确、系统相对稳定的场景下非常有效。然而，在现代软件开发中，"敏捷"和"探索式开发"往往是常态。

一个潜在的问题是：**过度的前期规划可能会抑制探索性创新**。有时候，最好的设计是在编码过程中"涌现"出来的，而不是在规划阶段完全确定的。作者的工作流程可能更适合增量式改进，而非从零开始的创新性架构设计。

另外，作者强调"实现应该是乏味的"，这暗示了一种**对编码劳动的贬低**。但实际上，许多开发者享受编码本身的创造性乐趣。如果将所有"有趣"的工作都交给 AI，而人类只负责"审阅"和"纠正"，这可能会改变软件开发的本质，甚至影响开发者的职业满意度。

### 深层启示

这篇文章揭示了一个更广泛的范式转变：**软件工程正在从"如何写代码"转向"如何与 AI 协作"**。作者的工作流程预示着一个未来，其中：

- **沟通能力**（撰写清晰的指令、添加精确的注释）可能比**编码能力**更重要
- **系统思维**（理解整体架构、识别依赖关系）可能比**语法知识**更有价值
- **审阅技能**（识别错误假设、评估设计方案）可能成为核心 competency

然而，这也带来了一个隐忧：如果未来的开发者过度依赖这种"规划-审阅"模式，他们可能会失去深入理解代码实现细节的能力。当 AI 的执行出现微妙错误时，缺乏编码经验的审阅者可能无法发现。

总的来说，这是一篇极具实践价值的文章，但其方法论更适合作为**工具箱中的一项工具**，而非**唯一正确的开发方式**。在不同的项目阶段、不同的团队结构、不同的创新需求下，开发者应该灵活调整人机协作的模式。
