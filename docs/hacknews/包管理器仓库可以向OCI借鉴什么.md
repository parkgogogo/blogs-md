Title: What Package Registries Could Borrow from OCI (包管理器仓库可以向 OCI 借鉴什么)
URL: https://nesbitt.io/2026/02/18/what-package-registries-could-borrow-from-oci.html

Every package manager ships code as an archive, and every one of them has a slightly different way to do it.

每个包管理器都以归档文件的形式分发代码，但每个都有自己的一套做法。

npm wraps tarballs in a package/ directory prefix.

npm 将 tar 包包裹在一个 package/ 目录前缀下。

RubyGems nests gzipped files inside an uncompressed tar.

RubyGems 在未压缩的 tar 内部嵌套 gzip 文件。

Alpine concatenates three gzip streams and calls it a package.

Alpine 将三个 gzip 流拼接在一起，称之为一个包。

Python cycled through four distribution formats in twenty years.

Python 在二十年内经历了四种分发格式。

RPM used cpio as its payload format for nearly three decades before finally dropping it in 2025.

RPM 在 2025 年之前近三十年都使用 cpio 作为其负载格式，才最终弃用。

Meanwhile, the container world converged on a single format: OCI, the Open Container Initiative spec.

与此同时，容器世界已经收敛于单一格式：OCI，即开放容器倡议规范。

And over the past few years, OCI registries have quietly started storing things that aren't containers at all: Helm charts, Homebrew bottles, WebAssembly modules, AI models.

在过去几年里，OCI 仓库已经开始悄悄存储那些根本不是容器的东西：Helm 图表、Homebrew 二进制包、WebAssembly 模块、AI 模型。

The format was designed for container images, but the underlying primitives turn out to be general enough that it's worth asking whether every package manager could use OCI for distribution.

该格式最初是为容器镜像设计的，但其底层原语的通用性足以让我们思考：是否每个包管理器都可以使用 OCI 进行分发？

### What OCI actually is (OCI 究竟是什么)

OCI defines three specifications: a Runtime Spec (how to run containers), an Image Spec (how to describe container contents), and a Distribution Spec (how to push and pull from registries).

OCI 定义了三项规范：运行时规范（如何运行容器）、镜像规范（如何描述容器内容），以及分发规范（如何从仓库推送和拉取）。

At the storage level, an OCI registry deals in two primitives: manifests and blobs.

在存储层面，OCI 仓库处理两种原语：清单（manifests）和 Blob。

A manifest is a JSON document that references one or more blobs by their SHA-256 digest.

清单是一份引用一个或多个 Blob 的 JSON 文档，通过它们的 SHA-256 摘要来标识。

A blob is an opaque chunk of binary content, and tags are human-readable names that point to manifests.

Blob 是不透明的二进制内容块，而标签（tags）是指向清单的人类可读的名称。

A container image manifest looks like this:

容器镜像清单看起来像这样：

```json
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
```

The config blob holds metadata (what OS, what architecture, what environment variables).

配置 Blob 保存元数据（什么操作系统、什么架构、什么环境变量）。

Each layer blob holds a tarball of filesystem changes.

每个层 Blob 保存文件系统变更的 tar 包。

The registry doesn't care what's inside the blobs, only that each one is identified and verified by its digest.

仓库不关心 Blob 内部是什么，只关心每个 Blob 都通过其摘要进行标识和验证。

The v1.1 update in February 2024 added artifactType, which declares what kind of thing a manifest describes so a registry can distinguish a Helm chart from a container image from a Homebrew bottle, and subject, which lets one artifact reference another and is how signatures and SBOMs get attached to the thing they describe.

2024 年 2 月的 v1.1 更新添加了 artifactType，用于声明清单描述的是什么类型的东西，这样仓库就能区分 Helm 图表、容器镜像和 Homebrew 二进制包；还添加了 subject，让一个制品可以引用另一个制品，这就是签名和 SBOM（软件物料清单）如何附加到它们所描述的东西上的。

Before 1.1, people stored non-container artifacts by setting custom media types on the config blob, which worked but registries sometimes rejected or mishandled the results.

在 1.1 之前，人们通过在配置 Blob 上设置自定义媒体类型来存储非容器制品，这虽然可行，但仓库有时会拒绝或错误处理结果。

To push an artifact, you upload each blob (to /v2/<name>/blobs/uploads/), then push a manifest that references those blobs by digest and size.

要推送一个制品，你先将每个 Blob 上传（到 /v2/<name>/blobs/uploads/），然后推送一个清单，通过摘要和大小引用这些 Blob。

To pull, you fetch the manifest, read the digests, and download the blobs.

要拉取，则先获取清单，读取摘要，然后下载 Blob。

Because everything is addressed by digest, the registry only stores one copy of any given blob even if multiple artifacts reference it.

因为所有内容都通过摘要寻址，即使多个制品引用同一个 Blob，仓库也只会存储一份副本。

### Why OCI and not something purpose-built (为什么选择 OCI 而不是专门构建的方案)

The format itself carries a lot of container-specific ceremony, but every major cloud provider already runs an OCI-compliant registry: GitHub Container Registry, Amazon ECR, Azure Container Registry, Google Artifact Registry.

该格式本身带有大量容器特定的仪式，但每个主流云提供商都已经运行着符合 OCI 标准的仓库：GitHub Container Registry、Amazon ECR、Azure Container Registry、Google Artifact Registry。

Self-hosted options like Harbor and Zot are mature.

Harbor 和 Zot 等自托管方案也很成熟。

Authentication, access control, replication, and CDN-backed blob storage all exist because container registries already solved those problems at scale, and a package registry built on OCI inherits all of it without reimplementing any of it.

认证、访问控制、复制和由 CDN 支持的 Blob 存储都已经存在，因为容器仓库已经在大规模上解决了这些问题，而基于 OCI 构建的包管理器仓库无需重新实现任何这些功能就能继承全部能力。

ORAS (OCI Registry As Storage) is a CNCF project that abstracts the multi-step OCI upload process into simple commands:

ORAS（OCI Registry As Storage）是一个 CNCF 项目，它将多步骤的 OCI 上传过程抽象为简单的命令：

```
oras push registry.example.com/mypackage:1.0.0 \
  package.tar.gz:application/vnd.example.package.v1.tar+gzip
```

This uploads the file as a blob, creates a manifest referencing it, and tags it.

这会将文件作为 Blob 上传，创建一个引用它的清单，并为其打上标签。

Helm, Flux, Crossplane, and the Sigstore signing tools all use ORAS or the underlying OCI client libraries.

Helm、Flux、Crossplane 以及 Sigstore 签名工具都使用 ORAS 或底层的 OCI 客户端库。

### What package managers ship today (当今包管理器分发什么)

No individual choice here is wrong, but seventeen different answers to the same basic problem suggests the archive format was never the part anyone thought hard about.

这里没有一个单独的选择是错误的，但十七个不同的答案指向同一个基本问题，这表明归档格式从来就不是任何人认真思考过的部分。

| Ecosystem | Format | What's inside |
|-----------|--------|---------------|
| npm | .tgz (gzip tar) | Files under a package/ prefix |
| PyPI | .whl (zip) or .tar.gz | Wheel: pre-built files + .dist-info. Sdist: source + PKG-INFO |
| RubyGems | .gem (tar of gzips) | metadata.gz + data.tar.gz + checksums.yaml.gz |
| Maven | .jar (zip) | Compiled .class files + META-INF/MANIFEST.MF |
| Cargo | .crate (gzip tar) | Source + Cargo.toml + Cargo.lock |
| NuGet | .nupkg (zip) | DLL assemblies + .nuspec XML metadata |
| Homebrew | .bottle.tar.gz | Compiled binaries under install prefix |
| Go | .zip | Source under module@version/ path prefix |
| Hex | Outer tar of inner files | VERSION + metadata.config + contents.tar.gz + CHECKSUM |
| Debian | .deb (ar archive) | debian-binary + control.tar.* + data.tar.* |
| RPM | Custom binary format | Header sections + cpio payload (v4) or custom format (v6) |
| Alpine | Concatenated gzip streams | Signature + control tar + data tar |
| Conda | .conda (zip of zstd tars) or .tar.bz2 | info/ metadata + package content |
| Dart/pub | .tar.gz | Source + pubspec.yaml |
| Swift PM | .zip | Source archive |
| CPAN | .tar.gz | .pm files + Makefile.PL + META.yml + MANIFEST |
| CocoaPods | No archive format | .podspec points to source URLs |

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

### The weird ones (那些奇怪的家伙)

RubyGems nests compression inside archiving instead of the other way around.

RubyGems 将压缩嵌套在归档内部，而不是反过来。

A .gem is an uncompressed tar containing individually gzipped files.

一个 .gem 是一个未压缩的 tar，包含单独 gzip 压缩的文件。

So the outer archive provides no compression, and each component is compressed separately.

因此外层归档不提供压缩，每个组件都单独压缩。

This means you can extract the metadata without decompressing the data, which is a reasonable optimization, but the format looks strange at first glance because everything else in the Unix world puts gzip on the outside.

这意味着你可以在不解压数据的情况下提取元数据，这是一个合理的优化，但该格式第一眼看起来很奇怪，因为 Unix 世界其他所有东西都习惯把 gzip 放在外面。

Alpine APK abuses a quirk of the gzip specification.

Alpine APK 滥用了 gzip 规范的一个特性。

The gzip format allows concatenation of multiple streams into a single file, and technically any compliant decompressor should handle it.

gzip 格式允许将多个流拼接成单个文件，技术上任何符合标准的解压器都应该能处理它。

Alpine packages are three separate gzip streams (signature, control, data) concatenated into one file.

Alpine 包是三个独立的 gzip 流（签名、控制、数据）拼接成一个文件。

Since gzip provides no metadata about where one stream ends and the next begins, you have to fully decompress each segment to find the boundary.

由于 gzip 不提供关于一个流在哪里结束、下一个流在哪里开始的元数据，你必须完全解压每个段才能找到边界。

Kernel modules inside APK packages are often already gzipped, so you get gzip-inside-tar-inside-gzip.

APK 包内的内核模块通常已经是 gzip 压缩的，所以你得到的是 gzip 套在 tar 套在 gzip 里。

RPM used cpio as its payload format from 1995 until RPM v6 shipped in September 2025.

RPM 从 1995 年到 2025 年 9 月 RPM v6 发布，一直使用 cpio 作为其负载格式。

The cpio format has a 4GB file size limit baked into its header fields.

cpio 格式的头部字段中有一个 4GB 的文件大小限制。

For 30 years, no RPM package could contain a file larger than 4GB.

三十年来，没有一个 RPM 包能包含大于 4GB 的文件。

RPM v6 finally dropped cpio in favor of a custom format.

RPM v6 最终弃用 cpio，改用自定义格式。

Debian deliberately chose the ar archive format from the 1970s.

Debian 故意选择了 1970 年代的 ar 归档格式。

The reasoning was practical: the extraction tools (ar, tar, gzip) are available on virtually every Unix system, even in minimal rescue environments.

理由很实际：解压工具（ar、tar、gzip）在几乎每个 Unix 系统上都可用，即使在最小化的救援环境中也是如此。

You can unpack a .deb with nothing but POSIX utilities.

你可以只用 POSIX 工具解压 .deb。

Probably the most intentional format choice on this list.

这可能是这个列表中最有意的格式选择。

npm's package/ prefix means every tarball wraps its contents in a package/ directory that gets stripped during install.

npm 的 package/ 前缀意味着每个 tar 包将其内容包裹在一个 package/ 目录中，安装时会被剥离。

This causes issues with relative file: dependencies inside tarballs, where npm tries to resolve paths relative to the tarball rather than the unpacked directory.

这会导致 tarball 内部相对 file: 依赖的问题，因为 npm 试图相对于 tar 包而不是解压后的目录来解析路径。

Python cycled through four distribution formats.

Python 经历了四种分发格式。

Source tarballs with setup.py (1990s), eggs (2004, inspired by Java JARs, could be imported while still zipped), sdists (standardized tar.gz), and finally wheels (2012).

带 setup.py 的源码 tar 包（1990 年代）、eggs（2004 年，受 Java JAR 启发，可以在压缩状态下直接导入）、sdists（标准化的 tar.gz），以及最终的 wheels（2012 年）。

Eggs lived for nineteen years before PyPI stopped accepting them in August 2023.

Eggs 存活了十九年，直到 PyPI 在 2023 年 8 月停止接受它们。

The wheel format encodes Python version, ABI tag, and platform tag in the filename, which is more metadata than most ecosystems put in the filename but less than what goes in the manifest.

Wheel 格式将 Python 版本、ABI 标签和平台标签编码在文件名中，这比大多数生态系统放在文件名中的元数据要多，但比清单中的元数据要少。

Conda maintained two incompatible formats for years.

Conda 多年来维护了两种不兼容的格式。

The legacy .tar.bz2 and the modern .conda (a zip containing zstandard-compressed tars).

传统的 .tar.bz2 和现代的 .conda（一个包含 zstandard 压缩 tar 的 zip）。

The switch from bzip2 to zstandard yielded significant decompression speedups, but every tool in the ecosystem had to support both formats indefinitely.

从 bzip2 切换到 zstandard 带来了显著的解压速度提升，但生态系统中的每个工具都必须无限期地支持这两种格式。

Hex (Erlang/Elixir) has two checksum schemes in the same package.

Hex（Erlang/Elixir）在同一个包中有两种校验和方案。

The deprecated "inner checksum" hashes concatenated file contents.

已弃用的"内部校验和"对拼接的文件内容进行哈希。

The current "outer checksum" hashes the entire tarball.

当前的"外部校验和"对整个 tar 包进行哈希。

Both are present for backward compatibility.

两者都出于向后兼容性而存在。

### Who's already using OCI (谁已经在使用 OCI)

Homebrew is a traditional package manager, not a "cloud-native" tool, and its migration to OCI already happened under pressure.

Homebrew 是一个传统的包管理器，不是"云原生"工具，而它在压力下的迁移已经发生。

In February 2021, JFrog announced that Bintray would shut down on May 1.

2021 年 2 月，JFrog 宣布 Bintray 将于 5 月 1 日关闭。

Homebrew's bottles were hosted on Bintray.

Homebrew 的二进制包托管在 Bintray 上。

The maintainers had about three months to move their entire archive of precompiled binaries somewhere else, and they landed on GitHub Packages, which stores everything as OCI blobs on ghcr.io.

维护者们有大约三个月的时间将整个预编译二进制文件归档迁移到其他地方，他们最终选择了 GitHub Packages，它将所有内容作为 OCI Blob 存储在 ghcr.io 上。

Homebrew 3.1.0 shipped April 12, 2021, with GHCR as the default download location.

Homebrew 3.1.0 于 2021 年 4 月 12 日发布，将 GHCR 作为默认下载位置。

The transition was rough in the ways you'd expect.

过渡过程出现了预期中的困难。

CI pipelines across the industry broke because macOS images on services like CircleCI shipped with old Homebrew versions that still pointed at Bintray.

整个行业的 CI 流水线崩溃，因为 CircleCI 等服务上的 macOS 镜像附带了仍然指向 Bintray 的旧版本 Homebrew。

During a brownout on April 26, any system running an older Homebrew got 502 errors.

在 4 月 26 日的计划中断期间，任何运行旧版本 Homebrew 的系统都会收到 502 错误。

Older bottle versions were never migrated, so anyone pinned to an old formula version got 404s and had to build from source.

旧版本的二进制包从未被迁移，所以任何固定到旧 formula 版本的人都会收到 404 错误，不得不从源码构建。

The fix was brew update, but CI environments cached old Homebrew versions and didn't auto-update.

解决方法是 brew update，但 CI 环境缓存了旧版本 Homebrew 且不会自动更新。

After the dust settled, the OCI-based storage enabled things that wouldn't have been practical on Bintray.

尘埃落定后，基于 OCI 的存储实现了在 Bintray 上不切实际的功能。

Homebrew 4.0.0 (February 2023) switched from git-cloned tap metadata to a JSON API that leverages the structured OCI manifests, and brew update dropped from running every 5 minutes to every 24 hours.

Homebrew 4.0.0（2023 年 2 月）从 git 克隆的 tap 元数据切换到 JSON API，该 API 利用结构化的 OCI 清单，brew update 从每 5 分钟运行一次降到每 24 小时运行一次。

Manifest-based integrity checking replaced the old checksum approach, though this introduced its own class of bugs where manifest checksums wouldn't match.

基于清单的完整性检查取代了旧的校验和方法，尽管这引入了一类新的 bug，即清单校验和不匹配。

Platform multiplexing came naturally from OCI image indexes, which map platform variants (arm64_sonoma, x86_64_linux) to individual manifests without Homebrew having to build that logic itself.

平台多路复用自然来自 OCI 镜像索引，它将平台变体（arm64_sonoma、x86_64_linux）映射到各个清单，而无需 Homebrew 自己构建该逻辑。

When you run brew install, the client fetches the OCI image index manifest from ghcr.io/v2/homebrew/core/<formula>/manifests/<version>, selects the right platform manifest, then HEADs the blob URL to get a 307 redirect to a signed URL on pkg-containers.githubusercontent.com where Fastly's CDN serves the actual bytes.

当你运行 brew install 时，客户端从 ghcr.io/v2/homebrew/core/<formula>/manifests/<version> 获取 OCI 镜像索引清单，选择正确的平台清单，然后 HEAD 请求 Blob URL 以获得一个 307 重定向到 pkg-containers.githubusercontent.com 上的签名 URL，Fastly 的 CDN 从该 URL 提供实际字节。

GHCR requires a bearer token even for public images, so Homebrew hardcodes QQ== as the bearer token.

GHCR 即使是公共镜像也需要 bearer 令牌，所以 Homebrew 将 QQ== 硬编码为 bearer 令牌。

The bottle inside the blob is still a gzipped tarball with the same internal structure it always had.

Blob 内部的二进制包仍然是 gzip 压缩的 tar 包，保持着与过去相同的内部结构。

Helm charts followed a similar path.

Helm 图表遵循了类似的路径。

Helm v3.8 added native OCI registry support, and the old index.yaml repository format is being phased out.

Helm v3.8 添加了原生的 OCI 仓库支持，旧的 index.yaml 仓库格式正在被淘汰。

Azure CLI retired legacy Helm repository support in September 2025.

Azure CLI 于 2025 年 9 月弃用了对旧版 Helm 仓库的支持。

Charts push with helm push using oci:// prefixed references, and the chart tarball goes into a layer blob.

图表使用 helm push 推送到带有 oci:// 前缀的引用，图表 tar 包进入层 Blob。

### What would change (会有什么变化)

Platform variants get first-class support.

平台变体获得原生支持。

OCI image indexes map platform descriptors to manifests.

OCI 镜像索引将平台描述符映射到清单。

A package with builds for five platforms would have an index pointing to five manifests, each pointing to the right blob.

一个有五个平台构建的包会有一个索引指向五个清单，每个清单指向正确的 Blob。

This is cleaner than npm's convention of publishing platform-specific binaries as separate optionalDependencies packages, or Python's approach of uploading multiple wheels with platform-encoded filenames and letting pip pick the right one.

这比 npm 将平台特定的二进制文件作为单独的 optionalDependencies 包发布的惯例更简洁，也比 Python 上传多个在文件名中编码平台的 wheels 并让 pip 选择正确的方法更干净。

Signing and attestation come built in.

签名和认证内置支持。

Every ecosystem is building its own signing infrastructure independently.

每个生态系统都在独立构建自己的签名基础设施。

npm added Sigstore-based provenance in 2023, PyPI added attestations in 2024, Cargo has RFC 3403 open, and RubyGems has had signature support for years that almost nobody uses because the tooling never reached the point where it was easy enough to be default behavior.

npm 在 2023 年添加了基于 Sigstore 的来源证明，PyPI 在 2024 年添加了认证，Cargo 有 RFC 3403 开放讨论，RubyGems 多年来都有签名支持但几乎没人使用，因为工具从未达到足够易用以成为默认行为。

Each effort required dedicated engineering time from small registry teams who were already stretched thin.

每个努力都需要来自本已捉襟见肘的小型仓库团队的专门工程时间。

OCI's subject field and referrers API provide a single mechanism for all of this.

OCI 的 subject 字段和 referrers API 为这一切提供了单一机制。

Cosign and Notation can sign any OCI artifact, storing the signature as a separate artifact in the same registry that references the signed content via subject.

Cosign 和 Notation 可以签名任何 OCI 制品，将签名作为单独的制品存储在同一仓库中，通过 subject 引用被签名的内容。

SBOMs attach the same way, as do build provenance attestations, vulnerability scan results, and license audits: push an artifact with subject pointing to the thing it describes, and any client can discover it through the referrers API.

SBOM 以相同方式附加，构建来源证明、漏洞扫描结果和许可证审计也是如此：推送一个带有指向它所描述的东西的 subject 的制品，任何客户端都可以通过 referrers API 发现它。

The security ecosystem around OCI registries (cosign, notation, Kyverno, OPA Gatekeeper, Ratify) represents years of investment that package registries could inherit.

围绕 OCI 仓库的安全生态系统（cosign、notation、Kyverno、OPA Gatekeeper、Ratify）代表了多年的投资，包管理器仓库可以继承这些投资。

A policy engine enforcing "all artifacts must be signed before deployment" wouldn't care whether it's looking at a container image or a RubyGem, because the referrers API works the same way for both.

一个强制执行"所有制品在部署前必须签名"的策略引擎不会关心它是在查看容器镜像还是 RubyGem，因为 referrers API 对两者的工作方式相同。

Deduplication and registry sustainability.

去重和仓库可持续性。

Content-addressable storage identifies every blob by its SHA-256 digest, so if two packages contain an identical file the registry stores it once, and if two concurrent uploads push the same blob the registry accepts both but keeps one copy.

内容可寻址存储通过 SHA-256 摘要标识每个 Blob，所以如果两个包包含相同的文件，仓库只存储一次；如果两个并发上传推送相同的 Blob，仓库接受两者但只保留一份副本。

Shared content between unrelated source packages is rare, so this matters more for binary packages where the same shared libraries get bundled into Homebrew bottles for different formulas, the same runtime components appear in multiple Conda packages, and Debian's archive carries the same .so files across dozens of packages and versions.

不相关的源码包之间的共享内容很少见，因此这对二进制包更重要，相同的共享库被打包到不同 formula 的 Homebrew 二进制包中，相同的运行时组件出现在多个 Conda 包中，Debian 的归档在数十个包和版本中携带相同的 .so 文件。

The community-funded registries are where this adds up.

社区资助的仓库是这些成本累积的地方。

rubygems.org, crates.io, PyPI, and hex.pm run on bandwidth donated by CDN providers, primarily Fastly.

rubygems.org、crates.io、PyPI 和 hex.pm 运行在 CDN 提供商捐赠的带宽上，主要是 Fastly。

These registries serve terabytes of package data to millions of developers on infrastructure that someone is volunteering to cover.

这些仓库向数百万开发者提供数 TB 的包数据，基础设施费用由某人志愿承担。

Content-addressable storage won't eliminate those costs, but a registry that's been running for ten years has accumulated a lot of identical blobs that a content-addressable backend would collapse into single copies, and the savings compound as the registry grows.

内容可寻址存储不会消除这些成本，但一个运行了十年的仓库累积了大量相同的 Blob，内容可寻址的后端会将它们合并为单份副本，并且随着仓库增长，节省会不断累积。

Content-addressed mirroring.

内容可寻址的镜像。

Mirroring a package registry today requires reimplementing each registry's API and storage format, and every ecosystem's mirror implementation is different: the Simple Repository API for PyPI, the registry API for npm, the compact index for RubyGems.

镜像包管理器仓库今天需要重新实现每个仓库的 API 和存储格式，每个生态系统的镜像实现都不同：PyPI 的 Simple Repository API、npm 的 registry API、RubyGems 的 compact index。

Anyone can stand up an OCI-compliant mirror with off-the-shelf software like Harbor, Zot, or the CNCF Distribution project, which is a much lower bar than reverse-engineering a bespoke registry protocol.

任何人都可以用现成的软件（如 Harbor、Zot 或 CNCF Distribution 项目）建立一个符合 OCI 标准的镜像，这比逆向工程定制的仓库协议门槛低得多。

Content-addressable storage changes the trust model.

内容可寻址存储改变了信任模型。

If you have a blob's SHA-256 digest, you can verify its integrity regardless of which server you downloaded it from, because two registries serving the same digest are provably serving the same bytes.

如果你有一个 Blob 的 SHA-256 摘要，无论它从哪个服务器下载，你都可以验证其完整性，因为两个提供相同摘要的仓库在可证明地提供相同的字节。

This is the same property that makes Docker images work as lockfiles for system packages: once you have the digest, the content is immutable and verifiable no matter where it came from.

这与 Docker 镜像作为系统包的 lockfile 的相同特性：一旦你有了摘要，无论它来自哪里，内容都是不可变且可验证的。

A mirror doesn't need to be trusted to be honest, only to be available.

镜像不需要被信任为诚实的，只需要是可用的。

The manifest contains the digests, and the blobs can come from anywhere: geographic mirrors, corporate caches, peer-to-peer distribution, even a USB drive with an OCI layout directory.

清单包含摘要，Blob 可以来自任何地方：地理镜像、企业缓存、点对点分发，甚至带有 OCI 布局目录的 USB 驱动器。

When Fastly has an outage and rubygems.org goes down with it, any alternative source that can serve matching bytes becomes a valid mirror without any special trust relationship.

当 Fastly 出现故障导致 rubygems.org 宕机时，任何能提供匹配字节的替代来源都成为一个有效的镜像，无需任何特殊的信任关系。

Registry infrastructure is already built.

仓库基础设施已经建成。

Running rubygems.org or crates.io means running custom storage, custom CDN configuration, and custom authentication.

运行 rubygems.org 或 crates.io 意味着运行自定义存储、自定义 CDN 配置和自定义认证。

A package registry built on OCI offloads the most expensive parts to infrastructure that already exists with SLAs and dedicated engineering teams, and the registry team can spend more time on what actually matters: governance, the package index, dependency resolution, and search.

基于 OCI 构建的包管理器仓库将最昂贵的部分卸载到已经存在且带有 SLA 和专门工程团队的基础设施上，仓库团队可以将更多时间花在真正重要的事情上：治理、包索引、依赖解析和搜索。

### What wouldn't work well (什么不会很好工作)

The two-step fetch.

两步获取。

If a package manager client talks directly to the OCI registry, it needs to fetch the manifest, parse it, then download the blob before extraction can start.

如果包管理器客户端直接与 OCI 仓库通信，它需要获取清单、解析它，然后才能开始下载 Blob。

The container world doesn't care about this because you're pulling maybe 5-10 layers for a single image.

容器世界不关心这一点，因为你可能只为单个镜像拉取 5-10 个层。

Package installs fan out across the dependency graph: a fresh npm install on a mid-sized project might resolve 800 transitive dependencies, each needing its own manifest fetch before the content download can begin.

包安装在依赖图中展开：在中等规模项目上进行全新的 npm install 可能会解析 800 个传递依赖，每个都需要自己的清单获取，然后内容下载才能开始。

A client could pipeline aggressively and fetch manifests concurrently, but the OCI Distribution Spec doesn't have a batch manifest endpoint, so 800 packages still means 800 separate HTTP requests that don't exist in the current model where npm can GET a tarball directly by URL.

客户端可以积极地进行流水线处理并并发获取清单，但 OCI 分发规范没有批量清单端点，所以 800 个包仍然意味着 800 个单独的 HTTP 请求，这在当前模型中不存在——当前模型中 npm 可以直接通过 URL GET 一个 tar 包。

There's a way around this: if registries included OCI blob digests in their existing metadata responses instead of (or alongside) direct tarball URLs, clients could skip the manifest fetch entirely and download blobs by digest.

有一种变通方法：如果仓库在其现有的元数据响应中包含 OCI Blob 摘要而不是（或同时提供）直接 tar 包 URL，客户端可以完全跳过清单获取，通过摘要下载 Blob。

The difference in request flow looks like this:

请求流的区别看起来像这样：

A pure OCI pull requires three hops: fetch the manifest, request the blob (which returns a 307 redirect), then download from the signed CDN URL.

纯 OCI 拉取需要三个跳转：获取清单，请求 Blob（返回 307 重定向），然后从签名的 CDN URL 下载。

A smarter integration where the registry resolves the manifest internally reduces that to two: the registry's metadata API returns the digest and a direct CDN URL, and the client downloads the blob and verifies it against the digest.

更智能的集成（仓库内部解析清单）将其减少到两个：仓库的元数据 API 返回摘要和直接 CDN URL，客户端下载 Blob 并根据摘要验证它。

Homebrew doesn't quite do this yet.

Homebrew 还没有完全做到这一点。

The brew install flow described earlier requires two extra round-trips on top of the content transfer: one for the manifest, one for the redirect.

前面描述的 brew install 流程需要在内容传输之上进行两次额外的往返：一次用于清单，一次用于重定向。

The 307 redirect isn't purely a latency cost; it's also how the registry verifies the bearer token before handing off to the CDN, so registries adopting this pattern would need to decide whether their blobs are truly public or whether they want to keep that gatekeeper step.

307 重定向不仅仅是延迟成本；它也是仓库在移交给 CDN 之前验证 bearer 令牌的方式，因此采用这种模式的仓库需要决定它们的 Blob 是否真正公开，或者它们是否想保留那个守门步骤。

For registries with private package tiers, like npm's paid plans or NuGet's Azure Artifacts integration, the redirect model matters because access control at the blob level is part of the product.

对于有私有包层级的仓库，如 npm 的付费计划或 NuGet 的 Azure Artifacts 集成，重定向模式很重要，因为 Blob 级别的访问控制是产品的一部分。

The formula metadata already knows the GHCR repository and tag, so the index service is already doing part of the resolution.

formula 元数据已经知道 GHCR 仓库和标签，所以索引服务已经在做部分解析工作。

If the formula JSON included the blob digest and a direct CDN URL, both hops disappear and the client downloads the blob in a single request while still verifying integrity by digest.

如果 formula JSON 包含 Blob 摘要和直接 CDN URL，两次跳转都会消失，客户端可以在一次请求中下载 Blob，同时仍然通过摘要验证完整性。

Package managers that separate download from install could take it further by batching blob fetches during a dedicated download phase.

那些将下载与安装分离的包管理器可以在专门的下载阶段进一步批量获取 Blob。

Metadata is the actual hard problem.

元数据才是真正困难的问题。

OCI manifests have annotations (arbitrary key-value strings) and a config blob, but package metadata like dependency trees, version constraints, platform compatibility rules, and license information doesn't fit naturally into either.

OCI 清单有注解（任意键值字符串）和一个配置 Blob，但包元数据如依赖树、版本约束、平台兼容性规则和许可证信息，无法自然地适配其中任何一个。

Each ecosystem would end up defining its own conventions for encoding metadata, its own mediaType for its config blob, its own annotation keys.

每个生态系统最终都会定义自己的约定来编码元数据，自己的配置 Blob 媒体类型，自己的注解键。

The reason every package manager invented its own archive format is not because tar and zip are insufficient for archiving files, but because the metadata conventions are what make each ecosystem different.

每个包管理器发明自己的归档格式的原因不是因为 tar 和 zip 不足以归档文件，而是因为元数据约定才是让每个生态系统与众不同的地方。

What makes a .gem different from a .crate is how dependencies are expressed and what platform compatibility means, not the compression algorithm wrapping the source code.

使 .gem 不同于 .crate 的是依赖如何表达以及平台兼容性意味着什么，而不是包裹源代码的压缩算法。

OCI standardizes how bytes move between machines, not what those bytes mean to a package manager.

OCI 标准化了字节如何在机器之间移动，而不是这些字节对包管理器意味着什么。

Small package overhead.

小包的开销。

The OCI ceremony of manifests, layers, media types, and digest computation makes sense for multi-layer container images that can be gigabytes.

OCI 的清单、层、媒体类型和摘要计算的仪式对于可以是数 GB 的多层容器镜像是有意义的。

For a 50KB npm package, the manifest JSON, config blob, digest computation for each, and the multi-step chunked upload API add up to several HTTP round-trips and a few hundred bytes of protocol overhead where the current model needs a single PUT.

对于一个 50KB 的 npm 包，清单 JSON、配置 Blob、每个的摘要计算以及多步分块上传 API 加起来是多个 HTTP 往返和几百字节的协议开销，而当前模型只需要一个 PUT。

The fixed cost doesn't scale down with the artifact, and a large share of packages on registries like npm and PyPI are small enough that the protocol overhead becomes a meaningful fraction of the payload.

固定成本不会随着制品缩小而降低，npm 和 PyPI 等仓库上的大量包足够小，协议开销会成为负载的有意义部分。

Registry UI confusion.

仓库 UI 混淆。

When a registry contains both container images and packages, the user experience gets muddled.

当一个仓库同时包含容器镜像和包时，用户体验变得混乱。

GitHub Container Registry shows docker pull commands for everything, but a Homebrew bottle needs brew install and a Helm chart needs helm pull.

GitHub Container Registry 对一切都显示 docker pull 命令，但 Homebrew 二进制包需要 brew install，Helm 图表需要 helm pull。

The UX for this is generally not great.

这方面的用户体验通常不是很好。

Not all registries are equal.

不是所有仓库都平等。

The OCI 1.1 features that make non-container artifacts work well (custom artifactType, the referrers API, the subject field) aren't universally supported.

使非容器制品良好工作的 OCI 1.1 功能（自定义 artifactType、referrers API、subject 字段）并未得到普遍支持。

The OCI Image Specification advises that artifacts concerned with portability should follow specific conventions for config.mediaType, and not all registries handle custom media types consistently.

OCI 镜像规范建议关注可移植性的制品遵循 config.mediaType 的特定约定，并非所有仓库都一致地处理自定义媒体类型。

Registry implementations lag the spec, and the gap between what the spec allows and what any given registry supports is a source of bugs.

仓库实现落后于规范，规范允许的内容与任何给定仓库支持的内容之间的差距是 bug 的来源。

Offline and air-gapped use.

离线气和隔离网络使用。

A .deb or .rpm file is self-contained.

一个 .deb 或 .rpm 文件是自包含的。

You can copy it to a USB drive and install it on an air-gapped machine.

你可以把它复制到 USB 驱动器上，在隔离网络的机器上安装它。

An OCI artifact requires a manifest and one or more blobs, stored by digest in a registry's content-addressable layout.

OCI 制品需要一个清单和一个或多个 Blob，通过摘要存储在仓库的内容可寻址布局中。

Exporting to a self-contained format (OCI layout on disk) is possible but adds a step that simpler archive formats don't need.

导出为自包含格式（磁盘上的 OCI 布局）是可能的，但增加了一个更简单的归档格式不需要的步骤。

Who pays.

谁来付费。

GHCR storage and bandwidth are currently free for public images, with a promise of at least one month's notice before that changes.

GHCR 的存储和带宽目前对公共镜像是免费的，承诺至少提前一个月通知才会改变。

At standard GitHub Packages rates ($0.25/GB/month for storage, $0.50/GB for bandwidth), Homebrew's bottle archive would cost substantially more than zero.

按照标准 GitHub Packages 费率（存储 $0.25/GB/月，带宽 $0.50/GB），Homebrew 的二进制包归档将比零成本显著更贵。

GitHub absorbs that as an in-kind subsidy, and the Homebrew 3.1.0 release notes explicitly thank them for it.

GitHub 将其作为实物补贴吸收，Homebrew 3.1.0 的发布说明明确感谢了他们。

If rubygems.org or PyPI moved all their package storage to GHCR tomorrow, someone would need to have a similar conversation with GitHub, or AWS, or Google.

如果 rubygems.org 或 PyPI 明天将所有包存储迁移到 GHCR，有人需要与 GitHub、AWS 或 Google 进行类似的对话。

The current model of Fastly donating CDN bandwidth is fragile, but it exists and it's understood.

当前 Fastly 捐赠 CDN 带宽的模式很脆弱，但它存在且被理解。

Adopting OCI for distribution is partly a technical decision about storage and protocols, but it's also a decision about who funds the infrastructure that the ecosystem depends on and what leverage that creates.

采用 OCI 进行分发部分是关于存储和协议的技术决策，但也是关于谁资助生态系统依赖的基础设施以及这创造什么杠杆的决策。

Shifting from Fastly-donated CDN to GitHub-donated OCI storage changes the answer to that question without necessarily improving it.

从 Fastly 捐赠的 CDN 转移到 GitHub 捐赠的 OCI 存储改变了这个问题的答案，而不一定改进了它。

### The smarter integration (更智能的集成)

Package registries do more than serve archives.

包管理器仓库做的不仅仅是提供归档。

They maintain an index of all packages, versions, and metadata that clients can search and resolve dependencies against, whether that's npm's registry API, PyPI's Simple Repository API, crates.io's git-based index, RubyGems' compact index, or Go's module proxy protocol.

它们维护所有包、版本和元数据的索引，客户端可以搜索和解析依赖，无论是 npm 的 registry API、PyPI 的 Simple Repository API、crates.io 的基于 git 的索引、RubyGems 的 compact index，还是 Go 的模块代理协议。

OCI registries have no equivalent: you can list tags for a repository, but there's no API for "give me all packages matching this query" or "resolve this dependency tree."

OCI 仓库没有等价物：你可以列出仓库的标签，但没有"给我匹配这个查询的所有包"或"解析这个依赖树"的 API。

Splitting the roles this way makes more sense than having clients talk to the OCI registry directly.

这样划分角色比让客户端直接与 OCI 仓库通信更有意义。

The registry uses OCI as a blob storage backend and integrates the content-addressable properties into the metadata APIs it already operates.

仓库使用 OCI 作为 Blob 存储后端，并将内容可寻址属性集成到它已经运行的元数据 API 中。

Every package manager client already makes a metadata request before downloading anything.

每个包管理器客户端在下载任何内容之前都已经进行元数据请求。

npm fetches the packument, pip fetches the Simple Repository API, Bundler fetches the compact index, go hits the module proxy.

npm 获取 packument，pip 获取 Simple Repository API，Bundler 获取 compact index，go 访问模块代理。

These responses already include download URLs for specific versions.

这些响应已经包含特定版本的下载 URL。

If those responses included OCI blob digests and direct download URLs pointing at OCI-backed storage, clients would get the content-addressable integrity checks, the mirroring properties, and the deduplication without ever needing to speak the OCI Distribution protocol themselves.

如果这些响应包含 OCI Blob 摘要和指向 OCI 支持存储的直接下载 URL，客户端将获得内容可寻址的完整性检查、镜像属性和去重，而无需自己讲 OCI 分发协议。

The registry's index service resolves the OCI manifest internally and hands the client a digest and a URL.

仓库的索引服务内部解析 OCI 清单，向客户端传递摘要和 URL。

The registry keeps full control of discovery, dependency resolution, version selection, and platform matching, all the ecosystem-specific logic that OCI doesn't and shouldn't try to handle.

仓库保留对发现、依赖解析、版本选择和平台匹配的完全控制，这些都是 OCI 不会也不应该尝试处理的生态特定逻辑。

The OCI layer underneath provides content-addressable blob storage, signing via the referrers API, and the ability for mirrors to serve blobs by digest without special trust.

下面的 OCI 层提供内容可寻址的 Blob 存储、通过 referrers API 的签名，以及镜像通过摘要提供 Blob 而无需特殊信任的能力。

Clients don't need to know they're talking to OCI-backed storage any more than they need to know whether the registry uses S3 or GCS underneath today.

客户端不需要知道它们在与 OCI 支持的存储通信，就像它们不需要知道仓库今天使用 S3 还是 GCS 一样。

Homebrew already works roughly this way: the formula metadata points clients at GHCR, and the OCI manifest and redirect are implementation details of the download path.

Homebrew 已经大致这样工作：formula 元数据将客户端指向 GHCR，OCI 清单和重定向是下载路径的实现细节。

A registry doesn't even need to migrate its existing packages to get some of these benefits.

仓库甚至不需要迁移其现有包就能获得其中一些好处。

OCI 1.1's artifactType allows minimal manifests that exist purely as anchors for the referrers API.

OCI 1.1 的 artifactType 允许仅作为 referrers API 锚点的最小清单存在。

A registry could push a small OCI manifest for each package version, with the package's digest in the annotations, and use it as the subject that signatures and SBOMs attach to.

仓库可以为每个包版本推送一个小的 OCI 清单，将包的摘要放在注解中，并将其用作签名和 SBOM 附加的 subject。

The actual tarball continues to be served from the existing CDN.

实际的 tar 包继续从现有的 CDN 提供。

The signing and attestation infrastructure works without moving a single byte of package data.

签名和认证基础设施无需移动单个字节的数据包就能工作。

The OCI metadata model could also inform how registries design their own APIs.

OCI 元数据模型还可以指导仓库如何设计自己的 API。

The Distribution Spec separates "list of versions" (the paginated tags endpoint, ?n=<limit>&last=<tag>) from "metadata for a specific version" (the manifest for that tag).

分发规范将"版本列表"（分页标签端点，?n=<limit>&last=<tag>）与"特定版本的元数据"（该标签的清单）分开。

npm's packument does neither: it returns a single JSON document containing metadata for every version of a package, with no pagination.

npm 的 packument 两者都不做：它返回一个包含包每个版本元数据的单一 JSON 文档，没有分页。

For a package with thousands of versions that response can be megabytes.

对于一个有数千个版本的包，该响应可能达到数兆字节。

When npm 10.4.0 stopped using the abbreviated metadata format, installing npm itself went from downloading 2.1MB of metadata to 21MB.

当 npm 10.4.0 停止使用缩写元数据格式时，安装 npm 本身从下载 2.1MB 元数据变成了 21MB。

The full packuments also caused out-of-memory crashes when the CLI cached them in an unbounded map during dependency resolution.

完整的 packuments 还导致内存不足崩溃，当 CLI 在依赖解析期间将它们缓存在无界映射中时。

Most registries were designed when packages had dozens of versions, not thousands, and pagination wasn't an obvious concern.

大多数仓库设计时包只有几十个版本，而不是数千个，分页不是一个明显的考虑因素。

PyPI's Simple Repository API lists all files for a package in one response, though PEP 700 added version listing metadata after the fact.

PyPI 的 Simple Repository API 在一个响应中列出包的所有文件，尽管 PEP 700 后来添加了版本列表元数据。

crates.io takes a different approach with a git-based index that stores one file per crate, all versions as line-delimited JSON, while RubyGems' compact index and Go's module proxy both return complete version lists in a single response.

crates.io 采取不同的方法，使用基于 git 的索引，每个 crate 一个文件，所有版本作为行分隔的 JSON，而 RubyGems 的 compact index 和 Go 的模块代理都在一个响应中返回完整的版本列表。

None of these designed for pagination early on because the scale wasn't there yet, and retrofitting pagination onto an existing API is harder than building it in from the start.

这些在设计初期都没有考虑分页，因为规模还不存在，而在现有 API 上改装分页比从一开始就构建它更困难。

If a registry is already rethinking its metadata endpoints to integrate OCI blob digests, that's a natural time to adopt the structural pattern of paginated version listing plus per-version metadata fetched on demand.

如果仓库已经在重新思考其元数据端点以集成 OCI Blob 摘要，那是采用分页版本列表加按需获取每个版本元数据的结构模式的自然时机。

### Would it actually help (这真的会有帮助吗)

Homebrew's migration happened under duress when Bintray died, and the rough edges were real: broken CI, missing old versions, a new class of checksum bugs.

Homebrew 的迁移是在 Bintray 消亡的压力下发生的，而粗糙的边缘是真实存在的：损坏的 CI、缺失的旧版本、一类新的校验和 bug。

None of it required changing the archive format: the bottles are the same gzipped tarballs they always were, just stored and addressed differently.

这些都不需要改变归档格式：二进制包仍然是它们一直以来的相同 gzip tar 包，只是存储和寻址方式不同。

Most of the drawbacks, the manifest fan-out, the redirect tax, the metadata gap, come from treating OCI as the client-facing protocol rather than as infrastructure behind the registry's existing API.

大多数缺点——清单扇出、重定向税、元数据差距——来自将 OCI 作为面向客户端的协议而非仓库现有 API 后的基础设施。

The technical path through that is less disruptive than adopting a new distribution protocol from scratch.

穿越这一点的技术路径比从一开始就采用新的分发协议的破坏性更小。

The registries that would benefit most from OCI's storage and signing primitives are the community-funded ones: rubygems.org, crates.io, PyPI, hex.pm.

最能从 OCI 的存储和签名原语中受益的仓库是社区资助的那些：rubygems.org、crates.io、PyPI、hex.pm。

They're also the ones least able to afford the migration or negotiate the hosting arrangements that make it sustainable.

它们也是最无力承担迁移或谈判使其可持续的托管安排的仓库。

This question is becoming less hypothetical as funding conversations around open source registries increasingly reference OCI adoption, and the registries on the receiving end of those conversations should understand what they'd be gaining and what they'd be giving up.

随着围绕开源仓库的资助对话越来越多地提到 OCI 采用，这个问题变得不那么假设性了，处于这些对话接收端的仓库应该了解它们将获得什么以及将放弃什么。

Converging on shared storage primitives is the easy part of the problem.

收敛于共享存储原语是问题中容易的部分。

Each ecosystem's metadata semantics are genuinely different and will stay that way.

每个生态系统的元数据语义是真正不同的，并且会保持不同。

The harder question is whether the funding arrangements that come with OCI adoption serve the registries or the infrastructure providers offering to host them.

更难的问题是，与 OCI 采用一起出现的资助安排是服务于仓库还是提供托管的基础设施提供商。

---

v5 was a fork by Jeff Johnson, RPM's long-time maintainer, after he split from Red Hat around 2007. No major distribution adopted it. The mainline project skipped to v6 to avoid confusion.

v5 是 Jeff Johnson 的分支，RPM 的长期维护者，在 2007 年左右与 Red Hat 分裂后。没有主要发行版采用它。主线项目跳过到 v6 以避免混淆。

---

## 批判性思考评论 (Critical Thinking Commentary)

### 作者主要论点分析

本文作者提出了一个核心论点：包管理器仓库可以向 OCI（开放容器倡议）规范借鉴，以实现更统一、更高效的分发机制。作者通过以下几个方面展开论证：

1. **问题诊断**：当前各个包管理器使用 17 种不同的归档格式，这种碎片化导致了重复建设和效率低下。作者用大量实例（如 RubyGems 的嵌套压缩、Alpine 的 gzip 流拼接、RPM 的 4GB 限制）展示了这种混乱的现状。

2. **OCI 的优势**：OCI 提供了内容可寻址存储、内置签名机制、平台多路复用等特性，这些特性可以解决包管理器面临的共同问题。

3. **成功案例**：Homebrew 在 Bintray 关闭后被迫迁移到 OCI 的实践证明了可行性，并且带来了额外的好处（如更新频率降低、平台多路复用）。

4. **平衡的观点**：作者没有盲目推崇 OCI，而是指出了其局限性（两步获取的开销、小包 overhead、元数据不匹配、资助模式的变化等）。

### 优点

1. **实证丰富**：作者对不同包管理器格式的细节了如指掌，17 种格式的对比表格令人印象深刻。这种深入的技术细节增强了论证的可信度。

2. **案例研究价值高**：Homebrew 的迁移案例详细描述了过渡期的阵痛（CI 损坏、旧版本丢失），这种真实的经验对考虑类似迁移的项目非常有价值。

3. **结构清晰**：文章采用"是什么-为什么-怎么做-局限性"的结构，逻辑严密，易于跟随。

4. **现实主义的视角**：作者关注到了技术之外的实际问题——谁来付费。这种对基础设施资助模式的敏感度在纯技术文章中很少见。

### 弱点

1. **对 OCI 生态的过度乐观**：虽然作者提到了仓库实现滞后于规范的问题，但似乎低估了将 OCI 作为通用存储层的实际复杂性。容器生态和包管理生态的需求差异可能比表面上更大。

2. **成功案例的代表性存疑**：Homebrew 是一个特殊情况——它在压力下被迫迁移，且有 GitHub 的实物补贴。这并不意味着其他包管理器（尤其是社区资助的）能够或应该复制这条路径。

3. **元数据问题的轻描淡写**：作者承认"元数据才是真正困难的问题"，但没有深入探讨为什么这个问题难以解决。不同生态系统的依赖解析逻辑差异巨大，OCI 的通用原语可能无法很好地映射这些语义。

4. **对去重效果的夸大**：作者提到"内容可寻址存储会将相同的 Blob 合并为单份副本"，但对于源代码包而言，重复内容的比例可能很低，去重效果可能不如预期。

### 我的批判视角

我认为作者的核心洞察是正确的——包管理器领域确实存在过度碎片化的问题，OCI 提供了一套经过验证的原语，值得认真考虑。然而，我有一些不同的看法：

**关于标准化的时间点**：包管理器格式之所以多样，部分原因是它们是在不同的时间、不同的约束条件下演化的。强制收敛到一个标准可能会扼杀创新。OCI 本身是容器生态标准化的产物，但容器是相对年轻且快速迭代的领域，而许多包管理器（如 CPAN、Debian）有着几十年的历史和庞大的遗留系统。

**关于"更智能的集成"**：作者提出的"仓库使用 OCI 作为后端存储，但保持现有 API"的方案实际上是最务实的路径。但这也意味着 OCI 只是作为一个"更好的 S3"存在，而不是真正改变包管理的工作方式。这种变革的深度可能比作者暗示的要浅。

**关于资助模式的担忧**：这是文章中最有价值的观察之一。从 Fastly 捐赠 CDN 到 GitHub 捐赠 OCI 存储，确实改变了权力格局。GitHub（微软）对开源基础设施的影响力将进一步增强，这对生态系统的长期健康意味着什么？

### 影响与启示

1. **对包管理器维护者**：OCI 值得作为存储后端进行评估，但不应急于替换现有 API。可以借鉴 Homebrew 的渐进式迁移策略。

2. **对云提供商**：GitHub、AWS、Google 等可以通过提供更友好的包管理器托管方案来竞争，而不仅仅是容器注册表。

3. **对开源社区**：需要警惕基础设施集中化的风险。当越来越多的开源项目依赖于少数几家公司的免费服务时，我们是否在创造新的单点故障？

4. **对标准制定者**：OCI 规范可以考虑更明确地支持非容器制品，减少各生态系统的重复工作。

### 结论

这是一篇技术深度与现实关怀兼具的优秀文章。作者成功地将一个看似抽象的技术话题与具体的运维问题、经济考量联系起来。尽管我对某些技术细节持有保留意见，但文章的核心信息——包管理器领域需要更认真地思考存储和分发层的标准化——是站得住脚的。最终，技术选择永远是权衡，OCI 不是银弹，但它提供了一个值得认真考虑的基准。
