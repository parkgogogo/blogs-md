Title: Intel 8087 浮点芯片中的指令解码 / Instruction Decoding in the Intel 8087 Floating-Point Chip
URL: http://www.righto.com/2026/02/8087-instruction-decoding.html

---

In the 1980s, if you wanted your IBM PC to run faster, you could buy an Intel 8087 floating-point coprocessor chip. With this chip, CAD software, spreadsheets, flight simulators, and other programs ran much faster.

在 1980 年代，如果你想让你的 IBM PC 运行得更快，你可以购买 Intel 8087 浮点协处理器芯片。有了这个芯片，CAD 软件、电子表格、飞行模拟器和其他程序都能快得多。

The 8087 chip could perform addition, subtraction, multiplication, and division, but it could also compute transcendental functions such as tangent and logarithm, as well as providing constants such as π. In total, the 8087 added 62 new instructions to the computer.

8087 芯片当然可以进行加法、减法、乘法和除法，但它还能计算正切和对数等超越函数，以及提供 π 等常数。总之，8087 为计算机增加了 62 条新指令。

But how did the PC decide if an instruction was a floating-point instruction for the 8087 or a regular instruction for the 8086 or 8088 CPU? And how did the 8087 chip interpret an instruction to figure out what it meant? It turns out that decoding an instruction inside the 8087 is more complex than you might think. The 8087 used multiple techniques and the decoding circuitry was spread across the chip. In this blog post, I'll explain how these decoding circuits worked.

但是 PC 如何决定一条指令是传给 8087 的浮点指令，还是传给 8086 或 8088 CPU 的普通指令呢？8087 芯片又是如何解读指令以确定其含义的？事实证明，在 8087 内部解码一条指令比你想像的更为复杂。8087 使用了多种技术，解码电路遍布整个芯片。在这篇博客文章中，我将解释这些解码电路的工作原理。

To reverse-engineer the 8087, I opened up an 8087 chip's ceramic package and took numerous photos of the silicon die with a microscope. The complex patterns on the die are formed by its metal wiring, along with the polysilicon and silicon underneath. The lower half of the chip is the "datapath", the circuitry that performs computations on 80-bit floating-point values. On the left side of the datapath, a constant ROM holds important constants such as π. On the right are the eight registers that programmers use to hold floating-point values; in an unusual design decision, these registers are arranged as a stack. Floating-point numbers cover a huge range of numbers by representing a number with a fractional part and an exponent; the 8087 has separate circuitry to handle the fraction and the exponent.

为了对 8087 进行逆向工程，我凿开了一个 8087 芯片的陶瓷封装，并用显微镜拍摄了硅晶片的众多照片。晶片上的复杂图案由其金属布线以及下方的多晶硅和硅形成。芯片的下半部分是"数据通路"，即对 80 位浮点值进行计算的电路。在数据通路的左侧，一个常数 ROM 保存着 π 等重要常数。在右侧是程序员用来保存浮点值的八个寄存器；在一个不寻常的设计决策中，这些寄存器被安排成一个堆栈。浮点数通过用分数部分和指数表示数字来覆盖巨大的范围；8087 有独立的电路来处理分数部分和指数。

https://static.righto.com/images/8087-decode/8087-die-labeled.jpg
Intel 8087 floating point unit chip die with main functional blocks labeled. The die is 5 mm × 6 mm. Click for a larger version.
Intel 8087 浮点单元芯片的晶片，主要功能块已标注。晶片尺寸为 5 毫米×6 毫米。点击图片（或任何其他图片）查看更大版本。

The chip's instructions are defined by the large microcode ROM in the middle. To execute an instruction, the 8087 first decodes the instruction and then the microcode engine starts executing the appropriate micro-instructions from the microcode ROM. In the upper right of the chip, the Bus Interface Unit (BIU) communicates with the main processor and memory over the computer's bus. The BIU and the rest of the chip run mostly independently, but as we will see, the BIU plays an important role in instruction decoding and execution.

芯片的指令由中间的大型微码 ROM 定义。为了执行一条指令，8087 先解码指令，然后微码引擎开始从微码 ROM 执行适当的微指令。在芯片的右上部分，总线接口单元（BIU）通过计算机的总线与主处理器和内存通信。在很大程度上，BIU 和芯片的其余部分独立运行，但正如我们将看到的，BIU 在指令解码和执行中扮演着重要角色。

## Cooperating with the main 8086/8088 processor / 与主 8086/8088 处理器的协作

The 8087 chip acted as a coprocessor to the main 8086 (or 8088) processor. When a floating-point instruction was encountered, the 8086 would let the 8087 floating-point chip execute the floating-point instruction. But how did the 8086 and 8087 decide which chip would execute a particular instruction? You might expect that the 8086 tells the 8087 when it should execute an instruction, but the cooperation is actually more complicated.

8087 芯片作为主 8086（或 8088）处理器的协处理器。当遇到浮点指令时，8086 会让 8087 浮点芯片执行该浮点指令。但是 8086 和 8087 如何决定由哪个芯片执行特定指令呢？你可能会期望 8086 告诉 8087 何时应该执行指令，但这种协作实际上更为复杂。

The 8086 has eight opcodes allocated to coprocessors, called ESCAPE opcodes. The 8087 determines what instruction the 8086 is executing by snooping on the bus, a task performed by the BIU (Bus Interface Unit). If the instruction is an ESCAPE instruction, the instruction is for the 8087. However, there's a problem. The 8087 can't access the 8086's registers (and vice versa), so the only way they can exchange data is through memory. But the 8086 addresses memory through a complex scheme involving offset registers and segment registers. How can the 8087 determine what memory address to use when it can't access the registers?

8086 有八个操作码分配给协处理器，称为 ESCAPE 操作码。8087 通过监视总线来确定 8086 正在执行什么指令，这个任务由 BIU（总线接口单元）执行。如果指令是 ESCAPE，则该指令是发给 8087 的。然而，这里有一个问题。8087 无法访问 8086 的寄存器（反之亦然），因此它们交换数据的唯一方式是通过内存。但 8086 通过涉及偏移寄存器和段寄存器的复杂方案来寻址内存。当 8087 无法访问寄存器时，它如何确定要使用什么内存地址呢？

The trick is that when an ESCAPE instruction is encountered, the 8086 processor starts executing the instruction, even though it is for the 8087. The 8086 calculates the memory address that the instruction references and reads that memory address, but ignores the result. Meanwhile, the 8087 watches the memory bus to see what address is accessed, and stores this address internally in a BIU register. When the 8087 starts executing the instruction, it uses the address from the 8086 to read or write memory. Essentially, the 8087 offloads the address calculation to the 8086 processor.

诀窍在于，当遇到 ESCAPE 指令时，8086 处理器开始执行该指令，即使它是发给 8087 的。8086 计算指令引用的内存地址并读取该内存地址，但忽略结果。与此同时，8087 监视内存总线以查看访问了什么地址，并将此地址内部存储在 BIU 寄存器中。当 8087 开始执行指令时，它使用来自 8086 的地址来读写内存。实际上，8087 将地址计算任务卸载给了 8086 处理器。

## The structure of 8087 instructions / 8087 指令的结构

To understand the 8087's instructions, we need to take a close look at the structure of 8086 instructions. In particular, something called the ModR/M byte is important because all 8087 instructions use it.

要理解 8087 的指令，我们需要仔细研究 8086 指令的结构。特别是，某种称为 ModR/M 字节的东西很重要，因为所有 8087 指令都使用它。

The 8086 uses a complex opcode system, mixing one-byte opcodes, prefix bytes, and longer instructions. About a quarter of the opcodes use a second byte, called the ModR/M, which specifies the registers and/or memory address to use through a complex encoding. For example, a memory address can be calculated by adding the BX and SI registers, or from the BP register plus a two-byte offset. The first two bits of the ModR/M byte are the "MOD" bits. For a memory access, the MOD bits indicate how many bytes of address displacement follow the ModR/M byte (0, 1, or 2), while the "R/M" bits specify how the address is calculated. However, a MOD value of 3 indicates that the instruction acts on a register and doesn't access memory.

8086 使用一个复杂的操作码系统，混合了单字节操作码、前缀字节和更长的指令。大约四分之一的操作码使用第二个字节，称为 ModR/M，它通过复杂的编码指定要使用的寄存器和/或内存地址。例如，内存地址可以通过将 BX 和 SI 寄存器相加计算，或从 BP 寄存器加上两字节偏移量计算。ModR/M 字节的前两位是"MOD"位。对于内存访问，MOD 位表示 ModR/M 字节后跟随的地址位移字节数（0、1 或 2），而"R/M"位指定地址的计算方式。然而，MOD 值为 3 表示指令在寄存器上操作，不访问内存。

https://static.righto.com/images/8087-decode/modrm.jpg
The structure of an 8087 instruction
一条 8087 指令的结构

The diagram above shows how an 8087 instruction consists of an ESCAPE opcode followed by the ModR/M byte. The ESCAPE opcode is indicated by the special bit pattern 11011, leaving three bits (in green) in the first byte available to specify the type of 8087 instruction. As described earlier, the ModR/M byte has two forms. The first form performs a memory access; its MOD bits are 00, 01, or 10, and the R/M bits specify how the memory address is calculated. This leaves three bits (green) to specify the instruction. The second form operates internally without a memory access; its MOD bits are 11. Since the second form doesn't use the R/M bits, six bits (green) in the R/M byte are available to specify the instruction.

上图显示了一条 8087 指令如何由 ESCAPE 操作码后跟 ModR/M 字节组成。ESCAPE 操作码由特殊的位模式 11011 指示，在第一个字节中留下三位（绿色）可用于指定 8087 指令的类型。如上所述，ModR/M 字节有两种形式。第一种形式执行内存访问；它的 MOD 位为 00、01 或 10，R/M 位指定内存地址的计算方式。这留下三位（绿色）来指定地址。第二种形式在内部操作，不进行内存访问；它的 MOD 位为 11。由于第二种形式不使用 R/M 位，R/M 字节中有六位（绿色）可用于指定指令。

The challenge for the 8087 designers was fitting all the instructions into the available bits so the decoding would be straightforward. The diagram below shows several 8087 instructions, illustrating how they achieve this. The first three instructions operate internally, so they have MOD bits of 11; the green bits specify the particular instruction. Addition is more complex because it can act on memory (the first format) or a register (the second format) depending on the MOD bits. All the ADD instructions have the same four bits (0000) highlighted in light green; the subtraction, multiplication, and division instructions use the same structure but have different values for the dark green bits. For instance, 0001 indicates multiplication, while 0100 indicates subtraction. The other green bits (MF, d, and P) select variants of the ADD instruction, changing the data format, the direction, and whether the stack is popped at the end. The last three bits select the R/M addressing mode for a memory operation, or the stack register ST(i) for a register operation.

8087 的设计者面临的挑战是如何将所有指令装入可用位中，使得解码变得简单明了。下图显示了几条 8087 指令，展示了它们如何实现这一点。前三条指令在内部操作，因此它们的 MOD 位为 11；绿色位指定特定的指令。加法更为复杂，因为它可以根据 MOD 位作用于内存（第一种格式）或寄存器（第二种格式）。所有 ADD 指令的亮绿色突出显示的四位（0000）相同；减法、乘法和除法指令使用相同的结构，但深绿色位有不同的值。例如，0001 表示乘法，0100 表示减法。其他绿色位（MF、d 和 P）选择加法指令的变体，改变数据格式、方向和最后弹出堆栈。最后三位为内存操作选择 R/M 寻址模式，或为寄存器操作选择堆栈寄存器 ST(i)。

https://static.righto.com/images/8087-decode/opcodes.jpg
The bit patterns for some 8087 instructions. Based on datasheet.
一些 8087 指令的位模式。基于数据表。

## Selecting a microcode routine / 选择微码例程

Most of the 8087's instructions are implemented in microcode, with low-level "micro-instructions" implementing each step of the instruction. The 8087 chip contains a microcode engine; you can think of it as a miniature CPU that controls the 8087 by executing micro-instructions from microcode routines. The microcode engine provides an 11-bit micro-address to the ROM, specifying the micro-instruction to execute. Normally, the microcode engine steps sequentially through the microcode, but it also supports conditional jumps and subroutine calls.

8087 的大多数指令都是用微码实现的，用低级别的"微指令"实现指令的每一步。8087 芯片包含一个微码引擎；你可以把它看作是一个迷你 CPU，通过一次执行一条微指令来控制 8087 执行微码例程。微码引擎向 ROM 提供一个 11 位微地址，指定要执行的微指令。通常，微码引擎按顺序遍历微码，但它也支持条件跳转和子程序调用。

But how does the microcode engine know where to start executing microcode for a particular machine instruction? Conceptually, you could put the instruction opcode into a ROM that would provide the starting micro-address. However, this would be impractical, requiring a 2048-word ROM to decode an 11-bit opcode. (Although a 2K ROM is tiny now, it was large at the time; the 8087's microcode ROM was just 1648 words, already a tight fit.) Instead, the 8087 uses a more efficient (but more complex) instruction decoding system built from a combination of logic gates and a PLA (Programmable Logic Array). This system holds 22 microcode entry points, which is much more practical than 2048.

但是微码引擎如何知道从哪里开始执行特定机器指令的微码呢？从概念上讲，你可以将指令操作码输入一个 ROM，它会提供起始微地址。然而，这将是不切实际的，因为需要一个 2048 字的 ROM 来解码一个 11 位操作码。（虽然 2K ROM 现在很小，但在当时很大；8087 的微码 ROM 只有 1648 字，已经是一个紧张的适配。）相反，8087 使用一个更有效（但更复杂）的指令解码系统，由逻辑门和 PLA（可编程逻辑阵列）组合构建而成。这个系统保存 22 个微码入口点，比 2048 实用得多。

Processors often use a circuit called a PLA (Programmable Logic Array) as part of instruction decoding. The idea of a PLA is to provide a dense but flexible way to implement arbitrary logic functions. Any Boolean logic function can be expressed as a "sum of products", a set of AND terms (the products) combined with OR operations (the sum). The PLA has one block of circuitry called the AND plane that generates the desired sum terms. The outputs from the AND plane feed into a second block, the OR plane, which combines the terms with OR operations. Physically, the PLA is implemented as a grid where each position in the grid can have a transistor or not. By changing the pattern of transistors, the PLA implements the desired functions.

处理器经常使用一种称为 PLA（可编程逻辑阵列）的电路作为指令解码的一部分。PLA 的想法是提供一种密集而灵活的方式来实现任意逻辑功能。任何布尔逻辑功能都可以表示为"积之和"，即一组 AND 项（积）通过 OR 运算组合在一起（求和）。PLA 有一个称为 AND 平面的电路块，生成所需的求和项。AND 平面的输出被送入第二个块，即 OR 平面，它将各项通过 OR 运算组合在一起。物理上，PLA 被实现为一个网格，其中网格中的每个位置可以有晶体管，也可以没有。通过改变晶体管模式，PLA 实现了所需的功能。

https://static.righto.com/images/8087-decode/pla-structure.jpg
A simplified diagram of a PLA.
PLA 的简化示意图。

A PLA can implement arbitrary logic, but in the 8087, the PLA acts mostly as an optimized ROM. The AND plane matches bit patterns and selects entries from the OR plane, which holds the output values, the micro-address for each routine. The advantage of a PLA over a standard ROM is that one column of outputs can be used for many different inputs, reducing the size.

PLA 可以实现任意逻辑，但在 8087 中，PLA 通常充当优化的 ROM。AND 平面匹配位模式，从 OR 平面中选择条目，OR 平面保存输出值，即每个例程的微地址。PLA 相对于标准 ROM 的优势在于，一列输出可以用于许多不同的输入，从而减小尺寸。

The photo below shows part of the instruction decode PLA. The horizontal input lines are polysilicon wires on top of the silicon. The pinkish regions are doped silicon. When polysilicon crosses doped silicon, it creates a transistor (green). Where the doped silicon has a gap, there is no transistor (red). (The output lines run vertically but are not visible here; I dissolved the metal layer to show the silicon underneath.) If a polysilicon line is energized, it turns on all the transistors in its row, pulling the associated output column low. (If no transistors are turned on, a pull-up transistor pulls the output high.) Thus, the pattern of doped silicon regions creates a grid of transistors in the PLA, implementing the desired logic functions.

下图显示了指令解码 PLA 的一部分。水平输入线是硅片顶部的多晶硅线。粉红色区域是掺杂硅。当多晶硅穿过掺杂硅时，它会创建一个晶体管（绿色）。当掺杂硅有间隙时，就没有晶体管（红色）。（输出线垂直运行，但在这里不可见；我溶解了金属层以显示下方的硅。）如果多晶硅线通电，它会打开其行中的所有晶体管，将相关的输出列拉低。（如果没有晶体管被打开，上拉晶体管会将输出拉高。）因此，掺杂硅区域的图案在 PLA 中创建了一个晶体管网格，实现了所需的逻辑功能。

https://static.righto.com/images/8087-decode/pla-diagram.jpg
Part of the instruction decode PLA.
指令解码 PLA 的一部分。

The standard way of decoding instructions with a PLA is to feed the instruction bits (and their complements) as inputs. The PLA can then pattern-match based on the bit patterns in the instruction. However, the 8087 also uses some preprocessing to shrink the size of the PLA. For example, the MOD bits are processed to generate one signal if the bits are 0, 1, or 2 (i.e. a memory operation), and a second signal if the bits are 3 (i.e. a register operation). This allows the cases for 0, 1, and 2 to be handled by a single PLA pattern. Another signal indicates if the high bits are 001 111xxxxx; this indicates that the R/M field participates in instruction selection. Sometimes a PLA output is fed back as an input, so one group of decoded instructions can be excluded from another. These techniques all shrink the size of the PLA at the cost of some additional logic gates.

用 PLA 解码指令的标准方式是将指令位（及其补码）作为输入。然后 PLA 可以根据指令中的位模式进行模式匹配。然而，8087 还使用了一些预处理来减小 PLA 的尺寸。例如，MOD 位被处理以生成一个信号，如果位是 0、1 或 2（即内存操作），以及第二个信号，如果位是 3（即寄存器操作）。这允许 0、1 和 2 的情况由单个 PLA 模式处理。另一个信号表示高位是 001 111xxxxx；这表明 R/M 字段参与指令选择。有时 PLA 输出被反馈作为输入，因此一组解码的指令可以从另一组中排除。这些技术都以一些额外的逻辑门为代价减小了 PLA 的尺寸。

The result of the AND plane of the instruction decode PLA is 22 signals, one for each instruction or group of instructions that share a microcode entry point. The lower part of the instruction decode PLA acts as a ROM, holding the 22 microcode entry points and providing the selected entry point.

指令解码 PLA 的 AND 平面的结果是 22 个信号，每个信号对应一个指令或共享微码入口点的指令组。指令解码 PLA 的下部充当一个 ROM，保存 22 个微码入口点并提供所选的入口点。

## Instruction decoding inside the microcode / 微码内部的指令解码

Many 8087 instructions share the same microcode routine. For instance, the addition, subtraction, multiplication, division, reverse subtraction, and reverse division instructions all go to the same microcode routine. This reduces the size of the microcode, since these instructions share microcode that sets up the instruction and processes the results. However, the microcode obviously needs to branch at some point to perform the specific operation. Moreover, some arithmetic opcodes access the top of the stack, some access an arbitrary location in the stack, some access memory, and some reverse the operands, requiring different microcode operations. How does the microcode do different things for the different opcodes while sharing code?

许多 8087 指令共享相同的微码例程。例如，加法、减法、乘法、除法、反向减法和反向除法指令都进入相同的微码例程。这减小了微码的尺寸，因为这些指令共享设置指令和处理结果的微码。然而，微码显然需要在某个时刻分叉以执行特定的操作。此外，一些算术操作码访问堆栈顶部，一些访问堆栈中的任意位置，一些访问内存，一些反转操作数，需要不同的微码操作。微码如何为不同的操作码做不同的事情，同时共享代码呢？

The trick is that the 8087's microcode engine supports conditional subroutine calls, returns, and jumps based on 49 different conditions. In particular, fifteen of the conditions examine the instruction. Some conditions test for specific bit patterns, such as branching if the low bit is set, or more complex patterns such as opcode matching 0xx 11xxxxxx. Other conditions detect specific instructions such as FMUL. The result is that the microcode can take different paths for different instructions. For instance, the reverse subtraction or reverse division is implemented by the microcode testing the instruction and swapping the arguments if necessary, while sharing the rest of the code.

诀窍在于 8087 的微码引擎支持基于 49 种不同条件的条件子程序调用、返回和跳转。特别是，十五个条件检查指令。一些条件测试特定的位模式，例如如果最低位被设置则分支，或更复杂的模式如操作码匹配 0xx 11xxxxxx。其他条件检测特定指令，如 FMUL。结果是微码可以为不同指令采用不同的路径。例如，反向减法或反向除法是通过微码测试指令并在必要时反转参数来实现的，同时共享其余代码。

The microcode also has a special jump target that performs a three-way jump based on the machine instruction currently being executed. The microcode engine has a jump ROM that holds entry points for 22 jumps or subroutine calls. However, jumping to target 0 uses special circuitry so it will instead jump to target 1 (if it is a multiply instruction), target 2 (if it is an addition/subtraction), or target 3 (if it is a divide). This special jump is implemented by the gates in the upper right of the jump decoder.

微码还有一个特殊的跳转目标，根据当前正在执行的机器指令执行三分支跳转。微码引擎有一个跳转 ROM，保存 22 个跳转或子程序调用的入口点。然而，跳转到目标 0 使用特殊电路，因此它将改为跳转到目标 1（如果是乘法指令）、目标 2（如果是加法/减法）或目标 3（如果是除法）。这个特殊的跳转由跳转解码器右上角的门实现。

https://static.righto.com/images/8087-decode/jump-rom.jpg
The jump decoder and ROM. Note that the rows are not in numeric order; apparently this made the layout slightly more compact. Click for larger version.
跳转解码器和 ROM。注意行不是按数字顺序排列的；显然，这使得布局稍微更紧凑。点击图片（或任何其他图片）查看更大版本。

## Hardwired instruction processing / 硬连线指令处理

Some of the 8087's instructions are implemented directly by hardware in the Bus Interface Unit (BIU), rather than using microcode. For example, the instructions that enable or disable interrupts, or save or restore the state, are implemented in hardware. The decoding of these instructions is performed by circuitry separate from the instruction decoder described above.

8087 的一些指令由总线接口单元（BIU）中的硬件直接实现，而不是使用微码。例如，启用或禁用中断的指令，或保存或恢复状态的指令，都是用硬件实现的。这些指令的解码由与上述指令解码器分开的电路执行。

In the first step, a small PLA decodes the first 5 bits of the instruction. Most importantly, if these bits are 11011, that indicates an ESCAPE instruction, the start of an 8087 operation. This causes the 8087 to start interpreting the instruction and storing the opcode in a BIU register for the instruction decoder. A second small PLA takes the output from the top-5 PLA and combines it with the low three bits. It decodes the specific instruction values: D9, DB, DD, E0, E1, E2, or E3. The first three values correspond to specific ESCAPE instructions and are recorded in a latch.

在第一步，一个小型 PLA 解码指令的前 5 位。最重要的是，如果这些位是 11011，则表示 ESCAPE 指令，即 8087 操作的开始。这会导致 8087 开始解释指令并将操作码存储在 BIU 寄存器中供指令解码器使用。第二个小型 PLA 从 top-5 PLA 获取输出并将其与低三位组合。它解码特定的指令值：D9、DB、DD、E0、E1、E2 或 E3。前三个值对应特定的 ESCAPE 指令，并被记录在锁存器中。

The two PLAs decode the second byte in the same way. Logic gates combine the PLA outputs from the second byte with the latched values from the first byte, detecting eleven hardwired instructions. Some of these instructions operate directly on registers, such as clearing an exception; the decoded instruction signal goes to the appropriate register and modifies it in an ad hoc way. Other hardwired instructions are more complex, writing the chip's status to memory or reading the status from memory. These instructions require multiple memory operations, controlled by the Bus Interface Unit's state machine. Each of these instructions has a flip-flop that gets triggered by the decoded instruction to keep track of which instruction is active.

两个 PLA 以相同的方式解码第二个字节。逻辑门将来自第二个字节的 PLA 输出与来自第一个字节的锁存值组合，检测十一个硬连线指令。其中一些指令直接在寄存器上操作，例如清除异常；解码的指令信号进入相关寄存器并以临时方式修改它。其他硬连线指令更为复杂，将芯片状态写入内存或从内存读取芯片状态。这些指令需要多次内存操作，由总线接口单元的状态机控制。这些指令中的每一个都有一个触发器，由解码的指令触发以跟踪哪个指令处于活动状态。

For the instructions that save and restore the 8087's state (FSAVE and FRSTOR), there is an additional complication. These instructions are partially implemented in the BIU, which moves the relevant BIU registers into or out of memory. But then, the instruction processing switches to microcode, where microcode routines save or load the floating-point registers. The jump to the microcode routines is not implemented through the regular microcode jump circuitry. Instead, two hard-coded values force the microcode address to be set to the save or restore routine.

对于保存和恢复 8087 状态的指令（FSAVE 和 FRSTOR），还有一个额外的复杂性。这些指令部分在 BIU 中实现，BIU 将相关的 BIU 寄存器移入或移出内存。但随后，指令处理切换到微码，在微码例程保存或加载浮点寄存器。跳转到微码例程不是通过常规微码跳转电路实现的。相反，两个硬编码值强制将微码地址设置为保存或恢复例程。

## Constants / 常数

The 8087 has seven instructions to load floating-point constants such as π, 1, or log₁₀(2). The 8087 has a constant ROM that holds these constants, as well as constants used for transcendental operations. You might expect that the 8087 would simply load the specified constant from the constant ROM, using the instruction to select the desired constant. However, the process is much more complex.

8087 有七条指令用于加载浮点常数，如 π、1 或 log10(2)。8087 有一个常数 ROM，保存这些常数，以及用于超越运算的常数。你可能会期望 8087 简单地从常数 ROM 加载指定的常数，使用指令来选择所需的常数。然而，这个过程要复杂得多。

Looking at the instruction decode ROM reveals that different constants are implemented with different microcode routines: the constant load instructions FLDLG2 and FLDLN2 have one entry point; FLD1, FLD2E, FLDL2T, and FLDPI have a second entry point, and FLDZ (zero) has a third entry point. It's understandable that zero is a special case, but why do the other constants have two routines?

查看指令解码 ROM 显示，不同的常数用不同的微码例程实现：常数加载指令 FLDLG2 和 FLDLN2 有一个入口点；FLD1、FLD2E、FLDL2T 和 FLDPI 有第二个入口点，FLDZ（零）有第三个入口点。可以理解零是一个特殊情况，但为什么其他常数有两个例程呢？

The explanation is that the fraction part of each constant is stored in the constant ROM, but the exponent is stored in a separate, smaller ROM. To shrink the size of the exponent ROM, only the exponents that were necessary are stored. If a constant needs an exponent one larger than a value in the ROM, the microcode adds 1 to the ROM value, computing the exponent on the fly.

解释是每个常数的分数部分存储在常数 ROM 中，但指数存储在一个单独的、较小的 ROM 中。为了减小指数 ROM 的尺寸，只存储了一些必要的指数。如果常数需要的指数比 ROM 中的值大 1，微码会将指数 ROM 值加 1，即时计算指数。

Thus, the constant load instructions use three separate instruction decoding mechanisms. First, the instruction decode ROM determines the appropriate microcode routine for the constant instruction, as described earlier. Second, the constant PLA decodes the instruction to select the appropriate constant. Finally, the microcode routine tests the low bit of the instruction and increments the exponent if necessary.

因此，加载常数指令使用三个独立的指令解码机制。首先，指令解码 ROM 确定常数指令的适当微码例程，如前所述。然后，常数 PLA 解码指令以选择适当的常数。最后，微码例程测试指令的最低位，并在必要时递增指数。

## Conclusion / 结论

To summarize the discussion of the decoding circuitry, the diagram below shows how the different circuits are arranged on the die. This image shows the upper right part of the die; the microcode engine is on the left and part of the ROM is at the bottom.

为了总结解码电路的讨论，下图显示了不同电路在晶片上的排列方式。此图像显示晶片的右上部分；微码引擎在左侧，ROM 的一部分在底部。

https://static.righto.com/images/8087-decode/decoding-labeled.jpg
Upper left part of the 8087 die with functional blocks labeled.
8087 晶片的左上部分，功能块已标注。

The 8087 doesn't have a clean, elegant architecture, but is full of ad hoc circuitry and special cases. The 8087's instruction decoding is one example. Because of the 8086's complex instruction format and the ModR/M byte, decoding starts out complicated. On top of this, the 8087's instruction decoding has multiple layers: an instruction decode PLA, microcode conditional branches that depend on the instruction, a special jump target that depends on the instruction, constant selection based on the instruction, and instructions decoded by the BIU.

8087 没有简洁的架构，而是充满了临时电路和特殊情况。8087 的指令解码就是一个例子。由于 8086 复杂的指令格式和 ModR/M 字节，解码一开始就复杂。除此之外，8087 的指令解码还有多个层次：指令解码 PLA、依赖于指令的微码条件跳转、依赖于指令的特殊跳转目标、基于指令选择的常数，以及由 BIU 解码的指令。

The 8087 has this complex architecture for a reason: at the time, chips were at the edge of what was technologically possible, so the designers needed to use any technique to shrink the chip. If implementing a special case would remove a few transistors from the chip or make the microcode ROM slightly smaller, the special case was worthwhile. Even so, the 8087 was initially almost impossible to manufacture; early yields were two working chips per silicon wafer. Despite this rocky start, the floating-point standard based on the 8087 is now part of almost every processor.

8087 有这种复杂架构是有原因的：在当时，芯片处于技术可能的边缘，因此设计者需要使用任何技术来减小芯片尺寸。如果实现一个特殊情况可以从芯片上减少几个晶体管或使微码 ROM 稍微小一点，这个特殊情况就是值得的。即便如此，8087 最初几乎无法制造；早期产量每片硅晶片只有两个工作芯片。尽管起步艰难，但基于 8087 的浮点标准现在几乎已成为每个处理器的一部分。

Thanks to the members of the "Opcode Collective", especially Smartest Blob and Gloriouscow.

感谢"Opcode Collective"的成员，特别是 Smartest Blob 和 Gloriouscow。

For updates, follow me on Bluesky (@righto.com), Mastodon (@kenshirriff@oldbytes.space), or RSS.

如需更新，请在 Bluesky (@righto.com)、Mastodon (@kenshirriff@oldbytes.space) 或 RSS 上关注我。

---

## Notes and references / 注释和参考文献

The contents of the microcode ROM are available here, with partial decoding due to Smartest Blob. ↩

微码 ROM 的内容可在此处获取，部分解码归功于 Smartest Blob。[↩]

The 8087 has difficulty figuring out what the 8086 is doing because the 8086 prefetches instructions. Thus, when an instruction is seen on the bus, the 8086 might execute it at some point in the future, or it might get discarded. To tell what instructions are being executed, the 8087 floating-point chip has a copy of the 8086 processor's queue inside it. The 8087 watches the memory bus and copies any prefetched instructions. Since the 8087 can't tell from the bus when the 8086 starts a new instruction or when it flushes the queue to jump to a new address, the 8086 processor provides two queue status signals to the 8087. With the help of these signals, the 8087 knows exactly what the 8086 is executing. The 8087's instruction queue has six 8-bit registers, the same as the 8086. Surprisingly, the last two queue registers in the 8087 are wired together so only five queue registers are usable. My hypothesis is that since the 8087 copies the active instruction into a separate register (unlike the 8086), only five queue registers are needed. This raises the question of why the extra registers weren't removed from the die, wasting valuable space. The 8088 processor used for the IBM PC has a four-byte queue instead of a six-byte queue. The 8088 is almost the same as the 8086, except that it has an 8-bit memory bus instead of a 16-bit memory bus. Because the memory bus is narrower, prefetching is more likely to get in the way of other memory accesses, so the smaller prefetch queue is implemented. Knowing the queue size is essential for the 8087 floating-point chip. To indicate this, one signal when the processor starts up lets the 8087 determine if the attached processor is an 8086 or an 8088. ↩

8087 很难确定 8086 在做什么，因为 8086 会预取指令。因此，当在总线上看到指令时，8086 可能会在未来的某个点执行它，或者它可能会被丢弃。为了告诉正在执行什么指令，8087 浮点芯片在内部复制了 8086 处理器的队列。8087 监视内存总线并复制预取的任何指令。由于 8087 无法从总线判断 8086 何时开始新指令或何时清空队列跳转到新地址，8086 处理器向 8087 提供两个队列状态信号。在这些信号的帮助下，8087 确切知道 8086 正在执行什么。8087 的指令队列有六个 8 位寄存器，与 8086 相同。令人惊讶的是，8087 中的最后两个队列寄存器连接在一起，因此只有五个可用的队列寄存器。我的假设是，由于 8087 将活动指令复制到单独的寄存器中（与 8086 不同），只需要五个队列寄存器。这就提出了一个问题，为什么多余的寄存器没有从晶片上移除，而是浪费宝贵的空间。用于 IBM PC 的 8088 处理器有一个四字节的队列，而不是六字节的队列。8088 与 8086 几乎相同，只是它有 8 位内存总线而不是 16 位内存总线。由于内存总线较窄，预取更有可能妨碍其他内存访问，因此实现了较小的预取队列。知道队列大小对 8087 浮点芯片至关重要。为了指示这一点，当处理器启动时，一个信号让 8087 确定连接的处理器是 8086 还是 8088。[↩]

The relevant part of the opcode is 11 bits: the first 5 bits are always 11011 for an ESCAPE opcode, so they can be ignored during decoding. The Bus Interface Unit has a 3-bit register that holds the first byte of the instruction, and an 8-bit register that holds the second byte. The BIU registers have an irregular appearance because there are 3-bit registers, 8-bit registers, and 10-bit registers (which hold half of a 20-bit address). ↩

操作码的相关部分是 11 位：前 5 位对于 ESCAPE 操作码总是 11011，因此可以在解码期间忽略它们。总线接口单元有一个 3 位寄存器保存指令的第一个字节，一个 8 位寄存器保存第二个字节。BIU 寄存器有不规则的外观，因为有 3 位寄存器、8 位寄存器和 10 位寄存器（保存 20 位地址的一半）。[↩]

What's the difference between a PLA and a ROM? There's a lot of overlap: a ROM can be substituted for a PLA, and a PLA can implement a ROM. A ROM is essentially a PLA where the first stage is a binary decoder, so the ROM has separate rows for each input value. However, the first stage of a ROM can be optimized so multiple inputs share the same output values; is that a ROM or a PLA? The "official" distinction is that in a ROM, one row is activated at a time, while in a PLA, multiple rows can be active at the same time, so the output values are combined. (Thus, reading a value from a ROM is straightforward, but reading a value from a PLA is more difficult.) I think the instruction decode PLA is best described as a PLA first stage that acts as a ROM second stage. You could also call it a partially-decoded ROM, or just a PLA. Hopefully my terminology won't be too confusing. ↩

PLA 和 ROM 有什么区别？有很多重叠：ROM 可以替代 PLA，而 PLA 可以实现 ROM。ROM 本质上是一个 PLA，其中第一阶段是二进制解码器，因此 ROM 对每个输入值都有单独的行。然而，ROM 的第一阶段可以优化，使多个输入共享相同的输出值；这是 ROM 还是 PLA？"官方"的区别在于，在 ROM 中，一次激活一行，而在 PLA 中，可以同时激活多行，因此输出值被组合。（因此，从 ROM 中读取值很简单，但从 PLA 中读取值则更困难。）我认为指令解码 PLA 最好被描述为具有充当 ROM 的第二阶段的 PLA 第一阶段。你也可以称它为部分解码的 ROM，或者只是 PLA。希望我的术语不会太令人困惑。[↩]

To match a bit pattern in the instruction, the bits of the instruction are fed into the PLA, along with the complements of these bits; this allows the PLA to match 0 bits or 1 bits. Each row in the PLA's AND plane will match a particular bit pattern in the instruction: bits that must be 1, bits that must be 0, and bits that don't matter. If the instruction opcodes were allocated sensibly, a small number of bit patterns would match all the opcodes, reducing the size of the decoder. I may be stretching the analogy too far, but a PLA is a lot like a neural network. Each column in the AND plane is like a neuron that fires when it recognizes a specific input pattern. The OR plane is like a second layer in the neural network, combining the signals from the first layer. The PLA's "weights", however, are fixed at 0 or 1, so it isn't as flexible as a "real" neural network. ↩

为了匹配指令中的位模式，指令的位被输入 PLA，以及这些位的补码；这允许 PLA 匹配 0 位或 1 位。PLA 的 AND 平面中的每一行将匹配指令中的特定位模式：必须为 1 的位、必须为 0 的位和不重要的位。如果指令操作码被合理分配，少量的位模式将匹配所有操作码，从而减小解码器的尺寸。我可能在这个类比上走得太远，但 PLA 很像神经网络。AND 平面中的每一列就像一个神经元，在识别特定输入模式时触发。OR 平面就像神经网络中的第二层，组合来自第一层的信号。PLA 的"权重"然而固定在 0 或 1，因此它不像"真正的"神经网络那样灵活。[↩]

The instruction decode PLA has an unusual layout where the second plane is rotated 90°. In a regular PLA (left), the inputs (red) go into the first stage, the vertical outputs from the first stage (purple) go into the second stage, and the PLA outputs (blue) exit parallel to the inputs. However, in the address PLA, the second stage is rotated 90°, so the outputs are perpendicular to the inputs. This approach requires additional wiring (horizontal purple lines), but presumably this layout worked out better in the 8087 because the outputs line up with the rest of the microcode engine. https://static.righto.com/images/8087-decode/folded.jpg A regular PLA conceptually on the left and the rotated PLA on the right. ↩

指令解码 PLA 有一个不寻常的布局，其中第二个平面旋转了 90°。在常规 PLA（左）中，输入（红色）进入第一阶段，第一阶段的垂直输出（紫色）进入第二阶段，PLA 输出（蓝色）与输入平行退出。然而，在地址 PLA 中，第二阶段旋转了 90°，因此输出与输入垂直。这种方法需要额外的布线（水平紫色线），但推测这种布局在 8087 中工作得更好，因为输出与其余微码引擎对齐。https://static.righto.com/images/8087-decode/folded.jpg 左侧是常规 PLA 的概念图，右侧是旋转的 PLA。[↩]

To describe the implementation of the PLA in more detail, the transistors in each row of the AND plane form a NOR gate, because if any transistor is turned on, it will pull the output low. Likewise, the transistors in each column of the OR plane form a NOR gate. So why is a PLA described as having an AND plane and an OR plane, rather than two NOR planes? Using De Morgan's laws, you can treat the NOR-NOR Boolean equation as equivalent to an AND-OR Boolean equation (with the inputs and outputs inverted). It's usually easier to understand the logic as AND terms combined with OR operations. The reverse question is why they didn't build the PLA from AND and OR gates, but instead from NOR gates? The reason is that it is harder to build AND and OR gates using NMOS transistors because explicit inverter circuits would need to be added. Also, NMOS NOR gates are usually faster than NAND gates because the transistors are in parallel. (CMOS is the opposite; NAND gates are faster because the weaker PMOS transistors are in parallel.) ↩

为了更详细地描述 PLA 的实现，AND 平面中每行的晶体管形成一个 NOR 门，因为如果任何晶体管被打开，它会将输出拉低。同样，OR 平面中每列的晶体管形成一个 NOR 门。那么为什么 PLA 被描述为具有 AND 平面和 OR 平面，而不是两个 NOR 平面呢？通过使用德摩根定律，你可以将 NOR-NOR 布尔方程视为等效于 AND-OR 布尔方程（输入和输出反转）。通常更容易理解逻辑为 AND 项通过 OR 运算组合在一起。相反的问题是为什么他们不从 AND 和 OR 门构建 PLA，而是从 NOR 门构建？原因是使用 NMOS 晶体管构建 AND 和 OR 门更难，因为需要添加显式反相器电路。此外，NMOS NOR 门通常比 NAND 门更快，因为晶体管是并联的。（CMOS 则相反；NAND 门更快，因为较弱的 PMOS 晶体管是并联的。）[↩]

The 8087 opcodes can be organized into tables, showing the underlying structure. (In each table, the row (Y) coordinate is the low 3 bits of the first byte and the column (X) coordinate is the 3 bits after the MOD bits in the second byte.) Memory operations use the following encoding, with MOD = 0, 1, or 2. Each box represents 8 different addressing modes.

8087 的操作码可以组织成表格，显示底层结构。（在每个表中，行（Y）坐标是第一个字节的低 3 位，列（X）坐标是第二个字节中 MOD 位后的 3 位。）内存操作使用以下编码，MOD = 0、1 或 2。每个框代表 8 种不同的寻址模式。

[Opcode tables omitted - see original article for full tables]

The important point is that the instruction encoding has a lot of regularity, making the decoding easier. For instance, the basic arithmetic operations (FADD through FDIVR) are repeated in alternating rows. However, the tables also have significant irregularities, which complicates the decoding. ↩

重要的点是指令编码有很多规律性，使解码过程更容易。例如，基本算术运算（FADD 到 FDIVR）在交替行中重复。然而，表格也有显著的不规则性，这 complicates 了解码过程。[↩]

The 22 outputs from the instruction decoder PLA correspond to the following instruction groups, activating a row of the ROM and yielding the corresponding microcode address. From this table, you can see which instructions are grouped together in the microcode. [Table omitted - see original article]

指令解码器 PLA 的 22 个输出对应于以下指令组，激活 ROM 的一行并产生相应的微码地址。从这个表中，你可以看到哪些指令在微码中组合在一起。[表格省略 - 见原文]

The instruction decode PLA has 22 entries, and the jump table also has 22 entries. It is a coincidence that these values are the same. An entry in the jump table ROM is selected by 5 bits from the micro-instruction. The ROM is structured as two 11-bit words per row, interleaved. (The 22 is also a coincidence.) The high 4 bits of the jump number select a row in the ROM, while the low bit selects one of the two rows. This implementation is modified for target 0 (the three-way jump). If the current instruction is a multiply, the first row of ROM is selected for target 0, or target 1. If the current instruction is an addition or subtraction, the second row is selected for target 0, or target 2. If the current instruction is a divide, the third row is selected for target 0, or target 3. Thus, target 0 ends up selecting row 1, 2, or 3. However, keep in mind that each row has two words, selected by the low bit of the target number. The problem is that target 0 with multiply would access the left word of row 1, while target 1 would access the right word of row 1, but both should provide the same address. The solution is that rows 1, 2, and 3 store the same address twice in each row, so these rows each "waste" a value. For reference, the contents of the jump table are: [Table omitted]

指令解码 PLA 有 22 个条目，跳转表也有 22 个条目。这些值相同是巧合。跳转表 ROM 中的一个条目由微指令的 5 位选择。ROM 的结构是每行两个 11 位字，交错排列。（有 22 位也是巧合。）跳转号的高 4 位选择 ROM 中的一行，而最低位选择两行之一。此实现针对目标 0（三分支跳转）进行了修改。如果当前指令是乘法，则选择第一行 ROM 作为目标 0，或作为目标 1。如果当前指令是加法或减法，则选择第二行作为目标 0，或作为目标 2。如果当前指令是除法，则选择第三行作为目标 0，或作为目标 3。因此，目标 0 最终选择第 1、2 或 3 行。然而，请记住，每行有两个字，由目标号的低位选择。问题在于目标 0 与乘法将访问第 1 行的左字，而目标 1 将访问第 1 行的右字，但两者都应提供相同的地址。解决方案是第 1、2 和 3 行在每行中存储相同的地址两次，因此这些行每个都"浪费"一个值。供参考，跳转表的内容是：[表格省略]

Eleven instructions are implemented in BIU hardware. Four of them are relatively simple, setting or clearing bits: FINIT (initialize), FENI (enable interrupts), FDISI (disable interrupts), and FCLEX (clear exceptions). Six are more complex, storing the status to memory or loading the status from memory: FLDCW (load control word), FSTCW (store control word), FSTSW (store status word), FSTENV (store environment), FLDENV (load environment), FSAVE (save state), and FRSTOR (restore state). As explained elsewhere, the last two instructions are partially implemented in microcode. ↩

十一个指令在 BIU 硬件中实现。其中四个相对简单，设置或清除位：FINIT（初始化）、FENI（启用中断）、FDISI（禁用中断）和 FCLEX（清除异常）。其中六个更为复杂，将状态存储到内存或从内存加载状态：FLDCW（加载控制字）、FSTCW（存储控制字）、FSTSW（存储状态字）、FSTENV（存储环境）、FLDENV（加载环境）、FSAVE（保存状态）和 FRSTOR（恢复状态）。如其他地方所解释的，最后两个指令部分在微码中实现。[↩]

Even seemingly trivial instructions use more circuitry than you'd expect. For example, the FCLEX (clear exceptions) instruction, after being decoded, the signal goes through nine gates before clearing the exception bits in the status register. Along the way, it goes through a flip-flop to synchronize the timing, a gate to combine it with a reset signal, and various inverters and drivers. Even though these instructions seem like they should be immediate, they typically take 5 clock cycles due to the 8087's overhead. ↩

即使看似微不足道的指令也使用比你预期更多的电路。例如，FCLEX（清除异常）指令解码后，信号在清除状态寄存器中的异常位之前通过九个门。在此过程中，它经过一个触发器以同步时序，一个门将其与复位信号组合，以及各种反相器和驱动器。尽管这些指令看起来应该立即完成，但它们通常由于 8087 的开销而需要 5 个时钟周期。[↩]

I'll provide more detail here on the circuitry that jumps to the save or restore microcode. The BIU sends two signals to the microcode engine, one to jump to the save code and one to jump to the restore code. These signals are buffered and delayed by capacitors, presumably to adjust the timing of the signals. In the microcode engine, there are two hard-coded constants for the routines, right above the jump table; the BIU signal causes the appropriate constant onto the micro-address lines. Each bit in the address has either a pull-up transistor to +5V or a pull-down transistor to ground. This approach is somewhat inefficient because each bit takes two transistor bits. In comparison, the jump address ROM and the instruction address ROM use one transistor bit per bit. (As in the PLA, each transistor is present or absent as needed, so there are fewer physical transistors than transistor bits.) https://static.righto.com/images/8087-decode/capacitors.jpg Two capacitors in the 8087. This photo shows the metal layer, with silicon and polysilicon underneath. Since capacitors are somewhat unusual in NMOS circuitry, I'll show them in the photo above. If a polysilicon line crosses doped silicon, it creates a transistor. However, if a polysilicon region is over doped silicon without crossing it, it forms a capacitor. (Transistors also have capacitance, but the gate capacitance is usually undesired.) ↩

我将在这里提供更多关于跳转到保存或恢复微码的电路的详细信息。BIU 向微码引擎发送两个信号，一个跳转到保存代码，一个跳转到恢复代码。这些信号由电容器缓冲和延迟，可能是为了调整信号的时序。在微码引擎中，有两个硬编码常量用于例程，就在跳转表上方；BIU 信号导致适当的常量进入微地址线。地址中的每一位都有一个到 +5V 的上拉晶体管或一个到地的下拉晶体管。这种方法有些低效，因为每位需要两个晶体管位。相比之下，跳转地址 ROM 和指令地址 ROM 使用每个位一个晶体管位。（与 PLA 中一样，每个晶体管根据需要存在或不存在，因此物理晶体管的数量少于晶体管位的数量。）https://static.righto.com/images/8087-decode/capacitors.jpg 8087 中的两个电容器。这张照片显示了金属层，下方有硅和多晶硅。由于电容器在 NMOS 电路中有些不寻常，我将在上面的照片中展示它们。如果多晶硅线穿过掺杂硅，它会创建一个晶体管。然而，如果多晶硅区域位于掺杂硅上方而不穿过它，它会形成一个电容器。（晶体管也存在电容，但栅极电容通常是不需要的。）[↩]

The documentation provides a hint that the microcode to load constants is complicated. Specifically, the documentation shows that different constants take different amounts of time to load. For example, log₂(e) takes 18 cycles, while log₂(10) takes 19 cycles, and log₁₀(2) takes 21 cycles. You would expect that pre-computed constants would all take the same amount of time, so the varying times suggest that more is happening behind the scenes. ↩

文档提供了一个提示，即加载常数的微码很复杂。具体来说，文档显示不同的常数需要不同的时间来加载。例如，log2(e) 需要 18 个周期，而 log2(10) 需要 19 个周期，log10(2) 需要 21 个周期。你会期望预计算的常数都需要相同的时间，因此变化的时间表明幕后发生了更多的事情。[↩]

---

## Critical Thinking Commentary / 批判性思考评论

### 一、作者主要论点分析

本文作者 Ken Shirriff 通过详细的芯片逆向工程分析，揭示了 Intel 8087 浮点协处理器指令解码机制的复杂性。作者的核心论点包括：

1. **技术折中的必然性**：8087 的复杂解码架构并非设计失误，而是在当时技术极限下的必然选择。芯片设计师不得不采用各种特殊案例和临时电路来减小芯片面积，降低制造成本。

2. **多层次解码策略**：作者详细阐述了 8087 采用的多种解码技术——从总线接口单元（BIU）的硬件解码，到 PLA（可编程逻辑阵列）的模式匹配，再到微码级别的条件分支——展示了早期处理器设计中"分层抽象"的思想雏形。

3. **历史延续性**：文章结尾指出，尽管 8087 制造困难（早期每片晶圆仅两个可用芯片），但它所确立的浮点标准已成为现代处理器的通用基础，体现了技术创新对行业标准的深远影响。

### 二、文章的优点

1. **实证研究方法的严谨性**：作者通过实际拆解芯片、显微镜摄影、晶体管级分析等逆向工程手段获取第一手资料，而非仅依赖文献研究。这种"边做边学"的方法使得技术分析具有高度的可信度。

2. **教学式叙述风格**：文章采用循序渐进的讲解方式，从基础概念（如 ModR/M 字节）逐步深入到复杂机制（如 PLA 和微码交互），并配合大量图示，使读者能够跟随作者的思路理解硬件工作原理。

3. **技术历史的语境化**：作者将技术细节置于历史背景中讨论——如 2K ROM 在当时是"大容量"、芯片良率问题等——帮助现代读者理解早期半导体工业面临的挑战。

### 三、文章的局限性

1. **受众门槛较高**：文章假设读者已具备数字逻辑、计算机体系结构的基础知识。对于非专业读者，诸如"积之和"、"NMOS 晶体管"、"微码引擎"等术语缺乏充分解释，可能形成阅读障碍。

2. **对设计决策的批判性不足**：虽然作者多次提到"临时电路"（ad hoc circuitry），但主要从实现效率角度肯定其价值，较少讨论这种复杂性可能带来的问题——如可维护性差、调试困难、设计错误风险增加等。

3. **缺乏比较视角**：文章专注于 8087 本身，未与其他同期浮点处理器（如 Motorola 68881、AMD 的协处理器方案）进行对比，读者难以评估 8087 设计方案的相对优劣。

### 四、个人批判视角

从现代计算机体系结构的角度看，8087 的设计体现了早期硬件设计中"硬件复杂度换软件简单性"的哲学。值得思考的几个问题：

**1. 复杂度的代价被低估了**

作者提到"如果实现一个特殊情况可以从芯片上减少几个晶体管...这个特殊情况就是值得的"，但这一判断主要基于硅片面积成本，未充分考量验证成本。现代芯片设计已证明，特殊案例的累积会导致验证空间爆炸，这是 Intel 后来在 Pentium FDIV 漏洞等问题中付出的代价。

**2. x87 架构的长期影响值得商榷**

虽然作者肯定 8087 确立了 IEEE 754 浮点标准的基础地位，但从架构演进角度看，x87 的寄存器堆栈设计被许多计算机科学家认为是"历史包袱"。SSE/AVX 等后续指令集转向平面寄存器文件，某种程度上是对 x87 复杂性的修正。文章对这部分技术债务的讨论不足。

**3. 微码 vs 硬连线的权衡**

文章展示了 8087 在微码和硬连线实现之间的混合策略。有趣的是，现代处理器设计出现了"去微码化"趋势（如 RISC-V 的简单指令集），通过将复杂度移至编译器来简化硬件。8087 的案例提醒我们：硬件/软件边界的划分是时代技术条件和社会经济因素共同作用的结果，而非绝对最优解。

### 五、技术启示

8087 的解码机制对当代技术实践仍有启发：

- **压缩与预处理的平衡**：PLA 预处理技术（如将 MOD 位映射为内存/寄存器信号）展示了如何通过适度的预处理来减小核心解码逻辑的规模，这一思想在现代 GPU 着色器编译器和神经网络加速器设计中仍有体现。

- **资源受限下的创新**：在资源受限环境下，设计师被迫探索非常规方案（如旋转 90° 的 PLA 布局、常数指数 ROM 的共享），这些约束驱动的创新往往比资源充裕时的"直来直去"更具创造性。

### 六、结语

Ken Shirriff 的这篇文章不仅是一篇技术考古学杰作，更是一面镜子，映照出计算机体系结构演进中的永恒主题：复杂度管理、硬件/软件边界划分、标准化与创新的张力。理解 8087 的"混乱"之美，有助于我们更深刻地理解现代处理器设计中那些看似理所当然的抽象和简化背后，凝聚着多少代工程师在技术与成本夹缝中的智慧权衡。
