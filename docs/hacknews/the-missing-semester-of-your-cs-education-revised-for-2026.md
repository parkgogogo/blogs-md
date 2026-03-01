---
title: "The Missing Semester of Your CS Education – Revised for 2026"
url: "https://missing.csail.mit.edu/"
rating: 10
category: "Computer Science Education"
date: "2026-02-28"
---

# The Missing Semester of Your CS Education – Revised for 2026

## IAP 2026

Classes teach you all about advanced topics within CS, from operating systems to machine learning, but there's one critical subject that's rarely covered, and is instead left to students to figure out on their own: proficiency with their tools. We'll teach you how to master the command-line, use a powerful text editor, use fancy features of version control systems, and much more!

Students spend hundreds of hours using these tools over the course of their education (and thousands over their career), so it makes sense to make the experience as fluid and frictionless as possible. Mastering these tools not only enables you to spend less time on figuring out how to bend your tools to your will, but it also lets you solve problems that would previously seem impossibly complex.

These days, many aspects of software engineering are also in flux through the introduction of AI-enabled and AI-enhanced tools and workflows. When used appropriately and with awareness of their shortcomings, these can often provide significant benefits to CS practitioners and are thus worth developing working knowledge of. Since AI is a cross-functional enabling technology, there is not a standalone AI lecture; we've instead folded the use of the latest applicable AI tools and techniques into each lecture directly.

## Why We Are Teaching This Class

During a traditional Computer Science education, chances are you will take plenty of classes that teach you advanced topics within CS, everything from Operating Systems to Programming Languages to Machine Learning. But at many institutions there is one essential topic that is rarely covered and is instead left for students to pick up on their own: computing ecosystem literacy.

Over the years, we have helped teach several classes at MIT, and over and over we have seen that many students have limited knowledge of the tools available to them. Computers were built to automate manual tasks, yet students often perform repetitive tasks by hand or fail to take full advantage of powerful tools such as version control and text editors. In the best case, this results in inefficiencies and wasted time; in the worst case, it results in issues like data loss or inability to complete certain tasks.

These topics are not taught as part of the university curriculum: students are never shown how to use these tools, or at least not how to use them efficiently, and thus waste time and effort on tasks that should be simple. The standard CS curriculum is missing critical topics about the computing ecosystem that could make students' lives significantly easier.

To help remedy this, we created a class that covers all the topics we consider crucial to be an effective computer scientist and programmer. The class is pragmatic and practical, and it provides hands-on introduction to tools and techniques that you can immediately apply in a wide variety of situations you will encounter. The latest iteration of this class, with substantially revised material, is being run during MIT's "Independent Activities Period" in January 2026 — a one-month semester that features shorter student-run classes.

## Course Schedule

**1/12/26**: Course Overview + Introduction to the Shell  
**1/13/26**: Command-line Environment  
**1/14/26**: Development Environment and Tools  
**1/15/26**: Debugging and Profiling  
**1/16/26**: Version Control and Git  
**1/20/26**: Packaging and Shipping Code  
**1/21/26**: Agentic Coding  
**1/22/26**: Beyond the Code  
**1/23/26**: Code Quality  

## What You'll Learn

### Command Shell
How to automate common and repetitive tasks with aliases, scripts, and build systems. No more copy-pasting commands from a text document. No more "run these 15 commands one after the other". No more "you forgot to run this thing" or "you forgot to pass this argument".

For example, searching through your history quickly can be a huge time saver. The course demonstrates several tricks related to navigating your shell history.

### Version Control
How to use version control *properly*, and take advantage of it to save you from disaster, collaborate with others, and quickly find and isolate problematic changes. No more `rm -rf; git clone`. No more merge conflicts (well, fewer of them at least). No more huge blocks of commented-out code. No more fretting over how to find what broke your code. No more "oh no, did we delete the working code?!". The course even teaches you how to contribute to other people's projects with pull requests!

The course demonstrates using `git bisect` to find which commit broke a unit test and then fixing it with `git revert`.

### Text Editing
How to efficiently edit files from the command-line, both locally and remotely, and take advantage of advanced editor features. No more copying files back and forth. No more repetitive file editing.

Vim macros are one of its best features — the course shows how to quickly convert an HTML table to CSV format using a nested vim macro.

### Remote Machines
How to stay sane when working with remote machines using SSH keys and terminal multiplexing. No more keeping many terminals open just to run two commands at once. No more typing your password every time you connect. No more losing everything just because your Internet disconnected or you had to reboot your laptop.

The course demonstrates using `tmux` to keep sessions alive in remote servers and `mosh` to support network roaming and disconnection.

### Finding Files
How to quickly find files that you are looking for. No more clicking through files in your project until you find the one that has the code you want.

The course shows how to quickly look for files with `fd` and for code snippets with `rg` (ripgrep). It also demonstrates quickly navigating to recent/frequent files/folders using `fasd`.

### Data Wrangling
How to quickly and easily modify, view, parse, plot, and compute over data and files directly from the command-line. No more copy pasting from log files. No more manually computing statistics over data. No more spreadsheet plotting.

### Code Quality and Continuous Integration
How to use autoformatting, linting, testing, and code coverage tools to improve code quality. No more ugly code. No more regressions. No more code that works on your computer but crashes on everyone else's.

### Beyond the Code
How to write great documentation, communicate clearly with open-source maintainers, submit actionable issues, and contribute pull requests that get merged. No more confused users who can't get started using your software. No more ghosting from maintainers.

## About the Class

**Staff**: This class is co-taught by Anish, Jon, and Jose.  
**Questions**: Email missing-semester@mit.edu

You can view lecture videos on YouTube. The course materials are available to the public, including video recordings of lectures.

The course has been shared beyond MIT in the hopes that others may benefit from these resources. It has been discussed on Hacker News, Lobsters, Reddit, X, Bluesky, Mastodon, LinkedIn, and YouTube.

## Translations

The course has been translated into 17 languages including Arabic, Bengali, Chinese (Simplified), Chinese (Traditional), German, Italian, Japanese, Kannada, Korean, Persian, Portuguese, Russian, Serbian, Spanish, Thai, Turkish, and Vietnamese.

The source code is available on GitHub and licensed under CC BY-NC-SA.

---

# 中文翻译

# 计算机科学教育中缺失的一学期 —— 2026修订版

## 2026年麻省理工独立活动期 (IAP 2026)

计算机科学课程教授从操作系统到机器学习等各种高级主题，但有一个关键课题却很少被涵盖，而是留给学生自己去摸索：对工具的熟练运用。我们将教你如何掌握命令行、使用强大的文本编辑器、利用版本控制系统的各种高级功能，以及更多实用技能！

学生在整个教育过程中要花数百小时使用这些工具（职业生涯中更是数千小时），因此让这些工具的使用变得流畅无阻是非常有意义的。掌握这些工具不仅能让你减少琢磨如何让工具听话的时间，还能让你解决以前看似不可能解决的复杂问题。

如今，随着AI驱动和AI增强工具及工作流的引入，软件工程的许多方面也在发生变化。如果恰当使用并了解其局限性，这些工具往往能为计算机科学从业者带来显著收益，因此值得培养相关的工作知识。由于AI是一项跨功能的使能技术，课程没有设置独立的AI讲座，而是将最新的适用AI工具和技术直接融入到每一讲中。

## 我们为什么要开设这门课

在传统的计算机科学教育中，你可能会学习大量高级课程，涵盖从操作系统到编程语言再到机器学习等各种主题。但在许多院校，有一个基本课题却很少被讲授，而是留给学生自己去摸索：计算生态系统素养。

多年来，我们在麻省理工协助教授多门课程，一次又一次地看到许多学生对可用工具的了解非常有限。计算机的出现是为了自动化人工任务，但学生们往往亲手执行重复性任务，或者未能充分利用版本控制、文本编辑器等强大工具。在最好的情况下，这会导致效率低下和时间浪费；在最坏的情况下，会导致数据丢失或无法完成某些任务。

这些主题不是大学课程的一部分：学生们从未被教授如何使用这些工具，或者至少没有被教授如何高效使用，因此在本应简单的任务上浪费时间和精力。标准的计算机科学课程缺少关于计算生态系统的关键主题，而这些本可以让学生的日子轻松得多。

为了帮助解决这一问题，我们创建了一门课程，涵盖我们认为成为高效计算机科学家和程序员所必需的所有主题。这门课程务实且实用，提供工具和技术的实践入门，你可以在各种情况下立即应用。这门课程的最新版本（经过大幅修订的内容）于2026年1月在麻省理工的"独立活动期"开设——这是一个为期一个月的学期，由学生主导开设较短的课程。

## 课程安排

**1月12日**：课程概览 + Shell 入门  
**1月13日**：命令行环境  
**1月14日**：开发环境与工具  
**1月15日**：调试与性能分析  
**1月16日**：版本控制与 Git  
**1月20日**：代码打包与发布  
**1月21日**：智能体编程 (Agentic Coding)  
**1月22日**：代码之外  
**1月23日**：代码质量  

## 你将学到什么

### 命令行 Shell
如何使用别名、脚本和构建系统自动化常见和重复的任务。再也不用从文本文档中复制粘贴命令。再也不用"一个接一个地运行这15条命令"。再也不用"你忘了运行这个东西"或"你忘了传这个参数"。

例如，快速搜索历史记录可以节省大量时间。课程演示了多种与 Shell 历史记录导航相关的技巧。

### 版本控制
如何*正确*使用版本控制，并利用它来避免灾难、与他人协作、快速查找和隔离有问题的更改。再也不用 `rm -rf; git clone`。再也不用处理合并冲突（好吧，至少少了很多）。再也不用保留大段注释掉的代码。再也不用纠结如何找出是什么破坏了代码。再也不用"哦不，我们把能用的代码删了吗？！"。课程甚至教你如何向他人的项目提交拉取请求 (Pull Request)！

课程演示了如何使用 `git bisect` 找出哪个提交破坏了单元测试，然后使用 `git revert` 修复它。

### 文本编辑
如何高效地从命令行编辑文件，无论是在本地还是远程，并利用编辑器的高级功能。再也不用来回复制文件。再也不用重复编辑文件。

Vim 宏是其最佳功能之一——课程展示了如何使用嵌套的 vim 宏快速将 HTML 表格转换为 CSV 格式。

### 远程机器
如何使用 SSH 密钥和终端多路复用 (terminal multiplexing) 在远程机器上工作时保持理智。再也不用打开多个终端只是为了同时运行两条命令。再也不用每次连接时输入密码。再也不用在互联网断开或重启笔记本时丢失所有工作。

课程演示了如何使用 `tmux` 保持远程服务器上的会话，以及使用 `mosh` 支持网络漫游和断开连接。

### 查找文件
如何快速找到你要找的文件。再也不用点击浏览项目中的文件，直到找到包含你想要的代码的那个。

课程展示了如何使用 `fd` 快速查找文件，使用 `rg` (ripgrep) 查找代码片段。还演示了如何使用 `fasd` 快速跳转到最近/常用的文件/文件夹。

### 数据处理 (Data Wrangling)
如何快速轻松地直接从命令行修改、查看、解析、绘制图表和计算数据及文件。再也不用从日志文件中复制粘贴。再也不用手动计算数据统计。再也不用用电子表格绘图。

### 代码质量与持续集成
如何使用自动格式化、代码检查 (linting)、测试和代码覆盖率工具来提高代码质量。再也不用写丑陋的代码。再也不用出现回归问题。再也不用出现在你电脑上能用但在别人电脑上崩溃的代码。

### 代码之外
如何编写优秀的文档、与开源维护者清晰沟通、提交可操作的问题报告，以及提交能被合并的拉取请求。再也不会有困惑的用户无法开始使用你的软件。再也不会被维护者无视。

## 关于本课程

**讲师**：本课程由 Anish、Jon 和 Jose 共同教授。  
**问题咨询**：missing-semester@mit.edu

你可以在 YouTube 上观看讲座视频。课程资料向公众开放，包括讲座的视频录像。

这门课程已分享到麻省理工之外，希望其他人也能从这些资源中受益。它已在 Hacker News、Lobsters、Reddit、X、Bluesky、Mastodon、LinkedIn 和 YouTube 上被广泛讨论。

## 翻译版本

本课程已被翻译成17种语言，包括阿拉伯语、孟加拉语、简体中文、繁体中文、德语、意大利语、日语、卡纳达语、韩语、波斯语、葡萄牙语、俄语、塞尔维亚语、西班牙语、泰语、土耳其语和越南语。

源代码可在 GitHub 上获取，采用 CC BY-NC-SA 许可证。
