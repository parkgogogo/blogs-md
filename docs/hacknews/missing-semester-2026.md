# The Missing Semester of Your CS Education – Revised for 2026

**计算机科学教育缺失的学期 —— 2026年修订版**

---

## Meta Information / 元信息

| Field | Value |
|-------|-------|
| **Title** | The Missing Semester of Your CS Education – Revised for 2026 |
| **URL** | https://missing.csail.mit.edu/ |
| **Publisher** | MIT CSAIL (MIT Computer Science and Artificial Intelligence Laboratory) |
| **Instructors** | Anish Athalye, Jon Gjengset, Jose Javier Gonzalez Ortiz |
| **Course Run** | MIT IAP (Independent Activities Period) January 2026 |
| **License** | CC BY-NC-SA 4.0 (Attribution-NonCommercial-ShareAlike) |

**课程信息**

| 字段 | 值 |
|------|-----|
| **标题** | 计算机科学教育缺失的学期 —— 2026年修订版 |
| **网址** | https://missing.csail.mit.edu/ |
| **发布机构** | 麻省理工学院计算机科学与人工智能实验室 (MIT CSAIL) |
| **讲师** | Anish Athalye, Jon Gjengset, Jose Javier Gonzalez Ortiz |
| **课程时间** | 2026年1月 MIT IAP（独立活动期） |
| **许可协议** | CC BY-NC-SA 4.0（署名-非商业性使用-相同方式共享） |

---

## Summary / 摘要

**The Missing Semester of Your CS Education** is a hands-on course from MIT that teaches the practical computing skills rarely covered in traditional CS curricula. While university classes focus on advanced topics like operating systems and machine learning, they typically leave students to figure out essential tooling on their own. This course fills that gap by covering command-line proficiency, text editors, version control, debugging, and modern additions like agentic coding with LLMs.

**《计算机科学教育缺失的学期》**是麻省理工学院开设的一门实践性课程，教授传统计算机科学课程中很少涉及的实用计算技能。虽然大学课程专注于操作系统和机器学习等高级主题，但通常让学生自行摸索必要的工具使用技能。本课程填补了这一空白，涵盖命令行熟练度、文本编辑器、版本控制、调试，以及大语言模型（LLM）辅助编程等现代新增内容。

---

## The Problem / 问题所在

Classes teach you all about advanced topics within CS, from operating systems to machine learning, but there's one critical subject that's rarely covered, and is instead left to students to figure out on their own: proficiency with their tools.

课程会教授计算机科学中的各种高级主题，从操作系统到机器学习，但有一个关键主题却很少被涵盖，而是留给学生自己去摸索：对工具的熟练掌握。

We believe that you can be ten times more productive if you know your tools well, and we want to help you learn how to leverage their full potential.

我们相信，如果你熟练掌握工具，你的效率可以提升十倍，我们希望能帮助你学会如何充分利用这些工具的潜力。

---

## Course Overview / 课程概览

The 2026 edition consists of **nine 1-hour lectures**, each centering on a particular topic. The lectures are largely independent, though as the semester progresses, later lectures presume familiarity with content from earlier sessions.

2026年版包含**九节一小时讲座**，每节聚焦于特定主题。这些讲座在很大程度上是独立的，但随着学期的推进，后面的讲座会假定你已熟悉前面课程的内容。

---

## Lecture Schedule / 讲座安排

### 1/12: Course Overview + Introduction to the Shell
**课程概览 + Shell 入门**

The not-for-credit class consists of nine 1-hour lectures, each one centering on a particular topic. This first lecture introduces the Unix shell — a command-line interface that gives you enormous power and control over your system.

这门不计学分的课程包含九节一小时讲座，每节聚焦于特定主题。第一节讲座介绍 Unix Shell —— 一种命令行界面，能让你对系统拥有巨大的控制力和权力。

> **Key Concepts:** File system navigation, command structure, stdin/stdout/stderr, pipes, redirects
> **关键概念：** 文件系统导航、命令结构、标准输入/输出/错误、管道、重定向

> **Exercise:** Write a command that copies a file to a backup with today's date in the filename (e.g., notes.txt → notes_2026-01-12.txt). Hint: `$(date +%Y-%m-%d)`
> **练习：** 编写一个命令，将文件复制为带今日日期的备份文件名（例如 notes.txt → notes_2026-01-12.txt）。提示：`$(date +%Y-%m-%d)`

---

### 1/13: Command-line Environment
**命令行环境**

Learn about environment variables, dotfiles, terminal multiplexers, remote machines, and advanced shell features.

学习环境变量、点文件（dotfiles）、终端复用器、远程机器以及高级 Shell 特性。

> **Key Concepts:** PATH, environment variables, ssh, tmux, dotfiles management
> **关键概念：** PATH、环境变量、SSH、tmux、点文件管理

---

### 1/14: Development Environment and Tools
**开发环境与工具**

Configure your text editor, IDE, and development workflow for maximum productivity.

配置你的文本编辑器、IDE 和开发工作流，以实现最高效率。

> **Key Concepts:** Vim/Neovim, VS Code, plugin ecosystems, linting, formatting
> **关键概念：** Vim/Neovim、VS Code、插件生态、代码检查（linting）、代码格式化

---

### 1/15: Debugging and Profiling
**调试与性能分析**

Techniques for finding and fixing bugs, plus tools for understanding program performance.

查找和修复 Bug 的技术，以及理解程序性能的工具。

> **Key Concepts:** Print debugging, logging, debuggers (gdb, pdb), profilers, timing
> **关键概念：** 打印调试、日志记录、调试器（gdb、pdb）、性能分析器、计时

---

### 1/16: Version Control and Git
**版本控制与 Git**

Master the essential tool for collaborative software development.

掌握协作软件开发必备工具。

> **Key Concepts:** Git internals, branching, merging, rebasing, remotes, workflows
> **关键概念：** Git 内部原理、分支、合并、变基、远程仓库、工作流

---

### 1/20: Packaging and Shipping Code ⭐ NEW for 2026
**代码打包与发布** ⭐ 2026年新增

The 2026 edition covers several new topics, including packaging and shipping code. Learn how to distribute your software effectively.

2026年版涵盖多个新主题，包括代码打包与发布。学习如何有效分发你的软件。

> **Key Concepts:** Build systems, package managers, containers, deployment
> **关键概念：** 构建系统、包管理器、容器、部署

---

### 1/21: Agentic Coding ⭐ NEW for 2026
**智能体编程** ⭐ 2026年新增

A brand new lecture for 2026 covering AI-assisted programming and agentic coding workflows.

2026年全新讲座，涵盖 AI 辅助编程和智能体编程工作流。

> **Key Concepts:** LLMs as coding assistants, prompt engineering, AI etiquette, agent harnesses, human-in-the-loop
> **关键概念：** 大语言模型作为编程助手、提示词工程、AI 礼仪、智能体框架、人在回路中

**Note:** Fully explaining the inner workings of modern large language models (LLMs) and infrastructure such as agent harnesses is beyond the scope of this course. This lecture focuses on practical usage patterns.

**注意：** 充分解释现代大语言模型（LLM）的内部工作原理以及智能体框架等基础设施超出了本课程的范围。本节讲座侧重于实用使用模式。

---

### 1/22: Beyond the Code ⭐ NEW for 2026
**代码之外** ⭐ 2026年新增

Learn about essential soft skills including documentation, open-source community norms, and AI etiquette.

学习基本软技能，包括文档编写、开源社区规范以及 AI 礼仪。

> **Key Concepts:** Technical writing, READMEs, commit messages, code review, open source contribution, LLM interaction best practices
> **关键概念：** 技术写作、README、提交信息、代码审查、开源贡献、大语言模型交互最佳实践

**Tip:** When working with LLMs, specifically tell the model you'd like a commit message focused on the "why" (and other nuances), and then tell it to query you for missing context. Essentially, you're acting like an MCP "tool" for the coding agent that it can use to "read" context.

**提示：** 与大语言模型协作时，明确告诉模型你希望提交信息侧重于"为什么"（以及其他细微差别），然后让它向你询问缺失的上下文。本质上，你就像是一个 MCP（模型上下文协议）"工具"，供编程智能体用来"读取"上下文。

---

## What's New in 2026 / 2026年新内容

Based on feedback and discussions with the community, the 2026 edition covers several new topics:

根据社区反馈和讨论，2026年版涵盖多个新主题：

1. **Packaging/Shipping Code** — Learn modern software distribution
   **代码打包/发布** — 学习现代软件分发

2. **Code Quality** — Best practices for maintainable software
   **代码质量** — 可维护软件的最佳实践

3. **Agentic Coding** — Working effectively with AI coding assistants
   **智能体编程** — 高效使用 AI 编程助手

4. **Soft Skills** — Documentation, community norms, and professional practices
   **软技能** — 文档编写、社区规范和专业实践

---

## Teaching Philosophy / 教学理念

Lessons dig into practical topics such as environment management, job control, shell pipelines, profiling, and reproducibility, with an emphasis on habits that save time and prevent errors.

课程深入探讨环境管理、作业控制、Shell 管道、性能分析和可重复性等实用主题，强调能够节省时间并预防错误的习惯。

We highly recommend making heavy use of **shellcheck** when writing shell scripts. LLMs are also great at writing and debugging shell scripts, as well as translating them to a "real" programming language (like Python) when they've grown too unwieldy for bash (100+ lines).

我们强烈建议在编写 Shell 脚本时大量使用 **shellcheck**。大语言模型也很擅长编写和调试 Shell 脚本，以及当脚本对于 bash 来说过于复杂（超过100行）时将其翻译成"真正的"编程语言（如 Python）。

---

## Exercises / 练习

Each lecture includes exercises for you to get more familiar with the tools on your own. The hands-on approach is central to the course — you learn by doing.

每节讲座都包含练习，供你自己深入熟悉这些工具。实践方法是本课程的核心 —— 通过实践来学习。

---

## Video Recordings / 视频录像

Lecture videos for the 2026 edition are available on YouTube. We thank Elaine Mello and MIT Open Learning for making it possible for us to record lecture videos. We thank Luis Turino / SIPB for supporting this class as part of SIPB IAP 2026.

2026年版的讲座视频可在 YouTube 上观看。我们感谢 Elaine Mello 和 MIT Open Learning 让我们能够录制讲座视频。我们感谢 Luis Turino / SIPB 将本课程作为 SIPB IAP 2026 的一部分提供支持。

---

## Previous Editions / 历史版本

If you can't wait for the 2026 content, you can also take a look at lectures from previous offerings of the course, which cover many of the same topics:

如果你等不及 2026 年的内容，也可以查看课程之前版本的讲座，它们涵盖了许多相同的主题：

- **2020 Edition** — The original 11-lecture series covering: The Shell, Shell Tools & Scripting, Editors (Vim), Data Wrangling, Command-line Environment, Version Control (Git), Debugging and Profiling, Metaprogramming, Security and Cryptography
  **2020年版** — 原始11讲系列，涵盖：Shell、Shell 工具与脚本、编辑器（Vim）、数据处理、命令行环境、版本控制（Git）、调试与性能分析、元编程、安全与密码学

---

## Community Feedback / 社区反馈

> "It was invaluable for courses such as Operating Systems and Distributed Systems, and it has continued to serve me well in my career. My classmates and coworkers have been impressed with how I use my text editor and command line, and I always reference Missing Semester as the foundation to all those skills."

> "这门课程对操作系统和分布式系统等课程来说非常宝贵，而且在我的职业生涯中一直很有帮助。我的同学和同事对我使用文本编辑器和命令行的方式印象深刻，我总是将《缺失的学期》作为所有这些技能的基础。"

---

## Resources / 资源

- **Course Website:** https://missing.csail.mit.edu/
- **YouTube Channel:** https://www.youtube.com/c/MissingSemester
- **GitHub Repository:** https://github.com/missing-semester/missing-semester
- **Video Editing DSL:** https://github.com/missing-semester/videos (The hacky Python DSL used for multi-camera-angle lecture videos)

---

## For Chinese Developers / 给中文开发者的建议

This course is particularly valuable for:
本课程对以下人群特别有价值：

- **CS students** looking to bridge the gap between academic knowledge and industry practices
  **计算机科学学生** — 希望弥合学术知识与行业实践之间的差距

- **Frontend developers** wanting to improve their terminal and Git workflows
  **前端开发者** — 希望改进终端和 Git 工作流

- **AI/ML engineers** interested in agentic coding with LLMs
  **AI/ML 工程师** — 对大语言模型智能体编程感兴趣

- **Self-taught programmers** seeking structured learning of essential tooling
  **自学程序员** — 寻求结构化的基本工具学习

---

## Technical Terms Glossary / 技术术语表

| English | 中文 | Description |
|---------|------|-------------|
| Shell | Shell / 命令行解释器 | Command-line interface for interacting with the operating system |
| Version Control | 版本控制 | System for tracking changes in code (e.g., Git) |
| Dotfiles | 点文件 / 配置文件 | Hidden configuration files (starting with .) in Unix systems |
| Terminal Multiplexer | 终端复用器 | Tool like tmux for managing multiple terminal sessions |
| Linting | 代码检查 / 静态分析 | Automated checking of code for errors/style issues |
| Profiling | 性能分析 | Measuring program performance and resource usage |
| Rebasing | 变基 | Git operation to move or combine commits |
| Agentic Coding | 智能体编程 | Using AI agents to assist with coding tasks |
| LLM | 大语言模型 | Large Language Model (e.g., GPT, Claude) |
| MCP | 模型上下文协议 | Model Context Protocol for AI tool integration |
| Prompt Engineering | 提示词工程 | Crafting effective inputs for AI models |
| Human-in-the-loop | 人在回路中 | Keeping human oversight in automated processes |

---

*Translation compiled from official MIT Missing Semester course materials.*
*翻译整理自 MIT Missing Semester 官方课程材料。*

*Original content licensed under CC BY-NC-SA 4.0*
*原始内容采用 CC BY-NC-SA 4.0 许可协议*
