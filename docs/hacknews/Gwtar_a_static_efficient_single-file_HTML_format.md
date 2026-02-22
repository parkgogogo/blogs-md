URL: https://simonwillison.net/2026/Feb/15/gwtar/
**原文链接**: https://simonwillison.net/2026/Feb/15/gwtar/

---

[Gwtar: a static efficient single-file HTML format](https://gwern.net/gwtar) ([via](https://news.ycombinator.com/item?id=47024506))
[Gwtar：一种静态高效的单文件 HTML 格式](https://gwern.net/gwtar)（[via](https://news.ycombinator.com/item?id=47024506)）

Fascinating new project from Gwern Branwen and Said Achmiz that targets the challenge of combining large numbers of assets into a single archived HTML file without that file being inconvenient to view in a browser.

这是一个来自 Gwern Branwen 和 Said Achmiz 的引人入胜的新项目，它致力于解决将大量资源整合到单个存档 HTML 文件中、同时又不影响浏览器查看便利性的挑战。

The key trick it uses is to fire [window.stop()](https://developer.mozilla.org/en-US/docs/Web/API/Window/stop) early in the page to prevent the browser from downloading the whole thing, then following that call with inline tar uncompressed content.

它使用的核心技巧是在页面早期调用 [window.stop()](https://developer.mozilla.org/en-US/docs/Web/API/Window/stop) 来阻止浏览器下载整个文件，然后在该调用之后跟随内联的 tar 未压缩内容。

It can then make HTTP range requests to fetch content from that tar data on-demand when it is needed by the page.

这样，当页面需要这些内容时，它可以通过 HTTP 范围请求（HTTP range requests）按需从 tar 数据中获取所需内容。

The JavaScript that has already loaded rewrites asset URLs to point to `https://localhost/` purely so that they will fail to load.

已经加载的 JavaScript 会将资源 URL 重写为指向 `https://localhost/`，纯粹是为了让它们加载失败。

Then it uses a [PerformanceObserver](https://developer.mozilla.org/en-US/docs/Web/API/PerformanceObserver) to catch those attempted loads:
然后它使用 [PerformanceObserver](https://developer.mozilla.org/en-US/docs/Web/API/PerformanceObserver) 来捕获这些尝试加载的操作：

```javascript
let perfObserver = new PerformanceObserver((entryList, observer) => {
    resourceURLStringsHandler(entryList.getEntries().map(entry => entry.name));
});
perfObserver.observe({ entryTypes: [ "resource" ] });
```

That `resourceURLStringsHandler` callback finds the resource if it is already loaded or fetches it with an HTTP range request otherwise and then inserts the resource in the right place using a `blob:` URL.

`resourceURLStringsHandler` 回调函数会查找已加载的资源，如果没有则通过 HTTP 范围请求获取，然后使用 `blob:` URL 将资源插入到正确的位置。

Here's what the `window.stop()` portion of the document looks like if you view the source:

如果你查看源代码，这就是文档中 `window.stop()` 部分的样子：

```html
<script>
// ... header JS ...
</script>
<!-- GWTAR END -->
```

Amusingly for an archive format it doesn't actually work if you open the file directly on your own computer.

有趣的是，作为一种存档格式，如果你直接在自己的计算机上打开该文件，它实际上无法工作。

Here's what you see if you try to do that:

如果你尝试这样做，你会看到以下内容：

> You are seeing this message, instead of the page you should be seeing, because gwtar files cannot be opened locally (due to web browser security restrictions).
> 你看到此消息，而不是应该看到的页面，是因为 gwtar 文件无法本地打开（由于 Web 浏览器的安全限制）。

> To open this page on your computer, use the following shell command:
> 要在你的计算机上打开此页面，请使用以下 shell 命令：

> ```bash
> perl -ne'print $_ if $x; $x=1 if /<!-- GWTAR END/' < foo.gwtar.html | tar --extract
> ```

> Then open the file `foo.html` in any web browser.
> 然后在任何 Web 浏览器中打开 `foo.html` 文件。

---

## Technical Deep Dive / 技术原理详解

### The Core Mechanism / 核心机制

Gwtar's core innovation lies in the combination of **lazy loading** with **archive format**.

Gwtar 的核心创新在于**延迟加载（Lazy Loading）**与**存档格式的结合**。

Traditional single-file HTML archives (like MHTML) require the browser to download the entire file before displaying content, but Gwtar solves this through the following mechanisms:

传统的单文件 HTML 存档（如 MHTML）需要浏览器下载整个文件才能显示内容，而 Gwtar 通过以下机制解决了这个问题：

- **Early truncation**: Uses `window.stop()` to immediately stop the browser from parsing subsequent content

- **提前截断**: 使用 `window.stop()` 立即停止浏览器解析后续内容

- **Inline archive**: Appends tar-format uncompressed resources after the HTML

- **内联存档**: 将 tar 格式的未压缩资源附加在 HTML 之后

- **On-demand fetching**: Uses HTTP range requests to load only currently needed resources

- **按需获取**: 通过 HTTP 范围请求仅加载当前需要的资源

### HTTP Range Requests / HTTP 范围请求

HTTP Range Requests are a feature introduced in HTTP/1.1 that allows clients to request specific byte ranges of a resource:

HTTP 范围请求（Range Requests）是 HTTP/1.1 引入的功能，允许客户端请求资源的特定字节范围：

```
Range: bytes=0-1023
```

Gwtar leverages this feature to precisely locate and extract individual resources from the tar archive without downloading the entire file.

Gwtar 利用这一特性从 tar 存档中精确定位并提取单个资源，而无需下载整个文件。

### Why Tar Format? / 为什么选择 Tar 格式？

The reasons for choosing tar format over compressed formats like zip:

选择 tar 格式而非 zip 等压缩格式的原因：

- **Uncompressed storage**: Allows direct byte-level range addressing

- **未压缩存储**: 允许直接进行字节级范围寻址

- **Simple structure**: Each file header contains fixed-size metadata, making offset calculation easy

- **简单结构**: 每个文件头部包含固定大小的元数据，便于计算偏移量

- **Stream processing**: Access internal files without decompressing the entire archive

- **流式处理**: 无需解压整个存档即可访问内部文件

### Local File Limitations / 本地文件限制

Due to browser same-origin policy and file protocol (`file://`) security restrictions:

由于浏览器的同源策略（Same-Origin Policy）和文件协议（file://）的安全限制：

- Local files cannot initiate HTTP requests (even range requests)

- 本地文件无法发起 HTTP 请求（即使是范围请求）

- `blob:` URLs may be restricted in local contexts

- `blob:` URL 在本地上下文中可能受到限制

- Therefore, local server (localhost) or extraction is required for viewing

- 因此需要通过本地服务器（localhost）或提取后查看

### Performance Comparison / 性能对比

Compared to traditional single-file archive solutions:

相比传统单文件存档方案：

| Approach | Initial Load | Random Access | Incremental Loading |
|----------|--------------|---------------|---------------------|
| Plain HTML | Fast | N/A | N/A |
| MHTML | Slow (full download) | Slow | Not supported |
| Gwtar | Fast (HTML only) | Fast (Range requests) | Supported |

| 方案 | 初始加载 | 随机访问 | 增量加载 |
|------|----------|----------|----------|
| 纯 HTML | 快 | N/A | N/A |

| MHTML | 慢（需全量） | 慢 | 不支持 |

| Gwtar | 快（仅 HTML） | 快（Range 请求） | 支持 |

---

## Summary / 总结

Gwtar represents a new approach to web archiving: **combining archive formats with web-native technologies (HTTP Range Requests, PerformanceObserver)** to achieve efficient browsing experience for large-capacity single-file archives.

Gwtar 代表了一种新的 Web 存档思路：**将存档格式与 Web 原生技术（HTTP Range Requests、PerformanceObserver）相结合**，实现了大容量单文件存档的高效浏览体验。

This has significant value for scenarios requiring offline distribution of documents, e-books, technical manuals, etc.

这对于需要离线分发的文档、电子书、技术手册等场景具有重要价值。

Project URL: https://gwern.net/gwtar
项目地址: https://gwern.net/gwtar

---

## Critical Thinking Commentary / 批判性思考评论

### Analysis of the Author's Main Arguments / 作者主要论点分析

The authors (Gwern Branwen and Said Achmiz) present Gwtar as a solution to what they call the "HTML Trilemma" — the impossibility of achieving static, single-file, and efficient archives simultaneously with existing formats.

作者（Gwern Branwen 和 Said Achmiz）将 Gwtar 呈现为解决所谓"HTML 三难困境"的方案——即现有格式无法同时实现静态、单文件和高效存档的不可能性。

Their core argument is compelling: traditional approaches force trade-offs between these three desirable properties, and Gwtar's innovative use of `window.stop()` combined with HTTP range requests provides a clever workaround that satisfies all three constraints.

他们的核心论点很有说服力：传统方法迫使我们在三个理想属性之间做出权衡，而 Gwtar 创新性地使用 `window.stop()` 结合 HTTP 范围请求提供了一个巧妙的解决方案，满足了所有三个约束条件。

### Strengths / 优点

1. **Technical ingenuity**: The `window.stop()` trick is genuinely clever. Using a browser API designed for stopping page loads to create a "tarball-like" partial random access archive is an elegant hack that exploits standard browser behavior in an unexpected way.

   **技术巧妙性**: `window.stop()` 技巧确实非常聪明。利用一个用于停止页面加载的浏览器 API 来创建类似 tar 的部分随机访问存档，是一种以意想不到的方式利用标准浏览器行为的优雅技巧。

2. **Standards compliance**: Gwtar relies entirely on standardized web technologies (HTTP Range Requests, PerformanceObserver, Blob URLs) that have been supported for years. This means forwards compatibility without requiring special software.

   **标准兼容性**: Gwtar 完全依赖于标准化的 Web 技术（HTTP 范围请求、PerformanceObserver、Blob URL），这些技术已经支持多年。这意味着向前兼容，无需特殊软件。

3. **Self-documenting format**: The ability to extract content using simple shell commands (`perl` + `tar`) makes the format transparent and accessible, unlike proprietary formats that require specific tools.

   **自文档化格式**: 能够使用简单的 shell 命令（`perl` + `tar`）提取内容，使该格式透明且易于访问，不像需要特定工具的专有格式。

4. **FEC support**: The built-in support for forward error correction (PAR2) shows thoughtful consideration for long-term archival durability.

   **FEC 支持**: 对前向纠错（PAR2）的内置支持表明了对长期存档耐久性的深思熟虑。

### Weaknesses / 缺点

1. **Local viewing limitations**: The fact that Gwtar files cannot be opened locally is a significant usability drawback. Users expect archive files to work when double-clicked. The workaround (running a Perl command) is technical and inaccessible to average users.

   **本地查看限制**: Gwtar 文件无法在本地打开这一事实是一个重大的可用性缺陷。用户期望存档文件在双击时就能工作。解决方法（运行 Perl 命令）技术要求高，普通用户难以操作。

2. **JavaScript dependency**: While the authors dismiss this as acceptable for their use case, requiring JavaScript for basic functionality contradicts the principles of progressive enhancement and excludes users who disable JavaScript for security or accessibility reasons.

   **JavaScript 依赖**: 虽然作者认为这对他们的用例来说可以接受，但需要 JavaScript 来实现基本功能违背了渐进增强的原则，并排除了出于安全或可访问性原因禁用 JavaScript 的用户。

3. **Cloudflare workarounds**: The need to use a custom MIME type (`x-gwtar`) to bypass Cloudflare's stripping of Range headers reveals how fragile the solution is in real-world CDN environments. This is a hack on top of a hack.

   **Cloudflare 变通方案**: 需要使用自定义 MIME 类型（`x-gwtar`）来绕过 Cloudflare 剥离 Range 标头的问题，揭示了该解决方案在真实 CDN 环境中的脆弱性。这是在一个技巧之上的另一个技巧。

4. **Compression limitations**: The unclear interaction between Range requests and transparent compression (gzip/Brotli) is acknowledged by the authors but remains unresolved. This could significantly impact performance in practice.

   **压缩限制**: 作者承认但尚未解决范围请求与透明压缩（gzip/Brotli）之间的不清晰交互问题。这可能在实际应用中显著影响性能。

### Personal Critical Perspective / 个人批判视角

While Gwtar is technically impressive, I question whether it solves the right problem in the right way. The fundamental issue is that web archiving has become unnecessarily complex because modern web development practices prioritize developer convenience over simplicity and longevity.

虽然 Gwtar 在技术层面令人印象深刻，但我质疑它是否以正确的方式解决了正确的问题。根本问题在于，由于现代 Web 开发实践优先考虑开发者便利性而非简单性和长期性，Web 存档变得不必要地复杂。

The fact that a 500MB archive is considered "normal" for a web page is itself a symptom of a broken ecosystem. Gwtar treats the symptom (large file sizes) rather than the disease (bloated web pages with unnecessary assets, fonts, and tracking scripts).

一个 500MB 的存档被认为是网页的"正常"大小，这本身就是破碎生态系统的一个症状。Gwtar 治疗的是症状（大文件大小）而非疾病（带有不必要资源、字体和跟踪脚本的臃肿网页）。

Furthermore, the approach of "exploiting browser APIs in unintended ways" while clever, creates technical debt. Browser vendors may change behavior in ways that break Gwtar, and the `window.stop()` trick relies on specific timing that could be fragile across different browsers or future updates.

此外，"以意想不到的方式利用浏览器 API" 的方法虽然聪明，但会产生技术债务。浏览器供应商可能会以破坏 Gwtar 的方式改变行为，而 `window.stop()` 技巧依赖于特定的时序，在不同浏览器或未来更新中可能很脆弱。

### Implications / 影响与启示

**For web archiving**: Gwtar demonstrates that there's still room for innovation in static archival formats. However, it also highlights how fundamentally broken the current web ecosystem is when such complex workarounds are needed.

**对于 Web 存档**: Gwtar 证明了静态存档格式仍有创新空间。然而，它也凸显了当前 Web 生态系统是多么根本性地破损，以至于需要如此复杂的变通方案。

**For preservation**: The format's reliance on JavaScript and specific browser behaviors raises concerns about long-term archival stability. True archival formats should be readable with minimal dependencies decades from now.

**对于保存**: 该格式对 JavaScript 和特定浏览器行为的依赖引发了关于长期存档稳定性的担忧。真正的存档格式应该能够在几十年后以最少的依赖可读。

**For developers**: Gwtar serves as a reminder that sometimes the "obvious" solution (in this case, server-side splitting) isn't always the best, and creative client-side solutions can solve problems without infrastructure changes. However, it also shows the cost of such creativity in terms of complexity and fragility.

**对于开发者**: Gwtar 提醒我们，有时"显而易见"的解决方案（在本例中是服务器端分割）并不总是最好的，创造性的客户端解决方案可以在不改变基础设施的情况下解决问题。然而，它也显示了这种创造力在复杂性和脆弱性方面的代价。

**For users**: The format highlights the tension between security (browser sandboxing, CORS restrictions) and usability. The inability to open archived content locally without technical workarounds is a regression in user experience, even if the underlying technical achievement is impressive.

**对于用户**: 该格式凸显了安全性（浏览器沙盒、CORS 限制）与可用性之间的张力。即使底层技术成就令人印象深刻，但无法在没有技术变通的情况下本地打开存档内容，这是用户体验的倒退。

In conclusion, Gwtar is a fascinating technical achievement that solves a real problem, but it also serves as a indictment of how far the web has strayed from the simplicity that made it successful in the first place. It's a clever solution to a problem that shouldn't exist.

总之，Gwtar 是一项令人着迷的技术成就，解决了一个真实的问题，但它也证明了 Web 已经偏离了最初使其成功的简单性有多远。这是一个针对不应该存在的问题的聪明解决方案。