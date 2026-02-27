# The First Fully General Computer Action Model
# 首个通用计算机动作模型

**Source**: https://si.inc/posts/fdm1/  
**Publisher**: Standard Intelligence Team  
**Category**: AI/ML  
**Rating**: 9/10

---

## Summary | 摘要

Standard Intelligence 推出了 FDM-1，这是首个能够在通用计算机上执行复杂多步骤任务的 AI 模型。该模型基于 1100 万小时的屏幕录制视频进行训练，可以在 30 FPS 的速度下浏览复杂网站、完成 CAD 建模序列，甚至驾驶真实汽车。与现有的视觉-语言模型 (VLM) 不同，FDM-1 直接在视频上训练而非静态截图，能够处理长达近两小时的视频上下文，实现真正的长程任务规划和执行。

---

## Introduction | 引言

**We designed FDM-1, a foundation model for computer use.** FDM-1 is trained on videos from a portion of our 11-million-hour screen recording dataset, which we labeled using an inverse dynamics model that we trained. Our video encoder can compress almost 2 hours of 30 FPS video in only 1M tokens. FDM-1 is the first model with the long-context training needed to become a coworker for CAD, finance, engineering, and eventually ML research, and it consistently improves with scale. It trains and infers directly on video instead of screenshots and can learn unsupervised from the entirety of the internet.

**我们设计了 FDM-1，一个面向计算机使用的基础模型。** FDM-1 基于我们 1100 万小时屏幕录制视频数据集的一部分进行训练，这些数据使用我们训练的逆动力学模型进行了标注。我们的视频编码器仅需 100 万个 token 即可压缩近 2 小时的 30 FPS 视频。FDM-1 是首个具备长上下文训练能力的模型，可以成为 CAD、金融、工程乃至机器学习研究领域的协作助手，并且其性能随规模扩展持续提升。它直接在视频上训练和推理，而非静态截图，并能从整个互联网进行无监督学习。

---

Before today, the recipe for building a computer use agent was to finetune a [vision-language model (VLM)](https://en.wikipedia.org/wiki/Vision-language_model) on contractor-annotated screenshots of computer use, then build reinforcement learning environments to learn each specific downstream task. Agents trained this way are unable to act on more than a few seconds of context, process high-framerate video, do long-horizon tasks, or scale to competent agents.

在此之前，构建计算机使用智能体的标准方法是：在承包商标注的计算机使用截图上微调[视觉-语言模型 (VLM)](https://en.wikipedia.org/wiki/Vision-language_model)，然后构建强化学习环境来学习每个特定的下游任务。以这种方式训练的智能体无法处理超过几秒钟的上下文、无法处理高帧率视频、无法完成长程任务，也难以扩展到真正胜任的智能体。

Moreover, training these VLMs requires contractor-labeled annotations. These are expensive, so current computer action datasets are tiny: [the largest open dataset](https://arxiv.org/abs/2509.15221) is less than 20 hours of 30 FPS video. Meanwhile, millions of hours of film editing, coding livestreams, video game playthroughs, and more have accumulated on the internet over the past two decades. Building a general computer agent requires an internet-scale video corpus, just as building GPT-3 required an internet-scale text corpus. FDM-1 is the first model that can train at this scale.

此外，训练这些 VLM 需要承包商标注的数据，成本极高，因此现有的计算机动作数据集非常小：[最大的公开数据集](https://arxiv.org/abs/2509.15221)仅有不到 20 小时的 30 FPS 视频。与此同时，过去二十年互联网积累了数百万小时的影片编辑、编程直播、游戏通关视频等内容。构建通用计算机智能体需要互联网规模的视频语料库，就像构建 GPT-3 需要互联网规模的文本语料库一样。FDM-1 是首个能够在此规模上训练的模型。

---

## Training Recipe | 训练方案

Our training recipe consists of three stages (see Figure 4). First, we train an IDM on 40,000 hours of contractor-labeled screen recordings. Second, we use the IDM to label our 11-million-hour video corpus. Finally, we use the IDM-labeled videos to autoregressively train a "forward dynamics model" (FDM) on next action prediction. The FDM's output token space consists of key presses and mouse movement deltas, expressive enough to model any action taken on a computer.

我们的训练方案包含三个阶段（见图 4）。首先，我们在 40,000 小时的承包商标注屏幕录制数据上训练 IDM（逆动力学模型）。其次，我们使用 IDM 为 1100 万小时的视频语料库进行标注。最后，我们使用 IDM 标注的视频来自回归地训练一个"前向动力学模型"（FDM），用于预测下一个动作。FDM 的输出 token 空间由按键和鼠标移动增量组成，足以建模在计算机上执行的任何操作。

### Video Encoder | 视频编码器

Videos of the real world and bodies of text both have relatively uniform information densities throughout, and both can be compressed into a latent representation without losing much semantic content. Screen recordings are different because information density can vary rapidly. There is a massive information difference between moving a cursor across a blank screen and scrolling through pages of dense text. Existing approaches with fixed-size embedding spaces inevitably trade off between semantic detail and compression ratio.

真实世界的视频和文本块都具有相对均匀的信息密度，两者都可以压缩为潜在表示而不会丢失太多语义内容。屏幕录制则不同，因为信息密度可能快速变化。在空白屏幕上移动光标与滚动浏览密集文本页面之间存在巨大的信息差异。现有使用固定大小嵌入空间的方法不可避免地需要在语义细节和压缩比之间做出权衡。

We created a model without this tradeoff by training our video encoder on a masked compression objective. This unsupervised training enables our encoder to produce information-dense features at a high compression rate. Because our training is unsupervised, we use tasks like inverse dynamics, action prediction, frame reconstruction, and random text transcription to measure the abilities of our encoder.

我们通过在掩码压缩目标上训练视频编码器，创建了一个无需这种权衡的模型。这种无监督训练使我们的编码器能够以高压缩率生成信息密集的特征。由于训练是无监督的，我们使用逆动力学、动作预测、帧重建和随机文本转录等任务来衡量编码器的能力。

Comparing our video encoder to a [ViT](https://en.wikipedia.org/wiki/Vision_transformer), we observe ~100x faster convergence during training.

与 [ViT（视觉 Transformer）](https://en.wikipedia.org/wiki/Vision_transformer) 相比，我们的视频编码器在训练期间收敛速度提高了约 100 倍。

Our encoder achieves a state-of-the-art compression ratio of video frames to tokens, as shown in Figure 7. Our video context unlocks long-horizon workflows such as CAD, while still maintaining the ability to read text with high fidelity.

我们的编码器实现了视频帧到 token 的最先进压缩比（见图 7）。我们的视频上下文解锁了 CAD 等长程工作流，同时仍保持高精度读取文本的能力。

| Context Window | Average Video Duration |
|----------------|------------------------|
| 32k tokens     | 3 minutes 30 seconds   |
| 200k tokens    | 20 minutes             |
| 1M tokens      | 1 hour 40 minutes      |

| 上下文窗口 | 平均视频时长 |
|------------|--------------|
| 32k token  | 3 分 30 秒   |
| 200k token | 20 分钟      |
| 100 万 token | 1 小时 40 分 |

### Inverse Dynamics | 逆动力学

In order to train on orders of magnitude more labeled data than contractors can provide, we need to automatically label our internet-scale dataset with predicted computer actions—mouse movements, key presses, etcetera. We created an IDM to predict high-quality labels, letting us achieve similar efficiency when training on任意 videos as when training on human-gathered ground-truth data.

为了在比承包商能提供的数据多几个数量级的标注数据上进行训练，我们需要用预测的计算机操作（鼠标移动、按键等）自动为互联网规模的数据集打标。我们创建了 IDM 来预测高质量的标签，使我们在任意视频上的训练效率与使用人工收集的真实数据训练时相当。

Labeling video is fundamentally non-causal—you can't label a Cmd+C until you see the resulting pasted sequence. To train a non-causal, generative model, we adopted a masked diffusion architecture.

视频标注本质上是非因果的——在看到粘贴结果序列之前，你无法标注 Cmd+C 操作。为了训练非因果的生成模型，我们采用了掩码扩散架构。

Our [masked diffusion](https://s-sahoo.com/mdlm) method predicts actions conditioned on all frames simultaneously with masked action tokens. During inference, we feed frames interleaved with mask tokens and have the model predict log probabilities for each masked position. We then select the top-k highest-confidence predictions, unmask those tokens, and repeat until the full sequence is labeled.

我们的[掩码扩散](https://s-sahoo.com/mdlm)方法同时基于所有帧预测动作，使用掩码动作 token。在推理过程中，我们输入与掩码 token 交错的帧，让模型预测每个掩码位置的对数概率。然后选择置信度最高的 top-k 预测，对这些 token 解除掩码，重复此过程直到整个序列都被标注。

### Forward Dynamics | 前向动力学

The FDM predicts the next action given the prior frames and actions. Unlike VLM-based approaches, our FDM operates directly on video and action tokens—no chain-of-thought reasoning, byte-pair encoding, or tool use. This keeps inference low-latency and allows modeling a multitude of tasks that current designs cannot capture—e.g. scrolling, 3D modelling, gameplay. We trained FDM-1 with no language model transfer.

FDM 基于先前的帧和动作预测下一个动作。与基于 VLM 的方法不同，我们的 FDM 直接在视频和动作 token 上运行——无需思维链推理、字节对编码或工具使用。这保持了低延迟推理，并允许建模当前设计无法捕获的多种任务——例如滚动、3D 建模、游戏。我们在没有语言模型迁移的情况下训练了 FDM-1。

To comprehensively model computer action, we need to tokenize key presses, mouse movements, and scroll events into discrete bins. Key presses and scrolls are easy: we tokenize each key press, key release, and scroll event individually.

为了全面建模计算机操作，我们需要将按键、鼠标移动和滚动事件分词为离散区间。按键和滚动很容易：我们分别对每个按键、释放键和滚动事件进行分词。

Mouse movements are harder to tokenize because the mouse can move any number of pixels per frame—this state space is too large and inefficient to effectively train on. To reduce the state space and use tokens more uniformly, we exponentially bin the mouse movements. The mouse delta per frame is split into X and Y components. Then, each component is normalized relative to the screen's width and height before being placed into one of 49 exponentially-sized bins.

鼠标移动更难分词，因为鼠标每帧可以移动任意数量的像素——这种状态空间太大且低效，难以有效训练。为了减少状态空间并更均匀地使用 token，我们对鼠标移动进行指数级分箱。每帧的鼠标增量被分为 X 和 Y 分量，然后每个分量相对于屏幕的宽度和高度进行归一化，最后放入 49 个指数大小的区间之一。

This way, small, frequent movements are tokenized into finer bins and large, infrequent movements into coarser ones. We also train our FDM to predict the next click position alongside every mouse movement token, which helps produce accurate trajectories.

这样，小而频繁的动作被分词到更细的区间，大而罕见的动作则分到更粗的区间。我们还训练 FDM 在每个鼠标移动 token 旁边预测下一个点击位置，这有助于生成准确的轨迹。

---

## Eval Infrastructure | 评估基础设施

Evaluating an action model requires testing it many times in many live environments. We built eval infrastructure that drives over 1M rollouts per hour across 80,000 forking virtual machines. Each VM is a minimal Ubuntu desktop environment with 1 vCPU and 8GB of RAM; a single H100 can control 42 of these in parallel.

评估动作模型需要在多个实时环境中多次测试。我们构建了评估基础设施，每小时可在 80,000 个分叉虚拟机上执行超过 100 万次 rollout。每个 VM 是一个精简的 Ubuntu 桌面环境，配备 1 个 vCPU 和 8GB 内存；单个 H100 可以并行控制其中 42 个。

Forking lets us capture a full memory snapshot of an OS state and replicate it onto a fresh VM without corrupting the base environment. This allows us to reuse a single evaluation starting state across thousands of rollouts, effectively leveraging test-time-compute.

分叉让我们能够捕获操作系统状态的完整内存快照，并将其复制到全新的 VM 上而不会破坏基础环境。这使我们能够在数千次 rollout 中重复使用单一的评估起始状态，有效利用测试时计算。

Our VM infrastructure is also optimized for low latency. This is important so the model is in distribution during inference because it wasn't exposed to latency during training—the model has never seen lag before. We mitigate latency through a variety of methods: colocating the GPUs and VMs in the same cloud region, using cumulative sequence length packing, tuning a low-latency VNC configuration, and writing custom Rust bindings for device input. The combination of these optimizations lets us achieve a round trip screen capture to action latency of 11ms.

我们的 VM 基础设施还针对低延迟进行了优化。这很重要，因为在推理期间模型需要保持与训练时一致的分布——模型在训练中从未接触过延迟，它从未见过"卡顿"。我们通过多种方法缓解延迟：将 GPU 和 VM 部署在同一云区域、使用累积序列长度打包、调优低延迟 VNC 配置，以及为设备输入编写自定义 Rust 绑定。这些优化组合使我们实现了从屏幕捕获到动作的往返延迟仅为 11 毫秒。

---

## Results | 实验结果

The IDM-labeled data outperforms our contractor dataset in general mouse movement and action capabilities (as seen in *Target Accuracy*, *Symbolic Memory*, and *UI Manipulation* above). For typing and verbal understanding, the model improves on the IDM-labeled data, but more slowly than on contractor datasets. We believe this is caused by noise introduced by the IDM. In the future, we will consider using a mix of IDM and contractor data when scaling up the model.

IDM 标注的数据在一般鼠标移动和动作能力方面优于我们的承包商数据集（见上文的"目标准确性"、"符号记忆"和"UI 操作"）。对于打字和语言理解，模型在 IDM 标注数据上有所改进，但比使用承包商数据集时更慢。我们认为这是由 IDM 引入的噪声造成的。未来，在扩大模型规模时，我们将考虑混合使用 IDM 和承包商数据。

Our model successfully and scalably infers human behavior on complex tasks like object segmentation and 3D manipulation. We also demonstrate that training on computer use generalizes to the real world significantly more easily than a model without such training. In our self-driving tests, the model is able to use a web interface to navigate turns around a block in San Francisco after finetuning on less than 1 hour of collected data. FDM-1 starts with 50% accuracy on key press prediction (a choice between no action, move left, or move right), significantly higher than the baseline model with only our video encoder (and no internet video pretraining). Our model also achieves steeper scaling trends compared to the baseline. We expect to achieve zero shot performance on such tasks in the future.

我们的模型成功且可扩展地推断出人类在对象分割和 3D 操作等复杂任务上的行为。我们还证明，在计算机使用上训练的模型比没有这种训练的模型更容易泛化到现实世界。在我们的自动驾驶测试中，模型在仅使用不到 1 小时收集的数据进行微调后，就能够使用 Web 界面在旧金山街区周围导航转弯。FDM-1 在按键预测上的初始准确率为 50%（在"无动作"、"左移"或"右移"之间选择），显著高于仅使用视频编码器（无互联网视频预训练）的基线模型。与基线相比，我们的模型还表现出更陡峭的扩展趋势。我们预计未来将在这类任务上实现零样本性能。

---

## Now What? | 未来展望

Computer action used to be fundamentally data-constrained, expensive, and unscalable. We unlocked both **multi-hour 30 FPS video contexts** and the ability to **train on 11 million hours of data**. This brings computer action from a data-constrained regime to a compute-constrained one.

计算机动作过去从根本上受到数据限制、成本高昂且无法扩展。我们同时解锁了**多小时 30 FPS 视频上下文**和**在 1100 万小时数据上训练**的能力。这将计算机动作从数据受限状态转变为计算受限状态。

We believe artificial general intelligence will be created within our lifetimes, and likely within the next decade. Our recent work closes the gap on self-directing, competent computer use agents, but there are still a lot of technical problems to be solved before aligned general learners can exist. Standard Intelligence exists to solve these problems.

我们相信通用人工智能（AGI）将在我们有生之年被创造出来，很可能在未来十年内。我们最近的工作缩小了自主、胜任的计算机使用智能体之间的差距，但在对齐的通用学习器能够存在之前，仍有许多技术问题需要解决。Standard Intelligence 的存在就是为了解决这些问题。

---

## Research Team | 研究团队

- Neel Redkar
- Yudhister Kumar
- Devansh Pandey
- Galen Mead

---

## Technical Terms | 技术术语对照

| English | 中文 |
|---------|------|
| Foundation Model | 基础模型 |
| Vision-Language Model (VLM) | 视觉-语言模型 |
| Inverse Dynamics Model (IDM) | 逆动力学模型 |
| Forward Dynamics Model (FDM) | 前向动力学模型 |
| Masked Diffusion | 掩码扩散 |
| Video Encoder | 视频编码器 |
| Token | Token（标记）|
| Context Window | 上下文窗口 |
| Autoregressive Training | 自回归训练 |
| Exponential Binning | 指数分箱 |
| Forking VM | 分叉虚拟机 |
| Rollout | Rollout（推演/ rollout）|
| Test-Time Compute | 测试时计算 |
| Zero-Shot | 零样本 |
| Long-Horizon Tasks | 长程任务 |
| Contractor-Labeled Data | 承包商标注数据 |
| Screen Recording | 屏幕录制 |
| Frame Reconstruction | 帧重建 |
