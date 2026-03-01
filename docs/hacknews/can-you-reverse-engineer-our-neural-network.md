---
title: "Can you reverse engineer our neural network?"
url: "https://blog.janestreet.com/can-you-reverse-engineer-our-neural-network/"
rating: 9
category: "machine-learning"
date: "2026-02-28"
---

# Can you reverse engineer our neural network?

A lot of "capture-the-flag" style ML puzzles give you a black box neural net, and your job is to figure out what it does. When we were thinking of creating our [own ML puzzle](https://huggingface.co/spaces/jane-street/puzzle) early last year, we wanted to do something a little different. We thought it'd be neat to give users a complete specification of the neural net, weights and all. They would then be forced to use the tools of mechanistic interpretability to reverse engineer the network—which is a situation we sometimes find ourselves facing in our own research, when trying to interpret features of complex models.

We published the puzzle last February. At the time, we weren't even sure it was solvable. The neural network we'd designed would output 0 for almost all inputs. A reasonable solver might assume that the goal was to furnish an input that produced 1 or some other nonzero value. But we'd engineered the network in such a way, as you'll soon see, that you couldn't use traditional methods to brute force your way to an answer—say, by backpropagating a nonzero output all the way back to the input layer. You had to actually think about what the net was doing.

We were amazed by the response the puzzle got. Mostly by luck, it seemed like we'd calibrated the difficulty just so: it wasn't so hard that no one could solve it, and wasn't so easy that we were flooded with responses. In fact if you can solve this puzzle, there's a decent chance you'd fit in well here at Jane Street.

We'll restate the problem below, but be warned that the rest of this post contains huge spoilers. If you want to try solving the puzzle yourself, avert your eyes. The rest of this post will walk through the process that an actual solver took, with all the twists and turns before they finally cracked it.

## The problem

> Today I went on a hike and found a pile of tensors hidden underneath a neolithic burial mound! I sent it over to the local neural plumber, and they managed to cobble together this.
>
> [model.pt](http://model.pt)
>
> Anyway, I'm not sure what it does yet, but it must have been important to this past civilization. Maybe start by looking at the last two layers.
>
> Model Input
>
> `vegetable dog`
>
> Model Output
>
> `0`
>
> If you do figure it out, please let us know.

That `model.pt` file is basically just a pickled PyTorch model.

## A solution

### Getting started

A senior at university named Alex was in his dorm room when a roommate told him about a puzzle that was making the rounds on Twitter. The roommate had tried it himself but given up after two nights. Alex, in his final winter at school, was looking for something to do and decided to have a look.

He started by downloading the model and poking around, focusing on the last layer in particular:

```python
import torch
import plotly.express as px
model = torch.load('./model.pt')
linears = [x for x in model if isinstance(x, torch.nn.Linear)]
px.imshow(linears[-1].weight.detach())
```

Immediately it was plain that this was not an ordinary neural network. It clearly hadn't been trained: all the weights had integer values. Instead, it had been designed by hand, probably to carry out some very specific computation.

The last layer was a 48x1 matrix, but apparently broken into three sections. And indeed if you looked at the activations from the previous layer, they were always three repetitions of the same thing. The second-to-last layer appeared to be three repetitions of the same weights, while its bias contained the same 16 bytes, but incremented by 1 each time, as if encoding a vector v, then v + 1, and v + 2.

Thinking about it some—and about the fact that the last layer emitted a single bit—Alex realized that this second-to-last ReLU layer must be computing whether two 16-byte integers were equal to one another (with one byte per neuron). The way it seemed to work is that it made three copies of the input vector v, a 16-byte number. It tried to check that against a reference number x (which was determined by the bias of the second-to-last layer). So the three copies would actually represent v - x - 1, v - x, and v - x + 1. The last layer applied weights 1, -2, and 1 to these cases respectively. We can do some casework on an individual value here: consider the value of ReLU(v-x-1) - 2ReLU(v-x) + ReLU(v-x+1). If v=x, then this is equal to 1. We won't show the rest of the cases here, but they all result in 0. The bias on the last layer was -15, so the final neuron would only fire when v=x for all 16 bytes.

So now the question became, how do we get the activations of the second last layer to equal x?

### Reverse-engineering the program at the heart of the network

Alex figured that if there's some number that the network is checking against at the very end, then the rest of the network must be some sort of big equation. There indeed appears to be a lot of structure in the network, as you can see just from plotting the size of the 2500 linear layers (about half the full network).

So Alex began looking at various sub-networks, tracing their dependencies. This involved staring at a lot of graph structures. But after hours of searching for legible sub-circuits, he came up short. For the moment there just seemed to be too much complexity to trace by hand. So he had a new idea: what if I treat this thing as a linear program and just solve it?

This is, of course, not possible with so many ReLU layers—ReLUs aren't linear—but they can be modelled by adding an additional *integer* value, corresponding to the statement "this activation is negative." You can thereby treat it as an integer linear program and use a constraint solver capable of integer programming. So that's what Alex did: he dutifully wrote some code to convert the layers of the neural network into a giant linear program and let it run.

And let it run.

That seemed to be going nowhere—so Alex now attempted to reduce the number of variables in the program. Perhaps there were some reductions you could do? Alex found that if you looked at a bunch of layers, they mostly looked like identity matrices. In fact in 1500 or so layers, 80% of the nodes were just performing an identity operation.

Alex treated each neuron in the network as a node in a DAG, where each node goes into the nodes in the next layer with some weights; but if you ever have a node with in-degree 1 and whose weight is exactly 1, you can combine those two nodes. (You know this is safe to do because the network has integer values everywhere: all the inputs are integers, as are all the weights.)

There were slightly fancier reductions. For instance, if you have a node whose every incoming edge has positive weight, then the fact that you're doing ReLU doesn't matter, because it's never going to hit the negative clamp—and so you can forward its in-edges to its children, directly passing them to the next layer. Also, if two neurons in a layer have exactly the same input vector, you can combine them, and redirect their descendents to the new merged neuron. And you can repeat this process many times.

Alex by now had poured hours into this analysis. He'd found circuits that appeared to be repeated across many layers. He'd print out different equivalence classes of nodes, looking at the sequence of weights that each node had as input, discovering that there were only a few *kinds* of nodes. For instance there was one class of nodes which effectively would forward a value from two layers back. Collapsing these, among other similar reductions, brought down the size of the linear program from something like 2 million nodes, to 75,000.

But after all that, Alex ran the solver again and again it churned without terminating.

### The final reductions

A new idea: what if you propagated bounds through the network? Just by reasoning through one layer at a time, you could figure out the maximum value that any given node could achieve; you'd do this simply by looking at the bounds on its inputs. It turns out that with fairly conservative assumptions, many nodes end up with very tight bounds, e.g. from 0-1.

Maybe this was enough to make the program tractable?

At this point Alex switched from a linear program to a SAT solver, since the total number of values had gotten so much smaller. In the SAT version, you had a boolean variable for each node equalling each value in its range. All told this resulted in 200,000 variables after all the reductions. After a day of running, the SAT solver reduced the program to 20,000 variables. From there it didn't seem to reduce further.

In effect Alex had discovered that inside this neural network there was a core program, irreducibly complex, that—much to his disappointment—was still too large to brute force. So after many days, he had to take a step back, effectively having gotten nowhere.

### Glancing off the solution

He thought meta: this has to be a solvable puzzle, right? How would someone build a puzzle like this that would be *interesting* to solve? If you generated random weights, a SAT solver would probably be able to solve it by brute force. This network was created by a human. At its core there seemed to be a function that you couldn't just use search or optimization to recover. It was an *irreversible* function. What were some go-to examples of irreversible functions?

Alex asked ChatGPT for some common hash functions, and compared them against some basic plots of the layer widths, which looked periodic. In fact there were 32 periods of length 48, repeating exactly each time. Maybe the network was doing 32 blocks of the same computation? To ChatGPT again: are there any common hash functions that use 32 blocks of computation? Bingo. It turned out that roughly all of them do.

To determine which one was in play here, he explored by hand: he'd input some string into the network, compute various hash flavors with separate programs, then look at the second-to-last layer. It turned out that md5 lined up and the other common hash functions didn't.

This was nice, because he already knew what the hash was supposed to be by looking at the second-to-last layer's biases. So the problem reduced to finding an input string that produced that particular md5 hash. But it was not obvious how to solve that—especially since he didn't have a real proof that this network *always* produces an md5 hash. Maybe the solution was to dig deeper, and hack the network to make it reversible?

### A glitch in the matrix

Alex noticed something odd in the network. It seemed to have a bug: if your input was greater than length 32, it no longer produced the correct md5 hash. Perhaps somewhere in that bug was a key to reversing the hash value that was built into the network?

He spent the next two days reverse-engineering the bug. To start, he got Gemini to write an implementation of the md5 hashing function. Then he matched up every neuron in the network to the corresponding variable in the md5 algorithm. He wrote some code that would store the sequence of values for a given intermediate variable, then search each of the 32 blocks in the network for that value; this would pick out which ranges of neurons corresponded to the bits for each variable. It turned out that some ranges of bits exactly corresponded to the variables, and others were intermediate computation values.

Then, with inputs that were >32, he could painstakingly trace through the blocks to find the exact spot where the network diverged from the correct algorithm.

The crux of it was in the first 7 layers—there was a circuit that would compute the length of the input, and attempt to store it in 4 bytes, in little-endian order. But when the length was 256 bits or greater, you'd have a length variable that contained the *value* 256, instead of the correct encoding. That is, if the length were >384 bits, the length bytes should be 128 1 0 0, but what the network encoded instead was 384 0 0 0.

Then the question was, is it possible to exploit this bug, by crafting a message of length 256 or greater? Some more painstaking tracing revealed a few observations: First, there aren't that many possible lengths. There were only 55 inputs, so he could do an exhaustive search to see how the network behaved with respect to these weird values. Second, the broken length value was converted to binary, and then propagated through every layer in the entire network. In binary, all of the bits would equal 1, and the rest of the number was concentrated in the lowest-order bit, so 384 would be encoded as 130,1,1,1,1,1,1,1. Third, the invalid bytes from the length of the message were only used in a few blocks of the md5 computation, which always reads bytes from the input in the same order.

Using these observations, it's possible to write down a modified version of the md5 algorithm, which corrects itself at the necessary blocks to be in line with the neural network. Looking closely at this, however, it still seems very difficult to reverse in general.

This took about two days to figure out, but—disappointment again—didn't lead Alex any closer to the solution. He wrote to the email address provided on the puzzle with what he'd discovered so far. What he heard back surprised him. The bug was not intentional. With that in mind, why don't you try to solve it one last time?

### The return of brute force

It turned out that once you knew the hash encoded in the bias of the second-to-last layer, you *were* done. Figuring that out was the meat of the puzzle. The puzzle creator had intentionally made the hash easy to brute force, leaving various small hints in the puzzle description and Python code that the solution was composed of two English words, lowercased, concatenated by a space.

Alex had actually tried to brute force the hash earlier, but had downloaded a list of the top 10,000 most popular words to do it, which turned out not to be big enough to find it. Once he had a big enough word list, he got the answer.

## Another puzzle

One of the things that made this puzzle challenging was designing a network of the right complexity. Using logic gates means the network won't be differentiable; but if you make the program encoded by those gates too complex, there'd be little hope of reverse engineering it. Md5 felt like a good compromise, though it was by no means trivial. Because md5 uses modular addition, creating the puzzle required implementing a parallel carry adder in 20ish layers of a neural network. Not easy! We were impressed that some solvers managed to figure that out—and Alex's discovery of the >32 bug was unexpected and quite extraordinary.

The experience of creating and releasing the puzzle, and engaging with the folks who solved it, went well enough that we've done it again. [Here you'll find the latest](https://huggingface.co/spaces/jane-street/droppedaneuralnet). In this new puzzle, a neural network whose layers have been jumbled up needs to be put back in the right order… Can you help?

*If this kind of thing is interesting to you, consider [applying](https://www.janestreet.com/join-jane-street/overview/). You'll join a close-knit group of brilliant, supportive colleagues, harnessing tens of thousands of GPUs, petabytes of training data, and the agility and resources to invest in the best ideas.*

---

# 中文翻译

许多"夺旗赛"（capture-the-flag）风格的机器学习谜题会给出一个黑盒神经网络，你的任务是弄清楚它在做什么。去年年初，当我们考虑创建[自己的机器学习谜题](https://huggingface.co/spaces/jane-street/puzzle)时，我们想做一些不同的东西。我们认为向用户提供神经网络的完整规范（包括所有权重）会很有趣。这样用户将被迫使用机械可解释性（mechanistic interpretability）工具来逆向工程这个网络——这是我们在自己的研究中有时会面临的情况，当试图解释复杂模型的特征时。

我们在去年二月发布了这个谜题。当时，我们甚至不确定它是否可解。我们设计的神经网络对几乎所有输入都输出0。一个合理的解谜者可能会假设目标是提供一个能产生1或其他非零值的输入。但我们以某种方式设计了这个网络，正如你很快会看到的，你无法使用传统方法暴力破解答案——比如通过反向传播将非零输出一直传回输入层。你必须真正思考这个网络在做什么。

我们对这个谜题的反响感到惊讶。大部分是靠运气，看起来我们把难度校准得恰到好处：它不太难以至于没有人能解出来，也不太简单以至于我们被大量回复淹没。事实上，如果你能解开这个谜题，你有很大的可能很适合在Jane Street工作。

我们将在下面重新陈述问题，但请注意，本文的其余部分包含大量剧透。如果你想自己尝试解这个谜题，请移开视线。本文的其余部分将介绍一个实际解谜者的过程，以及他最终破解之前的所有曲折和转折。

## 问题描述

> 今天我去徒步旅行，在一座新石器时代 burial mound 下面发现了一堆张量！我把它发给了当地的神经网络水管工，他们设法拼凑出了这个东西。
>
> [model.pt](http://model.pt)
>
> 不管怎样，我还不确定它是做什么的，但它对这个过去的文明来说一定很重要。也许可以从最后两层开始看起。
>
> 模型输入
>
> `vegetable dog`
>
> 模型输出
>
> `0`
>
> 如果你真的弄清楚了，请告诉我们。

那个 `model.pt` 文件基本上就是一个 pickled 的 PyTorch 模型。

## 一种解法

### 入门

一个名叫Alex的大学四年级学生正在宿舍里，室友告诉他一个谜题在Twitter上流传。室友自己试过，但两晚后就放弃了。Alex在学校的最后一个冬天，想找点事做，决定看看。

他开始下载模型并进行探索，特别关注最后一层：

```python
import torch
import plotly.express as px
model = torch.load('./model.pt')
linears = [x for x in model if isinstance(x, torch.nn.Linear)]
px.imshow(linears[-1].weight.detach())
```

立刻就很明显，这不是一个普通的神经网络。它显然没有被训练过：所有权重都是整数值。相反，它是手工设计的，可能是为了执行某种非常特定的计算。

最后一层是一个48×1的矩阵，但显然被分成了三个部分。事实上，如果你查看前一层的激活值，它们总是相同内容的三个重复。倒数第二层看起来是相同权重的三个重复，而其偏置包含相同的16个字节，但每次递增1，就像编码一个向量v，然后是v+1，以及v+2。

进一步思考——以及考虑到最后一层输出单个比特的事实——Alex意识到这个倒数第二层的ReLU层必须是在计算两个16字节整数是否相等（每个神经元一个字节）。它似乎的工作方式是：它制作输入向量v（一个16字节数字）的三个副本，然后尝试将其与参考数字x（由倒数第二层的偏置决定）进行比较。所以这三个副本实际上代表v-x-1、v-x和v-x+1。最后一层分别对这些情况应用权重1、-2和1。我们可以对单个值做一些情况分析：考虑ReLU(v-x-1) - 2ReLU(v-x) + ReLU(v-x+1)的值。如果v=x，那么这等于1。我们不会在这里展示其余的情况，但它们都产生0。最后一层的偏置是-15，所以只有当所有16个字节都满足v=x时，最终神经元才会触发。

所以现在问题变成了：我们如何让倒数第二层的激活值等于x？

### 逆向工程网络核心的程序

Alex推断，如果在最后网络正在检查某个数字，那么网络的其余部分必须是某种大型方程式。网络中确实存在很多结构，仅从绘制2500个线性层（约占整个网络的一半）的大小就可以看出。

于是Alex开始查看各种子网络，追踪它们的依赖关系。这涉及盯着很多图结构看。但在花了数小时寻找可读的子电路后，他没有取得进展。目前看来，复杂性太高，无法手工追踪。于是他有了一个新想法：如果我把它当作线性规划来求解呢？

当然，有这么多ReLU层是不可能这样做的——ReLU不是线性的——但可以通过添加一个额外的*整数*值来建模，对应于"这个激活是负的"这一陈述。因此你可以将其视为整数线性规划，并使用能够进行整数规划的约束求解器。所以Alex就是这么做的：他认真地编写了一些代码，将神经网络的各层转换成一个巨大的线性规划，然后让它运行。

让它一直运行。

这似乎没有进展——于是Alex尝试减少程序中的变量数量。也许可以做些简化？Alex发现，如果你查看一堆层，它们大多看起来像单位矩阵。事实上，在大约1500层中，80%的节点只是执行单位操作。

Alex将网络中的每个神经元视为DAG中的一个节点，其中每个节点以某些权重进入下一层的节点；但如果你有一个入度为1且权重恰好为1的节点，你可以将这两个节点合并。（你知道这样做是安全的，因为网络到处都有整数值：所有输入都是整数，所有权重也是整数。）

还有一些稍微复杂一点的简化。例如，如果你有一个每个入边权重都为正的节点，那么你做ReLU这一事实就不重要了，因为它永远不会碰到负的钳位——所以你可以将其入边转发给它的子节点，直接传递给下一层。此外，如果一层中的两个神经元具有完全相同的输入向量，你可以将它们合并，并将它们的后代重定向到新的合并神经元。你可以重复这个过程很多次。

到目前为止，Alex已经在这项分析上投入了数小时。他发现了在许多层中重复出现的电路。他打印出不同类别的节点，查看每个节点作为输入的权重序列，发现只有几种*类型*的节点。例如，有一类节点实际上会从两层之前转发一个值。将这些以及其他类似的简化折叠后，线性规划的规模从大约200万个节点减少到75,000个。

但做完所有这些后，Alex再次运行求解器，它仍然不停地运行而无法终止。

### 最后的简化

一个新想法：如果你通过网络传播边界呢？只需逐层推理，你就可以计算出任何给定节点可以达到的最大值；你只需查看其输入的边界即可。事实证明，在相当保守的假设下，许多节点最终具有非常紧的边界，例如从0到1。

也许这足以使规划变得可处理？

在这一点上，Alex从线性规划切换到SAT求解器，因为值的总数已经变得小得多。在SAT版本中，每个节点在其范围内的每个值都有一个布尔变量。总的来说，在所有简化之后，这产生了20万个变量。运行一天后，SAT求解器将程序减少到2万个变量。从那里开始，它似乎不再进一步减少。

实际上，Alex发现这个神经网络内部有一个核心程序，是不可约地复杂的——令他失望的是——它仍然太大而无法暴力破解。所以很多天后，他不得不退一步，实际上没有任何进展。

### 与解法擦肩而过

他进行了元思考：这必须是一个可解的谜题，对吧？有人会如何构建一个*有趣*的谜题来解？如果你生成随机权重，SAT求解器可能能够通过暴力破解来解决它。这个网络是由人类创建的。在其核心似乎有一个你无法仅仅通过搜索或优化来恢复的函数。它是一个*不可逆*的函数。有哪些常用的不可逆函数的例子？

Alex向ChatGPT询问了一些常见的哈希函数，并将它们与层宽的基本图进行比较，这些图看起来是周期性的。事实上，有32个长度为48的周期，每次都完全重复。也许网络正在执行32个相同计算的块？再次问ChatGPT：有什么常见的哈希函数使用32个计算块吗？中了。结果发现几乎所有哈希函数都是这样。

为了确定这里使用的是哪一个，他手工探索：他将一些字符串输入网络，用单独的程序计算各种哈希变体，然后查看倒数第二层。结果发现md5匹配上了，而其他常见哈希函数不匹配。

这很好，因为他已经通过查看倒数第二层的偏置知道了哈希应该是什么。所以问题简化为找到一个产生该特定md5哈希的输入字符串。但这如何解决并不明显——尤其是他没有真正的证据证明这个网络*总是*产生md5哈希。也许解决方案是更深入挖掘，并破解网络使其可逆？

### 矩阵中的故障

Alex注意到网络中有一些奇怪的东西。它似乎有一个bug：如果你的输入长度大于32，它就不再产生正确的md5哈希。也许在这个bug的某个地方，藏着逆转网络中内置哈希值的关键？

他花了接下来两天时间逆向工程这个bug。首先，他让Gemini写了一个md5哈希函数的实现。然后他将网络中的每个神经元与md5算法中相应的变量匹配起来。他写了一些代码，存储给定中间变量的值序列，然后在网络的32个块中搜索该值；这将挑选出哪些范围的神经元对应于每个变量的比特。结果发现，某些比特范围完全对应于变量，其他的是中间计算值。

然后，对于长度>32的输入，他可以 painstakingly 追踪这些块，找到网络偏离正确算法的准确位置。

关键在于前7层——有一个电路会计算输入的长度，并尝试以4字节的小端序存储它。但当长度为256位或更大时，你的长度变量将包含*值*256，而不是正确的编码。也就是说，如果长度>384位，长度字节应该是128 1 0 0，但网络编码的却是384 0 0 0。

然后问题是，是否可以通过构造长度为256或更大的消息来利用这个bug？一些更 painstaking 的追踪揭示了一些观察结果：首先，可能的长度并不多。只有55个输入，所以他可以进行穷举搜索，看看网络相对于这些奇怪值的表现如何。其次，损坏的长度值被转换为二进制，然后传播到整个网络的每一层。在二进制中，所有比特都等于1，其余数字集中在最低位，所以384将被编码为130,1,1,1,1,1,1,1。第三，消息长度的无效字节只在md5计算的几个块中使用，这些块总是以相同的顺序从输入中读取字节。

使用这些观察结果，可以写出一个修改版的md5算法，在必要的块中自我修正以与神经网络保持一致。然而，仔细观察，这看起来在一般情况下仍然很难逆转。

这花了大约两天时间才弄清楚，但——再次失望——并没有让Alex更接近解决方案。他写信给谜题提供的电子邮件地址，讲述了他到目前为止的发现。他收到的回复让他惊讶。这个bug不是故意的。考虑到这一点，为什么不最后一次尝试解决它呢？

### 暴力破解的回归

事实证明，一旦你知道了编码在倒数第二层偏置中的哈希，你就*完成*了。弄清楚那是谜题的核心。谜题创建者有意使哈希易于暴力破解，在谜题描述和Python代码中留下了各种小提示，表明解决方案由两个英文单词组成，小写，用空格连接。

Alex实际上早些时候尝试过暴力破解哈希，但他下载了最流行的10,000个单词列表来这样做，结果发现这不够大，找不到答案。一旦他有了足够大的单词列表，他就得到了答案。

## 另一个谜题

使这个谜题具有挑战性的原因之一是设计一个复杂度合适的网络。使用逻辑门意味着网络将不可微；但如果你让这些门编码的程序太复杂，就几乎没有逆向工程的希望了。Md5感觉是一个很好的折衷，尽管它绝非微不足道。因为md5使用模加，创建这个谜题需要在神经网络的约20层中实现一个并行进位加法器。不容易！我们对一些解谜者设法弄清楚这一点印象深刻——Alex发现>32的bug是出乎意料的，而且相当非凡。

创建和发布谜题以及与解谜者互动的体验进行得足够顺利，所以我们又做了一个。[在这里你可以找到最新的](https://huggingface.co/spaces/jane-street/droppedaneuralnet)。在这个新谜题中，一个层被打乱的神经网络需要被放回正确的顺序……你能帮忙吗？

*如果你对这类事情感兴趣，考虑[申请](https://www.janestreet.com/join-jane-street/overview/)。你将加入一个紧密联系的、才华横溢、互相支持的同事团队，利用数以万计的GPU、PB级的训练数据，以及投资最佳想法的灵活性和资源。*
