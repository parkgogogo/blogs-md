# Qwen3.5 122B and 35B models offer Sonnet 4.5 performance on local computers

> **TL;DR:** Alibaba releases four Qwen 3.5 medium models - Flash, 35B-A3B, 122B-A10B, and 27B - that match or beat the previous 235B flagship at a fraction of the compute. The 35B model activates just 3 billion parameters and still outperforms Qwen3-235B-A22B.

---

Ten days after dropping the 397B flagship that trades punches with GPT-5.2, Alibaba's Qwen team is now filling out the rest of the weight class. The Qwen 3.5 Medium Series puts four new models on the table, and the economics are the story here.

## The Lineup

| Model | Type | Total Params | Active Params | Context | License | API Price (Input/Output) |
|-------|------|--------------|---------------|---------|---------|--------------------------|
| Qwen3.5-Flash | Hosted API | Not disclosed | Not disclosed | 1M tokens | Proprietary | $0.10 / $0.40 per M |
| Qwen3.5-35B-A3B | MoE | 35B | 3B | 262K (1M ext.) | Apache 2.0 | Self-host |
| Qwen3.5-122B-A10B | MoE | 122B | 10B | 262K (1M ext.) | Apache 2.0 | Self-host |
| Qwen3.5-27B | Dense | 27B | 27B (all) | 262K (1M ext.) | Apache 2.0 | Self-host |

All four share the same Gated DeltaNet architecture that powers the 397B flagship: a 3:1 hybrid of linear attention (DeltaNet) and full softmax attention layers, native multimodal training from the ground up, and 256-expert MoE routing for the sparse models. The 27B is the odd one out - a dense model with all parameters active, using standard FFN layers instead of expert routing.

## The Numbers That Matter

The 35B-A3B model is the one that breaks brains. It activates 3 billion parameters - roughly the same compute budget as a small local model - and posts these scores:

| Benchmark | Qwen3.5-35B-A3B | Qwen3-235B-A22B | GPT-5-mini | Claude Sonnet 4.5 |
|-----------|-----------------|-----------------|------------|-------------------|
| MMLU-Pro | 85.3 | 84.4 | 83.7 | - |
| GPQA Diamond | 84.2 | 81.1 | 82.8 | - |
| HMMT Feb 25 | 89.0 | 85.1 | 89.2 | - |
| SWE-bench Verified | 69.2 | - | 72.0 | - |
| LiveCodeBench v6 | 74.6 | 75.1 | 80.5 | - |
| TAU2-Bench (Agent) | 81.2 | 58.5 | 69.8 | - |
| MMMU (Vision) | 81.4 | 80.6 | 79.0 | 79.6 |
| MathVision | 83.9 | 74.6 | 71.9 | 71.1 |
| ScreenSpot Pro | 68.6 | 62.0 | - | 36.2 |

The TAU2-Bench score - an agent task benchmark - is the standout. The 35B model scores 81.2 versus 58.5 for the previous 235B flagship. That's not a gap. That's a generation shift. On vision tasks, the medium models crush the previous vision-language flagship (Qwen3-VL-235B-A22B) across MMMU, MathVision, and ScreenSpot Pro.

The 122B-A10B and 27B dense models push even higher on most benchmarks, with the 27B posting the best SWE-bench Verified score of the trio at 72.4 - matching GPT-5-mini.

## Flash: The Production Play

Qwen3.5-Flash is the commercial wrapper. It gets 1M context by default, built-in tool support, and Alibaba's standard tiered pricing. At $0.10 per million input tokens, it undercuts virtually every frontier API on the market. For comparison, DeepSeek V3.2 charges $0.14/$0.28 per million tokens, and GPT-5-mini runs $2.50/$10.00.

## What This Means

The real signal isn't that Alibaba shipped four decent medium models. It's what the 35B-A3B result implies about the cost curve.

If 3 billion active parameters can match what 22 billion active parameters did six months ago - and do it with native vision, 256K context, and agent capabilities - then the inference cost floor just dropped by roughly an order of magnitude. Every company running Qwen3-235B in production can now get the same or better output from a model that uses 7x less compute per token.

Alibaba isn't being subtle about what this means. The tagline is "more intelligence, less compute," and the 35B model is the proof point. When better architecture, data quality, and RL can replace raw parameter count, the economics of AI inference change - and every lab charging per-token margins on frontier models needs to recalculate.

---

# Qwen3.5 122B和35B模型在本地电脑上提供Sonnet 4.5级别性能

> **太长不看：** 阿里巴巴发布了四款Qwen 3.5中型模型——Flash、35B-A3B、122B-A10B和27B——它们以极小的计算成本达到或超越了之前的235B旗舰模型。35B模型仅激活30亿参数，但仍能超越Qwen3-235B-A22B。

---

在发布能与GPT-5.2抗衡的397B旗舰模型仅十天后，阿里巴巴的Qwen团队正在完善其余的产品线。Qwen 3.5中型系列推出了四款新模型，而真正的亮点在于其经济性。

## 产品线

| 模型 | 类型 | 总参数量 | 激活参数量 | 上下文长度 | 许可证 | API价格（输入/输出） |
|------|------|----------|------------|------------|--------|---------------------|
| Qwen3.5-Flash | 托管API | 未公开 | 未公开 | 100万token | 专有 | $0.10 / $0.40 每百万 |
| Qwen3.5-35B-A3B | MoE | 350亿 | 30亿 | 262K（可扩展至1M） | Apache 2.0 | 自托管 |
| Qwen3.5-122B-A10B | MoE | 1220亿 | 100亿 | 262K（可扩展至1M） | Apache 2.0 | 自托管 |
| Qwen3.5-27B | Dense | 270亿 | 270亿（全部） | 262K（可扩展至1M） | Apache 2.0 | 自托管 |

四款模型均采用与397B旗舰模型相同的Gated DeltaNet架构：线性注意力（DeltaNet）与完整softmax注意力层以3:1比例混合、原生多模态训练，以及稀疏模型的256专家MoE路由。27B是个例外——它是一个密集模型，所有参数都激活，使用标准FFN层而非专家路由。

## 关键数据

35B-A3B模型是最令人震撼的。它仅激活30亿参数——计算预算与小型本地模型相当——却取得了以下成绩：

| 基准测试 | Qwen3.5-35B-A3B | Qwen3-235B-A22B | GPT-5-mini | Claude Sonnet 4.5 |
|----------|-----------------|-----------------|------------|-------------------|
| MMLU-Pro | 85.3 | 84.4 | 83.7 | - |
| GPQA Diamond | 84.2 | 81.1 | 82.8 | - |
| HMMT Feb 25 | 89.0 | 85.1 | 89.2 | - |
| SWE-bench Verified | 69.2 | - | 72.0 | - |
| LiveCodeBench v6 | 74.6 | 75.1 | 80.5 | - |
| TAU2-Bench (Agent) | 81.2 | 58.5 | 69.8 | - |
| MMMU (Vision) | 81.4 | 80.6 | 79.0 | 79.6 |
| MathVision | 83.9 | 74.6 | 71.9 | 71.1 |
| ScreenSpot Pro | 68.6 | 62.0 | - | 36.2 |

TAU2-Bench分数——一个智能体任务基准测试——尤为突出。35B模型得分81.2，而之前的235B旗舰仅为58.5。这不是差距，而是代际跨越。在视觉任务上，中型模型在MMMU、MathVision和ScreenSpot Pro上全面碾压之前的视觉-语言旗舰模型（Qwen3-VL-235B-A22B）。

122B-A10B和27B密集模型在大多数基准测试上表现更佳，其中27B在SWE-bench Verified上取得72.4的最佳成绩——与GPT-5-mini持平。

## Flash：生产环境的选择

Qwen3.5-Flash是商业封装版本。它默认支持100万token上下文，内置工具支持，以及阿里巴巴的标准分层定价。以每百万输入token仅$0.10的价格，它低于市场上几乎所有前沿API。相比之下，DeepSeek V3.2收费$0.14/$0.28每百万token，而GPT-5-mini则为$2.50/$10.00。

## 这意味着什么

真正的信号不在于阿里巴巴发布了四款不错的中型模型，而在于35B-A3B的结果对成本曲线意味着什么。

如果30亿激活参数能够达到六个月前220亿激活参数的水平——并且具备原生视觉、256K上下文和智能体能力——那么推理成本底线就下降了一个数量级。每个在生产环境中运行Qwen3-235B的公司现在都可以用每token少7倍计算量的模型获得相同或更好的输出。

阿里巴巴对此毫不讳言。他们的口号是"更智能，更少计算"，而35B模型就是明证。当更好的架构、数据质量和强化学习可以取代原始参数量时，AI推理的经济性就会改变——每个按token收费的前沿模型实验室都需要重新计算了。

---

**Source:** [Awesome Agents](https://awesomeagents.ai/news/qwen-3-5-medium-series/)  
**Original URL:** https://venturebeat.com/technology/alibabas-new-open-source-qwen3-5-medium-models-offer-sonnet-4-5-performance
