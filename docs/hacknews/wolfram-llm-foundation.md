# Making Wolfram Tech Available as a Foundation Tool for LLM Systems
# 让 Wolfram 技术成为 LLM 系统的基础工具

**Source**: https://writings.stephenwolfram.com/2026/02/making-wolfram-tech-available-as-a-foundation-tool-for-llm-systems/  
**Author**: Stephen Wolfram  
**Publisher**: Stephen Wolfram Writings  
**Date**: February 23, 2026  
**Category**: AI/ML  
**Rating**: 9/10

---

## Summary / 摘要

Stephen Wolfram 宣布 Wolfram 技术作为 LLM 系统的"基础工具"(Foundation Tool)正式发布。这是一个重要里程碑——Wolfram Language 经过40年发展，现在可以作为 LLM 的"计算增强生成"(CAG, Computation-Augmented Generation)基础设施，为大语言模型提供精确计算和深度知识能力。文章介绍了三种主要接入方式：MCP Service、Agent One API 和 CAG Component APIs。

---

## Foundation Models Need a Foundation Tool / 基础模型需要基础工具

LLMs don't—and can't—do everything. What they do is very impressive—and useful. It's broad. And in many ways it's human-like. But it's not precise. And in the end it's not about deep computation.

大语言模型（LLM）并不能——也无法——做到所有事情。它们的表现确实令人印象深刻且实用，能力范围广泛，在很多方面也很像人类。但它们并不精确，归根结底也无法进行深度计算。

So how can we supplement LLM foundation models? We need a foundation tool: a tool that's broad and general and does what LLMs themselves don't: provides deep computation and precise knowledge.

那么，我们该如何补充 LLM 基础模型呢？我们需要一个基础工具：一个广泛而通用的工具，能够做 LLM 自身做不到的事情——提供深度计算和精确知识。

And, conveniently enough, that's exactly what I've been building for the past 40 years! My goal with Wolfram Language has always been to make everything we can about the world computable. To bring together in a coherent and unified way the algorithms, the methods and the data to do precise computation whenever it's possible. It's been a huge undertaking, but I think it's fair to say it's been a hugely successful one—that's fueled countless discoveries and inventions (including my own) across a remarkable range of areas of science, technology and beyond.

 Conveniently, I've been building exactly that for the past 40 years! My goal with Wolfram Language has always been to make as much of the world as possible computable — bringing together algorithms, methods, and data in a coherent, unified way to enable precise computation wherever possible. It's been an enormous undertaking, but I think it's fair to say it has been hugely successful, powering countless discoveries and innovations (including my own) across a remarkable range of scientific, technological, and other fields.

But now it's not just humans who can take advantage of this technology; it's AIs—and in particular LLMs—as well. LLM foundation models are powerful. But LLM foundation models with our foundation tool are even more so. And with the maturing of LLMs we're finally now in a position to provide to LLMs access to Wolfram tech in a standard, general way.

但如今，能够利用这项技术的不仅是人类，还有 AI——尤其是 LLM。LLM 基础模型本身很强大，但配备了我们的基础工具后，它们将变得更加强大。随着 LLM 技术的成熟，我们终于能够以标准、通用的方式让 LLM 接入 Wolfram 技术。

It is, I believe, an important moment of convergence. My concept over the decades has been to build very broad and general technology—which is now a perfect fit for the breadth of LLM foundation models. LLMs can call specific specialized tools, and that will be useful for plenty of specific specialized purposes. But what Wolfram Language uniquely represents is a general tool—with general access to the great power that precise computation and knowledge bring.

我相信，这是一个重要的融合时刻。我数十年来的理念一直是构建广泛而通用的技术——而这与 LLM 基础模型的广泛性完美契合。LLM 可以调用特定的专用工具，这对许多特定用途都很有帮助。但 Wolfram Language 独特之处在于它是一个通用工具，能够广泛地获取精确计算和知识带来的强大能力。

But there's actually also much more. I designed Wolfram Language from the beginning to be a powerful medium not only for doing computation but also for representing and thinking about things computationally. I'd always assumed I was doing this for humans. But it now turns out that AIs need the same things—and that Wolfram Language provides the perfect medium for AIs to "think" and "reason" computationally.

但实际上还有更多。我从一开始就将 Wolfram Language 设计为一种强大的媒介，不仅用于执行计算，还用于以计算方式表示和思考事物。我一直以为这是为人类而做的。但现在事实证明，AI 也需要同样的东西——而 Wolfram Language 为 AI 提供了"以计算方式思考和推理"的完美媒介。

There's another point as well. In its effort to make as much as possible computable, Wolfram Language not only has an immense amount inside, but also provides a uniquely unified hub for connecting to other systems and services. And that's part of why it's now possible to make such an effective connection between LLM foundation models and the foundation tool that is the Wolfram Language.

还有另一点。为了使尽可能多的东西可计算，Wolfram Language 不仅内部包含了海量内容，还提供了一个独特的统一中心，用于连接其他系统和服务。这也是为什么现在可以在 LLM 基础模型和作为基础工具的 Wolfram Language 之间建立如此有效连接的原因之一。

---

## The Tech to Use Our Foundation Tool Is Here / 使用我们基础工具的技术已经到来

On January 9, 2023, just weeks after ChatGPT burst onto the scene, I posted a piece entitled "Wolfram|Alpha as the Way to Bring Computational Knowledge Superpowers to ChatGPT". Two months later we released the first Wolfram plugin for ChatGPT (and in between I wrote what quickly became a rather popular little book entitled What Is ChatGPT Doing … and Why Does It Work?). The plugin was a modest but good start. But at the time LLMs and the ecosystem around them weren't really ready for the bigger story.

2023年1月9日，就在 ChatGPT 横空出世几周后，我发布了一篇题为《Wolfram|Alpha：为 ChatGPT 带来计算知识超能力的方式》的文章。两个月后，我们发布了首个用于 ChatGPT 的 Wolfram 插件（期间我还写了一本很快变得非常受欢迎的小书《ChatGPT 在做什么……以及为什么它能工作？》）。这个插件是一个 modest 但良好的开端。但当时，LLM 及其周围的生态系统还没有真正准备好迎接更大的故事。

Would LLMs even in the end need tools at all? Or—despite the fundamental issues that seemed at least to me scientifically rather clear right from the start—would LLMs somehow magically find a way to do deep computation themselves? Or to guarantee to get precise, reliable results? And even if LLMs were going to use tools, how would that process be engineered, and what would the deployment model for it be?

LLM 最终到底是否需要工具？或者——尽管从一开始科学上就很清楚的根本问题——LLM 是否会以某种神奇的方式找到自行进行深度计算的方法？或者保证获得精确、可靠的结果？即使 LLM 要使用工具，这个过程将如何设计，其部署模式又是什么样的？

Three years have now passed, and much has clarified. The core capabilities of LLMs have come into better focus (even though there's a lot we still don't know scientifically about them). And it's become much clearer that—at least for the modalities LLMs currently address—most of the growth in their practical value is going to have to do with how they are harnessed and connected. And this understanding highlights more than ever the broad importance of providing LLMs with the foundation tool that our technology represents.

三年过去了，很多事情已经明朗。LLM 的核心能力变得更加清晰（尽管我们在科学上仍有许多不了解的地方）。并且越来越清楚的是——至少对于 LLM 目前处理的模式——它们实际价值的大部分增长将取决于它们如何被利用和连接。这种理解比以往任何时候都更加突出了为 LLM 提供我们技术所代表的基础工具的广泛重要性。

And the good news is that there are now streamlined ways to do this—using protocols and methods that have emerged around LLMs, and using new technology that we've developed. The tighter the integration between foundation models and our foundation tool, the more powerful the combination will be. Ultimately it'll be a story of aligning the pre-training and core engineering of LLMs with our foundation tool. But an approach that's immediately and broadly applicable today—and for which we're releasing several new products—is based on what we call computation-augmented generation, or CAG.

好消息是，现在有简化的方法来实现这一点——使用围绕 LLM 出现的协议和方法，以及我们开发的新技术。基础模型与我们的基础工具之间的集成越紧密，组合就越强大。最终，这将是一个将 LLM 的预训练和核心工程与我们的基础工具对齐的故事。但一种今天就能立即广泛应用的方法——也是我们正在发布几款新产品的基础——是基于我们所谓的"计算增强生成"（Computation-Augmented Generation，简称 CAG）。

The key idea of CAG is to inject in real time capabilities from our foundation tool into the stream of content that LLMs generate. In traditional retrieval-augmented generation, or RAG, one is injecting content that has been retrieved from existing documents. CAG is like an infinite extension of RAG, in which an infinite amount of content can be generated on the fly—using computation—to feed to an LLM. Internally, CAG is a somewhat complex piece of technology that has taken a long time for us to develop. But in its deployment it's something that we've made easy to integrate into existing LLM-related systems and workflows. And today we're launching it, so that going forward any LLM system—and LLM foundation model—can count on being able to access our foundation tool, and being able to supplement their capabilities with the superpower of precise, deep computation and knowledge.

CAG 的核心思想是实时将我们基础工具的能力注入到 LLM 生成的内容流中。在传统的检索增强生成（RAG）中，人们注入从现有文档中检索到的内容。CAG 就像是 RAG 的无限扩展，其中可以使用计算即时生成无限量的内容来供给 LLM。从内部来看，CAG 是一项相当复杂的技术，我们花了很长时间才开发出来。但在部署方面，我们已经使其易于集成到现有的 LLM 相关系统和工作流程中。今天，我们正式发布它，以便今后任何 LLM 系统——任何 LLM 基础模型——都可以依赖能够访问我们的基础工具，并能够用精确、深度计算和知识的超能力来补充它们的能力。

---

## The Practicalities / 实践层面

Today we're launching three primary methods for accessing our Foundation Tool, all based on computation-augmented generation (CAG), and all leveraging our rather huge software engineering technology stack.

今天，我们推出了三种主要的基础工具访问方式，全部基于计算增强生成（CAG），并都利用了我们相当庞大的软件工程技术栈。

### MCP Service / MCP 服务

Immediately call our Foundation Tool from within any MCP-compatible LLM-based system. Most consumer LLM-based systems now support MCP, making this extremely easy to set up. Our main MCP Service is a web API, but there's also a version that can use a local Wolfram Engine.

从任何兼容 MCP 的基于 LLM 的系统中立即调用我们的基础工具。现在大多数面向消费者的基于 LLM 的系统都支持 MCP，这使得设置变得极其简单。我们的主要 MCP 服务是一个 Web API，但也有一个可以使用本地 Wolfram 引擎的版本。

### Agent One API / Agent One API

A one-stop-shop "universal agent" combining an LLM foundation model with our Foundation Tool. Set up as a drop-in replacement for traditional LLM APIs.

一个一站式"通用智能体"，将 LLM 基础模型与我们的基础工具相结合。设置为传统 LLM API 的直接替代品。

### CAG Component APIs / CAG 组件 API

Direct fine-grained access to Wolfram tech for LLM systems, supporting optimized, custom integration into LLM systems of any scale. (All Wolfram tech is available in both hosted and on-premise form.)

为 LLM 系统提供对 Wolfram 技术的直接细粒度访问，支持针对任何规模的 LLM 系统进行优化的自定义集成。（所有 Wolfram 技术都提供托管和本地部署两种形式。）

---

## Key Technical Terms / 关键技术术语

| English | Chinese | Description |
|---------|---------|-------------|
| Foundation Tool | 基础工具 | Wolfram 为 LLM 提供的底层计算和知识基础设施 |
| CAG (Computation-Augmented Generation) | 计算增强生成 | 实时将计算能力注入 LLM 内容流的技术 |
| RAG (Retrieval-Augmented Generation) | 检索增强生成 | 从现有文档检索内容来增强 LLM 的传统方法 |
| MCP (Model Context Protocol) | 模型上下文协议 | Anthropic 推出的开放协议，用于 AI 工具集成 |
| Wolfram Language | Wolfram 语言 | Stephen Wolfram 开发的计算语言，集成算法、数据和知识 |
| Wolfram Engine | Wolfram 引擎 | 执行 Wolfram Language 的核心计算引擎 |

---

## Why This Matters / 为什么这很重要

This article marks a significant milestone in the evolution of AI tooling. Stephen Wolfram is essentially positioning Wolfram Language as the "computational backend" for LLMs—filling the critical gap of precise calculation and structured knowledge that neural networks inherently struggle with.

这篇文章标志着 AI 工具演进中的一个重要里程碑。Stephen Wolfram 实质上是在将 Wolfram Language 定位为 LLM 的"计算后端"——填补神经网络本身难以应对的精确计算和结构化知识的关键空白。

For AI/frontend developers, this means:

对于 AI/前端开发者来说，这意味着：

1. **New Integration Patterns**: CAG introduces a new pattern beyond RAG—real-time computation as a service to LLMs
   **新的集成模式**：CAG 引入了超越 RAG 的新模式——实时计算作为服务提供给 LLM

2. **MCP Standard**: The support for MCP (Model Context Protocol) means easier integration with existing AI workflows
   **MCP 标准**：对 MCP（模型上下文协议）的支持意味着与现有 AI 工作流程的更轻松集成

3. **Hybrid AI Systems**: We can now build systems that combine neural reasoning with symbolic computation
   **混合 AI 系统**：我们现在可以构建将神经推理与符号计算相结合的系统

4. **Enterprise Ready**: With both hosted and on-premise options, this is ready for production deployments
   **企业就绪**：提供托管和本地部署选项，已为生产部署做好准备

---

*Translated for AI/Frontend developers. Original article by Stephen Wolfram, published February 23, 2026.*
*为 AI/前端开发者翻译。原文由 Stephen Wolfram 撰写，发表于 2026年2月23日。*
