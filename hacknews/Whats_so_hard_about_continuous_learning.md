URL: https://seangoedecke.com/continuous-learning/

Why can't models continue to get smarter after they're deployed? If you hire a human employee, they will grow more familiar with your systems over time, and (if they stick around long enough) eventually become a genuine domain expert. AI models are not like this. They are always exactly as capable as the first moment you use them.

为什么模型在部署后不能继续变得更聪明？如果你雇用一个人类员工，他们会随着时间的推移对你的系统越来越熟悉，而且（如果他们待得足够久）最终会成为真正的领域专家。AI 模型则不是这样。它们的能力永远和你第一次使用时一模一样。

This is because model weights are frozen once the model is released. The model can only "learn" as much as can be stuffed into its context window: in effect, it can take new information into its short-term working memory, but not its long-term memory. "Continuous learning" - the ability for a model to update its own weights over time - is thus [often described](https://www.dwarkesh.com/p/timelines-june-2025) as the bottleneck for AGI[1](#fn-1).

这是因为模型权重一旦发布就被冻结了。模型只能"学习"能够塞进其上下文窗口的内容：实际上，它可以将新信息纳入短期工作记忆，但不能纳入长期记忆。因此，"持续学习"——即模型能够随时间更新自身权重的能力——被[经常描述](https://www.dwarkesh.com/p/timelines-june-2025)为 AGI 的瓶颈[1](#fn-1)。

### Continuous learning is an easy technical problem

### 持续学习是一个简单的技术问题

However, the mechanics of continuous learning are not hard. The technical problem of "how do you change the weights of a model at runtime" is straightforward. It's the exact same process as post-training: you simply keep running new user input through the training pipeline you already have. In a sense, every LLM since GPT-3 is already capable of continuous learning (via RL, RLHF, or whatever). It's just that the continuous learning process is stopped when the model is released to the public.

然而，持续学习的机制并不困难。"如何在运行时改变模型权重"这个技术问题是直截了当的。这与后训练的过程完全相同：你只是不断地将新的用户输入通过你已经拥有的训练管道。从某种意义上说，自 GPT-3 以来的每个 LLM 都已经具备持续学习的能力（通过 RL、RLHF 或其他方式）。只是当模型向公众发布时，持续学习过程被停止了。

Internally, the continuous learning process might continue. I think it's fair to guess that OpenAI's GPT-5 is constantly training in the background, at least partly on outputs from ChatGPT and Codex[2](#fn-2). New checkpoints are constantly being cut from this process, some of which eventually become GPT-5.2 or GPT-5.3. In one sense, that's continuous learning!

在内部，持续学习过程可能会继续。我们有理由猜测 OpenAI 的 GPT-5 正在后台不断训练，至少部分是基于 ChatGPT 和 Codex 的输出[2](#fn-2)。这个过程不断产生新的检查点，其中一些最终成为 GPT-5.2 或 GPT-5.3。从某种意义上说，这就是持续学习！

So why can't I use a version of Codex that gets better at my own codebase over time?

那么，为什么我不能使用一个随时间推移在我的代码库上变得更好的 Codex 版本呢？

### Continuous learning is a hard technical problem

### 持续学习是一个困难的技术问题

The hard part about continuous learning is changing the model in ways that make it better, not worse. I think many people believe that model training improves linearly with data and计算: if you keep providing more of both, the model will keep getting smarter. This is false. If you simply hook up the model to learn continuously from its inputs, you are likely to end up with a model that gets worse over time. At least right now, model learning is a delicate process that requires careful human supervision.

持续学习的困难之处在于如何改变模型使其变得更好，而不是更糟。我认为许多人相信模型训练会随着数据和计算线性改善：如果你持续提供更多数据和计算，模型就会不断变得更聪明。这是错误的。如果你只是简单地将模型连接起来，让它持续从输入中学习，你很可能会得到一个随时间推移而变差的模型。至少现在，模型学习是一个需要精心人工监督的微妙过程。

Model training also has a big element of luck to it. If you train the "same" model a hundred times with a hundred different similarly-sized datasets (or even the same dataset and different seeds), you'll get a hundred different models with different capabilities[3](#fn-3). Sometimes I wonder if a big part of what AI labs are doing is continually pulling the lever on the slot machine by training many different model runs. Surprisingly strong models, like Claude Sonnet 4, might represent a genuinely better model architecture or training set. But part of it might be that Anthropic just hit on a lucky seed.

模型训练也有很大的运气成分。如果你用一百个不同但大小相似的数据集（甚至是相同的数据集但不同的随机种子）训练"相同"的模型一百次，你会得到一百个具有不同能力的不同模型[3](#fn-3)。有时我想知道，AI 实验室所做的大部分工作是否就是通过训练许多不同的模型运行来不断拉动老虎机的杠杆。像 Claude Sonnet 4 这样出人意料地强大的模型，可能代表了一个真正更好的模型架构或训练集。但部分原因可能是 Anthropic 恰好碰到了一个幸运的种子。

### Learning lessons from fine-tuning

### 从微调中汲取教训

The great hope for continuous learning is that it produces an AI software engineer who will eventually know all about your codebase, without having to go and research it from-scratch every time. But isn't there an easier way to produce this? Couldn't we simply fine-tune a LLM on the codebase we wanted it to learn?

对持续学习的最大期望是它能培养出一个 AI 软件工程师，最终了解你的整个代码库，而不必每次都从头开始研究。但难道没有更简单的方法来实现这一点吗？我们不能简单地在希望它学习的代码库上对 LLM 进行微调吗？

As it turns out, no. It is surprisingly non-trivial to do this. Way back in 2023, [everyone thought](https://huggingface.co/blog/personal-copilot) that fine-tuning was the next obvious step for LLM-assisted programming. But it's largely fizzled out, because it [doesn't really work](https://discuss.huggingface.co/t/fine-tuning-llms-on-large-proprietary-codebases/155828)[4](#fn-4). Just fine-tuning a LLM on your repository does not give it knowledge on how the repository works.

事实证明，不行。做到这一点出奇地不 trivial。早在 2023 年，[每个人都认为](https://huggingface.co/blog/personal-copilot)微调是 LLM 辅助编程的下一个显而易见的一步。但它基本上已经不了了之，因为它[并不太奏效](https://discuss.huggingface.co/t/fine-tuning-llms-on-large-proprietary-codebases/155828)[4](#fn-4)。仅仅在你的代码库上对 LLM 进行微调并不能让它了解代码库的工作原理。

It's unclear to me exactly why this should be. Maybe each individual piece of training data is just too small to make much difference, like a handful of grains of sand trying to change整个沙丘的形状。或者可能 LoRA 微调不够深入，无法真正融入对代码库的隐含理解（这可能非常复杂）。或者可能你需要在训练过程的更早阶段就融入代码库，在模型内部架构已经建立之前。

我不清楚为什么会是这样。也许每个单独的训练数据片段都太小了，无法产生太大影响，就像一把沙子试图改变整个沙丘的形状。或者可能 LoRA 微调不够深入，无法真正融入对代码库的隐含理解（这可能非常复杂）。或者可能你需要在训练过程的更早阶段就融入代码库，在模型内部架构已经建立之前。

In any case, fine-tuning a coding model on a specific codebase may be useful eventually. But it's not particularly useful now, which is bad news for people who hope that continuous learning can easily instil a real understanding of their codebases into a LLM. If you can't get that out of a deliberate fine-tune, why would you expect to get it out of a slapdash, automatic one? There may well be a series of ordinary "learning" problems to solve before "continuous learning" is possible.

无论如何，在特定代码库上微调编程模型最终可能是有用的。但现在它并不是特别有用，这对那些希望持续学习能轻松让 LLM 真正理解他们代码库的人来说是个坏消息。如果你无法从有意的微调中获得这种理解，为什么你会期望从一个草率的、自动的过程中获得呢？在"持续学习"成为可能之前，可能还有一系列普通的"学习"问题需要解决。

### Continuous learning is unsafe

### 持续学习是不安全的

Another reason why continuous learning is not currently an AI product is that it's dangerous. [Prompt injection](https://en.wikipedia.org/wiki/Prompt_injection) is already a real concern for LLM systems that ingest external内容。如果可以通过权重注入来远程后门模型，攻击者只需要广撒网然后等待。如果任何被攻击的模型最终获得了对某些敏感内容的访问权限（例如支付能力），攻击就可以在那時触发，即使模型当时没有暴露在提示注入之下。这要可怕得多。

持续学习目前还不是 AI 产品的另一个原因是它很危险。对于摄取外部内容的 LLM 系统来说，[提示注入](https://en.wikipedia.org/wiki/Prompt_injection)已经是一个真正令人担忧的问题。权重注入会有多糟糕呢？

We don't yet fully understand all the ways a LLM can be deliberately poisoned by a piece of training data, though some [Anthropic research](https://www.anthropic.com/research/small-samples-poison) suggests that it may not take much. Right now, prompt injection attacks are unsophisticated: the attacker just has to hope that they hit a LLM with the right access right now. But if you can remotely backdoor models via continuous learning, attackers just have to cast a wide net and wait. If any of the attacked models ever get given access to something sensitive (e.g. payment capability), the attack can trigger then, even if the model is not exposed to prompt injection at that time. That's much scarier.

我们还没有完全理解 LLM 可以通过训练数据被故意毒害的所有方式，尽管一些 [Anthropic 的研究](https://www.anthropic.com/research/small-samples-poison)表明这可能不需要太多。现在，提示注入攻击还不够复杂：攻击者只能希望他们在正确的时间击中具有正确访问权限的 LLM。但如果可以通过持续学习远程后门模型，攻击者只需要广撒网然后等待。如果任何被攻击的模型最终获得了对某些敏感内容的访问权限（例如支付能力），攻击就可以在那時触发，即使模型当时没有暴露在提示注入之下。这要可怕得多。

Big AI labs care a lot about how good their frontier models are (both in the moral and practical sense). The last thing they want is for someone's continous version of Claude Opus 5 to be poisoned into uselessness, or worse, into [Mecha-Hitler](/ai-personality-space). Microsoft's famously disastrous chatbot [Tay](https://blogs.microsoft.com/blog/2016/03/25/learning-tays-introduction/) happened less than ten years ago.

大型 AI 实验室非常关心他们的前沿模型有多好（无论是在道德层面还是实践层面）。他们最不希望看到的就是某人持续学习的 Claude Opus 5 版本被毒害到毫无用处，或者更糟，变成 [机械希特勒](/ai-personality-space)。微软臭名昭著的灾难性聊天机器人 [Tay](https://blogs.microsoft.com/blog/2016/03/25/learning-tays-introduction/) 就发生在不到十年前。

### Continuous learning is not portable

### 持续学习是不可移植的

Finally, I want to mention a fixable-but-annoying product problem with continuous learning. Say you have Claude-Sonnet-7-continuous running on your codebase for six months and it's working great. What do you do when Anthropic releases Claude-Sonnet-8? How do you upgrade?

最后，我想提到一个持续学习的可修复但令人讨厌的产品问题。假设你已经在你的代码库上运行了六个月的 Claude-Sonnet-7-continuous，而且效果很好。当 Anthropic 发布 Claude-Sonnet-8 时，你该怎么办？你如何升级？

Everything your model has learned from your codebase is encoded into its weights. At best, it might be encoded into a technically-portable LoRA adapter, which might work on the new model (or might not, if the architecture has changed). You're very likely to be unable to upgrade without losing all the data you've learned.

你的模型从代码库中学到的所有内容都编码在其权重中。充其量，它可能被编码成一个技术上可移植的 LoRA 适配器，这在新模型上可能奏效（也可能不奏效，如果架构已经改变）。你很可能无法在不丢失所有已学习数据的情况下进行升级。

I suppose it's sort of like having to hire a new, smarter engineer every six months. Some companies already try to do this with humans, so maybe they'd be happy doing it with models. But it creates an unpleasant incentive for users. Imagine you'd been using a continuous version of GPT-4o all this time. You should switch to GPT-5.3-Codex. But would you? Would your company?

我想这有点像每六个月就必须雇佣一个新的、更聪明的工程师。一些公司已经在尝试对人类这样做，所以也许他们对模型这样做也会满意。但这为用户创造了一个令人不快的激励。想象一下，你一直以来都在使用 GPT-4o 的持续学习版本。你应该切换到 GPT-5.3-Codex。但你会吗？你的公司会吗？

### Summary

### 总结

The hard part about continuous learning is not the continuous part, it's the automatic part. We already understand how to make a model that continuously "learns" from its outputs and updates its own weights. The problem is that model training is a manual process that requires constant intervention: to back off from a failed方向，让一个卡住的训练运行重新启动，等等。如果任其自行发展，持续学习很可能会陷入局部最小值，最终成为一个比你开始时更差的模型。

持续学习的困难之处不在于"持续"部分，而在于"自动"部分。我们已经知道如何制作一个从其输出中持续"学习"并更新自身权重的模型。问题在于模型训练是一个需要不断干预的手动过程：从失败的方向后退，让一个卡住的训练运行重新启动，等等。如果任其自行发展，持续学习很可能会陷入局部最小值，最终成为一个比你开始时更差的模型。

It's also not clear to me that simply running my Codex logs back through the Codex model would rapidly cause my model to understand my own codebases (at anything like the speed a human would). If we were living in that世界，我预计所有主要的 AI 编程公司都会提供代码库特定的模型微调作为一流产品——但他们没有，因为代码库特定的微调并不能可靠地奏效。

我也不清楚仅仅将我的 Codex 日志重新通过 Codex 模型运行，是否能迅速让我的模型理解我自己的代码库（以接近人类的速度）。如果我们生活在那个世界，我预计所有主要的 AI 编程公司都会提供代码库特定的模型微调作为一流产品——但他们没有，因为代码库特定的微调并不能可靠地奏效。

Why not just offer it anyway, and see what happens? First, AI labs go to a lot of effort to make their models safe, and allowing many customers to train their own unique models makes that basically impossible. Second, AI companies already have a terrible time getting their users to upgrade models: as an example, take the GPT-4o users who have been [captured](https://www.reddit.com/r/ChatGPT/comments/1mm9hns/we_request_to_keep_4o_forever/) by its sycophancy. Continuously-learning models would be hard to upgrade, even when users obviously ought to.

为什么不干脆提供它，看看会发生什么？首先，AI 实验室付出了很多努力来确保他们的模型安全，而允许许多客户训练他们自己独特的模型基本上使这成为不可能。其次，AI 公司在让用户升级模型方面已经遇到了很大困难：举个例子，那些因 GPT-4o 的谄媚而被["俘获"](https://www.reddit.com/r/ChatGPT/comments/1mm9hns/we_request_to_keep_4o_forever/) 的 GPT-4o 用户。持续学习的模型将很难升级，即使用户显然应该升级。

- AI systems can "continuously learn" in a sense by forming "memories": making notes to themselves in a database or text files. I'm not counting any of that stuff. It's like saying that the guy in Memento could remember things, since he was able to tattoo them onto his body. Proponents of continuous learning are talking about actual memory.
[↩](#fnref-1)

- AI 系统可以通过形成"记忆"来某种意义上"持续学习"：在数据库或文本文件中给自己做笔记。我不把这些算在内。这就像说《记忆碎片》里的 guy 能记住事情，因为他能把它们纹在身上。持续学习的支持者谈论的是真正的记忆。
[↩](#fnref-1)

- This is a guess on my part, but I'd be pretty surprised if I were wrong.
[↩](#fnref-2)

- 这只是我的猜测，但如果我错了，我会非常惊讶。
[↩](#fnref-2)

- I think most people who've spent time training models will agree with this. It could be different at big-lab scale! But I've seen enough speculation along these lines from AI lab employees on Twitter that I'm fairly confident advancing the idea.
[↩](#fnref-3)

- 我认为大多数花时间训练模型的人都会同意这一点。在大实验室规模上可能会有所不同！但我在 Twitter 上看到足够多的 AI 实验室员工对此类猜测，所以我相当有信心提出这个想法。
[↩](#fnref-3)

- Obviously it's hard to find a "we tried this and it didn't work" writeup from any tech company, so here's a HuggingFace thread from this year demonstrating that it is still not a solved problem.
[↩](#fnref-4)

- 显然，很难找到任何科技公司写的"我们试过这个，但没用"的文章，所以这里有一个来自今年 HuggingFace 的讨论串，证明这仍然是一个未解决的问题。
[↩](#fnref-4)

---

## 批判性思考评论

这篇文章对"持续学习"这一热门话题提出了务实的冷思考，值得肯定。作者从技术实现、安全性、产品化三个维度剖析了为什么持续学习听起来美好却难以落地。

**值得赞同的观点：**

1. **区分"能做什么"和"应该做什么"**：作者指出持续学习的技术机制（更新权重）本身不难，难的是如何让模型变好而不是变坏。这种区分很重要——很多 AI 讨论混淆了技术可行性和产品可用性。

2. **对微调现实的清醒认识**：2023 年整个行业都在鼓吹"个性化微调"，但现实是代码库微调并未产生预期效果。作者敢于指出皇帝没穿衣服。

3. **安全风险的深层思考**：权重注入比提示注入更危险，因为它可以被延迟触发。这个观点很有洞察力——攻击面从"即时触发"变成了"休眠后门"。

**可以质疑或补充的观点：**

1. **过于悲观的技术预设**：作者假设持续学习必须是"无人监督的自动学习"。但为什么不能是人机协同的持续学习？人类监督 + 自动化更新可能是中间路线。

2. **忽略了检索增强的进展**：虽然作者明确排除了"外部记忆"（数据库/文件），但现代 RAG 技术已经能在很大程度上模拟"学习效果"，而不需要改变模型权重。这可能是一条更务实的路径。

3. **对人类学习的类比过于简化**：作者暗示人类员工会自然成为领域专家，但现实中很多员工工作多年也没有真正理解系统。人类学习也不是自动的——需要刻意练习、反馈、反思。

4. **未探讨"混合架构"的可能性**：持续学习不一定要全部在基座模型上进行。或许可以有专门的轻量级适配层持续学习，而基座模型保持稳定。

**总体评价：**

这是一篇高质量的批判性文章，戳破了"持续学习 = AGI 瓶颈"的简单叙事。但作者可能过于聚焦"完全自动化的权重更新"这一极端情况，而忽略了渐进式、混合式的实现路径。持续学习的未来可能不是"全有或全无"，而是一个连续谱——从 RAG 到适配器微调到全模型更新，不同场景选择不同策略。
