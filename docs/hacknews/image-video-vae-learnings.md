# Learnings from 4 months of Image-Video VAE experiments
# 四个月图像-视频 VAE 实验的心得

**Source**: https://www.linum.ai/field-notes/vae-reconstruction-vs-generation  
**Category**: AI/ML  
**Rating**: 9/10  
**Original Title**: Better Reconstruction ≠ Better Generation  
**Original Author**: Manu Chopra & Sahil Chopra  
**Publisher**: Field Notes by Linum (Linum, Inc.)  
**Published**: February 23, 2026

## Summary / 摘要

**EN**: This post documents Linum’s 4-month journey building an image-video VAE for latent diffusion. They detail architecture choices, co-training failures, NaN instability, artifact debugging, normalization changes (GroupNorm → SMC/PixelNorm), and multi-resolution curriculum design. Their core conclusion is important: better reconstruction metrics do not necessarily improve downstream diffusion generation quality. Over-optimizing reconstruction can force the latent space to encode noise/compression artifacts, harming learnability.

**CN**：本文记录了 Linum 团队用 4 个月构建图像-视频 VAE（用于潜空间扩散模型）的全过程，包括架构选择、图文共训失败、NaN 不稳定、伪影排查、归一化策略调整（GroupNorm → SMC/PixelNorm）以及多分辨率训练课程设计。最关键结论是：VAE 重建质量更好，并不必然带来下游扩散生成质量更好。若过度优化重建，潜空间会学习到噪声和压缩伪影，反而降低“可学习性”。

---

## Intro / 引言

**EN**: Modern video generation relies on diffusion transformers, but attention scales quadratically so pixel-space calculation is intractable at high resolution and long duration. A VAE compresses images/videos into continuous latent space, making diffusion training feasible.

**CN**：现代视频生成依赖扩散 Transformer，但注意力复杂度随序列长度二次增长，在高分辨率和长时长下直接在像素空间训练几乎不可行。VAE 通过将图像/视频压缩到连续潜空间，使扩散训练变得可行。

**EN**: Linum open-sources their Image-Video VAE, logs, and a key finding: stronger compression/reconstruction does not always correlate with VAE stability or downstream generation quality.

**CN**：Linum 开源了他们的图像-视频 VAE、实验日志，并给出关键发现：更强的压缩/重建效果并不总能对应更好的 VAE 稳定性或下游生成质量。

**EN**: They trained this model from Jul–Nov 2024, encountered months of NaNs, strange splotches, and co-training instability. Although they later used Wan 2.1 VAE for production text-to-video due to cost/speed tradeoffs, the lessons remain valuable.

**CN**：他们在 2024 年 7–11 月训练该模型，经历了数月 NaN、彩色斑块伪影、图文共训不稳定等问题。尽管后续在生产 T2V 中因成本与速度权衡采用了 Wan 2.1 VAE，这些经验仍很有价值。

---

## Why build a VAE? / 为什么要做 VAE？

**EN**: Diffusion models generate by denoising Gaussian noise. Whether autoregressive diffusion (token-by-token) or parallel diffusion (e.g., Stable Diffusion/FLUX style), transformer attention remains the bottleneck.

**CN**：扩散模型通过逐步去噪高斯噪声生成样本。无论是自回归扩散（逐 token）还是并行扩散（如 Stable Diffusion/FLUX），Transformer 注意力始终是计算瓶颈。

**EN**: A 720p, 5-second, 24 FPS clip has about 110M raw pixel tokens. This is too expensive for direct diffusion modeling.

**CN**：一个 720p、5 秒、24 FPS 的短视频约有 1.1 亿原始像素 token，直接用于扩散建模成本极高。

**EN**: VAEs provide continuous compressed latents (unlike JPEG/AV1’s discrete quantization), which neural networks can consume efficiently.

**CN**：VAE 提供连续压缩潜变量（不同于 JPEG/AV1 的离散量化），更适合神经网络高效处理。

---

## A crash course on VAEs / VAE 速览

**EN**: Autoencoder maps input x → latent z via encoder, then reconstructs x̂ via decoder. Bottleneck enforces information compression.

**CN**：自编码器通过编码器把输入 x 压成潜变量 z，再由解码器重建 x̂。瓶颈迫使模型学习有效压缩。

**EN**: VAE extends this by encoding a distribution over z (typically Gaussian parameters μ and σ), then sampling z.

**CN**：VAE 的区别在于编码的是 z 的概率分布（通常是高斯参数 μ、σ），再从中采样 z。

**EN**: Training objective (per modality) combines KL, reconstruction, perceptual, and adversarial terms:

**CN**：训练目标（每种模态）通常包含 KL、重建、感知和对抗项：

```text
L_modality = λ1·L_KL + λ2·L_recon + λ3·L_perceptual + λ4·L_adversarial
```

**EN**: In practice, KL is given tiny weight (e.g., 1e-6) because the VAE is primarily used as a compressor for diffusion, not as a standalone generator.

**CN**：实践中 KL 权重很小（如 1e-6），因为这里的 VAE 主要用于给扩散模型做压缩，而非独立生成器。

**EN**: Reconstruction uses NLL (L1-like under Laplacian decoder assumption with learned confidence scale). Perceptual loss (VGG features) and adversarial loss sharpen outputs.

**CN**：重建项采用负对数似然（在 Laplace 解码分布下近似 L1，并带可学习置信度尺度）；感知损失（VGG 特征）与对抗损失用于提升清晰度。

**EN**: For image-video training, total objective is weighted sum of image and video losses:

**CN**：图像+视频共训时，总损失是两者的加权和：

```text
L = w1·L_image + w2·L_video
```

---

## Building a baseline (1 week) / 构建基线（1 周）

**EN**: In Fall 2024 there were no strong open-source video VAEs, so they started with video-only VAE using Conv3D-based CNN encoder/decoder.

**CN**：2024 年秋当时缺少高质量开源视频 VAE，因此他们先从纯视频 VAE 开始，采用 Conv3D CNN 编码器/解码器。

**EN**: Initial setup used 4× spatial and 4× temporal downsampling. Reconstructions looked nearly identical, but compression was too weak for practical diffusion training (OOM even for short 360p clips on 80GB H100).

**CN**：初始设定为空间 4×、时间 4× 下采样。虽然重建观感接近原图，但压缩率太低，不适合扩散训练（在 80GB H100 上短 360p 视频也会 OOM）。

**EN**: They diagnosed super-linear memory growth from AttentionBlock. Experiments showed 8× spatial + 4× temporal (effective ~48×) was the best usable tradeoff.

**CN**：他们定位到 AttentionBlock 导致内存超线性增长。实验表明空间 8× + 时间 4×（等效约 48×）是可用性最好的折中方案。

**EN**: Insight: fixed latent sizes tied only to resolution are suboptimal; content-aware adaptive tokenization is likely better long-term.

**CN**：洞察：仅按分辨率机械决定潜变量大小并不理想，长期看应走“内容自适应 tokenization（自适应标记化）”。

---

## Co-training image and video (3 months) / 图像与视频共训（3 个月）

### Handling 1-frame images / 处理单帧图像

**EN**: They padded each image into a 4-frame “static video” so temporal downsampling reduced it back to one latent frame. Video reconstructions were fine; image reconstructions became blurry.

**CN**：他们把单张图像复制成 4 帧“静态视频”，经时间下采样后回到 1 帧潜变量。结果是视频重建正常，但图像重建明显变糊。

### Death by summation / “求和致死”

**EN**: Their recon loss summed over all elements then divided by batch size, making larger tensors dominate optimization.

**CN**：他们的重建损失对所有元素求和后仅按 batch size 归一，导致大张量样本主导优化。

**EN**: A 180p 2s video has ~10× more elements than their padded image sample, so optimizer effectively ignored image quality.

**CN**：180p 2 秒视频元素数量约是其“静态视频图像样本”的 10 倍，优化器几乎“看不见”图像质量。

**EN**: Naive mean-normalization fixed dominance but over-amplified per-pixel gradients on smaller tensors. Their fix: normalize sum-loss using a fixed reference shape S_ref to keep gradient behavior sane while enabling explicit modality/resolution reweighting.

**CN**：简单取均值虽能消除“大样本支配”，却会让小张量每像素梯度过大。其修复方案是用固定参考形状 S_ref 缩放 sum-loss，在不扭曲梯度结构的前提下做模态/分辨率再加权。

### NaN Hell / NaN 地狱

**EN**: Even with weighting tweaks, training still exploded. GroupNorm stabilized early phase but not late training.

**CN**：即便调整权重，训练仍会爆炸。GroupNorm 只能稳定早期训练，无法解决后期崩溃。

**EN**: They added FiLM (Feature-wise Linear Modulation) conditioned on image/video identity embedding, but once modulation activated, gradients exploded again.

**CN**：他们引入按图像/视频身份嵌入条件化的 FiLM（特征级线性调制），但调制一旦生效，梯度再次爆炸。

**EN**: FiLM was removed. They then used adaptive gradient clipping (AGC variant), which stabilized NaNs but introduced colored splotch artifacts.

**CN**：最终移除了 FiLM，改用自适应梯度裁剪（AGC 变体）来稳定 NaN，但又引入了彩色斑块伪影。

---

## Out, damned spot! / 斑点问题排查

**EN**: Inspired by LiteVAE, they replaced GroupNorm+CNN style with Self-Modulating Convolution (SMC), which normalizes weights (not activations) and modulates channels more flexibly.

**CN**：受 LiteVAE 启发，他们将 GroupNorm+CNN 风格替换为 SMC（Self-Modulating Convolution，自调制卷积）：归一化的是卷积权重而非激活，并以更细粒度调制通道。

**EN**: SMC removed splotches at 180p, but black dots reappeared at 360p/720p.

**CN**：SMC 在 180p 消除了斑块，但在 360p/720p 又出现黑点。

**EN**: By instrumenting layer-wise activation L2 norms, they traced the issue to the Encoder Mid-Block AttentionBlock.

**CN**：通过逐层记录激活 L2 范数，他们把问题定位到编码器中间块（Mid Block）的 AttentionBlock。

**EN**: Fully removing GroupNorm in mid-block was unstable, so they switched to PixelNorm/QK-Norm-like normalization to prevent high-norm outlier pixels from hijacking attention maps.

**CN**：直接移除中间块 GroupNorm 不稳定，于是改用更轻的 PixelNorm（近似 QK-Norm/cosine attention 思路），防止高范数离群像素“劫持”注意力图。

**EN**: They also note Meta’s MovieGen used a different fix: adding an activation-outlier penalty term in VAE loss.

**CN**：他们还提到 Meta MovieGen 的另一种方案：在 VAE 损失中增加激活离群值惩罚项。

---

## Training across resolutions (2 weeks) / 跨分辨率训练（2 周）

**EN**: A 720p final checkpoint forgot low-resolution reconstruction. Sequential curriculum (180p→360p→720p) caused catastrophic forgetting.

**CN**：720p 最终检查点出现对低分辨率重建能力的灾难性遗忘。顺序式课程（180p→360p→720p）是诱因。

**EN**: They switched to mixed-resolution curriculum and tuned loss weights: ~1.1 (180p), 0.1 (360p), 0.01 (720p).

**CN**：他们改为多分辨率并行课程，并通过超参搜索得到权重：约 1.1（180p）、0.1（360p）、0.01（720p）。

---

## Why switch to Wan 2.1 VAE? / 为什么换到 Wan 2.1 VAE？

**EN**: Diffusion training usually embeds dataset offline once via VAE. When Wan 2.1 VAE was released (Feb 2025), Linum benchmarked it against their own.

**CN**：扩散训练通常先离线用 VAE 对数据集做一次嵌入。2025 年 2 月 Wan 2.1 VAE 发布后，Linum 做了对比测试。

**EN**: Performance was similar, but Wan was smaller/faster (without full spatio-temporal attention), reducing embedding cost for large-scale data.

**CN**：生成效果相当，但 Wan 模型更小更快（不做完整时空注意力），可显著降低大规模数据集嵌入成本。

---

## Better reconstruction ≠ better generation / 更好重建 ≠ 更好生成

**EN**: Their biggest retrospective: over-focusing on difficult low-quality samples was likely a mistake; many such samples are heavily compressed/noisy and not worth forcing perfect reconstruction.

**CN**：他们最重要的复盘：过度执着于难样本（尤其低质量样本）可能是错误方向；这类样本多含重压缩噪声，不值得追求“完美重建”。

**EN**: Over-optimizing reconstruction encourages latent space to memorize compression artifacts/noise, harming semantic disentanglement and diffusion learnability.

**CN**：过度优化重建会驱使潜空间记忆压缩伪影与噪声，破坏语义解耦能力，降低扩散模型可学习性。

**EN**: They cite evidence: improved VAE rFID can still worsen downstream generation gFID (e.g., Yao et al. 2025).

**CN**：他们引用了相关证据：即便 VAE 的重建指标 rFID 变好，下游生成 gFID 仍可能变差（如 Yao et al., 2025）。

**EN**: Two active directions for more “learnable” latent spaces:
1) Regularize/alignment-train VAE toward semantic features (REPA, VA-VAE, VTP line of work).  
2) Skip VAE and learn compression inside diffusion directly (e.g., JIT).

**CN**：当前更“可学习”潜空间的两条路径：
1）做语义对齐正则化，让 VAE 更贴近语义表征（REPA、VA-VAE、VTP 等路线）；  
2）跳过 VAE，让扩散模型直接学习压缩（如 JIT）。

**EN**: Their view: JIT is promising but may still overfit noise; semantic alignment may be key.

**CN**：他们判断：JIT 很有潜力，但仍可能过拟合噪声；语义对齐很可能是关键。

---

## Who are we? / 团队介绍

**EN**: Linum is run by two brothers building text-to-video models from scratch, aiming to make animation creation accessible to everyone.

**CN**：Linum 由两兄弟创立，从零训练文本到视频模型，目标是让动画创作对所有人更可及。

---

## Key technical terms glossary / 关键术语对照

- **VAE (Variational Autoencoder)**：变分自编码器  
- **Latent space**：潜空间  
- **Diffusion Transformer**：扩散 Transformer  
- **Autoregressive diffusion**：自回归扩散  
- **Perceptual loss**：感知损失  
- **Adversarial loss**：对抗损失  
- **GroupNorm / PixelNorm / QK-Norm**：组归一化 / 像素归一化 / QK 归一化  
- **SMC (Self-Modulating Convolution)**：自调制卷积  
- **AGC (Adaptive Gradient Clipping)**：自适应梯度裁剪  
- **NaN instability**：NaN 不稳定（数值爆炸）  
- **rFID / gFID**：重建 FID / 生成 FID  
- **Catastrophic forgetting**：灾难性遗忘
