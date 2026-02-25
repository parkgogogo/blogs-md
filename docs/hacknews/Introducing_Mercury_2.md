URL: https://www.inceptionlabs.ai/blog/introducing-mercury-2

## The fastest reasoning LLM, powered by diffusion

最快的推理型大语言模型，由扩散模型驱动

Today, we're introducing Mercury 2 — the world's fastest reasoning language model, built to make production AI feel instant.

今天，我们推出 Mercury 2 —— 世界上最快的推理型语言模型，旨在让生产级 AI 实现即时响应。

### Why speed matters more now

### 为什么速度现在比以往更重要

Production AI isn't one prompt and one answer anymore. It's loops: agents, retrieval pipelines, and extraction jobs running in the background at volume. In loops, latency doesn't show up once. It compounds across every step, every user, every retry.

生产级 AI 已经不再是"一个提示对应一个回答"的模式了。它是一个循环：智能体、检索管道和后台批量运行的抽取任务。在这样的循环中，延迟并非只出现一次，而是在每一步、每个用户、每次重试中层层累积。

Yet current LLMs still share the same bottleneck: autoregressive, sequential decoding. One token at a time, left to right.

然而，当前的 LLM 仍然面临着同样的瓶颈：自回归的、顺序解码。一次一个 token，从左到右。

### A new foundation: Diffusion for real-time reasoning

### 全新基础：面向实时推理的扩散模型

Mercury 2 doesn't decode sequentially. It generates responses through parallel refinement, producing multiple tokens simultaneously and converging over a small number of steps. Less typewriter, more editor revising a full draft at once. The result: >5x faster generation with a fundamentally different speed曲线.

Mercury 2 不进行顺序解码。它通过并行精炼生成回复，同时产生多个 token，并在少量步骤内收敛。不再是打字机式的逐字敲击，更像编辑一次性修订完整草稿。结果是：生成速度提升 5 倍以上，速度曲线发生了根本性改变。

That speed advantage also changes the reasoning trade-off. Today, higher intelligence means more test-time compute — longer chains, more samples, more retries — bought at the direct expense of latency and成本. Diffusion-based reasoning gets you reasoning-grade quality inside real-time latency budgets.

这种速度优势也改变了推理的权衡关系。如今，更高的智能意味着更多的测试时计算 —— 更长的推理链、更多的采样、更多的重试 —— 而这直接以延迟和成本为代价。基于扩散的推理则能在实时延迟预算内提供推理级别的质量。

## Mercury 2 at a glance

## Mercury 2 概览

Mercury 2 shifts the quality-speed curve for production deployments:

Mercury 2 改变了生产部署的质量-速度曲线：

- Speed: 1,009 tokens/sec on NVIDIA Blackwell GPUs
- 速度：在 NVIDIA Blackwell GPU 上达到 1,009 tokens/秒

- Price: $0.25/1M input tokens · $0.75/1M output tokens
- 价格：每百万输入 tokens $0.25 · 每百万输出 tokens $0.75

- Quality: competitive with leading speed-optimized models
- 质量：与领先的、速度优化型模型相媲美

- Features: tunable reasoning · 128K context · native tool use · schema-aligned JSON output
- 功能：可调推理深度 · 128K 上下文 · 原生工具调用 · 符合 schema 的 JSON 输出

We optimize for speed users actually feel: responsiveness in the moments users experience - p95 latency under high并发, consistent turn-to-turn behavior, and stable throughput when systems get busy.

我们优化的是用户真正能感知到的速度：用户实际体验时刻的响应性 —— 高并发下的 p95 延迟、一致的轮次间表现，以及系统繁忙时稳定的吞吐量。

"Inception's Mercury 2 demonstrates what's possible when new model architecture meets NVIDIA AI infrastructure. Surpassing 1,000 tokens per second on NVIDIA GPUs underscores the performance, scalability, and versatility of our platform to power the full spectrum of AI workloads."

"Inception 的 Mercury 2 展示了当新模型架构遇上 NVIDIA AI 基础设施时所能达到的可能性。在 NVIDIA GPU 上突破每秒 1,000 tokens 的速度，凸显了我们平台在性能、可扩展性和多功能性方面的优势，能够为全谱系 AI 工作负载提供动力。"

Shruti Koparkar, Senior Manager of Product, Accelerated Computing Group at NVIDIA

Shruti Koparkar，NVIDIA 加速计算集团产品高级经理

## What Mercury 2 unlocks in production

## Mercury 2 在生产中的应用价值

Mercury 2 excels in latency-sensitive applications where the user experience is non-negotiable.

Mercury 2 在延迟敏感型应用中表现出色，这类应用的用户体验不容妥协。

#### 1. Coding and editing

#### 1. 编程和编辑

Autocomplete, next-edit suggestions, refactors, interactive code agents - workflows where the developer is in the loop and any pause breaks flow.

自动补全、下一处编辑建议、重构、交互式代码智能体 —— 这些工作流中开发人员始终处于核心地位，任何停顿都会打断流畅感。

"Suggestions land fast enough to feel like part of your own thinking, not something you have to wait for."

"建议来得足够快，感觉就像是你自己思考的一部分，而不是需要等待的东西。"

Max Brunsfeld, Co-Founder, Zed

Max Brunsfeld，Zed 联合创始人

#### 2. Agentic loops

#### 2. 智能体循环

Agentic workflows chain dozens of inference calls per task. Cutting latency per call doesn't just save time, it changes how many steps you can afford to run, and how good the final output gets.

智能体工作流每个任务会串联数十个推理调用。降低每次调用的延迟不仅节省时间，还改变了你能负担多少步骤，以及最终输出能达到多好的质量。

"We're now leveraging the latest Mercury model to intelligently optimize campaign execution at scale. By surfacing insights and dynamically enhancing delivery in real time, we're driving stronger performance, greater efficiency, and a more resilient, AI-powered advertising ecosystem. This advancement reinforces our commitment to autonomous advertising, where intelligent systems continuously refine execution to deliver measurable outcomes for our clients."

"我们正在利用最新的 Mercury 模型来智能地大规模优化广告活动执行。通过实时呈现洞察和动态增强投放，我们实现了更强的性能、更高的效率，以及更具韧性的 AI 驱动广告生态系统。这一进步强化了我们致力于自主广告的决心，让智能系统持续优化执行，为客户带来可衡量的成果。"

Adrian Witas, SVP, Chief Architect, Viant

Adrian Witas，Viant 高级副总裁兼首席架构师

"We've been evaluating Mercury 2 because of its unparalleled latency and quality, especially valuable for real time transcript cleanup and interactive HCI applications. No other model has come close to the speed Mercury can provide!"

"我们一直在评估 Mercury 2，因为它无与伦比的延迟和质量，对于实时转录清理和交互式人机界面应用尤为宝贵。没有其他模型能接近 Mercury 提供的速度！"

Sahaj Garg, CTO & Co-Founder, Wispr Flow

Sahaj Garg，Wispr Flow 首席技术官兼联合创始人

"Mercury 2 is at least twice as fast as GPT-5.2, which is a game changer for us."

"Mercury 2 至少比 GPT-5.2 快两倍，这对我们来说是改变游戏规则的产品。"

Suchintan Singh, CTO & Co-Founder, Skyvern

Suchintan Singh，Skyvern 首席技术官兼联合创始人

#### 3. Real-time voice and interaction

#### 3. 实时语音和交互

Voice interfaces have the tightest latency budget in AI. Mercury 2 makes reasoning-level quality viable within natural speech cadences.

语音界面是 AI 中延迟预算最紧张的。Mercury 2 让推理级别的质量在自然语音节奏内成为可能。

"We build lifelike AI video avatars that hold real-time conversations with real people, so low latency isn't a nice-to-have, it's everything. Mercury 2 has been a big unlock in our voice stack: fast, consistent text generation that keeps the whole experience feeling natural and human."

"我们打造栩栩如生、能与真人实时对话的 AI 视频化身，因此低延迟不是锦上添花，而是生死攸关。Mercury 2 是我们语音技术栈的重大突破：快速、一致的文本生成，让整个体验保持自然和人性化。"

Max Sapo, CEO & Co-Founder, Happyverse AI

Max Sapo，Happyverse AI 首席执行官兼联合创始人

"Mercury 2 quality is excellent, and the model's low latency enables more responsive voice agents."

"Mercury 2 的质量非常出色，模型的低延迟让语音智能体响应更加灵敏。"

Oliver Silverstein, CEO & Co-Founder, OpenCall

Oliver Silverstein，OpenCall 首席执行官兼联合创始人

#### 4. Search and RAG pipelines

#### 4. 搜索和 RAG 管道

Multi-hop retrieval, reranking, and summarization latencies stack fast. Mercury 2 lets you add reasoning to the search loop without blowing your latency budget.

多跳检索、重新排序和摘要的延迟会快速叠加。Mercury 2 让你在搜索循环中加入推理能力，而不会突破你的延迟预算。

"Our partnership with Inception makes real-time AI for our search product practical. Every SearchBlox customer, across customer support, compliance, risk, analytics, and e-commerce, benefits from sub-second intelligence across all of their data."

"我们与 Inception 的合作让我们的搜索产品实现实时 AI 成为现实。每一位 SearchBlox 客户，无论是客户支持、合规、风控、分析还是电商领域，都能受益于跨所有数据的亚秒级智能。"

Timo Selvaraj, Chief Product Officer, SearchBlox

Timo Selvaraj，SearchBlox 首席产品官

## Get started

## 开始使用

Mercury 2 is available now.

Mercury 2 现已可用。

Mercury 2 is OpenAI API compatible. Drop into your existing stack - no rewrites required.

Mercury 2 兼容 OpenAI API。直接接入你现有的技术栈 —— 无需重写代码。

If you're doing an enterprise evaluation, we'll partner with you on workload fit, eval design, and performance validation under your expected serving constraints.

如果你正在进行企业级评估，我们将与你合作进行工作负载适配、评估设计和在你预期服务约束下的性能验证。

### Mercury 2 is live. Welcome to diffusion.

### Mercury 2 已上线。欢迎来到扩散模型的时代。

---

### 虾虾的批判性思考

**关于技术突破的审视**

Mercury 2 确实提出了一个有趣的命题：用扩散模型替代自回归模型来解决 LLM 的延迟问题。1,009 tokens/秒的速度在 Blackwell GPU 上确实令人印象深刻。但需要注意的是，这个速度数据是在特定的、顶级的硬件上测得的，普通用户或企业是否能获得相同的性能体验尚存疑问。

**定价策略的"甜蜜陷阱"**

$0.25/$0.75 的定价看似很有竞争力，但必须考虑到实际应用场景中，推理型模型往往需要多步思考和工具调用，这会导致输出 tokens 数量激增。"看起来便宜"和"实际便宜"之间可能有很大差距。文中没有披露典型的输出 token 量或平均推理步数，这让成本估算变得困难。

**客户证言的"幸存者偏差"**

文章列举了多家公司的积极评价，但我们看不到那些试用后没有采用 Mercury 2 的公司的声音。任何新产品都会有早期采用者，但大规模生产环境的稳定性、可靠性和长期表现才是真正的考验。此外，这些引述中使用了大量"听起来很厉害"的营销语言，实质性的技术细节描述较少。

**"推理质量"的模糊定义**

文章多次提到"reasoning-grade quality"（推理级质量），但并未给出具体的基准测试结果或与竞品的详细对比。"与领先的、速度优化型模型相媲美"这句话非常模糊 —— 是指与 GPT-4 Turbo？Claude 3.5 Sonnet？还是其他模型？缺乏量化的质量指标让这一声称难以验证。

**扩散模型的局限**

扩散模型在图像生成领域取得了巨大成功，但在语言任务中的应用仍相对新颖。文章没有讨论扩散模型可能面临的挑战，比如：对精确数值或代码的准确性如何？长程依赖的处理能力？以及最重要的一点 —— 在某些需要确定性输出的场景下，扩散模型的"生成"本质是否会成为劣势？

**总结**

Mercury 2 代表了一个值得关注的架构创新方向，但任何技术都需要时间和真实世界的大规模验证。作为潜在的采用者，建议从小规模试点开始，重点关注：1) 在你的具体用例上的准确率和召回率；2) 真实负载下的成本表现；3) 模型在边界情况下的鲁棒性。速度很重要，但如果以牺牲可靠性为代价，那可能得不偿失。
