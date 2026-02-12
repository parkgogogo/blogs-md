> 一句话摘要：`pi` 的提示词设计不是“写一段很强的 system prompt”，而是把 **工具契约、运行规则、项目上下文、可扩展资源** 以可组合的方式注入模型上下文，从而提升长期稳定性与可维护性。

### 背景：为什么同一个模型，在不同工具里表现差很多

实践中常见的现象是：同一模型在不同工具里的“靠谱程度”差异很大。

差异通常不在模型本身，而在 **运行环境是否被清晰描述**：

- 有些工具把工具能力、使用边界、输出要求写清楚 → 模型更像“受控的执行系统”。
- 有些工具只给一个泛化提示 → 模型更像“自由聊天”。

`pi-mono` 在“操作提示词”上采取了工程化设计：提示词不仅描述角色，还明确工具契约与工作规则，并把项目级约束作为可插拔片段注入。

### 核心理念（一句话）

`pi` 的提示词设计可概括为：

> 把 agent 当作在受限环境里执行任务的系统；system prompt 的职责是声明工具契约与不变量（invariants），降低跑偏概率。

### 术语地图（先读这段）

- **system prompt（系统提示词）**：最高优先级的“工作说明书”。
- **tools（工具）**：read/bash/edit/write 等能力的接口约定。
- **guidelines（运行规则）**：哪些行为必须遵守（例如“先读再改”）。
- **project context（项目上下文）**：项目里的约束文件（AGENTS/SYSTEM/CLAUDE 等）。
- **skills（技能包）**：任务相关的可复用规则/脚本/参考资料，按需加载。

### 提示词原文：pi 的默认 system prompt（节选）

来源：`pi-mono/packages/coding-agent/src/core/system-prompt.ts`。

英文原文（节选）：

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

中文翻译（对照）：

```text
你是一个运行在 pi 这个“编码代理框架”里的资深编码助手。你的工作方式是读文件、执行命令、编辑代码、写新文件。

可用工具：
- read：读取文件内容
- bash：执行 bash 命令（ls/grep/find 等）
- edit：对文件做精确替换式编辑（必须精确匹配旧文本）
- write：创建或覆盖文件
...

运行规则：
- 编辑前必须先用 read 读文件；不要用 cat/sed 代替。
- 使用 edit 做精确修改（旧文本必须完全匹配）。
- write 仅用于新文件或整文件重写。
- 总结执行结果时，直接输出纯文本总结，不要再用 cat/bash 把内容打印出来。
- 回答要简洁。
- 操作文件时要明确写出文件路径。
```

### 设计拆解：为什么这套提示词“稳定”

提示词“稳定”通常来自三类设计：

- 声明工具契约（能做什么、不能怎么替代）
- 声明不变量（必须遵守的规则）
- 把变化因素模块化（项目上下文与技能包）

下面按机制拆开。

### 机制：工具契约（Tool Contract）——把工具当 API 写

### 它是什么

提示词中对工具的描述使用“工具名 + 一句话能力”的形式，接近 API 说明。

### 为什么需要

常见失败模式是“存在专用工具但模型绕行”。例如：

- 提供了 `read`，却去 `bash` 里 `cat file`

绕行带来的后果是：

- 不同环境输出不一致
- 权限/沙箱边界被破坏
- 后续难以做统一审计与恢复

### 怎么做（pi 的做法）

关键做法是把替代路径直接禁止：

```text
Use read ... instead of cat or sed.
```

### 错了会怎样

- 读文件路径/编码处理不一致 → 误读 → 误改
- 审计链断裂 → 无法复盘“读了什么、改了什么”

### 机制：规则少但硬（Invariants）——只写“会炸的规则”

### 它是什么

`pi` 的 guidelines 不是“写得多”，而是“写得硬”。典型规则集中在：

- read before edit
- edit 必须精确匹配
- write 只做整文件覆盖

### 为什么需要

在代码修改场景，最昂贵的错误不是“回答不够礼貌”，而是：

- 没读文件就改
- patch 失败还以为成功
- 反复输出噪音，掩盖真实改动

### 怎么做

用明确、可检查的动作约束（例如“old text must match exactly”），而不是“请谨慎”。

### 错了会怎样

- 修改不可复现、不可回滚
- 变更质量不稳定，难以规模化

### 机制：项目上下文注入（Project Context）——把项目规则外置

### 它是什么

`buildSystemPrompt()` 支持把项目上下文文件拼接到 system prompt。

英文原文（节选）：

```text
# Project Context

Project-specific instructions and guidelines:

## <file path>
<file content>
```

### 为什么需要

项目规则天然是“随 repo 变化”的：目录结构、约束、分支策略、CI 规则都不同。

把它们写死在默认 prompt 会导致：

- 跨项目复用差
- prompt 越写越长

### 怎么做

把项目规则当作“外置片段”，运行时发现并拼接（资源加载器负责发现/加载）。

### 错了会怎样

- 模型在不同 repo 里复用同一套假设 → 经常改错路径/违背项目约束

### 机制：skills（技能包）——把复杂工作法模块化

### 它是什么

skills 通过 `formatSkillsForPrompt()` 以“可触发的操作手册”形式进入 prompt（前提是 read 可用）。

### 为什么需要

系统提示词应尽量稳定，而工作流往往会变化。

把变化放在 skills 中可带来：

- 可维护（模块化更新）
- 可共享（团队复用）
- 可按需加载（减少主 prompt 膨胀）

### 怎么做

将“流程性强、需要反复引用”的内容放进 skill，而不是塞进 system prompt。

### 错了会怎样

- 主 prompt 过长，噪音增加
- 变更难以迭代（每次改 prompt 都像改内核）

### 机制：环境锚点（时间 + 工作目录）——减少无意义猜测

提示词末尾写入：

```text
Current date and time: ...
Current working directory: ...
```

目的很直接：

- 时间相关任务不再靠猜
- 文件操作有明确 cwd，减少“改错项目”的低级事故

### 补充：总结专用 system prompt（避免 compaction 跑偏）

位置：`pi-mono/packages/coding-agent/src/core/compaction/utils.ts`。

英文原文（节选）：

```text
You are a context summarization assistant...
Do NOT continue the conversation.
Do NOT respond to any questions...
ONLY output the structured summary.
```

中文翻译（对照）：

```text
你是一个上下文总结助手。
不要继续对话，不要回答对话里的问题。
只输出结构化总结。
```

设计思想：不同任务使用不同 system prompt，把“禁止跑偏”的边界写死。

### 可复用的设计清单（不依赖 pi 实现）

以下 5 条可以直接迁移到其它 agent 系统：

- 工具即契约：列出工具 + 禁止替代路径
- 规则少但硬：只写会导致事故的不变量
- 项目上下文外置：自动发现并拼接项目约束
- skills 模块化：把复杂工作流放在可维护模块里
- 环境锚点：时间 + cwd

### 附录：源码索引

- 默认 system prompt：`pi-mono/packages/coding-agent/src/core/system-prompt.ts`
- 上下文拼接与资源加载：`pi-mono/packages/coding-agent/src/core/resource-loader.ts`
- CLI 参数（system prompt/append）：`pi-mono/packages/coding-agent/src/cli/args.ts`
- 总结专用 prompt：`pi-mono/packages/coding-agent/src/core/compaction/utils.ts`
