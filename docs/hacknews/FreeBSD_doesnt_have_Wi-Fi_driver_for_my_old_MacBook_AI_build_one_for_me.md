URL: https://vladimir.varank.in/notes/2026/02/freebsd-brcmfmac/

My old 2016 MacBook Pro has been collecting dust in a cabinet for some time now. The laptop suffers from a ["flexgate" problem](https://www.macrumors.com/guide/flexgate-macbook-pro-display-issue/), and I don't have any practical use for it. For quite some time, I've been thinking about repurposing it as a guinea pig, to play with FreeBSD — an OS that I'd aspired to play with for a long while, but had never had a real reason to.

我的旧款 2016 年 MacBook Pro 已经在柜子里积灰有一段时间了。这台笔记本有["flexgate"问题](https://www.macrumors.com/guide/flexgate-macbook-pro-display-issue/)，我也没有任何实际用途。很长一段时间以来，我一直在考虑把它当作实验品重新利用，用来折腾 FreeBSD——这是一个我一直想尝试的操作系统，但从来没有一个真正的理由去做。

During the recent holiday season, right after FreeBSD 15 release, I've finally found time to set the laptop up. Doing that I didn't plan, or even think, this may turn into a story about AI coding.

在最近假期期间，就在 FreeBSD 15 发布后，我终于找到时间来设置这台笔记本。当时我并没有计划，甚至没有想到，这可能会变成一个关于 AI 编程的故事。

## Background

2016 MacBook Pro models use Broadcom BCM4350 Wi-Fi chip. FreeBSD doesn't have native support for this chip. To have a working Wi-Fi, a typical suggestion on FreeBSD forums, is to run wifibox — a tiny Linux VM, with the PCI Wi-Fi device in pass through, that allows Linux to manage the device through its brcmfmac driver.

2016 款 MacBook Pro 使用的是博通 BCM4350 Wi-Fi 芯片。FreeBSD 没有对这个芯片的原生支持。为了让 Wi-Fi 工作，FreeBSD 论坛上的一个典型建议是使用 wifibox——一个微型 Linux 虚拟机，将 PCI Wi-Fi 设备直通给它，让 Linux 通过其 brcmfmac 驱动来管理这个设备。

Brcmfmac is a Linux driver (ISC licence) for set of FullMAC chips from Broadcom. The driver offloads the processing jobs, like 802.11 frame movement, WPA encryption and decryption, etc, to the firmware, which is running inside the chip. Meanwhile, the driver and the OS do high-level management work (ref [Broadcom brcmfmac(PCIe) in Linux Wireless documentation](https://wireless.docs.kernel.org/en/latest/en/users/drivers/brcm80211.html)).

Brcmfmac 是一个 Linux 驱动（ISC 许可证），用于博通的一系列 FullMAC 芯片。该驱动将处理任务（如 802.11 帧传输、WPA 加密和解密等）卸载到运行在芯片内部的固件。与此同时，驱动和操作系统负责高层管理工作（参考 [Linux 无线文档中的 Broadcom brcmfmac(PCIe)](https://wireless.docs.kernel.org/en/latest/en/users/drivers/brcm80211.html)）。

Say we want to build a native FreeBSD kernel module for the BCM4350 chip. In theory, this separation of jobs between the firmware and the driver sounds perfect. The "management" part of work is what FreeBSD already does for其他支持的 Wi-Fi 设备。We need to port some amount of existing "glue code" from specifics of Linux to FreeBSD. If we ignore a lot of details, the problem doesn't sound too complicated, right?

假设我们想为 BCM4350 芯片构建一个原生的 FreeBSD 内核模块。理论上，固件和驱动之间的这种任务分离听起来很完美。"管理"部分的工作正是 FreeBSD 已经为其他支持的 Wi-Fi 设备所做的。我们需要将一些现有的"胶水代码"从 Linux 的特性移植到 FreeBSD。如果我们忽略很多细节，这个问题听起来不会太复杂，对吧？

## Act 1

A level-zero idea, when one hears about "porting a bunch of existing code from A to B", in 2026 is, of course, to use AI. So that was what I tried.

当人们在 2026 年听到"将一堆现有代码从 A 移植到 B"时，第一个念头当然是使用 AI。所以我就是这么尝试的。

I cloned the brcmfmac subtree, and asked Claude Code to make it work for FreeBSD. FreeBSD already has drivers that work through LinuxKPI — compatibility layer for running Linux kernel drivers. So I specifically pointed Claude at the iwlwifi driver (a softmac driver for Intel wireless network card), asking "do as they did it". And, at first, this even looked like this can work — Claude told me so.

我克隆了 brcmfmac 子树，并要求 Claude Code 让它在 FreeBSD 上工作。FreeBSD 已经有通过 LinuxKPI 工作的驱动程序——这是一个用于运行 Linux 内核驱动的兼容层。所以我特别让 Claude 参考 iwlwifi 驱动（一个用于英特尔无线网卡的 softmac 驱动），告诉它"照着他们做"。起初，这看起来甚至像是可行的——Claude 也这么告诉我。

[https://bsky.app/profile/vladimir.varank.in/post/3mawf7xbdws2r](https://bsky.app/profile/vladimir.varank.in/post/3mawf7xbdws2r)

The module, indeed, compiled, but it didn't do anything. Because, of course: the VM, where we tested the module, didn't even have the hardware. After I set the PCI device into the VM, and attempted to load the driver against the chip, the challenges started to pop up immediately. The kernel paniced, and after Claude fixed the panics, it discovered that "module didn't do anything". Claude honestly tried to sift through the code, adding more and more #ifdef __FreeBSD__ wrappers here and there. It complained about missing features in LinuxKPI. The module kept causing panics, and the agent kept building FreeBSD-specific shims and callbacks, while warning me that this project will be very complicated and messy.

这个模块确实编译成功了，但它什么都没做。因为当然：我们测试模块的虚拟机根本没有这个硬件。在我将 PCI 设备设置到虚拟机后，尝试针对芯片加载驱动时，挑战立即开始出现。内核崩溃了，在 Claude 修复崩溃后，它发现"模块什么都没做"。Claude 诚实地尝试梳理代码，到处添加越来越多的 #ifdef __FreeBSD__ 包装器。它抱怨 LinuxKPI 缺少功能。模块不断导致崩溃，而 agent 不断构建 FreeBSD 特定的垫片和回调，同时警告我这个项目将非常复杂和混乱。

## Act 2

After a number of sessions, the diff, produced by the agent, stared to look significantly larger than what I'd hoped it will be. Even worse, the driver didn't look even close to be working. This was right around time when Armin Ronacher posted about his experience [building a game from scratch with Claude Opus and PI agent](https://youtu.be/ANQ1IYsFM2s?si=GP6oVkBN-5_hmIFM).

经过若干次会话后，agent 生成的 diff 开始看起来比我预期的要大得多。更糟糕的是，驱动看起来离能工作还差得远。就在这个时候，Armin Ronacher 发布了他[使用 Claude Opus 和 PI agent 从零开始构建游戏](https://youtu.be/ANQ1IYsFM2s?si=GP6oVkBN-5_hmIFM)的经验。

Besides the part that working in [Pi coding agent](https://pi.dev) feels more productive, than in Claude Code, the video got me thinking that my approach to the task was too straightforward. The code of brcmfmac driver is moderately large. The driver supports several generations of Wi-Fi adaptors, different capabilities, etc. But my immediate task was very narrow: one chip, only PCI, only Wi-Fi client.

除了在 [Pi coding agent](https://pi.dev) 中工作比在 Claude Code 中更高效之外，这个视频让我思考我对这个任务的方法过于直接了。brcmfmac 驱动的代码量中等偏大。该驱动支持几代 Wi-Fi 适配器、不同的功能等。但我当前的任务非常狭窄：一个芯片，仅 PCI，仅 Wi-Fi 客户端。

Instead of continuing with the code, I spawned a fresh Pi session, and asked the agent to write a detailed specification of how the brcmfmac driver works, with the focus on BCM4350 Wi-Fi chip. I explicitly set the audience for the specification to be readers, who are tasked with implementing the specification in a clean-room environment. I asked the agent to explain how things work "to the bits". I added some high-level details for how I wanted the specification to be laid out, and let the agent go brrrr.

我没有继续编写代码，而是开启了一个全新的 Pi 会话，要求 agent 编写一份关于 brcmfmac 驱动如何工作的详细规范，重点聚焦在 BCM4350 Wi-Fi 芯片上。我明确将规范的目标读者设定为需要在洁净室环境中实现该规范的开发者。我要求 agent "深入到比特级别"解释事物的工作原理。我添加了一些关于我希望如何组织规范的高层细节，然后让 agent 开始工作。

After a couple of rounds, the agent produced me a "book of 11 chapters", that honestly looked like a fine specification

经过几轮迭代后，agent 为我生成了一本"11 章的书"，老实说看起来像是一份不错的规范

```
spec
├── 00-overview.md
├── 01-data-structures.md
├── 02-bus-layer.md
├── 03-protocol-layer.md
├── 04-firmware-interface.md
├── 05-event-handling.md
├── 06-cfg80211-operations.md
├── 07-initialization.md
├── 08-data-path.md
├── 09-firmware-commands.md
└── 10-structures-reference.md
```

Of course, one can't just trust what AI has written.

当然，不能轻易相信 AI 写的内容。

To proofread the spec I spawned a clean Pi sessions, and — for fun — asked Codex model, to read the specification, and flag any places, where the text isn't aligned with the driver's code ("Source code是最终的真理。The spec needs to be verified, and updated with any missing or wrong details"). The agent followed through and found several places to fix, and also proposed multiple improvements.

为了校对规范，我开启了一个干净的 Pi 会话，然后——出于好玩——要求 Codex 模型阅读规范，并标出任何与驱动代码不一致的地方（"源代码是最终的真理。规范需要被验证，并用任何缺失或错误的细节进行更新"）。agent 照做了，发现了几个需要修复的地方，还提出了多处改进建议。

Of course, one can't just trust what AI has written, even if this was in a proofreading session.

当然，即使在校对会话中，也不能轻易相信 AI 写的内容。

To double-proofread the fixes I spawned another clean Pi sessions, asking Opus model to verify if what was proposed was aligned with how it works in the code of the driver.

为了双重校对修复内容，我开启了另一个干净的 Pi 会话，要求 Opus 模型验证所提出的内容是否与驱动代码中的工作方式一致。

As a procrastination exercise, I tried this loop with a couple of coding models: Opus 4.5, Opus 4.6, Codex 5.2, Gemini 3 Pro preview. So far my experience was that Gemini hallucinated the most. This was quite sad, given that the model itself isn't too bad for simple coding tasks, and it is free for a limited use.

作为一个拖延练习，我用几个编程模型尝试了这个循环：Opus 4.5、Opus 4.6、Codex 5.2、Gemini 3 Pro preview。到目前为止，我的经验是 Gemini 的幻觉最严重。这相当令人遗憾，因为这个模型本身对于简单的编程任务来说还不错，而且有限使用时是免费的。

Having a written specification should have (in theory) explained how a driver's code interacts with the firmware.

拥有一份书面规范应该（理论上）解释了驱动代码如何与固件交互。

## Act 3

I started a fresh project, with nothing but the mentioned "spec", and prompted the Pi agent, that we were building a brand new FreeBSD driver for BCM4350 chip. I pointed the agent to the specification, and asked it to ask me back about any important decisions we must make, and details we must outline, before jumping into "slopping the code". The agent came back with questions and decision points, like "Will the driver live in the kernels source-tree?", "Will we write the code in C?", "Will we rely on LinuxKPI?", "What are our high-level milestones?", etc. One influential bit, that turned fairly productive moving forward, was that I asked the agent to document all these decision points in the project's docs, and to explicitly referenced to these decision docs in the project's AGENTS.md.

我启动了一个全新的项目，只有前面提到的"规范"，并提示 Pi agent 我们正在为 BCM4350 芯片构建一个全新的 FreeBSD 驱动。我引导 agent 参考规范，并要求它在开始"写代码"之前，向我询问任何我们必须做出的重要决定和必须概述的细节。agent 带回了一些问题和决策点，比如"驱动会放在内核源代码树中吗？"、"我们会用 C 语言编写代码吗？"、"我们会依赖 LinuxKPI 吗？"、"我们的高层里程碑是什么？"等等。其中一个相当有影响力的、在后续工作中变得相当高效的做法是，我要求 agent 在项目的文档中记录所有这些决策点，并在项目的 AGENTS.md 中明确引用这些决策文档。

It's worth saying that, just like in any real project, not all decisions stayed to the end. For example,

值得一提的是，就像在任何真实项目中一样，并非所有决定都保持到最后。例如，

Initially I asked the agent to build the driver using linuxkpi and linuxkpi_wlan. My naive thinking was that, given the spec was written after looking at Linux driver's code, it might be simpler for the agent, than building the on top of the native primitives. After a couple of sessions, it didn't look like this was the case. I asked the agent to drop LinuxKPI from the code, and to refactor everything. The agent did it in one go, and updated the decision document.

最初我要求 agent 使用 linuxkpi 和 linuxkpi_wlan 来构建驱动。我天真的想法是，鉴于规范是在查看 Linux 驱动代码后编写的，对 agent 来说可能比基于原生原语构建更简单。经过几次会话后，看起来并非如此。我要求 agent 从代码中移除 LinuxKPI，并重构所有内容。agent 一次性完成了这个任务，并更新了决策文档。

With specification, docs and a plan, the workflow process turned into a "boring routine". The agent had SSH access to both the build host, and a testing VM, that had been running with the Wi-Fi PCI device passed from the host. It methodically crunch through the backlog of its own milestones, iterating over the code, building and testing the module. Every time a milestone or a portion was finished, I asked the agent to record the progress to the docs. Occasionally, an iteration of the code crashed or hanged the VM. When this happened, before fixing the problem, I asked — in a forked Pi's session — to summarize, investigate and record the problem for agent's future-self.

有了规范、文档和计划，工作流程变成了"枯燥的例行公事"。agent 对构建主机和测试虚拟机都有 SSH 访问权限，测试虚拟机运行时将 Wi-Fi PCI 设备从主机直通过来。它有条不紊地处理自己里程碑的积压任务，迭代代码，构建和测试模块。每当完成一个里程碑或一部分时，我要求 agent 将进度记录到文档中。偶尔，某次代码迭代会导致虚拟机崩溃或挂起。当这种情况发生时，在修复问题之前，我要求在分叉的 Pi 会话中总结、调查并记录问题，供 agent 的"未来自己"参考。

After many low-involved sessions, I got a working FreeBSD kernel module for the BCM4350 Wi-Fi chip. The module supports Wi-Fi network scanning, 2.4GHz/5GHz connectivity, WPA/WPA2 authentication.

经过许多低参与度的会话后，我获得了一个可以工作的 BCM4350 Wi-Fi 芯片 FreeBSD 内核模块。该模块支持 Wi-Fi 网络扫描、2.4GHz/5GHz 连接、WPA/WPA2 认证。

[https://bsky.app/profile/vladimir.varank.in/post/3mfhnvunnr22d](https://bsky.app/profile/vladimir.varank.in/post/3mfhnvunnr22d)

The source code is in repository [github.com/narqo/freebsd-brcmfmac](https://github.com/narqo/freebsd-brcmfmac). I didn't write any piece of code there. There are several known issues, which I will task the agent to resolve, eventually. Meanwhile, I strongly advise against using it for anything beyond a studying exercise.

源代码位于仓库 [github.com/narqo/freebsd-brcmfmac](https://github.com/narqo/freebsd-brcmfmac)。我在那里没有写任何代码。有几个已知问题，我最终会让 agent 去解决。同时，我强烈建议不要将其用于学习练习之外的任何用途。

---

## 批判性思考与评论

这篇文章展示了 AI 辅助编程的一个有趣案例研究，值得我们深入思考：

**1. 从"直接移植"到"规范驱动"的方法论转变**
作者的第一阶段尝试（直接用 AI 移植代码）失败了，而第二阶段（先写规范，再重新实现）成功了。这揭示了一个重要的软件工程原则：对于复杂系统，"理解问题"比"急于编码"更重要。AI 在处理大规模、复杂的遗留代码移植时容易陷入细节泥潭，但通过规范驱动的方式，可以将问题分解为更可控的模块。

**2. AI 作为"协作者"而非"替代者"**
值得注意的是，作者始终处于决策者的位置：决定使用哪个模型、要求 AI 记录决策点、让 AI 在编码前提出问题等。最成功的 AI 编程案例往往是这种人机协作模式，而不是完全交给 AI 自主完成。

**3. "验证链"的重要性**
作者使用多个 AI 模型（Claude、Codex、Opus、Gemini）进行交叉验证，特别是让不同的模型来验证规范的正确性。这在当前 AI 容易产生"幻觉"的现实下是一个明智的做法。源代码作为" ground truth"的概念在这里被反复强调。

**4. 技术债务的考量**
虽然作者成功构建了一个工作驱动，但他明确警告不要用于生产环境。AI 生成的代码可能存在隐藏的问题、不符合最佳实践，或缺乏充分的边界情况处理。这提醒我们：AI 可以加速原型开发，但生产级代码仍需要专业审查。

**5. 关于 Gemini 的观察**
作者提到 Gemini"幻觉最严重"，这个观察很有趣。不同模型在不同任务上的表现差异很大，选择合适的工具对于 AI 辅助编程至关重要。

**6. 文档的价值**
AGENTS.md 和决策文档的使用展示了在 AI 项目中维护上下文的重要性。由于 AI 没有持久的"记忆"，良好的文档成为保持项目一致性的关键。

总的来说，这篇文章提供了一个现实的视角：AI 确实可以完成复杂的系统级编程任务，但成功需要正确的方法论、人类的监督和多层验证机制。它不是魔法，而是一种需要学习和掌握的新工具。
