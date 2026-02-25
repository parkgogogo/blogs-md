# Rewriting pycparser with the help of an LLM

> 原文作者：Eli Bendersky  
> 发布日期：February 04, 2026  
> 原文链接：https://eli.thegreenplace.net/2026/rewriting-pycparser-with-the-help-of-an-llm/

---

[pycparser](https://github.com/eliben/pycparser) is my most widely used open source project (with ~20M daily downloads from PyPI). It's a pure-Python parser for the C programming language, producing ASTs inspired by [Python's own](https://docs.python.org/3/library/ast.html). Until very recently, it's been using [PLY: Python Lex-Yacc](https://www.dabeaz.com/ply/ply.html) for the core parsing.

[pycparser](https://github.com/eliben/pycparser) 是我使用最广泛的开源项目（每天从 PyPI 下载约 2000 万次）。它是一个纯 Python 实现的 C 语言解析器，生成的 AST 受到 [Python 自己的 AST 模块](https://docs.python.org/3/library/ast.html) 的启发。直到最近，它的核心解析一直使用 [PLY: Python Lex-Yacc](https://www.dabeaz.com/ply/ply.html)。

In this post, I'll describe how I collaborated with an LLM coding agent (Codex) to help me rewrite pycparser to use a hand-written recursive-descent parser and remove the dependency on PLY. This has been an interesting experience and the post contains lots of information and is therefore quite long; if you're just interested in the final result, check out the latest code of pycparser - the main branch already has the new implementation.

在这篇文章中，我将描述我是如何与 LLM 编程代理（Codex）合作，重写 pycparser 以使用手写递归下降解析器并移除对 PLY 的依赖的。这是一次有趣的经历，文章内容丰富且篇幅较长；如果你只对最终结果感兴趣，请查看 pycparser 的最新代码——主分支已经有了新的实现。

---

## The issues with the existing parser implementation

## 现有解析器实现的问题

While pycparser has been working well overall, there were a number of nagging issues that persisted over years.

虽然 pycparser 总体上运行良好，但多年来一直存在一些令人困扰的问题。

### Parsing strategy: YACC vs. hand-written recursive descent

### 解析策略：YACC 与手写递归下降

I began working on pycparser in 2008, and back then using a YACC-based approach for parsing a whole language like C seemed like a no-brainer to me. Isn't this what everyone does when writing a serious parser? Besides, the K&R2 book famously carries the entire grammar of the C99 language in an appendix - so it seemed like a simple matter of translating that to PLY-yacc syntax.

我在 2008 年开始开发 pycparser，那时使用基于 YACC 的方法来解析像 C 这样的完整语言对我来说似乎是理所当然的。这不就是每个人在编写严肃的解析器时都会做的事吗？此外，著名的 K&R2 书籍在附录中包含了整个 C99 语言的语法——所以这似乎只是将其翻译成 PLY-yacc 语法的简单问题。

And indeed, it wasn't *too* hard, though there definitely were some complications in building the ASTs for declarations (C's [gnarliest part](https://eli.thegreenplace.net/2008/10/18/implementing-cdecl-with-pycparser)).

事实上，这并不算太难，尽管在构建声明的 AST 时确实存在一些复杂问题（C 语言[最棘手的部分](https://eli.thegreenplace.net/2008/10/18/implementing-cdecl-with-pycparser)）。

Shortly after completing pycparser, I got more and more interested in compilation and started learning about the different kinds of parsers more seriously. Over time, I grew convinced that [recursive descent](https://eli.thegreenplace.net/tag/recursive-descent-parsing) is the way to go - producing parsers that are easier to understand and maintain (and are often faster!).

在完成 pycparser 后不久，我对编译越来越感兴趣，开始更认真地学习不同类型的解析器。随着时间的推移，我越来越相信[递归下降](https://eli.thegreenplace.net/tag/recursive-descent-parsing)是正确的方法——它产生的解析器更容易理解和维护（而且通常更快！）。

It all ties in to the [benefits of dependencies in software projects as a function of effort](https://eli.thegreenplace.net/2017/benefits-of-dependencies-in-software-projects-as-a-function-of-effort/). Using parser generators is a heavy *conceptual* dependency: it's really nice when you have to快速生成许多小语言的解析器。但当你必须在一个大型项目中维护一个单一的、非常复杂的解析器时——好处很快就会消散，你会留下一个你必须不断与之斗争的实质性依赖。

这一切都联系到[软件项目中依赖的好处作为工作量的函数](https://eli.thegreenplace.net/2017/benefits-of-dependencies-in-software-projects-as-a-function-of-effort/)。使用解析器生成器是一个沉重的*概念性*依赖：当你需要快速生成许多小语言的解析器时，它确实很好。但当你必须在一个大型项目中维护一个单一的、非常复杂的解析器时——好处很快就会消失，你会留下一个你必须不断与之斗争的实质性依赖。

### The other issue with dependencies

### 依赖的其他问题

And then there are the usual problems with dependencies; dependencies get abandoned, and they may also develop security issues. Sometimes, both of these become true.

然后是依赖的常见问题；依赖会被遗弃，也可能产生安全问题。有时，这两件事都会发生。

Many years ago, pycparser forked and started vendoring its own version of PLY. This was part of transitioning pycparser to a dual Python 2/3 code base when PLY was slower to adapt. I believe this was the right decision, since PLY "just worked" and I didn't have to deal with active (and very tedious in the Python ecosystem, where packaging tools are replaced faster than dirty socks) dependency management.

多年前，pycparser 分叉并开始维护自己的 PLY 版本。这是将 pycparser 过渡到双 Python 2/3 代码库的一部分，当时 PLY 适应较慢。我相信这是正确的决定，因为 PLY "只是工作"，我不必处理活跃的（而且在 Python 生态系统中非常乏味，在那里打包工具比脏袜子更换得更快）依赖管理。

A couple of weeks ago [this issue](https://github.com/eliben/pycparser/issues/588) was opened for pycparser. It turns out the some old PLY code triggers security checks used by some Linux distributions; while this code was fixed in a later commit of PLY, PLY itself was apparently abandoned and archived in late 2025. And guess what? That happened in the middle of a large rewrite of the package, so re-vendoring the pre-archiving commit seemed like a risky proposition.

几周前，[这个问题](https://github.com/eliben/pycparser/issues/588)被提出。原来一些旧的 PLY 代码触发了某些 Linux 发行版使用的安全检查；虽然这段代码在 PLY 的后续提交中被修复了，但 PLY 本身显然在 2025 年底被遗弃并归档了。你猜怎么着？这发生在一个大型包重写的中间，所以重新引入归档前的提交似乎是一个冒险的提议。

On the issue it was suggested that "hopefully the dependent packages move on to a non-abandoned parser or implement their own"; I originally laughed this idea off, but then it got me thinking... which is what this post is all about.

在这个问题上，有人建议"希望依赖包转向一个未被遗弃的解析器或实现自己的"；我最初嘲笑这个想法，但后来它让我开始思考……这就是这篇文章的全部内容。

### Growing complexity of parsing a messy language

### 解析混乱语言的不断增长的复杂性

The original K&R2 grammar for C99 had - famously - a single shift-reduce conflict having to do with dangling elses belonging to the most recent if statement. And indeed, other than the famous [lexer hack](https://en.wikipedia.org/wiki/Lexer_hack) used to deal with [C's type name / ID ambiguity](https://eli.thegreenplace.net/2011/05/02/the-context-sensitivity-of-cs-grammar-revisited), pycparser only had this single shift-reduce conflict.

著名的 K&R2 C99 语法只有一个移入-规约冲突，与属于最近 if 语句的悬空 else 有关。事实上，除了用于处理 [C 语言类型名/ID 歧义](https://eli.thegreenplace.net/2011/05/02/the-context-sensitivity-of-cs-grammar-revisited) 的著名[词法分析器 hack](https://en.wikipedia.org/wiki/Lexer_hack) 外，pycparser 只有这一个移入-规约冲突。

But things got more complicated. Over the years, features were added that weren't strictly in the standard but were supported by all the industrial compilers. The more advanced C11 and C23 standards weren't beholden to the promises of conflict-free YACC parsing (since almost no industrial-strength compilers use YACC at this point), so all caution went out of the window.

但事情变得更复杂了。多年来，添加了一些严格来说不在标准中但被所有工业编译器支持的功能。更先进的 C11 和 C23 标准不受无冲突 YACC 解析承诺的约束（因为此时几乎没有工业级编译器使用 YACC），所以所有的谨慎都烟消云散了。

The latest (PLY-based) release of pycparser has many reduce-reduce conflicts; these are a severe maintenance hazard because it means the parsing rules essentially have to be tie-broken by order of appearance in the code. This is very brittle; pycparser has only managed to maintain its stability and quality through its comprehensive test suite. Over time, it became harder and harder to extend, because YACC parsing rules have all kinds of spooky-action-at-a-distance effects. The straw that broke the camel's back was [this PR](https://github.com/eliben/pycparser/pull/590) which again proposed to increase the number of reduce-reduce conflicts.

最新的（基于 PLY 的）pycparser 版本有许多规约-规约冲突；这些是严重的维护隐患，因为这意味着解析规则基本上必须通过代码中出现的顺序来打破僵局。这非常脆弱；pycparser 只能通过其全面的测试套件来维持其稳定性和质量。随着时间的推移，它变得越来越难扩展，因为 YACC 解析规则有各种幽灵般的远距离作用效应。压垮骆驼的最后一根稻草是[这个 PR](https://github.com/eliben/pycparser/pull/590)，它再次提出增加规约-规约冲突的数量。

This - again - prompted me to think "what if I just dump YACC and switch to a hand-written recursive descent parser", and here we are.

这——再次——促使我思考"如果我干脆抛弃 YACC 转而使用手写的递归下降解析器会怎样"，于是我们就有了这篇文章。

---

## The mental roadblock

## 心理障碍

None of the challenges described above are new; I've been pondering them for many years now, and yet biting the bullet and rewriting the parser didn't feel like something I'd like to get into. By my private estimates it'd take at least a week of deep heads-down work to port the gritty 2000 lines of YACC grammar rules to a recursive descent parser. Moreover, it wouldn't be a particularly *fun* project either - I didn't feel like I'd learn much new and my interests have shifted away from this project. In short, the [Potential well](https://en.wikipedia.org/wiki/Potential_well) was just too deep.

上述挑战都不是新鲜事；我已经思考它们很多年了，但下定决心重写解析器并不是我想做的事情。根据我的私人估计，将艰难的 2000 行 YACC 语法规则移植到递归下降解析器至少需要一周的深度埋头工作。此外，这也不会是一个特别*有趣*的项目——我觉得我不会学到什么新东西，而且我的兴趣已经从这个项目转移了。简而言之，[势阱](https://en.wikipedia.org/wiki/Potential_well)太深了。

---

## Why would this even work? Tests

## 为什么这能行？测试

I've definitely noticed the improvement in capabilities of LLM coding agents in the past few months, and many reputable people online rave about using them for increasingly larger projects. That said, would an LLM agent really be able to accomplish such a complex project on its own? This isn't just a toy, it's thousands of lines of dense parsing code.

我确实注意到了过去几个月 LLM 编程代理能力的提升，网上许多有声望的人都热衷于将它们用于越来越大的项目。也就是说，LLM 代理真的能自己完成如此复杂的项目吗？这不仅仅是一个玩具，而是数千行密集的解析代码。

What gave me hope is the concept of [conformance suites mentioned by Simon Willison](https://simonwillison.net/2025/Dec/31/the-year-in-llms/#the-year-of-conformance-suites). Agents seem to do well when there's a very clear and rigid goal function - such as a large, high-coverage conformance test套件。而 pycparser 有一个[非常广泛的测试套件](https://github.com/eliben/pycparser/blob/main/tests/test_c_parser.py)。超过 2500 行的测试代码解析各种 C 代码片段到带有预期结果的 AST，这些代码是在十多年的真实问题和用户报告的错误中积累起来的。

给我希望的是 [Simon Willison 提到的合规套件概念](https://simonwillison.net/2025/Dec/31/the-year-in-llms/#the-year-of-conformance-suites)。当有一个非常明确和严格的目标函数时——比如一个大型、高覆盖率的合规测试套件——代理似乎表现得很好。而 pycparser 有一个[非常广泛的测试套件](https://github.com/eliben/pycparser/blob/main/tests/test_c_parser.py)。超过 2500 行的测试代码解析各种 C 代码片段到带有预期结果的 AST，这些代码是在十多年的真实问题和用户报告的错误中积累起来的。

I figured the LLM can either succeed or fail and throw its hands up in despair, but it's quite unlikely to produce a *wrong* port that would still pass all the tests. So I set it to run.

我认为 LLM 要么成功要么失败并绝望地放弃，但它不太可能产生一个仍然能通过所有测试的*错误*移植。所以我让它运行了。

---

## The initial port

## 初始移植

I fired up Codex in pycparser's repository, and wrote this prompt just to make sure it understands me and can run the tests:

我在 pycparser 的仓库中启动了 Codex，并写下了这个提示，只是为了确保它理解我并能运行测试：

```
This repository implements a Python parser producing an AST. It has a very
extensive test suite; can you first verify you successfully run all the tests?
(with python3 -m unittest discover, from the root dir)
```

"这个仓库实现了一个生成 AST 的 Python 解析器。它有一个非常广泛的测试套件；你能先验证你成功运行了所有测试吗？（从根目录使用 python3 -m unittest discover）"

Codex figured it out (I gave it the exact command, after all!); my next prompt was the real thing:

Codex 搞清楚了（毕竟我给了它确切的命令！）；我的下一个提示才是真正的东西：

```
pycparser uses the PLY library for its lexer and parser, and its own AST
package for the ASTs created by the parser. I want to explore replacing the
Parser component (leaving the Lexer alone for now) with a hand written
recursive descent parser that will pass all the same tests. Can you try that?
```

"pycparser 使用 PLY 库作为其词法分析器和解析器，并使用自己的 AST 包来创建解析器生成的 AST。我想探索用能通过所有相同测试的手写递归下降解析器来替换解析器组件（暂时保留词法分析器）。你能试试吗？"

Here Codex went to work and churned *for over an hour*. Having never observed an agent work for nearly this long, I kind of assumed it went off the rails and will fail sooner or later. So I was rather surprised and skeptical when it eventually came back with:

在这里，Codex 开始工作并*持续了一个多小时*。从来没有观察过代理工作这么长时间，我有点假设它偏离了轨道，迟早会失败。所以当它最终带着以下回复回来时，我相当惊讶和怀疑：

```
Replaced the PLY parse path with a handwritten recursive‑descent parser while
keeping the existing lexer and AST helpers intact; CParser now points to the
new RD implementation, with the old PLY version preserved as PLYCParser in
pycparser/c_parser.py. The RD parser includes a token stream, declarator/type
parsing, expression precedence handling, pragmas, and statement parsing to
match the previous AST output and coordinate behavior.
```

"用保留现有词法分析器和 AST 辅助工具的手写递归下降解析器替换了 PLY 解析路径；CParser 现在指向新的 RD 实现，旧版本保留为 pycparser/c_parser.py 中的 PLYCParser。RD 解析器包括标记流、声明符/类型解析、表达式优先级处理、pragma 和语句解析，以匹配之前的 AST 输出并协调行为。"

It took me a while to poke around the code and run it until I was convinced - it had actually done it! It wrote a new recursive descent parser with only ancillary dependencies on PLY, and that parser passed the test suite. After a few more prompts, we've removed the ancillary dependencies and made the structure clearer. I hadn't looked too deeply into code quality at this point, but at least on the functional level - it succeeded. This was very impressive!

我花了一段时间仔细查看代码并运行它，直到我相信——它真的做到了！它写了一个新的递归下降解析器，只对 PLY 有辅助依赖，而且该解析器通过了测试套件。在几个更多的提示之后，我们移除了辅助依赖并使结构更清晰。此时我还没有深入研究代码质量，但至少在功能层面上——它成功了。这非常令人印象深刻！

---

## A quick note on reviews and branches

## 关于代码审查和分支的简短说明

A change like the one described above is impossible to code-review as one PR in any meaningful way; so I used a different strategy. Before embarking on this path, I created a new branch and once Codex finished the initial rewrite, I committed this change, knowing that I will review it in detail, piece-by-piece later on.

像上面描述的那样大的变更不可能作为一个 PR 以任何有意义的方式进行代码审查；所以我使用了不同的策略。在开始这条路之前，我创建了一个新分支，一旦 Codex 完成了初始重写，我就提交了这个变更，知道稍后我会逐一详细审查它。

Even though coding agents have their own notion of history and can "revert" certain changes, I felt much safer relying on Git. In the worst case if all of this goes south, I can nuke the branch and it's as if nothing ever happened. I was determined to only merge this branch onto main once I was fully satisfied with the code. In what follows, I had to git reset several times when I didn't like the direction in which Codex was going. In hindsight, doing this work in a branch was absolutely the right choice.

尽管编程代理有自己的历史概念并且可以"回退"某些变更，但我感觉依赖 Git 更安全。在最坏的情况下，如果这一切都出了问题，我可以删除分支，就像什么都没发生过一样。我决心只有在对代码完全满意时才将这个分支合并到主分支。在接下来的过程中，当我不喜欢 Codex 的方向时，我不得不多次 git reset。事后看来，在分支中进行这项工作绝对是正确的选择。

---

## The long tail of goofs

## 错误的漫长尾巴

Once I've sufficiently convinced myself that the new parser is actually working, I used Codex to similarly rewrite the lexer and get rid of the PLY dependency entirely, deleting it from the repository. Then, I started looking more deeply into code quality - reading the code created by Codex and trying to wrap my head around it.

一旦我充分确信新解析器确实在工作，我就使用 Codex 以类似的方式重写词法分析器并完全摆脱 PLY 依赖，将其从仓库中删除。然后，我开始更深入地研究代码质量——阅读 Codex 创建的代码并试图理解它。

And - oh my - this was quite the journey. Much has been written about the code produced by agents, and much of it seems to be true. Maybe it's a setting I'm missing (I'm not using my own custom AGENTS.md yet, for instance), but Codex seems to be that eager programmer that wants to get from A to B whatever the cost. Readability, minimalism and code clarity are very much secondary goals.

——天哪——这是一段相当漫长的旅程。关于代理生成的代码已经有很多文章，其中很多似乎都是真的。也许是我缺少某个设置（例如，我还没有使用自己的自定义 AGENTS.md），但 Codex 似乎是那种渴望的程序员，不惜一切代价想从 A 到 B。可读性、极简主义和代码清晰度都是非常次要的目标。

Using raise...except for control flow? Yep. Abusing Python's weak typing (like having None, false and other values all mean different things for a given variable)? For sure. Spreading the logic of a complex function all over the place instead of putting all the key parts in a single switch statement? You bet.

使用 raise...except 进行控制流？是的。滥用 Python 的弱类型（比如让 None、false 和其他值对一个给定变量都意味着不同的东西）？当然。将一个复杂函数的逻辑分散到各处，而不是把所有关键部分放在一个 switch 语句中？你猜对了。

Moreover, the agent is hilariously *lazy*. More than once I had to convince it to do something it initially said is impossible, and even insisted again in follow-up messages. The anthropomorphization here is mildly concerning, to be honest. I could never imagine I would be writing something like the following to a computer, and yet - here we are: "Remember how we moved X to Y before? You can do it again for Z, definitely. Just try".

此外，这个代理可笑地*懒惰*。不止一次，我不得不说服它去做它最初说不可能的事情，甚至在后续消息中再次坚持。老实说，这里的人格化有点令人担忧。我从未想过我会对计算机写下类似以下的内容，然而——我们就在这里："记得我们以前是怎么把 X 移到 Y 的吗？你绝对可以再次为 Z 做这件事。试试看"。

My process was to see how I can instruct Codex to fix things, and intervene myself (by rewriting code) as little as possible. I've *mostly* succeeded in this, and did maybe 20% of the work myself.

我的过程是看看如何指导 Codex 修复问题，并尽可能少地自己干预（通过重写代码）。我在这一点上*大部分*成功了，自己可能只做了 20% 的工作。

My branch grew *dozens* of commits, falling into roughly these categories:

我的分支增长了*数十个*提交，大致分为以下几类：

1. The code in X is too complex; why can't we do Y instead?
   X 中的代码太复杂了；为什么我们不能改做 Y？

2. The use of X is needlessly convoluted; change Y to Z, and T to V in all instances.
   X 的使用不必要地复杂；在所有实例中将 Y 改为 Z，T 改为 V。

3. The code in X is unclear; please add a detailed comment - with examples - to explain what it does.
   X 中的代码不清楚；请添加详细的注释——并带示例——来解释它做什么。

Interestingly, after doing (3), the agent was often more effective in giving the code a "fresh look" and succeeding in either (1) or (2).

有趣的是，在做完（3）之后，代理通常更有效地给代码一个"新的视角"，并在（1）或（2）中取得成功。

---

## The end result

## 最终结果

Eventually, after many hours spent in this process, I was reasonably pleased with the code. It's far from perfect, of course, but taking the essential complexities into account, it's something I could see myself maintaining (with or without the help of an agent). I'm sure I'll find more ways to improve it in the future, but I have a reasonable degree of confidence that this will be doable.

最终，在这个过程中花费了许多小时后，我对代码相当满意。当然，它远非完美，但考虑到本质的复杂性，这是我可以想象自己维护的东西（无论有没有代理的帮助）。我相信将来我会找到更多改进它的方法，但我有相当程度的信心认为这是可以做到的。

It passes all the tests, so I've been able to release a new version (3.00) without major issues so far. The only issue I've discovered is that some of CFFI's tests are overly precise about the phrasing of errors reported by pycparser; this was [an easy fix](https://github.com/python-cffi/cffi/pull/224).

它通过了所有测试，所以我能够发布一个新版本（3.00），到目前为止没有重大问题。我唯一发现的问题是，CFFI 的一些测试对 pycparser 报告的错误措辞过于精确；这是一个[简单的修复](https://github.com/python-cffi/cffi/pull/224)。

The new parser is also faster, by about 30% based on my benchmarks! This is typical of recursive descent when compared with YACC-generated parsers, in my experience. After reviewing the initial rewrite of the lexer, I've spent a while instructing Codex on how to make it faster, and it worked reasonably well.

新解析器也更快了，根据我的基准测试大约快了 30%！根据我的经验，与 YACC 生成的解析器相比，这是递归下降的典型特征。在审查了词法分析器的初始重写后，我花了一段时间指导 Codex 如何使其更快，效果相当不错。

---

## Followup - static typing

## 后续——静态类型

While working on this, it became quite obvious that static typing would make the process easier. LLM coding agents really benefit from closed loops with strict guardrails (e.g. a test suite to pass), and type-annotations act as such.

在这样做的时候，静态类型会使这个过程变得更容易这一点变得相当明显。LLM 编程代理真的受益于有严格护栏的封闭循环（例如要通过的测试套件），而类型注释就是这样一种护栏。

For example, had pycparser already been type annotated, Codex would probably not have overloaded values to multiple types (like None vs. False vs. others).

例如，如果 pycparser 已经有类型注释，Codex 可能不会将值重载到多种类型（如 None vs. False vs. 其他）。

In a followup, I asked Codex to type-annotate pycparser (running checks using ty), and this was also a back-and-forth because the process exposed some issues that needed to be refactored. Time will tell, but hopefully it will make further changes in the project simpler for the agent.

在后续工作中，我要求 Codex 为 pycparser 添加类型注释（使用 ty 运行检查），这也是一个反复的过程，因为这个过程暴露了一些需要重构的问题。时间会证明一切，但希望这能让代理在项目中进行进一步的变更变得更简单。

Based on this experience, I'd bet that coding agents will be somewhat more effective in strongly typed languages like Go, TypeScript and especially Rust.

根据这次经验，我敢打赌编程代理在像 Go、TypeScript 尤其是 Rust 这样的强类型语言中会稍微更有效。

---

## Conclusions

## 结论

Overall, this project has been a really good experience, and I'm impressed with what modern LLM coding agents can do! While there's no reason to expect that progress in this domain will stop, even if it does - these are already very useful tools that can significantly improve programmer productivity.

总的来说，这个项目是一次非常好的经历，我对现代 LLM 编程代理的能力印象深刻！虽然没有理由期望这个领域的进步会停止，但即使它停止了——这些已经是非常有用的工具，可以显著提高程序员的生产力。

Could I have done this myself, without an agent's help? Sure. But it would have taken me *much* longer, assuming that I could even muster the will and concentration to engage in this project. I estimate it would take me at least a week of full-time work (so 30-40 hours) spread over who knows how long to accomplish. With Codex, I put in an order of magnitude less work into this (around 4-5 hours, I'd estimate) and I'm happy with the result.

没有代理的帮助，我自己能做这个吗？当然。但这会花费我*更长的*时间，假设我甚至有足够的意愿和集中力来投入这个项目。我估计这需要我至少一周的全职工作（所以是 30-40 小时），分散在不知道多长的时间内完成。使用 Codex，我投入的工作量大约少了一个数量级（我估计大约 4-5 小时），而且我对结果很满意。

It was also *fun*. At least in one sense, my professional life can be described as the pursuit of focus, deep work and *flow*. It's not easy for me to get into this state, but when I do I'm highly productive and find it very enjoyable. Agents really help me here. When I know I need to write some code and it's hard to get started, asking an agent to write a prototype is a great catalyst for my motivation. Hence the meme at the beginning of the post.

这也*很有趣*。至少在一种意义上，我的职业生活可以被描述为对专注、深度工作和*心流*的追求。我进入这种状态并不容易，但当我进入时，我非常有生产力，并发现它非常愉快。代理在这里真的帮助了我。当我知道我需要写一些代码但很难开始时，让代理写一个原型是我动机的绝佳催化剂。因此才有了文章开头的梗图。

### Does code quality even matter?

### 代码质量真的重要吗？

One can't avoid a nagging question - does the quality of the code produced by agents even matter? Clearly, the agents themselves can understand it (if not today's agent, then at least next year's). Why worry about future maintainability if the agent can maintain it? In other words, does it make sense to just go full vibe-coding?

有一个挥之不去的问题无法避免——代理生成的代码质量真的重要吗？显然，代理自己可以理解它（如果不是今天的代理，那么至少明年的）。如果代理可以维护它，为什么还要担心未来的可维护性？换句话说，全身心投入 vibe-coding 有意义吗？

This is a fair question, and one I don't have an answer to. Right now, for projects I maintain and *stand behind*, it seems obvious to me that the code should be fully understandable and accepted by me, and the agent is just a tool helping me get to that state more efficiently. It's hard to say what the future holds here; it's going to interesting, for sure.

这是一个公平的问题，也是我没有答案的问题。现在，对于我维护并*支持*的项目，对我来说很明显，代码应该被我完全理解和接受，而代理只是帮助我更有效地达到这种状态的工具。很难说未来会怎样；但这肯定会很有趣。

---

## 💭 批判性思考与评论

### 1. LLM 作为"势阱"突破者的角色

作者用"势阱"（Potential well）这个物理学概念来描述他多年来面对重写 pycparser 的心理障碍。这是一个非常贴切的比喻——很多时候，阻止我们完成某项任务的不是技术难度，而是启动成本和心理阻力。LLM 在这里扮演了一个"催化剂"的角色，将原本需要 30-40 小时的工作压缩到 4-5 小时，这种数量级的效率提升确实令人印象深刻。

但这引出了一个深层问题：**如果 LLM 让困难任务变得容易，它是否也在某种程度上剥夺了我们通过克服困难而获得的学习机会？** 作者提到"这不会是一个特别有趣的项目"、"我觉得我不会学到什么新东西"，这种态度在某种程度上反映了资深工程师对"脏活累活"的厌倦——但历史上，正是这些脏活累活塑造了工程师的直觉和深度理解。

### 2. 测试套件作为"真理来源"的哲学

文章中最令人信服的观点是：LLM 在存在明确、严格的目标函数时表现最佳。作者提到 Simon Willison 的"合规套件"概念，这让我想到：**在 LLM 时代，测试代码可能比生产代码更有价值**。如果你的测试套件足够全面，LLM 就不太可能产生"看起来对但实际错"的代码——因为测试充当了自动验证的护栏。

这是一种范式转变：以前我们写测试来验证代码的正确性，现在我们可能需要先写测试，然后让 LLM 来"填充"实现。测试成为了规范（specification）的可执行形式。

### 3. "Vibe-coding"与代码质量的矛盾

作者在文末提出了一个尖锐的问题：如果 LLM 可以维护它自己生成的代码，那么代码质量还重要吗？这是一个存在主义式的问题。我的看法是：**这取决于时间尺度**。

在短期内，"vibe-coding"确实可行——LLM 可以理解它自己生成的混乱代码。但在长期（5-10 年）尺度上，技术栈会变化，LLM 的架构会变化，甚至可能整个 AI 范式都会变化。如果代码质量差到只有特定版本的特定 LLM 才能理解，那么这种"技术债务"可能是灾难性的。

此外，作者观察到 Codex "可笑地懒惰"，使用 raise...except 进行控制流，滥用弱类型——这些不是风格问题，而是**架构问题**。糟糕的代码结构会在未来产生连锁反应，当需求变化时，债务会以指数形式增长。

### 4. 静态类型的战略价值

作者的经验强烈支持在 LLM 辅助开发中使用静态类型。这一点非常有洞察力：类型系统本质上是一种"轻量级规范"，它在编译时提供了额外的约束条件。对于 LLM 来说，这些约束就像是额外的"测试"——它们限制了可能解的空间，减少了 LLM "犯错"的自由度。

这也解释了为什么作者打赌 LLM 在 Go、TypeScript、Rust 中会更有——这些语言的类型系统提供了更强的约束，LLM 在其中"胡闹"的空间更小。

### 5. "人格化"的风险

作者提到他发现自己对计算机说"记得我们以前是怎么做的吗？你绝对可以为 Z 再做一次。试试看"，并感到"人格化有点令人担忧"。这触及了一个更深层次的问题：**当 LLM 越来越像人，我们是否会在情感上过度依赖它们？**

这种依赖可能不仅仅是技术层面的。当 LLM 成为我们解决问题的默认方式，我们的独立思考能力是否会退化？作者说"代理真的帮助了我进入心流状态"，但这是真正的心流，还是一种外包式的心流？

### 6. 分支策略的智慧

作者采用 Git 分支作为"安全网"的策略值得学习。即使在 LLM 可以"回退"自己的更改的时代，Git 提供的版本控制仍然是更可靠、更透明的基础设施。这提醒我们：**不要盲目信任新工具，要利用已有工具的成熟优势**。

### 总结

这篇文章是一次诚实的自我反思。作者没有盲目吹捧 LLM，也没有固守传统开发方式。他展示了 LLM 作为"力量倍增器"的潜力，同时也诚实地记录了它的局限性——代码质量差、需要大量提示工程、存在"懒惰"问题。

最终，最有价值的洞见可能是：**LLM 不会改变软件开发的基本规律**——好的架构仍然重要，测试仍然重要，代码质量仍然重要。它只是改变了我们到达那里的路径，让我们可以跳过一些繁琐的步骤，但核心的工程判断力和责任感仍然是人类的专利。

正如作者所说："这肯定会很有趣"——但有趣的方向，取决于我们如何使用这个工具。
