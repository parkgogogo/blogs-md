---
title: "BuildKit: Docker's Hidden Gem That Can Build Almost Anything"
url: "https://tuananh.net/2026/02/25/buildkit-docker-hidden-gem/"
rating: 9
category: "DevOps/Containers"
date: "2026-02-28"
---

# BuildKit: Docker's Hidden Gem That Can Build Almost Anything

[Discussion on Hacker News](https://news.ycombinator.com/item?id=47166264)

Most people interact with BuildKit every day without realizing it. When you run `docker build`, BuildKit is the engine behind it. But reducing BuildKit to "the thing that builds Dockerfiles" is like calling LLVM "the thing that compiles C." It undersells the architecture by an order of magnitude.

BuildKit is a general-purpose, pluggable build framework. It can produce OCI images, yes, but also tarballs, local directories, APK packages, RPMs, or anything else you can describe as a directed acyclic graph of filesystem operations. The Dockerfile is just one frontend. You can write your own.

## The architecture

BuildKit's design is clean and surprisingly understandable once you see the layers. There are three key concepts.

### LLB: the intermediate representation

At the heart of BuildKit is **LLB** (Low-Level Build definition). Think of it as the LLVM IR of build systems. LLB is a binary protocol (protobuf) that describes a DAG of filesystem operations: run a command, copy files, mount a filesystem. It's content-addressable, which means identical operations produce identical hashes, enabling aggressive caching.

When you write a Dockerfile, the Dockerfile frontend parses it and emits LLB. But nothing in BuildKit requires that the input be a Dockerfile. Any program that can produce valid LLB can drive BuildKit.

### Frontends: bring your own syntax

A **frontend** is a container image that BuildKit runs to convert your build definition (Dockerfile, YAML, JSON, HCL, whatever) into LLB. The frontend receives the build context and the build file through the BuildKit Gateway API, and returns a serialized LLB graph.

This is the key insight: the build language is not baked into BuildKit. It's a pluggable layer. You can write a frontend that reads a YAML spec, a TOML config, or a custom DSL, and BuildKit will execute it the same way it executes Dockerfiles.

You've actually seen this mechanism before. The `# syntax=` directive at the top of a Dockerfile tells BuildKit which frontend image to use. `# syntax=docker/dockerfile:1` is just the default. You can point it at any image.

### Solver and cache: content-addressable execution

The **solver** takes the LLB graph and executes it. Each vertex in the DAG is content-addressed, so if you've already built a particular step with the same inputs, BuildKit skips it entirely. This is why BuildKit is fast: it doesn't just cache layers linearly like the old Docker builder. It caches at the operation level across the entire graph, and it can execute independent branches in parallel.

The cache can be local, inline (embedded in the image), or remote (a registry). This makes BuildKit builds reproducible and shareable across CI runners.

## Not just images

BuildKit's `--output` flag is where this gets practical. You can tell BuildKit to export the result as:

- `type=image` — push to a registry (the default for `docker build`)
- `type=local,dest=./out` — dump the final filesystem to a local directory
- `type=tar,dest=./out.tar` — export as a tarball
- `type=oci` — export as an OCI image tarball

The `type=local` output is the most interesting for non-image use cases. Your build can produce compiled binaries, packages, documentation, or anything else, and BuildKit will dump the result to disk. No container image required.

Projects like [Earthly](https://earthly.dev), [Dagger](https://dagger.io), and [Depot](https://depot.dev) are all built on top of BuildKit's LLB. It's a proven pattern.

## Building APK packages with a custom frontend

To demonstrate this concretely, I built [apkbuild](https://github.com/tuananh/apkbuild): a custom BuildKit frontend that reads a YAML spec and produces Alpine APK packages. No Dockerfile involved. The entire build pipeline — from source compilation to APK packaging — runs inside BuildKit using LLB operations. Think of this like a dummy version of [Chainguard's melange](https://github.com/chainguard-dev/melange)

I chose YAML for familiarity, but the spec could be anything you want (JSON, TOML, a custom DSL) as long as your frontend can parse it.

My package YAML spec looks like this:

```yaml
name: hello
version: "1.0.0"
epoch: "0"
url: https://example.com/hello
license: MIT
description: Minimal CMake APK demo

sources:
  app:
    context: {}

build:
  source_dir: hello
```

That's it. No Dockerfile. BuildKit reads this spec through the custom frontend and produces a `.apk` file.

### Running it

Build the frontend image:

```shell
docker build -t tuananh/apkbuild -f Dockerfile .
```

Then use it to build an APK package:

```shell
cd example
docker buildx build \
  -f spec.yml \
  --build-arg BUILDKIT_SYNTAX=tuananh/apkbuild \
  --output type=local,dest=./out \
  .
```

You should be able to see the APK package in the `out` folder like below

`BUILDKIT_SYNTAX` tells BuildKit to use our custom frontend instead of the default Dockerfile parser. The `--output type=local` dumps the resulting `.apk` files to `./out`. No image is created. No registry is involved.

## Why this matters

BuildKit gives you a content-addressable, parallelized, cached build engine for free. You don't need to reinvent caching, parallelism, or reproducibility. You write a frontend that translates your spec into LLB, and BuildKit handles the rest.

This is relevant beyond toy demos. Dagger uses LLB as its execution engine for CI/CD pipelines. Earthly compiles Earthfiles into LLB. The pattern is proven at scale.

If you're building a tool that needs to compile code, produce artifacts, or orchestrate multi-step builds, consider BuildKit as your execution backend. The Dockerfile is just the default frontend. The real power is in the engine underneath.

---

# 中文翻译

# BuildKit：Docker 隐藏的宝石，几乎可以构建任何东西

[Hacker News 讨论](https://news.ycombinator.com/item?id=47166264)

大多数人每天都在与 BuildKit 交互，却没有意识到它的存在。当你运行 `docker build` 时，BuildKit 就是背后的引擎。但将 BuildKit 简化为"构建 Dockerfile 的工具"，就像把 LLVM 叫做"编译 C 语言的东西"一样——这大大低估了它的架构能力，至少低估了一个数量级。

BuildKit 是一个通用的、可插拔的构建框架。是的，它可以生成 OCI 镜像，但也可以生成 tar 压缩包、本地目录、APK 包、RPM 包，或者任何你能描述为文件系统操作有向无环图（DAG）的东西。Dockerfile 只是众多前端中的一种，你完全可以编写自己的前端。

## 架构设计

一旦你理解了各个层次，BuildKit 的设计是清晰且出人意料地易于理解的。有三个核心概念：

### LLB：中间表示层

BuildKit 的核心是 **LLB**（Low-Level Build definition，低级构建定义）。把它想象成构建系统中的 LLVM IR。LLB 是一个二进制协议（protobuf），描述了文件系统操作的 DAG：运行命令、复制文件、挂载文件系统。它是内容可寻址的，这意味着相同的操作会产生相同的哈希值，从而实现激进的缓存策略。

当你编写 Dockerfile 时，Dockerfile 前端会解析它并生成 LLB。但 BuildKit 并不强制要求输入必须是 Dockerfile。任何能够生成有效 LLB 的程序都可以驱动 BuildKit。

### 前端：自带语法

**前端**（frontend）是一个容器镜像，BuildKit 运行它来将你的构建定义（Dockerfile、YAML、JSON、HCL 等）转换为 LLB。前端通过 BuildKit Gateway API 接收构建上下文和构建文件，并返回一个序列化的 LLB 图。

这是关键的洞察：构建语言并不是硬编码在 BuildKit 中的，它是一个可插拔的层。你可以编写一个读取 YAML 规范、TOML 配置或自定义 DSL 的前端，BuildKit 会以执行 Dockerfile 相同的方式来执行它。

你实际上之前已经见过这种机制。Dockerfile 顶部的 `# syntax=` 指令告诉 BuildKit 使用哪个前端镜像。`# syntax=docker/dockerfile:1` 只是默认值，你可以将其指向任何镜像。

### 求解器和缓存：内容可寻址执行

**求解器**（solver）接收 LLB 图并执行它。DAG 中的每个顶点都是内容可寻址的，所以如果你已经用相同的输入构建过某个步骤，BuildKit 会完全跳过它。这就是 BuildKit 快的原因：它不像旧的 Docker 构建器那样只是线性缓存层，而是在整个图的操层面进行缓存，并且可以并行执行独立的分支。

缓存可以是本地的、内联的（嵌入在镜像中）或远程的（注册表）。这使得 BuildKit 的构建是可重现的，并且可以在 CI 运行器之间共享。

## 不仅仅是镜像

BuildKit 的 `--output` 标志是让这一切变得实用的地方。你可以告诉 BuildKit 将结果导出为：

- `type=image` —— 推送到注册表（`docker build` 的默认值）
- `type=local,dest=./out` —— 将最终文件系统转储到本地目录
- `type=tar,dest=./out.tar` —— 导出为 tar 压缩包
- `type=oci` —— 导出为 OCI 镜像 tar 包

对于非镜像用例来说，`type=local` 输出是最有趣的。你的构建可以生成编译后的二进制文件、软件包、文档或其他任何东西，BuildKit 会将结果转储到磁盘。不需要容器镜像。

[Earthly](https://earthly.dev)、[Dagger](https://dagger.io) 和 [Depot](https://depot.dev) 等项目都是基于 BuildKit 的 LLB 构建的。这是一个经过验证的模式。

## 使用自定义前端构建 APK 包

为了具体演示这一点，我构建了 [apkbuild](https://github.com/tuananh/apkbuild)：一个自定义的 BuildKit 前端，它读取 YAML 规范并生成 Alpine APK 包。完全不涉及 Dockerfile。整个构建管道——从源代码编译到 APK 打包——都在 BuildKit 内部使用 LLB 操作运行。可以把它看作 [Chainguard 的 melange](https://github.com/chainguard-dev/melange) 的一个简化版本。

我选择 YAML 是为了熟悉度，但规范可以是任何你想要的格式（JSON、TOML、自定义 DSL），只要你的前端能够解析它。

我的包 YAML 规范看起来像这样：

```yaml
name: hello
version: "1.0.0"
epoch: "0"
url: https://example.com/hello
license: MIT
description: Minimal CMake APK demo

sources:
  app:
    context: {}

build:
  source_dir: hello
```

就是这样。没有 Dockerfile。BuildKit 通过自定义前端读取这个规范并生成 `.apk` 文件。

### 运行它

构建前端镜像：

```shell
docker build -t tuananh/apkbuild -f Dockerfile .
```

然后使用它来构建 APK 包：

```shell
cd example
docker buildx build \
  -f spec.yml \
  --build-arg BUILDKIT_SYNTAX=tuananh/apkbuild \
  --output type=local,dest=./out \
  .
```

你应该能在 `out` 文件夹中看到 APK 包，如下所示

`BUILDKIT_SYNTAX` 告诉 BuildKit 使用我们的自定义前端而不是默认的 Dockerfile 解析器。`--output type=local` 将生成的 `.apk` 文件转储到 `./out`。不创建镜像，不涉及注册表。

## 为什么这很重要

BuildKit 免费为你提供了一个内容可寻址、并行化、带缓存的构建引擎。你不需要重新发明缓存、并行性或可重现性。你编写一个将规范翻译成 LLB 的前端，BuildKit 会处理其余的事情。

这不仅仅适用于玩具演示。Dagger 使用 LLB 作为其 CI/CD 管道的执行引擎。Earthly 将 Earthfiles 编译成 LLB。这种模式已经在规模上得到了验证。

如果你正在构建一个需要编译代码、生成产物或编排多步骤构建的工具，请考虑将 BuildKit 作为你的执行后端。Dockerfile 只是默认的前端，真正的力量在于底层的引擎。
