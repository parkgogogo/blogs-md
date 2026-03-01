---
title: "Mercury 2: The fastest reasoning LLM, powered by diffusion"
url: "https://www.inceptionlabs.ai/blog/introducing-mercury-2"
rating: 9
category: "AI/ML - LLM Architecture"
date: "2026-02-28"
---

# Mercury 2: The fastest reasoning LLM, powered by diffusion

Today, we're introducing Mercury 2 — the world's fastest reasoning language model, built to make production AI feel instant.

## A New Architecture for Language Models

While the AI industry spends billions squeezing incremental speed from token-by-token autoregressive models, Inception's diffusion-based generation represents the architectural breakthrough that makes high throughput reasoning native to the model.

### The Problem with Autoregressive Models

All traditional large language models generate text one token at a time, left to right. This sequential generation creates inherent latency bottlenecks that limit real-world deployment of reasoning systems, especially for applications requiring fast response times.

### The Diffusion Solution

Mercury 2 doesn't decode sequentially. It generates responses through parallel refinement, producing multiple tokens simultaneously and converging over a small number of steps. Think of it as: less typewriter, more editor revising a full draft at once.

This diffusion-based approach enables:
- **5x faster performance** than leading speed-optimized LLMs
- **Dramatically lower inference costs** through improved GPU efficiency
- **Parallel token generation** rather than sequential token-by-token output
- **1000+ tokens per second** generation speed

## Technical Architecture

Mercury 2 is built on a diffusion-based large language model (dLLM) architecture. While diffusion implies specific training and generation algorithms, it doesn't constrain the underlying neural network architecture. Mercury models are parameterized via the Transformer architecture and trained to predict multiple tokens in parallel.

The key insight is that improvements are suggested by a neural network trained on large amounts of data to globally improve the quality of the answer by modifying multiple tokens in parallel — rather than generating left-to-right one token at a time.

## The First Reasoning dLLM

Mercury 2 represents the world's first commercial-scale diffusion-based LLM specifically designed for reasoning tasks. This paradigm shift from autoregressive to diffusion-based text generation enables:

- **Fine-grained control** over the generation process
- **Enhanced reasoning capabilities** through parallel refinement
- **Multi-modal data processing** potential
- **Improved reliability** for real-world use cases

## Real-World Impact

The launch of Mercury 2 delivers on the promise of making production AI feel truly instant. By reducing the latency and cost barriers that have limited real-world deployment of reasoning systems, Mercury 2 opens new possibilities for AI applications that require both high-quality reasoning and fast response times.

Inception Labs continues to pioneer diffusion-based language models, offering capabilities comparable to traditional LLMs — including code generation and question-answering — but with significantly faster performance and reduced computing costs.

---

# 中文翻译

今天，我们正式推出 Mercury 2 —— 全球最快的推理语言模型，专为让生产级 AI 实现真正的即时响应而打造。

## 语言模型的新架构

当 AI 行业投入数十亿美元，试图从逐词生成的自回归模型中压榨出 incremental 的速度提升时，Inception Labs 的扩散式生成技术代表了让高吞吐推理成为模型原生能力的架构级突破。

### 自回归模型的问题

所有传统的大型语言模型都是逐词、从左到右地生成文本。这种顺序生成方式造成了固有的延迟瓶颈，限制了推理系统在现实世界中的部署，尤其是对响应速度有要求的应用场景。

### 扩散模型的解决方案

Mercury 2 不按顺序解码。它通过并行精炼来生成响应，同时产出多个词元（token），并在少量步骤内收敛。可以这样想：不再是打字机式的逐字敲击，更像是编辑一次性修改整篇草稿。

这种基于扩散的方法实现了：
- **比领先的速度优化型 LLM 快 5 倍**的性能
- 通过提升 GPU 效率实现**大幅降低的推理成本**
- **并行词元生成**而非顺序的逐词输出
- **每秒 1000+ 词元**的生成速度

## 技术架构

Mercury 2 建立在基于扩散的大型语言模型（dLLM，diffusion-based Large Language Model）架构之上。虽然扩散意味着特定的训练和生成算法，但它并不限制底层神经网络架构。Mercury 模型采用 Transformer 架构进行参数化，并经过训练以并行预测多个词元。

核心洞察在于：由一个在大规模数据上训练的神经网络来全局性地提升答案质量，通过同时修改多个词元来实现 —— 而不是从左到右一次生成一个词元。

## 首个推理型 dLLM

Mercury 2 代表了全球首个专为推理任务设计的商业级扩散式大语言模型。这种从自回归到扩散式文本生成的范式转变实现了：

- 对生成过程的**细粒度控制**
- 通过并行精炼实现的**增强推理能力**
- **多模态数据处理**潜力
- 针对真实应用场景的**更高可靠性**

## 现实世界的影响

Mercury 2 的发布兑现了让生产级 AI 真正即时响应的承诺。通过降低限制推理系统现实世界部署的延迟和成本障碍，Mercury 2 为需要高质量推理和快速响应时间的 AI 应用开辟了新的可能性。

Inception Labs 继续引领基于扩散的语言模型，提供与传统 LLM 相当的能力 —— 包括代码生成和问答 —— 但具有显著更快的性能和更低的计算成本。
