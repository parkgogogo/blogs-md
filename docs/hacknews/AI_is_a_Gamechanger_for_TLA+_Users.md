URL: https://buttondown.com/hillelwayne/archive/ai-is-a-gamechanger-for-tla-users/

[Computer Things](https://buttondown.com/hillelwayne)

[计算机那些事](https://buttondown.com/hillelwayne)

June 5, 2025

2025年6月5日

# AI is a gamechanger for TLA+ users

# AI 是 TLA+ 用户的游戏规则改变者

## There has never been a better time to learn formal specification.

## 现在是学习形式化规范的最佳时机。

### New Logic for Programmers Release

### 《程序员逻辑学》新版本发布

[v0.10 is now available](https://leanpub.com/logic/)! This is a minor release, mostly focused on logic-based refactoring, with new material on set类型 and testing refactors are correct. See the full release notes at [the changelog page](https://github.com/logicforprogrammers/book-assets/blob/master/CHANGELOG.md). Due to [conference pressure](https://systemsdistributed.com/) v0.11 will also likely be a minor release.

[v0.10 现已发布](https://leanpub.com/logic/)！这是一个小版本更新，主要关注基于逻辑的重构，新增了关于集合类型和验证重构正确性的内容。完整发布说明请参见[更新日志页面](https://github.com/logicforprogrammers/book-assets/blob/master/CHANGELOG.md)。由于[会议压力](https://systemsdistributed.com/)，v0.11 可能也会是一个小版本更新。

# AI is a gamechanger for TLA+ users

# AI 是 TLA+ 用户的游戏规则改变者

[TLA+](https://lamport.azurewebsites.net/tla/tla.html) is a specification language to model and debug distributed systems. While very powerful, it's also hard for programmers to learn, and there's always questions of connecting specifications with actual code.

[TLA+](https://lamport.azurewebsites.net/tla/tla.html) 是一种用于建模和调试分布式系统的规范语言。虽然它非常强大，但程序员很难学习，而且如何将规范与实际代码连接起来也始终是个问题。

That's why [The Coming AI Revolution in Distributed Systems](https://zfhuang99.github.io/github%20copilot/formal%20verification/tla%2B/2025/05/24/ai-revolution-in-distributed-systems.html) caught my interest. In the post, Cheng Huang claims that Azure successfully used LLMs to examine an existing codebase, derive a TLA+ spec, and find a production bug in that spec. "After a decade of manually crafting TLA+ specifications", he wrote, "I must acknowledge that this AI-generated specification rivals human work".

这就是为什么[《分布式系统中即将到来的 AI 革命》](https://zfhuang99.github.io/github%20copilot/formal%20verification/tla%2B/2025/05/24/ai-revolution-in-distributed-systems.html)引起了我的兴趣。在这篇文章中，黄成声称 Azure 成功地使用大语言模型检查现有代码库，推导出 TLA+ 规范，并在该规范中发现了一个生产环境的 bug。他写道："在手工编写 TLA+ 规范十年之后，我必须承认这个 AI 生成的规范可以与人类的工作相媲美"。

This inspired me to experiment with LLMs in TLA+ myself. My goals are a little less ambitious than Cheng's: I wanted to see how LLMs could help junior specifiers write TLA+, rather than handling the entire spec automatically. Details on what did and didn't work below, but my takeaway is that **LLMs are an immense specification force multiplier.**

这激发了我自己在 TLA+ 中试验大语言模型的兴趣。我的目标比黄成的稍微保守一些：我想看看大语言模型如何帮助初级规范编写者编写 TLA+，而不是自动处理整个规范。以下是哪些方法有效、哪些无效的详细说明，但我的结论是**大语言模型是一个巨大的规范编写倍增器。**

All tests were done with a standard VSCode Copilot subscription, writing Claude 3.7 in Agent mode. Other LLMs or IDEs may be more or less effective, etc.

所有测试都是使用标准的 VSCode Copilot 订阅完成的，使用 Claude 3.7 的 Agent 模式。其他大语言模型或 IDE 可能效果会有所不同。

## Things Claude was good at

## Claude 擅长的方面

### Fixing syntax errors

### 修复语法错误

TLA+ uses a very different syntax than mainstream programming languages, meaning beginners make a lot of mistakes where they do a "programming syntax" instead of TLA+ syntax:

TLA+ 使用的语法与主流编程语言非常不同，这意味着初学者经常会犯用"编程语法"而不是 TLA+ 语法的错误：

```
NotThree(x) = \* should be ==, not =
x != 3 \* should be #, not !=
```

The problem is that the TLA+ syntax checker, SANY, is 30 years old and doesn't provide good information. Here's what it says for that snippet:

问题在于 TLA+ 的语法检查器 SANY 已经有 30 年历史了，无法提供良好的错误信息。对于上面的代码片段，它给出的信息是：

```
Was expecting "==== or more Module body"
Encountered "NotThree" at line 6, column 1
```

That only isolates one error and doesn't tell us what the problem is, only where it is. Experienced TLA+ users get "error eyes" and can quickly see what the problem is, but beginners really struggle with this.

这只能定位到一个错误，而且不告诉我们问题是什么，只告诉我们问题在哪里。有经验的 TLA+ 用户能够练就"错误之眼"，可以快速看出问题所在，但初学者在这方面确实很吃力。

The TLA+ foundation has made LLM integration a priority, so the VSCode extension [naturally supports several agents actions](https://github.com/tlaplus/vscode-tlaplus/blob/master/src/main.ts#L174). One of these is running SANY, meaning an agent can get an error, fix it, get another error, fix it, etc. Provided the above sample and asked to make it work, Claude successfully fixed both errors. It also fixed many errors in a larger spec, as well as figure out why PlusCal specs weren't compiling to TLA+.

TLA+ 基金会已将大语言模型集成列为优先事项，因此 VSCode 扩展[自然地支持多种代理操作](https://github.com/tlaplus/vscode-tlaplus/blob/master/src/main.ts#L174)。其中之一就是运行 SANY，这意味着代理可以获取错误、修复它、获取另一个错误、修复它，如此循环。提供上面的示例并要求它使其正常工作，Claude 成功地修复了两个错误。它还修复了一个更大规范中的许多错误，并找出了 PlusCal 规范无法编译为 TLA+ 的原因。

This by itself is already enough to make LLMs a worthwhile tool, as it fixes one of the biggest barriers to entry.

仅凭这一点就足以让大语言模型成为一个值得使用的工具，因为它解决了入门最大的障碍之一。

### Understanding error traces

### 理解错误追踪

When TLA+ finds a violated property, it outputs the sequence of steps that leads to the error. This starts in plaintext, and VSCode parses it into an interactive table:

当 TLA+ 发现违反的属性时，它会输出导致错误的步骤序列。这以纯文本开始，然后 VSCode 将其解析为交互式表格：

Learning to read these error traces is a skill in itself. You have to understand what's happening in each step and how it relates back to the actually broken property. It takes a long time for people to learn how to do this well.

学会阅读这些错误追踪本身就是一种技能。你必须理解每一步发生了什么，以及它与实际被破坏的属性之间的关系。人们需要很长时间才能学会如何做好这一点。

Claude was successful here, too, accurately reading 20+ step error traces and giving a high-level explanation of what went wrong. It also could condense error traces: if ten steps of the error trace could be condensed into a one-sentence summary (which can happen if you're modeling a lot of process internals) Claude would do it.

Claude 在这方面也很成功，能够准确阅读 20 多个步骤的错误追踪，并对出错的原因给出高层次的解释。它还可以压缩错误追踪：如果错误追踪中的十个步骤可以压缩成一句话的总结（如果你在建模大量进程内部状态时可能发生这种情况），Claude 会这样做。

I did have issues here with doing this in agent mode: while the extension does provide a "run model checker" command, the agent would regularly ignore this and prefer to run a terminal command instead. This would be fine except that the LLM consistently hallucinated invalid commands. I had to amend every prompt with "run the model checker via vscode, do not use a terminal command". You can skip this if you're willing to copy and paste the error trace into the prompt.

我在使用 agent 模式执行此操作时确实遇到了问题：虽然扩展确实提供了"运行模型检查器"命令，但代理经常会忽略这个命令，而更倾向于运行终端命令。如果大语言模型没有持续产生无效的命令幻觉，这本来没问题。我不得不在每个提示中补充"通过 vscode 运行模型检查器，不要使用终端命令"。如果你愿意将错误追踪复制粘贴到提示中，你可以跳过这一步。

As with syntax checking, if this was the *only* thing LLMs could effectively do, that would already be enough[1](#fn:dayenu) to earn a strong recommend. Even as a TLA+ expert I expect I'll be using this trick regularly.

与语法检查一样，如果这是大语言模型唯一能做的事情，那也足以[1](#fn:dayenu)获得强烈推荐。即使作为 TLA+ 专家，我预计我也会经常使用这个技巧。

### Boilerplate tasks

### 样板任务

TLA+ has a lot of boilerplate. One of the most notorious examples is `UNCHANGED` rules. Specifications are extremely precise — so precise that you have to specify what variables *don't* change in every step. This takes the form of an `UNCHANGED` clause at the end of relevant actions:

TLA+ 有很多样板代码。其中最臭名昭著的例子之一就是 `UNCHANGED` 规则。规范非常精确——精确到你必须在每一步中指定哪些变量*不会*改变。这表现为在相关操作末尾添加 `UNCHANGED` 子句：

```
RemoveObjectFromStore(srv, o, s) ==
/\ o \in stored[s]
/\ stored' = [stored EXCEPT ![s] = @ \ {o}]
/\ UNCHANGED <>
```

Writing this is really annoying. Updating these whenever you change an action, or add a new variable to the spec, is doubly so. Syntax checking and error analysis are important for beginners, but this is what I wanted for *myself*. I took a spec and prompted Claude

编写这个真的很烦人。每当你改变一个操作或向规范添加新变量时更新这些就更加烦人。语法检查和错误分析对初学者很重要，但这是为*我自己*想要的东西。我拿出一个规范并提示 Claude：

> Add UNCHANGED <> for each variable not changed in an action.

> 为每个在操作中未改变的变量添加 UNCHANGED <>。

And it worked! It successfully updated the `UNCHANGED` in every action.

而且它奏效了！它成功地更新了每个操作中的 `UNCHANGED`。

(Note, though, that it was a "well-behaved" spec in this regard: only one "action" happened at a time. In TLA+ you can have two actions happen simultaneously, that each update half of the variables, meaning neither of them should have an `UNCHANGED` clause. I haven't tested how Claude handles that!)

（不过要注意的是，在这方面它是一个"行为良好"的规范：一次只发生一个"操作"。在 TLA+ 中，你可以让两个操作同时发生，每个操作更新一半的变量，这意味着它们都不应该有 `UNCHANGED` 子句。我还没有测试 Claude 如何处理这种情况！）

That's the most obvious win, but Claude was good at handling other tedious work, too. Some examples include updating `vars` (the conventional collection of all state variables), lifting a hard-coded value into a model parameter, and changing data formats. Most impressive to me, though, was rewriting a spec designed for one process to instead handle multiple processes. This means taking all of the process variables, which originally have types like `Int`, converting them to types like `[Process -> Int]`, and then updating the uses of all of those variables in the spec. It didn't account for race conditions in the new concurrent behavior, but it was an excellent scaffold to do more work.

这是最明显的胜利，但 Claude 也擅长处理其他繁琐的工作。一些例子包括更新 `vars`（所有状态变量的常规集合）、将硬编码值提升为模型参数，以及更改数据格式。然而，最让我印象深刻的是重写一个为单个进程设计的规范，使其能够处理多个进程。这意味着将所有进程变量（最初类型为 `Int`）转换为 `[Process -> Int]` 这样的类型，然后更新规范中所有这些变量的使用方式。它没有考虑新并发行为中的竞态条件，但这是一个进行更多工作的优秀脚手架。

### Writing properties from an informal description

### 根据非正式描述编写属性

You have to be pretty precise with your intended property description but it handles converting that precise description into TLA+'s formalized syntax, which is something beginners often struggle with.

你必须非常精确地描述你想要的属性，但它擅长将这种精确的描述转换为 TLA+ 的形式化语法，而这正是初学者经常 struggling 的地方。

## Things it is less good at

## 它不太擅长的方面

### Generating model config files

### 生成模型配置文件

To model check TLA+, you need both a specification (`.tla`) and a model config file (`.cfg`), which have separate syntaxes. Asking the agent to generate the second often lead to it using TLA+ syntax. It automatically fixed this after getting parsing errors, though.

要对 TLA+ 进行模型检查，你需要一个规范文件（`.tla`）和一个模型配置文件（`.cfg`），它们有各自的语法。要求代理生成第二个文件经常会导致它使用 TLA+ 语法。不过，在得到解析错误后，它会自动修复这个问题。

### Fixing specs

### 修复规范

Whenever the ran model checking and discovered a bug, it would naturally propose a change to either the invalid property or the spec. Sometimes the changes were good, other times the changes were not physically realizable. For example, if it found that a bug was due to a race condition between processes, it would often suggest fixing it by saying race conditions were okay. I mean yes, if you say bugs are okay, then the spec finds that bugs are okay! Or it would alternatively suggest adding a constraint to the spec saying that race conditions don't happen. [But that's a huge mistake in specification](https://www.hillelwayne.com/post/alloy-facts/), because race conditions happen if we don't have coordination. We need to specify the *mechanism* that is supposed to prevent them.

每当运行模型检查并发现 bug 时，它自然会建议对无效属性或规范进行更改。有时这些更改是好的，有时这些更改在物理上无法实现。例如，如果它发现 bug 是由于进程之间的竞态条件造成的，它经常会建议通过说竞态条件没问题来修复它。我的意思是，如果你说 bug 没问题，那么规范就会发现 bug 没问题！或者它会建议向规范添加一个约束，说竞态条件不会发生。[但这是在规范中犯的一个巨大错误](https://www.hillelwayne.com/post/alloy-facts/)，因为如果没有协调，竞态条件就会发生。我们需要指定应该防止它们的*机制*。

### Finding properties of the spec

### 发现规范的属性

After seeing how capable it was at translating my properties to TLA+, I started prompting Claude to come up with properties on its own. Unfortunately, almost everything I got back was either trivial,不有趣, or too coupled to实现细节. I haven't tested if it would work better to ask it for "properties that may be violated".

在看到它在将我的属性转换为 TLA+ 方面的能力后，我开始提示 Claude 自己提出属性。不幸的是，我得到的几乎所有结果要么太简单、要么不有趣，要么与实现细节耦合得太紧。我还没有测试如果要求它提供"可能被违反的属性"是否会效果更好。

### Generating code from specs

### 从规范生成代码

I have to be specific here: Claude *could* sometimes convert Python into a passable spec, an vice versa. It *wasn't* good at recognizing abstraction. For example, TLA+ specifications often represent sequential operations with a state variable, commonly called `pc`. If modeling code that nonatomically retrieves a counter value and increments it, we'd have one action that requires `pc = "Get"` and sets the new value to `"Inc"`, then another that requires it be `"Inc"` and sets it to `"Done"`.

我在这里必须具体说明：Claude *有时*可以将 Python 转换为一个还可以的规范，反之亦然。但它*不*擅长识别抽象。例如，TLA+ 规范通常用一个状态变量来表示顺序操作，通常称为 `pc`。如果要建模非原子地获取计数器值并递增的代码，我们会有一个操作要求 `pc = "Get"` 并将新值设置为 `"Inc"`，然后另一个操作要求它是 `"Inc"` 并将其设置为 `"Done"`。

I found that Claude would try to somehow convert `pc` into part of the Python program's state, rather than recognize it as a TLA+ abstraction. On the other side, when converting python code to TLA+ it would often try to translate things like `sleep` into some part of the spec, not recognizing that it is abstractable into a distinct action. I didn't test other possible misconceptions, like converting randomness to nondeterminism.

我发现 Claude 会试图以某种方式将 `pc` 转换为 Python 程序状态的一部分，而不是将其识别为 TLA+ 的抽象。另一方面，当将 Python 代码转换为 TLA+ 时，它经常试图将 `sleep` 之类的东西翻译成规范的一部分，而没有认识到它可以抽象为一个独立的操作。我没有测试其他可能的误解，比如将随机性转换为非确定性。

For the record, when converting TLA+ to Python Claude tended to make simulators of the spec, rather than possible production code implementing the spec. I really wasn't expecting otherwise though.

顺便说一下，当将 TLA+ 转换为 Python 时，Claude 倾向于制作规范的模拟器，而不是实现规范的可能的生产代码。不过我真的没有期待其他的结果。

## Unexplored Applications

## 尚未探索的应用

Things I haven't explored thoroughly but could possibly be effective, based on what I know about TLA+ and AI:

根据我对 TLA+ 和 AI 的了解，以下是我尚未深入探索但可能有效的方法：

### Writing Java Overrides

### 编写 Java 覆盖

Most TLA+ operators are resolved via TLA+ interpreters, but you can also implement them in "native" Java. This lets you escape the standard language semantics and add capabilities like [executing programs during model-checking](https://github.com/tlaplus/CommunityModules/blob/master/modules/IOUtils.tla) or [dynamically constrain the depth of the searched state空间](https://github.com/tlaplus/tlaplus/blob/master/tlatools/org.lamport.tlatools/src/tla2sany/StandardModules/TLC.tla#L62). There's a lot of cool things I think would be possible with overrides. The problem is there's only a handful of people in the world知道如何编写它们。But that handful have written quite a few overrides and I think there's enough there for Claude to work with.

大多数 TLA+ 操作符是通过 TLA+ 解释器解析的，但你也可以在"原生" Java 中实现它们。这让你可以脱离标准语言语义，并添加诸如[在模型检查期间执行程序](https://github.com/tlaplus/CommunityModules/blob/master/modules/IOUtils.tla)或[动态限制搜索状态空间的深度](https://github.com/tlaplus/tlaplus/blob/master/tlatools/org.lamport.tlatools/src/tla2sany/StandardModules/TLC.tla#L62)等功能。我认为通过覆盖可以实现很多很酷的东西。问题是世界上只有少数人知道如何编写它们。但那少数人已经编写了不少覆盖，我认为有足够的内容供 Claude 使用。

### Writing specs, given a reference mechanism

### 给定参考机制编写规范

In all my experiments, the LLM only had my prompts and the occasional Python script as information. That makes me suspect that some of its problems with writing and fixing specs come down to not having a system model. Maybe it wouldn't suggest fixes like "these processes never race" if it had a design doc saying that the processes can't coordinate.

在我所有的实验中，大语言模型只有我的提示和偶尔的 Python 脚本作为信息。这让我怀疑它在编写和修复规范方面的一些问题归结为没有系统模型。如果它有一份设计文档说明进程无法协调，也许它就不会建议像"这些进程永远不会竞态"这样的修复。

(Could a Sufficiently Powerful LLM derive some TLA+ specification from a design document?)

（一个足够强大的大语言模型能从设计文档中推导出一些 TLA+ 规范吗？）

### Connecting specs and code

### 连接规范和代码

This is the holy grail of TLA+: taking a codebase and showing it correctly implements a spec. Currently the best ways to do this are by either using TLA+ to generate a test套件, or by taking logged production traces and matching them to TLA+ behaviors. [This blog post discusses both](https://www.mongodb.com/blog/post/engineering/conformance-checking-at-mongodb-testing-our-code-matches-our-tla-specs). While I've seen a lot of academic research into these approaches there are no industry-ready tools. So if you want trace validation you have to do a lot of manual labour tailored to your specific product.

这是 TLA+ 的圣杯：获取一个代码库并证明它正确地实现了一个规范。目前最好的方法要么是使用 TLA+ 生成测试套件，要么是获取记录的生产追踪并将它们与 TLA+ 行为匹配。[这篇博客文章讨论了这两种方法](https://www.mongodb.com/blog/post/engineering/conformance-checking-at-mongodb-testing-our-code-matches-our-tla-specs)。虽然我见过很多关于这些方法的学术研究，但没有行业就绪的工具。所以如果你想要追踪验证，你必须做大量针对你特定产品的手工劳动。

If LLMs could do some of this work for us then that'd really amplify the usefulness of TLA+ to many companies.

如果大语言模型能为我们做一些这样的工作，那将真正放大 TLA+ 对许多公司的有用性。

## Thoughts

## 思考

*Right now*, agents seem good at the tedious and routine parts of TLA+ and worse at the strategic and abstraction parts. But, since the routine parts are often a huge barrier to beginners, this means that LLMs have the potential to make TLA+ far, far more accessible than it previously was.

*目前*，代理似乎擅长 TLA+ 的繁琐和常规部分，而在战略和抽象部分表现较差。但是，由于常规部分通常是初学者面临的巨大障碍，这意味着大语言模型有可能让 TLA+ 比以前更容易接触得多。

I have mixed thoughts on this. As an *advocate*, this is incredible. I want more people using formal specifications because I believe it leads to cheaper, safer, more reliable software. Anything that gets people comfortable with specs is great for our industry. As a *professional TLA+ consultant*, I'm worried that this obsoletes me. Most of my income comes from培训和 coaching, which companies will have far less demand of now. Then again, maybe this an opportunity to pitch "agentic TLA+ training" to companies!

我对此有复杂的想法。作为一个*倡导者*，这太不可思议了。我希望更多人使用形式化规范，因为我相信这会带来更便宜、更安全、更可靠的软件。任何让人们适应规范的东西对我们的行业都是有益的。作为一个*专业的 TLA+ 顾问*，我担心这会使我过时。我的大部分收入来自培训和指导，而公司现在对这些的需求会大大减少。不过，也许这是一个向公司推销"代理式 TLA+ 培训"的机会！

Anyway, if you're interested in TLA+, there has never been a better time to try it. I mean it, these tools handle so much of the hard part now. I've got a [free book available online](https://learntla.com/), as does [the inventor of TLA+](https://lamport.azurewebsites.net/tla/book.html). I like [this guide too](https://elliotswart.github.io/pragmaticformalmodeling/). Happy modeling!

不管怎样，如果你对 TLA+ 感兴趣，现在是从未有过的最佳尝试时机。我是认真的，这些工具现在处理了这么多困难的部分。我有一本[免费的在线书籍](https://learntla.com/)，[TLA+ 的发明者](https://lamport.azurewebsites.net/tla/book.html)也有。我也喜欢[这份指南](https://elliotswart.github.io/pragmaticformalmodeling/)。祝你建模愉快！

---

Dayenu.

这就够了（Dayenu）。

*If you're reading this on the web, you can subscribe [here](/hillelwayne). Updates are once a week. My main website is [here](https://www.hillelwayne.com).*

*如果你在网页上阅读本文，可以在[这里](/hillelwayne)订阅。每周更新一次。我的主网站在[这里](https://www.hillelwayne.com)。*

*My new book,* Logic for Programmers*, is now in early access! Get it [here](https://leanpub.com/logic/).*

*我的新书《程序员的逻辑学》现已开放早期访问！在[这里](https://leanpub.com/logic/)获取。*

---

💭 批判性思考

这篇文章深入探讨了 AI（特别是大语言模型）如何改变 TLA+ 形式化规范的使用方式，但我认为有几个关键点值得进一步思考：

**1. AI 作为"倍增器"而非"替代者"的定位**

作者明确将 LLM 定位为"规范编写的倍增器"（force multiplier）而非完全的自动替代工具，这是相当务实的观点。在形式化方法这个领域，纯自动化生成规范仍然是一个未解决的难题，但 AI 在降低入门门槛方面确实展现出了巨大潜力。这提醒我们：AI 最有价值的应用可能不是取代人类专家，而是让新手更容易成为专家。

**2. 深度理解与表面模式的张力**

文章指出了一个关键局限：Claude 擅长处理"繁琐和常规部分"，但在"战略和抽象部分"表现较差。这反映了一个更广泛的 AI 局限——大语言模型本质上是模式匹配系统，它们可以识别和复制语法模式，但缺乏对分布式系统本质的深层理解。例如，当 AI 建议"竞态条件没问题"时，它暴露了对形式化规范核心目的的误解：规范不是为了证明系统没有 bug，而是为了发现潜在的 bug。

**3. 形式化方法的民主化悖论**

作者作为 TLA+ 顾问的身份揭示了一个有趣的悖论：AI 降低了 TLA+ 的学习曲线，可能减少了对专业培训的需求，这对他个人的商业模式构成威胁。但这同时也代表了一个更大的市场机会——当工具变得更易用时，总体的采用率可能会上升。这让我想到 Photoshop 或 Excel 的历史：当软件变得更易用时，专业人士并没有消失，而是转移到了更高层次的价值创造。

**4. 抽象能力的缺失是最根本的局限**

文章多次提到 AI 在识别抽象方面的困难——将 `pc` 变量误认为是程序状态的一部分，或者无法正确地将 `sleep` 抽象为独立的操作。这触及了形式化方法的核心：好的规范不是对代码的字面翻译，而是对系统本质行为的抽象建模。这种抽象能力需要深层的领域理解和创造性思维，这正是当前 AI 系统最薄弱的地方。

**5. "代码到规范" vs "规范到代码"的不对称性**

有趣的是，AI 在从 Python 到 TLA+ 的转换中表现尚可，但在反向转换时往往产生模拟器而非生产代码。这暗示了形式化规范和实现代码之间存在本质的不对称性：规范是更抽象的，代码是更具体的，而从抽象到具体的映射存在多种可能的实现。这也解释了为什么形式化验证（证明代码正确实现规范）仍然是一个开放的研究问题。

**6. 对初学者的真正价值**

尽管存在局限，作者仍然强烈推荐初学者现在尝试 TLA+，因为 AI 处理了"这么多困难的部分"。这提出了一个重要问题：在 AI 辅助学习的环境中，初学者的学习路径会发生什么变化？他们可能会更快上手，但也可能错过通过挣扎解决语法错误而获得的深层理解。这是一种权衡——效率与深度的权衡。

总的来说，这篇文章提供了一个平衡而深入的视角，既不夸大 AI 的能力，也不忽视其真正的实用价值。对于形式化方法社区来说，这是一个激动人心的时刻，但也是一个需要保持清醒头脑的时刻——AI 是强大的工具，但不是万能的解决方案。
