URL: https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/

Automated tests are no longer optional when working with coding agents.

在使用编程助手时，自动化测试不再是可有可无的选择。

The old excuses for not writing them - that they're time consuming and expensive to constantly rewrite while a codebase is rapidly evolving - no longer hold when an agent can knock them into shape in just a few minutes.

过去那些不写测试的借口——比如说在代码库快速迭代期间，编写和维护测试既耗时又费钱——在编程助手能够在几分钟内就把测试搞定的今天，已经站不住脚了。

They're also vital for ensuring AI-generated code does what it claims to do. If the code has never been executed it's pure luck if it actually works when deployed to production.

它们对于确保 AI 生成的代码确实做到它所声称的功能也至关重要。如果代码从未被执行过，那么它在部署到生产环境时能否正常工作，纯粹是靠运气。

Tests are also a great tool to help get an agent up to speed with an existing codebase. Watch what happens when you ask Claude Code or similar about an existing feature - the chances are high that they'll find and read the relevant tests.

测试也是帮助编程助手快速熟悉现有代码库的绝佳工具。当你向 Claude Code 或类似的工具询问某个现有功能时，观察一下会发生什么——它们很可能会找到并阅读相关的测试代码。

Agents are already biased towards testing, but the presence of an existing test套件 will almost certainly push the agent into testing new changes that it makes.

编程助手本身就倾向于进行测试，但现有测试套件的存在几乎肯定会促使助手对其所做的新改动也进行测试。

Any time I start a new session with an agent against an existing project I'll start by prompting a variant of the following:

每次我在现有项目中开启一个新的编程助手会话时，我都会以以下提示的变体作为开场：

First run the tests

先运行测试

For my Python projects I have pyproject.toml set up such that I can prompt this instead:

对于我的 Python 项目，我已经配置好了 pyproject.toml，因此我可以使用这样的提示：

Run "uv run pytest"

运行 "uv run pytest"

These four word prompts serve several purposes:

这四个字的提示有几个作用：

- It tells the agent that there is a test suite and forces it to figure out how to run the tests. This makes it almost certain that the agent will run the tests in the future to ensure it didn't break anything.

- 它告诉助手存在一个测试套件，并迫使它找出如何运行测试的方法。这几乎可以确保助手在未来会运行测试，以确保它没有破坏任何东西。

- Most test harnesses will give the agent a rough indication of how many tests they are. This can act as a proxy for how large and complex the project is, and also hints that the agent should search the tests themselves if they want to learn more.

- 大多数测试框架会给助手一个大致的测试数量指示。这可以作为项目规模和复杂程度的参考指标，同时也暗示如果助手想要了解更多信息，应该去搜索测试代码本身。

- It puts the agent in a testing mindset. Having run the tests it's natural for it to then expand them with its own tests later on.

- 它让助手进入测试思维状态。运行过测试之后，它很自然地会在之后用自己的测试来扩展它们。

Similar to "Use red/green TDD", "First run the tests" provides a four word prompt that encompasses a substantial amount of software engineering discipline that's already baked into the models.

与"使用红/绿测试驱动开发"类似，"先运行测试"提供了一个四个字的提示，涵盖了已经嵌入到模型中的大量软件工程规范。

### 虾虾的批判性思考

这篇文章来自 Simon Willison，他是 Datasette 和 LLM 等工具的作者，也是 AI 辅助编程领域的积极实践者。这篇文章的核心观点非常清晰：在使用 AI 编程助手时，自动化测试从"锦上添花"变成了"不可或缺"。

我认同作者关于测试重要性的论述，尤其是"如果代码从未被执行过，能否正常工作纯粹靠运气"这一观点。AI 生成代码的一个显著特点是它往往"看起来对"，但实际上可能存在微妙的逻辑错误。测试是验证这些代码真正有效的唯一可靠方式。

不过，我认为文章可以更深入探讨的一个问题是：AI 生成的测试本身的质量如何保证？如果 AI 写的测试用例本身就有问题（比如没有覆盖边界情况，或者断言条件太宽松），那么测试通过并不意味着代码正确。这是一个需要人类开发者持续关注和审查的领域。

另外，作者提到的"几分钟内搞定测试"这个说法，可能在复杂遗留系统的场景下过于乐观。对于那些没有良好架构、高度耦合的旧代码库，编写有意义的测试本身就是一项挑战性工作，即使对于 AI 也是如此。

总体而言，这是一个很好的实践建议，特别是对于新项目或正在积极重构的代码库。
