URL: https://martinalderson.com/posts/which-web-frameworks-are-most-token-efficient-for-ai-agents/

I wrote an article a couple of months ago about which languages are the [most token efficient](https://martinalderson.com/posts/which-programming-languages-are-most-token-efficient/). I've been thinking about this for quite a while - and many others have too, thinking through what happens to programming languages now increasingly agents are writing code, not humans.

几个月前，我写了一篇关于哪些编程语言[token效率最高](https://martinalderson.com/posts/which-programming-languages-are-most-token-efficient/)的文章。这个问题我已经思考了相当长一段时间——其他人也是如此，都在思考现在越来越多的代码是由AI智能体而非人类编写时，编程语言会发生什么变化。

However, it did occur to me that maybe this is the wrong angle to look at the question. These days, frameworks tend to matter far more than the language itself, so I thought I'd see if I could repeat the previous research by looking at what web frameworks were the most efficient.

然而，我突然想到，也许这不是看待这个问题的正确角度。如今，框架往往比语言本身重要得多，所以我想看看能否通过研究哪些Web框架效率最高来重复之前的研究。

## Methodology

## 研究方法

This isn't a hugely scientific approach - but I suspect it is directionally correct and maps to my own experience with various web frameworks.

这并不是一个非常科学的方法——但我怀疑它在方向上是正确的，并且与我使用各种Web框架的经验相符。

I chose 19 different frameworks that I'm somewhat familiar with (some far more than others), and asked Claude Code w/ Opus 4.6 in a fresh context window with a prompt along these lines, slightly modifying it for each one. It was pretty much identical apart from framework specific libraries and setup (I wanted to focus more on its ability to code in the framework, rather than burning tokens choosing libraries that may not be installed on the system).

我选择了19个我比较熟悉的框架（有些比其他熟悉得多），并在全新的上下文窗口中使用Claude Code（Opus 4.6版本），对每个框架使用类似下面这样的提示词，稍作修改。除了框架特定的库和设置之外，提示词几乎完全相同（我更想关注它在框架中编写代码的能力，而不是浪费token去选择可能未安装在系统上的库）。

I also installed the main packages that each language needed, so the agent had npm, nodejs, go, cargo, etc preinstalled.

我还安装了每种语言所需的主要包，因此智能体已经预先安装了npm、nodejs、go、cargo等。

Build a simple blog app using Express.js with EJS templates. It should have:
 1. A home page listing blog posts (title, date, excerpt)
 2. A post detail page showing the full post content
 3. A create post page with a form (title, body) that saves the post
 4. SQLite for persistent storage (use better-sqlite3)
 5. Basic CSS styling - make it look presentable, not raw HTML

使用Express.js和EJS模板构建一个简单的博客应用。它应该包含：
 1. 一个首页，列出博客文章（标题、日期、摘要）
 2. 一个文章详情页，显示完整的文章内容
 3. 一个创建文章页面，带有表单（标题、正文）用于保存文章
 4. 使用SQLite进行持久化存储（使用better-sqlite3）
 5. 基本的CSS样式——让它看起来体面，而不是原始的HTML

 Run it on port 3003. Initialize with `npm init -y`, then install express, ejs,
 and better-sqlite3. When done, start the server and confirm it works by curling
 the home page. Leave the server running.

在3003端口运行。使用`npm init -y`初始化，然后安装express、ejs和better-sqlite3。完成后，启动服务器并通过curl访问首页来确认它正常工作。保持服务器运行。

 Work in the current directory. Do not create a subdirectory - use the repo root
 as the project root.

在当前目录下工作。不要创建子目录——使用仓库根目录作为项目根目录。

I then left it running with it being allowed to do common read/write commands and use e.g. npm (or similar for the other ecosystems). Once they had completed I counted the number of tool calls, tokens, time elapsed and also checked that the server they started was running correctly and we had a blog presented with the specification.

然后我让它继续运行，允许它执行常见的读/写命令并使用例如npm（或其他生态系统的类似工具）。完成后，我统计了工具调用次数、token数量、经过的时间，并检查它们启动的服务器是否正常运行，以及我们是否按照规范获得了一个博客应用。

## Results

## 结果

The first thing to point out was how good the results were in every single environment. Every single one produced a working blog with no obvious bugs. While this is obviously a very simple prompt, they all figured out how to run the server, install any packages they needed, start the server and tested it worked. It astonishes me how far we've come in a year in agentic development - I think it would have been impressive if even one of these experiments worked out of the box back then.

首先要指出的是，在每个环境中结果都非常好。每一个都生成了一个可以正常工作的博客，没有明显的bug。虽然这显然是一个非常简单的提示词，但它们都弄清楚了如何运行服务器、安装所需的任何包、启动服务器并测试它是否工作。智能体开发在一年内取得的进步让我惊讶——我认为，如果当时这些实验中哪怕有一个能开箱即用，那都会令人印象深刻。

I've grouped the frameworks in two categories:

我将框架分为两类：

- Minimal - web frameworks that are designed to be very small and don't tend to come with much functionality out of the box (think Express or Flask)

- 极简型——设计得非常小巧的Web框架，开箱即用功能不多（比如Express或Flask）

- Full featured - bigger frameworks that tend to be far more opinionated and include a lot more functionality (Rails or Django).

- 全功能型——更大的框架，往往更有主见，包含更多功能（如Rails或Django）。

Very clear pattern on minimal frameworks being very token efficient. ASP.NET Minimal API was the cheapest at 26k tokens, while Phoenix was the most expensive at 74k - a 2.9x gap. The minimal frameworks all clustered tightly between 26-29k tokens, while the full featured ones spread from 28k (SvelteKit) all the way up to 74k.

极简框架在token效率方面呈现出非常明显的模式。ASP.NET Minimal API最便宜，仅需26k token，而Phoenix最贵，需要74k——差距达2.9倍。极简框架都集中在26-29k token之间，而全功能型则从28k（SvelteKit）一直延伸到74k。

SvelteKit and Django stood out to me as the most efficient of the full featured ones. Phoenix was very interesting, it spent an awful lot of tokens reading the scaffolded code - I suspect it just didn't have much in its training data so decided to read much more of the scaffolding output.

SvelteKit和Django在我看来是全功能框架中效率最高的。Phoenix非常有趣，它花了大量的token来阅读脚手架代码——我怀疑它只是训练数据中没有太多相关内容，所以决定多读一些脚手架输出。

Similar pattern on tool calls - though there is definitely a pattern emerging that more esoteric frameworks tend to require more effort on the part of the agent.

工具调用也呈现出类似的模式——尽管确实出现了一个模式，即更冷门的框架往往需要更多的智能体努力。

## Follow up task

## 后续任务

While I thought this was interesting, I thought it'd be more interesting to then look at adding a feature to see how that changes things. As such I resumed each agent (the context of the build still in the context window) and sent this prompt:

虽然我觉得这很有趣，但我认为看看添加一个功能会如何改变情况会更有趣。因此，我恢复了每个智能体（构建的上下文仍在上下文窗口中）并发送了以下提示词：

Add categories to the blog app. Each post belongs to one category. Specifically:
 1. Add a categories table with a name field
 2. Pre-seed 4 categories: Technology, Travel, Food, General
 3. Update the create post form with a category dropdown
 4. Show the category on the home page listing and post detail page
 5. Add a filter on the home page to view posts by category
Restart the server when done and verify it works by curling the home page.

为博客应用添加分类功能。每篇文章属于一个分类。具体要求：
 1. 添加一个categories表，包含name字段
 2. 预先填充4个分类：Technology、Travel、Food、General
 3. 更新创建文章表单，添加分类下拉菜单
 4. 在首页列表和文章详情页显示分类
 5. 在首页添加按分类筛选文章的功能
完成后重启服务器，并通过curl访问首页验证它是否正常工作。

Interestingly, Spring Boot resulted in a broken app - migrations didn't get run correctly - though if they were, then it'd have worked fine. Apart from that, all of the agents implemented this successfully. Again, 18/19 following prompts so well was very interesting to me - I again did not expect such a high success rate across such a variety of frameworks and生态系统中。

有趣的是，Spring Boot导致应用损坏——迁移没有正确运行——但如果运行了，它应该可以正常工作。除此之外，所有智能体都成功实现了这个功能。同样，19个中有18个如此好地遵循了提示词，这对我来说非常有趣——我再一次没有预料到在如此多样化的框架和生态系统中会有如此高的成功率。

The follow-up did not have as much impact as I expected. Go stdlib really struggled (burnt through so many tool calls because of a problem with datetime parsing trying to upgrade the database). I was expecting to see the fully featured frameworks be far more efficient at features than the minimal ones - they'd already done all the "DRY" stuff, but this doesn't seem to be the case. Most frameworks landed in a 15-30k token band for the follow-up regardless of their initial build cost. The framework overhead hits you on the first build, but extending existing code的成本在各种框架中大致相同。

后续任务的影响没有我预期的那么大。Go标准库确实很挣扎（因为datetime解析问题试图升级数据库而消耗了大量工具调用）。我本来期望看到全功能框架在添加功能方面比极简框架效率高得多——它们已经完成了所有的"DRY"（不要重复自己）工作，但似乎并非如此。无论初始构建成本如何，大多数框架在后续任务中都落在了15-30k token的范围内。框架开销在第一次构建时影响你，但扩展现有代码的成本在各种框架中大致相同。

## Conclusions

## 结论

Minimal API web frameworks are far quicker and more cost effective for agents to work with. This is just a starting point - ideally I'd rerun each agent many times and try a much more complex project - but the direction is clear.

极简API Web框架让智能体工作起来更快、更具成本效益。这只是一个起点——理想情况下，我会多次重新运行每个智能体并尝试一个更复杂的项目——但方向是明确的。

This shouldn't be a real surprise - they are for humans too. But the delta was bigger than I expected.

这不应该是一个真正的惊喜——对人类来说也是如此。但差距比我预期的要大。

Having said that - all of the agents did get working software, even out of the quite esoteric ones. My main takeaway from this isn't actually about efficiency - it really shows that agents can build software with any框架 you throw at them. If you are building a very quick and dirty app that needs a web interface though, it's probably better to use a minimal API framework. ASP.NET Minimal really shines here - it's statically typed and very fast to run, with low memory use.

话虽如此——所有智能体都生成了可以工作的软件，即使是那些相当冷门的框架也是如此。我从这得到的主要收获实际上与效率无关——它真正展示的是智能体可以用你扔给它们的任何框架来构建软件。然而，如果你正在构建一个需要Web界面的快速粗糙应用，使用极简API框架可能更好。ASP.NET Minimal在这里真的很出色——它是静态类型的，运行速度非常快，内存使用也很低。

In terms of more fully featured frameworks SvelteKit and Django really shine - this doesn't surprise me as they're both extremely well thought through web frameworks.

就功能更全面的框架而言，SvelteKit和Django真的很出色——这并不让我感到惊讶，因为它们都是经过深思熟虑的Web框架。

A 2.9x token gap doesn't matter much on a single task. It matters a lot when agents are building and modifying code hundreds of times a day.

在单个任务上，2.9倍的token差距无关紧要。但当智能体每天数百次构建和修改代码时，这就很重要了。

---

**Footnotes | 脚注：**

- I felt this was more representative of how a developer may have their system set up than pure yolo mode.

- 我觉得这更能代表开发者设置系统的方式，而不是纯YOLO模式。

- In the interests of transparency, I did have to rerun Rails and Laravel as it got completely stuck with various missing system packages. I felt this was fair as in the real world you wouldn't have missing system packages like it did here, but it was interesting to me that these popular frameworks gave the agents the most confusion trying to get them up and running.

- 为了透明起见，我确实不得不重新运行Rails和Laravel，因为它们因为各种缺少的系统包而完全卡住了。我觉得这是公平的，因为在现实世界中你不会像这里那样缺少系统包，但有趣的是，这些流行的框架让智能体在尝试启动和运行时最困惑。

---

## 批判性思考与评论

这篇文章提供了一个有趣的实证研究，探讨了AI智能体在不同Web框架下的token效率问题。以下是几点值得思考的观察：

**1. 研究方法的局限性**

作者自己也承认这不是" hugely scientific approach"。样本量小（每个框架只测试一次）、任务相对简单（博客应用），这些限制了结论的普适性。特别是Phoenix花费大量token阅读脚手架代码，可能更多反映了训练数据的偏差，而非框架本身的复杂性。

**2. 长期维护成本的考量**

文章提到"扩展现有代码的成本在各种框架中大致相同"，这与软件工程直觉相悖。全功能框架的DRY原则和约定优于配置理念，在大型项目中应该显现优势。也许需要更复杂的后续任务才能看出差异。

**3. 框架选择的权衡**

虽然极简框架在token效率上占优，但实际项目中还需考虑：团队熟悉度、生态系统成熟度、长期维护性、安全性等因素。ASP.NET Minimal API虽然效率高，但.NET生态的学习曲线不容忽视。

**4. AI时代的编程范式转变**

最深刻的启示可能是：当AI成为主要编码者时，人类程序员的角色将转向架构设计、需求澄清和代码审查。框架的"人类可读性"可能变得不那么重要，而"机器可预测性"（convention over configuration）可能更加关键。

**5. 对开发者的实际建议**

对于快速原型或一次性脚本，极简框架确实更合适。但对于需要长期维护的生产系统，全功能框架（如Django、Rails）的内置最佳实践和安全机制可能更值得那额外的token开销。关键是根据项目生命周期做出明智选择。
