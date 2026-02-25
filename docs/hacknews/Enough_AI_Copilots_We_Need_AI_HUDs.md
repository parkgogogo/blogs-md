# Enough AI Copilots! We Need AI HUDs

**Enough AI copilots! We need AI HUDs**  
*够了，AI 副驾驶！我们需要 AI 抬头显示器*

---

In my opinion, one of the best critiques of modern AI design comes from [a 1992 talk](https://cgi.csc.liv.ac.uk/~coopes/comp319/2016/papers/UbiquitousComputingAndInterfaceAgents-Weiser.pdf) by the researcher [Mark Weiser](https://en.wikipedia.org/wiki/Mark_Weiser) where he ranted against "copilot" as a metaphor for AI.

在我看来，对现代 AI 设计最好的批评之一来自研究员 [Mark Weiser](https://en.wikipedia.org/wiki/Mark_Weiser) 在 [1992 年的一次演讲](https://cgi.csc.liv.ac.uk/~coopes/comp319/2016/papers/UbiquitousComputingAndInterfaceAgents-Weiser.pdf)，他在演讲中猛烈抨击将"副驾驶"作为 AI 的隐喻。

This was 33 years ago, but it's still incredibly relevant for anyone designing with AI.

这已经是 33 年前的事了，但对于任何从事 AI 设计的人来说，它仍然具有惊人的现实意义。

---

## Weiser's Rant

## Weiser 的抨击

Weiser was speaking at an [MIT Media Lab event](https://www.dropbox.com/scl/fo/axpzd925tcsnkc9x5nd51/AJMdLqxafEYFun4Ns6fqMHo?dl=0&e=1&preview=frames_1992_014_Nov.pdf&rlkey=znit21hyth8w24m6gm02rq2y7) on "interface agents". They were grappling with many of the same issues we're discussing in 2025: how to make a personal assistant that automates tasks for you and knows your full context. They even had a human "butler" on stage representing an AI agent.

Weiser 是在 [MIT 媒体实验室](https://www.dropbox.com/scl/fo/axpzd925tcsnkc9x5nd51/AJMdLqxafEYFun4Ns6fqMHo?dl=0&e=1&preview=frames_1992_014_Nov.pdf&rlkey=znit21hyth8w24m6gm02rq2y7) 一个关于"界面代理"的活动上发言的。他们正在努力解决许多我们在 2025 年仍在讨论的相同问题：如何创建一个为你自动执行任务并了解你全部上下文的个人助手。他们甚至在舞台上安排了一个真人"管家"来代表 AI 代理。

Everyone was super excited about this… except Weiser. He was opposed to the whole idea of agents! He gave this example: how should a computer help you fly a plane and avoid collisions?

除了 Weiser，每个人对此都兴奋不已。他反对代理的整个概念！他举了这样一个例子：计算机应该如何帮助你驾驶飞机并避免碰撞？

**The agentic option is a "copilot" — a virtual human who you talk with to get help flying the plane.** If you're about to run into another plane it might yell at you "collision, go right and down!"

**代理式的选择是一个"副驾驶"——一个虚拟的人，你可以与之交谈以获得驾驶飞机的帮助。**如果你即将撞上另一架飞机，它可能会对你大喊："碰撞，向右下方躲避！"

Weiser offered a different option: **design the cockpit so that the human pilot is naturally aware of their surroundings.** In his words: "You'll no more run into another airplane than you would try to walk through a wall."

Weiser 提出了另一种选择：**设计驾驶舱，使人类飞行员能够自然地感知周围环境。**用他的话说："你撞上另一架飞机的可能性，不会比你试图穿墙而过的可能性更大。"

Weiser's goal was an "invisible computer"—not an assistant that grabs your attention, but a computer that fades into the background and becomes "an extension of [your] body".

Weiser 的目标是"隐形的计算机"——不是抓住你注意力的助手，而是淡入背景、成为"[你]身体的延伸"的计算机。

> Weiser's 1992 slide on airplane interfaces  
> *Weiser 1992 年关于飞机界面的幻灯片*

---

## HUDs

## 抬头显示器 (HUDs)

There's a tool in modern planes that I think nicely illustrates Weiser's philosophy: **the Head-Up Display (HUD), which overlays flight info like the horizon and altitude on a transparent display directly in the pilot's field of view.**

现代飞机中有一种工具很好地体现了 Weiser 的哲学：**抬头显示器（HUD），它将地平线、高度等飞行信息叠加在透明显示屏上，直接显示在飞行员的视野中。**

A HUD feels completely different from a copilot! You don't talk to it. It's literally part invisible—you just become naturally aware of more things, as if you had magic eyes.

HUD 给人的感觉与副驾驶完全不同！你不用和它交谈。它本质上是无形的——你只是自然地意识到更多事物，就好像你拥有了神奇的眼睛。

---

## Designing HUDs

## 设计 HUD

OK enough analogies. What might a HUD feel like in modern software design?

好了，类比够多了。在现代软件设计中，HUD 会是什么感觉？

One familiar example is spellcheck. Think about it: **spellcheck isn't designed as a "virtual collaborator" talking to you about your spelling.** It just instantly adds red squigglies when you misspell something! You now have a new sense you didn't have before. It's a HUD.

一个熟悉的例子是拼写检查。想想看：**拼写检查并不是被设计成一个"虚拟协作者"来和你讨论拼写。**它只是在你拼写错误时立即添加红色波浪线！你现在拥有了一个以前没有的新感知。这就是一个 HUD。

(This example comes from Jeffrey Heer's excellent [Agency plus Automation](https://idl.cs.washington.edu/files/2019-AgencyPlusAutomation-PNAS.pdf) paper. We may not consider spellcheck an AI feature today, but it's still a fuzzy algorithm under the hood.)

（这个例子来自 Jeffrey Heer 的优秀论文 [Agency plus Automation](https://idl.cs.washington.edu/files/2019-AgencyPlusAutomation-PNAS.pdf)。我们今天可能不认为拼写检查是一个 AI 功能，但它本质上仍然是一个模糊算法。）

> Spellcheck makes you aware of misspelled words without an "assistant" interface.  
> *拼写检查让你意识到拼写错误的单词，而无需"助手"界面。*

Here's another personal example from AI coding. Let's say you want to fix a bug. The obvious "copilot" way is to open an agent chat and ask it to do the fix.

这里还有一个来自 AI 编程的个人例子。假设你想修复一个 bug。显而易见的"副驾驶"方式是打开代理聊天并要求它进行修复。

But there's another approach I've found more powerful at times: **use AI to build a custom debugger UI which visualizes the behavior of my program!** In one example, I [built a hacker-themed debug view of a Prolog interpreter](/2024/12/22/making-programming-more-fun-with-an-ai-generated-debugger).

但我发现另一种方法有时更强大：**使用 AI 构建一个自定义调试器 UI 来可视化我的程序行为！**在一个例子中，我[为 Prolog 解释器构建了一个黑客主题的调试视图](/2024/12/22/making-programming-more-fun-with-an-ai-generated-debugger)。

With the debugger, I have a HUD! I have new senses, I can see how my program runs. The HUD extends beyond the narrow task of fixing the bug. I can ambiently build up my own understanding, spotting new problems and opportunities.

有了调试器，我就有了一个 HUD！我有了新的感知，我可以看到我的程序如何运行。HUD 超越了修复 bug 这个狭隘的任务。我可以在环境中建立自己的理解，发现新的问题和机会。

Both the spellchecker and custom debuggers show that automation / "virtual assistant" isn't the only possible UI. We can instead use tech to build better HUDs that enhance our human senses.

拼写检查和自定义调试器都表明，自动化/"虚拟助手"并不是唯一可能的 UI。相反，我们可以使用技术来构建更好的 HUD，以增强我们人类的感知。

---

## Tradeoffs

## 权衡

I don't believe HUDs are universally better than copilots! But I do believe **anyone serious about designing for AI should consider non-copilot form factors that more directly extend the human mind.**

我并不认为 HUD 在任何情况下都比副驾驶更好！但我确实相信，**任何认真对待 AI 设计的人都应该考虑非副驾驶的形式因素，那些能更直接地扩展人类思维的方式。**

So when should we use one or the other? I think it's quite tricky to answer that, but we can try to use the airplane analogy for some intuition:

那么我们应该在什么时候使用哪一种呢？我认为这个问题很难回答，但我们可以尝试用飞机类比来获得一些直觉：

When pilots just want the plane to fly straight and level, they fully delegate that task to an autopilot, which is close to a "virtual copilot". But if the plane just hit a flock of birds and needs to land in the Hudson, the pilot is going to take manual控制, and we better hope they have great instruments that help them understand the situation.

当飞行员只想让飞机平飞时，他们会完全将任务委托给自动驾驶仪，这接近于"虚拟副驾驶"。但如果飞机刚刚撞上一群鸟，需要在哈德逊河紧急迫降，飞行员就会接管手动控制，我们最好希望他们有很好的仪表来帮助他们了解情况。

In other words: routine predictable work might make sense to delegate to a virtual copilot / assistant. But when you're shooting for extraordinary outcomes, perhaps the best bet is to equip human experts with new superpowers.

换句话说：常规的可预测工作可能适合委托给虚拟副驾驶/助手。但当你追求非凡的结果时，最好的选择可能是为人类专家配备新的超能力。

---

## Further Reading

## 延伸阅读

- A nice discussion of one approach to this idea can be found in [Using Artificial Intelligence to Augment Human Intelligence](https://distill.pub/2017/aia/) by Michael Nielsen and Shan Carter.

- 关于这种方法的一个很好的讨论可以在 Michael Nielsen 和 Shan Carter 的 [使用人工智能增强人类智能](https://distill.pub/2017/aia/) 中找到。

- A more cryptic take on the same topic: [Is chat a good UI for AI? A Socratic dialogue](/2025/06/29/chat-ai-dialogue)

- 关于同一主题的一个更隐晦的看法：[聊天是 AI 的好 UI 吗？苏格拉底式对话](/2025/06/29/chat-ai-dialogue)

- A discussion of how the HUD philosophy intersects with on-demand software creation: [Malleable software in the age of LLMs](/2023/03/25/llm-end-user-programming)

- 关于 HUD 哲学如何与按需软件创建相交的讨论：[LLM 时代的可塑软件](/2023/03/25/llm-end-user-programming)

---

## 批判性思考 (Critical Commentary)

这篇文章提出了一个深刻的洞见：当前 AI 产品设计中"副驾驶"隐喻的泛滥可能限制了我们对于人机交互的想象力。作者通过 Weiser 1992 年的演讲，揭示了一个被忽视的视角——**技术应该扩展人类的能力，而不是替代人类的决策**。

**值得肯定的几个观点：**

1. **对"副驾驶"隐喻的质疑**确实击中要害。当前 ChatGPT、Claude 等产品的聊天界面虽然直观，但将 AI 局限在"对话助手"的角色中，可能错过了更丰富的交互可能性。

2. **拼写检查作为 HUD 的例子**非常精妙——它展示了技术如何在不打扰用户的情况下增强能力。这种"环境智能"（ambient intelligence）的理念在今天仍然具有启发性。

3. **自动驾驶 vs 紧急迫降的类比**提供了一个实用的决策框架：常规任务可以自动化，但关键时刻人类需要掌握主动权。

**值得商榷的地方：**

1. **HUD 的局限性被低估了**。拼写检查之所以能成为成功的 HUD，是因为它的反馈是**确定性的**（这个词拼错就是拼错）。但大多数 AI 任务（如代码生成、创意写作）的输出是**概率性的**，需要对话来澄清意图和迭代改进。在这种情况下，"副驾驶"界面可能是必要的选择。

2. **忽略了认知负荷问题**。HUD 假设用户能够同时处理更多信息，但这并不总是成立。当信息过载时，一个能够筛选和总结的"副驾驶"可能比持续显示所有信息的 HUD 更有价值。

3. **对 Weiser 哲学的引用需要更多批判**。"隐形计算机"的理想在特定场景下成立（如智能家居），但在知识工作中，用户往往需要**理解**系统如何工作，而不仅仅是使用它。完全隐形的系统可能导致"算法盲区"——用户不知道系统何时出错。

**一个更深层的思考：**

也许"副驾驶"和"HUD"并不是对立的选择，而是可以结合的设计元素。理想的 AI 产品可能应该具备：
- **HUD 模式**：在用户需要专注时提供环境感知增强
- **副驾驶模式**：在用户遇到复杂问题时提供对话式协助
- **智能切换**：根据上下文自动调整介入程度

正如作者在文中暗示的，关键在于**赋予人类专家新的超能力**，而不是简单地将任务外包给 AI。这个原则——增强而非替代——应该是所有 AI 产品设计的北极星。

---

*原文作者：Geoffrey Litt*  
*原文链接：https://geoffreylitt.com/2025/07/27/enough-ai-copilots-we-need-ai-huds.html*  
*翻译与评论：AI Assistant | 2025*
