# FreeBSD doesn't have Wi-Fi driver for my old MacBook. AI built one for me

> Original: [FreeBSD doesn't have Wi-Fi driver for my old MacBook. AI built one for me](https://vladimir.varank.in/notes/2026/02/freebsd-brcmfmac/)  
> Author: Vladimir Varankin  
> Published: February 23, 2026

My old 2016 MacBook Pro has been collecting dust in a cabinet for some time now. The laptop suffers from a ["flexgate" problem](https://www.macrumors.com/guide/flexgate-macbook-pro-display-issue/), and I don't have any practical use for it. For quite some time, I've been thinking about repurposing it as a guinea pig, to play with FreeBSD — an OS that I'd aspired to play with for a long while, but had never had a real reason to.

During the recent holiday season, right after FreeBSD 15 release, I've finally found time to set the laptop up. Doing that I didn't plan, or even think, this may turn into a story about AI coding.

## Background

2016 MacBook Pro models use Broadcom BCM4350 Wi-Fi chip and FreeBSD doesn't support it natively. To have a working Wi-Fi, a typical suggestion on FreeBSD forums, is to run wifibox — a tiny Linux VM, with the PCI Wi-Fi device in pass through, that allows Linux to manage the device through its brcmfmac driver.

Brcmfmac is a Linux driver (ISC licence) for set of FullMAC chips from Broadcom. The driver offloads the processing jobs, like 802.11 frame movement, WPA encryption and decryption, etc, to the firmware, which is running inside the chip. Meanwhile, the driver and the OS do high-level management work (ref [Broadcom brcmfmac(PCIe) in Linux Wireless documentation](https://wireless.docs.kernel.org/en/latest/en/users/drivers/brcm80211.html)).

Say we want to build a native FreeBSD kernel module for BCM4350. In theory, the separation of jobs between the firmware and the driver sounds perfect. The "management" part of work is what FreeBSD already does for other Wi-Fi devices it supports. What's left is to port some amount of existing "glue code" from the specifics of Linux to FreeBSD. If we ignore a lot of details, the problem doesn't sound too complicated, right?

## Act 1

A level-zero idea, when one hears about "porting a bunch of existing code from A to B", in 2026 is, of course, to use AI. So that was what I tried.

I cloned the brcmfmac subtree from Linux, and asked Claude Code to make it work for FreeBSD. FreeBSD already has drivers that work through LinuxKPI — compatibility layer for running Linux kernel drivers. So I specifically pointed Claude at the iwlwifi driver (a softmac driver for Intel wireless network card), asking "do as they did it". And, at first, this even looked like this can work — Claude told me so.

![Bluesky post 1](http://vladimir.varank.in/images/2026/bsky-freebsd-brcmfmac-1.png)

The module, indeed, compiled, but it didn't do anything. Because, of course: the VM, where we tested the module, didn't even have the hardware. After I set the PCI device into the VM, and attempted to load the driver against the chip, the challenges started to pop up immediately. The kernel paniced, and after Claude fixed the panics, it discovered that "module didn't do anything". Claude honestly tried to sift through the code, adding more and more `#ifdef __FreeBSD__` wrappers here and there. It complained about missing features in LinuxKPI. The module kept causing panics, and the agent kept building FreeBSD-specific shims and callbacks, while warning me that this project will be very complicated and messy.

## Act 2

After a number of sessions, the diff, produced by the agent, stared to look significantly larger than what I'd hoped it will be. Even worse, the driver didn't look even close to be working. This was right around time when Armin Ronacher posted about his experience [building a game from scratch with Claude Opus and PI agent](https://youtu.be/ANQ1IYsFM2s?si=GP6oVkBN-5_hmIFM).

Besides the part that working in [Pi coding agent](https://pi.dev/) feels more productive, than in Claude Code, the video got me thinking that my approach to the task was too straightforward. The code of brcmfmac driver is moderately large. The driver supports several generations of Wi-Fi adaptors, different capabilities, etc. But my immediate task was very narrow: one chip, only PCI, only Wi-Fi client.

Instead of continuing with the code, I spawned a fresh Pi session, and asked the agent to write a detailed specification of how the brcmfmac driver works, with the focus on BCM4350 Wi-Fi chip. I explicitly set the audience for the specification to be readers, who are tasked with implementing the specification in a clean-room environment. I asked the agent to explain how things work "to the bits". I added some high-level details for how I wanted the specification to be laid out, and let the agent go brrrr.

After a couple of rounds, the agent produced me a "book of 11 chapters", that honestly looked like a fine specification:

```
spec/
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

To proofread the spec I spawned a clean Pi sessions, and — for fun — asked Codex model, to read the specification, and flag any places, where the text isn't aligned with the driver's code (_"Source code is the ground truth. The spec needs to be verified, and updated with any missing or wrong details"_). The agent followed through and found several places to fix, and also proposed multiple improvements.

Of course, one can't just trust what AI has written, even if this was in a proofreading session.

To double-proofread the fixes I spawned another clean Pi sessions, asking Opus model to verify if what was proposed was aligned with how it works in the code of the driver.

> As a procrastination exercise, I tried this loop with a couple of coding models: Opus 4.5, Opus 4.6, Codex 5.2, Gemini 3 Pro preview. So far my experience was that Gemini hallucinated the most. This was quite sad, given that the model itself isn't too bad for simple coding tasks, and it is free for a limited use.

Having a written specification should have (in theory) explained how a driver's code interacts with the firmware.

## Act 3

I started a fresh project, with nothing but the mentioned "spec", and prompted the Pi agent, that we were building a brand new FreeBSD driver for BCM4350 chip. I pointed the agent to the specification, and asked it to ask me back about any important decisions we must make, and details we must outline, before jumping into "slopping the code". The agent came back with questions and decision points, like "Will the driver live in the kernels source-tree?", "Will we write the code in C?", "Will we rely on LinuxKPI?", "What are our high-level milestones?", etc. One influential bit, that turned fairly productive moving forward, was that I asked the agent to document all these decision points in the project's docs, and to explicitly referenced to these decision docs in the project's AGENTS.md.

* * *

It's worth saying that, just like in any real project, not all decisions stayed to the end. For example,

Initially I asked the agent to build the driver using `linuxkpi` and `linuxkpi_wlan`. My naive thinking was that, given the spec was written after looking at Linux driver's code, it might be simpler for the agent, than building the on top of the native primitives. After a couple of sessions, it didn't look like this was the case. I asked the agent to drop LinuxKPI from the code, and to refactor everything. The agent did it in one go, and updated the decision document.

With specification, docs and a plan, the workflow process turned into a "boring routine". The agent had SSH access to both the build host, and a testing VM, that had been running with the Wi-Fi PCI device passed from the host. It methodically crunched through the backlog of its own milestones, iterating over the code, building and testing the module. Every time a milestone or a portion was finished, I asked the agent to record the progress to the docs. Occasionally, an iteration of the code crashed or hanged the VM. When this happened, before fixing the problem, I asked — in a forked Pi's session — to summarize, investigate and record the problem for agent's future-self.

After many low-involved sessions, I got a working FreeBSD kernel module for the BCM4350 Wi-Fi chip. The module supports Wi-Fi network scanning, 2.4GHz/5GHz connectivity, WPA/WPA2 authentication.

![Bluesky post 2](http://vladimir.varank.in/images/2026/bsky-freebsd-brcmfmac-2.png)

The source code is in repository [github.com/narqo/freebsd-brcmfmac](https://github.com/narqo/freebsd-brcmfmac). I didn't write any piece of code there. There are several known issues, which I will task the agent to resolve, eventually. Meanwhile, I advise against using it for anything beyond a studying exercise.

* * *

Hacker News spawned an [existential discussion](https://news.ycombinator.com/item?id=47129361) following this note, where comments are clustering around several points:

1. **Is the driver's code licensed accurately?**

Really, this isn't the battle I choose to participate in. If there is an explanation for how to properly license this type of code artefact, I can follow through.

The agent didn't put any license for me, by default. Choosing a license was yet another decision, that is [documented](https://github.com/narqo/freebsd-brcmfmac/blob/be9b49c1bf9425966cedd97bf7952f6d9b6ed988/docs/01-decisions.md#license) for the agent to follow, in the future iterations. Today, the code in freebsd-brcmfmac uses ISC license, because this is what the original code of brcmfmac Linux driver uses.

2. **Is there a value here when the driver "isn't done" yet?**

In software engineering, there aren't many things that are "done". We produce code. Others find bugs, security vulnerabilities, corner cases, and so on. We iterate. AI coding hasn't changed these fundamentals — not by 2026, at least. Agents speeded up the part of producing code, just like other toolings have been speeding up the process of collaborating, finding bugs, etc.

Is there "value" in the driver today? Probably not. Is there "value" in my outdated and broken MacBook? Not much. Was it insightful for me to walk the journey from "claude can't just take the code and port it" to "agent needs to plan, record, iterate in order to progress" (_and doing that didn't mean that I had to write a ton of markdown essays myself_)? Yes.

---

# 我的旧 MacBook 没有 FreeBSD Wi-Fi 驱动。AI 帮我写了一个

> 原文：[FreeBSD doesn't have Wi-Fi driver for my old MacBook. AI built one for me](https://vladimir.varank.in/notes/2026/02/freebsd-brcmfmac/)  
> 作者：Vladimir Varankin  
> 发布时间：2026年2月23日

我那台2016年的旧 MacBook Pro 已经在柜子里积灰好一阵子了。这台笔记本有["flexgate" 排线门问题](https://www.macrumors.com/guide/flexgate-macbook-pro-display-issue/)，对我来说已经没什么实用价值了。很长一段时间以来，我一直在考虑把它当实验品，用来玩 FreeBSD —— 这个我一直想玩但从来没有真正理由去玩的操作系统。

在刚过去的假期里，FreeBSD 15 发布之后，我终于抽出时间来配置这台笔记本。我原本没计划，甚至没想到这会变成一个关于 AI 编程的故事。

## 背景

2016款 MacBook Pro 使用的是 Broadcom BCM4350 Wi-Fi 芯片，而 FreeBSD 原生不支持它。为了在 FreeBSD 上使用 Wi-Fi，论坛上典型的建议是运行 wifibox —— 一个微型 Linux 虚拟机，通过 PCI 直通把 Wi-Fi 设备交给 Linux，让 Linux 用它的 brcmfmac 驱动来管理设备。

Brcmfmac 是 Linux 的一个驱动（ISC 许可证），用于 Broadcom 的一系列 FullMAC 芯片。这个驱动把处理工作（如 802.11 帧传输、WPA 加解密等）卸载给在芯片内部运行的固件。同时，驱动和操作系统负责高层管理工作（参考 [Linux Wireless 文档中的 Broadcom brcmfmac(PCIe)](https://wireless.docs.kernel.org/en/latest/en/users/drivers/brcm80211.html)）。

假设我们想为 BCM4350 构建一个原生的 FreeBSD 内核模块。理论上，固件和驱动之间的职责分离听起来很完美。"管理"部分的工作正是 FreeBSD 为其他支持的 Wi-Fi 设备所做的事情。剩下的就是把一些现有的"胶水代码"从 Linux  specifics 移植到 FreeBSD。如果我们忽略很多细节，这个问题听起来不算太复杂，对吧？

## 第一幕

当听到"把一堆现有代码从 A 移植到 B"时，2026年的第一反应当然是用 AI。所以我就是这么尝试的。

我从 Linux 克隆了 brcmfmac 子树，让 Claude Code 把它改成能在 FreeBSD 上运行。FreeBSD 已经有通过 LinuxKPI（运行 Linux 内核驱动的兼容层）工作的驱动了。所以我特意让 Claude 参考 iwlwifi 驱动（Intel 无线网卡的 softmac 驱动），告诉它"照着他们的做法做"。起初，这看起来甚至能行 —— Claude 是这么跟我说的。

![Bluesky 帖子 1](http://vladimir.varank.in/images/2026/bsky-freebsd-brcmfmac-1.png)

模块确实编译通过了，但什么都没发生。因为很显然：我们测试模块的虚拟机根本没有那块硬件。在我把 PCI 设备配置进虚拟机后，尝试加载驱动到芯片上，挑战立刻开始涌现。内核 panic 了，Claude 修好 panic 后，发现"模块什么都没做"。Claude 诚实地尝试梳理代码，到处添加越来越多的 `#ifdef __FreeBSD__` 包装器。它抱怨 LinuxKPI 缺少功能。模块不断引起 panic，agent 不断构建 FreeBSD 特定的垫片和回调，同时警告我这个项目会非常复杂和混乱。

## 第二幕

经过几次会话后，agent 生成的 diff 看起来比我预期的大得多。更糟糕的是，驱动看起来离能工作还差得远。就在那个时候，Armin Ronacher 发布了他 [用 Claude Opus 和 Pi agent 从零开始开发游戏](https://youtu.be/ANQ1IYsFM2s?si=GP6oVkBN-5_hmIFM) 的经历。

除了在 [Pi coding agent](https://pi.dev/) 里工作感觉比 Claude Code 更高效之外，这个视频让我意识到我的方法太直接了。brcmfmac 驱动的代码量中等偏大。这个驱动支持好几代 Wi-Fi 适配器、不同的功能等。但我的直接任务非常狭窄：一个芯片、仅 PCI、仅 Wi-Fi 客户端。

我没有继续折腾代码，而是开启了一个全新的 Pi 会话，让 agent 写一份详细的规范文档，说明 brcmfmac 驱动是如何工作的，重点聚焦在 BCM4350 Wi-Fi 芯片上。我明确把规范的受众设定为那些要在"洁净室"环境中实现该规范的读者。我让 agent 把工作原理"深入到比特级别"地解释清楚。我添加了一些关于规范结构的高层要求，然后让 agent 开始工作。

几轮之后，agent 给我产出了"11章的书"，坦白说看起来像是一份不错的规范：

```
spec/
├── 00-overview.md              # 概述
├── 01-data-structures.md       # 数据结构
├── 02-bus-layer.md             # 总线层
├── 03-protocol-layer.md        # 协议层
├── 04-firmware-interface.md    # 固件接口
├── 05-event-handling.md        # 事件处理
├── 06-cfg80211-operations.md   # cfg80211 操作
├── 07-initialization.md        # 初始化
├── 08-data-path.md             # 数据路径
├── 09-firmware-commands.md     # 固件命令
└── 10-structures-reference.md  # 结构体参考
```

当然，不能完全相信 AI 写的东西。

为了校对规范，我开启了一个干净的 Pi 会话，然后 —— 为了好玩 —— 让 Codex 模型阅读这份规范，标记出任何与驱动代码不一致的地方（"源代码是唯一的真理。规范需要被验证，并用任何缺失或错误的细节更新"）。Agent 照做了，发现了几处需要修复的地方，还提出了多个改进建议。

当然，即使在校对环节，也不能完全相信 AI 写的东西。

为了双重校对修复内容，我又开启了一个干净的 Pi 会话，让 Opus 模型验证提议的修改是否与驱动代码的实际工作方式一致。

> 作为拖延症练习，我用几个编程模型尝试了这个循环：Opus 4.5、Opus 4.6、Codex 5.2、Gemini 3 Pro preview。到目前为止我的经验是 Gemini 幻觉最严重。这挺遗憾的，因为模型本身做简单编码任务还不错，而且有限使用是免费的。

有了书面规范（理论上）应该能解释驱动代码如何与固件交互。

## 第三幕

我开启了一个全新的项目，只有那份"规范"，然后提示 Pi agent：我们在为 BCM4350 芯片构建一个全新的 FreeBSD 驱动。我把规范指向 agent，让它向我反馈任何我们必须做出的重要决定，以及我们在一头扎进"糊代码"之前必须明确的细节。Agent 反馈了问题和决策点，比如"驱动会放在内核源代码树里吗？"、"我们用 C 语言写吗？"、"我们会依赖 LinuxKPI 吗？"、"我们的高层里程碑是什么？"等等。其中一个后来证明相当有成效的关键点是，我让 agent 把所有的决策点都记录在项目的文档里，并在项目的 AGENTS.md 中明确引用这些决策文档。

* * *

值得一提的是，就像任何真实项目一样，并非所有决定都坚持到了最后。比如，

最初我让 agent 用 `linuxkpi` 和 `linuxkpi_wlan` 来构建驱动。我天真的想法是，既然规范是看了 Linux 驱动代码之后写的，对 agent 来说可能比基于原生原语构建更简单。几次会话后，看起来并不是这么回事。我让 agent 从代码中移除 LinuxKPI，重构所有内容。Agent 一次性完成了，并更新了决策文档。

有了规范、文档和计划，工作流程变成了"无聊的例行公事"。Agent 有 SSH 访问权限，可以同时访问构建主机和测试虚拟机（测试 VM 运行着从主机透传过来的 Wi-Fi PCI 设备）。它有条不紊地处理自己的里程碑待办清单，迭代代码，构建和测试模块。每次完成一个里程碑或一部分功能，我都让 agent 把进度记录到文档中。偶尔，某次代码迭代会崩溃或卡死 VM。当这种情况发生时，在修复问题之前，我会 —— 在一个 fork 出来的 Pi 会话中 —— 总结、调查并记录问题，供 agent 的"未来自己"参考。

经过许多次低参与度的会话后，我得到了一个能工作的 BCM4350 Wi-Fi 芯片 FreeBSD 内核模块。该模块支持 Wi-Fi 网络扫描、2.4GHz/5GHz 连接、WPA/WPA2 认证。

![Bluesky 帖子 2](http://vladimir.varank.in/images/2026/bsky-freebsd-brcmfmac-2.png)

源代码在仓库 [github.com/narqo/freebsd-brcmfmac](https://github.com/narqo/freebsd-brcmfmac) 中。我没有写任何一行代码。还有一些已知问题，我最终会交给 agent 去解决。同时，我建议除了学习练习之外不要用于其他任何用途。

* * *

Hacker News 在这篇文章之后引发了[一场存在主义讨论](https://news.ycombinator.com/item?id=47129361)，评论主要集中在几个点上：

**1. 驱动代码的许可证是否准确？**

说真的，这不是我选择参与的战斗。如果有关于如何正确给这类代码产物授权的解释，我可以照做。

Agent 默认没有帮我加任何许可证。选择许可证是另一个决策，它被[记录在文档中](https://github.com/narqo/freebsd-brcmfmac/blob/be9b49c1bf9425966cedd97bf7952f6d9b6ed988/docs/01-decisions.md#license)，供 agent 在未来的迭代中遵循。目前，freebsd-brcmfmac 的代码使用 ISC 许可证，因为这是原始 brcmfmac Linux 驱动所用的许可证。

**2. 驱动还没"完成"，这里有什么价值？**

在软件工程中，没有多少东西是"完成"的。我们生产代码。其他人发现 bug、安全漏洞、边界情况，等等。我们迭代。AI 编程没有改变这些基本原则 —— 至少到2026年还没有。Agent 加速了代码生产这部分，就像其他工具一直在加速协作、发现 bug 等过程一样。

这个驱动今天有"价值"吗？可能没有。我那台过时且坏了的 MacBook 有"价值"吗？没多少。对我来说，走这段从"Claude 不能直接拿代码来移植"到"agent 需要规划、记录、迭代才能进展"的旅程有洞察力吗（而且这样做并不意味着我必须自己写一大堆 markdown 文档）？是的。
