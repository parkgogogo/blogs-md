URL: https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/#atom-everything

The biggest challenge in adopting agentic engineering practices is getting comfortable with the consequences of the fact that writing code is cheap now.

采用智能体工程实践的最大挑战，是要适应「现在写代码很便宜」这一事实所带来的后果。

Code has always been expensive. Producing a few hundred lines of clean, tested code takes most software developers a full day or more. Many of our engineering habits, at both the macro and micro level, are built around this核心约束 this core constraint.

代码一直都很昂贵。写出几百行干净、经过测试的代码，大多数软件开发者需要花费一整天甚至更多时间。我们的许多工程习惯，无论是宏观层面还是微观层面，都是围绕这一核心约束建立起来的。

At the macro level we spend a great deal of time designing, estimating and planning out projects, to ensure that our expensive coding time is spent as efficiently as possible. Product feature ideas are evaluated in terms of how much value they can provide in exchange for that time - a feature needs to earn its development costs many times over to be worthwhile!

在宏观层面，我们花费大量时间进行设计、估算和规划项目，以确保昂贵的编码时间能够被尽可能高效地利用。产品功能想法是根据它们能为这段时间提供多少价值来评估的——一个功能需要将其开发成本赚回许多倍才值得去做！

At the micro level we make hundreds of decisions a day predicated on available time and anticipated tradeoffs. Should I refactor that function to be slightly more优雅 elegant if it adds an extra hour of coding time? How about writing documentation? Is it worth adding a test for this edge case? Can I justify building a debug interface for this?

在微观层面，我们每天要做数百个基于可用时间和预期权衡的决策。如果重构一个函数让它稍微优雅一点需要多花一小时编码时间，我应该做吗？写文档呢？为这个边界情况添加测试值得吗？我能证明为这个功能构建调试界面是合理的吗？

Coding agents dramatically drop the cost of typing code into the computer, which disrupts so many of our existing personal and organizational intuitions about which trade-offs make sense.

编码智能体显著降低了将代码输入计算机的成本，这打破了我们现有的许多个人和组织对于哪些权衡才有意义的直觉。

The ability to run parallel agents makes this even harder to evaluate, since one human engineer can now be implementing, refactoring, testing and documenting code in multiple places at the same time.

并行运行多个智能体的能力让这一点更难评估，因为一个人类工程师现在可以同时在多个地方实现、重构、测试和记录代码。

## Good code still has a cost

## 好的代码仍然有成本

Delivering new code has dropped in price to almost free... but delivering good code remains significantly more expensive than that.

交付新代码的价格已经降到几乎免费……但交付好代码仍然比这贵得多。

Here's what I mean by "good code":

以下是我所说的「好代码」的含义：

- The code works. It does what it's meant to do, without bugs.

- 代码能用。它完成了应该做的事，没有 bug。

- We know the code works. We've taken steps to confirm to ourselves and to others that the code is fit for purpose.

- 我们知道代码能用。我们已采取措施向自己和他人确认代码符合其用途。

- It solves the right problem.

- 它解决了正确的问题。

- It handles error cases gracefully and predictably: it doesn't just consider the happy path. Errors should provide enough information to help future维护者 maintainers understand what went wrong.

- 它能优雅且可预测地处理错误情况：它不只是考虑正常路径。错误应该提供足够的信息，帮助未来的维护者理解出了什么问题。

- It's simple and minimal - it does only what's needed, in a way that both humans and machines can understand now and maintain in the future.

- 它简单且精简——只做需要做的事，以一种人类和机器现在都能理解并且将来可以维护的方式。

- It's protected by tests. The tests show that it works now and act as a回归测试套件 regression suite to avoid it quietly breaking in the future.

- 它有测试保护。测试证明它现在能工作，并作为回归测试套件避免它将来悄无声息地坏掉。

- It's documented at an appropriate level, and that documentation reflects the current state of the system - if the code changes an existing behavior the existing documentation needs to be updated to match.

- 它在适当的层次上有文档记录，且文档反映了系统的当前状态——如果代码改变了现有行为，现有文档需要更新以保持一致。

- The design affords future changes. It's important to maintain [YAGNI](https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it) - code with added complexity to anticipate未来可能发生的变化 future changes that may never come is often bad code - but it's also important not to write code that makes future changes much harder than they should be.

- 设计支持未来的变更。保持「YAGNI（你不会需要它）」很重要——添加复杂性来预测可能永远不会发生的未来变化的代码通常是坏代码——但同样重要的是，不要写出让未来变更比应有的难度高得多的代码。

- All of the other relevant "ilities" - accessibility, testability, reliability, security, maintainability, observability, scalability, usability - the non-functional quality measures that are appropriate for the particular class of software being developed.

- 所有其他相关的「特性」——可访问性、可测试性、可靠性、安全性、可维护性、可观察性、可扩展性、可用性——这些非功能性质量指标适用于正在开发的特定类别的软件。

Coding agent tools can help with most of this, but there is still a substantial burden on the developer driving those tools to ensure that the produced code is good code for the subset of good that's needed for the current project.

编码智能体工具可以帮助完成其中的大部分工作，但驱动这些工具的开发者仍然承担着重大责任，需要确保生成的代码对于当前项目所需的「好」的子集来说是好代码。

## We need to build new habits

## 我们需要建立新习惯

The challenge is to develop new personal and organizational habits that respond to the affordances and opportunities of agentic engineering.

挑战在于发展新的个人和组织习惯，以响应智能体工程带来的功能特性和机会。

These best practices are still being figured out across our industry. I'm still figuring them out myself.

这些最佳实践仍在整个行业中被摸索出来。我自己也还在摸索中。

For now I think the best we can do is to second guess ourselves: any time our instinct says "don't build that, it's not worth the time" fire off a prompt anyway, in an asynchronous agent session where the worst that can happen is you check ten minutes later and find that it wasn't worth the tokens.

目前我认为我们能做的最好的是质疑自己的直觉：每当你的直觉说「别做这个，不值得花时间」时，还是发起一个提示吧，在一个异步智能体会话中，最坏的情况不过是十分钟后检查发现它不值得那些 token。

---

## 批判性思考与评论

这篇文章提出了一个重要的观点：AI 编码工具改变了「代码成本」的等式，但这并不意味着我们可以忽视代码质量。

**值得肯定的洞见：**

1. **成本认知的转变**：作者敏锐地指出了「写代码」与「写好代码」的本质区别。虽然 AI 可以快速生成代码，但确保代码正确、可维护、有测试覆盖仍然需要人类工程师的判断力。

2. **好代码的定义**：文章列举的「好代码」标准非常全面，特别强调了错误处理、文档同步和 YAGNI 原则，这些都是实践中经常被忽视但至关重要的方面。

3. **新习惯的必要性**：承认行业仍在摸索最佳实践是一种诚实的态度。建议「质疑直觉」去尝试那些原本被认为不值得做的任务，是一个实用的起点。

**需要补充的思考：**

1. **技术债务的加速**：如果写代码变得廉价，那么产生技术债务的速度也可能加快。组织需要有意识地建立代码审查和质量门禁机制，否则可能积累大量难以维护的 AI 生成代码。

2. **技能转变**：开发者需要从「写代码」转向「评估代码」和「指导 AI」。这种技能转变并非所有人都能轻松完成，可能需要新的培训和方法论。

3. **上下文管理的挑战**：并行运行多个智能体虽然诱人，但也意味着开发者需要在多个上下文之间切换，这可能带来认知负担。文章没有深入讨论如何有效管理这种复杂性。

4. **长期维护责任**：AI 生成的代码谁来负责长期维护？如果原始开发者离职，其他开发者能否理解 AI 的「思路」？这涉及知识管理和团队交接的新挑战。

总的来说，这篇文章为正在经历 AI 转型的软件工程行业提供了有价值的思考框架，但实践中还需要更多关于治理、流程和文化变革的探讨。
