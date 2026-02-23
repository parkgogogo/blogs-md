URL: https://worksonmymachine.ai/p/as-complexity-grows-architecture

## As Complexity Grows, Architecture Dominates Material

随着复杂性增长，架构胜过材料

There's [this talk from 1997](https://www.youtube.com/watch?v=oKg1hTOQXoY) that I keep bringing up on here, but there's a different part I want to call to your attention this time. Alan Kay, standing in front of a room of programmers, talking about dog houses.

我在这篇文章中[反复提到 1997 年的这个演讲](https://www.youtube.com/watch?v=oKg1hTOQXoY)，但这次我想引起你注意的是一个不同的部分。Alan Kay 站在一屋子程序员面前，谈论狗屋。

"You take any random boards, nail and hammer, pound them together and you've got a structure that will stay up. You don't have to know anything except how to pound a nail to do that."

"你随便拿些木板，用钉子和锤子，把它们敲在一起，你就得到了一个能立起来的结构。除了如何敲钉子，你不需要知道任何事情。"

So imagine someone scales this dog house up by a factor of 100. A cathedral-sized dog house. Thirty stories. "When you blow something up by a factor of 100, its mass goes up by a factor of a million, and its strength... only goes up by a factor of 10,000... And in fact what will happen to this doghouse is it will just collapse into a pile of rubble."

想象一下有人把这个狗屋放大 100 倍。一个 cathedral 大小的狗屋。三十层楼。"当你把某物放大 100 倍时，它的质量会增加一百万倍，而它的强度……只会增加一万倍……事实上，这个狗屋会发生的事情是它只会倒塌成一堆瓦砾。"

There are pretty much two reactions to seeing the pile. The popular one, Kay says, is to look at the rubble and go: "Well that was what we were trying to do all along." Plaster it over with limestone. Call it a pyramid. Ship it.

看到这一堆瓦砾基本上有两种反应。Kay 说，流行的反应是看着瓦砾说："嗯，那一直是我们想做的事情。"用石灰石 plaster 它。称它为金字塔。发布它。

The other reaction is to invent architecture. Which Kay refers to as "literally the designing and building of successful arches... a non-obvious, non-linear interaction between simple materials to give you non-obvious synergies."

另一种反应是发明建筑学。Kay 将其称为"字面上成功拱门的建造……简单材料之间非显而易见的、非线性的相互作用，以产生非显而易见的协同效应。"

Then he mentions this thing about Chartres Cathedral. That it contains less material than the Parthenon, despite being enormously larger (Claude tells me that's likely not literally true, but proportionally less material absolutely!). Because it's almost all air. Almost all glass. "Everything is cunningly organized in a beautiful structure to make the whole have much more integrity than any of its parts."

然后他提到了关于沙特尔大教堂的事情。它包含的材料比帕特农神庙少，尽管它大得多（Claude 告诉我这在字面上可能不是真的，但按比例来说材料更少绝对是真的！）。因为它几乎都是空气。几乎都是玻璃。"一切都被巧妙地组织在一个美丽的结构中，使整体比任何部分都具有更多的完整性。"

Less stuff. Better arrangement. Bigger result.

更少的东西。更好的安排。更大的结果。

## The pyramid approach to software engineering

软件工程的金字塔方法

A stone cannot be a bridge. Everyone knows this. A stone just sits there, or falls. Sitting and falling is basically the entire repertoire of stones.

石头不能成为桥梁。每个人都知道这一点。石头只是坐在那里，或者掉下来。坐和掉基本上是石头的全部本领。

But if you lean one stone against another stone, and lean another stone against that, and keep going in a very specific shape, what you get is an arch. And the arch can hold up a bridge. And the bridge can hold up a cart. And the cart can carry things that would crush any individual stone.

但如果你把一块石头靠在另一块石头上，再把另一块石头靠在那块上，并以一个非常特定的形状继续下去，你得到的就是一个拱门。拱门可以支撑一座桥。桥可以支撑一辆马车。马车可以运载会压碎任何单独石头的东西。

There's this problem with chaining agents together (or microservices, or LLM calls, or steps in a pipeline, or whatever...) Success rates multiply. If you have three things in a chain, each 80% reliable the math looks like this: 0.80 × 0.80 × 0.80 = 0.512. Your system succeeds about as often as a coin flip.

将智能体链接在一起（或微服务、或 LLM 调用、或管道中的步骤，或无论什么……）存在这个问题。成功率是相乘的。如果你链中有三个东西，每个 80% 可靠，数学看起来像这样：0.80 × 0.80 × 0.80 = 0.512。你的系统成功的频率大约和抛硬币一样。

Five agents: 33%. Seven: 21%. The longer your chain, the weaker it gets. Every link is an opportunity for the whole thing to give up and become rubble.

五个智能体：33%。七个：21%。你的链越长，它就越弱。每个环节都是整个东西放弃并成为瓦砾的机会。

---

**批判性思考评论：**

这篇文章的核心论点是：在复杂系统中，架构设计比材料（组件）质量更重要。作者借用 Alan Kay 关于 Chartres Cathedral 的比喻，说明优秀的架构可以用更少的材料实现更大的成果。

这对当前 AI 智能体生态系统有直接的启示：

1. **可靠性乘法问题**：当链接多个 AI 智能体时，系统可靠性是相乘而非相加的。三个 80% 可靠性的智能体串联后，整体可靠性降至 51%。这是微服务架构和 AI 管道设计中的根本挑战。

2. **两种工程哲学**：
   - 金字塔方法：遇到问题时添加更多层（guardrails、retries、fallbacks），最终产生臃肿但脆弱的系统
   - 建筑学方法：设计智能体之间的协作方式，使整体大于部分之和

3. **Prompt Objects 的尝试**：作者提出的"提示对象"概念——使用消息传递而非链式调用——可能是一种建筑学解决方案。每个对象可以反思、询问澄清、重新表述，从而在运行时纠正错误，而不是让错误传播。

这篇文章提醒我们：在 AI 时代，软件工程的基本原则没有改变——复杂性管理仍然是核心挑战，而优秀的架构设计是应对复杂性的最佳工具。
