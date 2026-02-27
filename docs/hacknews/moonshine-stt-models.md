# Show HN: Moonshine Open-Weights STT models – higher accuracy than WhisperLargev3
# 展示 HN：Moonshine 开源权重语音转文字模型——准确率超越 WhisperLargev3

**Source:** https://github.com/moonshine-ai/moonshine  
**Date:** 2026-02-24

Moonshine is a new family of open-weight speech-to-text models that achieves higher accuracy than OpenAI's Whisper Large v3 while being significantly smaller and faster. This breakthrough represents a major advancement in accessible, high-quality speech recognition.

Moonshine 是一系列新的开源权重语音转文字模型，比 OpenAI 的 Whisper Large v3 实现了更高的准确率，同时体积更小、速度更快。这一突破代表了可访问、高质量语音识别技术的重大进步。

The Moonshine models range from 100M to 1B parameters and are designed to run efficiently on consumer hardware, including laptops and mobile devices. Despite their smaller size, they outperform Whisper on multiple benchmarks including word error rate and transcription accuracy.

Moonshine 模型从 1 亿到 10 亿参数不等，设计用于在消费级硬件（包括笔记本电脑和移动设备）上高效运行。尽管体积更小，它们在多个基准测试（包括词错误率和转录准确率）上超越了 Whisper。

Key achievements:
- 15% lower word error rate than Whisper Large v3 on LibriSpeech
- 5x faster inference on CPU
- Support for 99 languages with competitive performance
- Model sizes ranging from 150MB to 1.5GB

主要成就：
- 在 LibriSpeech 上比 Whisper Large v3 词错误率低 15%
- CPU 上推理速度快 5 倍
- 支持 99 种语言，性能具有竞争力
- 模型大小从 150MB 到 1.5GB 不等

The models are trained on a diverse dataset including audiobooks, podcasts, and conversational speech, making them robust across different audio domains. They handle challenging scenarios including multiple speakers, background noise, and various accents.

这些模型在包括有声读物、播客和对话语音在内的多样化数据集上训练，使它们在不同音频领域都很稳健。它们处理具有挑战性的场景，包括多人说话、背景噪音和各种口音。

Moonshine is released under the Apache 2.0 license, making it suitable for both commercial and research use. The project includes pre-trained models, training code, and a simple API for integration.

Moonshine 在 Apache 2.0 许可证下发布，适用于商业和研究用途。该项目包括预训练模型、训练代码和用于集成的简单 API。

The development team has also created efficient quantization and streaming implementations, enabling real-time transcription on resource-constrained devices.

开发团队还创建了高效的量化和流式实现，使资源受限设备上的实时转录成为可能。
