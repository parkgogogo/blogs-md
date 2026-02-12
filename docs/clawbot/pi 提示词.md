> 一句话摘要：`pi` 的“提示词设计”不是一段玄学咒语，而是一套把 **工具、规则、项目上下文、可扩展性** 装进 system prompt 的工程方法。看懂它，你就能为自己的 agent 设计出同样稳定的“操作提示词”。

### 开场故事：为什么同一个模型，在不同工具里表现差很多？

很多人会误以为：只要模型一样，效果就差不多。

但你很快会发现：

- A 工具里它像个靠谱同事：会先读文件、会谨慎改动、会给清晰路径。
- B 工具里它像“刚入职”：乱猜、乱改、忘了约束。

差异往往不在模型，而在“操作提示词”（system prompt）怎么把 **运行环境** 讲清楚。

`pi` 在这件事上做得非常工程化。

### 核心理念（一句话）

`pi` 的提示词设计思想可以浓缩成一句话：

> 把 agent 当成一个在受限环境里工作的“可执行系统”，提示词负责把工具契约和工作规则说清楚。

### 术语地图（先读这段）

- **system prompt（系统提示词）**：给模型的最高优先级“工作说明书”。
- **tools（工具）**：read/bash/edit/write 等能力的接口约定。
- **guidelines（规范）**：告诉模型“先读再改、用哪个工具、如何输出”。
- **project context（项目上下文）**：项目里的约束文件（比如 AGENTS.md / SYSTEM.md 等）。
- **skills（技能包）**：额外加载的规则/脚本/参考资料（通过资源加载器注入提示词）。

### 先看原文：pi 的默认 system prompt 长什么样？

`pi` 的默认系统提示词来自：

- `pi-mono/packages/coding-agent/src/core/system-prompt.ts`

核心开头原文（节选，英文原文）：

```text
You are an expert coding assistant operating inside pi, a coding agent harness. You help users by reading files, executing commands, editing code, and writing new files.

Available tools:
- read: Read file contents
- bash: Execute bash commands (ls, grep, find, etc.)
- edit: Make surgical edits to files (find exact text and replace)
- write: Create or overwrite files
...

Guidelines:
- Use read to examine files before editing. You must use this tool instead of cat or sed.
- Use edit for precise changes (old text must match exactly)
- Use write only for new files or complete rewrites
- When summarizing your actions, output plain text directly - do NOT use cat or bash to display what you did
- Be concise in your responses
- Show file paths clearly when working with files
```

中文翻译（我翻译，便于你读）：

```text
你是一个运行在 pi 这个“编码代理框架”里的资深编码助手。你通过读文件、执行命令、编辑代码、写新文件来帮助用户。

可用工具：
- read：读取文件内容
- bash：执行 bash 命令（ls/grep/find 等）
- edit：对文件做精确替换式编辑（必须精确匹配旧文本）
- write：创建或覆盖文件
...

工作规范：
- 编辑前必须先用 read 读文件；不要用 cat/sed 去读。
- 用 edit 做精确修改（旧文本必须完全匹配）。
- write 只用于新文件或整文件重写。
- 总结你做过什么时，直接输出纯文本总结，不要再用 cat/bash 把内容打印出来。
- 回答要简洁。
- 操作文件时明确写出文件路径。
```

### 深入拆解：pi 的提示词为什么“好用”？

很多提示词写得很长，但不解决问题。`pi` 的好处在于：它每一段都在解决“真实会坏的点”。

### 机制：把工具当契约写进提示词（Tool Contract）

### 它是什么

`pi` 把工具描述写得像 API 文档：名字 + 一句话能力。

### 为什么需要

模型最常见的失败，是“明明有工具却不用、或者用错工具”。

比如：你提供了 `read`，它却去 `bash: cat file`。

### 怎么做（pi 的做法）

它不仅列出 tool，还给出强约束：

- “必须用 read，不能用 cat/sed”
- “edit 必须精确匹配 oldText”

### 错了会怎样

- 读错文件/读不到文件 → 瞎改
- patch 失败 → 反复重试、输出变噪音

### 机制：Guidelines 只写“会炸的规则”（少但硬）

`pi` 的 guideline 很克制：它不是写 100 条“你要友好”，而是写最影响正确性的几条。

典型几条：

- Read before edit
- Edit is surgical
- Write is full overwrite
- Summary 不要再用工具重复打印

这是“操作型提示词”最重要的特点：**避免泛泛而谈，专打事故点**。

### 机制：把“项目上下文”作为可插拔段落注入

这件事藏在 `buildSystemPrompt()` 里。

当你提供 context files（来自资源加载器发现的 AGENTS/SYSTEM 等文件）时，prompt 会追加一段：

英文原文（节选）：

```text
# Project Context

Project-specific instructions and guidelines:

## <file path>
<file content>
```

中文解释：

- `pi` 不把项目规则写死在默认 prompt
- 它把项目规则当“外置片段”，运行时自动拼接进 system prompt

这使得同一套 agent，在不同 repo 里能自然切换规则。

### 机制：技能（skills）不是“给模型背书”，而是“按需加载的操作手册”

`pi` 会把 skills 通过 `formatSkillsForPrompt()` 追加到 prompt（前提是 read 工具存在）。

这背后的思想是：

- 默认 prompt 保持小
- 具体任务的“工作法”放在 skill 里
- 只有在需要时才让模型读 skill（这是一种“渐进披露”）

这种结构非常适合做团队工作流：你不需要把所有规范塞进 system prompt，而是让 skill 作为可维护的模块。

### 机制：提示词末尾写入“当前时间 + 当前工作目录”

英文原文（节选）：

```text
Current date and time: ...
Current working directory: ...
```

这看起来很小，但能解决两个常见坑：

- 模型胡乱猜日期/时间
- 模型改错目录下的文件（尤其在 monorepo/多项目）

### 额外值得看：pi 的“总结专用提示词”

`pi` 的 compaction/branch summary 不是随便总结，它还有“总结专用系统提示词”。

位置：

- `packages/coding-agent/src/core/compaction/utils.ts`

原文（节选）：

```text
You are a context summarization assistant...
Do NOT continue the conversation.
Do NOT respond to any questions...
ONLY output the structured summary.
```

中文翻译：

```text
你是一个上下文总结助手。
不要继续对话，不要回答对话里的问题。
只输出结构化总结。
```

这体现了 `pi` 的一个很强的工程习惯：

> 不同任务用不同提示词，把“不要跑偏”的边界写死。

### 你要抄 pi 的提示词思想，抄什么最值？

我建议你只抄 5 条（足够做出 80% 的稳定性）：

- 把工具当契约：列工具 + 禁止替代路径（read≠cat）
- 规则少但硬：只写会炸的规则
- 项目上下文外置：自动拼接 AGENTS/SYSTEM
- skill 模块化：把复杂工作流放在 skill，不塞 prompt
- 末尾加环境锚点：时间 + cwd

### 附录：源码索引

- 默认 system prompt：`pi-mono/packages/coding-agent/src/core/system-prompt.ts`
- 资源加载与上下文拼接：`pi-mono/packages/coding-agent/src/core/resource-loader.ts`
- CLI 参数（system prompt/append）：`pi-mono/packages/coding-agent/src/cli/args.ts`
- 总结专用 prompt：`pi-mono/packages/coding-agent/src/core/compaction/utils.ts`
