# Automatic Programming

> 原文链接：http://antirez.com/news/159  
> 作者：antirez (Redis 作者)  
> 日期：2025年2月

---

In my YouTube channel, for some time now I started to refer to the process of writing software using AI assistance (soon to become just "the process of writing software", I believe) with the term "Automatic Programming".

在我的 YouTube 频道中，一段时间以来，我开始使用"自动编程"（Automatic Programming）这个术语来指代使用 AI 辅助编写软件的过程——我相信，这很快将会成为"编写软件"本身的标准定义。

---

In case you didn't notice, automatic programming produces vastly different results with the same LLMs depending on the human that is guiding the process with their intuition, design, continuous steering and idea of software.

如果你还没有注意到，自动编程即使使用相同的大型语言模型，也会产生截然不同的结果——这取决于指导这个过程的人，取决于他们的直觉、设计能力、持续的引导方向以及对软件的理解。

---

Please, stop saying "Claude vibe coded this software for me". Vibe coding is the process of generating software using AI without being part of the process at all. You describe what you want in very general terms, and the LLM will produce whatever happens to be the first idea/design/code it would spontaneously, given the training, the specific sampling that happened to dominate in that run, and so forth. The vibe coder will, at most, report things not working or not in line with what they expected.

请不要再这样说："Claude 用氛围编码帮我写了这个软件"。氛围编码（Vibe coding）是指在使用 AI 生成软件时，完全不参与这个过程本身。你用非常笼统的术语描述你想要什么，而 LLM 会根据其训练数据、该次运行中占主导地位的特定采样等因素，自发地产生它想到的第一个想法/设计/代码。氛围编码者最多只是报告某些功能不工作或不符合他们的预期。

---

When the process is actual software production where you know what is going on, remember: it is the software *you* are producing. Moreover remember that the pre-training data, while not the only part where the LLM learns (RL has its big weight) was produced by humans, so we are not appropriating something else. We can pretend AI generated code is "ours", we have the right to do so. Pre-training is, actually, our collective gift that allows many individuals to do things they could otherwise never do, like if we are now linked in a collective mind, in a certain way.

当这个过程是你在清楚了解发生什么的真正软件生产时，请记住：这是你*自己*在生产的软件。此外，请记住预训练数据——虽然这不是 LLM 学习的唯一部分（强化学习也占有重要权重）——是由人类产生的，所以我们并没有侵占他人的成果。我们可以认为 AI 生成的代码是"我们的"，我们有权利这样做。预训练实际上是我们集体的礼物，它让许多个人能够做他们本来永远无法做到的事情，就像在某种程度上我们现在连接在一个集体意识中一样。

---

That said, if vibe coding is the process of producing software without much understanding of what is going on (which has a place, and democratizes software production, so it is totally ok with me), automatic programming is the process of producing software that attempts to be high quality and strictly following the producer's vision of the software (this vision is multi-level: can go from how to do, exactly, certain things, at a higher level, to stepping in and tell the AI how to write a certain function), with the help of AI assistance. Also a fundamental part of the process is, of course, *what* to do.

话虽如此，如果氛围编码是在不太理解发生什么的情况下生产软件的过程（这自有其位置，并且使软件生产民主化，所以我完全认可），那么自动编程则是借助 AI 辅助，试图生产高质量软件并严格遵循生产者对软件愿景的过程（这个愿景是多层次的：可以从高层面上确切地知道如何做某些事情，到具体介入并告诉 AI 如何编写某个函数）。当然，这个过程的一个基本部分也是*做什么*。

---

I'm a programmer, and I use automatic programming. The code I generate in this way is mine. My code, my output, my production. I, and you, can be proud.

我是一名程序员，我使用自动编程。我以这种方式生成的代码是我的。我的代码，我的产出，我的作品。我，还有你，都可以为此感到自豪。

---

If you are not completely convinced, think to Redis. In Redis there is not much technical novelty, especially at its start it was just a sum of basic data structures and networking code that every competent system programmer could write. So, why it became a very useful piece of software? Because of the ideas and visions it contained.

如果你还不完全信服，想想 Redis。Redis 中并没有太多的技术新奇之处，尤其是在它刚起步时，它只是每个有能力的系统程序员都能编写的基本数据结构和网络代码的总和。那么，为什么它成为了一款非常有用的软件？因为它所包含的想法和愿景。

---

Programming is now automatic, vision is not (yet).

编程现在已经是自动的了，但愿景（还）不是。

---

## 批判性思考 🧠

### 1. 术语之争背后的权力话语

antirez 区分"自动编程"与"氛围编码"的尝试，本质上是在争夺对 AI 辅助编程的话语定义权。作为 Redis 的创造者，他的立场可以理解：当他说"我的代码，我的产出"时，他在捍卫的是程序员作为创造者的主体性。

但这种区分是否过于二元对立？现实中，大多数开发者可能处于两者之间的光谱上——既不是完全放手给 AI 的"氛围编码者"，也不是完全掌控每一个细节的"自动编程师"。

### 2. 关于"集体礼物"的乐观主义

antirez 将预训练数据称为"集体礼物"，这个观点既温暖又值得警惕。温暖之处在于它承认了开源社区和人类知识积累的价值；但警惕之处在于，这种修辞可能掩盖了训练数据的来源伦理问题——并非所有被用于训练的数据都是被"捐赠"的，也并非所有贡献者都真正同意他们的作品被如此使用。

"我们有权利声称 AI 生成的代码是我们的"——这个断言在法律和伦理层面都仍是一个开放的问题，而非定论。

### 3. Redis 类比的深意与局限

用 Redis 来说明"愿景重于实现"是一个强有力的例子。确实，Redis 的成功更多来自于 Salvatore Sanfilippo 对内存数据结构服务的清晰愿景，而非其底层代码的技术复杂性。

但这个类比也有局限：AI 辅助编程的"愿景"是否与 Redis 时代的愿景相同？当 AI 可以生成无数种实现方案时，选择哪一种、放弃哪一种，这种决策能力本身就是新的技能。antirez 所说的"直觉、设计、持续引导"，恰恰是这种新技能的核心。

### 4. 最后的断言：自动化的边界

"Programming is now automatic, vision is not (yet)."

这句话既是宣言，也是警示。它提醒我们：工具民主化不等于创造力民主化。当编码的技术门槛降低时，真正的区分度将来自于问题定义能力、系统思维、品味和判断力。

但"yet"这个词也留下了一丝不安——如果连愿景也能被自动化呢？如果 LLM 不仅能实现我们的想法，还能比我们更好地提出想法呢？那时候，程序员的主体性又将安身何处？

---

*翻译完成于 2026-02-25*
