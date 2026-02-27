# How we rebuilt Next.js with AI in one week
# 我们如何在一周内用 AI 重建 Next.js

**Source:** https://blog.cloudflare.com/vinext/  
**Date:** 2026-02-24

Cloudflare's engineering team shares their experience of using AI to rebuild significant portions of Next.js in just one week. The project, codenamed ViNext, demonstrates the transformative potential of AI-assisted software development at scale.

Cloudflare 的工程团队分享了他们使用 AI 在一周内重建 Next.js 大部分功能的经验。这个代号为 ViNext 的项目展示了 AI 辅助大规模软件开发的变革潜力。

The team leveraged Claude and other AI coding assistants to accelerate development tasks that would traditionally take months. The project focused on creating a Next.js-compatible edge runtime that could run efficiently on Cloudflare's Workers platform.

团队利用 Claude 和其他 AI 编程助手来加速传统上需要数月时间的开发任务。该项目专注于创建一个与 Next.js 兼容的边缘运行时，可以在 Cloudflare 的 Workers 平台上高效运行。

Key insights from the project:
- AI assistants excelled at boilerplate generation and API implementation
- Human engineers focused on architecture decisions and edge case handling
- The hybrid approach achieved 10x speedup in initial implementation
- Code review remained essential for ensuring quality and security

项目的主要见解：
- AI 助手在样板代码生成和 API 实现方面表现出色
- 人类工程师专注于架构决策和边缘情况处理
- 混合方法在初始实现中实现了 10 倍加速
- 代码审查对于确保质量和安全仍然至关重要

The Cloudflare team found that AI was particularly effective at translating specifications into working code, implementing standard patterns, and refactoring existing codebases. However, complex debugging and performance optimization still required human expertise.

Cloudflare 团队发现，AI 在将规范转化为工作代码、实现标准模式和重构现有代码库方面特别有效。然而，复杂的调试和性能优化仍然需要人类专业知识。

The article details their workflow of using AI for rapid prototyping followed by human refinement. This approach allowed them to explore multiple implementation strategies quickly before committing to a final architecture.

文章详细介绍了他们使用 AI 进行快速原型设计，然后进行人工优化的工作流程。这种方法使他们能够在确定最终架构之前快速探索多种实现策略。

ViNext now powers thousands of applications on Cloudflare's edge network, demonstrating that AI-assisted development can produce production-ready systems when properly supervised.

ViNext 现在为 Cloudflare 边缘网络上的数千个应用提供支持，证明了在适当监督下，AI 辅助开发可以生产出可用于生产的系统。
