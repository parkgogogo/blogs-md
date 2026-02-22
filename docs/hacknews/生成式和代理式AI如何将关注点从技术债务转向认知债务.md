# How Generative and Agentic AI Shift Concern from Technical Debt to Cognitive Debt

**原文链接 / Original URL**: https://simonwillison.net/2026/Feb/15/cognitive-debt/

---

The term technical debt is often used to refer to the accumulation of design or implementation choices that later make the software harder and more costly to understand, modify, or extend over time.

"技术债务"这一术语通常指设计或实现决策的累积，这些决策会使软件在日后更难理解、修改或扩展，且成本更高。

Technical debt nicely captures that "human understanding" also matters, but the words "technical debt" conjure up the notion that the accrued debt is a property of the code and effort needs to be spent on removing that debt from code.

技术债务很好地捕捉到了"人类理解"同样重要这一点，但"技术债务"这个词让人联想到累积的债务是代码的一种属性，需要花费精力从代码中消除这种债务。

Cognitive debt, a term gaining traction recently, instead communicates the notion that the debt compounded from going fast lives in the brains of the developers and affects their lived experiences and abilities to "go fast" or to make changes.

认知债务（cognitive debt）是一个最近越来越受关注的术语，它传达的理念是：追求快速开发所累积的债务存在于开发者的大脑中，影响他们的实际体验以及"快速前进"或做出变更的能力。

Even if AI agents produce code that could be easy to understand, the humans involved may have simply lost the plot and may not understand what the program is supposed to do, how their intentions were implemented, or how to possibly change it.

即使AI代理生成的代码本身易于理解，参与开发的人员可能已经完全迷失了方向——他们可能不理解程序应该做什么、他们的意图是如何被实现的，或者如何对其进行修改。

Technical debt lives in the code; cognitive debt lives in developers' minds.

技术债务存在于代码中；认知债务存在于开发者的大脑中。

Cognitive debt is likely a much bigger threat than technical debt, as AI and agents are adopted.

随着AI和代理技术的采用，认知债务可能比技术债务构成更大的威胁。

Peter Naur reminded us some decades ago that a program is more than its source code.

几十年前，Peter Naur提醒我们，程序不仅仅是其源代码。

Rather a program is a theory that lives in the minds of the developer(s) capturing what the program does, how developer intentions are implemented, and how the program can be changed over time.

相反，程序是一种存在于开发者头脑中的理论，它捕捉程序做什么、开发者的意图如何实现，以及程序如何随时间变化。

Usually this theory is not just in the minds of one developer but fragments of this theory are distributed across the minds of many, if not thousands, of other developers.

通常，这种理论不仅存在于一个开发者的头脑中，而且这一理论的碎片分布在许多（如果不是数千个）其他开发者的头脑中。

I saw this dynamic play out vividly in an entrepreneurship course I taught recently.

我在最近教授的一门创业课程中生动地看到了这种动态。

Student teams were building software products over the semester, moving quickly to ship features and meet milestones.

学生团队在一个学期内构建软件产品，快速推进以交付功能并达到里程碑。

But by weeks 7 or 8, one team hit a wall.

但到了第7、8周，有一支队伍撞上了墙。

They could no longer make even simple changes without breaking something unexpected.

他们甚至无法做出简单的修改而不破坏某些意想不到的东西。

When I met with them, the team initially blamed technical debt: messy code, poor architecture, hurried implementations.

当我与他们见面时，团队最初将其归咎于技术债务：混乱的代码、糟糕的架构、仓促的实现。

But as we dug deeper, the real problem emerged: no one on the team could explain why certain design decisions had been made or how different parts of the system were supposed to work together.

但当我们深入挖掘后，真正的问题浮现出来：团队中没有一个人能够解释为什么做出了某些设计决策，或者系统的不同部分应该如何协同工作。

The code might have been messy, but the bigger issue was that the theory of the system, their shared understanding, had fragmented or disappeared entirely.

代码可能很混乱，但更大的问题是，系统的理论——他们共同的理解——已经支离破碎或完全消失了。

They had accumulated cognitive debt faster than technical debt, and it paralyzed them.

他们积累认知债务的速度比技术债务更快，这使他们陷入了瘫痪。

This dynamic echoes a classic lesson from Fred Brooks' Mythical Man-Month.

这种动态呼应了Fred Brooks《人月神话》中的经典教训。

Adding more agents to a project may add more coordination overhead, invisible decisions, and thus cognitive load.

在项目中添加更多代理可能会增加更多的协调开销、不可见的决策，从而增加认知负荷。

Of course, agents can also be used to manage cognitive load by summarizing what changes have been made and how, but the core constraints of human memory and working capacity will be stretched with the push for speed at all costs.

当然，代理也可以通过总结已做出的更改以及如何做出的来管理认知负荷，但人类记忆和工作能力的核心限制将在不惜一切代价追求速度的过程中被拉伸。

The reluctance to slow down and to do the work that Kent Beck calls "make the hard change easy" is what will lead to cognitive debt and load in the future.

不愿放慢脚步去做Kent Beck所说的"让艰难的改变变得容易"的工作，将导致未来的认知债务和负荷。

In a breakout session at a recent Future of Software Engineering Retreat (arranged by Martin Fowler and Thoughtworks) we discussed how developers need to slow down and use practices such as pair programming, refactoring, and test-driven development to address technical debt AND cognitive debt.

在最近一次由Martin Fowler和Thoughtworks安排的软件工程未来研讨会的一个分组讨论中，我们讨论了开发者如何需要放慢脚步，使用结对编程、重构和测试驱动开发等实践来解决技术债务和认知债务。

By slowing down and following these practices, cognitive debt can also be reduced and shared understanding across developers and teams rebuilt.

通过放慢脚步并遵循这些实践，认知债务也可以减少，开发者和团队之间的共同理解也可以重建。

But what can teams do concretely as AI and agents become more prevalent?

但随着AI和代理技术变得更加普及，团队具体可以做什么？

First, they may need to recognize that velocity without understanding is not sustainable.

首先，他们可能需要认识到没有理解的开发速度是不可持续的。

Teams should establish cognitive debt mitigation strategies.

团队应该建立认知债务缓解策略。

For example, they may wish to require that at least one human on the team fully understands each AI-generated change before it ships, document not just what changed but why, and create regular checkpoints where the team rebuilds shared understanding through code审查、retrospectives, or knowledge-sharing sessions.

例如，他们可能希望要求团队中至少有一个人在每个AI生成的变更交付之前完全理解它，记录不仅是什么发生了变化，还有为什么，并创建定期检查点，团队通过代码审查、回顾或知识分享会议来重建共同理解。

Second, we need better ways to detect cognitive debt before it becomes crippling.

其次，我们需要更好的方法来在认知债务变得严重之前检测到它。

Warning signs include: team members hesitating to make changes for fear of unintended consequences, increased reliance on "tribal knowledge" held by just one or two people, or a growing sense that the system is becoming a black box.

警告信号包括：团队成员因担心意外后果而犹豫是否做出改变，越来越依赖仅由一两个人持有的"部落知识"，或者越来越感觉系统正在变成一个黑盒。

These may be signals that the shared theory is eroding.

这些可能是共同理论正在侵蚀的信号。

Finally, this phenomenon demands serious research attention.

最后，这一现象需要严肃的研究关注。

How do we measure cognitive debt?

我们如何衡量认知债务？

What practices are most effective at preventing or reducing it in AI-augmented development environments?

在AI增强的开发环境中，哪些实践对预防或减少认知债务最有效？

How does cognitive debt scale across distributed teams or open-source projects where the "theory" must be reconstructed by newcomers?

在分布式团队或开源项目中，认知债务如何扩展，因为在这些项目中"理论"必须由新人重建？

As generative and agentic AI reshape how software is built, understanding and managing cognitive debt may be one of the most important challenges our field faces.

随着生成式和代理式AI重塑软件的构建方式，理解和管理认知债务可能是我们领域面临的最重要挑战之一。

Cognitive debt tends not to announce itself through failing builds or subtle bugs after deployment, but rather shows up through a silent loss of shared theory.

认知债务往往不会通过构建失败或部署后的细微bug来宣告自己的存在，而是通过共同理论的悄然丧失来显现。

As generative and agentic AI accelerate development, protecting that shared theory of what the software does and how it can change may matter more for long-term软件健康 than any single metric of speed or output.

随着生成式和代理式AI加速开发，保护关于软件做什么以及如何变化的共同理论，对于长期软件健康可能比任何单一的速度或产出指标都更重要。

---

## 批判性思考评论 / Critical Thinking Commentary

### 作者主要论点分析

Margaret-Anne Storey这篇文章的核心论点是：AI辅助编程工具的普及正在将软件开发中的主要风险从技术债务转向认知债务。作者区分了两种债务的本质差异——技术债务是代码层面的问题，而认知债务是心智模型层面的问题。这一区分具有重要的理论价值，因为它提醒我们软件不仅仅是代码的集合，更是人类理解和意图的载体。

作者引用Peter Naur的"程序即理论"观点作为理论基础是恰当的。Naur早在几十年前就指出，程序的真正价值在于存在于开发者头脑中的理论，而非源代码本身。这一观点在AI时代显得尤为深刻——当AI可以瞬间生成大量代码时，人类是否还能保持对系统的理论理解？

### 优点

1. **概念创新**："认知债务"这一术语填补了现有软件工程词汇的空白。技术债务已经不足以描述AI时代的挑战，而认知债务精准地捕捉了问题的本质。

2. **实证支撑**：作者通过学生团队的真实案例说明了认知债务如何形成和爆发，这比纯理论论述更有说服力。学生在第7-8周突然"撞墙"的经历生动地展示了认知债务的隐蔽性和爆发性。

3. **解决方案具体**：作者不仅诊断问题，还提出了可操作的缓解策略，包括要求人类理解AI生成的变更、记录变更原因、建立知识分享机制等。

### 局限性

1. **测量难题**：作者承认认知债务难以测量（"不会通过构建失败来宣告自己"），但这也使得在实践中监控和管理认知债务变得困难。文章未能提供具体的评估框架或指标。

2. **适用范围模糊**：认知债务的概念主要适用于需要长期维护的软件项目。对于一次性原型或短期项目，追求速度而积累认知债务可能是一种理性的权衡。文章对此区分不够明确。

3. **AI的双刃剑效应讨论不足**：虽然作者提到AI可以用来总结变更、管理认知负荷，但没有深入探讨AI本身是否可能成为解决认知债务的工具——例如，AI能否帮助恢复"系统的理论"？

### 我的批判视角

我认为作者提出了一个极其重要的问题，但可能低估了AI在缓解认知债务方面的潜力。如果我们把AI视为团队的"新成员"而非纯粹的工具，那么关键在于如何设计人机协作模式，使得AI不仅生成代码，还能帮助维护和传递"系统的理论"。

此外，认知债务与技术债务并非完全独立——糟糕的技术债务往往会加速认知债务的积累（混乱的代码更难理解），反之亦然。两者的关系可能需要更深入的探讨。

### 影响与启示

1. **对教育者**：编程教育需要强调"理解"而非"产出"，培养学生阅读和理解代码的能力，而不仅仅是编写代码的能力。

2. **对团队管理者**：需要重新审视开发速度的衡量标准——真正的速度不是代码行数或功能数量，而是持续交付价值的能力。

3. **对工具设计者**：AI编程助手应该设计得不仅帮助生成代码，还要帮助开发者理解和维护心智模型。

总的来说，这篇文章是对AI时代软件工程挑战的及时警示。它提醒我们，技术的进步不应该以牺牲人类理解为代价——因为最终，软件是由人来维护、演进和依赖的。
