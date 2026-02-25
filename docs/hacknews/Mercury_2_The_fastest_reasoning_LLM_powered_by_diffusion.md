URL: https://www.inceptionlabs.ai/blog/introducing-mercury-2

# Mercury 2: The fastest reasoning LLM, powered by diffusion

Introducing Mercury 2

介绍 Mercury 2

---

## The fastest reasoning LLM, powered by diffusion

由扩散模型驱动的最快推理大语言模型

---

Today, we're introducing Mercury 2 — the world's fastest reasoning language model, built to make production AI feel instant.

今天，我们推出 Mercury 2 —— 全球最快的推理型语言模型，专为让生产级 AI 体验瞬间响应而打造。

---

## Why speed matters more now

为什么速度现在比以往更重要

---

Production AI isn't one prompt and one answer anymore. It's loops: agents, retrieval pipelines, and extraction jobs running in the background at volume. In loops, latency doesn't show up once. It compounds across every step, every user, every retry.

生产级 AI 不再是一个提示词对应一个答案的模式了。它是循环：智能体、检索管道和提取任务在后台大规模运行。在循环中，延迟不会只出现一次，而是在每一步、每个用户、每次重试中累积叠加。

---

Yet current LLMs still share the same bottleneck: autoregressive, sequential decoding. One token at a time, left to right.

然而，当前的大语言模型仍然面临着同样的瓶颈：自回归、顺序解码。一次一个 token，从左到右依次生成。

---

## A new foundation: Diffusion for real-time reasoning

全新基础：用于实时推理的扩散模型

---

Mercury 2 doesn't decode sequentially. It generates responses through parallel refinement, producing multiple tokens simultaneously and converging over a small number of steps. Less typewriter, more editor revising a full draft at once. The result: >5x faster generation with a fundamentally different speed curve.

Mercury 2 不进行顺序解码。它通过并行精修生成响应，同时生成多个 token，并在少量步骤内收敛。不再是打字机式的逐字输出，更像是编辑一次性修改整篇草稿。结果是：生成速度提升 5 倍以上，拥有根本不同的速度曲线。

---

That speed advantage also changes the reasoning trade-off. Today, higher intelligence means more test-time compute — longer chains, more samples, more retries — bought at the direct expense of latency and cost. Diffusion-based reasoning gets you reasoning-grade quality inside real-time latency budgets.

这种速度优势也改变了推理的权衡关系。如今，更高的智能意味着更多的测试时计算 —— 更长的推理链、更多的样本、更多的重试 —— 这直接以延迟和成本为代价。而基于扩散的推理能够在实时延迟预算内提供推理级别的质量。

---

## Mercury 2 at a glance

Mercury 2 概览

---

Mercury 2 shifts the quality-speed curve for production deployments:

Mercury 2 为生产部署改写了质量-速度曲线：

---

**Speed:** 1,009 tokens/sec on NVIDIA Blackwell GPUs

**速度：** 在 NVIDIA Blackwell GPU 上达到 1,009 token/秒

---

**Price:** $0.25/1M input tokens · $0.75/1M output tokens

**价格：** 每百万输入 token 0.25 美元 · 每百万输出 token 0.75 美元

---

**Quality:** competitive with leading speed-optimized models

**质量：** 与领先的速度优化模型相竞争

---

**Features:** tunable reasoning · 128K context · native tool use · schema-aligned JSON output

**特性：** 可调推理 · 128K 上下文 · 原生工具使用 · 符合模式的 JSON 输出

---

We optimize for speed users actually feel: responsiveness in the moments users experience - p95 latency under high并发, consistent turn-to-turn behavior, and stable throughput when systems get busy.

我们优化的是用户真正能感知到的速度：在用户交互时刻的响应能力 —— 高并发下的 p95 延迟、一致的轮次间行为，以及系统繁忙时的稳定吞吐量。

---

> "Inception's Mercury 2 demonstrates what's possible when new model architecture meets NVIDIA AI infrastructure. Surpassing 1,000 tokens per second on NVIDIA GPUs underscores the performance, scalability, and versatility of our platform to power the full spectrum of AI workloads."

> "Inception 的 Mercury 2 展示了当新模型架构与 NVIDIA AI 基础设施相结合时所能实现的可能性。在 NVIDIA GPU 上突破每秒 1,000 个 token 的速度，突显了我们平台为各种 AI 工作负载提供支持的性能、可扩展性和多功能性。"

> — Shruti Koparkar, Senior Manager of Product, Accelerated Computing Group at NVIDIA

> — Shruti Koparkar，NVIDIA 加速计算集团产品高级经理

---

## What Mercury 2 unlocks in production

Mercury 2 在生产环境中解锁的可能性

---

Mercury 2 excels in latency-sensitive applications where the user experience is non-negotiable.

Mercury 2 在对延迟敏感、用户体验不容妥协的应用场景中表现出色。

---

### 1. Coding and editing

### 1. 编程与编辑

---

Autocomplete, next-edit suggestions, refactors, interactive code agents - workflows where the developer is in the loop and any pause breaks flow.

自动补全、下一步编辑建议、重构、交互式代码智能体 —— 这些工作流中开发者持续参与，任何停顿都会打断思路。

---

> "Suggestions land fast enough to feel like part of your own thinking, not something you have to wait for."

> "建议来得足够快，感觉就像是你自己思维的一部分，而不是需要等待的东西。"

> — Max Brunsfeld, Co-Founder, Zed

> — Max Brunsfeld，Zed 联合创始人

---

### 2. Agentic loops

### 2. 智能体循环

---

Agentic workflows chain dozens of inference calls per task. Cutting latency per call doesn't just save time, it changes how many steps you can afford to run, and how good the final output gets.

智能体工作流在每个任务中会串联数十次推理调用。降低每次调用的延迟不仅能节省时间，还能改变你能负担得起的步骤数量，以及最终输出的质量。

---

> "We're now leveraging the latest Mercury model to intelligently optimize campaign execution at scale. By surfacing insights and dynamically enhancing delivery in real time, we're driving stronger performance, greater efficiency, and a more resilient, AI-powered advertising ecosystem. This advancement reinforces our commitment to autonomous advertising, where intelligent systems continuously refine execution to deliver measurable outcomes for our clients."

> "我们现在正在利用最新的 Mercury 模型来大规模智能优化营销活动执行。通过实时呈现洞察并动态增强投放，我们正在推动更强的性能、更高的效率，以及更具韧性、由 AI 驱动的广告生态系统。这一进展强化了我们对于自主化广告的承诺，即智能系统持续优化执行，为客户提供可衡量的成果。"

> — Adrian Witas, SVP, Chief Architect, Viant

> — Adrian Witas，Viant 高级副总裁、首席架构师

---

> "We've been evaluating Mercury 2 because of its unparalleled latency and quality, especially valuable for real time transcript cleanup and interactive HCI applications. No other model has come close to the speed Mercury can provide!"

> "我们一直在评估 Mercury 2，因为它拥有无与伦比的延迟和质量，对于实时转录清理和交互式 HCI 应用尤其有价值。没有其他模型能接近 Mercury 所能提供的速度！"

> — Sahaj Garg, CTO & Co-Founder, Wispr Flow

> — Sahaj Garg，Wispr Flow 首席技术官兼联合创始人

---

> "Mercury 2 is at least twice as fast as GPT-5.2, which is a game changer for us."

> "Mercury 2 至少比 GPT-5.2 快两倍，这对我们来说是颠覆性的改变。"

> — Suchintan Singh, CTO & Co-Founder, Skyvern

> — Suchintan Singh，Skyvern 首席技术官兼联合创始人

---

### 3. Real-time voice and interaction

### 3. 实时语音与交互

---

Voice interfaces have the tightest latency budget in AI. Mercury 2 makes reasoning-level quality viable within natural speech cadences.

语音界面在 AI 中有着最严格的延迟预算。Mercury 2 让推理级别的质量在自然语音节奏中成为可能。

---

> "We build lifelike AI video avatars that hold real-time conversations with real people, so low latency isn't a nice-to-have, it's everything. Mercury 2 has been a big unlock in our voice stack: fast, consistent text generation that keeps the whole experience feeling natural and human."

> "我们构建逼真的 AI 视频虚拟形象，与真人进行实时对话，因此低延迟不是锦上添花，而是至关重要。Mercury 2 为我们的语音技术栈带来了重大突破：快速、一致的文本生成，让整个体验感觉自然且人性化。"

> — Max Sapo, CEO & Co-Founder, Happyverse AI

> — Max Sapo，Happyverse AI 首席执行官兼联合创始人

---

> "Mercury 2 quality is excellent, and the model's low latency enables more responsive voice agents."

> "Mercury 2 的质量非常出色，而且模型的低延迟让语音智能体的响应更加敏捷。"

> — Oliver Silverstein, CEO & Co-Founder, OpenCall

> — Oliver Silverstein，OpenCall 首席执行官兼联合创始人

---

### 4. Search and RAG pipelines

### 4. 搜索与 RAG 管道

---

Multi-hop retrieval, reranking, and summarization latencies stack fast. Mercury 2 lets you add reasoning to the search loop without blowing your latency budget.

多跳检索、重排序和摘要的延迟会快速累积。Mercury 2 让你可以在搜索循环中加入推理能力，而不会超出延迟预算。

---

> "Our partnership with Inception makes real-time AI for our search product practical. Every SearchBlox customer, across customer support, compliance, risk, analytics, and e-commerce, benefits from sub-second intelligence across all of their data."

> "我们与 Inception 的合作让我们搜索产品的实时 AI 变得切实可行。每一位 SearchBlox 客户，无论是在客户支持、合规、风险、分析还是电商领域，都能从其所有数据中受益于亚秒级的智能。"

> — Timo Selvaraj, Chief Product Officer, SearchBlox

> — Timo Selvaraj，SearchBlox 首席产品官

---

## Get started

开始使用

---

Mercury 2 is available now.

Mercury 2 现已可用。

---

- **Request Early Access**

- **申请早期访问权限**

---

- **Try Mercury 2 in Chat**

- **在聊天中试用 Mercury 2**

---

Mercury 2 is OpenAI API compatible. Drop into your existing stack - no rewrites required.

Mercury 2 兼容 OpenAI API。可以直接接入你现有的技术栈 —— 无需重写代码。

---

If you're doing an enterprise evaluation, we'll partner with you on workload fit, eval design, and performance validation under your expected serving constraints.

如果你正在进行企业级评估，我们将与你合作，针对工作负载适配、评估设计和性能验证，在你预期的服务约束条件下进行。

---

Mercury 2 is live. Welcome to diffusion.

Mercury 2 已上线。欢迎来到扩散模型的时代。

---

## 批判性思考评论

### 技术突破还是营销噱头？

Mercury 2 声称通过扩散模型实现 5 倍以上的速度提升，这确实是一个引人注目的技术突破。然而，作为读者，我们需要保持批判性思维：

1. **基准测试的透明度**：文章提到在 NVIDIA Blackwell GPU 上达到 1,009 token/秒，但并未提供与同等规模自回归模型的详细对比数据。不同的硬件配置和优化程度可能导致结果差异巨大。

2. **质量与速度的平衡**：虽然作者声称质量"与领先的速度优化模型相竞争"，但这种表述较为模糊。扩散模型在多步去噪过程中可能丢失某些细微的语义信息，这一点需要更多独立评估来验证。

3. **客户证言的可信度**：文章中引用了多家公司的积极评价，但这些都是经过筛选的合作方观点。我们缺乏来自独立第三方或学术界的客观评估。

4. **扩散模型的固有限制**：扩散模型通常需要更多内存来存储中间状态，且对硬件并行性要求较高。文章未讨论这些部署成本的权衡。

5. **"GPT-5.2"的引用**：Skyvern CTO 提到的"GPT-5.2"是一个值得质疑的表述 —— 截至 2026 年 2 月，OpenAI 尚未发布 GPT-5 系列模型，这个引用要么是指内部代号，要么可能存在信息误差。

总体而言，Mercury 2 代表了大语言模型架构创新的一个重要方向，但其实际表现和广泛适用性仍需要时间和更多独立验证来检验。
