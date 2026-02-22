Title: Intel 8087 浮点芯片中的指令解码 / Instruction decoding in the Intel 8087 floating-point chip
URL: http://www.righto.com/2026/02/8087-instruction-decoding.html

In the 1980s, if you wanted your IBM PC to run faster, you could buy the Intel 8087 floating-point coprocessor chip. With this chip, CAD software, spreadsheets, flight simulators, and other programs were much speedier. The 8087 chip could add, subtract, multiply, and divide, of course, but it could also compute transcendental functions such as tangent and logarithms, as well as provide constants such as π. In total, the 8087 added 62 new instructions to the computer.

在 1980 年代，如果你想让你的 IBM PC 运行得更快，你可以购买 Intel 8087 浮点协处理器芯片。有了这个芯片，CAD 软件、电子表格、飞行模拟器和其他程序都能快得多。8087 芯片当然可以进行加法、减法、乘法和除法，但它还能计算正切和对数等超越函数，以及提供 π 等常数。总之，8087 为计算机增加了 62 条新指令。

But how does a PC decide if an instruction was a floating-point instruction for the 8087 or a regular instruction for the 8086 or 8088 CPU? And how does the 8087 chip interpret instructions to determine what they mean? It turns out that decoding an instruction inside the 8087 is more complicated than you might expect. The 8087 uses multiple techniques, with decoding circuitry spread across the chip. In this blog post, I'll explain how these decoding circuits work.

但是 PC 如何决定一条指令是传给 8087 的浮点指令，还是传给 8086 或 8088 CPU 的普通指令呢？8087 芯片又是如何解读指令以确定其含义的？事实证明，在 8087 内部解码一条指令比你想像的更为复杂。8087 使用了多种技术，解码电路遍布整个芯片。在这篇博客文章中，我将解释这些解码电路的工作原理。

To reverse-engineer the 8087, I chiseled open the ceramic package of an 8087 chip and took numerous photos of the silicon die with a microscope. The complex patterns on the die are formed by its metal wiring, as well as the polysilicon and silicon underneath. The bottom half of the chip is the "datapath", the circuitry that performs calculations on 80-bit floating point values. At the left of the datapath, a constant ROM holds important constants such as π. At the right are the eight registers that the programmer uses to hold floating-point values; in an unusual design decision, these registers are arranged as a stack. Floating-point numbers cover a huge range by representing numbers with a fractional part and an exponent; the 8087 has separate circuitry to process the fractional part and the exponent.

为了对 8087 进行逆向工程，我凿开了一个 8087 芯片的陶瓷封装，并用显微镜拍摄了硅晶片的众多照片。晶片上的复杂图案由其金属布线以及下方的多晶硅和硅形成。芯片的下半部分是"数据通路"，即对 80 位浮点值进行计算的电路。在数据通路的左侧，一个常数 ROM 保存着 π 等重要常数。在右侧是程序员用来保存浮点值的八个寄存器；在一个不寻常的设计决策中，这些寄存器被安排成一个堆栈。浮点数通过用分数部分和指数表示数字来覆盖巨大的范围；8087 有独立的电路来处理分数部分和指数。

https://static.righto.com/images/8087-decode/8087-die-labeled.jpg
Die of the Intel 8087 floating point unit chip, with main functional blocks labeled. The die is 5 mm×6 mm. Click this image (or any others) for a larger image.

Intel 8087 浮点单元芯片的晶片，主要功能块已标注。晶片尺寸为 5 毫米×6 毫米。点击图片（或任何其他图片）查看更大版本。

The chip's instructions are defined by the large microcode ROM in the middle. To execute an instruction, the 8087 decodes the instruction and the microcode engine starts executing the appropriate micro-instructions from the microcode ROM. In the upper right part of the chip, the Bus Interface Unit (BIU) communicates with the main processor and memory over the computer's bus. For the most part, the BIU and the rest of the chip operate independently, but as we will see, the BIU plays important roles in instruction decoding and execution.

芯片的指令由中间的大型微码 ROM 定义。为了执行一条指令，8087 先解码指令，然后微码引擎开始从微码 ROM 执行适当的微指令。在芯片的右上部分，总线接口单元（BIU）通过计算机的总线与主处理器和内存通信。在很大程度上，BIU 和芯片的其余部分独立运行，但正如我们将看到的，BIU 在指令解码和执行中扮演着重要角色。

## Cooperation with the main 8086/8088 processor / 与主 8086/8088 处理器的协作

The 8087 chip acted as a coprocessor with the main 8086 (or 8088) processor. When a floating-point instruction was encountered, the 8086 would let the 8087 floating-point chip carry out the floating-point instruction. But how do the 8086 and the 8087 determine which chip executes a particular instruction? You might expect the 8086 to tell the 8087 when it should execute an instruction, but this cooperation turns out to be more complicated.

8087 芯片作为主 8086（或 8088）处理器的协处理器。当遇到浮点指令时，8086 会让 8087 浮点芯片执行该浮点指令。但是 8086 和 8087 如何决定由哪个芯片执行特定指令呢？你可能会期望 8086 告诉 8087 何时应该执行指令，但这种协作实际上更为复杂。

The 8086 has eight opcodes that are assigned to the coprocessor, called ESCAPE opcodes. The 8087 determines what instruction the 8086 is executing by watching the bus, a task performed by the BIU (Bus Interface Unit). If the instruction is an ESCAPE, the instruction is intended for the 8087. However, there's a problem. The 8087 doesn't have any access to the 8086's registers (and vice versa), so the only way that they can exchange data is through memory. But the 8086 addresses memory through a complicated scheme involving offset registers and segment registers. How can the 8087 determine what memory address to use when it doesn't have access to the registers?

8086 有八个操作码分配给协处理器，称为 ESCAPE 操作码。8087 通过监视总线来确定 8086 正在执行什么指令，这个任务由 BIU（总线接口单元）执行。如果指令是 ESCAPE，则该指令是发给 8087 的。然而，这里有一个问题。8087 无法访问 8086 的寄存器（反之亦然），因此它们交换数据的唯一方式是通过内存。但 8086 通过涉及偏移寄存器和段寄存器的复杂方案来寻址内存。当 8087 无法访问寄存器时，它如何确定要使用什么内存地址呢？

The trick is that when an ESCAPE instruction is encountered, the 8086 processor starts executing the instruction, even though it is intended for the 8087. The 8086 computes the memory address that the instruction references and reads that memory address, but ignores the result. Meanwhile, the 8087 watches the memory bus to see what address is accessed and stores this address internally in a BIU register. When the 8087 starts executing the instruction, it uses the address from the 8086 to read and write memory. In effect, the 8087 offloads address computation to the 8086 processor.

诀窍在于，当遇到 ESCAPE 指令时，8086 处理器开始执行该指令，即使它是发给 8087 的。8086 计算指令引用的内存地址并读取该内存地址，但忽略结果。与此同时，8087 监视内存总线以查看访问了什么地址，并将此地址内部存储在 BIU 寄存器中。当 8087 开始执行指令时，它使用来自 8086 的地址来读写内存。实际上，8087 将地址计算任务卸载给了 8086 处理器。

## The structure of 8087 instructions / 8087 指令的结构

To understand the 8087's instructions, we need to take a closer look at the structure of 8086 instructions. In particular, something called the ModR/M byte is important since all 8087 instructions use it.

要理解 8087 的指令，我们需要仔细研究 8086 指令的结构。特别是，某种称为 ModR/M 字节的东西很重要，因为所有 8087 指令都使用它。

The 8086 uses a complex system of opcodes with a mixture of single-byte opcodes, prefix bytes, and longer instructions. About a quarter of the opcodes use a second byte, called ModR/M, that specifies the registers and/or memory address to use through a complicated encoding. For instance, the memory address can be computed by adding the BX and SI registers, or from the BP register plus a two-byte offset. The first two bits of the ModR/M byte are the "MOD" bits. For a memory access, the MOD bits indicate how many address displacement bytes follow the ModR/M byte (0, 1, or 2), while the "R/M" bits specify how the address is computed. A MOD value of 3, however, indicates that the instruction operates on registers and does not access memory.

8086 使用一个复杂的操作码系统，混合了单字节操作码、前缀字节和更长的指令。大约四分之一的操作码使用第二个字节，称为 ModR/M，它通过复杂的编码指定要使用的寄存器和/或内存地址。例如，内存地址可以通过将 BX 和 SI 寄存器相加计算，或从 BP 寄存器加上两字节偏移量计算。ModR/M 字节的前两位是"MOD"位。对于内存访问，MOD 位表示 ModR/M 字节后跟随的地址位移字节数（0、1 或 2），而"R/M"位指定地址的计算方式。然而，MOD 值为 3 表示指令在寄存器上操作，不访问内存。

https://static.righto.com/images/8087-decode/modrm.jpg
Structure of an 8087 instruction

一条 8087 指令的结构

The diagram above shows how an 8087 instruction consists of an ESCAPE opcode, followed by a ModR/M byte. An ESCAPE opcode is indicated by the special bit pattern 11011, leaving three bits (green) available in the first byte to specify the type of 8087 instruction. As mentioned above, the ModR/M byte has two forms. The first form performs a memory access; it has MOD bits of 00, 01, or 10 and the R/M bits specify how the memory address is computed. This leaves three bits (green) to specify the address. The second form operates internally, without a memory access; it has MOD bits of 11. Since the R/M bits aren't used in the second form, six bits (green) are available in the R/M byte to specify the instruction.

上图显示了一条 8087 指令如何由 ESCAPE 操作码后跟 ModR/M 字节组成。ESCAPE 操作码由特殊的位模式 11011 指示，在第一个字节中留下三位（绿色）可用于指定 8087 指令的类型。如上所述，ModR/M 字节有两种形式。第一种形式执行内存访问；它的 MOD 位为 00、01 或 10，R/M 位指定内存地址的计算方式。这留下三位（绿色）来指定地址。第二种形式在内部操作，不进行内存访问；它的 MOD 位为 11。由于第二种形式不使用 R/M 位，R/M 字节中有六位（绿色）可用于指定指令。

The challenge for the designers of the 8087 was to fit all the instructions into the available bits in such a way that decoding is straightforward. The diagram below shows a few 8087 instructions, illustrating how they achieve this. The first three instructions operate internally, so they have MOD bits of 11; the green bits specify the particular instruction. Addition is more complicated because it can act on memory (first format) or registers (second format), depending on the MOD bits. The four bits highlighted in bright green (0000) are the same for all ADD instructions; the subtract, multiplication, and division instructions use the same structure but have different values for the dark green bits. For instance, 0001 indicates multiplication and 0100 indicates subtraction. The other green bits (MF, d, and P) select variants of the addition instruction, changing the data format, direction, and popping the stack at the end. The last three bits select the R/M addressing mode for a memory operation, or the stack register ST(i) for a register operation.

8087 的设计者面临的挑战是如何将所有指令装入可用位中，使得解码变得简单明了。下图显示了几条 8087 指令，展示了它们如何实现这一点。前三条指令在内部操作，因此它们的 MOD 位为 11；绿色位指定特定的指令。加法更为复杂，因为它可以根据 MOD 位作用于内存（第一种格式）或寄存器（第二种格式）。所有 ADD 指令的亮绿色突出显示的四位（0000）相同；减法、乘法和除法指令使用相同的结构，但深绿色位有不同的值。例如，0001 表示乘法，0100 表示减法。其他绿色位（MF、d 和 P）选择加法指令的变体，改变数据格式、方向和最后弹出堆栈。最后三位为内存操作选择 R/M 寻址模式，或为寄存器操作选择堆栈寄存器 ST(i)。

https://static.righto.com/images/8087-decode/opcodes.jpg
The bit patterns for some 8087 instructions. Based on the datasheet.

一些 8087 指令的位模式。基于数据表。

## Selecting a microcode routine / 选择微码例程

Most of the 8087's instructions are implemented in microcode, implementing each step of an instruction in low-level "micro-instructions". The 8087 chip contains a microcode engine; you can think of it as the mini-CPU that controls the 8087 by executing a microcode routine, one micro-instruction at a time. The microcode engine provides an 11-bit micro-address to the ROM, specifying the micro-instruction to execute. Normally, the microcode engine steps through the microcode sequentially, but it also supports conditional jumps and subroutine calls.

8087 的大多数指令都是用微码实现的，用低级别的"微指令"实现指令的每一步。8087 芯片包含一个微码引擎；你可以把它看作是一个迷你 CPU，通过一次执行一条微指令来控制 8087 执行微码例程。微码引擎向 ROM 提供一个 11 位微地址，指定要执行的微指令。通常，微码引擎按顺序遍历微码，但它也支持条件跳转和子程序调用。

But how does the microcode engine know where to start executing the microcode for a particular machine instruction? Conceptually, you could feed the instruction opcode into a ROM that would provide the starting micro-address. However, this would be impractical since you'd need a 2048-word ROM to decode an 11-bit opcode. (While a 2K ROM is small nowadays, it was large at the time; the 8087's microcode ROM was a tight fit at just 1648 words.) Instead, the 8087 uses a more efficient (but complicated) instruction decode system constructed from a combination of logic gates and PLAs (Programmable Logic Arrays). This system holds 22 microcode entry points, much more practical than 2048.

但是微码引擎如何知道从哪里开始执行特定机器指令的微码呢？从概念上讲，你可以将指令操作码输入一个 ROM，它会提供起始微地址。然而，这将是不切实际的，因为需要一个 2048 字的 ROM 来解码一个 11 位操作码。（虽然 2K ROM 现在很小，但在当时很大；8087 的微码 ROM 只有 1648 字，已经是一个紧张的适配。）相反，8087 使用一个更有效（但更复杂）的指令解码系统，由逻辑门和 PLA（可编程逻辑阵列）组合构建而成。这个系统保存 22 个微码入口点，比 2048 实用得多。

Processors often use a circuit called a PLA (Programmable Logic Array) as part of instruction decoding. The idea of a PLA is to provide a dense and flexible way of implementing arbitrary logic functions. Any Boolean logic function can be expressed as a "sum-of-products", a collection of AND terms (products) that are OR'd together (summed). A PLA has a block of circuitry called the AND plane that generates the desired sum terms. The outputs of the AND plane are fed into a second block, the OR plane, which ORs the terms together. Physically, a PLA is implemented as a grid, where each spot in the grid can either have a transistor or not. By changing the transistor pattern, the PLA implements the desired function.

处理器经常使用一种称为 PLA（可编程逻辑阵列）的电路作为指令解码的一部分。PLA 的想法是提供一种密集而灵活的方式来实现任意逻辑功能。任何布尔逻辑功能都可以表示为"积之和"，即一组 AND 项（积）通过 OR 运算组合在一起（求和）。PLA 有一个称为 AND 平面的电路块，生成所需的求和项。AND 平面的输出被送入第二个块，即 OR 平面，它将各项通过 OR 运算组合在一起。物理上，PLA 被实现为一个网格，其中网格中的每个位置可以有晶体管，也可以没有。通过改变晶体管模式，PLA 实现了所需的功能。

https://static.righto.com/images/8087-decode/pla-structure.jpg
A simplified diagram of a PLA.

PLA 的简化示意图。

A PLA can implement arbitrary logic, but in the 8087, PLAs often act as optimized ROMs. The AND plane matches bit patterns, selecting an entry from the OR plane, which holds the output values, the micro-address for each routine. The advantage of the PLA over a standard ROM is that one output column can be used for many different inputs, reducing the size.

PLA 可以实现任意逻辑，但在 8087 中，PLA 通常充当优化的 ROM。AND 平面匹配位模式，从 OR 平面中选择条目，OR 平面保存输出值，即每个例程的微地址。PLA 相对于标准 ROM 的优势在于，一列输出可以用于许多不同的输入，从而减小尺寸。

The image below shows part of the instruction decoding PLA. The horizontal input lines are polysilicon wires on top of the silicon. The pinkish regions are doped silicon. When polysilicon crosses doped silicon, it creates a transistor (green). Where there is a gap in the doped silicon, there is no transistor (red). (The output wires run vertically, but are not visible here; I dissolved the metal layer to show the silicon underneath.) If a polysilicon line is energized, it turns on all the transistors in its row, pulling the associated output columns to ground. (If no transistors are turned on, the pull-up transistor pulls the output high.) Thus, the pattern of doped silicon regions creates a grid of transistors in the PLA that implements the desired logic function.

下图显示了指令解码 PLA 的一部分。水平输入线是硅片顶部的多晶硅线。粉红色区域是掺杂硅。当多晶硅穿过掺杂硅时，它会创建一个晶体管（绿色）。当掺杂硅有间隙时，就没有晶体管（红色）。（输出线垂直运行，但在这里不可见；我溶解了金属层以显示下方的硅。）如果多晶硅线通电，它会打开其行中的所有晶体管，将相关的输出列拉低。（如果没有晶体管被打开，上拉晶体管会将输出拉高。）因此，掺杂硅区域的图案在 PLA 中创建了一个晶体管网格，实现了所需的逻辑功能。

https://static.righto.com/images/8087-decode/pla-diagram.jpg
Part of the PLA for instruction decoding.

指令解码 PLA 的一部分。

The standard way to decode instructions with a PLA is to take the instruction bits (and their complements) as inputs. The PLA can then pattern-match against bit patterns in the instruction. However, the 8087 also uses some pre-processing to reduce the size of the PLA. For instance, the MOD bits are processed to generate a signal if the bits are 0, 1, or 2 (i.e. a memory operation) and a second signal if the bits are 3 (i.e. a register operation). This allows the 0, 1, and 2 cases to be handled by a single PLA pattern. Another signal indicates that the top bits are 001 111xxxxx; this indicates that the R/M field takes part in instruction selection. Sometimes a PLA output is fed back in as an input, so a decoded group of instructions can be excluded from another group. These techniques all reduce the size of the PLA at the cost of some additional logic gates.

用 PLA 解码指令的标准方式是将指令位（及其补码）作为输入。然后 PLA 可以根据指令中的位模式进行模式匹配。然而，8087 还使用了一些预处理来减小 PLA 的尺寸。例如，MOD 位被处理以生成一个信号，如果位是 0、1 或 2（即内存操作），以及第二个信号，如果位是 3（即寄存器操作）。这允许 0、1 和 2 的情况由单个 PLA 模式处理。另一个信号表示高位是 001 111xxxxx；这表明 R/M 字段参与指令选择。有时 PLA 输出被反馈作为输入，因此一组解码的指令可以从另一组中排除。这些技术都以一些额外的逻辑门为代价减小了 PLA 的尺寸。

The result of the instruction decoding PLA's AND plane is 22 signals, where each signal corresponds to an instruction or group of instructions with a shared microcode entry point. The lower part of the instruction decoding PLA acts as a ROM that holds the 22 microcode entry points and provides the selected one.

指令解码 PLA 的 AND 平面的结果是 22 个信号，每个信号对应一个指令或共享微码入口点的指令组。指令解码 PLA 的下部充当一个 ROM，保存 22 个微码入口点并提供所选的入口点。

## Instruction decoding inside the microcode / 微码内部的指令解码

Many 8087 instructions share the same microcode routines. For instance, the addition, subtraction, multiplication, division, reverse subtraction, and reverse division instructions all go to the same microcode routine. This reduces the size of the microcode since these instructions share the microcode that sets up the instruction and handles the result. However, the microcode obviously needs to diverge at some point to perform the specific operation. Moreover, some arithmetic opcodes access the top of the stack, some access an arbitrary location in the stack, some access memory, and some reverse the operands, requiring different microcode actions. How does the microcode do different things for different opcodes while sharing code?

许多 8087 指令共享相同的微码例程。例如，加法、减法、乘法、除法、反向减法和反向除法指令都进入相同的微码例程。这减小了微码的尺寸，因为这些指令共享设置指令和处理结果的微码。然而，微码显然需要在某个时刻分叉以执行特定的操作。此外，一些算术操作码访问堆栈顶部，一些访问堆栈中的任意位置，一些访问内存，一些反转操作数，需要不同的微码操作。微码如何为不同的操作码做不同的事情，同时共享代码呢？

The trick is that the 8087's microcode engine supports conditional subroutine calls, returns, and jumps, based on 49 different conditions. In particular, fifteen conditions examine the instruction. Some conditions test specific bit patterns, such as branching if the lowest bit is set, or more complex patterns such as an opcode matching 0xx 11xxxxxx. Other conditions detect specific instructions such as FMUL. The result is that the microcode can take different paths for different instructions. For instance, a reverse subtraction or reverse division is implemented in the microcode by testing the instruction and reversing the arguments if necessary, while sharing the rest of the code.

诀窍在于 8087 的微码引擎支持基于 49 种不同条件的条件子程序调用、返回和跳转。特别是，十五个条件检查指令。一些条件测试特定的位模式，例如如果最低位被设置则分支，或更复杂的模式如操作码匹配 0xx 11xxxxxx。其他条件检测特定指令，如 FMUL。结果是微码可以为不同指令采用不同的路径。例如，反向减法或反向除法是通过微码测试指令并在必要时反转参数来实现的，同时共享其余代码。

The microcode also has a special jump target that performs a three-way jump depending on the current machine instruction that is being executed. The microcode engine has a jump ROM that holds 22 entry points for jumps or subroutine calls. However, a jump to target 0 uses special circuitry so it will instead jump to target 1 for a multiplication instruction, target 2 for an addition/subtraction, or target 3 for division. This special jump is implemented by gates in the upper right corner of the jump decoder.

微码还有一个特殊的跳转目标，根据当前正在执行的机器指令执行三分支跳转。微码引擎有一个跳转 ROM，保存 22 个跳转或子程序调用的入口点。然而，跳转到目标 0 使用特殊电路，因此它将改为跳转到目标 1（如果是乘法指令）、目标 2（如果是加法/减法）或目标 3（如果是除法）。这个特殊的跳转由跳转解码器右上角的门实现。

https://static.righto.com/images/8087-decode/jump-rom.jpg
The jump decoder and ROM. Note that the rows are not in numerical order; presumably, this made the layout slightly more compact. Click this image (or any other) for a larger version.

跳转解码器和 ROM。注意行不是按数字顺序排列的；显然，这使得布局稍微更紧凑。点击图片（或任何其他图片）查看更大版本。

## Hardwired instruction handling / 硬连线指令处理

Some of the 8087's instructions are implemented directly by hardware in the Bus Interface Unit (BIU), rather than using microcode. For example, instructions to enable or disable interrupts, or to save or restore state are implemented in hardware. The decoding for these instructions is performed by separate circuitry from the instruction decoder described above.

8087 的一些指令由总线接口单元（BIU）中的硬件直接实现，而不是使用微码。例如，启用或禁用中断的指令，或保存或恢复状态的指令，都是用硬件实现的。这些指令的解码由与上述指令解码器分开的电路执行。

In the first step, a small PLA decodes the top 5 bits of the instruction. Most importantly, if these bits are 11011, it indicates an ESCAPE instruction, the start of an 8087 operation. This causes the 8087 to start interpreting the instruction and stores the opcode in a BIU register for use by the instruction decoder. A second small PLA takes the outputs from the top-5 PLA and combines them with the lower three bits. It decodes specific instruction values: D9, DB, DD, E0, E1, E2, or E3. The first three values correspond to specific ESCAPE instructions, and are recorded in latches.

在第一步，一个小型 PLA 解码指令的前 5 位。最重要的是，如果这些位是 11011，则表示 ESCAPE 指令，即 8087 操作的开始。这会导致 8087 开始解释指令并将操作码存储在 BIU 寄存器中供指令解码器使用。第二个小型 PLA 从 top-5 PLA 获取输出并将其与低三位组合。它解码特定的指令值：D9、DB、DD、E0、E1、E2 或 E3。前三个值对应特定的 ESCAPE 指令，并被记录在锁存器中。

The two PLAs decode the second byte in the same way. Logic gates combine the PLA outputs from the second byte with the latched values from the first byte, detecting eleven hardwired instructions. Some of these instructions operate directly on registers, such as clearing exceptions; the decoded instruction signal goes to the relevant register and modifies it in an ad hoc way. Other hardwired instructions are more complicated, writing chip state to memory or reading chip state from memory. These instructions require multiple memory operations, controlled by the Bus Interface Unit's state machine. Each of these instructions has a flip-flop that is triggered by the decoded instruction to keep track of which instruction is active.

两个 PLA 以相同的方式解码第二个字节。逻辑门将来自第二个字节的 PLA 输出与来自第一个字节的锁存值组合，检测十一个硬连线指令。其中一些指令直接在寄存器上操作，例如清除异常；解码的指令信号进入相关寄存器并以临时方式修改它。其他硬连线指令更为复杂，将芯片状态写入内存或从内存读取芯片状态。这些指令需要多次内存操作，由总线接口单元的状态机控制。这些指令中的每一个都有一个触发器，由解码的指令触发以跟踪哪个指令处于活动状态。

For the instructions that save and restore the 8087's state (FSAVE and FRSTOR), there's one more complication. These instructions are partially implemented in the BIU, which moves the relevant BIU registers to or from memory. But then, instruction processing switches to microcode, where a microcode routine saves or loads the floating-point registers. Jumping to the microcode routine is not implemented through the regular microcode jump circuitry. Instead, two hardcoded values force the microcode address to the save or restore routine.

对于保存和恢复 8087 状态的指令（FSAVE 和 FRSTOR），还有一个额外的复杂性。这些指令部分在 BIU 中实现，BIU 将相关的 BIU 寄存器移入或移出内存。但随后，指令处理切换到微码，在微码例程保存或加载浮点寄存器。跳转到微码例程不是通过常规微码跳转电路实现的。相反，两个硬编码值强制将微码地址设置为保存或恢复例程。

## Constants / 常数

The 8087 has seven instructions to load floating-point constants such as π, 1, or log10(2). The 8087 has a constant ROM that holds these constants, as well as constants for transcendental operations. You might expect that the 8087 simply loads the specified constant from the constant ROM, using the instruction to select the desired constant. However, the process is much more complicated.

8087 有七条指令用于加载浮点常数，如 π、1 或 log10(2)。8087 有一个常数 ROM，保存这些常数，以及用于超越运算的常数。你可能会期望 8087 简单地从常数 ROM 加载指定的常数，使用指令来选择所需的常数。然而，这个过程要复杂得多。

Looking at the instruction decode ROM shows that different constants are implemented with different microcode routines: the constant-loading instructions FLDLG2 and FLDLN2 have one entry point; FLD1, FLD2E, FLDL2T, and FLDPI have a second entry point, and FLDZ (zero) has a third entry point. It's understandable that zero is a special case, but why are there two routines for the other constants?

查看指令解码 ROM 显示，不同的常数用不同的微码例程实现：常数加载指令 FLDLG2 和 FLDLN2 有一个入口点；FLD1、FLD2E、FLDL2T 和 FLDPI 有第二个入口点，FLDZ（零）有第三个入口点。可以理解零是一个特殊情况，但为什么其他常数有两个例程呢？

The explanation is that the fraction part of each constant is stored in the constant ROM, but the exponent is stored in a separate, smaller ROM. To reduce the size of the exponent ROM, only some of the necessary exponents are stored. If a constant needs an exponent one larger than a value in the ROM, the microcode adds one to the exponent ROM value, computing the exponent on the fly.

解释是每个常数的分数部分存储在常数 ROM 中，但指数存储在一个单独的、较小的 ROM 中。为了减小指数 ROM 的尺寸，只存储了一些必要的指数。如果常数需要的指数比 ROM 中的值大 1，微码会将指数 ROM 值加 1，即时计算指数。

Thus, the load-constant instructions use three separate instruction decoding mechanisms. First, the instruction decode ROM determines the appropriate microcode routine for the constant instruction, as before. Then, the constant PLA decodes the instruction to select the appropriate constant. Finally, the microcode routine tests the bottom bit of the instruction and increments the exponent if necessary.

因此，加载常数指令使用三个独立的指令解码机制。首先，指令解码 ROM 确定常数指令的适当微码例程，如前所述。然后，常数 PLA 解码指令以选择适当的常数。最后，微码例程测试指令的最低位，并在必要时递增指数。

## Conclusions / 结论

To wrap up the discussion of the decoding circuitry, the diagram below shows how the different circuits are arranged on the die. This image shows the upper-right part of the die; the microcode engine is at the left and part of the ROM is at the bottom.

为了总结解码电路的讨论，下图显示了不同电路在晶片上的排列方式。此图像显示晶片的右上部分；微码引擎在左侧，ROM 的一部分在底部。

https://static.righto.com/images/8087-decode/decoding-labeled.jpg
The upper-left portion of the 8087 die, with functional blocks labeled.

8087 晶片的左上部分，功能块已标注。

The 8087 doesn't have a clean architecture, but instead is full of ad hoc circuits and corner cases. The 8087's instruction decoding is an example of this. Decoding is complicated to start with due to the 8086's convoluted instruction formats and the ModR/M byte. On top of that, the 8087's instruction decoding has multiple layers: the instruction decode PLA, microcode conditional jumps that depend on the instruction, a special jump target that depends on the instruction, constants selected based on the instruction, and instructions decoded by the BIU.

8087 没有简洁的架构，而是充满了临时电路和特殊情况。8087 的指令解码就是一个例子。由于 8086 复杂的指令格式和 ModR/M 字节，解码一开始就复杂。除此之外，8087 的指令解码还有多个层次：指令解码 PLA、依赖于指令的微码条件跳转、依赖于指令的特殊跳转目标、基于指令选择的常数，以及由 BIU 解码的指令。

The 8087 has a reason for this complicated architecture: at the time, the chip was on the edge of what was possible, so the designers needed to use whatever techniques they could to reduce the size of the chip. If implementing a corner case could shave a few transistors off the chip or make the microcode ROM slightly smaller, the corner case was worthwhile. Even so, the 8087 was barely manufacturable at first; early yield was just two working chips per silicon wafer. Despite this difficult start, a floating-point standard based on the 8087 is now part of almost every processor.

8087 有这种复杂架构是有原因的：在当时，芯片处于技术可能的边缘，因此设计者需要使用任何技术来减小芯片尺寸。如果实现一个特殊情况可以从芯片上减少几个晶体管或使微码 ROM 稍微小一点，这个特殊情况就是值得的。即便如此，8087 最初几乎无法制造；早期产量每片硅晶片只有两个工作芯片。尽管起步艰难，但基于 8087 的浮点标准现在几乎已成为每个处理器的一部分。

Thanks to the members of the "Opcode Collective" for their contributions, especially Smartest Blob and Gloriouscow.

感谢"Opcode Collective"的成员，特别是 Smartest Blob 和 Gloriouscow。

For updates, follow me on Bluesky (@righto.com), Mastodon (@kenshirriff@oldbytes.space), or RSS.

如需更新，请在 Bluesky (@righto.com)、Mastodon (@kenshirriff@oldbytes.space) 或 RSS 上关注我。

## Notes and references / 注释和参考文献

1. The contents of the microcode ROM are available here, partially decoded thanks to Smartest Blob.

   微码 ROM 的内容可在此处获取，部分解码归功于 Smartest Blob。

2. It is difficult for the 8087 to determine what the 8086 is doing because the 8086 prefetches instructions. Thus, when an instruction is seen on the bus, the 8086 may execute it at some point in the future, or it may end up discarded. In order to tell what instruction is being executed, the 8087 floating-point chip internally duplicates the 8086 processor's queue. The 8087 watches the memory bus and copies any instructions that are prefetched. Since the 8087 can't tell from the bus when the 8086 starts a new instruction or when the 8086 empties the queue when jumping to a new address, the 8086 processor provides two queue status signals to the 8087. With the help of these signals, the 8087 knows exactly what the 8086 is executing. The 8087's instruction queue has six 8-bit registers, the same as the 8086. Surprisingly, the last two queue registers in the 8087 are tied together, so there are only five usable queue registers. My hypothesis is that since the 8087 copies the active instruction into separate registers (unlike the 8086), only five queue registers are needed. This raises the question of why the excess register wasn't removed from the die, rather than wasting valuable space. The 8088 processor, used in the IBM PC, has a four-byte queue instead of a six-byte queue. The 8088 is almost identical to the 8086 except it has an 8-bit memory bus instead of a 16-bit memory bus. With the narrower memory bus, prefetching is more likely to get in the way of other memory accesses, so a smaller prefetch queue was implemented. Knowing the queue size is essential to the 8087 floating-point chip. To indicate this, when the processor boots, a signal lets the 8087 determine if the attached processor is an 8086 or an 8088.

   8087 很难确定 8086 在做什么，因为 8086 会预取指令。因此，当在总线上看到指令时，8086 可能会在未来的某个点执行它，或者它可能会被丢弃。为了告诉正在执行什么指令，8087 浮点芯片在内部复制了 8086 处理器的队列。8087 监视内存总线并复制预取的任何指令。由于 8087 无法从总线判断 8086 何时开始新指令或何时清空队列跳转到新地址，8086 处理器向 8087 提供两个队列状态信号。在这些信号的帮助下，8087 确切知道 8086 正在执行什么。8087 的指令队列有六个 8 位寄存器，与 8086 相同。令人惊讶的是，8087 中的最后两个队列寄存器连接在一起，因此只有五个可用的队列寄存器。我的假设是，由于 8087 将活动指令复制到单独的寄存器中（与 8086 不同），只需要五个队列寄存器。这就提出了一个问题，为什么多余的寄存器没有从晶片上移除，而是浪费宝贵的空间。用于 IBM PC 的 8088 处理器有一个四字节的队列，而不是六字节的队列。8088 与 8086 几乎相同，只是它有 8 位内存总线而不是 16 位内存总线。由于内存总线较窄，预取更有可能妨碍其他内存访问，因此实现了较小的预取队列。知道队列大小对 8087 浮点芯片至关重要。为了指示这一点，当处理器启动时，一个信号让 8087 确定连接的处理器是 8086 还是 8088。

3. The relevant part of the opcode is 11 bits: the top 5 bits are always 11011 for an ESCAPE opcode, so they can be ignored during decoding. The Bus Interface Unit has a 3-bit register to hold the first byte of the instruction and an 8-bit register to hold the second byte. The BIU registers have an irregular appearance because there are 3-bit registers, 8-bit registers, and 10-bit registers (holding half of a 20-bit address).

   操作码的相关部分是 11 位：前 5 位对于 ESCAPE 操作码总是 11011，因此可以在解码期间忽略它们。总线接口单元有一个 3 位寄存器保存指令的第一个字节，一个 8 位寄存器保存第二个字节。BIU 寄存器有不规则的外观，因为有 3 位寄存器、8 位寄存器和 10 位寄存器（保存 20 位地址的一半）。

4. What's the difference between a PLA and a ROM? There is a lot of overlap: a ROM can replace a PLA, while a PLA can implement a ROM. A ROM is essentially a PLA where the first stage is a binary decoder, so the ROM has a separate row for each input value. However, the first stage of a ROM can be optimized so multiple inputs share the same output value; is this a ROM or a PLA? The "official" difference is that in a ROM, one row is activated at a time, while in a PLA, multiple rows can be activated at once, so the output values are combined. (Thus, it is straightforward to read the values out of a ROM, but more difficult to read the values out of a PLA.) I consider the instruction decoding PLA to be best described as a PLA first stage with the second stage acting as a ROM. You could also call it a partially-decoded ROM, or just a PLA. Hopefully my terminology isn't too confusing.

   PLA 和 ROM 有什么区别？有很多重叠：ROM 可以替代 PLA，而 PLA 可以实现 ROM。ROM 本质上是一个 PLA，其中第一阶段是二进制解码器，因此 ROM 对每个输入值都有单独的行。然而，ROM 的第一阶段可以优化，使多个输入共享相同的输出值；这是 ROM 还是 PLA？"官方"的区别在于，在 ROM 中，一次激活一行，而在 PLA 中，可以同时激活多行，因此输出值被组合。（因此，从 ROM 中读取值很简单，但从 PLA 中读取值则更困难。）我认为指令解码 PLA 最好被描述为具有充当 ROM 的第二阶段的 PLA 第一阶段。你也可以称它为部分解码的 ROM，或者只是 PLA。希望我的术语不会太令人困惑。

5. To match a bit pattern in an instruction, the bits of the instruction are fed into the PLA, along with the complements of these bits; this allows the PLA to match against a 0 bit or a 1 bit. Each row of a PLA will match a particular bit pattern in the instruction: bits that must be 1, bits that must be 0, and bits that don't matter. If the instruction opcodes are assigned rationally, a small number of bit patterns will match all the opcodes, reducing the size of the decoder. I may be going too far with this analogy, but a PLA is a lot like a neural net. Each column in the AND plane is like a neuron that fires when it recognizes a particular input pattern. The OR plane is like a second layer in a neural net, combining signals from the first layer. The PLA's "weights", however, are fixed at 0 or 1, so it's not as flexible as a "real" neural net.

   为了匹配指令中的位模式，指令的位被输入 PLA，以及这些位的补码；这允许 PLA 匹配 0 位或 1 位。PLA 的每一行将匹配指令中的特定位模式：必须为 1 的位、必须为 0 的位和不重要的位。如果指令操作码被合理分配，少量的位模式将匹配所有操作码，从而减小解码器的尺寸。我可能在这个类比上走得太远，但 PLA 很像神经网络。AND 平面中的每一列就像一个神经元，在识别特定输入模式时触发。OR 平面就像神经网络中的第二层，组合来自第一层的信号。PLA 的"权重"然而固定在 0 或 1，因此它不像"真正的"神经网络那样灵活。

6. The instruction decoding PLA has an unusual layout, where the second plane is rotated 90°. In a regular PLA (left), the inputs (red) go into the first plane, the perpendicular outputs from the first plane (purple) go into the second plane, and the PLA outputs (blue) exit parallel to the inputs. In the address PLA, however, the second plane is rotated 90°, so the outputs are perpendicular to the inputs. This approach requires additional wiring (horizontal purple lines), but presumably, this layout worked better in the 8087 since the outputs are lined up with the rest of the microcode engine.

   指令解码 PLA 有一个不寻常的布局，其中第二个平面旋转了 90°。在常规 PLA（左）中，输入（红色）进入第一阶段，第一阶段的垂直输出（紫色）进入第二阶段，PLA 输出（蓝色）与输入平行退出。然而，在地址 PLA 中，第二阶段旋转了 90°，因此输出与输入垂直。这种方法需要额外的布线（水平紫色线），但推测这种布局在 8087 中工作得更好，因为输出与其余微码引擎对齐。

7. To describe the implementation of a PLA in more detail, the transistors in each row of the AND plane form a NOR gate, since if any transistor is turned on, it pulls the output low. Likewise, the transistors in each column of the OR plane form a NOR gate. So why is the PLA described as having an AND plane and an OR plane, rather than two NOR planes? By using De Morgan's law, you can treat the NOR-NOR Boolean equations as equivalent to AND-OR Boolean equations (with the inputs and outputs inverted). It's usually much easier to understand the logic as AND terms OR'd together. The converse question is why don't they build the PLA from AND and OR gates instead of NOR gates? The reason is that AND and OR gates are harder to build with NMOS transistors, since you need to add explicit inverter circuits. Moreover, NMOS NOR gates are typically faster than NAND gates because the transistors are in parallel. (CMOS is the opposite; NAND gates are faster because the weaker PMOS transistors are in parallel.)

   为了更详细地描述 PLA 的实现，AND 平面中每行的晶体管形成一个 NOR 门，因为如果任何晶体管被打开，它会将输出拉低。同样，OR 平面中每列的晶体管形成一个 NOR 门。那么为什么 PLA 被描述为具有 AND 平面和 OR 平面，而不是两个 NOR 平面呢？通过使用德摩根定律，你可以将 NOR-NOR 布尔方程视为等效于 AND-OR 布尔方程（输入和输出反转）。通常更容易理解逻辑为 AND 项通过 OR 运算组合在一起。相反的问题是为什么他们不从 AND 和 OR 门构建 PLA，而是从 NOR 门构建？原因是使用 NMOS 晶体管构建 AND 和 OR 门更难，因为需要添加显式反相器电路。此外，NMOS NOR 门通常比 NAND 门更快，因为晶体管是并联的。（CMOS 则相反；NAND 门更快，因为较弱的 PMOS 晶体管是并联的。）

8. The 8087's opcodes can be organized into tables, showing the underlying structure. (In each table, the row (Y) coordinate is the bottom 3 bits of the first byte and the column (X) coordinate is the 3 bits after the MOD bits in the second byte.) Memory operations use the following encoding with MOD = 0, 1, or 2. Each box represents 8 different addressing modes.

   8087 的操作码可以组织成表格，显示底层结构。（在每个表中，行（Y）坐标是第一个字节的低 3 位，列（X）坐标是第二个字节中 MOD 位后的 3 位。）内存操作使用以下编码，MOD = 0、1 或 2。每个框代表 8 种不同的寻址模式。

   [Memory operations table / 内存操作表]

   The important point is that the instruction encoding has a lot of regularity, making the decoding process easier. For instance, the basic arithmetic operations (FADD through FDIVR) are repeated on alternating rows. However, the table also has significant irregularities, which complicate the decoding process. The register operations (MOD = 3) have a related layout, but there are even more irregularities.

   重要的点是指令编码有很多规律性，使解码过程更容易。例如，基本算术运算（FADD 到 FDIVR）在交替行中重复。然而，表格也有显著的不规则性，这 complicates 了解码过程。寄存器操作（MOD = 3）有相关的布局，但有更多的不规则性。

   [Register operations table / 寄存器操作表]

   In most cases, each box indicates 8 different values for the stack register, but there are exceptions. The NOP and FCOMPP instructions each have a single opcode, "wasting" the rest of the box. Five of the boxes in the table encode multiple instructions instead of the register number. The first four (red) are miscellaneous instructions handled by the decoding PLA:

   在大多数情况下，每个框表示堆栈寄存器的 8 个不同值，但有例外。NOP 和 FCOMPP 指令每个都有单个操作码，"浪费"了框的其余部分。表格中的五个框编码多个指令而不是寄存器号。前四个（红色）是由解码 PLA 处理的杂项指令：

   misc1 = FCHS, FABS, FTST, FXAM
   misc2 = FLD1, FLDL2T, FLDL2E, FLDPI, FLDLG2, FLDLN2, FLDZ (the constant-loading instructions / 常数加载指令)
   misc3 = F2XM1, FYL2X, FPTAN, FPATAN, FXTRACT, FDECSTP, FINCSTP
   misc4 = FPREM, FYL2XP1, FSQRT, FRNDINT, FSCALE

   The last miscellaneous box (yellow) holds instructions that are handled by the BIU.

   最后一个杂项框（黄色）保存由 BIU 处理的指令。

   misc5 = FENI, FDISI, FCLEX, FINIT

   Curiously, the 8087's opcodes (like the 8086's) make much more sense in octal than in hexadecimal. In octal, an 8087 opcode is simply 33Y MXR, where X and Y are the table coordinates above, M is the MOD value (0, 1, 2, or 3), and R is the R/M field or the stack register number.

   奇怪的是，8087 的操作码（像 8086 的）在八进制中比十六进制更有意义。在八进制中，8087 操作码只是 33Y MXR，其中 X 和 Y 是上面的表坐标，M 是 MOD 值（0、1、2 或 3），R 是 R/M 字段或堆栈寄存器号。

9. The 22 outputs from the instruction decoder PLA correspond to the following groups of instructions, activating one row of ROM and producing the corresponding microcode address. From this table, you can see which instructions are grouped together in the microcode.

   指令解码器 PLA 的 22 个输出对应于以下指令组，激活 ROM 的一行并产生相应的微码地址。从这个表中，你可以看到哪些指令在微码中组合在一起。

   [Entry points table / 入口点表]

10. The instruction decoding PLA has 22 entries, and the jump table also has 22 entries. It's a coincidence that these values are the same. An entry in the jump table ROM is selected by five bits of the micro-instruction. The ROM is structured with two 11-bit words per row, interleaved. (It's also a coincidence that there are 22 bits.) The upper four bits of the jump number select a row in the ROM, while the bottom bit selects one of the two rows. This implementation is modified for target 0, the three-way jump. The first ROM row is selected for target 0 if the current instruction is multiplication, or for target 1. The second row is selected for target 0 if the current instruction is addition or subtraction, or for target 2. The third row is selected for target 0 if the current instruction is division, or for target 3. Thus, target 0 ends up selecting rows 1, 2, or 3. However, remember that there are two words per row, selected by the low bit of the target number. The problem is that target 0 with multiplication will access the left word of row 1, while target 1 will access the right word of row 1, but both should provide the same address. The solution is that rows 1, 2, and 3 have the same address stored twice in the row, so these rows each "waste" a value.

    指令解码 PLA 有 22 个条目，跳转表也有 22 个条目。这些值相同是巧合。跳转表 ROM 中的一个条目由微指令的 5 位选择。ROM 的结构是每行两个 11 位字，交错排列。（有 22 位也是巧合。）跳转号的高 4 位选择 ROM 中的一行，而最低位选择两行之一。此实现针对目标 0（三分支跳转）进行了修改。如果当前指令是乘法，则选择第一行 ROM 作为目标 0，或作为目标 1。如果当前指令是加法或减法，则选择第二行作为目标 0，或作为目标 2。如果当前指令是除法，则选择第三行作为目标 0，或作为目标 3。因此，目标 0 最终选择第 1、2 或 3 行。然而，请记住，每行有两个字，由目标号的低位选择。问题在于目标 0 与乘法将访问第 1 行的左字，而目标 1 将访问第 1 行的右字，但两者都应提供相同的地址。解决方案是第 1、2 和 3 行在每行中存储相同的地址两次，因此这些行每个都"浪费"一个值。

11. Eleven instructions are implemented in the BIU hardware. Four of these are relatively simple, setting or clearing bits: FINIT (initialize), FENI (enable interrupts), FDISI (disable interrupts), and FCLEX (clear exceptions). Six of these are more complicated, storing state to memory or loading state from memory: FLDCW (load control word), FSTCW (store control word), FSTSW (store status word), FSTENV (store environment), FLDENV (load environment), FSAVE (save state), and FRSTOR (restore state). As explained elsewhere, the last two instructions are partially implemented in microcode.

    十一个指令在 BIU 硬件中实现。其中四个相对简单，设置或清除位：FINIT（初始化）、FENI（启用中断）、FDISI（禁用中断）和 FCLEX（清除异常）。其中六个更为复杂，将状态存储到内存或从内存加载状态：FLDCW（加载控制字）、FSTCW（存储控制字）、FSTSW（存储状态字）、FSTENV（存储环境）、FLDENV（加载环境）、FSAVE（保存状态）和 FRSTOR（恢复状态）。如其他地方所解释的，最后两个指令部分在微码中实现。

12. Even a seemingly trivial instruction uses more circuitry than you might expect. For instance, after the FCLEX (clear exception) instruction is decoded, the signal goes through nine gates before it clears the exception bits in the status register. Along the way, it goes through a flip-flop to synchronize the timing, a gate to combine it with the reset signal, and various inverters and drivers. Even though these instructions seem like they should complete immediately, they typically take 5 clock cycles due to overhead in the 8087.

    即使看似微不足道的指令也使用比你预期更多的电路。例如，FCLEX（清除异常）指令解码后，信号在清除状态寄存器中的异常位之前通过九个门。在此过程中，它经过一个触发器以同步时序，一个门将其与复位信号组合，以及各种反相器和驱动器。尽管这些指令看起来应该立即完成，但它们通常由于 8087 的开销而需要 5 个时钟周期。

13. I'll give more details here on the circuit that jumps to the save or restore microcode. The BIU sends two signals to the microcode engine, one to jump to the save code and one to jump to the restore code. These signals are buffered and delayed by a capacitor, probably to adjust the timing of the signal. In the microcode engine, there are two hardcoded constants for the routines, just above the jump table; the BIU signal causes the appropriate constant to go onto the micro-address lines. Each bit in the address has a pull-up transistor to +5V or a pull-down transistor to ground. This approach is somewhat inefficient since it requires two transistor sites per bit. In comparison, the jump address ROM and the instruction address ROM use one transistor site per bit.

    我将在这里提供更多关于跳转到保存或恢复微码的电路的详细信息。BIU 向微码引擎发送两个信号，一个跳转到保存代码，一个跳转到恢复代码。这些信号由电容器缓冲和延迟，可能是为了调整信号的时序。在微码引擎中，有两个硬编码常量用于例程，就在跳转表上方；BIU 信号导致适当的常量进入微地址线。地址中的每一位都有一个到 +5V 的上拉晶体管或一个到地的下拉晶体管。这种方法有些低效，因为每位需要两个晶体管位。相比之下，跳转地址 ROM 和指令地址 ROM 使用每个位一个晶体管位。

    https://static.righto.com/images/8087-decode/capacitors.jpg
    Two capacitors in the 8087. This photo shows the metal layer with the silicon and polysilicon underneath. Since capacitors are somewhat unusual in NMOS circuits, I'll show them in the photo above. If a polysilicon line crosses over doped silicon, it creates a transistor. However, if a polysilicon region sits on top of the doped silicon without crossing it, it forms a capacitor instead.

    8087 中的两个电容器。这张照片显示了金属层，下方有硅和多晶硅。由于电容器在 NMOS 电路中有些不寻常，我将在上面的照片中展示它们。如果多晶硅线穿过掺杂硅，它会创建一个晶体管。然而，如果多晶硅区域位于掺杂硅上方而不穿过它，它会形成一个电容器。（晶体管也存在电容，但栅极电容通常是不需要的。）

14. The documentation provides a hint that the microcode to load constants is complicated. Specifically, the documentation shows that different constants take different amounts of time to load. For instance, log2(e) takes 18 cycles while log2(10) takes 19 cycles and log10(2) takes 21 cycles. You'd expect that pre-computed constants would all take the same time, so the varying times show that more is happening behind the scenes.

    文档提供了一个提示，即加载常数的微码很复杂。具体来说，文档显示不同的常数需要不同的时间来加载。例如，log2(e) 需要 18 个周期，而 log2(10) 需要 19 个周期，log10(2) 需要 21 个周期。你会期望预计算的常数都需要相同的时间，因此变化的时间表明幕后发生了更多的事情。

---

## 批判性思考评论 / Critical Thinking Commentary

### 作者的主要论点分析

Ken Shirriff 这篇文章的核心论点是：Intel 8087 浮点协处理器的指令解码系统远比表面看起来复杂，它是多层解码机制（PLA、微码条件跳转、硬连线电路等）的叠加结果。作者通过逆向工程视角，揭示了这种复杂性并非设计失误，而是当时技术约束下的必要妥协——芯片面积极其珍贵，每减少几个晶体管都值得采用特殊技巧。

作者进一步指出，这种"临时拼凑"（ad hoc）的架构最终成功奠定了现代浮点标准（IEEE 754）的基础，尽管早期良品率低得惊人（每片晶圆仅两个可用芯片）。

### 文章的优点

1. **技术深度与可视化结合**：文章不仅有晶体管级别的电路分析，还配有大量显微镜照片和示意图，使抽象的硬件概念具象化。这种"考古式"技术写作风格独特且引人入胜。

2. **历史语境的呈现**：作者将技术选择置于1980年代的制造约束中考量，让读者理解为什么工程师会接受如此复杂的解决方案。这种"技术史"视角避免了用现代标准简单否定过去设计的陷阱。

3. **多层级解码逻辑的清晰梳理**：从 ModR/M 字节解析到微码入口点选择，再到硬连线指令处理，作者构建了一个层次分明的叙述结构，帮助读者理解不同解码机制的协作关系。

### 文章的局限与值得商榷之处

1. **对设计权衡的呈现不够全面**：文章强调了复杂度是为了节省芯片面积，但并未深入讨论这种选择带来的长期维护成本、验证难度和潜在可靠性问题。如果当时采用更简洁但稍大的设计，是否会加速 x87 浮点单元的普及？

2. **缺少与其他架构的比较**：文章将 8087 的解码复杂性视为必然，但没有对比同时代的其他浮点实现（如 Motorola 68881）。这种比较可能揭示 Intel 的设计是行业惯例还是特定约束下的特例。

3. **对"成功"的归因可能过于简化**：作者认为 8087 的成功在于其浮点标准被广泛采纳，但忽略了市场因素（IBM PC 的统治地位、软件兼容性需求）对技术标准锁定的影响。技术上"不够好但足够早"的方案往往胜过技术上更优但晚到的竞争者。

### 我的批判性视角

从计算机体系结构演进的角度看，8087 的解码复杂性体现了 CISC（复杂指令集）设计哲学的一个关键张力：**硬件复杂度 vs 软件便利性**。8087 将大量复杂性推向硬件，使汇编程序员能使用丰富的浮点指令，但这种做法的代价是硬件实现变得难以理解和验证。

值得注意的是，这种设计哲学在后来的 CPU 演进中被逐步抛弃。RISC 运动的核心主张正是将复杂性从硬件移回软件（编译器）。现代 x86 处理器虽然仍兼容 8087 指令集，但实际上通过内部解码将 CISC 指令转换为类似 RISC 的微操作（μops）执行。这暗示了 8087 的"临时电路"方法可能并非最优长期架构，而是特定历史条件下的权宜之计。

### 技术启示与当代意义

1. **技术债务的积累**：8087 的复杂解码机制成为 x86 架构的"技术债务"，至今仍需在现代处理器中维护兼容。这提醒我们：早期设计决策的约束会在技术栈中长期存在。

2. **逆向工程的价值**：作者通过物理拆解和显微镜分析还原历史芯片的方法，展示了当官方文档缺失或不完整时，逆向工程对技术史研究的关键作用。

3. **芯片面积与能效的权衡**：当时的优化目标（最小化晶体管数量）与当代芯片设计（在功耗约束下最大化性能）形成有趣对比。今天的设计师可能更愿意增加晶体管来简化控制逻辑，因为功耗而非面积成为主要约束。

总之，这篇文章不仅是对一个历史芯片的技术分析，更是对一个关键问题的案例研究：**当技术可能性边界与设计理想冲突时，工程师如何在约束中创造可行的解决方案**——以及这些解决方案如何在几十年后继续塑造我们使用的技术。
