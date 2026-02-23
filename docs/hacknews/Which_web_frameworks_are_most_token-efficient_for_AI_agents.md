URL: https://martinalderson.com/posts/which-web-frameworks-are-most-token-efficient-for-ai-agents/

## Which web frameworks are most token-efficient for AI agents?

哪些 Web 框架对 AI 智能体最具 token 效率？

I wrote an article a couple of months ago about which languages are the [most token efficient](https://martinalderson.com/posts/which-programming-languages-are-most-token-efficient/). I've been thinking about this for quite a while - and many others have too, thinking through what happens to programming languages now increasingly agents are writing code, not humans.

几个月前，我写了一篇关于[哪些编程语言最具 token 效率](https://martinalderson.com/posts/which-programming-languages-are-most-token-efficient/)的文章。这个问题我已经思考了相当长一段时间——许多人也在思考，在智能体 increasingly 编写代码而非人类的今天，编程语言会发生什么变化。

However, it did occur to me that maybe this is the wrong angle to look at the question. These days, frameworks tend to matter far more than the language itself, so I thought I'd see if I could repeat the previous research by looking at what web frameworks were the most efficient.

然而，我突然想到，也许这个问题的角度是错误的。如今，框架往往比语言本身重要得多，所以我想看看能否通过研究哪些 Web 框架最有效率来重复之前的研究。

## Methodology

方法论

This isn't a hugely scientific approach - but I suspect it is directionally correct and maps to my own experience with various web frameworks.

这不是一个非常科学的方法——但我怀疑它在方向上是正确的，并且与我使用各种 Web 框架的经验相符。

I chose 19 different frameworks that I'm somewhat familiar with (some far more than others), and asked Claude Code w/ Opus 4.6 in a fresh context window with a prompt along these lines, slightly modifying it for each one. It was pretty much identical apart from framework specific libraries and setup (I wanted to focus more on its ability to code in the framework, rather than burning tokens choosing libraries that may not be installed on the system).

我选择了 19 个我比较熟悉的框架（有些比其他的熟悉得多），在一个全新的上下文窗口中使用 Claude Code + Opus 4.6，使用类似这样的提示词，对每个框架稍作修改。除了框架特定的库和设置外，提示词几乎完全相同（我想更多地关注它在框架中编码的能力，而不是浪费 token 去选择可能未安装在系统上的库）。

Build a simple blog app using Express.js with EJS templates. It should have:
 1. A home page listing blog posts (title, date, excerpt)
 2. A post detail page showing the full post content
 3. A create post page with a form (title, body) that saves the post
 4. SQLite for persistent storage (use better-sqlite3)
 5. Basic CSS styling - make it look presentable, not raw HTML

使用 Express.js 和 EJS 模板构建一个简单的博客应用。它应该包括：
 1. 一个首页，列出博客文章（标题、日期、摘要）
 2. 一个文章详情页，显示完整内容
 3. 一个创建文章页面，带有表单（标题、正文）来保存文章
 4. 使用 SQLite 进行持久化存储（使用 better-sqlite3）
 5. 基本的 CSS 样式——让它看起来体面，而不是原始 HTML

## Results

结果

The first thing to point out was how good the results were in every single environment. Every single one produced a working blog with no obvious bugs. While this is obviously a very simple prompt, they all figured out how to run the server, install any packages they needed, start the server and tested it worked. It astonishes me how far we've come in a year in agentic development - I think it would have been impressive if even one of these experiments worked out of the box back then.

首先要指出的是，在每个环境中结果都非常好。每一个都生成了一个可以正常工作的博客，没有明显的 bug。虽然这显然是一个非常简单的提示，但它们都想出了如何运行服务器、安装所需的任何包、启动服务器并测试它是否工作。这让我惊讶于我们在智能体开发方面一年内取得的进步——我想如果当时这些实验中哪怕有一个能开箱即用，都会令人印象深刻。

Very clear pattern on minimal frameworks being very token efficient. ASP.NET Minimal API was the cheapest at 26k tokens, while Phoenix was the most expensive at 74k - a 2.9x gap. The minimal frameworks all clustered tightly between 26-29k tokens, while the full featured ones spread from 28k (SvelteKit) all the way up to 74k.

极简框架在 token 效率方面表现出非常明显的模式。ASP.NET Minimal API 最便宜，仅需 26k token，而 Phoenix 最贵，需要 74k——差距达 2.9 倍。极简框架都紧密聚集在 26-29k token 之间，而全功能框架则从 28k（SvelteKit）一直 spread 到 74k。

---

**批判性思考评论：**

这项研究揭示了一个被忽视但至关重要的趋势：在 AI 智能体时代，框架的选择标准正在发生变化。传统上我们选择框架基于性能、生态系统或开发者体验，但现在"token 效率"成为新的关键指标。

极简框架（如 Express.js、Flask、Go 的 net/http）在 token 效率上胜出，这并不令人意外——它们的 API 表面更小，概念更少，智能体需要"记住"的东西就更少。但有趣的问题是：这种效率优势会随着项目复杂度增加而持续吗？

对于全功能框架，SvelteKit 的表现出人意料地好（28k token），接近极简框架的水平。这可能反映了 Svelte 的设计哲学：较少的样板代码，更直观的 API。相比之下，Phoenix 的 74k token 消耗令人震惊，作者推测是因为训练数据不足导致智能体需要阅读更多脚手架代码。

这个研究对 AI 原生开发工具的设计有重要启示：未来的框架可能需要针对"智能体友好性"进行优化，而不仅仅是人类开发者友好性。
