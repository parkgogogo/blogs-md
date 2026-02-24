URL: https://nesbitt.io/2026/02/23/where-do-specifications-fit-in-the-dependency-tree.html

Your Ruby gem declares `required_ruby_version >= 3.0`. That constraint references the Ruby 3.0 language specification, expressed through the implementation version, checked against whichever runtime happens to be running, with no distinction between MRI and JRuby, and no connection to the specification document that defines what Ruby 3.0 even is.

你的 Ruby gem 声明了 `required_ruby_version >= 3.0`。这个约束引用的是 Ruby 3.0 语言规范，通过实现版本来表达，并针对任何正在运行的运行时进行检查，不区分 MRI 和 JRuby，也与定义 Ruby 3.0 的规范文档没有任何关联。

Runtimes at least show up somewhere in the tooling. Your HTTP library also depends on RFC 9110, your JSON parser on ECMA-404, your TLS implementation on RFC 8446, and none of those appear in any manifest, lockfile, or SBOM.

运行时至少在工具链的某个地方出现。你的 HTTP 库还依赖于 RFC 9110，你的 JSON 解析器依赖于 ECMA-404，你的 TLS 实现依赖于 RFC 8446，而这些都不会出现在任何清单、锁文件或 SBOM 中。

Library dependencies get the full treatment: manifests declare them, lockfiles pin them, SBOMs track them, scanners check them for vulnerabilities. Runtime versions sit one layer down, handled differently by every ecosystem. Python has `Requires-Python` in package元数据, enforced by pip but ignored by trove classifiers that may disagree with it. Ruby has `required_ruby_version` in the gemspec, enforced by both RubyGems and Bundler. Node.js has the `engines` field in package.json, advisory by default in npm unless you flip a config flag. Go's `go` directive in go.mod was advisory until Go 1.21, when it flipped to a hard minimum in a single release and started auto-downloading the required toolchain if yours is too old.

库依赖获得完整处理：清单声明它们，锁文件固定它们，SBOM 跟踪它们，扫描器检查它们的漏洞。运行时版本位于下一层，每个生态系统处理方式不同。Python 在包元数据中有 `Requires-Python`，由 pip 强制执行，但可能被与其不一致的 trove 分类器忽略。Ruby 在 gemspec 中有 `required_ruby_version`，由 RubyGems 和 Bundler 共同强制执行。Node.js 在 package.json 中有 `engines` 字段，在 npm 中默认只是建议性的，除非你更改配置标志。Go 在 go.mod 中的 `go` 指令在 Go 1.21 之前都是建议性的，之后在一次发布中变成了硬性最低要求，并在你的工具链太旧时自动下载所需工具链。

Developers keep inventing new layers because none of these are reliable enough on their own. A Ruby project might have `required_ruby_version >= 3.0` in the gemspec, `ruby "3.2.2"` in the Gemfile, and `ruby 3.2.2` in .tool-versions for asdf or mise. That's the same dependency declared in three places with three enforcement mechanisms, and they can disagree. The .tool-versions file exists because the gemspec constraint is too loose and the Gemfile directive doesn't control which binary is on your PATH.

开发者不断创造新的层级，因为这些机制单独都不够可靠。一个 Ruby 项目可能在 gemspec 中有 `required_ruby_version >= 3.0`，在 Gemfile 中有 `ruby "3.2.2"`，在 .tool-versions 中有 `ruby 3.2.2` 用于 asdf 或 mise。这是同一个依赖在三个地方用三种执行机制声明，而且它们可能不一致。.tool-versions 文件存在是因为 gemspec 约束太宽松，而 Gemfile 指令无法控制哪个二进制文件在你的 PATH 中。

Runtime implementation is barely tracked at all. JRuby 9.4 reports `RUBY_VERSION` as "3.1.0", so a gem requiring >= 3.0 passes. If the gem has a C extension, it fails at build time because JRuby can't run C extensions, and the gemspec has no way to express that it needs MRI specifically. .NET is the only ecosystem that formally addressed this with .NET Standard, a versioned API surface that works across .NET Framework, .NET Core, Mono, and Xamarin, essentially a spec for the spec implementations.

运行时实现几乎完全不被跟踪。JRuby 9.4 报告 `RUBY_VERSION` 为 "3.1.0"，所以要求 >= 3.0 的 gem 会通过。如果 gem 有 C 扩展，它会在构建时失败，因为 JRuby 无法运行 C 扩展，而 gemspec 无法表达它特别需要 MRI。.NET 是唯一正式解决这个问题的生态系统，通过 .NET Standard，一个跨 .NET Framework、.NET Core、Mono 和 Xamarin 的版本化 API 表面，本质上就是规范实现的规范。

And below all of this sit the specifications themselves, language definitions and protocol standards and encoding rules, none of which appear in any dependency graph.

而在所有这一切之下是规范本身，语言定义、协议标准和编码规则，这些都不会出现在任何依赖图中。

## Spack

## Spack

Spack, the HPC package manager, spent seven years learning what happens when you leave a dependency implicit.

Spack，这个 HPC 包管理器，花了七年时间学习当你将依赖隐式处理时会发生什么。

Before Spack v1.0, compilers were a special "node attribute" rather than actual nodes in the dependency graph. You configured them in compilers.yaml as external tools. Every package carried a compiler annotation, but compilers weren't dependencies in any meaningful sense.

在 Spack v1.0 之前，编译器是依赖图中的特殊"节点属性"，而不是实际的节点。你在 compilers.yaml 中将它们配置为外部工具。每个包都带有编译器注释，但编译器在任何有意义的层面上都不是依赖。

Compiler runtime libraries like gcc-runtime (libgcc, libstdc++) were invisible. If you needed clang for C but gfortran for Fortran, the monolithic compiler attribute couldn't express that. Build tools like cmake inherited the same exotic compiler as your main software even when they could have used a standard one. And if a Fortran compiler was missing, you'd find out deep in the dependency tree at build time rather than upfront during resolution.

编译器运行时库如 gcc-runtime（libgcc、libstdc++）是不可见的。如果你需要 clang 编译 C 但需要 gfortran 编译 Fortran，这个单体式编译器属性无法表达这一点。像 cmake 这样的构建工具继承了与主软件相同的特殊编译器，即使它们本可以使用标准编译器。而如果缺少 Fortran 编译器，你会在构建时深入依赖树才发现，而不是在解析时提前发现。

The idea to fix this was filed in 2016. The motivation came from a debugging story: a sysadmin installed a large dependency graph, gfortran was missing, openmpi built without Fortran support, and then hypre failed much later. If packages declared language dependencies, resolution itself would have caught the missing compiler before anything started building.

修复这个问题的想法在 2016 年提出。动机来自一个调试故事：一个系统管理员安装了一个大型依赖图，gfortran 缺失，openmpi 在没有 Fortran 支持的情况下构建，然后 hypre 在很久之后失败。如果包声明了语言依赖，解析器本身会在开始构建之前捕获缺失的编译器。

It took until March 2025 for PR #45189 ("Turn compilers into nodes") to merge. In Spack v1.0, languages like c, cxx, and fortran are virtual packages. Compilers are providers of those virtuals. A package declares `depends_on("c")` and `depends_on("cxx")`, and the resolver finds a compiler that satisfies both. The DAG now shows gcc injecting gcc-runtime as a visible runtime dependency, and the compiler wrapper is an explicit node included in the hash. The whole journey spanned dozens of intermediate issues, a FOSDEM 2018 talk, and a complete rethinking of how Spack's concretizer works.

直到 2025 年 3 月，PR #45189（"将编译器转换为节点"）才合并。在 Spack v1.0 中，c、cxx 和 fortran 等语言是虚拟包。编译器是这些虚拟包的提供者。包声明 `depends_on("c")` 和 `depends_on("cxx")`，解析器找到一个同时满足两者的编译器。现在 DAG 显示 gcc 将 gcc-runtime 注入为可见的运行时依赖，编译器包装器是哈希中包含的显式节点。整个过程跨越了几十个中间问题、2018 年 FOSDEM 的一次演讲，以及对 Spack 具体化器工作原理的完全重新思考。

Nix has always treated the compiler as a hashed dependency. Every derivation gets its build tools through stdenv, and the compiler toolchain is a content-addressed derivation like anything else. Bazel does something similar with hermetic toolchains. conda-forge uses compiler('c') in recipe metadata, which expands to platform-specific compiler packages. But even Nix stops at the same boundary, with the runtime, compiler, and glibc as content-addressed nodes while the specifications those tools implement remain outside the graph entirely.

Nix 一直将编译器视为哈希依赖。每个派生通过 stdenv 获取构建工具，编译器工具链像其他任何东西一样是一个内容寻址的派生。Bazel 对其密封工具链做类似的事情。conda-forge 在配方元数据中使用 compiler('c')，它会扩展为平台特定的编译器包。但即使是 Nix 也在同一边界停止，运行时、编译器和 glibc 是内容寻址节点，而这些工具实现的规范完全留在图外。

## Spec transitions

## 规范过渡

What happens at that boundary, when a spec changes and the implementations have to follow? The results are rarely clean.

当规范改变而实现必须跟随时，在这个边界会发生什么？结果很少是干净的。

When Chrome and Firefox enabled TLS 1.3 for testing in February 2017, failure rates were unexpectedly high. Chrome-to-Gmail connections succeeded 98.3% of the time with TLS 1.2 but only 92.3% with TLS 1.3. The culprit was middleboxes: corporate proxies and firewalls that had hardcoded expectations about TLS handshake fields. The TLS spec always allowed those fields to change, but because they had been stable for so long, middlebox developers treated them as constants.

2017 年 2 月，当 Chrome 和 Firefox 启用 TLS 1.3 进行测试时，失败率高得令人意外。Chrome 到 Gmail 的连接使用 TLS 1.2 时成功率 98.3%，但使用 TLS 1.3 时只有 92.3%。罪魁祸首是中端设备：对 TLS 握手字段有硬编码预期的企业代理和防火墙。TLS 规范一直允许这些字段改变，但因为它们稳定了很长时间，中端设备开发者将它们视为常量。

TLS 1.3 now lies about its own version. The ClientHello claims to be TLS 1.2, includes dummy session_id and ChangeCipherSpec fields that TLS 1.3 doesn't need, and uses a supported_versions extension to negotiate the real protocol. Separately, GREASE (Generate Random Extensions And Sustain Extensibility, RFC 8701) has implementations advertise reserved IANA values for cipher suites, extensions, and other fields, training middleboxes to tolerate unknown values rather than ossifying around a fixed set. A spec had to disguise itself as an older版本 of itself because the ecosystem had ossified around implicit assumptions about the previous version.

TLS 1.3 现在对自己的版本撒谎。ClientHello 声称是 TLS 1.2，包含 TLS 1.3 不需要的虚拟 session_id 和 ChangeCipherSpec 字段，并使用 supported_versions 扩展来协商真正的协议。另外，GREASE（生成随机扩展并保持可扩展性，RFC 8701）让实现为密码套件、扩展和其他字段宣传保留的 IANA 值，训练中端设备容忍未知值而不是固化在固定集合上。一个规范不得不伪装成自己的旧版本，因为生态系统已经围绕对前一版本的隐式假设而固化了。

Unicode releases new versions roughly annually, and each version can change character properties for existing characters, not just add new ones. When Chrome updated its ICU data, the wrestler and handshake emoji lost their Emoji_Base classification, causing emoji with skin tone modifiers to visually split into a base character and an orphaned modifier. Most software has no way to declare "I depend on Unicode 14.0 character properties." The Unicode version is baked into whatever runtime you happen to be using, and it changes when you update your JDK or system ICU library. Breakage happens not because developers chose to upgrade the spec, but because they upgraded something else and the spec came along for the ride.

Unicode 大约每年发布新版本，每个版本都可以改变现有字符的属性，而不仅仅是添加新字符。当 Chrome 更新其 ICU 数据时，摔跤和握手表情符号失去了它们的 Emoji_Base 分类，导致带有肤色修饰符的表情符号在视觉上分裂为基础字符和孤立的修饰符。大多数软件无法声明"我依赖 Unicode 14.0 字符属性"。Unicode 版本嵌入在你碰巧使用的任何运行时中，当你更新 JDK 或系统 ICU 库时它会改变。破坏发生不是因为开发者选择升级规范，而是因为他们升级了其他东西而规范随之而来。

PyPI classifiers let packages declare `Programming Language :: Python :: 3`, and Brett Cannon built caniusepython3 to analyze dependency树并报告哪些包阻塞了 Python 2 到 3 的迁移。但分类器是可选的，经常是错误的。如果 python_requires 从一开始就是强制性的且机器可执行的，pip 本可以自动拒绝安装不兼容的包。Python 3 耻辱墙在 2011 年 2 月推出，显示在其发布两年多后，前 200 个包中只有 9% 支持 Python 3。Guido van Rossum 后来称这个过渡是一个错误，不是因为 Python 3 错了，而是因为核心团队低估了存在多少 Python 2 代码。

PyPI 分类器让包声明 `Programming Language :: Python :: 3`，Brett Cannon 构建了 caniusepython3 来分析依赖树并报告哪些包阻塞了 Python 2 到 3 的迁移。但分类器是可选的，经常是错误的。如果 python_requires 从一开始就是强制性的且机器可执行的，pip 本可以自动拒绝安装不兼容的包。Python 3 耻辱墙在 2011 年 2 月推出，显示在其发布两年多后，前 200 个包中只有 9% 支持 Python 3。Guido van Rossum 后来称这个过渡是一个错误，不是因为 Python 3 错了，而是因为核心团队低估了存在多少 Python 2 代码。

CommonJS and ES Modules in Node.js are two incompatible module specs: ESM can import CJS, but CJS cannot `require()` ESM because ESM loads asynchronously and supports top-level await. If package.json had required declaring module system compatibility from the start, npm could have flagged incompatibilities at install time instead of leaving developers to discover them at runtime.

Node.js 中的 CommonJS 和 ES 模块是两个不兼容的模块规范：ESM 可以导入 CJS，但 CJS 无法 `require()` ESM，因为 ESM 异步加载并支持顶级 await。如果 package.json 从一开始就需要声明模块系统兼容性，npm 本可以在安装时标记不兼容性，而不是让开发者在运行时发现。

SMTP's transition to ESMTP negotiates at the protocol level: clients send EHLO instead of HELO, and if the server doesn't understand it, they fall back. The server's response lists supported extensions, essentially runtime dependency resolution for protocol capabilities. HTTP/1.1 to HTTP/2 used similar ALPN negotiation.

SMTP 向 ESMTP 的过渡在协议级别协商：客户端发送 EHLO 而不是 HELO，如果服务器不理解，它们就回退。服务器的响应列出支持的扩展，本质上是对协议能力的运行时依赖解析。HTTP/1.1 到 HTTP/2 使用了类似的 ALPN 协商。

## Executable specs

## 可执行规范

Web Platform Tests has over 56,000 tests and 1.8 million subtests, each mapped to a specific section of a W3C or WHATWG specification. The WPT Dashboard shows which browser engines pass which tests. TC39's Test262 does the same for ECMAScript. When a browser team says "we implement CSS Grid Level 1," what they mean in practice is that they pass a specific set of WPT tests.

Web Platform Tests 有超过 56,000 个测试和 180 万个子测试，每个都映射到 W3C 或 WHATWG 规范的特定部分。WPT 仪表板显示哪些浏览器引擎通过哪些测试。TC39 的 Test262 对 ECMAScript 做同样的事情。当浏览器团队说"我们实现了 CSS Grid Level 1"时，他们实际上的意思是他们通过了一组特定的 WPT 测试。

These test suites are closer to something you could declare as a dependency than any prose RFC. They're versioned, concrete artifacts with commit hashes. If you wanted a PURL-like identifier for spec dependencies, the test suite version might be more useful than the spec document version: `pkg:spec/w3c/wpt-css-grid@sha256:abc123` pins actual behavior, while `pkg:spec/w3c/css-grid@level-1` pins intent. They don't always agree, and they don't always change at the same time. A browser can pass all current WPT tests for a spec while the spec itself is still being revised, or a spec can be finalized while the test suite lags behind. When they diverge, you get a new class of version mismatch beyond the usual "pinned vs. unpinned" problem: did your package depend on what the spec said, or on what the test suite checked? A library might conform to the prose spec but fail the test suite because the tests encode a stricter interpretation, or pass every test while relying on behaviour the spec committee is about to remove. Tracking spec dependencies would need to account for both, and for the fact that they drift independently.

这些测试套件比任何散文式 RFC 更接近你可以声明为依赖的东西。它们是有提交哈希的版本化具体制品。如果你想要规范依赖的类似 PURL 的标识符，测试套件版本可能比规范文档版本更有用：`pkg:spec/w3c/wpt-css-grid@sha256:abc123` 固定实际行为，而 `pkg:spec/w3c/css-grid@level-1` 固定意图。它们并不总是一致，也不总是同时改变。浏览器可以通过规范的所有当前 WPT 测试，而规范本身仍在修订中，或者规范可以最终确定而测试套件落后。当它们分歧时，你会得到一类新的版本不匹配，超越了通常的"固定 vs 未固定"问题：你的包依赖的是规范所说的，还是测试套件检查的？一个库可能符合散文式规范但未能通过测试套件，因为测试编码了更严格的解释，或者通过每个测试却依赖于规范委员会即将删除的行为。跟踪规范依赖需要考虑两者，以及它们独立漂移的事实。

Most specs have no conformance suite at all, though. IETF RFCs rarely ship with official tests. Where tests exist, they tend to emerge from interoperability testing during standardization and然后无人维护。大多数软件的依赖链仍然是 包 -> 实现 -> 对散文文档的隐式理解，中间没有机器可读的契约。

大多数规范根本没有一致性测试套件。IETF RFC 很少附带官方测试。在存在测试的地方，它们往往从标准化期间的互操作性测试中出现，然后无人维护。大多数软件的依赖链仍然是 包 -> 实现 -> 对散文文档的隐式理解，中间没有机器可读的契约。

TypeScript's DefinitelyTyped ecosystem already does something like this for runtime APIs. @types/node describes what the Node.js runtime provides as a versioned npm package with its own semver, tracked in lockfiles and resolved by the same dependency machinery as any other package, but it declares the shape of an API without providing it. They version independently from the runtime they describe, so @types/node@20 might not match the actual Node 20 API surface perfectly, and the mismatch only surfaces when someone notices. Developers voluntarily创建和维护这些制品，因为工具奖励它，这表明规范即包的主要障碍不是意愿而是基础设施。

TypeScript 的 DefinitelyTyped 生态系统已经对运行时 API 做了类似的事情。@types/node 描述 Node.js 运行时提供的内容作为一个带自己语义化版本的版本化 npm 包，在锁文件中跟踪并由与其他任何包相同的依赖机制解析，但它声明 API 的形状而不提供它。它们独立于它们描述的运行时进行版本控制，所以 @types/node@20 可能不完全匹配实际的 Node 20 API 表面，不匹配只在有人注意到时才浮现。开发者自愿创建和维护这些制品，因为工具奖励它，这表明规范即包的主要障碍不是意愿而是基础设施。

## De facto specifications

## 事实规范

Not all specifications live in standards bodies. Node.js module resolution has no formal spec; it's defined by Node's behavior, and anything that resolves modules the same way is depending on that behavior whether or not anyone writes it down.

并非所有规范都存在于标准机构中。Node.js 模块解析没有正式规范；它由 Node 的行为定义，任何以相同方式解析模块的东西都依赖于该行为，无论是否有人将其写下。

Oracle donated Java EE to the Eclipse Foundation but retained the Java trademark, which prevented the Eclipse Foundation from modifying the javax namespace. The compromise was renaming every package from `javax.*` to `jakarta.*` in Jakarta EE 9, keeping the APIs identical under different names. Every application, library, and framework that imported `javax.servlet` or `javax.persistence` broke. Tools like OpenRewrite automated the rename, but it remains one of the most disruptive compatibility events in Java's history, caused entirely by a trademark dispute rather than any technical change. If Java EE's spec dependency had been an explicit, versioned node in the graph, the scope of the breakage would at least have been visible before the rename happened.

Oracle 将 Java EE 捐赠给 Eclipse 基金会，但保留了 Java 商标，这阻止了 Eclipse 基金会修改 javax 命名空间。妥协是在 Jakarta EE 9 中将每个包从 `javax.*` 重命名为 `jakarta.*`，在不同名称下保持 API 相同。每个导入 `javax.servlet` 或 `javax.persistence` 的应用程序、库和框架都崩溃了。像 OpenRewrite 这样的工具自动化了重命名，但它仍然是 Java 历史上最具破坏性的兼容性事件之一，完全由商标争议引起而非任何技术变更。如果 Java EE 的规范依赖在图中是一个显式的版本化节点，破坏的范围至少会在重命名发生前可见。

## Spec-to-spec dependencies

## 规范到规范的依赖

Specifications have their own dependency graphs. JSON relies on UTF-8 and through it on Unicode. HTTP sits on TLS, which sits on X.509 and ASN.1, so a breaking change to ASN.1 encoding would ripple through TLS implementations into HTTP libraries and from there into everything that makes network requests. CSS Grid builds on the Box Model and Visual Formatting contexts.

规范有自己的依赖图。JSON 依赖 UTF-8，并通过它依赖 Unicode。HTTP 建立在 TLS 之上，TLS 建立在 X.509 和 ASN.1 之上，所以对 ASN.1 编码的破坏性改变会波及 TLS 实现，进入 HTTP 库，再进入所有进行网络请求的东西。CSS Grid 建立在盒模型和视觉格式化上下文之上。

The rfcdeps tool graphs these relationships by parsing the "obsoletes" and "updates" headers from the RFC Editor's XML index, but it has no way to connect the spec graph to the software dependency graph, and nobody seems to have tried.

rfcdeps 工具通过解析 RFC 编辑器 XML 索引中的"废弃"和"更新"头来绘制这些关系，但它无法将规范图连接到软件依赖图，而且似乎没有人尝试过。

## Naming

## 命名

Package management is naming, and the naming problem for specifications is worse than for packages.

包管理就是命名，而规范的命名问题比包更严重。

The IETF uses sequential numbers where a new version of a spec gets a new number entirely. RFC 9110 obsoletes RFC 7231, which obsoleted RFC 2616. If you want to reference "HTTP semantics," you need to pick which RFC number, and that choice encodes a point in time rather than a version range. W3C uses levels for CSS (CSS Grid Level 1, Level 2), numbered versions for older specs (HTML 4.01), and maturity stages (Working Draft, Candidate Recommendation, Recommendation). WHATWG abandoned versioning entirely; HTML is a "Living Standard" with no version number and no snapshots. ECMA uses both edition numbers and year names (ECMA-262 6th Edition is also ES2015). ISO uses structured identifiers with amendment and corrigenda layers (ISO/IEC 5962:2021). IEEE uses base number plus year (IEEE 754-2019).

IETF 使用顺序编号，规范的新版本获得一个全新的编号。RFC 9110 废弃了 RFC 7231，后者废弃了 RFC 2616。如果你想引用"HTTP 语义"，你需要选择哪个 RFC 编号，这个选择编码了一个时间点而不是版本范围。W3C 对 CSS 使用级别（CSS Grid Level 1、Level 2），对旧规范使用编号版本（HTML 4.01），以及成熟度阶段（工作草案、候选推荐、推荐）。WHATWG 完全放弃了版本控制；HTML 是一个"活标准"，没有版本号，没有快照。ECMA 同时使用版本号和年份名称（ECMA-262 第 6 版也是 ES2015）。ISO 使用带修订和勘误层的结构化标识符（ISO/IEC 5962:2021）。IEEE 使用基础编号加年份（IEEE 754-2019）。

An Internet-Draft (draft-claise-semver-02) proposed applying semver to IETF specifications, giving RFCs the same kind of machine-comparable version identifiers that packages use, but it expired without adoption. The barriers weren't really technical; standards bodies have versioned things their own way for decades, and the conventions are embedded in their工具、引用实践和组织流程中。让 IETF、W3C、WHATWG、ECMA、ISO 和 IEEE 同意一个共同的版本控制方案是一个比让包管理器同意锁文件格式更难的协调问题。

一份互联网草案（draft-claise-semver-02）提议将语义化版本应用于 IETF 规范，给 RFC 与包使用的相同类型的机器可比版本标识符，但它在没有被采纳的情况下过期了。障碍实际上不是技术性的；标准机构几十年来一直以自己的方式对事物进行版本控制，这些惯例嵌入在他们的工具、引用实践和组织流程中。让 IETF、W3C、WHATWG、ECMA、ISO 和 IEEE 同意一个共同的版本控制方案是一个比让包管理器同意锁文件格式更难的协调问题。

If you wanted a PURL-like scheme for specifications, something like `pkg:spec/ietf/rfc9110@2022`, you'd need to normalize across all of these conventions. PURL already handles per-ecosystem naming differences for packages, so the approach isn't unprecedented, but someone would need to define the type mappings and get buy-in from communities that see no reason to change. PURL itself is now a spec (ECMA-427), so the identifier scheme for tracking spec dependencies would itself be a spec dependency that needs tracking.

如果你想要规范的类似 PURL 的方案，比如 `pkg:spec/ietf/rfc9110@2022`，你需要在所有这些惯例中进行规范化。PURL 已经处理了包的每个生态系统命名差异，所以这种方法并非前所未有，但需要有人定义类型映射，并从看不到改变理由的社区获得认同。PURL 本身现在是一个规范（ECMA-427），所以跟踪规范依赖的标识符方案本身也将是一个需要跟踪的规范依赖。

The NVD's CPE (Common Platform Enumeration) identifiers already name specifications in a limited way, as Jean-Baptiste Maillet pointed out: `cpe:2.3:a:ietf:ipv6` appears in IPv6-related CVEs, and `cpe:2.3:a:bluetooth:bluetooth_core_specification` covers versions 1.1b through 5.2 of the Bluetooth spec, because when a vulnerability lives in the specification rather than any single implementation, the security database needs some way to say so. CPE's vendor/product naming is too coarse and ad hoc for package metadata, but it's interesting that vulnerability tracking arrived at a version of this problem before package management did.

NVD 的 CPE（通用平台枚举）标识符已经在有限程度上命名了规范，正如 Jean-Baptiste Maillet 指出的：`cpe:2.3:a:ietf:ipv6` 出现在与 IPv6 相关的 CVE 中，`cpe:2.3:a:bluetooth:bluetooth_core_specification` 覆盖了蓝牙规范 1.1b 到 5.2 版本，因为当漏洞存在于规范中而非任何单个实现中时，安全数据库需要某种方式来说明。CPE 的供应商/产品命名对于包元数据来说太粗糙和临时，但有趣的是漏洞跟踪在包管理之前就遇到了这个问题的一个版本。

Making specs explicit doesn't require solving the whole problem at once. Some of the data model already exists: SPDX 3.0 includes a hasSpecification relationship type linking software elements to specifications, and CycloneDX 1.6 introduced "definitions" for standards and "declarations" for conformance attestation. But no package manager reads any of this, and no SBOM generator populates it automatically. A spec field in package metadata, even if it were just a list of RFC numbers or W3C 短名，也会让工具能够回答目前不可能的问题：哪些包实现了 RFC 9110，有多少依赖 Unicode 15 字符属性，你的哪些依赖仍然实现 TLS 1.2 并需要迁移。目前，在软件供应链中不可见的规范作者将获得与帮助证明开源库资助合理性相同的传递依赖计数。主权技术机构资助 curl 和 OpenSSL 等协议实现，并正在开始探索直接支持标准工作，但还没有人能指出一个数字说此 RFC 有 40 万个传递依赖。

让规范显式化不需要一次性解决整个问题。一些数据模型已经存在：SPDX 3.0 包含一个 hasSpecification 关系类型，将软件元素链接到规范，CycloneDX 1.6 引入了标准的"定义"和一致性证明的"声明"。但没有包管理器读取这些，也没有 SBOM 生成器自动填充它。包元数据中的规范字段，即使只是 RFC 编号列表或 W3C 短名，也会让工具能够回答目前不可能的问题：哪些包实现了 RFC 9110，有多少依赖 Unicode 15 字符属性，你的哪些依赖仍然实现 TLS 1.2 并需要迁移。目前，在软件供应链中不可见的规范作者将获得与帮助证明开源库资助合理性相同的传递依赖计数。主权技术机构资助 curl 和 OpenSSL 等协议实现，并正在开始探索直接支持标准工作，但还没有人能指出一个数字说此 RFC 有 40 万个传递依赖。

---

## 批判性思考

这篇文章深刻揭示了软件依赖管理中一个长期被忽视的"隐形层"——规范依赖。作者通过丰富的案例展示了一个令人不安的现实：我们的软件基础设施建立在一层层隐含的假设之上，而这些假设从未被显式声明或跟踪。

**核心洞察：**

1. **规范即隐式依赖**：从 Ruby 版本要求到 TLS 实现，从 JSON 解析到 Unicode 字符属性，软件无时无刻不在依赖各种规范，但这些依赖在现有的包管理系统中完全不可见。这是一个根本性的缺口。

2. **Spack 的教训极具启发性**：花费七年时间才将编译器从"节点属性"转变为真正的依赖节点，这提醒我们——看似简单的问题往往涉及深层架构变革。Spack 的经验表明，一旦规范被显式化，整个依赖解析、缓存、哈希计算都需要重新思考。

3. **TLS 1.3 的"谎言"令人警醒**：一个规范不得不伪装成自己的旧版本，因为生态系统已经"固化"（ossified）在对旧版本的隐含假设上。这揭示了一个悖论：规范本应是稳定和可预测的，但当它们真正演进时，却可能引发连锁故障。

4. **测试套件 vs 规范的分离**：文章提出的可执行规范概念很有前瞻性。WPT 和 Test262 等测试套件确实比散文式 RFC 更适合作为依赖对象，但测试与规范的漂移（一个通过了测试但规范正在改变，或规范已定但测试滞后）又引入了新的复杂性。

5. **命名的政治性**：不同标准机构（IETF、W3C、WHATWG、ECMA、ISO、IEEE）使用完全不同的版本控制方案，使得统一的规范标识符系统几乎不可能。这不仅是技术问题，更是组织文化和历史惯性的体现。

**批判性反思：**

- **现实的复杂性**：虽然作者呼吁让规范显式化，但文章也展示了这条路有多么艰难。规范之间存在复杂的依赖链（JSON → UTF-8 → Unicode），规范与实现之间存在漂移，测试套件与规范之间存在错位。

- **Nix 的边界**：有趣的是，即便是 Nix——以其极端的显式化和可重现性著称——也在规范面前止步。运行时、编译器、glibc 可以是内容寻址节点，但它们实现的规范却完全留在图外。这说明了什么？或许规范本质上是抽象的、多解释的，难以像软件包那样被"固定"。

- **CPE 的先行**：安全漏洞跟踪（NVD/CPE）比包管理更早意识到需要标识规范本身，因为当漏洞存在于规范而非实现时，必须有一种方式来表达。这暗示了安全需求可能是推动规范显式化的重要力量。

**结论**：这篇文章不仅是对现状的诊断，更是对未来的一种呼吁。SPDX 3.0 和 CycloneDX 1.6 已经迈出第一步，但真正的改变需要整个生态系统的协调。当我们开始问"此 RFC 有多少传递依赖者"时，我们才能更好地理解和资助软件基础设施的真正基础层。
