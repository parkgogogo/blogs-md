URL: https://blog.onepatchdown.net/2026/02/22/are-compilers-deterministic-nerd-version/

## Are Compilers Deterministic?

编译器是确定性的吗？

Betteridge says "no," and for normal developer experience that answer is mostly right.

Betteridge 说"不"，对于正常的开发者体验来说，这个答案大体是正确的。

Here's my take. There's a computer science answer and an engineering answer. The computer science answer: a compiler is deterministic as a function of its full input state. Engineering answer: most real builds do not control the full input state, so outputs drift.

这是我的看法。有一个计算机科学答案和一个工程答案。计算机科学答案：编译器作为其完整输入状态的函数是确定性的。工程答案：大多数真实构建并不控制完整的输入状态，因此输出会漂移。

I worked at Ksplice back in the 2000s, where we patched running Linux kernels in RAM so you could take security updates without rebooting. Reading objdump output of crashy kernels was not daily routine, but I had to do it often enough that "compiler output versus source intent" stopped being theoretical.

2000 年代我在 Ksplice 工作，我们在 RAM 中修补运行的 Linux 内核，这样你就可以在不重启的情况下应用安全更新。阅读崩溃内核的 objdump 输出不是日常工作，但我不得不经常这样做，以至于"编译器输出与源代码意图"不再是理论问题。

Formally:

形式上：

artifact = F(
 source,
 flags,
 compiler binary,
 linker + assembler,
 libc + runtime,
 env vars,
 filesystem view,
 locale + timezone,
 clock,
 kernel behavior,
 hardware/concurrency schedule
)

产物 = F(
 源代码,
 编译标志,
 编译器二进制文件,
 链接器 + 汇编器,
 libc + 运行时,
 环境变量,
 文件系统视图,
 区域设置 + 时区,
 时钟,
 内核行为,
 硬件/并发调度
)

Most teams hold only source and maybe flags constant, then call everything else "noise." That "noise" is where non-reproducibility lives.

大多数团队只保持源代码和可能的编译标志不变，然后称其他一切为"噪音"。这种"噪音"就是不可重现性存在的地方。

## Compiler Contract: Semantics, Not Byte Identity

编译器契约：语义，而非字节身份

The commenter is right on this point: compilers are expected to preserve semantics. For programs with defined behavior, the output should be observationally equivalent to the source language's abstract machine.

评论者在这点上是对的：编译器应该保留语义。对于有定义行为的程序，输出应该在观察上与源代码语言的抽象机等价。

That means instruction order, register choice, inlining strategy, and block layout are fair game as long as externally visible behavior stays the same. In practice, "visible behavior" means things like I/O effects, volatile accesses, atomic synchronization guarantees, and defined return values, not byte-for-byte instruction identity.

这意味着指令顺序、寄存器选择、内联策略和块布局都是可变的，只要外部可见行为保持不变。在实践中，"可见行为"意味着 I/O 效果、volatile 访问、原子同步保证和定义的返回值，而不是逐字节的指令身份。

## Where Entropy Comes From

熵来自哪里

- __DATE__, __TIME__, __TIMESTAMP__
- embedded absolute paths in DWARF/debug info
- build path leakage (for example /home/fragmede/projects/foo)
- locale-sensitive sort behavior (LC_ALL)
- filesystem iteration order
- parallel build and link race ordering
- archive member order and metadata (ar, ranlib)
- build IDs, UUIDs, random seeds
- network fetches during build
- toolchain version skew
- host kernel/c library differences
- historical compiler internals depending on unstable pointer/hash traversal order

- __DATE__, __TIME__, __TIMESTAMP__
- DWARF/调试信息中嵌入的绝对路径
- 构建路径泄漏（例如 /home/fragmede/projects/foo）
- 区域设置敏感的排序行为 (LC_ALL)
- 文件系统迭代顺序
- 并行构建和链接竞争排序
- 归档成员顺序和元数据 (ar, ranlib)
- 构建 ID、UUID、随机种子
- 构建期间的网络获取
- 工具链版本差异
- 主机内核/c 库差异
- 依赖于不稳定指针/哈希遍历顺序的历史编译器内部实现

So "compilers are deterministic" is often true in a theorem sense and false in an operational sense.

所以"编译器是确定性的"在定理意义上经常是正确的，在操作意义上是错误的。

---

**批判性思考评论：**

这篇文章澄清了关于编译器确定性的一个常见误解。作者区分了三个层次的概念：

1. **确定性编译器**：相同的完整输入元组 → 相同的输出
2. **可重现构建**：两个独立的构建者重新创建逐位相同的输出
3. **可靠工具链**：差异在功能上很少重要

这是三个相关但不同的保证。

作者的核心论点是：虽然编译器在理论上是确定性的（作为其完整输入状态的函数），但在工程实践中，"完整输入状态"包括比大多数人意识到的多得多的因素——从环境变量到文件系统迭代顺序，从时区到硬件调度。

对 AI 时代的启示：
- 当我们使用 AI 智能体生成代码时，如果构建过程本身不可重现，"代码是否正确"的定义就会变得模糊
- 可重现构建不仅是安全需求（防止供应链攻击），也是开发效率需求（确保 AI 生成的代码在不同环境中行为一致）

这篇文章提醒我们：软件工程中的许多"显然"真理，在实践中往往更加微妙。
