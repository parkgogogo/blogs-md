URL: https://simonwillison.net/2026/Feb/22/how-i-think-about-codex/

## How I think about Codex

我如何看待 Codex

22nd February 2026

2026年2月22日

[How I think about Codex](https://www.linkedin.com/pulse/how-i-think-codex-gabriel-chua-ukhic). Gabriel Chua (Developer Experience Engineer for APAC at OpenAI) provides his take on the confusing terminology behind the term "Codex", which can refer to a bunch of of different things within the OpenAI ecosystem:

[我如何看待 Codex](https://www.linkedin.com/pulse/how-i-think-codex-gabriel-chua-ukhic)。Gabriel Chua（OpenAI 亚太区开发者体验工程师）分享了他对 "Codex" 这一令人困惑的术语的看法——在 OpenAI 生态系统中，这个词可以指代许多不同的东西：

In plain terms, Codex is OpenAI's software engineering agent, available through multiple interfaces, and an agent is a model plus instructions and tools, wrapped in a runtime that can execute tasks on your behalf. [...]

简单来说，Codex 是 OpenAI 的软件工程智能体，可通过多种界面使用。一个智能体等于模型加上指令和工具，包裹在一个可以代表你执行任务的运行时中。[...]

At a high level, I see Codex as three parts working together:

从高层次来看，我将 Codex 视为三个协同工作的部分：

Codex = Model + Harness + Surfaces [...]

Codex = 模型 + 工具架 + 交互界面 [...]

- Model + Harness = the Agent

- 模型 + 工具架 = 智能体

- Surfaces = how you interact with the Agent

- 交互界面 = 你与智能体交互的方式

He defines the harness as "the collection of instructions and tools", which is notably open source and lives in the [openai/codex](https://github.com/openai/codex) repository.

他将工具架定义为"指令和工具的集合"，值得注意的是，这部分是开源的，托管在 [openai/codex](https://github.com/openai/codex) 仓库中。

Gabriel also provides the first acknowledgment I've seen from an OpenAI insider that the Codex model family are directly trained for the Codex harness:

Gabriel 还提供了我从 OpenAI 内部人士那里看到的首次确认：Codex 模型系列是专门针对 Codex 工具架进行训练的：

Codex models are trained in the presence of the harness. Tool use, execution loops, compaction, and iterative verification aren't bolted on behaviors — they're part of how the model learns to operate. The harness, in turn, is shaped around how the model plans, invokes tools, and recovers from failure.

Codex 模型是在工具架的存在下进行训练的。工具使用、执行循环、压缩和迭代验证不是后期附加的行为——它们是模型学习操作方式的一部分。反过来，工具架也是根据模型如何规划、调用工具以及从失败中恢复来设计的。

---

**批判性思考评论：**

这篇文章澄清了 Codex 作为一个品牌名称的混乱之处。有趣的是，OpenAI 终于有人出来明确解释 Codex 不仅仅是一个模型，而是一个完整的系统：模型 + 工具架 + 交互界面。这种架构设计表明 OpenAI 正在从单纯的模型提供商向完整的智能体平台转型。

关键洞察是 Codex 模型是"在工具架的存在下进行训练"的——这意味着模型和工具是共同设计的，而不是简单地将工具调用能力 graft 到一个通用模型上。这与传统的 function calling 方法有本质区别。

然而，文章也暗示了一个潜在风险：如果工具架和模型紧密耦合，是否会降低系统的可扩展性和灵活性？当需要添加全新的工具类型时，是否意味着需要重新训练模型？
