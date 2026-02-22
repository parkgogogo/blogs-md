URL: https://worksonmymachine.ai/p/as-complexity-grows-architecture

---

有一段来自1997年的演讲，我一直在文章中反复提及，但这次我想引用其中不同的部分。

There's a 1997 lecture I keep referencing in my posts, but this time I want to quote a different part of it.

Alan Kay 站在一群程序员面前，谈论着狗屋。

Alan Kay stands before a group of programmers, talking about dog houses.

"你随便拿几块木板，用钉子和锤子把它们敲在一起，就得到了一个能立住的结构。除了知道怎么敲钉子，你不需要懂任何东西。"

"You take some boards, you nail them together with nails and a hammer, and you get something that stands up. You don't need to know anything beyond how to swing a hammer."

想象一下，有人把这个狗屋放大了100倍。一个教堂大小的狗屋。三十层楼高。

Imagine someone scales that dog house up by a factor of 100. A church-sized dog house. Thirty stories tall.

"当你把某样东西放大100倍时，它的质量会增加一百万倍，而它的强度……只增加一万倍……事实上，这个狗屋最终只会坍塌成一堆瓦砾。"

"When you scale something up by a factor of 100, its mass increases by a factor of a million, but its strength... only increases by a factor of ten thousand... The dog house, in fact, will just collapse into a pile of rubble."

面对这堆瓦砾，人们基本上有两种反应。

There are basically two responses to this pile of rubble.

Kay 说，流行的反应是看着瓦砾然后说："嗯，这就是我们一直以来想要做的。"用石灰岩把它糊起来。叫它金字塔。交付它。

Kay says the popular response is to look at the rubble and say: "Well, this is what we wanted to build all along." Slather it in limestone. Call it a pyramid. Ship it.

另一种反应是发明建筑学。Kay 将其称为"字面上的设计和建造成功的拱门……简单材料之间非显而易见的、非线性的相互作用，产生非显而易见的协同效应。"

The other response is to invent architecture. Kay calls it "literally designing and building the successful arch... the non-obvious, non-linear interactions of simple materials producing non-obvious synergies."

然后他提到了关于沙特尔大教堂（Chartres Cathedral）的一些事情。尽管它要大得多，但它比帕特农神庙（Parthenon）使用的材料更少（Claude 告诉我这可能不是字面意义上的真实，但从比例上使用更少材料绝对是真的！）。因为它几乎全是空气。几乎全是玻璃。"一切都以一种美丽的结构被巧妙地组织起来，使整体比任何部分都具有更强的完整性。"

Then he says something about Chartres Cathedral. Despite being much larger, it uses less material than the Parthenon (Claude tells me this might not be literally true, but proportionally using less material is absolutely true!). Because it's almost entirely air. Almost entirely glass. "Everything so beautifully structured and organized that the whole has more integrity than any of the parts."

更少的材料。更好的安排。更大的成果。

Less material. Better arrangement. Greater result.

一块石头不能成为一座桥。每个人都知道这一点。一块石头只是坐在那里，或者倒下。坐着和倒下基本上就是石头的全部本领。

One stone cannot be a bridge. Everyone knows this. One stone just sits there, or falls over. Sitting and falling are basically all one stone can do.

但如果你把一块石头靠在另一块石头上，再把另一块石头靠在上面，并且以一个非常特定的形状继续下去，你得到的就是一个拱门。而拱门可以支撑起一座桥。桥可以支撑起一辆马车。马车可以携带那些会压碎任何单独石头的东西。

But if you lean one stone against another, and another against that, and continue in a very particular shape, you get an arch. And an arch can support a bridge. A bridge can support a carriage. A carriage can carry what would crush any individual stone.

桥不在任何一块石头里。它在倾斜中。石头之间的关系才是桥存在的地方。

The bridge isn't in any one stone. It's in the leaning. The relationship between the stones is where the bridge lives.

我现在经常思考这个问题。可能想得太多了。昨天，我妻子问我为什么盯着一堵砖墙看，我说"我在想消息传递（message passing）"，她说"好的"——那种特定的语气意味着"我选择不追问这个。"

I think about this constantly now. Probably too much. Yesterday my wife asked why I was staring at a brick wall and I said "I'm thinking about message passing" and she said "Okay" — in that particular tone that means "I'm choosing not to follow up on that."

把代理（agents）串联在一起（或者微服务、或者 LLM 调用、或者管道中的步骤，或者任何……）存在这样一个问题：

There's a problem with chaining agents together (or microservices, or LLM calls, or steps in a pipeline, or anything...):

成功率会相乘。如果你有一个链条中的三个东西，每个都有80%的可靠性，数学看起来是这样的：

Success rates multiply. If you have three things in a chain, each 80% reliable, the math looks like this:

```
0.80 × 0.80 × 0.80 = 0.512
```

你的系统成功的几率大约和抛硬币一样。

Your system has about the same odds of success as a coin flip.

五个代理：33%。七个：21%。链条越长，它就越弱。每一个环节都是整个东西放弃并变成瓦砾的机会。

Five agents: 33%. Seven: 21%. The longer the chain, the weaker it becomes. Every link is a chance for the whole thing to give up and turn into rubble.

而每个人对此做了什么？他们看着那堆瓦砾。他们用石灰岩把它糊起来。更多的重试。更多的护栏。更多的回退逻辑。更多的材料。更大的金字塔。

And what does everyone do about this? They look at the rubble. They slather it in limestone. More retries. More guardrails. More fallback logic. More material. Bigger pyramid.

这就是软件工程的金字塔方法。Kay 在1997年谈论的是操作系统，但他本可以在2026年谈论 AI 代理生态系统而不需要改变一个字。

This is the pyramid approach to software engineering. Kay was talking about operating systems in 1997, but he could have been talking about AI agent ecosystems in 2026 without changing a word.

所以让我们深入探讨一下。

So let's get into it.

几周前我分享过，我一直在构建一个叫做提示对象（prompt objects）的东西。通过消息传递进行通信的对象，接收方在运行时用自然语言解释消息，任何东西都可以在系统运行时修改。Smalltalk 和面向对象编程背后的最初理念，但用 LLM 作为我们的消息解释器。

A few weeks ago I shared that I've been building something called prompt objects. Objects that communicate through message passing, where the receiver interprets messages in natural language at runtime, and anything can be modified while the system is running. The original idea behind Smalltalk and object-oriented programming, but with an LLM as our message interpreter.

我发现在这个系统中，数学可能会走向另一个方向。

I found that in this system, the math can go the other way.

因为每个对象都可以反思它收到的东西。提出澄清性问题。发送一条消息回来说"这没有意义，你能重新表述吗？"看着一个错误并修改自己来处理它。修改发送者。创建新对象来处理没有人预料到的问题。系统以某种方式绕过损伤，就像……我不知道……就像对话绕过误解一样。你说了一件事。另一个人眯起眼睛。你用不同的方式说。你们就达到了共识。

Because every object can reflect on what it receives. Ask clarifying questions. Send a message back saying "this doesn't make sense, can you rephrase?" Look at an error and modify itself to handle it. Modify the sender. Create new objects to handle problems nobody anticipated. The system routes around damage somehow, like... I don't know... like conversation routes around misunderstanding. You say something. The other person squints. You say it differently. You reach agreement.

而且，我不需要构建任何那些东西（我的意思是我不需要告诉 Claude 去构建任何那些东西）。

And, I didn't need to build any of that (I mean I didn't need to tell Claude to build any of that).

没有重试逻辑。没有错误恢复。没有协调层或编排框架或验证工具。只有能够接收消息并解释它们的对象。恢复、协调、自我纠正，这些都是从这种安排中自然产生的。它是涌现的。它是存在于倾斜中的桥，而不是在任何单独的石头里。

No retry logic. No error recovery. No coordination layer or orchestration framework or validation tooling. Just objects that can receive messages and interpret them. Recovery, coordination, self-correction — these emerge from the arrangement. They're emergent. They're the bridge that exists in the leaning, not in any individual stone.

**累积失败 vs 累积恢复。链条越长，系统就越具有反脆弱性。**

**Cumulative failure vs cumulative recovery. The longer the chain, the more antifragile the system becomes.**

标准的代理架构说：链条中的每一个环节都是失败的机会，所以你需要更多的基础设施来捕获这些失败。更多的重试。更多的护栏。更多的编排。更多的材料。更大的金字塔。

Standard agent architecture says: every link in the chain is an opportunity for failure, so you need more infrastructure to catch those failures. More retries. More guardrails. More orchestration. More material. Bigger pyramid.

提示对象架构说，每一次交互都是恢复的机会，因为对象会解释、协商和适应。错误纠正不是你在上面添加的一层。它是石头排列方式的一种属性。

Prompt object architecture says, every interaction is an opportunity for recovery because objects interpret, negotiate, and adapt. Error correction isn't a layer you add on top. It's a property of how the stones are arranged.

我没有设计这个。我不是要构建一个自我修复的架构。我是要认真对待消息传递的想法，看看会发生什么，而发生的事情是石头开始互相依靠，现在有了一座桥。

I didn't design this. I wasn't trying to build a self-healing architecture. I was taking the idea of message passing seriously and seeing what would happen, and what happened was that stones started leaning on each other and now there's a bridge.

比帕特农神庙更少的材料。几乎全是空气。

Less material than the Parthenon. Almost entirely air.

当你构建一个部分可以互相交谈并互相修改的系统时，会发生一种令人不安的事情。你查看日志和追踪记录，看看它是如何解决一个问题的，然后你会真正感到惊讶。系统开始发展出不在任何部分中的特性。那座不在任何石头里的桥。

Something unsettling happens when you build systems where parts can talk to each other and modify each other. You look at the logs and traces to see how it solved a problem and you genuinely get surprised. The system starts developing properties that aren't in any of the parts. The bridge that isn't in any stone.

我相信这里有一些关于意义如何运作的哲学思考。一条消息在被某物解释之前没有任何意义。一块石头在被某物依靠之前什么都不做。意义和结构是同一件事，或者是看待同一件事的两种方式，或者……我不知道……

I believe there's something philosophical here about how meaning works. A message has no meaning until something interprets it. A stone does nothing until something leans on it. Meaning and structure are the same thing, or two ways of looking at the same thing, or... I don't know...

当我第一次开始分享提示对象时，我总是被问到提示对象实际上能做什么。你不能只用 Langchain 什么的吗？公平的问题。我太深入这些理念了，以至于忘了指出一个具体的东西。

When I first started sharing prompt objects, I kept getting asked what prompt objects can actually do. Can't you just use Langchain or something? Fair question. I was so deep in the ideas that I forgot to point at a concrete thing.

所以前几天我决定指向 ARC-AGI。

So the other day I decided to point at ARC-AGI.

快速版本：François Chollet 的通用智能基准。网格谜题，彩色格子，从例子中找出规则。人类轻松解决它们。AI 大多不行。竞赛领先者使用多模型集成、进化搜索、自定义训练管道。

Quick version: François Chollet's general intelligence benchmark. Grid puzzles, colored cells, figure out the rules from examples. Humans solve them easily. AI mostly can't. Competition leaders use multi-model ensembles, evolutionary search, custom training pipelines.

我用提示对象构建了一个非常简单的求解器。它在 Haiku 4.5 上运行。小模型。几乎不花钱的那个。

I built a very simple solver with prompt objects. It runs on Haiku 4.5. Small model. The one that costs almost nothing.

它在解决它们。

It's solving them.

到目前为止大约解决了5个测试挑战。随着它解决每一个，我学到一些东西，更新对象，下一个就会做得更好。对象从它们自己的对话中学习。我从观察对象中学习。对象改变是因为我改变了它们，因为它们教会了我。你可以这样想……

About 5 test challenges solved so far. As it solves each one, I learn something, update the objects, and the next one does better. The objects learn from their own conversations. I learn from watching the objects. The objects change because I change them, because they teach me. You could think of it like...

……是的。我认为有一个词来形容系统穿过自己的层级并回来时被改变的循环。可能有。有人可能写了一本很长的书。带有赋格曲的那种。

...yeah. I think there's a word for cycles where systems pass through their own levels and come back changed. There probably is. Someone probably wrote a very long book about it. The kind with fugues in it.

现在听我说。我现在只在 ARC-AGI-1 上测试，这是2019年的原始版本。2023年之后训练的模型几乎肯定在它们的训练数据中见过这些模式。ARC Prize 团队自己说过，他们发现 Gemini 在没有被告知 ARC 的情况下使用了正确的 ARC 颜色映射。所以我在这里还不是来宣称排行榜分数的。（不过，看起来 GPT-5.2 (X-High) 在每项任务11.64美元的情况下得分90.5%，我的使用 Haiku 4.5 的提示对象系统在测试中每项任务不到1美元……）

Now hear me out. I'm only testing on ARC-AGI-1 right now, the original version from 2019. Models trained after 2023 have almost certainly seen these patterns in their training data. The ARC Prize team said themselves that they found Gemini using the correct ARC color mapping without being told about ARC. So I'm not here to claim leaderboard scores yet. (Though, looks like GPT-5.2 (X-High) scores 90.5% at $11.64 per task, and my prompt objects system with Haiku 4.5 costs less than $1 per task on tests...)

提示对象给你的是一种轻松建模过程的方式。也许你想要一个假设对象来提出规则。一个测试对象来对照例子检查它并解释为什么失败，而不仅仅是它失败了。有时一个对象可能意识到它需要帮助并创建一个新对象。推理就是对话。

What prompt objects give you is a way to model processes easily. Maybe you want a hypothesis object that proposes rules. A test object that checks it against examples and explains why it failed, not just that it failed. Sometimes an object might realize it needs help and create a new object. Reasoning is conversation.

我的整个求解器简单得荒谬，易于阅读。你可以在几分钟内跟踪执行并理解它。对比一下典型的代理管道：数百行的编排、重试逻辑、护栏、回退链。或者看看竞争性的 ARC-AGI 方法：测试时训练管道、对数千个候选者进行程序搜索，等等。整个基础设施的建立都是为了补偿底层架构的脆弱性。

My whole solver is ridiculously simple, readable. You can trace execution and understand it in minutes. Compare to a typical agent pipeline: hundreds of lines of orchestration, retry logic, guardrails, fallback chains. Or look at competitive ARC-AGI approaches: test-time training pipelines, program search over thousands of candidates, and so on. The whole infrastructure exists to compensate for fragility in the underlying architecture.

所有这些机械装置都是帕特农神庙。

All that machinery is the Parthenon.

这个小东西，这个 handful 的在一台廉价模型上传递消息的对象，是大量空气和玻璃，由它的排列方式支撑起来。

This little thing, this handful of objects passing messages on a cheap model, is a lot of air and glass, held up by its arrangement.

我一段时间以来一直在收到消息。友好的、深思熟虑的。人们问：你怎么让这个安全？你怎么约束它？类型在哪里？我们应该把它放在沙盒里吗？护栏在哪里？如果一个对象以你不打算的方式修改另一个对象怎么办？如果整个系统只是……走掉了怎么办？

I've been getting messages for a while now. Friendly, thoughtful ones. People asking: how do you make this safe? How do you constrain it? Where are the types? Should we put it in a sandbox? Where are the guardrails? What if an object modifies another object in ways you didn't intend? What if the whole system just... walks away?

我认出了这个。我实际上去年写过这个。钟摆。非形式主义者发现什么是可能的，然后形式主义者到来并使其可靠。自从 Kay 和 Dijkstra 在哲学峡谷中互相凝视以来，这种情况一直在发生。这里也会发生。

I recognize this. I actually wrote about this last year. The pendulum. The non-formalists discover what's possible, then the formalists arrive and make it reliable. This has been happening since Kay and Dijkstra stared at each other across the philosophical canyon. It will happen here too.

但回到我们开始谈论大教堂的时候。没有人在建造飞扶壁之前证明它会起作用。他们通过花费数世纪把石头靠在另一块石头上，弄清楚了石头的行为方式。形式化工程、结构分析、载荷计算，所有这些都是后来才出现的。你不能形式化一个你还没找到的东西。你甚至不知道什么是正确的约束，直到你看着系统做一些你没预料到的事情。

But back to when we were talking about cathedrals. Nobody proved flying buttresses would work before building them. They figured out how stones behaved by leaning them against each other for centuries. Formal engineering, structural analysis, load calculations — all of that came later. You can't formalize something you haven't found yet. You don't even know what the right constraints are until you watch the system do something you didn't anticipate.

而提示对象一直在做我没预料到的事情。

And prompt objects keep doing things I didn't anticipate.

所以是的。总有一天，有人会为这个构建类型系统。有人会编写形式化验证层。有人会弄清楚对于在运行时修改自己的系统，"正确"意味着什么，他们会构建工具来强制执行它。我期待那一天。我可能会使用那些工具。

So yeah. Someday, someone will build a type system for this. Someone will write formal verification layers. Someone will figure out what "correct" means for systems that modify themselves at runtime, and they'll build tools to enforce it. I look forward to that day. I'll probably use those tools.

但现在我们仍处于石头学习倾斜的部分。我们仍在弄清楚什么是可能的形状。如果你过早形式化，你就会锁定错误的形状，最终得到一个类型完美的金字塔。

But right now we're still in the part where stones are learning to lean. We're still figuring out what shapes are possible. If you formalize too early, you lock in the wrong shape and end up with a perfectly typed pyramid.

我宁愿现在拥有一个无类型的大教堂。

I'll take an untyped cathedral right now.

---

## 版本 0.5.0 发布 / Version 0.5.0 Release

0.5.0 版本刚刚发布，包含了一些新功能：

Version 0.5.0 just dropped with some new features:

**ARC-AGI 求解器模板** - 一个用 prompt_objects 构建的 ARC-AGI 求解器模板。一个起点。Fork 它。重新排列对象。系统设计为在运行时可以被重塑。尝试解决一些 ARC-AGI 问题，玩得开心。如果你想出了一些有趣的新想法，告诉我！

**ARC-AGI Solver Template** — A starter ARC-AGI solver built with prompt_objects. A starting point. Fork it. Rearrange the objects. The system is designed to be reshaped at runtime. Try solving some ARC-AGI problems, have fun. If you come up with interesting new ideas, tell me!

**如何开始：**

**How to get started:**

```bash
$ prompt_objects env create [YOUR ENVIRONMENT NAME] --template arc-agi-1
$ prompt_objects serve [YOUR ENVIRONMENT NAME] --open
```

**更新的交互式 Web 创作界面** - 你可以构建和测试你的提示对象系统。里面有很多功能。如果你有问题或想要导览，来 Discord 聊聊。

**Updated Interactive Web Authoring Interface** — You can build and test your prompt objects systems. There's a lot in there. If you have questions or want a tour, come chat on Discord.

**线程可视化器** - 你可以跟踪导出的执行过程，观察系统如何思考。一段对话。"对象 A 想到 X。告诉 B。B 不同意。A 创建了 C。C 找到了模式。"

**Thread Visualizer** — You can trace exported executions and watch the system think. A conversation. "Object A thought X. Told B. B disagreed. A created C. C found the pattern."

**实验性的基于画布（canvas）的界面** - 用于观察你的提示对象系统运行。这个我还在研究，但有时你想要对正在进行的通信有一个空间上的理解。如果你有改进建议，我很乐意听取！

**Experimental Canvas-based Interface** — For watching your prompt objects systems run. This one I'm still figuring out, but sometimes you want a spatial understanding of the communication happening. If you have suggestions for improvement, I'd love to hear them!

在 GitHub 上查看，或者从 Rubygems 安装 `gem install prompt_objects`

Check it out on GitHub, or install `gem install prompt_objects` from Rubygems.

ARC Prize 团队最近宣布了 ARC-AGI-3，这是他们第一个"代理评估基准"。它测试交互式推理：探索、规划、记忆、假设检验、跨步骤学习。

The ARC Prize team recently announced ARC-AGI-3, their first "agent evaluation benchmark." It tests interactive reasoning: exploration, planning, memory, hypothesis testing, learning across steps.

对我来说，这听起来像是在描述提示对象默认做的事情。几乎是偶然的。

To me, that sounds like describing what prompt objects do by default. Almost accidentally.

谁知道提示对象在 ARC-AGI-3 上会不会表现好。但这种架构正是为那种问题而构建的，因为消息传递和解释自然地产生那些行为。我没有把探索设计为一个功能。它只是因为石头被那样排列而出现了。

Who knows if prompt objects will perform well on ARC-AGI-3. But this architecture is exactly built for that kind of problem, because message passing and interpretation naturally produce those behaviors. I didn't design exploration as a feature. It just emerged because stones were arranged that way.

几乎全是空气。几乎全是玻璃。

Almost entirely air. Almost entirely glass.

---

## 批判性思考评论 / Critical Thinking Commentary

### 作者的主要论点分析

本文的核心论点是：**当系统复杂度增长时，架构设计的质量比单纯的材料堆砌更重要**。作者借用 Alan Kay 关于狗屋和建筑的比喻，生动地说明了简单的规模扩张（金字塔方法）与结构性创新（拱形/大教堂方法）之间的本质区别。

作者将这一思想应用于 AI 代理系统的设计，提出了"提示对象（prompt objects）"架构——一种基于消息传递、动态解释和涌现行为的系统设计理念。其核心洞察在于：**传统的链式代理架构存在可靠性乘积递减问题，而消息传递架构则能通过累积恢复机制实现反脆弱性**。

### 论证的优点

1. **比喻的力量**：狗屋→金字塔 vs 石头→拱桥→大教堂的比喻非常有力，将软件工程中抽象的架构问题具象化为建筑学中直观可见的结构原理。这种跨学科类比有助于读者快速抓住核心思想。

2. **数学直觉清晰**：0.8³=0.512 这个简单的概率计算直观地展示了链式系统的脆弱性，而"累积恢复"的概念则提供了一种令人耳目一新的解决思路。

3. **理论与实践结合**：作者不仅提出理论，还提供了 ARC-AGI 求解器的实际案例，用 Haiku 4.5（低成本小模型）对比 GPT-5.2（高成本大模型）的性能/成本比，增强了说服力。

4. **历史视角**：引用 Kay 1997年的演讲，将当代 AI 架构问题与计算机科学史上的经典辩论（如 Kay vs Dijkstra）联系起来，赋予了文章深度和历史纵深感。

### 论证的弱点与局限

1. **样本量问题**：作者承认只在 ARC-AGI-1（2019年版）上测试，且仅解决了约5个测试挑战。这一样本量过小，难以支撑"架构胜过材料"的普遍性结论。同时，训练数据污染问题（模型可能在训练中见过这些题目）也削弱了实验的严谨性。

2. **选择性证据**：作者对比 GPT-5.2 的成本时提到"每项任务11.64美元"，但省略了关键信息——GPT-5.2 达到了90.5%的成功率，而提示对象系统的成功率未明确说明。如果成功率差距巨大，成本对比就缺乏意义。

3. **概念模糊性**："涌现（emergent）"、"反脆弱性（antifragile）"、"消息传递"等核心概念缺乏形式化定义。虽然作者有意避免过早形式化，但这使得读者难以客观评估这些概念的内涵与边界。

4. **安全与可控性回避**：面对"如何约束系统"、"如果系统走掉怎么办"等关键问题，作者以"形式化会锁定错误的形状"为由回避了直接回答。这种态度在追求创新的同时，可能低估了实际部署中的风险。

### 我的批判性视角

**关于"架构 vs 材料"的二元对立**：作者将架构与材料对立起来的框架本身可能过于简化。在软件工程中，"材料"（如编程语言、框架、基础设施）与"架构"并非截然分离——好的材料（如具有强大类型系统的语言）本身就能支撑更好的架构。作者对"无类型大教堂"的浪漫化描述，可能忽视了类型系统在大型协作项目中的价值。

**关于"涌现"的解释力**：将系统的自修复能力归因于"涌现"可能是一种事后解释。真正的科学解释需要说明**为什么**以及**在什么条件下**会出现涌现行为。目前文章中描述的更像是启发式观察，而非系统性的因果分析。

**关于钟摆理论的适用性**：作者提到"非形式主义者发现可能，形式主义者使其可靠"的钟摆模式，但暗示当前处于"发现可能"阶段。然而，AI 系统的特殊性在于其影响的广泛性和潜在风险——与编程语言或操作系统不同，失控的 AI 代理可能造成即时、不可逆的伤害。"先建造，后规范"的策略可能不适用于高风险领域。

### 启示与影响

尽管存在上述局限，本文仍提出了值得深思的问题：

1. **对 AI 工程实践的启示**：当前 AI 应用开发确实存在"金字塔化"倾向——通过不断增加重试、护栏、编排层来掩盖底层模型的不可靠性。作者提出的"让交互本身成为恢复机会"的思路，可能为设计更具韧性的 AI 系统提供新方向。

2. **对研究方向的启示**：基于消息传递和动态解释的架构确实值得进一步探索，特别是在多代理协作、自适应系统等场景中。但这也呼唤更严格的理论框架和评估方法。

3. **对技术哲学的启示**：文章触及了软件工程中一个深层张力——形式化与探索性之间的平衡。作者倾向于后者，但健康的生态系统需要两者共存：探索性架构推动边界，形式化方法确保可靠性。

**结语**：这是一篇富有启发性的文章，其价值不在于提供了经过验证的技术方案，而在于提出了一个有力的思想框架来重新审视 AI 系统设计。正如作者所说，"石头仍在学习倾斜"——这个学习过程需要开放的探索精神，也需要严谨的批判审视。真正的大教堂需要既懂拱形原理、又懂材料特性的建筑师。
