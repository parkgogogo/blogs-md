# Capybara: A Unified Visual Creation Model
# Capybara: 统一视觉创作模型

**Source**: https://github.com/xgen-universe/Capybara  
**Category**: AI/ML  
**Rating**: 9/10

---

## Summary
## 摘要

Capybara is an open-source unified visual creation model that brings image generation, video generation, and instruction-based editing into a single pipeline. Released in February 2026 by the xgen-universe team, it supports Text-to-Image (T2I), Text-to-Video (T2V), Text+Image-to-Image (TI2I), and Text+Video-to-Video (TV2V) tasks—all within one model architecture built on top of HunyuanVideo.

Capybara 是一个开源的统一视觉创作模型，将图像生成、视频生成和基于指令的编辑整合到一个统一的流水线中。由 xgen-universe 团队于 2026 年 2 月发布，它支持文本到图像（T2I）、文本到视频（T2V）、文本+图像到图像（TI2I）和文本+视频到视频（TV2V）任务——所有这些都在基于 HunyuanVideo 的单一模型架构中实现。

---

## Key Features
## 核心特性

### 🎬 Multi-Task Unified Architecture
### 🎬 多任务统一架构

**EN**: Capybara consolidates multiple visual generation tasks into a single model, eliminating the need for separate models for each task type. This unified approach simplifies deployment and reduces memory overhead when switching between generation modes.

**CN**: Capybara 将多种视觉生成任务整合到一个模型中，无需为每种任务类型使用单独的模型。这种统一的方法简化了部署，并在切换生成模式时减少了内存开销。

Supported tasks include:
支持的任务包括：
- **T2I (Text-to-Image)**: Generate images from text prompts
- **T2I（文本到图像）**: 从文本提示生成图像
- **T2V (Text-to-Video)**: Generate videos from text descriptions
- **T2V（文本到视频）**: 从文本描述生成视频
- **TI2I (Text+Image-to-Image)**: Edit images using text instructions
- **TI2I（文本+图像到图像）**: 使用文本指令编辑图像
- **TV2V (Text+Video-to-Video)**: Edit videos based on text instructions
- **TV2V（文本+视频到视频）**: 基于文本指令编辑视频

### 🚀 Efficient Inference with Quantization Support
### 🚀 高效推理与量化支持

**EN**: The model supports multiple precision formats to accommodate different GPU memory constraints:

**CN**: 该模型支持多种精度格式以适应不同的 GPU 内存限制：

- **BF16**: Full precision for maximum quality (~20GB VRAM recommended)
- **BF16**: 完整精度以获得最佳质量（推荐约 20GB VRAM）
- **FP8**: 8-bit floating point for balanced quality and efficiency (~10-12GB VRAM)
- **FP8**: 8 位浮点数，平衡质量与效率（约 10-12GB VRAM）
- **FP4**: 4-bit for edge devices with limited memory
- **FP4**: 4 位精度用于内存受限的边缘设备

**EN**: When FP8 quantization is enabled with CPU offloading, the transformer weights stay quantized on GPU while activations and compute remain in the selected dtype (bf16 or fp16). Only weights are quantized; they are dequantized on-the-fly during matrix multiplications.

**CN**: 当启用 FP8 量化并配合 CPU 卸载时，transformer 权重在 GPU 上保持量化状态，而激活值和计算保持在选定的数据类型（bf16 或 fp16）。只有权重被量化；它们在矩阵乘法期间实时反量化。

### 🛠️ ComfyUI Integration
### 🛠️ ComfyUI 集成

**EN**: Capybara provides native ComfyUI nodes for visual workflow creation. The custom nodes include:

**CN**: Capybara 提供原生的 ComfyUI 节点用于可视化工作流创建。自定义节点包括：

- `CapybaraLoadPipeline`: Load all model components (transformer, VAE, text encoders, vision encoder, scheduler)
- `CapybaraLoadPipeline`: 加载所有模型组件（transformer、VAE、文本编码器、视觉编码器、调度器）
- `CapybaraGenerate`: Main generation node
- `CapybaraGenerate`: 主生成节点
- `CapybaraLoadVideo` / `GetVideoComponents` / `CreateVideo`: Video I/O utilities
- `CapybaraLoadVideo` / `GetVideoComponents` / `CreateVideo`: 视频输入/输出工具

**EN**: The ComfyUI workflow follows a simple pattern: LoadVideo → GetVideoComponents → CapybaraLoadPipeline → CapybaraGenerate → CreateVideo → SaveVideo for video tasks, with similar flows for image generation and editing.

**CN**: ComfyUI 工作流遵循简单模式：视频任务为 LoadVideo → GetVideoComponents → CapybaraLoadPipeline → CapybaraGenerate → CreateVideo → SaveVideo，图像生成和编辑有类似的流程。

---

## Technical Architecture
## 技术架构

**EN**: Capybara is built on the HunyuanVideo foundation, leveraging its diffusion transformer architecture. The model uses:

**CN**: Capybara 基于 HunyuanVideo 基础构建，利用其扩散 transformer 架构。该模型使用：

- **3D VAE with CausalConv3D**: Compresses pixel-space videos and images into a compact latent space with compression ratios of 4 (temporal), 8 (spatial), and 16 (channel)
- **3D VAE with CausalConv3D**: 将像素空间的视频和图像压缩到紧凑的潜在空间，压缩比分别为 4（时间）、8（空间）和 16（通道）
- **Full Attention Mechanism**: Unified attention for both image and video generation, outperforming divided spatiotemporal attention approaches
- **Full Attention 机制**: 图像和视频生成的统一注意力机制，性能优于分离的时空注意力方法
- **Multi-Resolution Training**: Supports various input resolutions without quality degradation
- **多分辨率训练**: 支持各种输入分辨率而不会降低质量

---

## Installation & Usage
## 安装与使用

### Requirements
### 环境要求

**EN**: The recommended environment includes:

**CN**: 推荐环境包括：

- Python 3.10+
- PyTorch 2.0+
- CUDA-capable GPU (NVIDIA recommended)
- 10-24GB VRAM depending on quantization mode
- 根据量化模式需要 10-24GB VRAM

### Quick Start
### 快速开始

**EN**: To use Capybara with ComfyUI:

**CN**: 在 ComfyUI 中使用 Capybara：

```bash
# Install dependencies
pip install -r requirements.txt

# Symlink to ComfyUI custom nodes
ln -s /path/to/Capybara /path/to/ComfyUI/custom_nodes/Capybara
```

**EN**: For T2V/T2I tasks, no reference image/video is needed. For TI2I, connect a LoadImage node to the reference input. For TV2V, connect video frames from LoadVideo → GetVideoComponents to the reference input.

**CN**: 对于 T2V/T2I 任务，不需要参考图像/视频。对于 TI2I，将 LoadImage 节点连接到参考输入。对于 TV2V，将 LoadVideo → GetVideoComponents 的视频帧连接到参考输入。

---

## Model Capabilities
## 模型能力

**EN**: Capybara represents a significant advancement in unified visual AI by combining:

**CN**: Capybara 通过结合以下功能代表了统一视觉 AI 的重大进步：

1. **Unified Training**: Single model handles diverse tasks without task-specific fine-tuning
2. **统一训练**: 单一模型处理多种任务，无需针对特定任务的微调
3. **Instruction Following**: Natural language editing commands for precise control
4. **指令遵循**: 自然语言编辑命令实现精确控制
5. **Cross-Modal Generation**: Seamless transition between image and video domains
6. **跨模态生成**: 图像和视频领域之间的无缝转换
7. **Memory Efficiency**: Smart offloading and quantization reduce hardware requirements
8. **内存效率**: 智能卸载和量化降低硬件要求

---

## Citation
## 引用

**EN**: If you use Capybara in your research, please cite:

**CN**: 如果在研究中使用 Capybara，请引用：

```bibtex
@misc{capybara2026rao,
  title={Capybara: A Unified Visual Creation Model},
  author={Rao, Zhefan and Che, Haoxuan and Hu, Ziwen and Zou, Bin and 
          Liu, Yaofang and He, Xuanhua and Choi, Chong-Hou and He, Yuyang and 
          Chen, Haoyu and Su, Jingran and Li, Yanheng and Chu, Meng and 
          Lei, Chenyang and Zhao, Guanhua and Li, Zhaoqing and Zhang, Xichen and 
          Li, Anping and Liu, Lin and Tu, Dandan and Liu, Rui},
  year={2026}
}
```

---

## License
## 许可证

**EN**: Released under the MIT License.

**CN**: 基于 MIT 许可证发布。

---

## Resources
## 资源链接

- **GitHub Repository**: https://github.com/xgen-universe/Capybara
- **Hugging Face Model**: https://huggingface.co/xgen-universe/Capybara
- **ComfyUI Workflows**: https://comfy.org/templates/Image_capybara_v0_1_text_to_image/
- **YouTube Demo**: https://www.youtube.com/watch?v=4uteHsrYjxY

---

## Why It Matters
## 为什么重要

**EN**: Capybara addresses a major pain point in the generative AI ecosystem: the fragmentation of tools. Previously, creators needed separate models (SDXL/FLUX for images, HunyuanVideo/Wan for video, InstructPix2Pix for editing). Capybara unifies these capabilities, reducing model management complexity and enabling new creative workflows where images can seamlessly become videos and vice versa—all with consistent style and quality.

**CN**: Capybara 解决了生成式 AI 生态系统中的一个主要痛点：工具的碎片化。以前，创作者需要单独的模型（SDXL/FLUX 用于图像、HunyuanVideo/Wan 用于视频、InstructPix2Pix 用于编辑）。Capybara 统一了这些能力，减少了模型管理复杂性，并启用了新的创意工作流——图像可以无缝变成视频，反之亦然——所有这些都保持一致的风格和质量。

**EN**: For AI/frontend developers, this means simplified deployment pipelines, reduced infrastructure costs, and the ability to build richer multimedia applications with a single model endpoint.

**CN**: 对于 AI/前端开发者来说，这意味着简化的部署流程、降低的基础设施成本，以及使用单一模型端点构建更丰富多媒体应用的能力。
