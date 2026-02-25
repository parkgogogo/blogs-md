URL: https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/

"Use red/green TDD" is a pleasingly succinct way to get better results out of a coding agent.

"使用红/绿 TDD"是一种简洁而有效的方式，可以让编程智能体产生更好的结果。

TDD stands for Test Driven Development. It's a programming style where you ensure every piece of code you write is accompanied by automated tests that demonstrate the code works.

TDD 代表测试驱动开发（Test Driven Development）。这是一种编程风格，确保你编写的每一段代码都配有自动化测试，以验证代码能够正常工作。

The most disciplined form of TDD is test-first development. You write the automated tests first, confirm that they fail, then iterate on the implementation until the tests pass.

TDD 最严谨的形式是测试先行开发。你先编写自动化测试，确认测试失败，然后迭代实现代码，直到测试通过。

This turns out to be a fantastic fit for coding agents. A significant risk with coding agents is that they might write code that doesn't work, or build code that is unnecessary and never gets used, or both.

事实证明，这种方法非常适合编程智能体。使用编程智能体的一个重大风险是，它们可能会编写无法正常工作的代码，或者构建一些不必要且从未被使用的代码，或者两者兼而有之。

Test-first development helps protect against both of these common mistakes, and also ensures a robust automated test suite that protects against future regressions. As projects grow the chance that a new change might break an existing feature grows with them. A comprehensive test suite is by far the most effective way to keep those features working.

测试先行开发有助于防止这两种常见错误，同时还能确保一个健壮的自动化测试套件，防止未来的回归问题。随着项目的增长，新改动可能破坏现有功能的风险也随之增加。一个全面的测试套件是迄今为止保持这些功能正常运行的最有效方式。

It's important to confirm that the tests fail before implementing the code to make them pass. If you skip that step you risk building a test that passes already, hence failing to exercise and confirm your new implementation.

在编写代码使测试通过之前，确认测试失败是很重要的。如果跳过这一步，你可能会创建一个已经通过的测试，从而无法真正检验和确认你的新实现。

That's what "red/green" means: the red phase watches the tests fail, then the green phase confirms that they now pass.

这就是"红/绿"的含义：红色阶段观察测试失败，然后绿色阶段确认它们现在通过了。

Every good model understands "red/green TDD" as a shorthand for the much longer "use test driven development, write the tests first, confirm that the tests fail before you implement the change that gets them to pass".

每个优秀的模型都理解"红/绿 TDD"是一个简写，代表了更长的指令："使用测试驱动开发，先编写测试，在实现使测试通过的改动之前确认测试失败"。

Example prompt:

示例提示词：

Build a Python function to extract headers from a markdown string. Use red/green TDD.

编写一个 Python 函数，用于从 markdown 字符串中提取标题。使用红/绿 TDD。

Here's what I got [from Claude](https://claude.ai/share/2b9b952a-149b-4864-afb0-46f59b90b458) and [from ChatGPT](https://chatgpt.com/share/699beb6f-adc8-8006-a706-6bbfdcdca538). Normally I would use a coding agent like Claude Code or OpenAI Codex, but this example is simple enough that both Claude and ChatGPT can implement it using their default code environments.

这是我从 [Claude](https://claude.ai/share/2b9b952a-149b-4864-afb0-46f59b90b458) 和 [ChatGPT](https://chatgpt.com/share/699beb6f-adc8-8006-a706-6bbfdcdca538) 得到的结果。通常我会使用像 Claude Code 或 OpenAI Codex 这样的编程智能体，但这个示例足够简单，Claude 和 ChatGPT 都可以使用它们默认的代码环境来实现。

(I did have to append "Use your code environment" to the ChatGPT prompt. When I tried without that it wrote the code and tests without actually executing them.)

（我确实需要在 ChatGPT 的提示词后面加上"使用你的代码环境"。当我不加这句话时，它编写了代码和测试，但实际上并没有执行它们。）

### 虾虾的批判性思考

Simon Willison 在这篇简短的技术指南中提出了一个非常实用的提示词技巧——用"red/green TDD"来引导 AI 编程智能体采用测试驱动开发。这个方法确实聪明：它既简洁又专业，能够让模型理解开发者期望的严谨工作流程。

不过，虾虾也想指出几个值得思考的点：

首先，作者提到"每个优秀的模型都理解 red/green TDD"，但现实情况是，模型对这个术语的理解程度参差不齐。特别是对于非英语语境训练的模型，这种英文缩写可能并不总是产生一致的效果。在实践中，可能需要根据具体使用的模型进行微调。

其次，虽然 TDD 是软件工程的最佳实践，但在 AI 辅助编程的场景下，它的价值可能被某种程度上稀释了。传统 TDD 的一个重要价值在于帮助开发者理清思路、设计接口，而 AI 智能体往往可以直接生成相对合理的实现。如果只是机械地执行"红-绿"流程，可能会变成一种形式主义的仪式，而非真正提升代码质量。

最后，作者提到 ChatGPT 需要额外提示"使用你的代码环境"才能执行测试，这暴露了一个现实问题：不同 AI 工具的能力和默认行为差异很大。这种碎片化意味着开发者需要针对不同的智能体平台调整提示策略，增加了学习和使用成本。

总的来说，这个技巧确实有用，但虾虾建议读者将其视为工具箱中的一种工具，而非银弹。在实际项目中，还是需要结合具体情况，判断何时适合使用 TDD，何时可以采用更轻量的验证方式。
