# Code Like a Surgeon

> 原文作者：[Geoffrey Litt](https://geoffreylitt.com/)  
> 原文链接：https://geoffreylitt.com/2025/10/24/code-like-a-surgeon.html  
> 发布时间：2025-10-24

---

A lot of people say AI will make us all "managers" or "editors"…but I think this is a dangerously incomplete view!

很多人说 AI 会让我们所有人都变成"管理者"或"编辑"……但我认为这是一个危险且不完整的观点！

Personally, I'm trying to **code like a surgeon.**

就我个人而言，我正在努力**像外科医生一样编程。**

A surgeon isn't a manager, they do the actual work! But their skills and time are highly leveraged with a support team that handles prep, secondary tasks, admin. The surgeon focuses on the important stuff they are uniquely good at.

外科医生不是管理者，他们亲自做实际的工作！但他们的技能和时间被支持团队高度放大利用，这个团队负责准备工作、次要任务、行政事务。外科医生专注于他们独特擅长的关键事项。

My current goal with AI coding tools is to spend 100% of my time doing stuff that matters. (As a UI prototyper, that mostly means tinkering with design concepts.)

我目前使用 AI 编程工具的目标是将 100% 的时间花在真正重要的事情上。（作为 UI 原型设计师，这主要意味着钻研设计概念。）

It turns out there are a LOT of secondary tasks which AI agents are now good enough to help out with. Some things I'm finding useful to hand off these days:

事实证明，有很多次要任务现在的 AI Agent 已经能够很好地协助完成。最近我发现以下任务很适合交给 AI 处理：

- Before attempting a big task, write a guide to relevant areas of the codebase
- 在尝试大型任务之前，编写代码库相关区域的指南

- Spike out an attempt at a big change. Often I won't use the result but I'll review it as a sketch of where to go
- 快速实现一次重大变更的尝试。通常我不会直接使用结果，但会将其作为方向的草图来参考

- Fix typescript errors or bugs which have a clear specification
- 修复具有明确规范的 TypeScript 错误或 Bug

- Write documentation about what I'm building
- 编写关于我正在构建内容的文档

I often find it useful to run these secondary tasks async in the background – while I'm eating lunch, or even literally overnight!

我经常发现将这些次要任务异步放在后台运行很有用——在我吃午饭时，甚至真的在通宵时运行！

When I sit down for a work session, I want to feel like a surgeon walking into a prepped operating room. Everything is ready for me to do what I'm good at.

当我坐下来开始工作时，我想感觉像一位走进已准备就绪手术室的外科医生。一切都已准备妥当，让我可以专注于自己擅长的事情。

## Mind the autonomy slider
## 注意自主性滑块

Notably, there is a *huge* difference between how I use AI for primary vs secondary tasks.

值得注意的是，我将 AI 用于主要任务和次要任务的方式存在*巨大*差异。

For the core design prototyping work, I still do a lot of coding by hand, and when I do use AI, I'm more careful and in the details. I need fast feedback loops and good visibility. (eg, I like Cursor tab-complete here)

对于核心设计原型工作，我仍然大量手动编码，当我确实使用 AI 时，我会更加谨慎并关注细节。我需要快速的反馈循环和良好的可见性。（例如，我喜欢在这里使用 Cursor 的标签补全功能）

Whereas for secondary tasks, I'm much much looser with it, happy to let an agent churn for hours in the background. The ability to get the job done eventually is the most important thing; speed and visibility matter less. Claude Code has been my go-to for long unsupervised sessions but Codex CLI is becoming a strong contender there too, possibly my new favorite.

而对于次要任务，我对它宽松得多，乐于让 Agent 在后台运行数小时。最终能够完成任务是最重要的；速度和可见性没那么重要。Claude Code 一直是我在长时间无人监督会话中的首选，但 Codex CLI 也正在成为强有力的竞争者，可能是我新的最爱。

These are *very* different work patterns! Reminds me of Andrej Karpathy's ["autonomy slider"](https://www.latent.space/p/s3) concept. **It's dangerous to conflate different parts of the autonomy spectrum** – the tools and mindset that are needed vary quite a lot.

这些是*非常*不同的工作模式！这让我想起了 Andrej Karpathy 的["自主性滑块"](https://www.latent.space/p/s3)概念。**混淆自主性光谱的不同部分是危险的**——所需的工具和心态差异很大。

## Your agent doesn't need a career trajectory
## 你的 Agent 不需要职业发展轨迹

The "software surgeon" concept is a very old idea – Fred Brooks attributes it to Harlan Mills in his 1975 classic "The Mythical Man-Month". He [talks about](https://www.embeddedrelated.com/showarticle/1484.php) a "chief programmer" who is supported by various staff including a "copilot" and various administrators. Of course, at the time, the idea was to have humans be in these support roles.

"软件外科医生"这个概念是一个由来已久的想法——Fred Brooks 在他 1975 年的经典著作《人月神话》中将其归功于 Harlan Mills。他[谈到](https://www.embeddedrelated.com/showarticle/1484.php)一个由各种人员支持的"首席程序员"，包括"副驾驶"和各种管理员。当然，在当时，这个想法是让人类担任这些支持角色。

OK, so there is a super obvious angle here, that "AI has now made this approach economically viable where it wasn't before", yes yes… but **I am also noticing a more subtle thing at play, something to do with status hierarchies.**

好吧，这里有一个超级明显的角度，即"AI 现在使这种方法在经济上可行，而以前不可行"，是的，是的……但**我也注意到一个更微妙的事情在起作用，与地位等级有关。**

A lot of the "secondary" tasks are "grunt work", not the most intellectually fulfilling or creative part of the work. I have a strong preference for teams where everyone共享粗活；我讨厌把所有粗活都交给团队中地位较低的成员的想法。是的，初级成员通常会有更多的粗活，但他们也应该被给予许多有趣的任务来帮助他们成长。

A lot of the "secondary" tasks are "grunt work", not the most intellectually fulfilling or creative part of the work. I have a strong preference for teams where everyone shares the grunt work; I hate the idea of giving all the grunt work to some lower-status members of the team. Yes, junior members will often have more grunt work, but they should also be given many interesting tasks to help them grow.

很多"次要"任务都是"苦差事"，不是工作中最能满足智力或最具创造性的部分。我强烈偏好人人都分担苦差事的团队；我讨厌把所有苦差事都交给团队中地位较低成员的想法。是的，初级成员通常会有更多苦差事，但他们也应该被给予许多有趣的任务来帮助他们成长。

With AI this concern completely disappears! **Now I can happily delegate pure grunt work.** And the 24/7 availability is a big deal. I would never call a human intern at 11pm and tell them to have a research report on some code ready by 7am… but here I am, commanding my agent to do just that!

有了 AI，这种担忧完全消失了！**现在我可以愉快地将纯粹的苦差事委托出去。**而且 24/7 的可用性意义重大。我绝不会在晚上 11 点打电话给人类实习生，让他们在早上 7 点前准备好某段代码的研究报告……但现在，我正在命令我的 Agent 做这件事！

## Notion is for surgeons?
## Notion 是为外科医生准备的？

Finally I'll mention a couple thoughts on how this approach to work intersects with my employer, [Notion](https://notion.com/).

最后，我想谈谈这种工作方式如何与我的雇主 [Notion](https://notion.com/) 相交集的几点想法。

First, as an employee, I find it incredibly valuable right now to work at a place that is bullish on AI coding tools. Having support for heavy use of AI coding tools, and a codebase that's well setup for it, is enabling serious productivity gains for me – *especially* as a newcomer to a big codebase.

首先，作为一名员工，我发现现在在一个看好 AI 编程工具的地方工作非常有价值。对大量使用 AI 编程工具的支持，以及为此做好准备的代码库，为我带来了显著的生产力提升——*尤其*是作为一个大型代码库的新手。

Secondly, as a product – in a sense I would say we are trying to bring this way of working to a broader group of knowledge工作者 beyond programmers. When I think about how that will play out, I like the mental model of enabling everyone to "work like a surgeon".

其次，作为一个产品——从某种意义上说，我认为我们正在努力将这种工作方式带给程序员之外的更广泛的知识工作者群体。当我思考这将如何实现时，我喜欢让每个人都能"像外科医生一样工作"的心智模型。

The goal isn't to delegate your core work, it's to **identify and delegate the secondary grunt work tasks, so you can focus on the main thing that matters.**

目标不是委托你的核心工作，而是**识别并委托次要的苦差事任务，这样你就可以专注于真正重要的主要事情。**

---

If you liked this perspective, you might enjoy reading these other posts I've written about the nature of human-AI collaboration:

如果你喜欢这个观点，你可能也会喜欢阅读我写的这些关于人机协作本质的其他文章：

- [Enough AI copilots! We need AI HUDs](https://www.geoffreylitt.com/2025/07/27/enough-ai-copilots-we-need-ai-huds): "anyone serious about designing for AI should consider non-copilot form factors that more directly extend the human mind…"
- [Enough AI copilots! We need AI HUDs](https://www.geoffreylitt.com/2025/07/27/enough-ai-copilots-we-need-ai-huds)："任何认真为 AI 设计的人都应该考虑非副驾驶形式的因素，更直接地扩展人类思维……"

- [AI-generated tools can make programming more fun](https://www.geoffreylitt.com/2024/12/22/making-programming-more-fun-with-an-ai-generated-debugger): "Instead, I used AI to build a custom debugger UI… which made it more fun for me to do the coding myself…"
- [AI-generated tools can make programming more fun](https://www.geoffreylitt.com/2024/12/22/making-programming-more-fun-with-an-ai-generated-debugger)："相反，我使用 AI 构建了一个自定义调试器 UI……这让我自己编码变得更有趣……"

- [ChatGPT as muse, not oracle](https://www.geoffreylitt.com/2023/02/26/llm-as-muse-not-oracle): "What if we were to think of LLMs not as tools for answering questions, but as tools for asking us questions and inspiring our creativity?"
- [ChatGPT as muse, not oracle](https://www.geoffreylitt.com/2023/02/26/llm-as-muse-not-oracle)："如果我们不把 LLM 看作回答问题的工具，而是看作向我们提问并激发我们创造力的工具，会怎样？"

---

## 思考与评论

### 1. 关于"外科医生模式"的历史延续性

作者提到的"软件外科医生"概念确实可以追溯到 1975 年 Fred Brooks 的《人月神话》。有趣的是，这个概念在近 50 年后因为 AI 的出现而重新焕发活力。Harlan Mills 当年设想的是人类担任支持角色，而今天 AI 填补了这个位置。这提醒我们：**好的软件工程思想往往具有跨越时代的生命力**，只是实现方式随着技术演进发生了变化。

### 2. "自主性滑块"是一个关键洞察

Andrej Karpathy 的"自主性滑块"概念被作者很好地应用到了实际工作中。核心任务需要高精度、快速反馈、深度参与；次要任务可以接受异步、长时间的运行。这种区分非常重要，因为很多人在使用 AI 编程工具时犯的错误就是——要么对所有任务都过度干预，要么对所有任务都过度放任。**找到适合自己当前任务的"滑块位置"**是高效使用 AI 的关键。

### 3. 关于地位等级与道德困境的消解

作者提到的一个微妙但重要的点是：AI 消除了将"苦差事"委派给人类时的道德不适感。在现实团队中，让初级成员承担所有杂活是有问题的——这阻碍他们的成长，也造成不平等。但 AI 没有"职业发展"需求，没有自尊心，不会因为做杂活而感到被低估。**这让我们可以更纯粹地从效率角度考虑任务分配**，而不必担心人际关系和团队动态的影响。

### 4. 对"AI 会让人变成管理者"论点的反驳

作者开篇就反驳了流行的"AI 会让所有人都变成管理者/编辑"的观点。这是一个很有价值的纠正。外科医生模式表明，**人类仍然深度参与核心创造工作**，AI 只是承担了支持性角色。这不是从"执行者"到"管理者"的转变，而是从"独自完成一切"到"专注于高价值工作"的进化。

### 5. 值得进一步思考的问题

- 如果所有人都像外科医生一样工作，谁来培养"AI 支持团队"的能力？
- 当 AI 能力边界不断扩大，今天的"核心任务"明天是否也会变成"次要任务"？
- 这种模式是否会加剧程序员之间的能力分化——那些善于使用 AI 工具的人与那些不善于使用的人之间的差距？

总的来说，这是一篇非常务实的经验分享，提供了可操作的工作模式建议，而非空洞的理论探讨。
