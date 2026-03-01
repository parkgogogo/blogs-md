---
title: "Implementing a clear room Z80 / ZX Spectrum emulator with Claude Code"
url: "https://antirez.com/news/160"
rating: 10
category: "Programming & Retro Computing"
date: "2026-02-28"
---

# Implementing a clear room Z80 / ZX Spectrum emulator with Claude Code

Anthropic recently released a blog post with the description of an experiment in which the last version of Opus, the 4.6, was instructed to write a C compiler in Rust, in a "clean room" setup.

The experiment methodology left me dubious about the kind of point they wanted to make. Why not provide the agent with the ISA documentation? Why Rust? Writing a C compiler is exactly a giant graph manipulation exercise: the kind of program that is harder to write in Rust. Also, in a clean room experiment, the agent should have access to all the information about well established computer science progresses related to optimizing compilers: there are a number of papers that could be easily synthesized in a number of markdown files. SSA, register allocation, instructions selection and scheduling. Those things needed to be researched *first*, as a prerequisite, and the implementation would still be "clean room".

Not allowing the agent to access the Internet, nor any other compiler source code, was certainly the right call. Less understandable is the almost-zero steering principle, but this is coherent with a certain kind of experiment, if the goal was showcasing the completely autonomous writing of a large project. Yet, we all know how this is not how coding agents are used in practice, most of the time. Who uses coding agents extensively knows very well how, even never touching the code, a few hits here and there completely changes the quality of the result.

## The Z80 experiment

I thought it was time to try a similar experiment myself, one that would take one or two hours at max, and that was compatible with my Claude Code Max plan: I decided to write a Z80 emulator, and then a ZX Spectrum emulator (and even more, a CP/M emulator, see later) in a condition that I believe makes a more sense as "clean room" setup. The result can be found here: https://github.com/antirez/ZOT.

## The process I used

1. I wrote a markdown file with the specification of what I wanted to do. Just English, high level ideas about the scope of the Z80 emulator to implement. I said things like: it should execute a whole instruction at a time, not a single clock step, since this emulator must be runnable on things like an RP2350 or similarly limited hardware. The emulator should correctly track the clock cycles elapsed (and I specified we could use this feature later in order to implement the ZX Spectrum contention with ULA during memory accesses), provide memory access callbacks, and should emulate all the known official and unofficial instructions of the Z80.

For the Spectrum implementation, performed as a successive step, I provided much more information in the markdown file, like, the kind of rendering I wanted in the RGB buffer, and how it needed to be optional so that embedded devices could render the scanlines directly as they transferred them to the ST77xx display (or similar), how it should be possible to interact with the I/O port to set the EAR bit to simulate cassette loading in a very authentic way, and many other desiderata I had about the emulator.

This file also included the rules that the agent needed to follow, like:

- Accessing the internet is prohibited, but you can use the specification and test vectors files I added inside ./z80-specs.
- Code should be simple and clean, never over-complicate things.
- Each solid progress should be committed in the git repository.
- Before committing, you should test that what you produced is high quality and that it works.
- Write a detailed test suite as you add more features. The test must be re-executed at every major change.
- Code should be very well commented: things must be explained in terms that even people not well versed with certain Z80 or Spectrum internals details should understand.
- Never stop for prompting, the user is away from the keyboard.
- At the end of this file, create a work in progress log, where you note what you already did, what is missing. Always update this log.
- Read this file again after each context compaction.

2. Then, I started a Claude Code session, and asked it to fetch all the useful documentation on the internet about the Z80 (later I did this for the Spectrum as well), and to extract only the useful factual information into markdown files. I also provided the binary files for the most ambitious test vectors for the Z80, the ZX Spectrum ROM, and a few other binaries that could be used to test if the emulator actually executed the code correctly. Once all this information was collected (it is part of the repository, so you can inspect what was produced) I completely removed the Claude Code session in order to make sure that no contamination with source code seen during the search was possible.

3. I started a new session, and asked it to check the specification markdown file, and to check all the documentation available, and start implementing the Z80 emulator. The rules were to never access the Internet for any reason (I supervised the agent while it was implementing the code, to make sure this didn't happen), to never search the disk for similar source code, as this was a "clean room" implementation.

4. For the Z80 implementation, I did zero steering. For the Spectrum implementation I used extensive steering for implementing the TAP loading. More about my feedback to the agent later in this post.

5. As a final step, I copied the repository in /tmp, removed the ".git" repository files completely, started a new Claude Code (and Codex) session and claimed that the implementation was likely stolen or too strongly inspired from somebody else's work. The task was to check with all the major Z80 implementations if there was evidence of theft. The agents (both Codex and Claude Code), after extensive search, were not able to find any evidence of copyright issues. The only similar parts were about well established emulation patterns and things that are Z80 specific and can't be made differently, the implementation looked distinct from all the other implementations in a significant way.

## Results

Claude Code worked for 20 or 30 minutes in total, and produced a Z80 emulator that was able to pass ZEXDOC and ZEXALL, in 1200 lines of very readable and well commented C code (1800 lines with comments and blank spaces). The agent was prompted zero times during the implementation, it acted absolutely alone. It never accessed the internet, and the process it used to implement the emulator was of continuous testing, interacting with the CP/M binaries implementing the ZEXDOC and ZEXALL, writing just the CP/M syscalls needed to produce the output on the screen. Multiple times it also used the Spectrum ROM and other binaries that were available, or binaries it created from scratch to see if the emulator was working correctly. In short: the implementation was performed in a very similar way to how a human programmer would do it, and not outputting a complete implementation from scratch "uncompressing" it from the weights. Instead, different classes of instructions were implemented incrementally, and there were bugs that were fixed via integration tests, debugging sessions, dumps, printf calls, and so forth.

## Next step: the ZX Spectrum

I repeated the process again. I instructed the documentation gathering session very accurately about the kind of details I wanted it to search on the internet, especially the ULA interactions with RAM access, the keyboard mapping, the I/O port, how the cassette tape worked and the kind of PWM encoding used, and how it was encoded into TAP or TZX files.

As I said, this time the design notes were extensive since I wanted this emulator to be specifically designed for embedded systems, so only 48k emulation, optional framebuffer rendering, very little additional memory used (no big lookup tables for ULA/Z80 access contention), ROM not copied in the RAM to avoid using additional 16k of memory, but just referenced during the initialization (so we have just a copy in the executable), and so forth.

The agent was able to create a very detailed documentation about the ZX Spectrum internals. I provided a few .z80 images of games, so that it could test the emulator in a real setup with real software. Again, I removed the session and started fresh. The agent started working and ended 10 minutes later, following a process that really fascinates me, and that probably you know very well: the fact is, you see the agent working using a number of diverse skills. It is expert in everything programming related, so as it was implementing the emulator, it could immediately write a detailed instrumentation code to "look" at what the Z80 was doing step by step, and how this changed the Spectrum emulation state. In this respect, I believe automatic programming to be already super-human, not in the sense it is currently capable of producing code that humans can't produce, but in the concurrent usage of different programming languages, system programming techniques, DSP stuff, operating system tricks, math, and everything needed to reach the result in the most immediate way.

When it was done, I asked it to write a simple SDL based integration example. The emulator was immediately able to run the Jetpac game without issues, with working sound, and very little CPU usage even on my slow Dell Linux machine (8% usage of a single core, including SDL rendering).

Once the basic stuff was working, I wanted to load TAP files directly, simulating cassette loading. This was the first time the agent missed a few things, specifically about the timing the Spectrum loading routines expected, and here we are in the territory where LLMs start to perform less efficiently: they can't easily run the SDL emulator and see the border changing as data is received and so forth. I asked Claude Code to do a refactoring so that zx_tick() could be called directly and was not part of zx_frame(), and to make zx_frame() a trivial wrapper. This way it was much simpler to sync EAR with what it expected, without callbacks or the wrong abstractions that it had implemented. After such change, a few minutes later the emulator could load a TAP file emulating the cassette without problems.

This is how it works now:

```c
do {
    zx_set_ear(zx, tzx_update(&tape, zx->cpu.clocks));
} while (!zx_tick(zx, 0));
```

I continued prompting Claude Code in order to make the key bindings more useful and a few things more.

## CP/M

One thing that I found really interesting was the ability of the LLM to inspect the COM files for ZEXALL / ZEXCOM tests for the Z80, easily spot the CP/M syscalls that were used (a total of three), and implement them for the extended z80 test (executed by make fulltest). So, at this point, why not implement a full CP/M environment? Same process again, same good result in a matter of minutes. This time I interacted with it a bit more for the VT100 / ADM3 terminal escapes conversions, reported things not working in WordStar initially, and in a few minutes everything I tested was working well enough (but, there are fixes to do, like simulating a 2Mhz clock, right now it runs at full speed making CP/M games impossible to use).

## What is the lesson here?

The obvious lesson is: always provide your agents with design hints and extensive documentation about what they are going to do. Such documentation can be obtained by the agent itself. And, also, make sure the agent has a markdown file with the rules of how to perform the coding tasks, and a trace of what it is doing, that is updated and read again quite often.

But those tricks, I believe, are quite clear to everybody that has worked extensively with automatic programming in the latest months. To think in terms of "what a human would need" is often the best bet, plus a few LLMs specific things, like the forgetting issue after context compaction, the continuous ability to verify it is on the right track, and so forth.

Returning back to the Anthropic compiler attempt: one of the steps that the agent failed was the one that was more strongly related to the idea of memorization of what is in the pretraining set: the assembler. With extensive documentation, I can't see any way Claude Code (and, even more, GPT5.3-codex, which is in my experience, for complex stuff, more capable) could fail at producing a working assembler, since it is quite a mechanical process. This is, I think, in contradiction with the idea that LLMs are memorizing the whole training set and uncompress what they have seen. LLMs can memorize certain over-represented documents and code, but while they can extract such verbatim parts of the code if prompted to do so, they don't have a copy of everything they saw during the training set, nor they spontaneously emit copies of already seen code, in their normal operation. We mostly ask LLMs to create work that requires assembling different knowledge they possess, and the result is normally something that uses known techniques and patterns, but that is new code, not constituting a copy of some pre-existing code.

It is worth noting, too, that humans often follow a less rigorous process compared to the clean room rules detailed in this blog post, that is: humans often download the code of different implementations related to what they are trying to accomplish, read them carefully, then try to avoid copying stuff verbatim but often times they take strong inspiration. This is a process that I find perfectly acceptable, but it is important to take in mind what happens in the reality of code written by humans. After all, information technology evolved so fast even thanks to this massive cross pollination effect.

For all the above reasons, when I implement code using automatic programming, I don't have problems releasing it MIT licensed, like I did with this Z80 project. In turn, this code base will constitute quality input for the next LLMs training, including open weights ones.

## Next steps

To make my experiment more compelling, one should try to implement a Z80 and ZX Spectrum emulator without providing any documentation to the agent, and then compare the result of the implementation. I didn't find the time to do it, but it could be quite informative.

---

# 中文翻译

Anthropic 最近发布了一篇博客文章，描述了一个实验：他们让最新版本的 Opus 4.6 在一个"净室(clean room)"环境下用 Rust 编写一个 C 编译器。

这个实验的方法论让我对他们想要表达的观点感到疑惑。为什么不给 Agent 提供 ISA 文档？为什么用 Rust？编写 C 编译器本质上就是一个巨大的图操作练习：而这类程序用 Rust 写会更困难。此外，在净室实验中，Agent 应该能够访问所有与优化编译器相关的、成熟的计算机科学进展信息：有很多论文可以轻松地综合成若干 Markdown 文件。SSA（静态单赋值形式）、寄存器分配、指令选择和调度。这些东西应该*首先*作为先决条件进行研究，而且这样实现仍然算是"净室"。

不允许 Agent 访问互联网或其他编译器源代码无疑是正确的决定。较难理解的是几乎零引导的原则，但这与某种实验思路是一致的——如果目标是展示完全自主编写大型项目的能力。然而，我们都知道在实际使用中，编码 Agent 并不是这样被使用的。任何广泛使用编码 Agent 的人都深知，即使从不触碰代码，在这里那里的几次调整就能完全改变结果的质量。

## Z80 实验

我认为是时候自己也尝试一个类似的实验了，一个最多只需一两个小时、且与我的 Claude Code Max 套餐兼容的实验：我决定编写一个 Z80 模拟器，然后是一个 ZX Spectrum 模拟器（甚至更多，还有一个 CP/M 模拟器，详见后文），在一个我认为更符合"净室"定义的条件下进行。结果可以在这里找到：https://github.com/antirez/ZOT。

## 我使用的过程

1. 我写了一个 Markdown 文件，说明我想要做什么。只是用英语描述高层次的想法，关于要实现的 Z80 模拟器的范围。我说了一些事情，比如：它应该一次执行整条指令，而不是单时钟步进，因为这个模拟器必须能在 RP2350 或类似有限硬件上运行。模拟器应该正确跟踪经过的时钟周期（我指出以后可以用这个功能来实现 ZX Spectrum 在内存访问时与 ULA 的争用模拟），提供内存访问回调，并应该模拟 Z80 所有已知的官方和非官方指令。

对于作为后续步骤的 Spectrum 实现，我在 Markdown 文件中提供了更多信息，比如我希望在 RGB 缓冲区中进行的渲染类型，以及为什么它需要是可选的，以便嵌入式设备可以在将扫描行传输到 ST77xx 显示屏（或类似设备）时直接渲染它们，如何通过与 I/O 端口交互来设置 EAR 位以非常真实地模拟磁带加载，以及我对该模拟器的许多其他期望。

这个文件还包括 Agent 需要遵循的规则，比如：

- 禁止访问互联网，但可以使用我放在 ./z80-specs 中的规格说明和测试向量文件。
- 代码应该简单干净，永远不要过度复杂化。
- 每个扎实的进展都应该提交到 Git 仓库中。
- 提交之前，你应该测试你产出的东西质量高且能正常工作。
- 在添加更多功能时编写详细的测试套件。每次重大更改后都必须重新执行测试。
- 代码应该有非常好的注释：必须用即使不太熟悉某些 Z80 或 Spectrum 内部细节的人也能理解的术语来解释事情。
- 不要为了提示而停下来，用户不在键盘前。
- 在此文件末尾创建一个工作进展日志，记录你已经做了什么、还缺什么。始终更新此日志。
- 每次上下文压缩后重新阅读此文件。

2. 然后，我启动了一个 Claude Code 会话，让它从互联网上获取所有关于 Z80 的有用文档（后来我也对 Spectrum 做了同样的事情），并只将有用的事实信息提取到 Markdown 文件中。我还提供了 Z80 最雄心勃勃的测试向量、ZX Spectrum ROM 的二进制文件，以及其他一些可以用来测试模拟器是否正确执行代码的二进制文件。一旦收集了所有这些信息（它是仓库的一部分，所以你可以检查产出了什么），我完全删除了 Claude Code 会话，以确保不会因搜索期间看到的源代码而受到污染。

3. 我启动了一个新会话，让它检查规格说明 Markdown 文件，检查所有可用的文档，并开始实现 Z80 模拟器。规则是绝不允许因任何原因访问互联网（我在 Agent 实现代码时监督它，以确保这不会发生），绝不允许在磁盘上搜索类似的源代码，因为这是一个"净室"实现。

4. 对于 Z80 的实现，我没有进行任何引导。对于 Spectrum 的实现，我在实现 TAP 加载时使用了大量引导。稍后在本帖中会有更多关于我对 Agent 的反馈。

5. 作为最后一步，我将仓库复制到 /tmp，完全删除 ".git" 仓库文件，启动一个新的 Claude Code（和 Codex）会话，并声称该实现很可能是从其他人的作品抄袭或过度借鉴的。任务是检查所有主要的 Z80 实现，看是否有盗窃的证据。这些 Agent（Codex 和 Claude Code）在广泛搜索后，未能找到任何版权问题的证据。唯一相似的部分是关于众所周知的模拟模式，以及那些 Z80 特定的、无法以不同方式完成的事情，该实现在显著程度上看起来与所有其他实现都不同。

## 结果

Claude Code 总共工作了 20 到 30 分钟，产出了一个能够通过 ZEXDOC 和 ZEXALL 测试的 Z80 模拟器，用了 1200 行非常易读且有良好注释的 C 代码（含注释和空行共 1800 行）。在实现过程中，Agent 被提示了零次，它完全独立行动。它从未访问互联网，它用来实现模拟器的过程是持续测试，与实现 ZEXDOC 和 ZEXALL 的 CP/M 二进制文件交互，只编写在屏幕上产生输出所需的 CP/M 系统调用。它还多次使用 Spectrum ROM 和其他可用的二进制文件，或从头创建的二进制文件来查看模拟器是否正常工作。简而言之：实现的方式与人类程序员的做法非常相似，而不是从权重中"解压"出一个完整的实现。相反，不同类型的指令是增量实现的，有通过集成测试、调试会话、转储、printf 调用等方式修复的 Bug。

## 下一步：ZX Spectrum

我重复了这个过程。我准确地指导文档收集会话搜索互联网上我想要的那种细节，特别是 ULA 与 RAM 访问的交互、键盘映射、I/O 端口、磁带的工作原理、使用的 PWM 编码类型，以及它如何编码到 TAP 或 TZX 文件中。

正如我所说，这次设计说明非常详细，因为我希望这个模拟器专门设计用于嵌入式系统，所以只有 48k 模拟、可选的帧缓冲区渲染、使用很少的额外内存（没有用于 ULA/Z80 访问争用的大型查找表）、ROM 不复制到 RAM 中以避免使用额外的 16k 内存，而只是在初始化期间引用（所以我们只在可执行文件中有一个副本），等等。

Agent 能够创建一份关于 ZX Spectrum 内部的非常详细的文档。我提供了一些游戏的 .z80 镜像文件，以便它可以在真实设置中用真实软件测试模拟器。再次，我删除了会话并重新开始。Agent 开始工作，10 分钟后结束，遵循一个真的让我着迷的过程，你可能也很熟悉：事实上，你看到 Agent 工作时使用了各种不同的技能。它在所有与编程相关的事情上都是专家，所以在实现模拟器时，它可以立即编写详细的插桩代码来"观察"Z80 一步一步在做什么，以及这如何改变 Spectrum 模拟状态。在这方面，我相信自动编程已经是超人类的了，不是说它目前能够产出人类无法产出的代码，而是在于它能够同时使用不同的编程语言、系统编程技术、DSP 技术、操作系统技巧、数学，以及达到目标所需的一切，以最直接的方式。

完成后，我让它编写了一个简单的基于 SDL 的集成示例。模拟器立即能够无问题地运行 Jetpac 游戏，有正常工作的声音，即使在我的慢速戴尔 Linux 机器上 CPU 使用率也很低（包括 SDL 渲染在内，单核使用率为 8%）。

一旦基本功能正常工作，我想直接加载 TAP 文件，模拟磁带加载。这是 Agent 第一次漏掉了一些东西，特别是关于 Spectrum 加载例程期望的时序，在这里我们进入了 LLM 开始表现不那么有效的领域：它们不容易运行 SDL 模拟器并观察数据接收时边框的变化等等。我让 Claude Code 进行重构，使 zx_tick() 可以直接调用，而不是 zx_frame() 的一部分，并使 zx_frame() 成为一个简单的包装器。这样同步 EAR 与它的期望就简单多了，不需要回调或它实现的错误抽象。经过这样的更改，几分钟后模拟器就可以毫无问题地加载 TAP 文件模拟磁带了。

现在它是这样工作的：

```c
do {
    zx_set_ear(zx, tzx_update(&tape, zx->cpu.clocks));
} while (!zx_tick(zx, 0));
```

我继续提示 Claude Code，使键绑定更有用一些，还做了一些其他事情。

## CP/M

我发现真正有趣的一点是，LLM 能够检查 Z80 的 ZEXALL / ZEXCOM 测试的 COM 文件，轻松发现使用的 CP/M 系统调用（总共三个），并为扩展的 Z80 测试（通过 make fulltest 执行）实现它们。那么，为什么不实现一个完整的 CP/M 环境呢？同样的过程，同样好的结果，只需几分钟。这次我在 VT100 / ADM3 终端转义序列转换方面与它交互得更多，最初报告了 WordStar 中不工作的东西，几分钟后我测试的所有东西都工作得足够好了（但是，还有一些修复要做，比如模拟 2MHz 时钟，现在它以全速运行，使 CP/M 游戏无法使用）。

## 这里的教训是什么？

显而易见的教训是：始终为你的 Agent 提供设计提示和关于它们将要做什么的广泛文档。这样的文档可以由 Agent 自己获取。而且，还要确保 Agent 有一个 Markdown 文件，其中包含如何执行编码任务的规则，以及一个关于它正在做什么的追踪记录，要经常更新和重新阅读。

但这些技巧，我相信，对于最近几个月广泛使用自动编程的人来说是相当清楚的。从"人类需要什么"的角度思考通常是最好的选择，再加上一些 LLM 特有的东西，比如上下文压缩后的遗忘问题、持续验证它是否在正确轨道上的能力，等等。

回到 Anthropic 的编译器尝试：Agent 失败的一个步骤是与预训练集中记忆内容这一想法最相关的：汇编器。有了广泛的文档，我无法想象 Claude Code（甚至更甚者，在我的经验中对于复杂事务更有能力的 GPT5.3-codex）会在产出一个工作正常的汇编器上失败，因为它是一个相当机械化的过程。这，我认为，与 LLM 正在记忆整个训练集并解压它们所看到的内容这一想法相矛盾。LLM 可以记忆某些过度代表的文档和代码，但虽然如果提示这样做它们可以提取此类代码的逐字部分，但它们并没有在训练集期间看到的所有内容的副本，也不会在正常操作中自发地发出已见代码的副本。我们主要要求 LLM 创建需要组装它们所拥有的不同知识的工作，结果通常是使用已知技术和模式的东西，但那是新代码，不构成某些现有代码的副本。

同样值得注意的是，与这篇博客文章中详述的净室规则相比，人类通常遵循不那么严格的过程，也就是说：人类经常下载与他们试图完成的事情相关的不同实现的代码，仔细阅读，然后试图避免逐字复制东西，但往往从中获得强烈灵感。这是一个我认为完全可以接受的过程，但重要的是要记住人类编写代码的现实中发生了什么。毕竟，信息技术之所以能够如此快速地发展，甚至要归功于这种大规模的交叉授粉效应。

出于以上所有原因，当我使用自动编程实现代码时，我没有问题地以 MIT 许可证发布它，就像我对这个 Z80 项目所做的那样。反过来，这个代码库将构成下一个 LLM 训练的高质量输入，包括开放权重的 LLM。

## 下一步

为了让我的实验更具说服力，应该尝试在不为 Agent 提供任何文档的情况下实现 Z80 和 ZX Spectrum 模拟器，然后比较实现的结果。我没有时间做这个，但它可能会相当有启发性。
