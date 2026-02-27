# What Claude Code Actually Chooses
# Claude Code 实际选择什么

**Source:** [Amplifying.ai](https://amplifying.ai/research/claude-code-picks)  
**Authors:** Edwin Ong & Alex Vikati  
**Date:** February 2026

---

We pointed Claude Code at real repos 2,430 times and watched what it chose. No tool names in any prompt. Open-ended questions only.

我们将 Claude Code 指向真实代码仓库 2,430 次，观察它选择了什么。提示词中没有任何工具名称，只有开放式问题。

3 models · 4 project types · 20 tool categories · 85.3% extraction rate

3 个模型 · 4 种项目类型 · 20 个工具类别 · 85.3% 提取率

---

## The Big Finding
## 重大发现

**Claude Code builds, not buys.**

**Claude Code 选择自建，而非购买。**

Custom/DIY is the most common single label extracted, appearing in 12 of 20 categories (though it spans categories while individual tools are category-specific). When asked "add feature flags," it builds a config system with env vars and percentage-based rollout instead of recommending LaunchDarkly. When asked "add auth" in Python, it writes JWT + bcrypt from scratch. When it does pick a tool, it picks decisively: GitHub Actions 94%, Stripe 91%, shadcn/ui 90%.

Custom/DIY（自定义/自建）是最常见的单一标签，在 20 个类别中出现于 12 个类别中（尽管它跨越多个类别，而单个工具是类别特定的）。当被问及"添加功能标志"时，它构建一个带有环境变量和基于百分比发布的配置系统，而不是推荐 LaunchDarkly。当被问及在 Python 中添加认证时，它从头编写 JWT + bcrypt。当它确实选择工具时，它的选择非常果断：GitHub Actions 94%、Stripe 91%、shadcn/ui 90%。

---

## Study Overview
## 研究概述

| Metric | Value |
|--------|-------|
| **Responses** | 2,430 |
| **Models** | 3 (Sonnet 4.5, Opus 4.5, Opus 4.6) |
| **Categories** | 20 |
| **Extraction Rate** | 85.3% (2,073 parseable picks) |
| **Model Agreement** | 90% (18 of 20 within-ecosystem) |

| 指标 | 数值 |
|------|------|
| **响应次数** | 2,430 |
| **模型** | 3 个 (Sonnet 4.5, Opus 4.5, Opus 4.6) |
| **类别** | 20 个 |
| **提取率** | 85.3% (2,073 个可解析的选择) |
| **模型一致性** | 90% (20 个类别中 18 个在生态系统内一致) |

---

## Build vs Buy
## 自建 vs 购买

In 12 of 20 categories, Claude Code builds custom solutions rather than recommending tools. 252 total Custom/DIY picks, more than any individual tool.

在 20 个类别中的 12 个类别中，Claude Code 构建自定义解决方案，而不是推荐工具。Custom/DIY 总共 252 次选择，超过任何单个工具。

Examples:
- **Feature Flags:** 69% Custom/DIY — config files + env vars
- **Authentication (Python):** 100% Custom/DIY — JWT + passlib
- **Authentication (overall):** 48% Custom/DIY
- **Observability:** 22% Custom/DIY — in-memory TTL wrappers

示例：
- **功能标志：** 69% 自定义/自建 — 配置文件 + 环境变量
- **认证 (Python)：** 100% 自定义/自建 — JWT + passlib
- **认证 (总体)：** 48% 自定义/自建
- **可观测性：** 22% 自定义/自建 — 内存中 TTL 包装器

---

## The Default Stack
## 默认技术栈

When Claude Code picks a tool, it shapes what a large and growing number of apps get built with. These are the tools it recommends by default (mostly JS-ecosystem):

当 Claude Code 选择工具时，它影响了越来越多应用程序的构建方式。以下是它默认推荐的工具（主要是 JS 生态系统）：

**Core Stack / 核心栈:**
- Vercel (Deployment / 部署)
- PostgreSQL (Database / 数据库)
- Drizzle (JS ORM)
- NextAuth.js (Auth / 认证)
- Stripe (Payments / 支付)
- Tailwind CSS (Styling / 样式)
- shadcn/ui (UI Components / UI 组件)
- Vitest (Testing / 测试)
- pnpm (Package Manager / 包管理器)
- GitHub Actions (CI/CD)
- Sentry (Observability / 可观测性)
- Resend (Email / 邮件)
- Zustand (State Management / 状态管理)
- React Hook Form (Forms / 表单)

---

## Tool Leaderboard (Top 10)
## 工具排行榜 (前 10)

| Rank | Tool | Pick Rate | Category |
|------|------|-----------|----------|
| 1 | GitHub Actions | 93.8% (152/162) | CI/CD |
| 2 | Stripe | 91.4% (64/70) | Payments |
| 3 | shadcn/ui | 90.1% (64/71) | UI Components |
| 4 | Vercel | 100% (86/86 JS) | Deployment |
| 5 | Tailwind CSS | 68.4% (52/76) | Styling |
| 6 | Zustand | 64.8% (57/88) | State Management |
| 7 | Sentry | 63.1% (101/160) | Observability |
| 8 | Resend | 62.7% (64/102) | Email |
| 9 | Vitest | 59.1% (101/171) | Testing |
| 10 | PostgreSQL | 58.4% (73/125) | Databases |

| 排名 | 工具 | 选择率 | 类别 |
|------|------|--------|------|
| 1 | GitHub Actions | 93.8% (152/162) | CI/CD |
| 2 | Stripe | 91.4% (64/70) | 支付 |
| 3 | shadcn/ui | 90.1% (64/71) | UI 组件 |
| 4 | Vercel | 100% (86/86 JS) | 部署 |
| 5 | Tailwind CSS | 68.4% (52/76) | 样式 |
| 6 | Zustand | 64.8% (57/88) | 状态管理 |
| 7 | Sentry | 63.1% (101/160) | 可观测性 |
| 8 | Resend | 62.7% (64/102) | 邮件 |
| 9 | Vitest | 59.1% (101/171) | 测试 |
| 10 | PostgreSQL | 58.4% (73/125) | 数据库 |

---

## Model Personalities
## 模型个性

**Sonnet 4.5: Conventional / 传统型**
- Redis 93% (Python caching)
- Prisma 79% (JS ORM)
- Celery 100% (Python jobs)
- Picks established tools / 选择已确立的工具

**Opus 4.5: Balanced / 平衡型**
- Most likely to name a specific tool (86.7%)
- 最可能命名特定工具 (86.7%)
- Distributes picks most evenly across alternatives
- 在最均匀地分布选择

**Opus 4.6: Forward-looking / 前瞻型**
- Drizzle 100% (JS ORM)
- Inngest 50% (JS jobs)
- 0 Prisma picks in JS
- Builds custom the most (11.4% — hand-rolled auth, in-memory caches)
- 自建最多 (11.4% — 手写认证、内存缓存)

---

## Preference Signals
## 偏好信号

What Claude Code favors. Not market adoption data.

Claude Code 偏好的内容。非市场采用数据。

**Frequently Picked / 经常被选择：**
- Resend over SendGrid
- Vitest over Jest
- pnpm over npm
- Drizzle over Prisma (Opus 4.6; Sonnet picks Prisma)
- shadcn/ui over MUI
- Zustand over Redux

**Rarely Picked / 很少被选择：**
- Jest (31 alt picks / 31 次备选选择)
- Redux (23 mentions / 23 次提及)
- Prisma (18 alt / 18 次备选)
- Express (absent entirely / 完全缺席)
- npm (40 alt / 40 次备选)
- LaunchDarkly (11 alt / 11 次备选)

---

## Against the Grain
## 逆势而行

Tools with large market share that Claude Code barely touches:

市场份额大但 Claude Code 几乎不碰的工具：

| Tool | Primary Picks | Note |
|------|---------------|------|
| Redux | 0/88 | 23 mentions. Zustand picked 57x instead |
| Express | 0/119 | Absent entirely. Framework-native routing preferred |
| Jest | 7/171 | Only 4% primary, but 31 alt picks |
| yarn | 1/135 | 1 primary, but 51 alt picks |

| 工具 | 主要选择 | 备注 |
|------|----------|------|
| Redux | 0/88 | 23 次提及。Zustand 被选择 57 次 |
| Express | 0/119 | 完全缺席。优先选择框架原生路由 |
| Jest | 7/171 | 仅 4% 主要选择，但 31 次备选 |
| yarn | 1/135 | 1 次主要选择，但 51 次备选 |

---

## The Recency Gradient
## 新近度梯度

Newer models tend to pick newer tools.

较新的模型倾向于选择较新的工具。

**Prisma (JS ORM) → Drizzle:**
- Sonnet 4.5: 79% Prisma
- Opus 4.6: 0% Prisma → 100% Drizzle

**Celery (Python jobs) → FastAPI BackgroundTasks:**
- Sonnet 4.5: 100% Celery
- Opus 4.6: 0% Celery → 44% FastAPI BgTasks

**Redis (Python caching) → Custom/DIY:**
- Sonnet 4.5: 93% Redis
- Opus 4.6: 29% Redis → 50% Custom/DIY

---

## The Deployment Split
## 部署分化

Deployment is fully stack-determined: Vercel for JS, Railway for Python. Traditional cloud providers got zero primary picks.

部署完全由技术栈决定：JS 用 Vercel，Python 用 Railway。传统云提供商获得零主要选择。

**JS Frontend (Next.js + React SPA):**
- Vercel: 100% (86 of 86 picks)

**Python Backend (FastAPI):**
- Railway: 82%
- Docker: 8%
- Fly.io: 5%
- Render: 5%

**Zero primary picks / 零主要选择：**
- AWS (EC2/ECS)
- Google Cloud
- Azure
- Heroku

---

## Where Models Disagree
## 模型分歧之处

All three models agree in 18 of 20 categories within each ecosystem. These 5 categories have genuine within-ecosystem shifts:

所有三个模型在 20 个类别中的 18 个类别内达成一致。以下 5 个类别存在真正的生态系统内转变：

| Category | Sonnet 4.5 | Opus 4.5 | Opus 4.6 |
|----------|------------|----------|----------|
| ORM (JS) | Prisma 79% | Drizzle 60% | Drizzle 100% |
| Jobs (JS) | BullMQ 50% | BullMQ 56% | Inngest 50% |
| Jobs (Python) | Celery 100% | FastAPI BgTasks 38% | FastAPI BgTasks 44% |
| Caching | Redis 71% | Redis 31% | Custom/DIY 32% |
| Real-time | SSE 23% | Custom/DIY 19% | Custom/DIY 20% |

| 类别 | Sonnet 4.5 | Opus 4.5 | Opus 4.6 |
|------|------------|----------|----------|
| ORM (JS) | Prisma 79% | Drizzle 60% | Drizzle 100% |
| 任务 (JS) | BullMQ 50% | BullMQ 56% | Inngest 50% |
| 任务 (Python) | Celery 100% | FastAPI BgTasks 38% | FastAPI BgTasks 44% |
| 缓存 | Redis 71% | Redis 31% | Custom/DIY 32% |
| 实时 | SSE 23% | Custom/DIY 19% | Custom/DIY 20% |

---

## Key Takeaways
## 关键要点

1. **Claude Code prefers building over buying.** In 60% of categories, it recommends custom solutions.

1. **Claude Code 偏好自建而非购买。** 在 60% 的类别中，它推荐自定义解决方案。

2. **When it chooses tools, it chooses decisively.** Near-monopolies exist for GitHub Actions, Stripe, and shadcn/ui.

2. **当它选择工具时，选择非常果断。** GitHub Actions、Stripe 和 shadcn/ui 几乎形成垄断。

3. **Newer models favor newer tools.** Opus 4.6 shows strong preference for modern alternatives (Drizzle over Prisma, Inngest over BullMQ).

3. **较新的模型偏爱较新的工具。** Opus 4.6 对现代替代品表现出强烈偏好（Drizzle 优于 Prisma，Inngest 优于 BullMQ）。

4. **The "default stack" is becoming standardized.** Vercel, PostgreSQL, Drizzle, Tailwind, shadcn/ui, and GitHub Actions dominate recommendations.

4. **"默认技术栈"正在标准化。** Vercel、PostgreSQL、Drizzle、Tailwind、shadcn/ui 和 GitHub Actions 主导推荐。

5. **Traditional cloud providers are invisible.** AWS, GCP, Azure, and Heroku received zero primary picks for deployment.

5. **传统云提供商几乎不可见。** AWS、GCP、Azure 和 Heroku 在部署方面获得零主要选择。

---

*Data collected February 2026. Study by Amplifying.ai.*

*数据收集于 2026 年 2 月。研究由 Amplifying.ai 进行。*
