Title: 包管理器仓库可以向 OCI 借鉴什么
URL: https://nesbitt.io/2026/02/18/what-package-registries-could-borrow-from-oci.html
Body:

每个包管理器都以归档文件的形式分发代码，但每个都有自己的一套做法。npm 将 tar 包包裹在一个 package/ 目录前缀下。RubyGems 在未压缩的 tar 内部嵌套 gzip 文件。Alpine 将三个 gzip 流拼接在一起，称之为一个包。Python 在二十年内经历了四种分发格式。RPM 在 2025 年之前近三十年都使用 cpio 作为其负载格式，才最终弃用。

与此同时，容器世界已经收敛于单一格式：OCI，即开放容器倡议规范。在过去几年里，OCI 仓库已经开始悄悄存储那些根本不是容器的东西：Helm 图表、Homebrew 二进制包、WebAssembly 模块、AI 模型。该格式最初是为容器镜像设计的，但其底层原语的通用性足以让我们思考：是否每个包管理器都可以使用 OCI 进行分发？

### OCI 究竟是什么

OCI 定义了三项规范：运行时规范（如何运行容器）、镜像规范（如何描述容器内容），以及分发规范（如何从仓库推送和拉取）。

在存储层面，OCI 仓库处理两种原语：清单（manifests）和 Blob。清单是一份引用一个或多个 Blob 的 JSON 文档，通过它们的 SHA-256 摘要来标识。Blob 是不透明的二进制内容块，而标签（tags）是指向清单的人类可读的名称。

容器镜像清单看起来像这样：

{
 "schemaVersion": 2,
 "mediaType": "application/vnd.oci.image.manifest.v1+json",
 "config": {
 "mediaType": "application/vnd.oci.image.config.v1+json",
 "digest": "sha256:abc123...",
 "size": 1234
 },
 "layers": [
 {
 "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
 "digest": "sha256:def456...",
 "size": 56789
 }
 ]
}

配置 Blob 保存元数据（什么操作系统、什么架构、什么环境变量）。每个层 Blob 保存文件系统变更的 tar 包。仓库不关心 Blob 内部是什么，只关心每个 Blob 都通过其摘要进行标识和验证。

2024 年 2 月的 [v1.1 更新](https://opencontainers.org/posts/blog/2024-03-13-image-and-distribution-1-1/) 添加了 artifactType，用于声明清单描述的是什么类型的东西，这样仓库就能区分 Helm 图表、容器镜像和 Homebrew 二进制包；还添加了 subject，让一个制品可以引用另一个制品，这就是签名和 SBOM（软件物料清单）如何附加到它们所描述的东西上的。在 1.1 之前，人们通过在配置 Blob 上设置自定义媒体类型来存储非容器制品，这虽然可行，但仓库有时会拒绝或错误处理结果。

要推送一个制品，你先将每个 Blob 上传（到 /v2/<name>/blobs/uploads/），然后推送一个清单，通过摘要和大小引用这些 Blob。要拉取，则先获取清单，读取摘要，然后下载 Blob。因为所有内容都通过摘要寻址，即使多个制品引用同一个 Blob，仓库也只会存储一份副本。

### 为什么选择 OCI 而不是专门构建的方案

该格式本身带有大量容器特定的仪式，但每个主流云提供商都已经运行着符合 OCI 标准的仓库：GitHub Container Registry、Amazon ECR、Azure Container Registry、Google Artifact Registry。Harbor 和 Zot 等自托管方案也很成熟。认证、访问控制、复制和由 CDN 支持的 Blob 存储都已经存在，因为容器仓库已经在大规模上解决了这些问题，而基于 OCI 构建的包管理器仓库无需重新实现任何这些功能就能继承全部能力。

[ORAS](https://oras.land/)（OCI Registry As Storage）是一个 CNCF 项目，它将多步骤的 OCI 上传过程抽象为简单的命令：

oras push registry.example.com/mypackage:1.0.0 \
 package.tar.gz:application/vnd.example.package.v1.tar+gzip

这会将文件作为 Blob 上传，创建一个引用它的清单，并为其打上标签。Helm、Flux、Crossplane 以及 Sigstore 签名工具都使用 ORAS 或底层的 OCI 客户端库。

### 当今包管理器分发什么

这里没有一个单独的选择是错误的，但十七个不同的答案指向同一个基本问题，这表明归档格式从来就不是任何人认真思考过的部分。

| 生态系统 | 格式 | 内部包含什么 |
|---------|------|-------------|
| npm | .tgz (gzip tar) | 文件位于 package/ 前缀下 |
| PyPI | .whl (zip) 或 .tar.gz | Wheel：预构建文件 + .dist-info。Sdist：源码 + PKG-INFO |
| RubyGems | .gem (gzip 压缩文件的 tar) | metadata.gz + data.tar.gz + checksums.yaml.gz |
| Maven | .jar (zip) | 编译后的 .class 文件 + META-INF/MANIFEST.MF |
| Cargo | .crate (gzip tar) | 源码 + Cargo.toml + Cargo.lock |
| NuGet | .nupkg (zip) | DLL 程序集 + .nuspec XML 元数据 |
| Homebrew | .bottle.tar.gz | 安装在前缀下的编译二进制文件 |
| Go | .zip | 位于 module@version/ 路径前缀下的源码 |
| Hex | 外层 tar 包含内层文件 | VERSION + metadata.config + contents.tar.gz + CHECKSUM |
| Debian | .deb (ar 归档) | debian-binary + control.tar.* + data.tar.* |
| RPM | 自定义二进制格式 | 头部区块 + cpio 负载 (v4) 或自定义格式 (v6) |
| Alpine | 拼接的 gzip 流 | 签名 + 控制 tar + 数据 tar |
| Conda | .conda (zstd tar 的 zip) 或 .tar.bz2 | info/ 元数据 + 包内容 |
| Dart/pub | .tar.gz | 源码 + pubspec.yaml |
| Swift PM | .zip | 源码归档 |
| CPAN | .tar.gz | .pm 文件 + Makefile.PL + META.yml + MANIFEST |
| CocoaPods | 无归档格式 | .podspec 指向源码 URL |

### 那些奇怪的家伙

RubyGems 将压缩嵌套在归档内部，而不是反过来。一个 .gem 是一个未压缩的 tar，包含单独 gzip 压缩的文件。因此外层归档不提供压缩，每个组件都单独压缩。这意味着你可以在不解压数据的情况下提取元数据，这是一个合理的优化，但该格式第一眼看起来很奇怪，因为 Unix 世界其他所有东西都习惯把 gzip 放在外面。

Alpine APK 滥用了 gzip 规范的一个特性。gzip 格式允许将多个流拼接成单个文件，技术上任何符合标准的解压器都应该能处理它。Alpine 包是三个独立的 gzip 流（签名、控制、数据）拼接成一个文件。由于 gzip 不提供关于一个流在哪里结束、下一个流在哪里开始的元数据，你必须完全解压每个段才能找到边界。APK 包内的内核模块通常已经是 gzip 压缩的，所以你得到的是 gzip 套在 tar 套在 gzip 里。

RPM 从 1995 年到 2025 年 9 月 RPM v6 发布，一直使用 cpio 作为其负载格式。cpio 格式的头部字段中有一个 4GB 的文件大小限制。三十年来，没有一个 RPM 包能包含大于 4GB 的文件。RPM v6 最终弃用 cpio，改用自定义格式。

Debian 故意选择了 1970 年代的 ar 归档格式。理由很实际：解压工具（ar、tar、gzip）在几乎每个 Unix 系统上都可用，即使在最小化的救援环境中也是如此。你可以只用 POSIX 工具解压 .deb。这可能是这个列表中最有意的格式选择。

cocoapods 的 package/ 前缀意味着每个 tar 包将其内容包裹在一个 package/ 目录中，安装时会被剥离。这会导致 tarball 内部相对 file: 依赖的问题，因为 npm 试图相对于 tar 包而不是解压后的目录来解析路径。

Python 经历了四种分发格式。带 setup.py 的源码 tar 包（1990 年代）、eggs（2004 年，受 Java JAR 启发，可以在压缩状态下直接导入）、sdists（标准化的 tar.gz），以及最终的 wheels（2012 年）。Eggs 存活了十九年，直到 PyPI 在 2023 年 8 月停止接受它们。Wheel 格式将 Python 版本、ABI 标签和平台标签编码在文件名中，这比大多数生态系统放在文件名中的元数据要多，但比清单中的元数据要少。

Conda 多年来维护了两种不兼容的格式。传统的 .tar.bz2 和现代的 .conda（一个包含 zstandard 压缩 tar 的 zip）。从 bzip2 切换到 zstandard 带来了显著的解压速度提升，但生态系统中的每个工具都必须无限期地支持这两种格式。

Hex（Erlang/Elixir）在同一个包中有两种校验和方案。已弃用的"内部校验和"对拼接的文件内容进行哈希。当前的"外部校验和"对整个 tar 包进行哈希。两者都出于向后兼容性而存在。

### 谁已经在使用 OCI

Homebrew 是一个传统的包管理器，不是"云原生"工具，而它在压力下的迁移已经发生。

2021 年 2 月，JFrog [宣布](https://jfrog.com/blog/into-the-sunset-bintray-jcenter-gocenter-and-chartcenter/) Bintray 将于 5 月 1 日关闭。Homebrew 的二进制包托管在 Bintray 上。维护者们有大约三个月的时间将整个预编译二进制文件归档迁移到其他地方，他们最终选择了 GitHub Packages，它将所有内容作为 OCI Blob 存储在 ghcr.io 上。[Homebrew 3.1.0](https://brew.sh/2021/04/12/homebrew-3.1.0/) 于 2021 年 4 月 12 日发布，将 GHCR 作为默认下载位置。

过渡过程出现了预期中的困难。整个行业的 CI 流水线崩溃，因为 [CircleCI](https://discuss.circleci.com/t/macos-image-users-homebrew-brownout-2021-04-26/39872) 等服务上的 macOS 镜像附带了仍然指向 Bintray 的旧版本 Homebrew。在 4 月 26 日的计划中断期间，任何运行旧版本 Homebrew 的系统都会收到 502 错误。旧版本的二进制包从未被迁移，所以任何固定到旧 formula 版本的人都会收到 404 错误，不得不从源码构建。解决方法是 brew update，但 CI 环境缓存了旧版本 Homebrew 且不会自动更新。

尘埃落定后，基于 OCI 的存储实现了在 Bintray 上不切实际的功能。Homebrew 4.0.0（2023 年 2 月）从 git 克隆的 tap 元数据切换到 [JSON API](https://brew.sh/2023/02/16/homebrew-4.0.0/)，该 API 利用结构化的 OCI 清单，brew update 从每 5 分钟运行一次降到每 24 小时运行一次。

基于清单的完整性检查取代了旧的校验和方法，尽管这引入了 [一类新的 bug](https://github.com/Homebrew/brew/issues/12300)，即清单校验和不匹配。平台多路复用自然来自 OCI 镜像索引，它将平台变体（arm64_sonoma、x86_64_linux）映射到各个清单，而无需 Homebrew 自己构建该逻辑。

当你运行 brew install 时，客户端从 ghcr.io/v2/homebrew/core/<formula>/manifests/<version> 获取 OCI 镜像索引清单，选择正确的平台清单，然后 HEAD 请求 Blob URL 以获得一个 307 重定向到 pkg-containers.githubusercontent.com 上的签名 URL，Fastly 的 CDN 从该 URL 提供实际字节。GHCR 即使是公共镜像也需要 bearer 令牌，所以 Homebrew 将 QQ== 硬编码为 bearer 令牌。Blob 内部的二进制包仍然是 gzip 压缩的 tar 包，保持着与过去相同的内部结构。

Helm 图表遵循了类似的路径。Helm v3.8 添加了原生的 OCI 仓库支持，旧的 index.yaml 仓库格式正在被淘汰。Azure CLI 于 2025 年 9 月弃用了对旧版 Helm 仓库的支持。图表使用 helm push 推送到带有 oci:// 前缀的引用，图表 tar 包进入层 Blob。

### 会有什么变化

平台变体获得原生支持。OCI 镜像索引将平台描述符映射到清单。一个有五个平台构建的包会有一个索引指向五个清单，每个清单指向正确的 Blob。这比 npm 将平台特定的二进制文件作为单独的 optionalDependencies 包发布的惯例更简洁，也比 Python 上传多个在文件名中编码平台的 wheels 并让 pip 选择正确的方法更干净。

签名和认证内置支持。每个生态系统都在独立构建自己的签名基础设施。npm 在 2023 年添加了 [基于 Sigstore 的来源证明](https://docs.npmjs.com/generating-provenance-statements)，PyPI 在 2024 年添加了 [认证](https://docs.pypi.org/attestations/)，Cargo 有 [RFC 3403](https://github.com/rust-lang/rfcs/pull/3403) 开放讨论，RubyGems 多年来都有签名支持但几乎没人使用，因为工具从未达到足够易用以成为默认行为。每个努力都需要来自本已捉襟见肘的小型仓库团队的专门工程时间。

OCI 的 subject 字段和 referrers API 为这一切提供了单一机制。Cosign 和 Notation 可以签名任何 OCI 制品，将签名作为单独的制品存储在同一仓库中，通过 subject 引用被签名的内容。SBOM 以相同方式附加，构建来源证明、漏洞扫描结果和许可证审计也是如此：推送一个带有指向它所描述的东西的 subject 的制品，任何客户端都可以通过 referrers API 发现它。

围绕 OCI 仓库的安全生态系统（cosign、notation、Kyverno、OPA Gatekeeper、Ratify）代表了多年的投资，包管理器仓库可以继承这些投资。一个强制执行"所有制品在部署前必须签名"的策略引擎不会关心它是在查看容器镜像还是 RubyGem，因为 referrers API 对两者的工作方式相同。

去重和仓库可持续性。内容可寻址存储通过 SHA-256 摘要标识每个 Blob，所以如果两个包包含相同的文件，仓库只存储一次；如果两个并发上传推送相同的 Blob，仓库接受两者但只保留一份副本。

不相关的源码包之间的共享内容很少见，因此这对二进制包更重要，相同的共享库被打包到不同 formula 的 Homebrew 二进制包中，相同的运行时组件出现在多个 Conda 包中，Debian 的归档在数十个包和版本中携带相同的 .so 文件。

社区资助的仓库是这些成本累积的地方。rubygems.org、crates.io、PyPI 和 hex.pm 运行在 CDN 提供商捐赠的带宽上，主要是 Fastly。这些仓库向数百万开发者提供数 TB 的包数据，基础设施费用由某人志愿承担。

内容可寻址存储不会消除这些成本，但一个运行了十年的仓库累积了大量相同的 Blob，内容可寻址的后端会将它们合并为单份副本，并且随着仓库增长，节省会不断累积。

内容可寻址的镜像。镜像包管理器仓库今天需要重新实现每个仓库的 API 和存储格式，每个生态系统的镜像实现都不同：PyPI 的 Simple Repository API、npm 的 registry API、RubyGems 的 compact index。任何人都可以用现成的软件（如 Harbor、Zot 或 CNCF Distribution 项目）建立一个符合 OCI 标准的镜像，这比逆向工程定制的仓库协议门槛低得多。

内容可寻址存储改变了信任模型。如果你有一个 Blob 的 SHA-256 摘要，无论它从哪个服务器下载，你都可以验证其完整性，因为两个提供相同摘要的仓库在可证明地提供相同的字节。这与 [Docker 镜像作为系统包的 lockfile](/2025/12/18/docker-is-the-lockfile-for-system-packages.html) 的相同特性：一旦你有了摘要，无论它来自哪里，内容都是不可变且可验证的。

镜像不需要被信任为诚实的，只需要是可用的。清单包含摘要，Blob 可以来自任何地方：地理镜像、企业缓存、点对点分发，甚至带有 OCI 布局目录的 USB 驱动器。当 Fastly 出现故障导致 rubygems.org 宕机时，任何能提供匹配字节的替代来源都成为一个有效的镜像，无需任何特殊的信任关系。

仓库基础设施已经建成。运行 rubygems.org 或 crates.io 意味着运行自定义存储、自定义 CDN 配置和自定义认证。基于 OCI 构建的包管理器仓库将最昂贵的部分卸载到已经存在且带有 SLA 和专门工程团队的基础设施上，仓库团队可以将更多时间花在真正重要的事情上：[治理](/2025/12/22/package-registries-are-governance-as-a-service.html)、包索引、依赖解析和搜索。

### 什么不会很好工作

两步获取。如果包管理器客户端直接与 OCI 仓库通信，它需要获取清单、解析它，然后才能开始下载 Blob。容器世界不关心这一点，因为你可能只为单个镜像拉取 5-10 个层。包安装在依赖图中展开：在中等规模项目上进行全新的 npm install 可能会解析 800 个传递依赖，每个都需要自己的清单获取，然后内容下载才能开始。

客户端可以积极地进行流水线处理并并发获取清单，但 OCI 分发规范没有批量清单端点，所以 800 个包仍然意味着 800 个单独的 HTTP 请求，这在当前模型中不存在——当前模型中 npm 可以直接通过 URL GET 一个 tar 包。

有一种变通方法：如果仓库在其现有的元数据响应中包含 OCI Blob 摘要而不是（或同时提供）直接 tar 包 URL，客户端可以完全跳过清单获取，通过摘要下载 Blob。请求流的区别看起来像这样：

纯 OCI 拉取需要三个跳转：获取清单，请求 Blob（返回 307 重定向），然后从签名的 CDN URL 下载。更智能的集成（仓库内部解析清单）将其减少到两个：仓库的元数据 API 返回摘要和直接 CDN URL，客户端下载 Blob 并根据摘要验证它。

Homebrew 还没有完全做到这一点。前面描述的 brew install 流程需要在内容传输之上进行两次额外的往返：一次用于清单，一次用于重定向。

307 重定向不仅仅是延迟成本；它也是仓库在移交给 CDN 之前验证 bearer 令牌的方式，因此采用这种模式的仓库需要决定它们的 Blob 是否真正公开，或者它们是否想保留那个守门步骤。对于有私有包层级的仓库，如 npm 的付费计划或 NuGet 的 Azure Artifacts 集成，重定向模式很重要，因为 Blob 级别的访问控制是产品的一部分。

formula 元数据已经知道 GHCR 仓库和标签，所以索引服务已经在做部分解析工作。如果 formula JSON 包含 Blob 摘要和直接 CDN URL，两次跳转都会消失，客户端可以在一次请求中下载 Blob，同时仍然通过摘要验证完整性。那些[将下载与安装分离](/2026/02/15/separating-download-from-install-in-docker-builds.html)的包管理器可以在专门的下载阶段进一步批量获取 Blob。

元数据才是真正困难的问题。OCI 清单有注解（任意键值字符串）和一个配置 Blob，但包元数据如依赖树、版本约束、平台兼容性规则和许可证信息，无法自然地适配其中任何一个。每个生态系统最终都会定义自己的约定来编码元数据，自己的配置 Blob 媒体类型，自己的注解键。

每个包管理器发明自己的归档格式的原因不是因为 tar 和 zip 不足以归档文件，而是因为元数据约定才是让每个生态系统与众不同的地方。使 .gem 不同于 .crate 的是依赖如何表达以及平台兼容性意味着什么，而不是包裹源代码的压缩算法。OCI 标准化了字节如何在机器之间移动，而不是这些字节对包管理器意味着什么。

小包的开销。OCI 的清单、层、媒体类型和摘要计算的仪式对于可以是数 GB 的多层容器镜像是有意义的。对于一个 50KB 的 npm 包，清单 JSON、配置 Blob、每个的摘要计算以及多步分块上传 API 加起来是多个 HTTP 往返和几百字节的协议开销，而当前模型只需要一个 PUT。固定成本不会随着制品缩小而降低，npm 和 PyPI 等仓库上的大量包足够小，协议开销会成为负载的有意义部分。

仓库 UI 混淆。当一个仓库同时包含容器镜像和包时，用户体验变得混乱。GitHub Container Registry 对一切都显示 docker pull 命令，但 Homebrew 二进制包需要 brew install，Helm 图表需要 helm pull。这方面的用户体验通常不是很好。

不是所有仓库都平等。使非容器制品良好工作的 OCI 1.1 功能（自定义 artifactType、referrers API、subject 字段）并未得到普遍支持。OCI 镜像规范建议关注可移植性的制品遵循 config.mediaType 的特定约定，并非所有仓库都一致地处理自定义媒体类型。仓库实现落后于规范，规范允许的内容与任何给定仓库支持的内容之间的差距是 bug 的来源。

离线气和隔离网络使用。一个 .deb 或 .rpm 文件是自包含的。你可以把它复制到 USB 驱动器上，在隔离网络的机器上安装它。OCI 制品需要一个清单和一个或多个 Blob，通过摘要存储在仓库的内容可寻址布局中。导出为自包含格式（磁盘上的 OCI 布局）是可能的，但增加了一个更简单的归档格式不需要的步骤。

谁来付费。GHCR 的存储和带宽目前对公共镜像[是免费的](https://docs.github.com/en/billing/concepts/product-billing/github-packages)，承诺至少提前一个月通知才会改变。按照标准 GitHub Packages 费率（存储 $0.25/GB/月，带宽 $0.50/GB），Homebrew 的二进制包归档将比零成本显著更贵。GitHub 将其作为实物补贴吸收，Homebrew 3.1.0 的发布说明明确感谢了他们。

如果 rubygems.org 或 PyPI 明天将所有包存储迁移到 GHCR，有人需要与 GitHub、AWS 或 Google 进行类似的对话。当前 Fastly 捐赠 CDN 带宽的模式很脆弱，但它存在且被理解。

采用 OCI 进行分发部分是关于存储和协议的技术决策，但也是关于谁资助生态系统依赖的基础设施以及这创造什么杠杆的决策。从 Fastly 捐赠的 CDN 转移到 GitHub 捐赠的 OCI 存储改变了这个问题的答案，而不一定改进了它。

### 更智能的集成

包管理器仓库做的不仅仅是提供归档。它们维护所有包、版本和元数据的索引，客户端可以搜索和解析依赖，无论是 npm 的 registry API、PyPI 的 Simple Repository API、crates.io 的[基于 git 的索引](https://github.com/rust-lang/crates.io-index)、RubyGems 的 compact index，还是 Go 的模块代理协议。OCI 仓库没有等价物：你可以列出仓库的标签，但没有"给我匹配这个查询的所有包"或"解析这个依赖树"的 API。

这样划分角色比让客户端直接与 OCI 仓库通信更有意义。仓库使用 OCI 作为 Blob 存储后端，并将内容可寻址属性集成到它已经运行的元数据 API 中。

每个包管理器客户端在下载任何内容之前都已经进行元数据请求。npm 获取 packument，pip 获取 Simple Repository API，Bundler 获取 compact index，go 访问模块代理。这些响应已经包含特定版本的下载 URL。

如果这些响应包含 OCI Blob 摘要和指向 OCI 支持存储的直接下载 URL，客户端将获得内容可寻址的完整性检查、镜像属性和去重，而无需自己讲 OCI 分发协议。仓库的索引服务内部解析 OCI 清单，向客户端传递摘要和 URL。

仓库保留对发现、依赖解析、版本选择和平台匹配的完全控制，这些都是 OCI 不会也不应该尝试处理的生态特定逻辑。下面的 OCI 层提供内容可寻址的 Blob 存储、通过 referrers API 的签名，以及镜像通过摘要提供 Blob 而无需特殊信任的能力。

客户端不需要知道它们在与 OCI 支持的存储通信，就像它们不需要知道仓库今天使用 S3 还是 GCS 一样。Homebrew 已经大致这样工作：formula 元数据将客户端指向 GHCR，OCI 清单和重定向是下载路径的实现细节。

仓库甚至不需要迁移其现有包就能获得其中一些好处。OCI 1.1 的 artifactType 允许仅作为 referrers API 锚点的最小清单存在。仓库可以为每个包版本推送一个小的 OCI 清单，将包的摘要放在注解中，并将其用作签名和 SBOM 附加的 subject。实际的 tar 包继续从现有的 CDN 提供。签名和认证基础设施无需移动单个字节的数据包就能工作。

OCI 元数据模型还可以指导仓库如何设计自己的 API。分发规范将"版本列表"（分页标签端点，?n=<limit>&last=<tag>）与"特定版本的元数据"（该标签的清单）分开。npm 的 packument 两者都不做：它返回一个包含包每个版本元数据的单一 JSON 文档，没有分页。

对于一个有数千个版本的包，该响应可能达到数兆字节。当 [npm 10.4.0 停止使用缩写元数据格式](https://github.com/npm/cli/issues/7529) 时，安装 npm 本身从下载 2.1MB 元数据变成了 21MB。完整的 packuments 还导致 [内存不足崩溃](https://github.com/npm/cli/issues/7276)，当 CLI 在依赖解析期间将它们缓存在无界映射中时。

大多数仓库设计时包只有几十个版本，而不是数千个，分页不是一个明显的考虑因素。PyPI 的 Simple Repository API 在一个响应中列出包的所有文件，尽管 [PEP 700](https://peps.python.org/pep-0700/) 后来添加了版本列表元数据。crates.io 采取不同的方法，使用基于 git 的索引，每个 crate 一个文件，所有版本作为行分隔的 JSON，而 RubyGems 的 compact index 和 Go 的模块代理都在一个响应中返回完整的版本列表。这些在设计初期都没有考虑分页，因为规模还不存在，而在现有 API 上改装分页比从一开始就构建它更困难。

如果仓库已经在重新思考其元数据端点以集成 OCI Blob 摘要，那是采用分页版本列表加按需获取每个版本元数据的结构模式的自然时机。

### 这真的会有帮助吗

Homebrew 的迁移是在 Bintray 消亡的压力下发生的，而粗糙的边缘是真实存在的：损坏的 CI、缺失的旧版本、一类新的校验和 bug。这些都不需要改变归档格式：二进制包仍然是它们一直以来的相同 gzip tar 包，只是存储和寻址方式不同。

大多数缺点——清单扇出、重定向税、元数据差距——来自将 OCI 作为面向客户端的协议而非仓库现有 API 后的基础设施。穿越这一点的技术路径比从一开始就采用新的分发协议的破坏性更小。

最能从 OCI 的存储和签名原语中受益的仓库是社区资助的那些：rubygems.org、crates.io、PyPI、hex.pm。它们也是最无力承担迁移或谈判使其可持续的托管安排的仓库。随着围绕开源仓库的资助对话越来越多地提到 OCI 采用，这个问题变得不那么假设性了，处于这些对话接收端的仓库应该了解它们将获得什么以及将放弃什么。

收敛于共享存储原语是问题中容易的部分。每个生态系统的元数据语义是真正不同的，并且会保持不同。更难的问题是，与 OCI 采用一起出现的资助安排是服务于仓库还是提供托管的基础设施提供商。

---

- v5 是 Jeff Johnson 的分支，RPM 的长期维护者，在 2007 年左右与 Red Hat 分裂后。没有主要发行版采用它。主线项目跳过到 v6 以避免混淆。
