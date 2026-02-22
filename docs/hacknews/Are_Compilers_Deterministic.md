URL: https://blog.onepatchdown.net/2026/02/22/are-compilers-deterministic-nerd-version/

Betteridge's law of headlines says "no," and for the ordinary developer experience, that's roughly correct. (And you're absolutely right! Here's an em-dash—so you know I had ChatGPT help me write this.)

Betteridge定律说"不是"，对于普通开发者体验来说，这个答案大体上是正确的。（而且你说得完全对！这里还有一个破折号——这样你就知道我用ChatGPT帮我写这篇文章了。）

Here is my thesis. There is a computer science answer, and there is an engineering answer. The computer science answer is: compilers are deterministic as a function of their complete input state. The engineering answer is: most real build processes do not control the complete input state, and so the output drifts.

以下是我的观点。有一个计算机科学的答案，也有一个工程学的答案。计算机科学的答案是：编译器作为其完整输入状态的函数，是确定性的。工程学的答案是：大多数真实的构建过程并没有控制完整的输入状态，因此输出会发生漂移。

I worked at Ksplice in the 2000s, where we patched running Linux kernel RAM to let you apply security updates without rebooting. Reading crash kernel objdump output isn't daily routine, but I had to do it often enough that "compiler output vs. source intent" stopped being a purely theoretical concern.

我在2000年代曾在Ksplice工作，我们在那里修补运行中的Linux内核RAM，让你可以在不重启的情况下应用安全更新。阅读崩溃内核的objdump输出并非日常例行工作，但我经常不得不这样做，以至于"编译器输出与源代码意图"不再只是理论上的问题。

Formally:

形式上：

Artifact = F(
  source code,
  compiler flags,
  compiler binary,
  linker + assembler,
  libc + runtime libraries,
  environment variables,
  filesystem view,
  locale + timezone,
  clock,
  kernel behavior,
  hardware/concurrency scheduling
)

产物 = F(
  源代码,
  编译选项,
  编译器二进制文件,
  链接器 + 汇编器,
  libc + 运行时库,
  环境变量,
  文件系统视图,
  区域设置 + 时区,
  时钟,
  内核行为,
  硬件/并发调度
)

Most teams keep the source code and maybe the compiler flags stable, then call everything else "noise." That "noise" is where non-reproducibility lives.

大多数团队只保持源代码和可能的编译选项不变，然后把其他一切都称为"噪音"。那个"噪音"就是非可复制性存在的地方。

I learned this the hard way at Ksplice in the 2000s. We generated rebootless Linux kernel updates by diffing old vs. new compiler output and hot-patching the differences into live kernel memory. Most diffs mapped cleanly to changed C code. But sometimes they would explode for reasons unrelated to semantic source changes: register allocation differences, optimization pass behavior changes, section/layout changes. Same intent, different machine code.

我在2000年代在Ksplice艰难地学到了这一点。我们通过比较新旧编译输出的差异来生成无需重启的Linux内核更新，并将热补丁缝入实时内核内存。大多数差异都能清晰地映射到变更的C代码。但有时它们会因为非语义源代码变更的原因而爆炸：寄存器分配差异、优化遍行为改变、节区/布局变更。相同的意图，不同的机器码。

If you want a concrete historical case, GCC bug 18574 has a gcc-bugs mailing list discussion pointing to pointer hash instability affecting traversal order, and SSA coalescing issues.

如果你想要一个具体的历史案例，GCC bug 18574有一个gcc-bugs邮件列表讨论，指出了影响遍历顺序的指针哈希不稳定性，以及SSA合并的问题。

The distinction matters:

这种区别很重要：

- Deterministic compiler: same complete input tuple → same output
- Reproducible build: two independent builders create bit-identical output
- Reliable toolchain: differences are functionally unimportant

- 确定性编译器：相同的完整输入元组 -> 相同的输出
- 可复现构建：两个独立的构建者创建逐位相同的输出
- 可靠工具链：差异在功能上很少重要

Related concepts, inequivalent guarantees.

相关概念，不等同的保证。

## Compiler Contract: Semantics, Not Byte Identity / 编译器契约：语义，而非字节一致性

The commenter is right about this: compilers are supposed to preserve semantics. For programs with defined behavior, output should be observationally equivalent to the source language's abstract machine.

评论者在这点上是对的：编译器应该保持语义。对于具有定义行为的程序，输出应该与源代码语言的抽象机在观察上等价。

This means instruction ordering, register selection, inlining decisions, and block layout are all fair game to change as long as externally visible behavior is preserved. In practice, "visible behavior" means I/O effects, volatile accesses, atomic synchronization guarantees, and defined return values—not per-instruction byte identity.

这意味着指令顺序、寄存器选择、内联策略和块布局都是可以调整的，只要外部可见的行为保持不变。在实践中，"可见行为"指的是I/O效果、易失性访问、原子同步保证和定义的返回值，而不是逐条指令的字节一致性。

Important caveats:

重要的注意事项：

- Undefined behavior weakens or voids semantic guarantees
- Timing, microarchitectural side channels, and exact memory layout are often outside the core language contract
- Reproducible builds are a stricter goal than semantic preservation (same bits, not just same behavior)

- 未定义行为会削弱或使语义保证失效
- 时序、微架构侧信道和确切的内存布局通常不在核心语言契约范围内
- 可复现构建是比语义保持更严格的目标（相同的位，而不仅仅是相同的行为）

## Where the Entropy Comes From / 熵从何而来

- __DATE__, __TIME__, __TIMESTAMP__
- Absolute paths embedded in DWARF/debug info
- Build path leakage (e.g., /home/fragmede/projects/foo)
- Locale-sensitive sorting behavior (LC_ALL)
- Filesystem iteration order
- Parallel build and link race ordering
- Archive member order and metadata (ar, ranlib)
- Build IDs, UUIDs, random seeds
- Network fetches during build
- Toolchain version differences
- Host kernel/C library differences
- Historical compiler internals relying on unstable pointer/hash traversal order

- __DATE__, __TIME__, __TIMESTAMP__

- DWARF/调试信息中嵌入的绝对路径

- 构建路径泄露（例如 /home/fragmede/projects/foo）

- 区域设置敏感的排序行为（LC_ALL）
- 文件系统迭代顺序
- 并行构建和链接的竞争排序
- 归档成员顺序和元数据（ar, ranlib）
- 构建ID、UUID、随机种子
- 构建期间的网络获取
- 工具链版本差异
- 宿主内核/C库差异
- 历史编译器内部依赖不稳定的指针/哈希遍历顺序

ASLR note: ASLR does not directly randomize produced binaries. It randomizes process memory layout. But if compiler pass behavior depends on pointer identity/ordering, ASLR can indirectly perturb results.

ASLR注：ASLR不会直接随机化生成的二进制文件。它随机化进程内存布局。但如果编译器遍的行为依赖于指针身份/顺序，ASLR可以间接地扰乱结果。

So "compilers are deterministic" is usually true in the theorem sense, and usually false in the operational sense.

所以"编译器是确定性的"在定理意义上通常是正确的，在操作意义上通常是错误的。

And even with reproducible artifacts, Ken Thompson's "Reflections on Trusting Trust" still applies. Also remember that compilers aren't exactly new technology: Grace Hopper's A-0 system dates to 1952 on UNIVAC. ChatGPT has only existed for 4 years; compilers have been around for 74?

而且即使有可复现的产物，Ken Thompson的《反思对信任的信任》仍然适用。还要记住，编译器并不是什么新技术：Grace Hopper的A-0系统可以追溯到1952年的UNIVAC。ChatGPT只存在了4年，而编译器已经74年了？

## Reproducible Builds: Deliberate Engineering Effort / 可复现构建：刻意的工程努力

Debian and the broader reproducible builds effort (starting roughly 2013) pushed this into the mainstream: same source + same build instructions should produce bit-identical artifacts.

Debian和更广泛的可复现构建工作（大约从2013年开始）将这一点推向了主流：相同的源代码 + 相同的构建指令应该产生逐位相同的产物。

Practical operational playbook:

实用的操作手册：

- Freeze toolchain and dependencies
- Stabilize environment (TZ=UTC, LC_ALL=C)
- Set SOURCE_DATE_EPOCH
- Normalize/strip volatile metadata
- Normalize path prefixes (-ffile-prefix-map, -fdebug-prefix-map)
- Deterministic archives (ar -D)
- Remove network from the build graph
- Build inside sealed containers/sandboxes
- Continuously diff artifacts across builders in CI

- 冻结工具链和依赖

- 稳定环境（TZ=UTC, LC_ALL=C）
- 设置 SOURCE_DATE_EPOCH

- 规范化/剥离易变元数据

- 规范化路径前缀（-ffile-prefix-map, -fdebug-prefix-map）

- 确定性归档（ar -D）
- 从构建图中移除网络
- 在封闭的容器/沙箱中构建
- 在CI中持续跨构建者比较产物差异

Then you get:

这样你就能得到：

- Repeatable
- Reproducible
- Verifiable
- Hermetic
- Deterministic

- 可重复的
- 可复现的
- 可验证的
- 封闭的
- 确定性的

Do we have this now? Broadly, yes, in many ecosystems. But it took years of very deliberate work across compilers, linkers, packaging, and build systems. We got here by grinding through weird edge cases one at a time, not by waving hands and declaring purity.

我们现在有了吗？在许多生态系统中，大体上是有的。但这花了数年时间，在编译器、链接器、打包和构建系统上进行了非常有意识的工作。我们是通过一点点地解决各种奇怪的边界情况才走到今天的，而不是挥挥手就宣布纯洁性。

## Why This Matters for LLMs / 为什么这对大语言模型很重要

Now this question appears in the form of "If LLMs are nondeterministic, does vibecoding even make sense?" Again: do you want the computer science answer, or the engineering answer?

现在这个问题以"如果大语言模型是非确定性的，那么vibecoding还有意义吗？"的形式出现。再说一遍：你想要计算机科学的答案，还是工程学的答案？

On LLMs, we have, and have not, solved the halting problem. We have not solved the halting problem in the formal sense at all. But for practical purposes, if I write a for-loop and get the condition wrong, an LLM can look at my code, tell me I'm being silly, and it can help me fix it.

关于大语言模型，我们已经、也还没有解决停机问题。我们在形式意义上根本没有解决停机问题。但在实际目的上，如果我写了一个for循环并把条件搞错了，大语言模型可以看着我的代码，告诉我我很傻，然后它可以帮我修复它。

Engineering never relied on perfectly deterministic intelligence. It relies on controlled interfaces, test oracles, reproducible pipelines, and observability. I believe in AI deeply enough to drive comma.ai every day, but I still want deterministic verification gates around the generated code. My girlfriend prefers I let it drive because it's smoother and less darty than I am, which is a useful reminder: "probabilistic system" and "operationally better outcome" can coexist.

工程学从不依赖完美确定性的智能。它依赖受控的接口、测试预言、可复现的流水线和可观察性。我对AI的信仰足够深，以至于每天开着comma.ai，但我仍然希望在生成的代码周围有确定性的验证关卡。我女朋友更喜欢我让它开车，因为它比我开得更平稳、更少飘忽，这是一个有用的提醒："概率系统"和"操作上更好的结果"可以共存。

The LLM-assisted coding pattern is the same:

大语言模型辅助编程也是同样的模式：

- Constrain inputs
- Make outputs testable
- Gate with deterministic CI
- Require reproducible artifacts
- Treat stochastic generation as upstream, not deployment-time truth

- 约束输入
- 使输出可测试
- 用确定性CI把关
- 要求可复现的产物
- 将随机生成视为上游，而非部署时的真相

Computer science answer: nondeterminism is scary.

计算机科学的答案：非确定性很可怕。

Engineering answer: control the boundary conditions, verify the outputs, ship.

工程学的答案：控制边界条件，验证输出，发布。

And yes, part of this argument is existential: most of us are still in the business of paying rent, not the business of philosophy. So we use tools that move the work forward, and then build the guardrails we need.

而且是的，这个论点的一部分是存在主义的：我们大多数人仍在从事支付房租的业务，而不是哲学业务。所以我们使用能够推动工作进展的工具，然后构建我们需要的护栏。

---

## 批判性思考评论 / Critical Thinking Commentary

### 作者的主要论点分析

本文作者提出了一个核心观点：编译器的"确定性"需要从两个维度来理解——理论上的计算机科学定义（相同输入产生相同输出）和工程实践中的现实（输入状态难以完全控制）。作者通过自己在Ksplice的工作经历，生动地说明了即使是相同的源代码意图，也可能因为编译环境的微小差异而产生不同的机器码输出。

作者进一步将这种分析框架延伸到当下热门的LLM（大语言模型）辅助编程讨论中，指出"非确定性"不应该成为拒绝使用新技术的理由，而应该通过工程手段（测试、CI、可复现构建）来管理和控制不确定性。

### 优点

1. **实践经验支撑**：作者以Ksplice的真实工作经历为例，使得抽象的技术概念变得具体可感。这种"战地记者"式的叙述比纯理论讨论更有说服力。

2. **概念辨析清晰**：文章明确区分了"确定性编译器"、"可复现构建"和"可靠工具链"三个相关但不同的概念，帮助读者建立更精确的思维模型。

3. **跨领域类比巧妙**：将编译器确定性的讨论与LLM辅助编程联系起来，展示了作者对技术发展趋势的敏锐洞察。这种类比不是牵强附会，而是基于"工程实践 vs 理论完美"这一共同主题。

4. **实用主义导向**：文章最后落脚于工程实践的现实需求（"支付房租的业务"），避免了陷入纯粹的理论空谈。

### 缺点与不足

1. **对编译器理论的最新进展关注不足**：文章提到GCC bug 18574（2004年）等历史案例，但对现代编译器（如LLVM、最新的GCC版本）在可复现构建方面取得的进展讨论不够深入。事实上，许多现代编译器已经将可复现构建作为核心目标。

2. **对ASLR影响的表述可能过度**：作者承认ASLR不会直接随机化二进制文件，但暗示它可能通过指针顺序间接影响编译结果。然而，这种影响在实际中极其罕见，且现代编译器通常会在设计上避免对指针值的依赖。

3. **LLM类比可能过于简化**：虽然类比有助于理解，但LLM的非确定性与编译器的非确定性在本质上是不同的——前者源于模型的概率性质和采样机制，后者源于环境因素的不可控。将两者简单类比可能掩盖了LLM特有的挑战（如幻觉、训练数据偏见等）。

4. **对安全性的讨论不足**：在讨论可复现构建时，作者提到了Ken Thompson的《反思对信任的信任》，但没有深入探讨可复现构建对于供应链安全的关键意义。在当前的软件供应链攻击频发的背景下，这一讨论显得尤为重要。

### 我的批判视角

我认为作者的核心论点——"工程学从不依赖完美确定性的智能"——是正确且有价值的，但这一观点需要更细致的限定。

首先，作者似乎低估了确定性在特定领域的重要性。在高安全性系统（如航空航天、医疗设备、金融基础设施）中，"可复现构建"不仅仅是工程便利性的问题，而是安全审计和故障排查的基础。在这些场景中，"相同的位"比"相同的行为"更重要，因为任何差异都可能引入难以追踪的漏洞。

其次，作者对LLM辅助编程的乐观态度可能需要更多的批判性审视。编译器的非确定性是"可控的"——通过冻结工具链和环境，我们可以实现确定性。但LLM的非确定性是"内生的"——源于其架构本身。这意味着我们无法通过简单的工程手段完全消除LLM输出的变异性。comma.ai的自动驾驶例子可能具有误导性：驾驶是一个容错性相对较高的场景（小误差不会立即导致灾难），但软件开发中的某些错误（如安全漏洞）可能具有灾难性的后果。

最后，我认为文章忽略了"确定性"的社会维度。可复现构建不仅仅是技术问题，它还关乎软件的自由、透明度和民主化。当软件构建过程无法复现时，用户和审计者就失去了验证软件真实性的能力，这实际上是一种权力的不对称。

### 启示与影响

这篇文章对于当前的技术讨论具有重要启示：

1. **技术评估需要双重视角**：在评估新技术（如LLM）时，我们既需要理解其理论局限性，也需要评估其在实际工程中的可用性。完美的敌人不应该成为好用的障碍。

2. **工程纪律的重要性**：无论工具如何变化，良好的工程实践（测试、CI、可观测性）始终是保证软件质量的基础。新工具不应该取代这些基础，而应该被这些基础所约束。

3. **可复现性作为基础设施**：可复现构建应该被视为软件工程的基础设施，而不仅仅是一个"锦上添花"的特性。这对于开源软件的信任、安全审计和长期维护都至关重要。

4. **对AI辅助开发的健康态度**：文章提供了一种对AI辅助开发的健康态度——既不盲目排斥其非确定性，也不过度依赖其输出，而是通过工程手段建立"护栏"。

总的来说，这是一篇富有洞察力且实用性强的文章，它提醒我们：在技术讨论中，区分"理论可能"和"工程现实"是至关重要的智慧。
