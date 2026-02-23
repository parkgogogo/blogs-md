URL: http://www.righto.com/2026/02/8087-instruction-decoding.html

## Instruction decoding in the Intel 8087 floating-point chip

Intel 8087 浮点芯片中的指令解码

In the 1980s, if you wanted your IBM PC to run faster, you could buy the Intel 8087 floating-point coprocessor chip. With this chip, CAD software, spreadsheets, flight simulators, and other programs were much speedier. The 8087 chip could add, subtract, multiply, and divide, of course, but it could also compute transcendental functions such as tangent and logarithms, as well as provide constants such as π. In total, the 8087 added 62 new instructions to the computer.

在 1980 年代，如果你想让你的 IBM PC 运行得更快，你可以购买 Intel 8087 浮点协处理器芯片。有了这块芯片，CAD 软件、电子表格、飞行模拟器和其他程序运行速度都会快得多。8087 芯片当然可以进行加减乘除，但它还能计算超越函数，如正切和对数，以及提供诸如 π 之类的常数。总的来说，8087 为计算机增加了 62 条新指令。

But how does a PC decide if an instruction was a floating-point instruction for the 8087 or a regular instruction for the 8086 or 8088 CPU? And how does the 8087 chip interpret instructions to determine what they mean? It turns out that decoding an instruction inside the 8087 is more complicated than you might expect. The 8087 uses multiple techniques, with decoding circuitry spread across the chip. In this blog post, I'll explain how these decoding circuits work.

但是 PC 如何决定一条指令是给 8087 的浮点指令，还是给 8086 或 8088 CPU 的普通指令呢？8087 芯片如何解释指令以确定它们的含义？事实证明，在 8087 内部解码指令比你想象的更复杂。8087 使用多种技术，解码电路分布在芯片各处。在这篇博客文章中，我将解释这些解码电路的工作原理。

To reverse-engineer the 8087, I chiseled open the ceramic package of an 8087 chip and took numerous photos of the silicon die with a microscope. The complex patterns on the die are formed by its metal wiring, as well as the polysilicon and silicon underneath.

为了对 8087 进行逆向工程，我凿开了一块 8087 芯片的陶瓷封装，并用显微镜对硅晶圆拍摄了多张照片。晶圆上的复杂图案由其金属布线以及下方的多晶硅和硅形成。

The bottom half of the chip is the "datapath", the circuitry that performs calculations on 80-bit floating point values. At the left of the datapath, a constant ROM holds important constants such as π. At the right are the eight registers that the programmer uses to hold floating-point values; in an unusual design decision, these registers are arranged as a stack. Floating-point numbers cover a huge range by representing numbers with a fractional part and an exponent; the 8087 has separate circuitry to process the fractional part and the exponent.

芯片的下半部分是"数据通路"，即对 80 位浮点值进行计算的电路。在数据通路的左侧，一个常量 ROM 存储着重要的常数，如 π。在右侧是程序员用来保存浮点值的八个寄存器；在一个不寻常的设计决策中，这些寄存器被安排成一个栈。浮点数通过用分数部分和指数来表示数字，从而覆盖巨大的范围；8087 有单独的电路来处理分数部分和指数。

## Cooperation with the main 8086/8088 processor

与主 8086/8088 处理器的协作

The 8087 chip acted as a coprocessor with the main 8086 (or 8088) processor. When a floating-point instruction was encountered, the 8086 would let the 8087 floating-point chip carry out the floating-point instruction. But how do the 8086 and the 8087 determine which chip executes a particular instruction?

8087 芯片作为主 8086（或 8088）处理器的协处理器。当遇到浮点指令时，8086 会让 8087 浮点芯片执行该浮点指令。但 8086 和 8087 如何确定哪个芯片执行特定指令呢？

You might expect the 8086 to tell the 8087 when it should execute an instruction, but this cooperation turns out to be more complicated. The 8086 has eight opcodes that are assigned to the coprocessor, called ESCAPE opcodes. The 8087 determines what instruction the 8086 is executing by watching the bus, a task performed by the BIU (Bus Interface Unit).

你可能期望 8086 告诉 8087 何时执行指令，但这种协作实际上更复杂。8086 有八个分配给协处理器的操作码，称为 ESCAPE 操作码。8087 通过监视总线来确定 8086 正在执行什么指令，这项任务由 BIU（总线接口单元）执行。

---

**批判性思考评论：**

这是一篇典型的 Ken Shirriff 风格的技术考古文章——通过芯片拆解和显微镜摄影来理解历史处理器的设计。8087 的指令解码机制展现了早期微处理器设计的巧妙之处：通过总线监听和 ESCAPE 操作码机制，实现了主处理器和协处理器之间的无缝协作。

几个值得注意的设计决策：
1. **寄存器栈架构**：8087 使用栈而不是独立的寄存器文件，这简化了指令编码（只需指定栈顶操作），但增加了编程复杂性。

2. **分离的数据通路**：分数部分和指数部分有独立的处理电路，这允许并行处理，提高性能。

3. **总线监听机制**：8087 不依赖 8086 显式告知，而是通过监听总线自主获取指令，这种设计减少了处理器间的协调开销。

从现代视角看，这些设计选择可能显得过时，但在 1980 年代的工艺限制下，它们代表了工程上的最优解。这篇文章提醒我们：理解计算机历史有助于我们欣赏现代处理器设计的演进路径。
