# Gwtar：一种静态高效的单文件 HTML 格式

**原文链接**: https://simonwillison.net/2026/Feb/15/gwtar/

**标签**: #WebArchive #HTML #HTTP-Range-Requests #Tar-Format #Browser-Security #JavaScript #Web-Performance

---

**2026年2月15日**

[Gwtar：一种静态高效的单文件 HTML 格式](https://gwern.net/gwtar)（[via](https://news.ycombinator.com/item?id=47024506)）

这是一个来自 Gwern Branwen 和 Said Achmiz 的引人入胜的新项目，它致力于解决将大量资源整合到单个存档 HTML 文件中、同时又不影响浏览器查看便利性的挑战。

它使用的核心技巧是在页面早期调用 [window.stop()](https://developer.mozilla.org/en-US/docs/Web/API/Window/stop) 来阻止浏览器下载整个文件，然后在该调用之后跟随内联的 tar 未压缩内容。

这样，当页面需要这些内容时，它可以通过 HTTP 范围请求（HTTP range requests）按需从 tar 数据中获取所需内容。

已经加载的 JavaScript 会将资源 URL 重写为指向 `https://localhost/`，纯粹是为了让它们加载失败。然后它使用 [PerformanceObserver](https://developer.mozilla.org/en-US/docs/Web/API/PerformanceObserver) 来捕获这些尝试加载的操作：

```javascript
let perfObserver = new PerformanceObserver((entryList, observer) => {
  resourceURLStringsHandler(entryList.getEntries().map(entry => entry.name));
});
perfObserver.observe({ entryTypes: [ "resource" ] });
```

`resourceURLStringsHandler` 回调函数会查找已加载的资源，如果没有则通过 HTTP 范围请求获取，然后使用 `blob:` URL 将资源插入到正确的位置。

如果你查看源代码，这就是文档中 `window.stop()` 部分的样子：

有趣的是，作为一种存档格式，如果你直接在自己的计算机上打开该文件，它实际上无法工作。如果你尝试这样做，你会看到以下内容：

> 你看到此消息，而不是应该看到的页面，是因为 gwtar 文件无法本地打开（由于 Web 浏览器的安全限制）。
>
> 要在你的计算机上打开此页面，请使用以下 shell 命令：
>
> ```bash
> perl -ne'print $_ if $x; $x=1 if /<!-- GWTAR END/' < foo.gwtar.html | tar --extract
> ```
>
> 然后在任何 Web 浏览器中打开 `foo.html` 文件。

---

## 技术原理详解

### 1. 核心机制

Gwtar 的核心创新在于**延迟加载（Lazy Loading）**与**存档格式的结合**。传统的单文件 HTML 存档（如 MHTML）需要浏览器下载整个文件才能显示内容，而 Gwtar 通过以下机制解决了这个问题：

- **提前截断**: 使用 `window.stop()` 立即停止浏览器解析后续内容
- **内联存档**: 将 tar 格式的未压缩资源附加在 HTML 之后
- **按需获取**: 通过 HTTP 范围请求仅加载当前需要的资源

### 2. HTTP 范围请求

HTTP 范围请求（Range Requests）是 HTTP/1.1 引入的功能，允许客户端请求资源的特定字节范围：

```
Range: bytes=0-1023
```

Gwtar 利用这一特性从 tar 存档中精确定位并提取单个资源，而无需下载整个文件。

### 3. Tar 格式优势

选择 tar 格式而非 zip 等压缩格式的原因：
- **未压缩存储**: 允许直接进行字节级范围寻址
- **简单结构**: 每个文件头部包含固定大小的元数据，便于计算偏移量
- **流式处理**: 无需解压整个存档即可访问内部文件

### 4. 本地文件限制

由于浏览器的同源策略（Same-Origin Policy）和文件协议（file://）的安全限制：
- 本地文件无法发起 HTTP 请求（即使是范围请求）
- `blob:` URL 在本地上下文中可能受到限制
- 因此需要通过本地服务器（localhost）或提取后查看

### 5. 性能优势

相比传统单文件存档方案：
| 方案 | 初始加载 | 随机访问 | 增量加载 |
|------|----------|----------|----------|
| 纯 HTML | 快 | N/A | N/A |
| MHTML | 慢（需全量） | 慢 | 不支持 |
| Gwtar | 快（仅 HTML） | 快（Range 请求） | 支持 |

---

## 总结

Gwtar 代表了一种新的 Web 存档思路：**将存档格式与 Web 原生技术（HTTP Range Requests、PerformanceObserver）相结合**，实现了大容量单文件存档的高效浏览体验。这对于需要离线分发的文档、电子书、技术手册等场景具有重要价值。

项目地址: https://gwern.net/gwtar
